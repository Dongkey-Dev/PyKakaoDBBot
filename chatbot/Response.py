def response(room, msg, sender, replier, msg_json, db, g):
    print(f"received: {sender} : {room} : {msg}")
    if msg == "$hi":
        replier.send_socket(True,"normal","test",room,replier.json)
