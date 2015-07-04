# -*- coding: utf-8 -*-
from firebase import firebase
from clint.textui import puts, indent, colored
import argparse
import config
from lib.todocollection import TodoCollection
from lib.userprofile import Profile
from lib.todoeditor import TodoEditor
from lib.rewards import Rewards
from lib.schedule import Schedule
import info


todobase = firebase.FirebaseApplication(config.FIREBASE_URL, None)
_version = info.VERSION


def main():
    parser = argparse.ArgumentParser(description='A Todo List Manager in your command line')
    # get argument
    parser.add_argument('-g','--get', nargs='?', metavar="task", action='append')
    # filter by tag argument
    parser.add_argument('-t', '--tag', nargs="+", metavar='tag')
    # filter by folder argument
    parser.add_argument('-f', '--folder', nargs='?', metavar='folder', action='append')
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
    parser.add_argument('-x','--redeem', nargs='+', metavar=('reward', 'times'))
    parser.add_argument('--structure', action='store_true')
    parser.add_argument('--timer', action='store_true')
    parser.add_argument('--reset', action='store_true')
    parser.add_argument('--snooze', nargs=2, metavar=('task', 'snooze'))
    parser.add_argument('--schedule', action='store_true')
    args = parser.parse_args()
    todos = TodoCollection(todobase, '/todos', 'todo')
    rewards = Rewards(todobase, '/rewards', 'reward')
    editor = TodoEditor(todos)
    user = Profile(todobase, '/profile', todos, rewards)

    print args

    if args.folder and args.folder[0] is None:
        args.folder = ['MAIN']

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
        if args.folder:
            # Editing Folder is equivalent to moving between folders.
            todos.move_to_folder(args.folder[0], args.edit[0])
        elif args.timer and args.reset:
            todos.start_time_for_todo(args.edit[0], reset=True)
        elif args.timer:
            todos.start_time_for_todo(args.edit[0])
        elif args.reset:
            todos.reset_timer_for_todo(args.edit[0])
        else:
            editor.editflow(args.edit[0])

    elif args.snooze:
        todos.handle_snooze(args.snooze[0], args.snooze[1])

    elif args.get is not None:
        if args.reward:
            if args.get[0] is None:
                rewards.get_all()
            else:
                rewards.get(args.get[0])
        else:
            if args.folder:
                todos.get_by_folder(args.folder[0])
            elif args.tag:
                if args.folder:
                    todos.get_by_folder(args.folder[0], args.tag)
                else:
                    todos.get_all(tags=args.tag)
            elif args.get[0] is None:
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
        elif args.folder:
            if len(args.delete) == 1:
                todos.delete_folder(args.delete[0])
            else:
                print "Cannot delete multiple Folders at once.\
                       \nDelete one by one."
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
        user.update()
        user.show_profile()

    elif args.version:
        puts( "Version: " + _version)
        APP_COPYRIGHT = colored.green((u'\u00a9').encode('utf-8') + " 2015 Inderjit Sidhu & Airbase IO")
        puts(APP_COPYRIGHT)
    elif args.structure:
        structure = todos.fetch_structure()
        print structure

    elif args.schedule:
        schedule = Schedule(todobase, todos.fetch_todos)
        schedule.print_schedule()




if __name__ == '__main__':
    main()
