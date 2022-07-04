from src.chains import Chains
from src.reqest_data import get_data

if __name__ == "__main__":
    urls = Chains(headless=True).logic()
    data = get_data(raw_urls=urls)
    # TODO: Some logic to save the data
