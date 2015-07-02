from clint.textui import puts, colored, indent
from datetime import datetime, timedelta
import re
class TodoEditor(object):
    def __init__(self, todos):
        self._todos = todos  #object not data
        self._todosdata = self._todos.fetch_todos()

    def addflow(self):
        print ("\tThis is Dynamic Addflow, so to avoid write long lines in the \n"
               + "\tcommand line. Add a new todo: \n\n")


        task = raw_input("Whats the thing! (req): ").strip()
        bounty = int(raw_input("How much is the reward (integer):(" + str(1) + ") ") or 1)
        due = raw_input("When its' due? (YYYY-MM-DD HH:mm)/ +(due_rules): ")
        due_datetime = None
        if (due):
            due_datetime = self._parse_due(due)
        tags = raw_input("Tags (comma seprated): ").strip().split(',')
        tags = self._clean_tags(tags)

        self._todos.add(task, bounty, due_datetime, tags)

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

    def _parse_due(self, duestring):
        if duestring[0] in ['+', '-']:
            """
            That means the duestring is of the format [+,-][0-9][hdwmy]

            """
            pattern = re.compile('(\+|\-)([0-9]+)([Mhdwmy])')
            matches = pattern.findall(duestring)
            time_now = datetime.now()
            due_datetime = time_now
            for match in matches:
                sign = match[0]
                n = int(match[1])
                unit = match[2]
                if unit == 'h':
                    delta = timedelta(hours=n)
                elif unit == 'M':
                    delta = timedelta(minutes=n)
                elif unit == 'd':
                    delta = timedelta(days=n)
                elif unit == 'w':
                    delta = timedelta(weeks=n)
                elif unit == 'm':
                    delta = timedelta(days=n*30)
                elif unit == 'y':
                    delta = timedelta(days=n*365)
                else:
                    delta = timedelta(days=0)

                if sign == '+':
                    due_datetime += delta
                else:
                    due_datetime -= delta
            return due_datetime

        else:
            date_format = '%Y-%m-%d'
            due_datetime = datetime.strptime(duestring, date_format)
            return due_datetime

    def _clean_tags(self, tags):
        pattern = re.compile('\s*(\w+)')
        res = []
        for tag in tags:
            match = pattern.match(tag)
            res.append(match.group(1))
        return res
