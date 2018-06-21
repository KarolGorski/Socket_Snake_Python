import socket
import render
import pygame
import keys
import threading
import pickle
import protocol_commands

host = 'localhost'
port = 777
server_address = (host,port)
buff_size = 1024

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)
gameRender = render.GameRender()

data = client_socket.recv(1000)
if data:
    client_socket.send(protocol_commands.pack_ok_reply())
    gameRender.game_start()

current_input = ""

def get_input():
    print("get_input")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            render.game_over()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                return keys.RIGHT
            if event.key == pygame.K_LEFT:
                return keys.LEFT
            if event.key == pygame.K_DOWN:
                return keys.DOWN
            if event.key == pygame.K_UP:
                return keys.UP


def server_recv_handler(client_socket, gameRender):
    while True:
        print("server_recv_handler")
        body1, body2, food_pos = protocol_commands.unpack_frame_info(client_socket.recv(4096))
        client_socket.send(protocol_commands.pack_ok_reply())
        gameRender.game_update(body1, food_pos)

def server_send_handler(client_socket):
    current_input = ""
    while True:

        current_input = get_input()
        print("server_send_handler")
        if (current_input != ""):
            client_socket.send(current_input.encode())
            client_socket.recv(2)
            current_input = ""


threading.Thread(target=server_recv_handler,args =[client_socket,gameRender]).start()
threading.Thread(target=server_send_handler,args=[client_socket]).start()

# while True:
#     snake_body = pickle.loads(client_socket.recv(4096))
#     client_socket.send(protocol_commands.pack_ok_reply())
#     food_pos = pickle.loads(client_socket.recv(50))
#     client_socket.send(protocol_commands.pack_ok_reply())
#     score = client_socket.recv(1024).decode()
#     client_socket.send(protocol_commands.pack_ok_reply())
#     gameRender.game_update(snake_body, food_pos, score)
#     get_input()
#     if(current_input != ""):
#         client_socket.send(current_input().encode())
#         client_socket.recv()
#         current_input = ""




#client_socket.close()