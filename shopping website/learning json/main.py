import json
import os

if os.getcwd().split("\\")[-1] != "shopping website": # os.getcwd() gets the folder the file runs on
    try:
        os.chdir("shopping website/learning json") # change the diractory it works on to discord bot(now it start it from the "games and projects" directory)
    except: # can cause a error if it starts it from the folder
        pass

with open("json file.json","r") as file:
    data = json.load(file) # load the json file

users = {}
for user in data["people"]:
    username = user["username"]
    del user["username"]
    users[username] = user
print(users)

"""for state in data['states']:
    print(state)"""
"""for state in data['states']:
    del state["area_codes"] # del a key

with open("new file.json", "w") as f:
    json.dump(data, f, indent=4) # write to the new file"""