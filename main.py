import json

jfile = open('default-cards-20260907090537.jsonl', 'r')
count = 0
for line in jfile:
    card = json.loads(line)
    if card['name'] == "Cultivate":
        print(card)
        count += 1
print(count)
jfile.close()
