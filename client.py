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
pygame.init()

while True:
    data = client_socket.recv(6)
    print(data)
    if protocol_commands.is_it_play(data):
        client_socket.send(protocol_commands.pack_ok_reply())
        gameRender.game_start()
        break
    else:
        client_socket.send(protocol_commands.pack_ok_reply())
        gameRender.game_intro(protocol_commands.decode_basic_msg(data))


def get_input():
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
    return None



def server_recv_handler(client_socket, gameRender, send_handler):
    while True:
        if(client_socket.recv(2).decode == ".6"):
            send_handler.stop()
            break
        print("server_recv_handler")
        body1, body2, food_pos = protocol_commands.unpack_frame_info(client_socket.recv(4096))
        client_socket.send(protocol_commands.pack_ok_reply())
        gameRender.game_update(body1, food_pos)

def server_send_handler(client_socket):
    while True:
        current_input = get_input()
        if (current_input!=None):
            print("server_send_handler")
            client_socket.send(protocol_commands.pack_input_info(current_input))
            client_socket.recv(2)


send_handler = threading.Thread(target=server_send_handler,args=[client_socket]).start()
threading.Thread(target=server_recv_handler,args =[client_socket,gameRender, send_handler]).start()


