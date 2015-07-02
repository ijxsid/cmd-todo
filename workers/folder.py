import sys
import os.path
# HACK: To make lib accesible here.
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
from lib.todocollection import TodoCollection
import config
from firebase import firebase

todobase = firebase.FirebaseApplication(config.FIREBASE_URL, None)

foldername = 'app_dev'
todos = TodoCollection(todobase, '/todos', 'test_folder')
todo = {}
task = "using the same collection."
bounty = 10
todo['done'] = False

todos.add(task, bounty, folder=foldername)
