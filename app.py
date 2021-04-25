import json
import colorama
from difflib import get_close_matches
import termcolor2

colorama.init()

data = json.load(open("data.json"))


def findInDictionary(w):
    colorama.init()
    w = w.lower()
    if w in data:
        return data[w]
    elif len(get_close_matches(w, data.keys())) > 0:
        matches = "Did you mean %s instead? Enter Y if yes, or N if no: " % get_close_matches(
            w, data.keys())[0]
        yn = input(matches)
        if yn == "Y":
            return data[get_close_matches(w, data.keys())[0]]
        elif yn == "N":
            return "The word doesn't exist. Please double check it."
        else:
            return "We didn't understand your entry."
    else:
        return "The word doesn't exist. Please double check it."


while True:
    try:
        word = input("Enter word: ")
        output = findInDictionary(word)
        if type(output) == list:
            for item in output:
                print(termcolor2.colored((item), 'green'))
        else:
            print(termcolor2.colored((output), 'green'))
    except KeyboardInterrupt as e:
        print(termcolor2.colored(("Are you really want to quit?y/n :"), 'red'))
        c = input()
        if(c.lower() == 'n'):
            continue
        else:
            exit(0)
