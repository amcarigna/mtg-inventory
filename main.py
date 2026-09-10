import json, os, requests, gzip, string


def get_bulk_data():
    print('\nremoving old bulk data...')
    folder = 'scryfall-data'
    extension = '.jsonl.gz'
    for file in os.listdir(folder):
        if file.endswith(extension):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    print(f'\tcannot remove {file_path}, permission error')
                else:
                    print(f'\tremoved {file_path}')
    print('finding bulk data...')
    url = 'https://api.scryfall.com/bulk-data'
    headers = {'User-Agent': 'myapp/v0.0.1'}
    url_response = requests.get(url, headers=headers)
    uri = url_response.json()['data'][2]['jsonl_download_uri']
    print('downloading bulk data...')
    uri_response = requests.get(uri, headers=headers)
    local_file = 'scryfall-data/bulk_data.jsonl.gz'
    print('saving bulk data...')
    if uri_response.status_code == 200:
        file = open(local_file, 'wb')
        file.write(uri_response.content)
        file.close()
        print(f'\tbulk data saved to {local_file}')
    else:
        print('bulk data not saved')


def get_sets():
    print('\nremoving old sets...')
    folder = 'scryfall-data'
    extension = '.json'
    for file in os.listdir(folder):
        if file.endswith(extension):
            file_path = os.path.join(folder, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f'\tremoved {file_path}')
    print('getting new sets...')
    url = 'https://api.scryfall.com/sets'
    headers = {'User-Agent': 'myapp/v0.0.1'}
    response = requests.get(url, headers=headers)
    local_file = 'scryfall-data/sets.json'
    print('saving sets...')
    if response.status_code == 200:
        file = open(local_file, 'wt')
        file.write(response.text)
        file.close()
        print(f'\tsets saved to {local_file}')
    else:
        print('sets not saved')


def clean_str(str):
    return ''.join(char for char in str if char not in string.punctuation).lower()


def search_bulk_data(name, **kwargs):
    name = clean_str(name)
    if (len(name) < 3) and (len(kwargs) == 0):
        best_results = []
        other_results = []
        print('error: name is too short, try again')
    elif len(name) >= 3:
        local_file = 'scryfall-data/bulk_data.jsonl.gz'
        file = gzip.open(local_file, 'rb')
        best_results, other_results = search_name(file, name, **kwargs)
        file.close()
    else:
        local_file = 'scryfall-data/bulk_data.jsonl.gz'
        file = gzip.open(local_file, 'rb')
        best_results, other_results = search_kwargs(file, name, **kwargs)
        file.close()
    return best_results, other_results


def search_name(file, name, **kwargs):
    best_results = []
    other_results = []
    for line in file:
        card_dict = json.loads(line)
        if name in clean_str(card_dict['name']):
            other_results.append(card_dict)
    for card_dict in other_results:
        if name == clean_str(card_dict['name']):
            best_results.append(card_dict)
    other_results = [dict for dict in other_results if dict not in best_results]
    if kwargs:
        for card_dict in best_results:
            test_dict = {key: card_dict[key] for key in kwargs.keys()}
            if test_dict != kwargs:
                other_results.append(card_dict)
    best_results = [dict for dict in best_results if dict not in other_results]
    other_results = other_results[::-1]
    return best_results, other_results


def search_kwargs(file, name, **kwargs):
    best_results = []
    other_results = []
    for line in file:
        card_dict = json.loads(line)
        test_dict = {key: card_dict[key] for key in kwargs.keys()}
        if test_dict == kwargs:
            other_results.append(card_dict)
    for card_dict in other_results:
        if name in clean_str(card_dict['name']):
            best_results.append(card_dict)
    other_results = [dict for dict in other_results if dict not in best_results]
    return best_results, other_results


def get_lowest_price(list_of_dicts):
    # released_at is the date key
    return list_of_dicts


if __name__ == '__main__':
    best_results, other_results = search_bulk_data("opt")
    for card in best_results:
        print(card['name'], card['id'], card['set'], card['collector_number'], card['prices'])
    print(len(best_results))
    print(get_lowest_price(best_results))
