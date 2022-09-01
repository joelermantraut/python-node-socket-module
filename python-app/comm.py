import socketio
import time

class SocketCom():
    """
    Sets sockets communication.
    """
    def __init__(self, port, namespaces):
        self.PORT = port
        self._last_message = None
        self.sioGeneral = socketio.Client()
        self.SLEEP_TIME = 0.1
        self.namespaces = namespaces
        self.read_callback = None
        self._init()

    def _init(self):
        """
        Inits comm in localhost.
        """
        self.sioGeneral.connect(f'http://localhost:{self.PORT}', namespaces=self.namespaces)
        self.sioGeneral.on("disconnect", self.disconnected)
        self.sioGeneral.on("message", self.message)

        for namespace in self.namespaces:
            self.sioGeneral.on("disconnect", lambda namespace=namespace: self.disconnected(namespace), namespace=namespace)
            self.sioGeneral.on("message", lambda data, namespace=namespace: self.message(data, namespace), namespace=namespace)

    def disconnect(self):
        """
        Methods called when disconnect is required.
        """
        self.sioGeneral.disconnect()

    def disconnected(self, namespace="/"):
        """
        Prints when server disconnects.
        """
        print(f"Puerto {self.PORT}, namespace {namespace} desconectado.")

    def message(self, msg, namespace="/"):
        """
        Receives a message and saves it in buffer.
        """
        self._last_message = msg

        if self.read_callback != None:
            self.read_callback(msg, namespace)

    def send_message(self, message, namespace='/'):
        """
        Sends a message, using namespace passed as parameter, or main
        namespace in default.
        """
        self.sioGeneral.emit('message', message, namespace=namespace)

    def new_message(self):
        """
        Returns True if there is something in buffer, False
        otherwise.
        """
        if self._last_message == None:
            return False
        else:
            return True

    def empty_buffer(self):
        """
        Empties last message variable.
        """
        self._last_message = None

    def get_received(self):
        """
        Returns last message and empties buffer.
        """
        aux = self._last_message
        self._last_message = None
        return aux

    def wait_to_receive(self):
        """
        Waits for a new data, and returns it.
        """
        while not(self.new_message()):
            time.sleep(self.SLEEP_TIME)

        return self.get_received()

    def send_and_receive(self, message):
        """
        Sends a message and waits the answer.
        """
        self.send_message(message)

        return self.wait_to_receive()

    def set_callback(self, callback):
        self.read_callback = callback
