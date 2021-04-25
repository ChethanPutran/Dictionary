import json
import colorama
from difflib import get_close_matches
import termcolor2
import mysql.connector
import credentials 
colorama.init()

keys = []

try:
    con = mysql.connector.connect(
        user=credentials.user,
        password=credentials.password,
        host=credentials.host,
        database=credentials.database
    )

    cursor = con.cursor()
except Exception as e:
    print(termcolor2.colored(("Unable to connect to the database!! Check your internet connection & try again!"),'red'))
    exit(0)
    
    
while True:

    try:
        word = input("Enter a word: ")
        query = cursor.execute(
            "SELECT * FROM Dictionary WHERE Expression ='%s' " % word)
        results = cursor.fetchall()

        if results:
            for result in results:
                print(termcolor2.colored((result[1]), 'green'))
        else:
            query = cursor.execute(
                "SELECT * FROM Dictionary WHERE Expression LIKE '{}%' AND length(Expression) < {}" .format(word[:-2], (len(word)+6)))
            results = cursor.fetchall()
            if(results):
                for result in results:
                    keys.append(result[0])

                matches = get_close_matches(word, keys)

                if len(matches) > 0:
                    test = "Did you mean %s instead? Enter Y if yes, or N if no: " % matches[0]
                    yn = input(test)
                    if yn.upper() == "Y":
                        for result in results:
                            if(result[0] == matches[0]):
                                meaning = result[1]
                                print(meaning)
                                break

                    elif yn == "N":

                        print(termcolor2.colored(
                            ("The word doesn't exist. Please double check it."), 'red'))

                    else:

                        print(termcolor2.colored(
                            ("We didn't understand your entry."), 'red'))
            else:

                print("The word doesn't exist. Please double check it.")

    except KeyboardInterrupt:

        print(termcolor2.colored(("Are you really want to exit?Y/N :"), 'red'))
        ans = input()
        if ans.lower() == 'n':
            continue
        else:
            con.close()
            exit(0)
