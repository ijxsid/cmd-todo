from utils import foreach, print_todo_item, Counter
from datetime import datetime
from timeit import Timer

class TodoCollection(object):

    def __init__(self, base, url, countername='todo'):
        self._base = base
        self._url = url
        self._todos = self._base.get(url, None)
        self._counter = Counter(countername, self._base)
        self._structure = self._make_folder_structure(self._todos)

    def _update(self):
        self._todos = self._base.get(self._url, None)

    def fetch_structure(self):
        return self._structure

    def fetch_todos(self):
        return {key: self._todos[foldername][key] for key, foldername in self._structure.iteritems()}

    def get_all(self, tags=None):
        todos = {key: self._todos[foldername][key] for key, foldername in self._structure.iteritems()}

        if tags:
            todos = {key: todos[key] for key in todos.keys() if self._is_tagged(key, tags)}
        foreach(todos, print_todo_item)

    def get(self, name):
        """
        get foldername from name and then look for todo with the given name
        inside the folder.
        """
        foldername = self._structure[name]
        print_todo_item(self._todos[foldername][name], name)

    def get_by_folder(self, foldername, tags=None):
        todos = self._todos[foldername]

        if tags:
            todos = {key: todos[key] for key in todos.keys() if self._is_tagged(key, tags)}
        foreach(todos, print_todo_item)

    def add(self, task, bounty, duetime=None, tags=[], folder=None):
        assert isinstance(task, str)
        assert len(task) > 0, "Task Cannot be left empty."
        assert isinstance(bounty, int)
        assert isinstance(tags, list)
        N = self._counter.get()
        name = 'todo' + str(N+1)
        todo = {'task': task, 'bounty': bounty, 'done': False}
        if duetime is not None:
            todo['due'] = str(duetime)
        if tags != []:
            todo['tags'] = tags
        if not folder:
            folder = 'MAIN' #Our default folder, uppercase to be unique
        res = self._base.put(self._url + "/" + folder, name, todo)
        print res
        self._update()

    def markdone(self, name):
        self.edit(name, {'done': True})

    def edit(self, name, newtodo):
        # TODO: Need to find a better way to print responses.
        if name in self._structure.keys():
            foldername = self._structure[name]
            res = self._base.patch(self._url + "/" + foldername + "/" + name , newtodo)
            print res
        else:
            print "Not Found"
        self._update()

    def delete(self, name):
        if name in self._structure.keys():
            foldername = self._structure[name]
            res = self._base.delete(self._url + '/' + foldername, name)
            print res
        else:
            print "Not Found. Can't Delete"
        self._update()

    def move_to_folder(self, foldername, key):
        src_foldername = self._structure[key]
        if src_foldername != foldername:
            todo = self._todos[src_foldername][key]
            self.delete(key)
            res = self._base.put(self._url + "/" + foldername, key, todo)
            print res
            self._structure[key] = foldername


    def delete_folder(self, foldername):
        if foldername == 'MAIN':
            print "Cannot delete default folder."
        elif foldername in self._todos.keys():
            keys_to_delete = []
            for key, value in self._structure.iteritems():
                if value == foldername:
                    keys_to_delete.append(key)
            for key in keys_to_delete:
                del self._structure[key]
            res = self._base.delete(self._url, foldername)
            print res
        else:
            print "Folder not found"


    def _is_tagged(self, key, tags):
        try:
            foldername = self._structure[key]
            item_tags = self._todos[foldername][key]['tags']
        except KeyError:
            item_tags = []
        return any(tag in item_tags for tag in tags)

    def _make_folder_structure(self, todos):
        res_structure = dict()
        for foldername in todos.keys():
            folder = todos[foldername]
            for name in folder.keys():
                res_structure[name] = foldername

        return res_structure

    def start_time_for_todo(self, name, reset=False):
        if name in self._structure.keys():
            folder = self._structure[name]
            todo = self._todos[folder][name]
            if 'time_taken' in todo.keys() and not(reset):
                timer = Timer(todo['done'], todo['time_taken'])
            else:
                timer = Timer(todo['done'])
            end, done = timer.print_elapsed()
            newtodo = {'time_taken': end}
            if done is not None:
                newtodo['done'] = done
            self.edit(name, newtodo)
        else:
            print "This todo doesn't exist"

    def reset_timer_for_todo(self, name):
        if name in self._structure.keys():
            folder = self._structure[name]
            todo = self._todos[folder][name]
            if 'time_taken' in todo.keys():
                newtodo = {'time_taken': '0:00:00'}
                self.edit(name, newtodo)
