import anvil

hash = anvil.get_url_hash()

url_components = hash.split("?")

if len(url_components) > 1:
    pattern = url_components[0]
    params = url_components[1]

    query_dict = {}
    for pair in params.split("&"):
        key, value = pair.split("=")
        query_dict[key] = value
else:
    pattern = hash
    query_dict = hash


anvil.alert(pattern)
anvil.alert(query_dict)

if pattern == "chatbox":
    anvil.open_form("Chatbox")
else:
    anvil.open_form("StandardPage")
