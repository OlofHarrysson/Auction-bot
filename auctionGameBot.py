import random

from games.GameBot import GameBot
from games.GameObject import GameObject
from games.strategy import Strategy


class AuctionItem:
    def __init__(self, in_data):
        self.name = in_data[0]
        self.valuation = in_data[1]

    def payoff(self, price):
        return self.valuation - price

    def __str__(self):
        return "%s: %d" % (self.name, self.valuation)


class AuctionGameBot(GameBot):
    def __init__(self, strategy):
        super(AuctionGameBot, self).__init__('1', strategy)


class RandomAI(Strategy):
    def __init__(self):
        super(RandomAI, self).__init__("RandomAI")
        self.budget = 1000
        self.player_id = 0
        self.item = None
        self.give_up = False

    def move(self, game_object):
        results = game_object.get('results')
        round = game_object.get('round')
        bids = game_object.get('bids')

        # We can't participate in this auction
        if not game_object.get('auction_active'):
            return game_object

        # start of the auction?
        if round == 0:
            self.give_up = False
            # store the new item
            self.item = AuctionItem(game_object.get('item'))
            print("Item %s, valuation %d"%(self.item.name,self.item.valuation))
            # update budget if we won the auction
            if results:
                print("Round ended. Final bids: %s\n" % results)
                if max(results) == results[self.player_id]:
                    self.budget -= results[self.player_id]
            return self.first_move(game_object)
        elif self.give_up:
            game_object.set('last_move', 0)
            return game_object
        else:
            print(bids)
            if max(bids) + 1 < self.item.valuation - 1 <= self.budget:
                game_object.set('last_move', max(bids) + random.randint(1, 5))
                print("I play %d"%game_object.get('last_move'))
            else:
                print("I give up")
                game_object.set('last_move', 0)
                self.give_up = True
            return game_object

    def first_move(self, game_object):
        first_bid = self.item.valuation // random.randint(20, 30)
        if first_bid >= self.budget:
            game_object.set('last_move', 0)
        else:
            game_object.set('last_move', first_bid)
        return game_object


class AuctionGameObject(GameObject):
    def __init__(self):
        super(AuctionGameObject, self).__init__()
        self._elements_dict['round'] = None
        self._elements_dict['item'] = None
        self._elements_dict['results'] = None
        self._elements_dict['player_id'] = None
        self._elements_dict['last_move'] = 0
        self._elements_dict['bids'] = None  # 4 players
        self._elements_dict['score'] = None
        self._elements_dict['auction_active'] = True
        self._elements_dict['game_active'] = True


gameBot = AuctionGameBot(RandomAI())
gameBot.start(AuctionGameObject())
