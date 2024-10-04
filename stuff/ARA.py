key_map = {}

def make_request():
    return 1

def filter_data(data):
    filtered_data = {}
    for keys in key_map.keys():
        filtered_data[key_map[keys]] = data[keys]

def get_data():
    response = make_request()[:]['values']
    return filter_data(response)