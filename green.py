"""A simple proof of echo server using greenlet

In most cases you're probably better off using a higher level library
like gevent or eventlet.
"""


import logging
import socket
import select

import greenlet


def accepter():
    parent = greenlet.getcurrent().parent
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 6666))
    sock.listen(100)  # 100 should be a large enough backlog
    while True:
        # busy waiting with select is not a very nice thing to do
        ready, _, _ = select.select([sock], [], [], 0)
        if ready:
            print "ready to accept"
            new_sock, address = sock.accept()
            parent.switch(new_sock)
        else:
            parent.switch(None)


def client(sock):
    print "new client!"
    parent = greenlet.getcurrent().parent
    parent.switch()
    while True:
        ready = select.select([sock], [], [], 0)[0]
        if ready:
            print "recv"
            buff = sock.recv(4096)
            if buff == '':
                print "client disconnected"
                return
            # sending could block, but it's good enough for this example
            print "send"
            sock.send(buff)
        parent.switch()


def main():
    acc = greenlet.greenlet(accepter)
    clients = []
    while True:
        dead_clients = []
        new_sock = acc.switch()
        if new_sock is not None:
            new_client = greenlet.greenlet(client)
            clients.append(new_client)
            new_client.switch(new_sock)

        for c in clients:
            try:
                c.switch()
            except:
                logging.exception("an error has occured")
                dead_clients.append(c)
            else:
                if c.dead:
                    dead_clients.append(c)

        for c in dead_clients:
            clients.remove(c)

if __name__ == "__main__":
    main()
