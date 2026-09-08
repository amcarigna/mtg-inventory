import json, os, requests


def get_bulk_data():
    print('removing old data...')
    folder = 'bulk_data'
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
            except PermissionError:
                print(f'cannot remove {file_path}, permission error')
            else:
                print(f'removed {file_path}')
    print('getting bulk data...')
    local_file = 'bulk_data.jsonl.gz'
    url = 'https://api.scryfall.com/bulk-data'
    response = requests.get(url)
    if response.status_code == 200:
        file = open(local_file, 'wt')
        file.write(response.text)



jfile = open('bulk-data/default-cards-20260907090537.jsonl', 'r')
count = 0
for line in jfile:
    card = json.loads(line)
    if card['name'] == "Cultivate":
        print(card)
        count += 1
print(count)
jfile.close()

if __name__ == '__main__':
    pass