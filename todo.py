# -*- coding: utf-8 -*-
from firebase import firebase
from clint.textui import puts, indent, colored
import argparse
import random
import config
import json
from lib.utils import Counter
from lib.todocollection import TodoCollection
from lib.userprofile import Profile
from workers.todoeditor import TodoEditor

todobase = firebase.FirebaseApplication(config.FIREBASE_URL, None)
_version = config.APP_VERSION

# TODO: Better Modelling for todos.
# TODO: Filtering Todos.
# TODO: Rewards and Stuff.
# TODO: Due dates and timers.



def main():
    parser = argparse.ArgumentParser(description='A Todo List Manager in your command line')
    # get argument
    parser.add_argument('-g','--get', nargs='?', metavar="task", action='append')
    # add todo argument
    parser.add_argument('-a', '--add', nargs='*')
    # done todo argument for marking something done
    parser.add_argument('-d', '--done', nargs='+', metavar='task')
    # removing a todo item
    parser.add_argument('-r', '--rm', nargs='+', metavar='task')
    # dashboard argument/ user profile.
    parser.add_argument('-m', '--me', action='store_true')
    # dynamic argument
    parser.add_argument('-e', '--edit', nargs=1, metavar=('task') )
    # Version Info
    parser.add_argument('-V', '--version', action='store_true')

    args = parser.parse_args()
    todos = TodoCollection(todobase, '/todos', 'todo')
    editor = TodoEditor(todos)
    user = Profile(todos)
    print args

    if isinstance(args.add, list):
        if len(args.add) == 0:
            editor.addflow()
        elif len(args.add) == 2:
            task = str(args.add[0]) # task
            bounty = int(args.add[1])
            todos.add(task, bounty)

    elif args.edit:
        editor.editflow(args.edit[0])

    elif args.get is not None:
        print "Case 2"
        if args.get[0] is None:
            todos.get_all()
        else:
            todos.get(args.get[0])

    elif args.done:
        print "Case 4"
        if isinstance(args.done, str):
            todos.markdone(args.done)
        elif isinstance(args.done, list):
            for task in args.done:
                todos.markdone(task)

    elif args.rm:
        print "Case 6"
        if isinstance(args.rm, str):
            todos.delete(args.rm)
        elif isinstance(args.rm, list):
            for task in args.rm:
                todos.delete(task)


    elif args.me:
        print "Case 5"
        user.show_profile()

    elif args.version:
        puts( "Version: " + _version)
        copyright = colored.green((u'\u00a9').encode('utf-8') + " 2015 Inderjit Sidhu & Airbase IO")
        puts(copyright)




if __name__ == '__main__':
    main()
