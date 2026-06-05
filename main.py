"""
Create a Python application that:
- Extracts the data from an api or csv
- Stores the data in MongoDB
- Serializes data into JSON
- Uploads exported data to an S3 bucket as json files
"""
import requests
import pymongo

def get_all_pokemon(limit=10):
    try:
        response = requests.get(f'https://pokeapi.co/api/v2/pokemon?limit={limit}')
        return response.json()['results']
    
    except Exception as e: 
        print(f'Error {e}')
        return 


def get_pokemon_details():
    all_pokemon = get_all_pokemon()
    for pokemon in all_pokemon:
        try:
            response = requests.get(pokemon['url'])

            pokemon['details'] = response.json()
    
        except Exception as e: 
            print(f'Error {e}')



#mongo connect

class mongo:
    def __init__(self):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["pokemon_db"]
        self.pokemon = db["pokemon"]

    def upload_data(self, data):
        self.pokemon.insert_many(data)

    def reset(self):
        self.pokemon.delete_many({})


if __name__=='__main__':
    data=get_all_pokemon()
    db = mongo() 
    db.upload_data(data)
