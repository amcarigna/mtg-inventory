import json, os, requests, gzip


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


def search_bulk_data(name, **kwargs):
    name = name.lower().strip(",'-")
    best_results = []
    other_results = []
    if (len(name) < 3) and (len(kwargs) == 0):
        print('error: name is too short, try again')
        return best_results, other_results
    local_file = 'scryfall-data/bulk_data.jsonl.gz'
    file = gzip.open(local_file, 'rb')
    for line in file:
        card_dict = json.loads(line)
        if name in card_dict['name'].lower().strip(",'-"):
            other_results.append(card_dict)
            test_dict = {key: card_dict[key] for key in kwargs.keys()}
            if (name == card_dict['name'].lower().strip(",'-")) or ((len(kwargs) > 0) and (test_dict == kwargs)):
                best_results.append(card_dict)
    file.close()
    if len(best_results) > 0:
        return best_results
    return other_results


if __name__ == '__main__':
    # get_bulk_data()
    results = search_bulk_data("", set='ltr')
    for card in results:
        print(card['name'], card['id'], card['set'], card['collector_number'], card['prices'])
    print(len(results))
    # get_sets()
    # local_file = 'scryfall-data/sets.json'
    # file = open(local_file, 'rt')
    # sets = file.read()
    # file.close()
    # sets = json.loads(sets)
    # for set in sets['data']:
    #     if set['code'] == 'lea':
    #         print(set)
