from clint.textui import puts, indent, colored, progress

class Profile(object):

    def __init__(self, base, url, todos, rewards):
        self._url = url
        self._base = base
        self._profile = self._base.get(self._url, 'me')
        self._todos = todos.fetch_todos()
        self._rewards = rewards.fetch_rewards()
        self._progress_bar_size = 40

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

        puts ( 'Total Items: ' +  colored.blue(str(self._profile['total_items'])))
        puts ( 'Total Done: ' +  colored.green(str(self._profile['done'])))
        percent_done = (self._profile['done'] / float(self._profile['total_items']))*100
        puts (self._print_progress_bar('Done', percent_done))
        puts ( 'Total Points: ' +  colored.blue(str(self._profile['available'])))

        puts ( 'Points Earned: ' +  colored.green(str(self._profile['points'])))
        percent_points = (self._profile['points'] / float(self._profile['available']))*100
        puts ( self._print_progress_bar('Points gained', percent_points ))
        puts ( 'Rewards Redeemed: ' +  colored.green(str(self._profile['rewards_redeemed'])))

    def _print_progress_bar(self, label, percent, ex_size=100):
        size = self._progress_bar_size
        scale = float(size)/ex_size
        bar_size = int(scale*percent)
        bar = '#'* bar_size + ">" + ' '*(size-bar_size-1) if bar_size < size-1 else '#'*bar_size
        return label + ': ['+ colored.green(bar)  +']'
