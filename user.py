from random import randrange

class User:
    def __init__(self, pocketAmount, UserNumber, minBet, maxBet):
        self.UserNumber = UserNumber
        self.EOSpocket = pocketAmount
        self.CasinoTokenPocket = 0
        self.minBet = minBet
        self.maxBet = maxBet

    def bet(self):

        bet = randrange(self.minBet, self.maxBet)
        if self.EOSpocket <= self.minBet:
            self.EOSpocket = 0
        elif (self.EOSpocket - bet) <= 0:
            self.EOSpocket = 0
        else:
            self.EOSpocket -= bet
        return bet


    def grabToken(self, recievedToken):
        self.CasinoTokenPocket += recievedToken

    def grabReward(self, recievedReward):
        self.EOSpocket += recievedReward



