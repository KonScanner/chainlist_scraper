from requests_toolbelt import threaded
import pandas as pd


def _get_urls_to_get(raw_urls: list) -> list:
    return [
        {
            "url": url,
            "method": "GET",
        }
        for url in raw_urls
    ]


def _core_logic(raw_urls: list) -> list:
    urls = _get_urls_to_get(raw_urls=raw_urls)
    data = []
    if not urls:
        return []
    responses_generator, _ = threaded.map(urls, num_processes=10)
    for response in responses_generator:
        r = response.response
        if r.status_code == 200:
            data.append(r.json()["pageProps"])
    return data


def get_data(raw_urls: list, default_ret_type="") -> pd.DataFrame:
    data = _core_logic(raw_urls=raw_urls)
    (
        full_name,
        chain_name,
        rpc_urls,
        faucets,
        currency_name,
        currency_symbol,
        currency_decimals,
        info_url,
        short_name,
        chain_id,
        network_id,
        explorers,
    ) = ([], [], [], [], [], [], [], [], [], [], [], [])

    for d in data:
        cl = d["chain"]
        full_name.append(cl.get("name", default_ret_type))
        chain_name.append(cl.get("chain", default_ret_type))
        rpc_urls.append(cl.get("rpc", default_ret_type))
        faucets.append(cl.get("faucets", default_ret_type))
        currency_name.append(cl.get("currency", {}).get("name", default_ret_type))
        currency_symbol.append(cl.get("currency", {}).get("symbol", default_ret_type))
        currency_decimals.append(
            cl.get("currency", {}).get("decimals", default_ret_type)
        )

        info_url.append(cl.get("infoURL", default_ret_type))
        short_name.append(cl.get("shortName", default_ret_type))
        chain_id.append(cl.get("chainId", default_ret_type))
        network_id.append(cl.get("networkId", default_ret_type))
        explorers.append(cl.get("explorers", default_ret_type))
    df = pd.DataFrame([])
    cols = [
        "full_name",
        "chain_name",
        "rpc_urls",
        "faucets",
        "currency_name",
        "currency_symbol",
        "currency_decimals",
        "info_url",
        "short_name",
        "chain_id",
        "network_id",
        "explorers",
    ]
    for column in cols:
        exec(f"df['{column}'] = {column}")

    def topic_like_hex(x):
        part1 = x.replace("0x","")
        part2 = 66 - x.__len__()
        return "0x" + "0" * part2 + part1
    
    # Extra columns
    df["hex_network_id"] = df["network_id"].apply(lambda x: str(hex(x)))
    df["topic_like_hex_network_id"] = df["hex_network_id"].apply(lambda x: topic_like_hex(x))
    return df
