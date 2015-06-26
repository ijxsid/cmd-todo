from firebase import firebase
import json

todobase = firebase.FirebaseApplication('https://shining-heat-5315.firebaseio.com/', None)

def get_todos():
    todos = todobase.get('/todos', None)
    for key in todos.keys():
        todo = todos[key]
        # print todo
        print todo['task'] + " : " + str(todo['bounty'])


def add_todo(task, points=1):
    todo = {'task': task, 'bounty': points}
    res = todobase.post('/todos', todo)
    print res


# add_todo('Do Laundry', 15)
# add_todo('Write Up A Blog Post', 15)
# add_todo('Set Up Private Eye Repo', 10)

get_todos()
