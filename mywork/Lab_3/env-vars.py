#!/opt/homebrew/bin/python3

import os

os.environ["FAV_ROLLER_COASTER"] = input('What is your favorite roller coaster? ')
os.environ["MAJOR"] = input('What is your major? ')
os.environ["HARDEST_CLASS"] = input('What is the hardest class you are taking this semester? ')

print(os.getenv("FAV_ROLLER_COASTER"))
print(os.getenv("MAJOR"))
print(os.getenv("HARDEST_CLASS"))
