from clint.textui import puts, colored, indent

class TodoEditor(object):
    def __init__(self, todos):
        self._todos = todos  #object not data
        self._todosdata = self._todos.fetch_todos()

    def addflow(self):
        print ("\tThis is Dynamic Addflow, so to avoid write long lines in the \n"
               + "\tcommand line. Add a new todo: \n\n")


        task = raw_input("Whats the thing! (req): ").strip()
        bounty = int(raw_input("How much is the reward (integer):(" + str(1) + ") ") or 1)
        self._todos.add(task, bounty)

    def editflow(self, name):
        print ("\tThis is Dynamic EditFlow, so to avoid writing long lines in the \n"
               + "\tcommand line. Editing (" + name + "): \n\n" )

        assert name in self._todosdata.keys(), "No todo with name " + name + " in database."
        todo = self._todosdata[name]
        task = raw_input("Whats the thing! ("+todo['task'] +"): ").strip()

        bounty = int(raw_input("How much is the reward ("+str(todo['bounty'])+") :"))

        done = int(raw_input("1 if done, 0 if not done yet: ") or 0)
        done = bool(done)
        newtodo = {}

        if (task != '' or task != todo['task']):
            newtodo['task'] = task
        if (bounty != todo['bounty']):
            newtodo['bounty'] = bounty
        if (done != todo['done']):
            newtodo['done'] = done

        self._todos.edit(name, newtodo)
