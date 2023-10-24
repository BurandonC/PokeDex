import requests


def get_pokemon_info(pokemon_name, display_moves=False):
    """
    Retrieves information about a Pokemon from the PokeAPI.

    Args:
        pokemon_name (str): The name of the Pokemon to retrieve information for.

    Returns:
        dict: A dictionary containing information about the specified Pokemon,
            including its name, types, abilities, and stats.
    """
    # Construct the API endpoint URL for the specified Pokemon
    endpoint_url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"

    # Send an HTTP GET request to the PokeAPI
    response = requests.get(endpoint_url)

    # Check if the response is successful (e.g., status code 200)
    if response.status_code == 200:
        # Parse the JSON response to extract Pokemon details
        pokemon_data = response.json()

        # Extract the relevant information
        name = pokemon_data["name"]
        types = [type_data["type"]["name"] for type_data in pokemon_data["types"]]
        abilities = [ability_data["ability"]["name"] for ability_data in pokemon_data["abilities"]]
        stats = {stat_data["stat"]["name"]: stat_data["base_stat"] for stat_data in pokemon_data["stats"]}
        version = [version_data["version"]["name"] for version_data in pokemon_data["game_indices"]]
        moves = []
        if display_moves:
            moves = [move_data["move"]["name"] for move_data in pokemon_data["moves"]]

        # Construct a dictionary containing the extracted information
        pokemon_info = {
            "name": name,
            "types": types,
            "abilities": abilities,
            "stats": stats,
            "version" : version,
            "moves": moves
        }

        return pokemon_info
    else:
        # Handle API error (e.g., show an error message, retry, etc.)
        print(f"Error: {response.status_code}")
        return None


if __name__ == "__main__":
    while True:
        command = input("Enter name of a Pokémon, 'moves', or type 'exit' to quit: ")

        if command.lower() == 'exit':
            break
        elif command.lower() == "moves":
            display_moves = True
            continue
        else:
            display_moves = False

        if command.strip():
            pokemon_info = get_pokemon_info(command, display_moves)
            if pokemon_info:
                print("Pokemon Info:")
                print(f"Name: {pokemon_info['name']}")
                print(f"Types: {', '.join(pokemon_info['types'])}")
                print(f"Abilities: {', '.join(pokemon_info['abilities'])}")
                if display_moves:
                    print(f"Moves: {', '.join(pokemon_info['moves'])}")
                print(f"Version Introduced: {', '.join(pokemon_info['version'])}")
                print("Stats:")
                for stat, value in pokemon_info['stats'].items():
                    print(f" - {stat}: {value}")
            else:
                print("An error occurred. Please try again.")
        else:
            print("Please enter a valid Pokémon name, 'moves', or type 'exit' to quit")