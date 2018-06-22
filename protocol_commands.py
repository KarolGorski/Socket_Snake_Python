import keys


def initial_parse(message):
    message_string = message.decode()
    parts = message_string.split('.', 1)
    message_id = int(parts[0])
    return message_id

def decode_basic_msg(message):
    print (message)
    return message.decode().split('.')[1]


def pack_ok_reply():
    string = "0."
    return string.encode()

def is_it_ok(message):
    if message.decode().split('.',1)[0] == "0":
        return True
    else:
        return False

def pack_join_request():
    string = "1."
    return string.encode()

def pack_join_reply(msg):
    string = "2."+msg
    return string.encode()

def is_it_play(msg):
    print (msg.decode())
    if msg.decode().split(".")[1] == keys.PLAY:
        return True
    else:
        return False

def pack_init_info(body1, body2,GAME_SPEED, BOARD_SIZE, BLOCK_SIZE):
    string ="3."
    string+=str(BOARD_SIZE)+"."
    string+=str(BLOCK_SIZE)+"."
    string+=str(GAME_SPEED)+"."
    #while()

def pack_frame_info(body1, body2, food_pos):
    string = "4."
    for i in body1:
        string+=';'+str(i[0])+','+str(i[1])
    string += '.'
    for i in body2:
        string+=';'+str(i[0])+','+str(i[1])
    string += '.'

    string +=str(food_pos[0])+','+str(food_pos[1])

    return string.encode()


def unpack_frame_info(message):
    body1 = []
    body2 = []
    food_pos = []
    string = message.decode()
    parts = string.split(".")
    #message_id = parts[0]
    body1_parts = parts[1].split(";")
    body2_parts = parts[2].split(";")
    raw_food_pos = parts[3]

    for i in body1_parts:
        tab = i.split(',')
        body1.append([int(tab[0]), int(tab[1])])
    for i in body2_parts:
        tab = i.split(',')
        body2.append([int(tab[0]), int(tab[1])])
    tab = raw_food_pos.split(',')
    food_pos.append([int(tab[0]), int(tab[1])])

    return (body1, body2, food_pos)


