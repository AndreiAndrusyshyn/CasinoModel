import pandas as pd
from random import choice
from user import User
from casino import Casino



def generateUsers(numberOfUsers, minBet, maxBet):
    ListOfUsers = []
    UserPocket = [10000, 100000, 500000]
    for i in range(0, numberOfUsers):
        ListOfUsers.append(User(choice(UserPocket), i, minBet, maxBet))
    return ListOfUsers


MinBet = 1000
MaxBet = 1001
TokenLimit = 1000000000
ProcentFromTotalCoinsMining = 0.85
DefaultProcent = 0.05

DataForWrite = pd.DataFrame()
writer = pd.ExcelWriter('user_data.xlsx', engine='xlsxwriter')
writer_d = pd.ExcelWriter('detailed_game.xlsx', engine='xlsxwriter')


for i in range(0, 7):
    NumberOfUsers = 1000000000
    Flag = 0
   # while not Flag:
    winCount = 0
    winRate = 0
    user = generateUsers(NumberOfUsers, MinBet, MaxBet)
    if i == 6:
        i = 10
    Strategy = Casino(user, i, TokenLimit, ProcentFromTotalCoinsMining,DefaultProcent)
    
    returnedData = Strategy.playGame()
    
    GamesData = pd.DataFrame(returnedData['Casino'])
    
    SummaryData = pd.DataFrame(returnedData['Summary'])
    if  not NumberOfUsers % 100:
        print(NumberOfUsers)
    if SummaryData['MiningStatus'][0] == 'Mined':
        print("Strategy "+ str(i) + "Minned")
        Flag = 1
        DetailedGame = pd.DataFrame(returnedData['DetailedGame'])
        DetailedGame = DetailedGame.drop_duplicates()
        for k in range(0, len(GamesData)):
            if GamesData['UserResult'][k] == 'Win':
                winCount += 1
        winRate = (winCount / len(GamesData)) * 100
        winRatedf = pd.DataFrame({"winRate": [winRate]})
    
        SummaryData.insert(4, "winRate", str(winRate) + "%")
        if i == 10:
            SummaryData.insert(4, "Strategy", "autobet")
        else:
            SummaryData.insert(4, "Strategy", "N "+str(i))
        
        SummaryData.insert(5, "TotalUsers", str(NumberOfUsers-1))
        DataForWrite = DataForWrite.append(SummaryData)
        if i == 10:
            GamesData.to_excel(writer, sheet_name='Autobet')
            DetailedGame.to_excel(writer_d, sheet_name='Autobet')
        else:
            GamesData.to_excel(writer, sheet_name='Strategy'+str(i))
            DetailedGame.to_excel(writer_d, sheet_name='Strategy'+str(i))
                #break
    #    else:
     #       NumberOfUsers += 1
         
   

DataForWrite.to_excel(writer, sheet_name='Summary')
writer_d.save()
writer.save()

