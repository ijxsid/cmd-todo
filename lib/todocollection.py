from utils import foreach, print_todo_item, Counter

class TodoCollection(object):

    def __init__(self, base, url, countername='todo'):
        self._base = base
        self._url = url
        self._todos = self._base.get(url, None)
        self._counter = Counter(countername, self._base)

    def _update(self):
        self._todos = self._base.get(self._url, None)

    def fetch_todos(self):
        return self._todos

    def get_all(self):
        foreach(self._todos, print_todo_item)

    def get(self, name):
        print_todo_item(self._todos[name], name)

    def add(self, task, bounty):
        assert isinstance(task, str)
        assert len(task) > 0, "Task Cannot be left empty."
        assert isinstance(bounty, int)
        N = self._counter.get()
        name = 'todo' + str(N+1)
        todo = {'task': task, 'bounty': bounty, 'done': False}
        res = self._base.put('/todos', name, todo)
        print res
        self._update()

    def markdone(self, name):
        self.edit(name, {'done': True})

    def edit(self, name, newtodo):
        # TODO: Need to find a better way to print responses.
        if name in self._todos.keys():
            res = self._base.patch(self._url + "/" +  name , newtodo)
            print res
        else:
            print "Not Found"
        self._update()

    def delete(self, name):
        if name in self._todos.keys():
            res = self._base.delete(self._url, name)
            print res
        else:
            print "Not Found. Can't Delete"
        self._update()
