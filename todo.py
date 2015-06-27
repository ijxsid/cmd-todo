# -*- coding: utf-8 -*-
from firebase import firebase
from clint.textui import puts, indent, colored
import argparse
import random

import json

todobase = firebase.FirebaseApplication('https://shining-heat-5315.firebaseio.com/', None)

# TODO: Better Way to Add todos.
# TODO: Better Modelling for todos.
# TODO: Better Way to Edit Todos.
# TODO: Filtering Todos
# TODO: Rewards and Stuff.
# TODO: User Dashboard.
def get_unique_count():
    """
    Returns unique count for adding new todos.
    """
    count = todobase.get('/counter', 'count')
    if count is None:
        count = random.randint(1,1000)
    else:
        count += 1
    todobase.put('/counter', 'count', count)
    return count

def get_todos():
    """
    fetches todos and show them.
    """
    # TODO: Divide this function into two. Does two things.
    todos = todobase.get('/todos', None)
    for key in todos.keys():
        todo = todos[key]
        donestring = colored.green((u'\u2713').encode('utf-8'))
        puts( key + " : "+colored.blue(str(todo['bounty'])) + " : " + todo['task']
             + " " + (donestring if todo['done'] else ''))

def get_todo(name):
    """
    fetches and displays a todo item.
    """
    # TODO: Divide this into two. Reuse code.
    todo = todobase.get('/todos', name)
    if todo is not None:
        puts ( colored.blue(str(todo['bounty'])) + " : " + todo['task'] )
    else:
        puts( colored.red('404: Nothing Found'))

def add_todo(task, points=1):
    """
    Handles Adding todos into the todo-list
    """
    N = get_unique_count()
    name = 'todo' + str(N+1)
    todo = {'task': task, 'bounty': points, 'done': False}
    res = todobase.put('/todos', name, todo)
    print res

def markdone(name):
    """
    marks done a todo item by name.
    """
    res = todobase.patch('/todos/' + name , {'done': True})
    print res

def main():
    parser = argparse.ArgumentParser(description='A Todo List Manager in your command line')
    # get argument
    parser.add_argument('-g','--get', nargs='?', metavar="task")
    # add todo argument
    parser.add_argument('-a', '--add', nargs=2, metavar=('task', 'bounty'))
    # done todo argument for marking something done
    parser.add_argument('-d', '--done', nargs='+', metavar='task')

    args = parser.parse_args()
    if args.add and len(args.add) == 2:
        print "Case 1"
        task = str(args.add[0]) # task
        bounty = int(args.add[1])
        add_todo(task, bounty)

    elif args.get is not None:
        print "Case 3"
        get_todo(args.get)

    elif args.done:
        print "Case 4"
        if isinstance(args.done, str):
            markdone(args.done)
        elif isinstance(args.done, list):
            for task in args.done:
                markdone(task)

    elif args.get == None:
        print "Case 2"
        get_todos()


if __name__ == '__main__':
    main()
