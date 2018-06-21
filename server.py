import socket
import game
import datetime
import threading
import queue
import pickle
import protocol_commands

host = 'localhost'
port = 777
server_address = (host,port)
buff_size = 1024

lock = threading.Lock()

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('starting up on %s port %s' % server_address)
serverSocket.bind(server_address)
print('listening')
serverSocket.listen(100)


gamesList = []

def gameplay(game):
    game.game_started = True
    while True:
        print("gameplay")
        game.game_loop()
        if game.game_finished:
            break


def add_player_to_game(player):
    print("add_player_to_game")
    if len(gamesList) == 0 or gamesList[len(gamesList)-1].add_player(player) == False:
        single_game = game.Game()
        gamesList.append(single_game)
        single_game.add_player(player)
        return single_game
    if gamesList[len(gamesList)-1].number_of_players == 1:
        gamesList[len(gamesList)-1].add_player(player)
        threading.Thread(target=gameplay,args=[gamesList[len(gamesList)-1]]).start()
        return gamesList[len(gamesList)-1]

def client_recv_handler(client_socket, player, single_game):
    while single_game.game_started == False:
        print("recv_handler_not started yet")
    while single_game.game_finished == False:
        print("client_recv_handler")
        data = client_socket.recv(1024)
        if data:
            player.input=data.decode()
            client_socket.send(protocol_commands.pack_ok_reply())


def client_send_handler(client_socket,player,single_game):
    while single_game.game_started == False:
        print("send_handler_not started yet")
    while single_game.game_finished == False:
        print("client_send_handler")
        data = protocol_commands.pack_frame_info(single_game.return_your_player(player).snake.body,
                                                 single_game.return_opposite_player(player).snake.body,
                                                 single_game.food_pos)
        client_socket.send(data)
        client_socket.recv(2)

def new_player_handler(client_socket):
    print("new_player_handler")
    player = game.Player()
    with lock:
        current_game = add_player_to_game(player)
    threading.Thread(target=client_send_handler,args=[client_socket, player, current_game]).start()
    threading.Thread(target=client_recv_handler,args=[client_socket,player,current_game]).start()



while True:
    client_socket , client_address = serverSocket.accept()
    try:
        client_socket.send("start".encode())
        print (client_socket.recv(5))
        threading.Thread(target=new_player_handler,args=[client_socket]).start()

    except socket.error:
        import trace
        print()
        break
    #finally:
        # print ('game_over')
        # client_socket\
        #     .send(("game_over").encode())
        # client_socket\
        #     .close()
        # print ('client disconnected')


#def new_player_appeared(client_socket
# , client_address, name):

#def set_new_game():


# recv_thread = threading.Thread(target=handle_client_recv,
#                                    args [[client_sock, addr],
#                                    daemon = True)
#     send_thread = threading.Thread(handle_client_send,
#                                    [client_sock,q,client_address],
#                                    True)
#     recv_thread.start()
#     send_thread.start()

print ("")