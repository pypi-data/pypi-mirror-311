import pandas as pd
from langchain.agents import load_tools, initialize_agent
import ast

class search_engine:
    def __init__(self, model):
        tools = load_tools(["google-serper"])
        self.agent = initialize_agent(tools, model, agent="zero-shot-react-description", verbose=False)
        
    def assets(self, assets_array, prompt=None, max_retries=2):
        if prompt is None:
            self.search_asset_prompt = """
            Please look up the instrument %s with ISIN %s and provide the details in the following format:
            {
            'Asset class': 'Equity/Bond/Money Market/Alternatives/Other',
            'Currency': 'USD/EUR/Other',
            'Country': 'ISO code (e.g., US, FR)'
            'Market': 'emerging markets/developed markets/Other',
            'Rating': 'government bond/high yield/investment grade/Other'
            'Type': 'stock/bond/derivative/fund/other'
            }
            """
        else:
            self.search_asset_prompt = prompt

        items = []
        for item in assets_array:
            print(f"Searching {item['id']} with isin {item['isin']}")
            retries = 0
            success = False
            while retries < max_retries and not success:
                try:
                    response = self.agent.run(self.search_asset_prompt % (item['id'], item['isin']))
                    parsed_response = ast.literal_eval(response)
                    item = {
                        **{'Isin': item['isin'], 'Name': item['id']},
                        **parsed_response
                    }
                    success = True  # Mark as successful
                except Exception as e:
                    retries += 1
                    if retries >= max_retries:
                        item = {
                            'Isin': item['isin'],
                            'Name': item['id'],
                            'Asset class': '',
                            'Currency': '',
                            'Country': '',
                            'Market': '',
                            'Rating': '',
                            'Type': ''
                        }
                        print(f"Failed to identify instrument after {retries} retries: {str(e)}")
                    else:
                        print(f"Retrying ({retries}/{max_retries}) due to error: {str(e)}")

            items.append(item)
        
        return pd.DataFrame(items)