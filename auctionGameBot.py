import random
import sys

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

class Bidding_bot(Strategy):
    def __init__(self):
        super(Bidding_bot, self).__init__("Bidding_bot")
        self.budget = 1000
        self.player_id = 0
        self.item = None
        self.give_up = False
        self.all_oppo_bids = []
        self.max_oppo_increase = 0

    def move(self, game_object):
        results = game_object.get('results')
        round = game_object.get('round')
        bids = game_object.get('bids')

        # We can't participate in this auction
        if not game_object.get('auction_active'):
            return game_object

        if self.give_up:
            game_object.set('last_move', 0)
            return game_object

        if round == 0: # Auction start
            self.give_up = False
            self.all_oppo_bids = []

            self.item = AuctionItem(game_object.get('item'))
            print("Item %s, valuation %d"%(self.item.name,self.item.valuation))
            # update budget if we won the auction
            if results:
                print("Round ended. Final bids: %s\n" % results)
                if max(results) == results[self.player_id]:
                    self.budget -= results[self.player_id]

            return self.first_move(game_object)
        else: # Rest of the rounds
            print(bids)
            self.process_bids(bids)
            next_bid = self.calc_next_bid(bids, round)
            game_object.set('last_move', next_bid)
            print("I play %d"%game_object.get('last_move'))
            return game_object

    def first_move(self, game_object):
        first_bid = int(1)
        if first_bid >= self.budget:
            game_object.set('last_move', 0)
        else:
            game_object.set('last_move', first_bid)

        return game_object

    def process_bids(self, bids):
        self.all_oppo_bids.append(bids[1:])
        self.calc_max_increase()

    def calc_max_increase(self):
        for i in range(len(self.all_oppo_bids) - 1):
            for j in range(3):
                increase = self.all_oppo_bids[i+1][j] - self.all_oppo_bids[i][j]
                if increase > self.max_oppo_increase:
                    self.max_oppo_increase = increase


    def calc_next_bid(self, bids, round):
        next_bid = 0
        max_bid = max(bids)

        if round is not 9:
            if max_bid + 1 < self.item.valuation:
                next_bid = max_bid + 1
            else:
                print("I give up")
                self.give_up = True
        else:
            if max_bid + int(self.max_oppo_increase * 1.2) < self.item.valuation:
                next_bid = max_bid + int(self.max_oppo_increase * 1.2)
            else:
                next_bid = self.item.valuation

        if next_bid > self.budget:
            raise NotImplementedError("This should never happen with a budget of 1000 and items worth 600")

        return next_bid


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


gameBot = AuctionGameBot(Bidding_bot())
gameBot.start(AuctionGameObject())
