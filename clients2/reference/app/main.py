import os
import threading
import time
from client import Battleship

grpc_host = os.getenv('GRPC_HOST', 'localhost')
grpc_port = os.getenv('GRPC_PORT', '50051')

playing = threading.Event()
playing.set()

battleship = Battleship(grpc_host=grpc_host, grpc_port=grpc_port)


global shipHitPoints
global s
shipHitPoints = 0


@battleship.on()
def begin():
    print("""____________________________________________
-BATTLESHIP- BOGAN REVENGE- Board Game!
-LET THE BATTLE BEGIN-
____________________________________________""")


@battleship.on()
def start_turn():
    global shipHitPoints
    board_data(myFleetBoard)
    while True:
        if shipHitPoints > 0:  # TODO: (server is not stable) Extra statement implemented to re-confirm LOSE.
            # noinspection PyBroadException
            try:
                global s
                s = input('Make your move, mate!> ').upper()
                if s == "A1" or s == "A2" or s == "A3" or s == "A4" or s == "A5" or s == "A6" or s == "A7" or s == "A8" or s == "A9" or s == "A0" \
                        or s == "B1" or s == "B2" or s == "B3" or s == "B4" or s == "B5" or s == "B6" or s == "B7" or s == "A8" or s == "A9" or s == "A0" \
                        or s == "C1" or s == "C2" or s == "C3" or s == "C4" or s == "C5" or s == "C6" or s == "C7" or s == "C8" or s == "C9" or s == "C0" \
                        or s == "D1" or s == "D2" or s == "D3" or s == "D4" or s == "D5" or s == "D6" or s == "D7" or s == "D8" or s == "D9" or s == "D0" \
                        or s == "E1" or s == "E2" or s == "E3" or s == "E4" or s == "E5" or s == "E6" or s == "E7" or s == "E8" or s == "E9" or s == "E0" \
                        or s == "F1" or s == "F2" or s == "F3" or s == "F4" or s == "F5" or s == "F6" or s == "F7" or s == "F8" or s == "F9" or s == "F0" \
                        or s == "G1" or s == "G2" or s == "G3" or s == "G4" or s == "G5" or s == "G6" or s == "G7" or s == "G8" or s == "G9" or s == "G0" \
                        or s == "H1" or s == "H2" or s == "H3" or s == "H4" or s == "H5" or s == "H6" or s == "H7" or s == "H8" or s == "H9" or s == "H0" \
                        or s == "I1" or s == "I2" or s == "I3" or s == "I4" or s == "I5" or s == "I6" or s == "I7" or s == "I8" or s == "I9" or s == "I0" \
                        or s == "J1" or s == "J2" or s == "J3" or s == "J4" or s == "J5" or s == "J6" or s == "J7" or s == "J8" or s == "J9" or s == "J0":
                    battleship.attack(s)
                    break
                else:
                    print("Wrong input, Try again!")
            except:
                continue
        else:
            lose()
            break


@battleship.on()
def hit():
    global s
    enemyBoard[s] = "X"
    board_data(enemyBoard)
    print('Good, You have hit an enemy ship, mate!')
    print('''____________________________________________\n''')


@battleship.on()
def miss():
    global s
    while True:
        # noinspection PyBroadException
        try:
            if enemyBoard[s] == "X":
                enemyBoard[s] = "X"
                board_data(enemyBoard)
                print('Buh..You wasted a shot in the same place, mate!')
                print('''____________________________________________\n''')
                break
            else:
                enemyBoard[s] = "O"
                board_data(enemyBoard)
                print('Buh..You missed, mate!')
                print('''____________________________________________\n''')
                break
        except:
            continue


@battleship.on()
def win():
    global s
    enemyBoard[s] = "X"
    board_data(enemyBoard)
    print('FK YEAH...! YOU WON THIS, MATE!')
    print('''____________________________________________\n''')
    playing.clear()


@battleship.on()
def lose():
    board_data(myFleetBoard)
    print('SHAME ON YOU, NOOB. YOU LOST!!!')
    print('''____________________________________________\n''')
    playing.clear()


@battleship.on()
def attack(vector):
    global shipHitPoints
    vector = vector[0]
    while True:
        # noinspection PyBroadException
        try:
            if myFleetBoard[vector] != ' ' and myFleetBoard[vector] != 'M' and myFleetBoard[vector] != 'H':
                myFleetBoard[vector] = 'H'
                battleship.hit()
                shipHitPoints = shipHitPoints - 1
                if shipHitPoints <= 0:
                    print(f'OUCH!!. Shot impacted your ship at {vector}. ')
                    print('Ship has lost 1 Hit Point!')
                    print(shipHitPoints, "Hit Points remaining.\n")
                    # noinspection PyBroadException
                    try:  # TODO: (server is not stable) Extra statement implement to reconfirm LOSE.
                        battleship.defeat()
                    except:
                        continue
                    break
                else:
                    print(f'OUCH!!. Shot impacted your ship at {vector}. ')
                    print('Ship has lost 1 Hit Point!')
                    print(shipHitPoints, "Hit Points remaining.\n")
                break

            elif myFleetBoard[vector] == ' ' or myFleetBoard[vector] == 'M':
                myFleetBoard[vector] = 'M'
                battleship.miss()
                print(f'Shot detected close by to your fleet; at {vector}')
                print(shipHitPoints, " Hit Points remaining.\n")
                break

            elif myFleetBoard[vector] == 'H':
                battleship.miss()
                print(f'Shot impacted again at {vector}. But no extra damage was done to your ship!')
                print(shipHitPoints, " Hit Points remaining.\n")
                break
        except:
            continue


def add_ship():
    #add_patrol_boat(2, 4)
    #add_destroyer(2, 3)
    #add_cruiser(3, 3)
    #add_submarine(4, 2)
    add_battleship(5, 1)
    #add_mothership(6, 1)


def add_patrol_boat(patrol_boat_length, patrol_boat_available):
    const_length = patrol_boat_length
    while patrol_boat_available > 0:
        patrol_boat_length = const_length
        while patrol_boat_length > 0:
            global shipHitPoints
            # noinspection PyBroadException
            try:
                print('''_________________________________________________\n''')
                print("Ship Hit points deployed: ", shipHitPoints, "\n")
                board_data(myFleetBoard)
                print("Patrol Boats available: ", patrol_boat_available)
                print("Ship Hit points unused: ", patrol_boat_length)
                patrolBoat = input("Place the Patrol Boats anywhere in the board: ").upper()
                if myFleetBoard[patrolBoat] == ' ':
                    myFleetBoard[patrolBoat] = "P"
                    shipHitPoints = shipHitPoints + 1
                    patrol_boat_length = patrol_boat_length - 1
                else:
                    print("Vector used already. Try somewhere else!")
            except:
                print("Wrong input. Try again!")
                continue

        patrol_boat_available = patrol_boat_available - 1
        print('''_________________________________________________\n''')
        print("Patrol Boats deployed!.")
        print('''_________________________________________________\n''')


def add_destroyer(destroyer_length, destroyer_available):
    const_length = destroyer_length
    while destroyer_available > 0:
        destroyer_length = const_length
        while destroyer_length > 0:
            global shipHitPoints
            # noinspection PyBroadException
            try:
                print('''_________________________________________________\n''')
                print("Ship Hit points deployed: ", shipHitPoints, "\n")
                board_data(myFleetBoard)
                print("Destroyers available: ", destroyer_available)
                print("Ship Hit points unused: ", destroyer_length)
                destroyer = input("Place the Destroyers anywhere in the board: ").upper()
                if myFleetBoard[destroyer] == ' ':
                    myFleetBoard[destroyer] = "D"
                    shipHitPoints = shipHitPoints + 1
                    destroyer_length = destroyer_length - 1
                else:
                    print("Vector used already. Try somewhere else!")
            except:
                print("Wrong input. Try again!")
                continue

        destroyer_available = destroyer_available - 1
        print('''_________________________________________________\n''')
        print("Destroyers deployed!.")


def add_cruiser(cruiser_length, cruiser_available):
    const_length = cruiser_length
    while cruiser_available > 0:
        cruiser_length = const_length
        while cruiser_length > 0:
            global shipHitPoints
            # noinspection PyBroadException
            try:
                print('''_________________________________________________\n''')
                print("Ship Hit points deployed: ", shipHitPoints, "\n")
                board_data(myFleetBoard)
                print("Cruisers available: ", cruiser_available)
                print("Ship Hit points unused: ", cruiser_length)
                cruiser = input("Place the Cruisers anywhere in the board: ").upper()
                if myFleetBoard[cruiser] == ' ':
                    myFleetBoard[cruiser] = "C"
                    shipHitPoints = shipHitPoints + 1
                    cruiser_length = cruiser_length - 1
                else:
                    print("Vector used already. Try somewhere else!")
            except:
                print("Wrong input. Try again!")
                continue

        cruiser_available = cruiser_available - 1
        print('''_________________________________________________\n''')
        print("Cruisers deployed!.")


def add_submarine(submarine_length, submarine_available):
    const_length = submarine_length
    while submarine_available > 0:
        submarine_length = const_length
        while submarine_length > 0:
            global shipHitPoints
            # noinspection PyBroadException
            try:
                print('''_________________________________________________\n''')
                print("Submarine Hit points deployed: ", shipHitPoints, "\n")
                board_data(myFleetBoard)
                print("Submarines available: ", submarine_available)
                print("Submarines Hit points unused: ", submarine_length)
                submarine = input("Place the Submarines anywhere in the board: ").upper()
                if myFleetBoard[submarine] == ' ':
                    myFleetBoard[submarine] = "S"
                    shipHitPoints = shipHitPoints + 1
                    submarine_length = submarine_length - 1
                else:
                    print("Vector used already. Try somewhere else!")
            except:
                print("Wrong input. Try again!")
                continue

        submarine_available = submarine_available - 1
        print('''_________________________________________________\n''')
        print("Submarines deployed!.")
        print('''_________________________________________________\n''')


def add_battleship(battleship_length, battleship_available):
    const_length = battleship_length
    while battleship_available > 0:
        battleship_length = const_length
        while battleship_length > 0:
            global shipHitPoints
            # noinspection PyBroadException
            try:
                print('''_________________________________________________\n''')
                print("Ship Hit points deployed: ", shipHitPoints, "\n")
                board_data(myFleetBoard)
                print("Battleships available: ", battleship_available)
                print("Ship Hit points unused: ", battleship_length)
                theBattleship = input("Place the Battleship anywhere in the board: ").upper()
                if myFleetBoard[theBattleship] == ' ':
                    myFleetBoard[theBattleship] = "B"
                    shipHitPoints = shipHitPoints + 1
                    battleship_length = battleship_length - 1
                else:
                    print("Vector used already. Try somewhere else!")
            except:
                print("Wrong input. Try again!")
                continue

        battleship_available = battleship_available - 1
        print('''_________________________________________________\n''')
        print("Battleship deployed!.")
        print('''_________________________________________________\n''')


def add_mothership(mothership_length, mothership_available):
    const_length = mothership_length
    while mothership_available > 0:
        mothership_length = const_length
        while mothership_length > 0:
            global shipHitPoints
            # noinspection PyBroadException
            try:
                print('''_________________________________________________\n''')
                print("Ship Hit points deployed: ", shipHitPoints, "\n")
                board_data(myFleetBoard)
                print("Motherships available: ", mothership_available)
                print("Ship Hit points unused: ", mothership_length)
                mothership = input("Place the Mothership anywhere in the board: ").upper()
                if myFleetBoard[mothership] == ' ':
                    myFleetBoard[mothership] = "A"
                    shipHitPoints = shipHitPoints + 1
                    mothership_length = mothership_length - 1
                else:
                    print("Vector used already. Try somewhere else!")
            except:
                print("Wrong input. Try again!")
                continue

        mothership_available = mothership_available - 1
        print('''_________________________________________________\n''')
        print("Mothership deployed!.")
        print('''_________________________________________________\n''')


enemyBoard = {'A1': ' ', 'A2': ' ', 'A3': ' ', 'A4': ' ', 'A5': ' ', 'A6': ' ', 'A7': ' ', 'A8': ' ', 'A9': ' ',
              'A0': ' ',
              'B1': ' ', 'B2': ' ', 'B3': ' ', 'B4': ' ', 'B5': ' ', 'B6': ' ', 'B7': ' ', 'B8': ' ', 'B9': ' ',
              'B0': ' ',
              'C1': ' ', 'C2': ' ', 'C3': ' ', 'C4': ' ', 'C5': ' ', 'C6': ' ', 'C7': ' ', 'C8': ' ', 'C9': ' ',
              'C0': ' ',
              'D1': ' ', 'D2': ' ', 'D3': ' ', 'D4': ' ', 'D5': ' ', 'D6': ' ', 'D7': ' ', 'D8': ' ', 'D9': ' ',
              'D0': ' ',
              'E1': ' ', 'E2': ' ', 'E3': ' ', 'E4': ' ', 'E5': ' ', 'E6': ' ', 'E7': ' ', 'E8': ' ', 'E9': ' ',
              'E0': ' ',
              'F1': ' ', 'F2': ' ', 'F3': ' ', 'F4': ' ', 'F5': ' ', 'F6': ' ', 'F7': ' ', 'F8': ' ', 'F9': ' ',
              'F0': ' ',
              'G1': ' ', 'G2': ' ', 'G3': ' ', 'G4': ' ', 'G5': ' ', 'G6': ' ', 'G7': ' ', 'G8': ' ', 'G9': ' ',
              'G0': ' ',
              'H1': ' ', 'H2': ' ', 'H3': ' ', 'H4': ' ', 'H5': ' ', 'H6': ' ', 'H7': ' ', 'H8': ' ', 'H9': ' ',
              'H0': ' ',
              'I1': ' ', 'I2': ' ', 'I3': ' ', 'I4': ' ', 'I5': ' ', 'I6': ' ', 'I7': ' ', 'I8': ' ', 'I9': ' ',
              'I0': ' ',
              'J1': ' ', 'J2': ' ', 'J3': ' ', 'J4': ' ', 'J5': ' ', 'J6': ' ', 'J7': ' ', 'J8': ' ', 'J9': ' ',
              'J0': ' '}
myFleetBoard = {'A1': ' ', 'A2': ' ', 'A3': ' ', 'A4': ' ', 'A5': ' ', 'A6': ' ', 'A7': ' ', 'A8': ' ', 'A9': ' ',
                'A0': ' ',
                'B1': ' ', 'B2': ' ', 'B3': ' ', 'B4': ' ', 'B5': ' ', 'B6': ' ', 'B7': ' ', 'B8': ' ', 'B9': ' ',
                'B0': ' ',
                'C1': ' ', 'C2': ' ', 'C3': ' ', 'C4': ' ', 'C5': ' ', 'C6': ' ', 'C7': ' ', 'C8': ' ', 'C9': ' ',
                'C0': ' ',
                'D1': ' ', 'D2': ' ', 'D3': ' ', 'D4': ' ', 'D5': ' ', 'D6': ' ', 'D7': ' ', 'D8': ' ', 'D9': ' ',
                'D0': ' ',
                'E1': ' ', 'E2': ' ', 'E3': ' ', 'E4': ' ', 'E5': ' ', 'E6': ' ', 'E7': ' ', 'E8': ' ', 'E9': ' ',
                'E0': ' ',
                'F1': ' ', 'F2': ' ', 'F3': ' ', 'F4': ' ', 'F5': ' ', 'F6': ' ', 'F7': ' ', 'F8': ' ', 'F9': ' ',
                'F0': ' ',
                'G1': ' ', 'G2': ' ', 'G3': ' ', 'G4': ' ', 'G5': ' ', 'G6': ' ', 'G7': ' ', 'G8': ' ', 'G9': ' ',
                'G0': ' ',
                'H1': ' ', 'H2': ' ', 'H3': ' ', 'H4': ' ', 'H5': ' ', 'H6': ' ', 'H7': ' ', 'H8': ' ', 'H9': ' ',
                'H0': ' ',
                'I1': ' ', 'I2': ' ', 'I3': ' ', 'I4': ' ', 'I5': ' ', 'I6': ' ', 'I7': ' ', 'I8': ' ', 'I9': ' ',
                'I0': ' ',
                'J1': ' ', 'J2': ' ', 'J3': ' ', 'J4': ' ', 'J5': ' ', 'J6': ' ', 'J7': ' ', 'J8': ' ', 'J9': ' ',
                'J0': ' '}


def board_data(board):
    print('     1   2   3   4   5   6   7   8   9   0  ')
    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' A' + ' | ' + board['A1'] + ' | ' + board['A2'] + ' | ' + board['A3'] + ' | ' + board['A4'] + ' | ' + board[
        'A5'] + ' | ' + board['A6'] + ' | ' + board['A7'] + ' | ' + board['A8'] + ' | ' + board['A9'] + ' | ' + board[
              'A0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' B' ' | ' + board['B1'] + ' | ' + board['B2'] + ' | ' + board['B3'] + ' | ' + board['B4'] + ' | ' + board[
        'B5'] + ' | ' + board['B6'] + ' | ' + board['B7'] + ' | ' + board['B8'] + ' | ' + board['B9'] + ' | ' + board[
              'B0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' C' ' | ' + board['C1'] + ' | ' + board['C2'] + ' | ' + board['C3'] + ' | ' + board['C4'] + ' | ' + board[
        'C5'] + ' | ' + board['C6'] + ' | ' + board['C7'] + ' | ' + board['C8'] + ' | ' + board['C9'] + ' | ' + board[
              'C0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' D' ' | ' + board['D1'] + ' | ' + board['D2'] + ' | ' + board['D3'] + ' | ' + board['D4'] + ' | ' + board[
        'D5'] + ' | ' + board['D6'] + ' | ' + board['D7'] + ' | ' + board['D8'] + ' | ' + board['D9'] + ' | ' + board[
              'D0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' E' ' | ' + board['E1'] + ' | ' + board['E2'] + ' | ' + board['E3'] + ' | ' + board['E4'] + ' | ' + board[
        'E5'] + ' | ' + board['E6'] + ' | ' + board['E7'] + ' | ' + board['E8'] + ' | ' + board['E9'] + ' | ' + board[
              'E0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' F' ' | ' + board['F1'] + ' | ' + board['F2'] + ' | ' + board['F3'] + ' | ' + board['F4'] + ' | ' + board[
        'F5'] + ' | ' + board['F6'] + ' | ' + board['F7'] + ' | ' + board['F8'] + ' | ' + board['F9'] + ' | ' + board[
              'F0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' G' ' | ' + board['G1'] + ' | ' + board['G2'] + ' | ' + board['G3'] + ' | ' + board['G4'] + ' | ' + board[
        'G5'] + ' | ' + board['G6'] + ' | ' + board['G7'] + ' | ' + board['G8'] + ' | ' + board['G9'] + ' | ' + board[
              'G0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' H' ' | ' + board['H1'] + ' | ' + board['H2'] + ' | ' + board['H3'] + ' | ' + board['H4'] + ' | ' + board[
        'H5'] + ' | ' + board['H6'] + ' | ' + board['H7'] + ' | ' + board['H8'] + ' | ' + board['H9'] + ' | ' + board[
              'H0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' I' ' | ' + board['I1'] + ' | ' + board['I2'] + ' | ' + board['I3'] + ' | ' + board['I4'] + ' | ' + board[
        'I5'] + ' | ' + board['I6'] + ' | ' + board['I7'] + ' | ' + board['I8'] + ' | ' + board['I9'] + ' | ' + board[
              'I0'] + ' | ')

    print('   +---+---+---+---+---+---+---+---+---+---+')
    print(' J' ' | ' + board['J1'] + ' | ' + board['J2'] + ' | ' + board['J3'] + ' | ' + board['J4'] + ' | ' + board[
        'J5'] + ' | ' + board['J6'] + ' | ' + board['J7'] + ' | ' + board['J8'] + ' | ' + board['J9'] + ' | ' + board[
              'J0'] + ' | ')
    print('   +---+---+---+---+---+---+---+---+---+---+\n')


print("""\n-------------------------------------------------
Welcome to -BATTLESHIP-BOGAN REVENGE- Board Game!
-------------------------------------------------\n""")
add_ship()
board_data(myFleetBoard)
print("Ship Hit points deployed: ", shipHitPoints, "\n")
print('Waiting for the game to start...')
battleship.join()
while playing.is_set():
    time.sleep(1.0)
