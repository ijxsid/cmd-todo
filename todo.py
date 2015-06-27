# -*- coding: utf-8 -*-
from firebase import firebase
from clint.textui import puts, indent, colored
import argparse
import random
import config
import json

todobase = firebase.FirebaseApplication(config.FIREBASE_URL, None)

# TODO: Better Way to Add todos.
# TODO: Better Modelling for todos.
# TODO: Better Way to Edit Todos.
# TODO: Filtering Todos
# TODO: Rewards and Stuff.

def foreach(collection, callback):
    for key in collection.keys():
        item = collection[key]
        callback(item, key)

def fetch_todos(name=None):
    return todobase.get('/todos', name)

def calculate_points(todos):
    """
    calculates points and other things for a user.
    """
    total_points = 0
    earned_points = 0
    items_done = 0
    total_items = 0
    for key in todos.keys():
        todo = todos[key]
        total_points += todo['bounty']
        earned_points += todo['bounty'] if todo['done'] else 0
        items_done += 1 if todo['done'] else 0
        total_items +=1

    return (total_points, earned_points, total_items, items_done)

def show_profile():
    """
    prints out user Dashboard.
    """
    todos = todobase.get('/todos', None)
    points, points_earned, num_of_items, done = calculate_points(todos)
    puts ( 'Total Items: ' +  colored.blue(str(num_of_items)))
    puts ( 'Total Done: ' +  colored.green(str(done)))
    puts ( 'Total Points: ' +  colored.blue(str(points)))
    puts ( 'Points Earned: ' +  colored.green(str(points_earned)))


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

def print_todo_item(item, key=None):
    """
    prints an todo item.
    """
    if item is not None:
        donestring = colored.green((u'\u2713').encode('utf-8'))
        puts( key + " : "+colored.blue(str(item['bounty'])) + " : " + item['task']
             + " " + (donestring if item['done'] else ''))
    else:
        puts( colored.red('404: Nothing Found'))



def get_todos():
    """
    fetches todos and show them.
    """
    todos = fetch_todos()
    foreach(todos, print_todo_item)


def get_todo(name):
    """
    fetches and displays a todo item.
    """
    todo = fetch_todos(name)
    print_todo_item(todo, name)

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
    parser.add_argument('-g','--get', nargs='?', metavar="task", action='append')
    # add todo argument
    parser.add_argument('-a', '--add', nargs=2, metavar=('task', 'bounty'))
    # done todo argument for marking something done
    parser.add_argument('-d', '--done', nargs='+', metavar='task')
    # dashboard argument/ user profile.
    parser.add_argument('-m', '--me', action='store_true')

    args = parser.parse_args()
    if args.add and len(args.add) == 2:
        print "Case 1"
        task = str(args.add[0]) # task
        bounty = int(args.add[1])
        add_todo(task, bounty)

    elif args.get is not None:
        print "Case 2"
        if args.get[0] is None:
            get_todos()
        else:
            get_todo(args.get[0])

    elif args.done:
        print "Case 4"
        if isinstance(args.done, str):
            markdone(args.done)
        elif isinstance(args.done, list):
            for task in args.done:
                markdone(task)

    elif args.me:
        print "Case 5"
        show_profile()



if __name__ == '__main__':
    main()
