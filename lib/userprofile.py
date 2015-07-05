from clint.textui import puts, indent, colored, progress
from goodtable import Goodtable
from profile_editor import ProfileEditor
class Profile(object):

    def __init__(self, base, url, todos, rewards):
        self._url = url
        self._base = base
        self._profile = self._base.get(self._url, 'me')
        self._todos = todos
        self._rewards = rewards.fetch_rewards()
        self._progress_bar_size = 30

    def update(self):
        todos = self._todos.fetch_todos()
        total_points, earned_points, total_items, items_done, rewards_redeemed = self._calculate_points(todos, main=True)
        user_profile = {'available': total_points, 'points': earned_points,
                        'done': items_done, 'total_items': total_items,
                        'rewards_redeemed': rewards_redeemed}
        if 'info' in self._profile.keys():
            user_profile['info'] = self._profile['info']
        self._base.put(self._url, 'me', user_profile)
        self._profile = self._base.get(self._url, 'me')

    def update_info_flow(self):
        profile_editor = ProfileEditor(self._profile)
        new_info = profile_editor.editflow()
        self._update_info(new_info)

    def _update_info(self, new_info):
        self._profile['info'] = new_info
        res = self._base.put(self._url, 'me', self._profile)

        print res


    def _calculate_points(self, todos, main=False):
        """
        calculates points and other things for a user.
        """
        total_points = 0
        earned_points = 0
        items_done = 0
        total_items = 0
        rewards_redeemed = 0

        for key in todos.keys():
            todo = todos[key]
            total_points += todo['bounty']
            earned_points += todo['bounty'] if todo['done'] else 0
            items_done += 1 if todo['done'] else 0
            total_items +=1
        if main:
            for key in self._rewards.keys():
                reward = self._rewards[key]
                redeemed = reward['redeemed']
                bounty = reward['bounty']
                earned_points -= redeemed * bounty
                rewards_redeemed +=1
        else:
            rewards_redeemed = None
        return (total_points, earned_points, total_items, items_done, rewards_redeemed)


    def show_profile(self):
        """
        prints out user Dashboard.
        """
        if 'info' in self._profile.keys():
            print "="*80
            print "Name: " + self._profile['info']['name']
            print "Email: " + self._profile['info']['email']
            print "="*80
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

        folderstable = Goodtable([80], "Folders/Projects Progress")
        folderstable.print_table()
        print "\n"
        self._print_dash(folder=True)

        print "\n\n"
        tagstable = Goodtable([80], 'Tags Progress')
        tagstable.print_table()
        print "\n"
        self._print_dash(folder=False)

    def _print_dash(self, folder=True):
        if folder:
            todos = self._todos.fetch_folderwise_todos()
        else:
            todos = self._todos.fetch_tagwise_todos()
        for foldername in todos.keys():
            folder = todos[foldername]
            points, earned, items, done, _ = self._calculate_points(folder)
            table = Goodtable([30, 50],  foldername.capitalize())
            percent_done = (done/float(items))*100
            progress_bar_done = self._print_progress_bar("Label", percent_done, 20)[1]

            table.add_row(['Tasks', "{:10}".format(str(done) + "/" + str(items)) + progress_bar_done ])
            percent_points = (earned/float(points))*100
            progress_bar_points = self._print_progress_bar("Label", percent_points, 20)[1]
            table.add_row(['XP Points', "{:10}".format(str(earned) + "/" + str(points)) + progress_bar_points ])
            table.print_table()


    def _print_progress_bar(self, label, percent, width=None, ex_size=100):
        if width is None:
            size = self._progress_bar_size
        else:
            size = width
        scale = float(size)/ex_size
        bar_size = int(scale*percent)
        bar = '#'* bar_size + ">" + ' '*(size-bar_size-1) if bar_size < size-1 else '#'*bar_size
        percent_string = "{:.2%}".format(percent/100)
        return [label , '['+ (bar)  +']' + percent_string]
