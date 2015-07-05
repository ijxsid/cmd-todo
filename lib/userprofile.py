from clint.textui import puts, indent, colored, progress
from goodtable import Goodtable

class Profile(object):

    def __init__(self, base, url, todos, rewards):
        self._url = url
        self._base = base
        self._profile = self._base.get(self._url, 'me')
        self._todos = todos.fetch_todos()
        self._rewards = rewards.fetch_rewards()
        self._progress_bar_size = 30

    def update(self):
        total_points, earned_points, total_items, items_done, rewards_redeemed = self._calculate_points()
        user_profile = {'available': total_points, 'points': earned_points,
                        'done': items_done, 'total_items': total_items,
                        'rewards_redeemed': rewards_redeemed}
        self._base.put(self._url, 'me', user_profile)
        self._profile = self._base.get(self._url, 'me')



    def _calculate_points(self):
        """
        calculates points and other things for a user.
        """
        total_points = 0
        earned_points = 0
        items_done = 0
        total_items = 0
        rewards_redeemed = 0

        for key in self._todos.keys():
            todo = self._todos[key]
            total_points += todo['bounty']
            earned_points += todo['bounty'] if todo['done'] else 0
            items_done += 1 if todo['done'] else 0
            total_items +=1
        for key in self._rewards.keys():
            reward = self._rewards[key]
            redeemed = reward['redeemed']
            bounty = reward['bounty']
            earned_points -= redeemed * bounty
            rewards_redeemed +=1

        return (total_points, earned_points, total_items, items_done, rewards_redeemed)


    def show_profile(self):
        """
        prints out user Dashboard.
        """
        table = Goodtable([30, 50], "Your Dashboard")
        table.add_row(['Total Tasks', str(self._profile['total_items'])] )
        table.add_row(['Total Done', str(self._profile['done'])])
        percent_done = (self._profile['done'] / float(self._profile['total_items']))*100
        table.add_row( self._print_progress_bar('Done', percent_done))
        table.add_row(['Available Points', str(self._profile['available'])])
        table.add_row(['Points Earned', str(self._profile['points'])])

        percent_points = (self._profile['points'] / float(self._profile['available']))*100
        table.add_row( self._print_progress_bar('XP Level', percent_points))


        table.add_row(['Rewards Redeemed', str(self._profile['rewards_redeemed'])])

        table.print_table()
        
    def _print_progress_bar(self, label, percent, ex_size=100):
        size = self._progress_bar_size
        scale = float(size)/ex_size
        bar_size = int(scale*percent)
        bar = '#'* bar_size + ">" + ' '*(size-bar_size-1) if bar_size < size-1 else '#'*bar_size
        percent_string = "{:.2%}".format(percent/100)
        return [label , '['+ (bar)  +']' + percent_string]
