import csv
import pandas as pd

reader = pd.read_csv(r'PokeDex.csv')
print(reader)
userInput = input("Enter a Pokemon name: ")
print(reader[reader.Pokemon == userInput])
typeInput = input("Enter a type: ")
print(reader[reader.Type1 == typeInput])
