import json

data = {
    "query": "Kapadokya şiirleri",
    "search_type": "search",
    "lang": "tr",
    "n_results": 2
}

result = json.dumps(data)
print(result)