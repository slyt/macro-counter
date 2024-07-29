
import requests
import json
import jmespath

# query_params = {
#     "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
#     "tcins": "84067786,13292010,84067787,12935716,13260927,84067789,12935827,12935775,13264003,13292613,13261183,13292554,12935652,50382871,84067788,12935771,14256016,86203814,86203810,15079780,21550208,15400825,14039583,13260978",
#     "store_id": "926",
#     "scheduled_delivery_store_id": "926",
#     "required_store_id": "926",
#     "skip_price_promo": "true",
#     "visitor_id": "018C30AC533702019CE9F6D48BA7C647",
#     "channel": "WEB",
#     "page": "/s/peanut butter"
# }

# headers = {
#     "authority": "redsky.target.com",
#     "method": "GET",
#     "scheme": "https",
#     "accept": "application/json",
#     "accept-encoding": "gzip, deflate, br, zstd",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
# }



# url = "https://redsky.target.com/redsky_aggregations/v1/web/product_summary_with_fulfillment_v1"

# response = requests.get(url, headers=headers, params=query_params)


# if response.status_code == 200:
#     data = response.json()
#     # pretty print json
    
#     print(json.dumps(data, indent=2))


#     # Neatly print each item and associated data
#     product_summaries = data.get("data", {}).get("product_summaries", [])
#     for i, product in enumerate(product_summaries):
#         print(f"Product {i+1}:")
#         title = jmespath.search("item.product_description.title", product)
#         buy_url = jmespath.search("item.enrichment.buy_url", product)
#         quantity = jmespath.search("fulfillment.store_options[*].location_available_to_promise_quantity", product)
#         store_positions = jmespath.search("store_positions", product)
#         price = jmespath.search("item.price.formatted_current_price", product)
#         print(f"  Price: {price}")
    

#         print(f"  Title: {title}")
#         print(f"  Buy URL: {buy_url}")
#         print(f"  Quantity: {quantity}")
#         print(f"  Store Positions: {store_positions}")
#         print("\n")

# else:
#     print(f"Request failed with status code {response.status_code}")
#     print(response.text)



# URL and parameters
# url = "https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2"
# params = {
#     "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
#     "channel": "WEB",
#     "count": "24",
#     "default_purchasability_filter": "true",
#     "include_dmc_dmr": "true",
#     "keyword": "peanut butter",
#     "new_search": "true",
#     "offset": "0",
#     "page": "/s/peanut butter",
#     "platform": "desktop",
#     "pricing_store_id": "926",
#     "scheduled_delivery_store_id": "926",
#     "spellcheck": "true",
#     "store_ids": "926,533,891,3374,860",
#     "useragent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#     "visitor_id": "018C30AC533702019CE9F6D48BA7C647",
#     "zip": "61241"
# }

# # Headers
# headers = {
#     "Referer": "https://www.target.com/s?searchTerm=peanut+butter&tref=typeahead%7Cterm%7Cpeanut+butter%7C%7C%7Chistory",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
#     "DNT": "1"
# }

# # Send GET request
# response = requests.get(url, headers=headers, params=params)



# # Check and print the response
# if response.status_code == 200:
#     data = response.json()
#     #print(json.dumps(data, indent=2))
#     price = jmespath.search("data.search.products[*].price", data)
#     buy_url = jmespath.search("data.search.products[*].item.enrichment.buy_url", data)
#     tcin = jmespath.search("data.search.products[*].tcin", data)
#     promotions = jmespath.search("data.search.products[*].promotions", data)
#     title = jmespath.search("data.search.products[*].product_descriptions.title", data)
#     print(json.dumps(promotions, indent=2))
#     #print(json.dumps(price, indent=2))

#     #print(buy_url)
# else:
#     print(f"Request failed with status code {response.status_code}")
#     print(response.text)


# # URL and parameters
url = "https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1"
params = {
    "key": "9f36aeafbe60771e321a7cc95a78140772ab3e96",
    "tcin": "84067786",
    "is_bot": "false",
    "store_id": "926",
    "pricing_store_id": "926",
    "has_pricing_store_id": "true",
    "has_financing_options": "true",
    "include_obsolete": "true",
    "visitor_id": "018C30AC533702019CE9F6D48BA7C647",
    "has_size_context": "true",
    "skip_personalized": "true",
    "skip_variation_hierarchy": "true",
    "channel": "WEB",
    "page": "/p/A-84067786"
}

# Headers
headers = {
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9",
    "dnt": "1",
    "origin": "https://www.target.com",
    "priority": "u=1, i",
    "referer": "https://www.target.com/p/creamy-peanut-butter-16oz-good-38-gather-8482/-/A-84067786",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

# Send GET request
response = requests.get(url, headers=headers, params=params)

# Check and print the response
if response.status_code == 200:
    data = response.json()
    #print(json.dumps(data, indent=2))
    # get barcoode
    barcode = jmespath.search("data.product.item.primary_barcode", data)
    ingredients = jmespath.search("data.product.item.enrichment.nutrition_facts.ingredients", data)

    print(f"{barcode = }")
    print(f"{ingredients = }")
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)