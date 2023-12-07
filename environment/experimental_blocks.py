import numpy as np
import itertools
import pandas as pd
from datetime import datetime

class DataLogger():
    def __init__(self):
        self.df = pd.DataFrame(columns=[
            'TimePressure',
            'PlayerCard1',
            'PlayerCard2',
            'DealerCard',
            'ResponseTime',
            'Response'])
        # self.df['TimePressure'] = [] # player informed of time pressure [y,n]
        # self.df['PlayerCard1'] = [] # first player card [2,10]
        # self.df['PlayerCard2'] = [] # second player card [2,10]
        # self.df['DealerCard'] = [] # dealer hand [2,10]
        # self.df['ResponseTime'] = [] # response time [sec]
        # self.df['Response'] = []  # response of player to take anouther card [y/n]

        now = datetime.now()
        self.filename = now.strftime("data_%m-%d-%Y_%H-%M-%S")

    def log(self,time_pressure,player_hand, dealer_hand,response_time,response):
        new_entry = pd.DataFrame({
            'TimePressure': [time_pressure],
            'PlayerCard1':[ player_hand[0]],
            'PlayerCard2': [player_hand[1]],
            'DealerCard': [dealer_hand],
            'ResponseTime': [response_time],
            'Response': [response]
        })
        self.df = self.df.append(new_entry)
    def save(self):
        self.df.to_csv(self.filename,index=False)
        print(f'Saved [{self.filename}]...')

    def print(self):
        print(self.df)




class BlackJack():
    def __init__(self):
        """INITIALIZE blackjack experimental block"""
        # self.dealer_sums = np.arange(2,11)
        # self.player_sums = np.arange(4,21)
        self.dealer_sums = np.arange(2, 11)
        self.player_sums = np.arange(12, 20)
        self.hand_sums = list(itertools.product(*[self.player_sums, self.dealer_sums]))
        np.random.shuffle(self.hand_sums)

        self.num_hands = np.shape(self.hand_sums)[0]
        self.hand_index = 0

    def sum2cards(self,card_sum):
        """convert sum to player cards"""
        for _ in itertools.count():
            c1 = np.random.choice(np.arange(2,11))
            if c1 <= card_sum -2 and (card_sum - c1 <= 10 and card_sum - c1 >= 2):
                break
        c2 = card_sum - c1
        return c1, c2

    def get_hand(self,hand_index=None):
        """ get card values for shuffled list of blackjack hands given experimental constraints"""
        i = self.hand_index if hand_index == None else hand_index
        player_cards = self.sum2cards(self.hand_sums[i][0])
        dealer_card = self.hand_sums[i][1]
        self.hand_index += 1 if hand_index==None else 0
        return player_cards,dealer_card
    def add_hand(self, player_cards,dealer_card):
        self.hand_sums.append([player_cards[0]+player_cards[1],dealer_card])
        self.num_hands = np.shape(self.hand_sums)[0]


if __name__ == "__main__":
    BJ = BlackJack()


    # print(np.arange(2,11))
    for i in range(70):
    #     print(BJ.get_hand())
        print(BJ.sum2cards(17))
