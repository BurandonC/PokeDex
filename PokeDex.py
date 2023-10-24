import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import io


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
            "versions" : version,
            "moves": moves
        }

        return pokemon_info
    else:
        # Handle API error (e.g., show an error message, retry, etc.)
        print(f"Error: {response.status_code}")
        return None

def display_pokemon_image(pokemon_name):
    image_url = f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/{pokemon_name}.png"
    response = requests.get(image_url)
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = response.content
            img = Image.open(io.BytesIO(image_data))
            img = img.resize((100, 100), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            label_image = tk.Label(root, image=photo)
            label_image.image = photo
            label_image.pack()
        else:
            print("Image not found.")
    except Exception as e:
        print(f"Error displaying image: {e}")

def search_pokemon():
    pokemon_name = entry.get()
    if pokemon_name.strip():
        pokemon_info = get_pokemon_info(pokemon_name)
        if pokemon_info:
            text_widget.config(state = tk.NORMAL)
            text_widget.delete(1.0, tk.END)

            # Display Pokémon data in the Tkinter window
            text_widget.insert(tk.END, "Pokemon Info:\n")
            text_widget.insert(tk.END, f"Name: {pokemon_info['name']}\n")
            text_widget.insert(tk.END, f"Types: {', '.join(pokemon_info['types'])}\n")
            text_widget.insert(tk.END, f"Abilities: {', '.join(pokemon_info['abilities'])}\n")
            text_widget.insert(tk.END, f"Versions Introduced: {', '.join(pokemon_info['versions'])}\n")
            text_widget.insert(tk.END, "Stats:\n")
            for stat, value in pokemon_info['stats'].items():
                text_widget.insert(tk.END, f" - {stat}: {value}\n")
            display_pokemon_image(pokemon_name)  # Call this function to display the image
            text_widget.config(state=tk.DISABLED)  # Set text widget back to DISABLED (read-only)
        else:
            text_widget.config(state=tk.NORMAL)
            text_widget.insert(tk.END, "An error occurred. Please try again.\n")
            text_widget.config(state=tk.DISABLED)
    else:
        text_widget.config(state=tk.NORMAL)
        text_widget.insert(tk.END, "Please enter a valid Pokémon name.\n")
        text_widget.config(state=tk.DISABLED)

root = tk.Tk()
root.title("Pokemon Info Search")

label = tk.Label(root, text="Enter the name of a Pokemon: ")
entry = tk.Entry(root)
search_button = tk.Button(root, text="Search", command=search_pokemon)

# Create a text widget to display Pokémon data
text_widget = tk.Text(root, wrap=tk.WORD, width=40, height=20)
text_widget.insert(tk.END, "Pokémon Info will be displayed here.\n")
text_widget.config(state=tk.DISABLED)  # Make it read-only

label.pack()
entry.pack()
search_button.pack()
text_widget.pack()



root.mainloop()