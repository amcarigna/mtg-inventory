import json, os, requests, gzip


def get_bulk_data():
    print('removing old bulk data...')
    folder = 'bulk-data'
    for file in os.listdir(folder):
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
    local_file = 'bulk-data/bulk_data.jsonl.gz'
    print('saving bulk data...')
    if uri_response.status_code == 200:
        file = open(local_file, 'wb')
        file.write(uri_response.content)
        file.close()
        print('bulk data saved to bulk_data/bulk_data.jsonl.gz')
    else:
        print('bulk data not saved to bulk_data/bulk_data.jsonl')


# jfile = open('bulk-data/default-cards-20260907090537.jsonl', 'r')
# count = 0
# for line in jfile:
#     card = json.loads(line)
#     if card['name'] == "Cultivate":
#         print(card)
#         count += 1
# print(count)
# jfile.close()

if __name__ == '__main__':
    get_bulk_data()
