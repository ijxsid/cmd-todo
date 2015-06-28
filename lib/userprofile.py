from clint.textui import puts, indent, colored

class Profile(object):

    def __init__(self, todos):
        self._todos = todos.fetch_todos()
        points = self._calculate_points()
        self._total_points = points[0]
        self._earned_points = points[1]
        self._total_items = points[2]
        self._items_done = points[3]

    def _calculate_points(self):
        """
        calculates points and other things for a user.
        """
        total_points = 0
        earned_points = 0
        items_done = 0
        total_items = 0
        for key in self._todos.keys():
            todo = self._todos[key]
            total_points += todo['bounty']
            earned_points += todo['bounty'] if todo['done'] else 0
            items_done += 1 if todo['done'] else 0
            total_items +=1

        return (total_points, earned_points, total_items, items_done)


    def show_profile(self):
        """
        prints out user Dashboard.
        """
        puts ( 'Total Items: ' +  colored.blue(str(self._total_items)))
        puts ( 'Total Done: ' +  colored.green(str(self._items_done)))
        puts ( 'Total Points: ' +  colored.blue(str(self._total_points)))

        puts ( 'Points Earned: ' +  colored.green(str(self._items_done)))
