import socket
import struct
import sys
import pickle
from users import Characters
from users import Rooms
from users import Weapons
from _thread import *
from users import User
from Guess import Accusation
from Guess import Suggestion
from respond import Respond

server = ""
port = 10011

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SOCK_STREAM, 1)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(3)
print("Waiting for Connection...")

#players = [User(1, "Alex", Characters.Colonel_Mustard, (0, 0), [Characters.PP, Rooms.Kitchen, Weapons.Rope]), User(
 #   2, "Kate", Characters.Miss_Scarlet, (600, 600), [Characters.MW, Rooms.Billiard, Weapons.Knife])]  # mocked 2 users to test start game
players = []
# Track how many players have connected
current_player = 0
current_user = User("","","","",[])

playersToConnectionDict = {}
# print(current_player)
HEADERSIZE = 10

def client_thread(connection, player):
    # connection.send(pickle.dumps("hello"))
    respond = ""
    while True:
        try:
            data = None
            full_msg = b''
            new_msg = True
            data_to_receive = 16
            msglen = 0
            while True:
                msg = connection.recv(data_to_receive)

                if new_msg:
                    print('new msg received')
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False

                full_msg += msg
                data_to_receive = msglen - len(full_msg[HEADERSIZE:])
                print('len(full_msg) - HEADERSIZE', len(full_msg) - HEADERSIZE)
                print('msglen', msglen)
                if len(full_msg) - HEADERSIZE == msglen:
                    data = pickle.loads(full_msg[HEADERSIZE:])
                    new_msg = True
                    full_msg = b""
                    break

            if not data:
                print("Disconnected")
                break
            else:

                print("Received: ", data)
                print("Sending: ", data)

                if data["type"] == Respond.PLAYER:
                    players.append(data["data"])
                    current_player = data["data"]
                    data_to_send = pickle.dumps(data)
                    data1 = {'type' : Respond.TOTAL_PLAYERS, 'data': len(players)}
                    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
                   # connection.sendall(data_size +data_to_send)
                    send_data_to_all_clients(data)
                    send_data_to_all_clients(data1)
                elif data["type"] == Respond.ACCUSATION:
                    #connection.sendall(pickle.dumps(data))
                    send_data_to_all_clients(data)
                elif data["type"] == Respond.SUGGESTION:
                    send_data_to_all_clients(data)
                elif data["type"] == Respond.TOTAL_PLAYERS:
                    data = {'type' : Respond.TOTAL_PLAYERS, 'data': len(players)}
                    data_to_send = pickle.dumps(data)
                    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
                    print("data", data)
                    send_data_to_all_clients(data)
                   # connection.sendall(data_size + data_to_send)
#                elif data["type"] == Respond.LIST_OF_PLAYERS:
#                    connection.sendall(pickle.dumps(players))
                elif data["type"] == Respond.LIST_OF_USERS:
                    data = {'type' : Respond.LIST_OF_USERS, 'data': players}
                    data_to_send = pickle.dumps(data)
                    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
                    send_data_to_all_clients(data)
                elif data["type"] == Respond.CHARACTER_MOVE:
                        send_data_to_all_clients(data)
                elif data["type"] == Respond.CHARACTER_CONNECTED:
                        send_data_to_all_clients(data)
                elif data["type"] == Respond.CHARACTER_MOVE_MSG:
                        send_data_to_all_clients(data)
                elif data["type"] == Respond.PLAYER_COUNTER_S:
                        send_data_to_all_clients(data)
                elif data["type"] == Respond.GAME_LOG:
                        print("DATA:", data)
                        send_data_to_all_clients(data)
                elif data["type"] == Respond.SINGLE_USER:
                        print("DATA1:",data)
                        send_data_to_particular_client(data)
                elif data["type"] == Respond.ANSWER:
                        print("DATA1:",data)
                        send_data_to_all_clients(data)

                else:
                    connection.sendall("Improper Input")
        except:
            break

    for key in playersToConnectionDict.keys(): # If client will disconnect then remove it from the player's dict
        if key == player:
            print("key")
            del playersToConnectionDict[key]
            break
    print("Connection Disconnected")
    players.remove(current_player)
    connection.close()

def send_data_to_all_clients(data):
    data_to_send = pickle.dumps(data)
    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
    #print("playersToConnectionDict", playersToConnectionDict)
    for player in playersToConnectionDict:
        playersToConnectionDict[player].sendall(data_size + data_to_send)

def send_data_to_particular_client(data): #pl is # of player in players list
    print("insideeeee", data)
    value = data["data"]
    #print("index",pl)
    index = value[0]
    message = value[1]
    print("particular", data)
    data1 = {'type': Respond.SINGLE_USER, 'data': message}
    data_to_send = pickle.dumps(data1)
    data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
    playersToConnectionDict[index].sendall(data_size + data_to_send)


while True:

    connection, address = s.accept()
    print('connection', connection)
    connection.send(pickle.dumps("Welcome to the server"))
    print("Connected to:", address)
    playersToConnectionDict[current_player] = connection

    start_new_thread(client_thread, (connection, current_player))
    current_player += 1

