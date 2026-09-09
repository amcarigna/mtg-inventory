# MTG Inventory
A simple application for keeping track of your mtg cards. The inventory is stored locally.  

Built on top of scryfall API. Python is necessary to run.  
Currently in development. Current functionality includes only a few standalone functions:
- `get_bulk_data()` gets a zipped JSON file containing every card object on Scryfall in English or the printed language if the card is only available in one language from scryfall. used as list of all mtg cards.
- `get_sets()` gets a JSON file of all mtg sets from scryfall.
- `search_card(name, id=None, set=None, collector_number=None)` searches bulk_data for a card based on input. currently only takes card name.