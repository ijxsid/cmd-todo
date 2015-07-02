from clint.textui import puts, indent, colored

class Profile(object):

    def __init__(self, base, url, todos, rewards):
        self._url = url
        self._base = base
        self._profile = self._base.get(self._url, 'me')
        self._todos = todos.fetch_todos()
        self._rewards = rewards.fetch_rewards()

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
        for folder in self._todos.keys()

            for key in folder.keys():
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
        puts ( 'Total Points: ' +  colored.blue(str(self._profile['available'])))

        puts ( 'Points Earned: ' +  colored.green(str(self._profile['points'])))
        puts ( 'Rewards Redeemed: ' +  colored.green(str(self._profile['rewards_redeemed'])))
