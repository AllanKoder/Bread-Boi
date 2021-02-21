import numpy as np
import discord
from discord.ext import commands
import math
import random as rd
import os

if os.path.isfile('BreadSave.txt'):
    with open('BreadSave.txt', 'r') as f:
        People_Data = f.read()
        People_Data = People_Data.split(',')
        peoples = [x for x in People_Data if x.strip()]
        print(peoples)


client = commands.Bot(command_prefix='.')

xSize = 7
ySize = 5

BreadX = 0
BreadY = 0
BreadScore = 0

grid = np.zeros([ySize, xSize])
TotalDistance = 0
PlayerX = rd.randrange(1, xSize - 1)
PlayerY = rd.randrange(1, ySize - 1)
grid[PlayerY, PlayerX] = 3

def EntireBoard():
    for x in range(rd.randrange(1, 4, 1)):
        grid[0:ySize,0] = 1
        grid[0:ySize,xSize - 1] = 1
        grid[0,0:xSize] = 1
        grid[ySize - 1,0:xSize] = 1

        BreadX = rd.randrange(1, xSize - 1)
        BreadY = rd.randrange(1, ySize - 1)
        distanceX = math.fabs(PlayerX) - math.fabs(BreadX)
        distanceY = math.fabs(PlayerY) - math.fabs(BreadY)
        TotalDistance = math.fabs(distanceX) + math.fabs(distanceY)
        #create the bread position
        while TotalDistance < 1:
            BreadX = rd.randrange(1,xSize - 1)
            BreadY = rd.randrange(1,ySize - 1)
            distanceX = math.fabs(PlayerX) - math.fabs(BreadX)
            distanceY = math.fabs(PlayerY) - math.fabs(BreadY)
            TotalDistance = math.fabs(distanceX) + math.fabs(distanceY)
        grid[BreadY, BreadX] = 2


EntireBoard()
EntireBoard()

output = ""
game_exists = 0

user_name = ""
@client.event
async def on_message(message):
    global PlayerX
    global PlayerY
    global BreadScore
    global user_name

    user_name = message.author
    user = message.content.lower()
    channel = message.channel

    BreadScore = 0
    with open('BreadSave.txt', 'r') as f:
        People_Data = f.read()
        People_Data = People_Data.split(',')
        peoples = [x for x in People_Data if x.strip()]
        for peopleID in range(len(peoples)):
            if str(user_name) in peoples[peopleID]:
                BreadScore = int(peoples[peopleID].split(': ')[1])


    if user[0:5] == "bread":
        if user == "bread add":
            EntireBoard()
        if user == "bread down":
            if PlayerY < ySize - 2:
                grid[PlayerY, PlayerX] = 0
                if grid[PlayerY + 1, PlayerX] == 2:
                    BreadScore += 1
                    IncreaseBreadData()
                grid[PlayerY + 1, PlayerX] = 3
                PlayerY += 1
        elif user == "bread up":
            if PlayerY > 1:
                grid[PlayerY, PlayerX] = 0
                if grid[PlayerY - 1, PlayerX] == 2:
                    BreadScore += 1
                    IncreaseBreadData()
                grid[PlayerY - 1, PlayerX] = 3
                PlayerY -= 1
        elif user == "bread right":
            if PlayerX < xSize - 2:
                grid[PlayerY, PlayerX] = 0
                if grid[PlayerY, PlayerX + 1] == 2:
                    BreadScore += 1
                    IncreaseBreadData()
                grid[PlayerY, PlayerX + 1] = 3
                PlayerX += 1
        elif user == "bread left":
            if PlayerX > 1:
                grid[PlayerY, PlayerX] = 0
                if grid[PlayerY, PlayerX - 1] == 2:
                    BreadScore += 1
                    IncreaseBreadData()
                grid[PlayerY, PlayerX - 1] = 3
                PlayerX += -1
        elif user == "bread help":
            await channel.send("'Bread Add' to add bread to the board \n'Bread left' to move left"
                               "\n'Bread right' to move right\n'Bread up' to move up"
                               "\n'Bread down' to move down\n'Bread board' to see top leaderboard")
        elif user == "bread board":
            LeaderBoard = []
            with open('BreadSave.txt', 'r') as f:
                People_Data = f.read()
                People_Data = People_Data.split(',')
                peoples = [x for x in People_Data if x.strip()]
                Person_Value = []
                Person_Name = []
                Person_Both = []
                for x in range(len(peoples)):
                    Person_Value.append(peoples[x].split(': ')[1])
                    Person_Name.append(peoples[x].split(': ')[0][0:len(peoples[x]) - 8])
                    Person_Both.append(peoples[x].split(': ')[0][0:len(peoples[x]) - 8] + peoples[x].split(': ')[1])
                highestValue = 0
                endindex = 0
                for index in range(len(peoples)):
                    if int(Person_Value[index]) > highestValue:
                        highestValue = int(Person_Value[index])
                        endindex = index
                await channel.send("The Breadiest Gamer: " + "\n" + Person_Name[endindex] + ", Bread Score: " + Person_Value[endindex])

        if user != "bread" and user != "bread help" and user != "bread board":
            output = ""
            index = 0;
            for y in range(ySize):
                for x in range(xSize):
                    if grid[y, x] == 0:
                        output += ":black_large_square:"
                    elif grid[y, x] == 1:
                        output += ":orange_square:"
                    elif grid[y, x] == 2:
                        output += ":bread:"
                    elif grid[y, x] == 3:
                        output += ":levitate:"
                    index += 1
                    if index % xSize == 0 and index > 0:
                        output += "\n"
            await channel.send(output + "\n" + "Your Bread Score: " + str(BreadScore))
            print(grid)
            print(PlayerX, PlayerY)


def IncreaseBreadData():
    if os.path.isfile('BreadSave.txt'):
        with open('BreadSave.txt', 'r') as file:
            OldData = file.read()
            People_Data = OldData.split(',')
            print(People_Data)

            peoples = [x for x in People_Data if x.strip()]
            print(People_Data)
            print(peoples)
            inlist = 0
            list_value = 0
            PersonIn = 0
            Past_Data = []
            for Other_People in peoples:
                if str(user_name) in Other_People:
                    PersonIn += 1
                    pass
                else:
                    Past_Data.append(Other_People + ',')
            print(Past_Data)

            for peopleID in peoples:
                list_value += 1
                print("add values in list")
                if str(user_name) in peopleID:
                    inlist += 1
                    # Replace the Person's value for an increased one
                    Person_Value = int(peopleID.split(': ')[1])
                    with open('BreadSave.txt', 'w') as FileWrite:
                        past_Data = ""
                        for items in Past_Data:
                            past_Data += str(items)
                        FileWrite.write(past_Data + str(user_name) + ': ' + str(Person_Value + 1) + ',')
                    print("person is found")
                else:
                    # Other_People_Data += peoples + ','
                    pass
            if PersonIn == 0:
                with open('BreadSave.txt', 'w') as FileWrite:
                    print('New Person Added')
                    FileWrite.write(OldData + str(user_name) + ': ' + str(1) + ',')
                print("Adding New person to index")
            print("list value: " + str(list_value))

print(grid)
print(TotalDistance)


client.run("ODEyODQ2MTY5NDk4NzE0MTMy.YDGr_A.kQ6Y2rMqw460zPRSDmt_-M0vzEc")