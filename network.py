import socket
import pickle
import select
import struct

from users import User
from respond import Respond
HEADERSIZE = 10



class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Put your IP Address Here
        self.server = "10.0.0.9"
        self.port = 10011
        self.addr = (self.server, self.port)
        self.players = self.connect()
        self.user = User("","","","",[])
        # maintains a list of possible input streams
        self.sockets_list = [self.client]

    def get_connected_users(self):
    # TODO get connected users from server
        return self.players

    def get_number_of_players(self):
        self.send(typ=Respond.TOTAL_PLAYERS, data=" ")

    def get_player_turn(self):
        return self.send(typ=Respond.PLAYER_COUNTER_S, data=" ")

    def get_list_of_players(self):
        return self.send(typ=Respond.LIST_OF_PLAYER, data=" ")

    def get_character_connected(self):
        return self.send(typ=Respond.CHARACTER_CONNECTED, data=" ")

    def get_character_move_msg(self):
        return self.send(typ=Respond.CHARACTER_MOVE_MSG, data=" ")


    def connect_user_to_game(self, user):
        self.send(typ=Respond.PLAYER, data=user)

    def get_all_players(self):
        return self.send(typ=Respond.LIST_OF_USERS, data=" ")


    def connect(self):
        try:
            self.client.connect(self.addr)
            # Load byte data
            return pickle.loads(self.client.recv(2048))

        except socket.error as e:
            print(e)

    def send(self, typ, data):
        try:
            info = {"type": typ, "data": data}
            data_to_send = pickle.dumps(info)
            data_size = bytes(f'{len(data_to_send):<{10}}', "utf-8")
            self.client.send(data_size + data_to_send)
           # return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

    def receive(self):
        # try:
        #     return pickle.loads(self.client.recv(2048))
        # except socket.error as e:
        #     print(e)
        full_msg = b''
        new_msg = True
        data_to_receive = 16
        msglen = 0
        while True:
            msg = self.client.recv(data_to_receive)

            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False


            full_msg += msg
            data_to_receive = msglen - len(full_msg[HEADERSIZE:])
            if len(full_msg) - HEADERSIZE == msglen:
                data = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b""
                break

        return data
