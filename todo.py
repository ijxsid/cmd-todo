from firebase import firebase
from clint.textui import puts, indent, colored
import argparse

import json

todobase = firebase.FirebaseApplication('https://shining-heat-5315.firebaseio.com/', None)

# TODO: Better Modelling for todos.
def get_todos():
    todos = todobase.get('/todos', None)
    for key in todos.keys():
        todo = todos[key]
        puts( colored.red(str(todo['bounty'])) + " : " + todo['task'] )


def add_todo(task, points=1):
    todo = {'task': task, 'bounty': points}
    res = todobase.post('/todos', todo)
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

    if args.get == None:
        get_todos()




if __name__ == '__main__':
    main()
