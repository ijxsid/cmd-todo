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
from lib.rewards import Rewards

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
    parser.add_argument('--delete', nargs='+', metavar='task')
    # dashboard argument/ user profile.
    parser.add_argument('-m', '--me', action='store_true')
    # dynamic argument
    parser.add_argument('-e', '--edit', nargs=1, metavar=('task') )
    # Version Info
    parser.add_argument('-V', '--version', action='store_true')

    # Add an optional rewards optional
    parser.add_argument('-r','--reward', action='store_true')
    # Add Redeem optional argument
    parser.add_argument('-t', '--redeem', nargs='+', metavar=('reward', 'times'))

    args = parser.parse_args()
    todos = TodoCollection(todobase, '/todos', 'todo')
    rewards = Rewards(todobase, '/rewards', 'reward')
    editor = TodoEditor(todos)
    user = Profile(todos)
    print args

    if isinstance(args.add, list):
        if args.reward:
            # Add an reward
            if len(args.add) == 2:
                reward = str(args.add[0])
                bounty = int(args.add[1])
                rewards.add(reward, bounty)

        else:
            if len(args.add) == 0:
                editor.addflow()
            elif len(args.add) == 2:
                task = str(args.add[0]) # task
                bounty = int(args.add[1])
                todos.add(task, bounty)

    elif args.edit:
        editor.editflow(args.edit[0])

    elif args.get is not None:
        if args.reward:
            if args.get[0] is None:
                rewards.get_all()
            else:
                rewards.get(args.get[0])
        else:
            if args.get[0] is None:
                todos.get_all()
            else:
                todos.get(args.get[0])


    elif args.done:
        if isinstance(args.done, str):
            todos.markdone(args.done)
        elif isinstance(args.done, list):
            for task in args.done:
                todos.markdone(task)

    elif args.delete:
        if args.reward:
            if isinstance(args.delete, str):
                rewards.delete(args.delete)
            elif isinstance(args.delete, list):
                for task in args.delete:
                    rewards.delete(task)
        else:
            if isinstance(args.delete, str):
                todos.delete(args.delete)
            elif isinstance(args.delete, list):
                for task in args.delete:
                    todos.delete(task)


    elif args.redeem:
        if args.reward:
            name = args.redeem[0]
            if len(args.redeem) == 2:
                times = int(args.redeem[1])
            else:
                times = 1
            rewards.redeem(name, times)

    elif args.me:
        user.show_profile()

    elif args.version:
        puts( "Version: " + _version)
        copyright = colored.green((u'\u00a9').encode('utf-8') + " 2015 Inderjit Sidhu & Airbase IO")
        puts(copyright)




if __name__ == '__main__':
    main()
