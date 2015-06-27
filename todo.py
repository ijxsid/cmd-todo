from firebase import firebase
from clint.textui import puts, indent, colored
import argparse

import json

todobase = firebase.FirebaseApplication('https://shining-heat-5315.firebaseio.com/', None)

# TODO: Better Modelling for todos.
# TODO: Better Way to Add todos.
# TODO: Better Way to Edit Todos.
# TODO: Filtering Todos
# TODO: Rewards and Stuff.
# TODO: User Dashboard.

def get_todos():
    todos = todobase.get('/todos', None)
    for key in todos.keys():
        todo = todos[key]
        puts( key + " : "+colored.blue(str(todo['bounty'])) + " : " + todo['task'] )

def get_todo(name):
    todo = todobase.get('/todos', name)
    if todo is not None:
        puts ( colored.blue(str(todo['bounty'])) + " : " + todo['task'] )
    else:
        puts( colored.red('404: Nothing Found'))

def add_todo(task, points=1):
    todos = todobase.get('/todos', None)
    N = 0 if todos is None else len(todos.keys())
    name = 'todo' + str(N+1)
    todo = {'task': task, 'bounty': points}
    res = todobase.put('/todos', name, todo)
    print res


# add_todo('Do Laundry', 15)
# add_todo('Write Up A Blog Post', 15)
# add_todo('Set Up Private Eye Repo', 10)

#get_todos()
def main():
    parser = argparse.ArgumentParser(description='A Todo List Manager in your command line')
    # get argument
    parser.add_argument('--get', nargs='?', metavar="task")
    # add todo argument
    parser.add_argument('--add', nargs=2, metavar=('task', 'bounty'))

    args = parser.parse_args()
    if args.add and len(args.add) == 2:
        task = str(args.add[0]) # task
        bounty = int(args.add[1])
        add_todo(task, bounty)

    elif args.get == None:
        get_todos()

    elif args.get is not None:
        get_todo(args.get)


if __name__ == '__main__':
    main()
