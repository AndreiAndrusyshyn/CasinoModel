import numpy as np

class Casino:
    
    def __init__(self, UserList, LevelPlaying, TokenLimit, ProcentFromTotalCoinsMining, DefaultProcent):
        self.CasinoBetPool = 0
        self.CasinoTokenPool = 0
        self.CasinoNumbers = []
        self.UserNumbers = []
        self.coefficient = 1.428
        self.UserBet = 0
        self.data = {}
        self.data['Casino'] = []
        self.data['Summary'] = []
        self.data['DetailedGame'] = []
        self.UserList = UserList
        self.LevelPlaying = LevelPlaying
        self.CasinoTokenLimit = TokenLimit
        self.ProcentFromTotalCoinsMining = ProcentFromTotalCoinsMining
        self.procent = []
        self.fix = 100
        self.TokensMax = list(range(1000000, 1000000000,1000000))
        self.defaultProcent = DefaultProcent
      #  self.calculatelistofprocent()
        
    def calculatelistofprocent(self):
        while len(self.procent) < len(self.TokensMax):
                self.fix = self.fix - (self.fix * self.defaultProcent)
                self.procent.append(int(self.fix+0.85))
                
    def make_roll(self):
        rollArray = np.random.randint(1, 4, size=10, dtype=np.uint8)
        return rollArray

    def playGame(self):
        GameCounter = 0
        if not (self.LevelPlaying):
            self.LevelPlaying = 10

        for i in range(0,len(self.UserList)):
            while self.UserList[i].EOSpocket > 0:
                GameCounter +=1
                self.CasinoNumbers = self.make_roll()
                self.UserNumbers = self.make_roll()
                self.UserBet = self.UserList[i].bet()
                IntialUserBet = self.UserBet
                
          
            for k in range(0, self.LevelPlaying):
                #if self.CasinoTokenPool % 100000 == 0:
                print(self.CasinoTokenPool)
                if self.CasinoTokenPool >= 799999998:
                    print(self.calculateTokenLimit())
                    print(self.CasinoTokenPool)
                    self.data['Summary'].append({
                'TotalGames':GameCounter,
                'TotalUserPlayed': len(self.UserList)-1,
                'CasinoEosPocket':self.CasinoBetPool,
                'CasinoTokenPocket': self.UserList[i].CasinoTokenPocket,
                'MiningStatus': 'Mined',
                        })
                    return self.data
                if self.CasinoNumbers[k] != self.UserNumbers[k]:

                    self.CasinoTokenPool += self.calculateRecievedTokens(k+1, self.UserBet, IntialUserBet)
                    self.UserList[i].grabToken(self.calculateRecievedTokens(k+1, self.UserBet, IntialUserBet))
                   
                    self.UserBet *= self.coefficient
                        
                    self.data['DetailedGame'].append({
                            'UserNumber': i,
                            'GameLevel': k+1,
                            'UserResult': 'Win',
                            'InitialUserBet': IntialUserBet,
                            'UserBetWhenStop': self.UserBet,
                            'UserEarnedTokens': self.UserList[i].CasinoTokenPocket,
                            'CasinoToken': self.CasinoTokenPool,
                            'CasinoEOS': self.CasinoBetPool,
                            'CUserNumbers': str(self.UserNumbers),
                            'CasinoNumbers': str(self.CasinoNumbers),

                        })
                    if k == self.LevelPlaying-1:
                        self.UserList[i].EOSpocket += self.UserBet - IntialUserBet
                        self.CasinoBetPool -= self.UserBet -IntialUserBet
                        self.data['Casino'].append({
                            'UserNumber': i,
                            'GameLevel': k+1,
                            'UserResult': 'Win',
                            'InitialUserBet': IntialUserBet,
                            'UserBetWhenStop': self.UserBet,
                            'UserEarnedTokens': self.UserList[i].CasinoTokenPocket,
                            'CasinoToken': self.CasinoTokenPool,
                            'CasinoEOS': self.CasinoBetPool,

                        })
                        self.data['DetailedGame'].append({
                            'UserNumber': i,
                            'GameLevel': k+1,
                            'UserResult': 'x-Win',
                            'InitialUserBet': IntialUserBet,
                            'UserBetWhenStop': self.UserBet,
                            'UserEarnedTokens': self.UserList[i].CasinoTokenPocket,
                            'CasinoToken': self.CasinoTokenPool,
                            'CasinoEOS': self.CasinoBetPool,
                            'CUserNumbers': str(self.UserNumbers),
                            'CasinoNumbers': str(self.CasinoNumbers),

                        })
                        break

                else:
                    self.CasinoBetPool += IntialUserBet
                    self.UserList[i].EOSpocket -= IntialUserBet

                    self.CasinoTokenPool += self.calculateRecievedTokens(k+1, self.UserBet, IntialUserBet)
                    self.UserList[i].grabToken(self.calculateRecievedTokens(k+1, self.UserBet, IntialUserBet))
                    self.data['DetailedGame'].append({
                            'UserNumber': i,
                            'GameLevel': k+1,
                            'UserResult': 'Lose',
                            'InitialUserBet': IntialUserBet,
                            'UserBetWhenStop': self.UserBet,
                            'UserEarnedTokens': self.UserList[i].CasinoTokenPocket,
                            'CasinoToken': self.CasinoTokenPool,
                            'CasinoEOS': self.CasinoBetPool,
                            'CUserNumbers': str(self.UserNumbers),
                            'CasinoNumbers': str(self.CasinoNumbers),

                        })
                    self.data['Casino'].append({
                        'UserNumber': i,
                        'GameLevel': k+1,
                        'UserResult': 'Lose',
                        'InitialUserBet': IntialUserBet,
                        'UserBetWhenStop': self.UserBet,
                        'UserEarnedTokens': self.UserList[i].CasinoTokenPocket,
                        'CasinoToken': self.CasinoTokenPool,
                        'CasinoEOS': self.CasinoBetPool,

                    })
        
                    break
        if i == len(self.UserList)-1:
            self.data['Summary'].append({
                'TotalGames':GameCounter,
                'TotalUserPlayed': len(self.UserList)-1,
                'CasinoEosPocket':self.CasinoBetPool,
                'CasinoTokenPocket': self.UserList[i].CasinoTokenPocket,
                'MiningStatus': 'NotEnough',
            })
        return self.data

    def calculateRecievedTokens(self, LevelPlaying, Bet, InitialUserBet):
     #   MiningRate = 1.05
       StartMiningRate = 100
       return Bet*(StartMiningRate*(800000000-self.CasinoTokenPool)/800000000)
       # for i in range(0, len(self.TokensMax)-1):
        #    if self.CasinoTokenPool >= self.TokensMax[i] and self.CasinoTokenPool <= self.TokensMax[i+1]:
         #       StartMiningRate = StartMiningRate * (self.procent[i]/100)
        
        #if LevelPlaying == 1:
            #return StartMiningRate * InitialUserBet
        #else:
          #  return (Bet/InitialUserBet)*(MiningRate**(LevelPlaying-1))*(StartMiningRate*InitialUserBet)
       

    def calculateTokenLimit(self):
        return self.CasinoTokenLimit*self.ProcentFromTotalCoinsMining


