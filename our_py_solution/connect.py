# White port 5800
# Black port 5801

import json
import socket
import struct


def connect(url, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
    client_socket.connect((url, port))

    return client_socket


def send_int(sock, integer):
    bytes_sent = sock.send(struct.pack('>i', integer))
    return bytes_sent == 4


def send_str(sock, string):
    string = string.encode('utf-8')
    length = len(string)
    if send_int(sock, length):
        bytes_sent = sock.send(string)
        return bytes_sent == length
    return False


def send_name(sock, role):
    if 'w' in role:
        player_name = "WHITE_GOD"
    else:
        player_name = "BLACK_GOD"

    send_str(sock, player_name)


def receive_int(sock):
    size = 4
    header = b''
    while len(header) < size:
        data = sock.recv(size - len(header))
        if not data:
            break
        header += data
    return struct.unpack("!i", header)[0]


def receive_str(sock):
    length = receive_int(sock)
    return sock.recv(length, socket.MSG_WAITALL).decode('utf-8')


def receive_state(sock):
    json_str = receive_str(sock)
    json_obj = json.loads(json_str)
    return json_obj["board"], json_obj["turn"]


def read_state(client_socket):
    board, to_move = receive_state(client_socket)
    return board, to_move


def from_move_to_server_action(move):
    from_move, to_move = move
    from_action = f'{chr(ord("`") + (from_move[1] + 1))}{from_move[0] + 1}'
    to_action = f'{chr(ord("`") + (to_move[1] + 1))}{to_move[0] + 1}'

    return from_action, to_action


def send_action(sock, move, role):
    from_action, to_action = from_move_to_server_action(move)
    if 'w' in role:
        turn = "WHITE"
    else:
        turn = "BLACK"

    action_dict = {
        "from": from_action,
        "to": to_action,
        "turn": turn
    }

    json_str = json.dumps(action_dict)
    return send_str(sock, json_str)