from clint.textui import puts, colored, indent
from utils import Counter, foreach, print_reward_item

class Rewards(object):

    def __init__(self, base, url, countername='rewardcount'):
        self._base = base
        self._url = url
        self._rewards = self._base.get(url, None)
        self._counter = Counter(countername, self._base)


    def _update(self):
        self._rewards = self._base.get(self._url, None)

    def fetch_rewards(self):
        return self._rewards

    def get_all(self):
        foreach(self._rewards, print_reward_item)

    def get(self, name):
        print_reward_item(self._rewards[name], name)

    def add(self, reward, bounty):
        N = self._counter.get()
        name = 'rw' + str(N+1)
        todo = {'reward': reward, 'bounty': bounty, 'redeemed':0}
        res = self._base.put(self._url, name, todo)
        print res
        self._update()

    def redeem(self, name, times=1):
        reward = self._rewards[name]
        assert isinstance(times, int), "times should be an Integer Value."
        newreward = {'redeemed': reward['redeemed'] + times}
        self.edit(name, newreward)

    def edit(self, name, newreward):
        # TODO: Need to find a better way to print responses.
        if name in self._rewards.keys():
            res = self._base.patch(self._url + "/" +  name , newreward)
            print res
        else:
            print "Not Found"
        self._update()

    def delete(self, name):
        if name in self._rewards.keys():
            res = self._base.delete(self._url, name)
            print res
        else:
            print "Not Found. Can't Delete"
        self._update()
