from comm import SocketCom
import time

def socket_callback(msg, namespace):
    print(msg, namespace)

def main():
    python_socket = SocketCom(3000, ["/", '/name1','/name2'])

    time.sleep(2)

    python_socket.send_message("message from name2", "/name2")

    python_socket.set_callback(socket_callback)

if __name__ == "__main__":
    main()
