from lib.filebase import FileBaseApplication
from config import FIREBASE_URL

def main():
    fbapp = FileBaseApplication(FIREBASE_URL, 'temp.json')
    todos = fbapp.get('/todos/app/todo398', 'task')
    print todos

if __name__ == '__main__':
    main()
