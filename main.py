from datetime import datetime, timedelta
import random
import os
import json

# starting values
money = 500
seeds = 0
crops = 0
planted = 0
games = 0
start = None
estado = None
growth = timedelta(minutes=30)

SAVE_FILE = "save"

def save():
    global money, seeds, planted, start, games
    start_str = start.isoformat() if isinstance(start, datetime) else start
    game_data = {
        "money": money,
        "seeds": seeds,
        "planted": planted,
        "start": start_str,
        "games": games
    }
    with open(SAVE_FILE, 'w') as file:
        json.dump(game_data, file)

def load():
    global money, seeds, planted, start, games
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, 'r') as file:
            game_data = json.load(file)
            money = game_data["money"]
            seeds = game_data["seeds"]
            planted = game_data["planted"]
            start_str = game_data.get("start")
            games = game_data["games"]
        if start_str == None:
            start = None
        else:
            start = datetime.fromisoformat(start_str)
    else:
        save()
        main()

def reset():
    global money, seeds, planted, start, games
    games += 1
    game_data = {
    "money": 500,
    "seeds": 0,
    "planted": 0,
    "start_str": None,
    "games": games
    }
    with open(SAVE_FILE, 'w') as file:
        json.dump(game_data, file)

def stats():
    clear()
    global money, seeds, planted, games
    print("STATS")
    print("money: " + str(money) + "€")
    print("seeds: " + str(seeds))
    print("planted seeds: " + str(planted))
    print("game count: " + str(games))
    input()

def clear(): # clear console
    os.system('cls' if os.name == 'nt' else 'clear')

def time(): # print time
    global estado
    now = datetime.now()
    hora = datetime.now().hour
    if 7 <= hora < 19:
        estado = "day"
    else:
        estado = "night"
    current_time = now.strftime("%H:%M")
    print(f"\rcurrent time: {current_time} ({estado})")

def russian():
    global money
    clear()
    bullet = random.randint(1, 6)
    pulls = 0
    try:
        bet = int(input("bet: "))
    except ValueError:
        print("Invalid Value!")
        input()
        russian()
    if bet > money:
        print("You dont have that kind of money!")
        input()
        bridge()
    else:
        clear()
        n = 0
        prize = 0
        while n < 6:
            trigger = input("press 'p' to pull the trigger\n")
            if trigger == "p":
                n += 1
                if n == bullet:
                    clear()
                    print("you killed yourself")
                    reset()
                    input()
                    exit()
                else:
                    prize += bet * (n+1)
                    money += prize
                    clear()
                    print("you survived!")
                    input()
            else:
                clear()
                print("you survived!")
                input()
                break
        print("you survived " + str(n) +" trigger pulls and made " + str(prize) + "€")
        input()
        bridge()


def bridge():
    clear()
    print("BRIDGE")
    print("[1] city")
    print("[2] jump")
    print("[3] russian roulete")
    print("")
    print("[s] STATS")
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        bridge()
    if option == "1":
        city()
    elif option == "2":
        clear()
        jump = input("are you sure you want to jump off the bridge? (yes/no)\n")
        if jump == "yes":
            luck = random.randint(1, 2)
            if luck == 1:
                reset()
                exit()
                print("you killed yourself")
                input()
    elif option == "3":
        russian()
    else:
        bridge()


def casino():
    global money, seeds, crops
    clear()
    print("CASINO")
    print("[1] city")
    print("[2] dice")
    print("[3] SOON")
    print("[4] SOON")
    print("")
    print("[s] STATS")
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        casino()
    if option == "1": # city
        city()
    elif option == "2":# DICE
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
                if estado == "day":
                    prize = bet*2
                else:
                    prize = bet*3
                print("you guessed the number and got " + str(prize) + "$")
                money += prize
                save()
                input()
                casino()
            else:
                clear()
                print("you guessed " + str(guess) + " but the number was " + str(number))
                print("you lost " + str(bet) + "$")
                money -= bet
                save()
                input()
                casino()

    elif option == "3":# SOON
        casino()
    elif option == "4":# SOON
        casino()
    elif option == "s":# STATS
        stats()
        casino()
    else:
        casino()

def farm():
    global money, seeds, crops, time, planted, start, growth, now
    clear()
    print("FARM")
    print("[1] home")
    print("[2] seed")
    print("[3] harvest")
    print("")
    print("[s] STATS")
    time()
    try:
        option = input("option: ")
    except ValueError:
        farm()
    if option == "1":
        main()
    elif option == "2": # plant
        clear()
        if planted == 0:
            planted += seeds
            print("planted " + str(seeds) + " seeds!")
            start = datetime.now()
            seeds = 0
            input()
            farm()
        else:
            print("you already have things planted here")
            input()
            farm()
    elif option == "3":
        clear()
        if planted == 0:
            print("you done have nothin planted!")
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
    elif option == "s":# STATS
        stats()
        farm()
    else:
        farm()

def store():
    save()
    global money, seeds, planted
    clear()
    print("FARM")
    print("[1] city")
    print("[2] buy 500 seeds - 500$")
    print("[3] buy 1000 seeds - 800$ ")
    print("")
    print("[s] STATS")
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        store()
    if option == "1":
        city()
    elif option == "2":
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
    elif option == "3":
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
    elif option == "s":# STATS
        stats()
        store()
    else:
        store()

def city():
    save()
    clear()
    print("CITY")
    print("[1] home")
    print("[2] store")
    print("[3] casino")
    print("[4] bridge")
    print("")
    print("[s] STATS")
    time()
    try:
        option = input("option: ")
    except ValueError:
        clear()
        main()
    if option == "1":
        main()
    elif option == "2":
        store()
    elif option == "3":
        casino()
    elif option == "4":
        bridge()
    elif option == "s":# STATS
        stats()
        city()
    else:
        city()



def main():
    save()
    clear()
    print("HOME")
    print("[1] farm")
    print("[2] city")
    print("")
    print("[0] exit")
    print("")
    print("[s] STATS")
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
        nigga = input("are you sure you want to quit? (yes/no)\n")
        if nigga == "yes":
            clear()
            print("saved and closed")
            save()
            exit()
        else:
            main()
    elif option == "s":# STATS
        stats()
        main()
    else:
        main()

if __name__ == "__main__":
    clear()
    load()
    main()

