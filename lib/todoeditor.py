from clint.textui import puts, colored, indent
from utils import parse_duestring, clean_tags, clean_foldername
import re
class TodoEditor(object):
    def __init__(self, todos):
        self._todos = todos  #object not data
        self._todosdata = self._todos.fetch_todos()
        self._todostructure = self._todos.fetch_structure()

    def addflow(self):
        print ("\tThis is Dynamic Addflow, so to avoid write long lines in the \n"
               + "\tcommand line. Add a new todo: \n\n")

        try:
            task = raw_input("Whats the thing! (req): ").strip()
            if task in ['', ' ']:
                raise ValueError
        except ValueError, e:
            raise ValueError(colored.red("Task cannot be left Empty"))

        try:
            bounty = int(raw_input("How much is the reward (integer):(" + str(1) + ") ") or 1)
        except ValueError, e:
            raise ValueError(colored.red("Bounty should be an integer"))

        try:
            due = raw_input("When its' due? (YYYY-MM-DD HH:mm)/ +(due_rules): ").strip()
            due_datetime = None
            if (due):
                due_datetime = parse_duestring(due)
        except ValueError, e:
            raise ValueError(colored.red("Bad Date Fomat: Expected Formats (YYYY-MM-DD or due_rules)"))

        tags = raw_input("Tags (comma seprated): ").strip().split(',')
        tags = clean_tags(tags)
        foldername = raw_input("Folder/Project :" ).strip()
        foldername = clean_foldername(foldername)

        self._todos.add(task, bounty, due_datetime, tags, foldername)

    def editflow(self, name):
        print ("\tThis is Dynamic EditFlow, so to avoid writing long lines in the \n"
               + "\tcommand line. Editing (" + name + "): \n\n" )

        assert name in self._todosdata.keys(), "No todo with name " + name + " in database."
        todo = self._todosdata[name]
        task = raw_input("Whats the thing! ("+todo['task'] +"): ").strip()
        try:
            bounty = int(raw_input("How much is the reward ("+str(todo['bounty'])+") :") or todo['bounty'])
        except ValueError, e:
            raise ValueError(colored.red("Bounty should be an integer"))
        try:
            done = int(raw_input("1 if done, 0 if not done yet: ") or todo['done'])
            if done not in [1, 0]:
                raise ValueError
            done = bool(done)
        except ValueError, e:
            raise ValueError(colored.red("Done should either be 1 or 0"))
        # due_datetime handling
        try:
            duestring = 'None'
            if 'due' in todo.keys():
                duestring = todo['due']
            due = raw_input("When its' due? (Prev: "+ duestring +" ): ").strip()
            due_datetime = None
            if (due):
                due_datetime = parse_duestring(due)
        except ValueError, e:
            raise ValueError(colored.red("Bad Date Fomat: Expected Formats (YYYY-MM-DD or due_rules)"))

        # tags_handling
        tag_string = 'None'
        if 'tags' in todo.keys():
            tag_string = ", ".join(todo['tags'])
        tags = raw_input("Tags (Prev: "+tag_string+" )\n New: ").strip().split(',')
        tags = clean_tags(tags)
        # folder_handling
        folder = self._todostructure[name]
        newfolder = raw_input("Folder (Prev: "+ folder +" ): ").strip()
        newfolder = clean_foldername(newfolder)

        newtodo = {}

        if (task != '' and task != todo['task']):
            newtodo['task'] = task
        if (bounty != todo['bounty']):
            newtodo['bounty'] = bounty
        if (done != todo['done']):
            newtodo['done'] = done
        if (tags != []):
            newtodo['tags'] = tags
        if (due_datetime is not None):
            newtodo['due'] = due_datetime

        self._todos.edit(name, newtodo)
        if (newfolder != ''):
            self._todos.move_to_folder(newfolder, name)
