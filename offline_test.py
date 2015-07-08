from lib.filebase import FileBaseApplication
from config import FIREBASE_URL

def main():
    fbapp = FileBaseApplication(FIREBASE_URL, 'temp.json')
    todos = fbapp.get('/todos/app/todo398/', 'task')
    print todos
    fbapp.put('/todos/app/', 'todo99113', {'task': "Offline_support", "bounty": 15})
    fbapp.delete('/todos/app/', 'todo99113')
    fbapp.patch('/todos/all_dev/todo393', {'task': "Burger king at 10AM"})
    fbapp.delete('/todos/MAIN', 'todo395')
    fbapp.save()
    fbapp.sync()

if __name__ == '__main__':
    main()
