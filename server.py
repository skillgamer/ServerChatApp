import socket
import pickle
from threading import Thread

global client_list
client_list = []

IP = "139.162.144.244"
PORT = 6969
ADDR = (IP, PORT)
users = {
    "a": "a",
    "vova": "ronik"
}


def keep_conn(serv_sock):
    while True:
        client, _ = serv_sock.accept()
        Thread(target=deal_with_client_login_attempt, args=(client,)).start()


def deal_with_client_login_attempt(client):
    global userdata
    global client_list
    while True:
        try:
            userdata = pickle.loads(client.recv(1024))  # User dict type object {username: "", password: ""}
            if userdata['username'] in users.keys() and users[userdata['username']] == userdata['password']:
                client.send(pickle.dumps(True))
                client_list.append(client)
                Thread(target=send_messages_after_login, args=(client,)).start()
                break
            else:
                client.send(pickle.dumps(False))
        except ConnectionResetError:
            print(f"client that tried to connect with username'{userdata['username']}' is gone")
            break


def deal_with_new_user(client):
    pass


def send_messages_after_login(client):
    try:
        while True:
            msg = client.recv(1024).decode()
            Thread(target=send_new_messages, args=(msg,)).start()
    except ConnectionResetError or Exception as e:
        pass


def send_new_messages(msg):
    for client_connection in client_list:
        try:
            client_connection.send(msg.encode())
        except ConnectionResetError or Exception as e:
            client_list.pop(client_list.index(client_connection))


def main():
    with socket.socket() as serv_socket:
        serv_socket.bind(ADDR)
        serv_socket.listen(5)
        print("waiting for clients")
        t = Thread(target=keep_conn, args=(serv_socket,))
        t.start()
        t.join()


if __name__ == '__main__':
    main()
