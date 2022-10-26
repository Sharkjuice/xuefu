from random import randint

#create a list of play options
t = ["石头", "布", "剪刀"]

#assign a random play to the computer
computer = t[randint(0,2)]

#set player to False
player = False

while player == False:
#set player to True
    player = input("石头, 布, 剪刀?")
    if player == computer:
        print("Tie!")
    elif player == "石头":
        if computer == "布":
            print("你输了!", computer, "包住", player)
        else:
            print("你赢了!", player, "打碎", computer)
    elif player == "布":
        if computer == "剪刀":
            print("你输了!", computer, "剪断", player)
        else:
            print("你赢了!", player, "包住", computer)
    elif player == "剪刀":
        if computer == "石头":
            print("你输了...", computer, "打碎", player)
        else:
            print("你赢了!", player, "剪断", computer)
    else:
        print("拼写不合法, 请检查是不是石头剪刀布.")
    #player was set to True, but we want it to be False so the loop continues
    player = False
    computer = t[randint(0,2)]