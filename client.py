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

input = ""

def get_input():
    print("get_input")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            render.game_over()
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                input = keys.RIGHT
            if event.key == pygame.K_LEFT:
                input = keys.LEFT
            if event.key == pygame.K_DOWN:
                input = keys.DOWN
            if event.key == pygame.K_UP:
                input = keys.UP

def server_recv_handler(client_socket, gameRender):
    while True:
        print("server_recv_handler")
        body1, body2, food_pos = protocol_commands.unpack_frame_info(client_socket.recv(4096))
        client_socket.send(protocol_commands.pack_ok_reply())
        gameRender.game_update(body1, food_pos)

def server_send_handler(client_socket):
    while True:
        print("server_send_handler")
        if (input != ""):
            client_socket.send(input().encode())
            client_socket.recv(2)
            input = ""


threading.Thread(server_recv_handler(client_socket,gameRender)).start()
threading.Thread(server_send_handler(client_socket)).start()

# while True:
#     snake_body = pickle.loads(client_socket.recv(4096))
#     client_socket.send(protocol_commands.pack_ok_reply())
#     food_pos = pickle.loads(client_socket.recv(50))
#     client_socket.send(protocol_commands.pack_ok_reply())
#     score = client_socket.recv(1024).decode()
#     client_socket.send(protocol_commands.pack_ok_reply())
#     gameRender.game_update(snake_body, food_pos, score)
#     get_input()
#     if(input != ""):
#         client_socket.send(input().encode())
#         client_socket.recv()
#         input = ""




#client_socket.close()