from utils import foreach, print_todo_item, Counter
from datetime import datetime

class TodoCollection(object):

    def __init__(self, base, url, countername='todo'):
        self._base = base
        self._url = url
        self._todos = self._base.get(url, None)
        self._counter = Counter(countername, self._base)
        self._structure = self._make_folder_structure(self._todos)

    def _update(self):
        # TODO: unimplemented for folders
        self._todos = self._base.get(self._url, None)

    def fetch_structure(self):
        return self._structure

    def fetch_todos(self):
        # TODO: unimplemented for folders
        return self._todos

    def get_all(self, tags=None):
        # TODO: unimplemented for folders
        res_todos = self._todos
        if tags:
            res_todos = {key: self._todos[key]  for key in self._todos.keys() if self._is_tagged(key, tags)}
        foreach(res_todos, print_todo_item)

    def get(self, name):
        """
        get foldername from name and then look for todo with the given name
        inside the folder.
        """
        foldername = self._structure[name]
        print_todo_item(self._todos[foldername][name], name)

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
        # TODO: unimplemented for folders
        self.edit(name, {'done': True})

    def edit(self, name, newtodo):
        # TODO: unimplemented for folders
        # TODO: Need to find a better way to print responses.
        if name in self._todos.keys():
            res = self._base.patch(self._url + "/" +  name , newtodo)
            print res
        else:
            print "Not Found"
        self._update()

    def delete(self, name):
        # TODO: unimplemented for folders
        if name in self._todos.keys():
            res = self._base.delete(self._url, name)
            print res
        else:
            print "Not Found. Can't Delete"
        self._update()

    def _is_tagged(self, key, tags):
        # TODO: unimplemented for folders
        try:
            item_tags = self._todos[key]['tags']
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
