import json
import os
from difflib import get_close_matches

#load JSON data
# data = json.load(open("data.json"))

#take word from user
# word = input('Enter word: ')
script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, 'data.json')

with open(file_path, 'r') as file:
    data = json.load(file)
    

#function to return meaning of the word from data
def getMeaning(w):
    #for case sensitivity
    w = w.lower()
    #if-else to check word exist in our data or not
    if w in data:
        return data[w]
    #give matching word
    elif len(get_close_matches(w,data.keys())) > 0:
        close_match = get_close_matches(w,data.keys())[0]
        print("Did you mean %s instead? Enter Y if yes or N if no: " % close_match)
        choice = input()
        choice = choice.lower()
        if choice == 'y':
            return data[close_match]
        elif choice == 'n':
            return "The word doesn't exist. Please double check it."
        else:
            return "Sorry, We didn't understand your entry."
    else:
        return "The word doesn't exist. Please double check it."

#function call to get meaning of the word entered by user


# if __name__ == '__main__':
#     word = input("Enter a word: ")
#     meaning = getMeaning(word)
#     if meaning:
#         print(f"The meaning of '{word}' is: {meaning}")
#     else:
#         print(f"No meaning found for '{word}'")
