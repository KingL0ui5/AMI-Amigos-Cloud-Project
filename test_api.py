"""
Tests the get_all_pokemon function from main.py.
Fetches a small number of Pokemon from the PokeAPI and prints the result.
Expected: A list of dicts each containing 'name' and 'url' keys.
Does not require MongoDB or AWS.
"""
from main import get_all_pokemon

def test_api():
    try:
        data = get_all_pokemon(5)
        assert isinstance(data, list), "Expected a list"
        assert len(data) == 5, f"Expected 5 results, got {len(data)}"
        assert 'name' in data[0] and 'url' in data[0], "Expected 'name' and 'url' keys"
        print("API fetch successful:", data)
    except Exception as e:
        print(f"API fetch failed: {e}")

if __name__ == '__main__':
    test_api()
