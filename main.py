from datetime import datetime, timedelta
import random
import os
import json

# starting values
money = 500
health = 100
seeds = 0
crops = 0
planted = 0
start = None
growth = timedelta(minutes=30)

SAVE_FILE = "save"

def save():
    global money, seeds, crops
    game_data = {
        "money": money,
        "seeds": seeds,
        "planted": planted,
        "start": start,
        "health": health
    }
    with open(SAVE_FILE, 'w') as file:
        json.dump(game_data, file)

def load():
    global money, seeds, crops
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as file:
            game_data = json.load(file)
            money = game_data["money"]
            seeds = game_data["seeds"]
            planted = game_data["planted"]
            start = game_data["start"]
            health = game_data["health"]
    else:
        save()
        main()

def clear(): # clear console
    os.system('cls' if os.name == 'nt' else 'clear')

def time(): # print time
    now = datetime.now()
    hora = datetime.now().hour
    if 7 <= hora < 19:
        estado = "day"
    else:
        estado = "night"
    current_time = now.strftime("%H:%M")
    print(f"\rcurrent time: {current_time} ({estado})")

def casino():
    global money, seeds, crops
    clear()
    print("CASINO")
    print("[1] dice")
    print("[2] SOON")
    print("[3] SOON")
    print("[4] city")
    print("")
    print("STATS")
    print("money: " + str(money) + "$")
    print("seeds: " + str(seeds))
    print("crops: " + str(crops))
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        casino()
    if option == "1": # DICE GAME
        clear()
        try:
            bet = int(input("bet ammount: "))
        except ValueError:
            print("Invalid Value!")
            input()
            casino()
        if bet > money:
            print("You dont have that kind of money!")
            input()
            casino()
        else:
            try:
                guess = int(input("choose a number between 1 and 6: "))
            except ValueError:
                clear()
                print("invalid value!")
                input()
                casino()
            number = random.randint(1, 6)
            if guess == number:
                clear()
                prize = bet*2
                print("you guessed the number and got " + str(prize) + "$")
                money += prize
                input()
                casino()
            else:
                clear()
                print("you guessed " + str(guess) + " but the number was " + str(number))
                print("you lost " + str(bet) + "$")
                money -= bet
                input()
                casino()
    elif option == "2":# SOON
        casino()
    elif option == "3":# SOON
        casino()
    elif option == "4":# MAIN
        city()
    else:
        casino()

def farm():
    global money, seeds, crops, time, planted, start, growth, now
    clear()
    print("FARM")
    print("[1] seed")
    print("[2] harvest")
    print("[3] home")
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        farm()
    if option == "3":
        main()
    elif option == "1": # plant
        clear()
        planted += seeds
        print("planted " + str(seeds) + " seeds!")
        start = datetime.now()
        seeds = 0
        input()
        farm()
    elif option == "2":
        clear()
        if start == None:
            print("you have to plant!!")
            input()
            farm()
        else:
            age = datetime.now() - start
            cooked = age + timedelta(hours=1)
            if age >= growth and age < cooked:
                crops += planted
                earnings = crops * 2
                money += earnings
                print("harvested " + str(crops) + " crops and made " + str(earnings) + "$")
                crops = 0
                start = None
                input()
                farm()
            elif age > cooked:
                planted = 0
                print("you let your crops rot\nage: " + str(age))
                start = None
                input()
                farm()
            else:
                print("your crops are not ready yet\nage: " + str(age))
                input()
                farm()
    else:
        farm()

def store():
    global money, seeds, crops
    clear()
    print("FARM")
    print("[1] buy 500 seeds - 500$")
    print("[2] buy 1000 seeds - 800$")
    print("[3] city")
    print("")
    print("STATS")
    print("money: " + str(money))
    print("seeds: " + str(seeds))
    print("crops: " + str(crops))
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        store()
    if option == "3":
        city()
    elif option == "1":
        clear()
        if money >= 500:
            money = money - 500
            seeds = seeds + 500
            store()
        else:
            clear()
            print("you are too poor")
            input()
            store()
    elif option == "2":
        clear()
        if money >= 800:
            money = money - 800
            seeds = seeds + 1000
            store()
        else:
            clear()
            print("you are too poor")
            input()
            store()
    else:
        store()

def city():
    clear()
    print("CITY")
    print("[1] casino")
    print("[2] store")
    print("")
    print("[0] home")
    print("")
    print("STATS")
    print("money: " + str(money))
    print("seeds: " + str(seeds))
    print("crops: " + str(crops))
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        main()
    if option == "1":
        casino()
    elif option == "2":
        store()
    elif option == "0":
        main()



def main():
    clear()
    print("HOME")
    print("[1] farm")
    print("[2] city")
    print("")
    print("[0] exit")
    print("")
    print("STATS")
    print("money: " + str(money))
    print("health: " + str(health))
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        main()
    if option == "1":
        farm()
    elif option == "2":
        city()
    elif option == "0":
        clear()
        nigga = input("(y/n) are you sure you want to quit? ")
        if nigga == "y":
            clear()
            print("comeback soon")
            save()
            exit()
        else:
            main()

    else:
        main()

if __name__ == "__main__":
    clear()
    load()
    main()

