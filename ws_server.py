import logging
import tornado
import tornado.web
from tornado import httpserver
from tornado import ioloop
from tornado import websocket
import pdb 


client_id = 0
clients = {}
class ExchangeWebSocket(websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id = -1

    def open(self):
        global client_id
        logging.info("OPEN")
        self.client_id = client_id
        clients[client_id] = self
        client_id += 1
        logging.info(f"clients num: {len(clients)}")

    def on_message(self, message):
        logging.info("ON_MESSAGE: {0}".format(message))
        for c_id, cli in clients.items():
            if c_id == self.client_id:
                continue
            cli.write_message(message)

    def on_close(self):
        logging.info(f"ON_CLOSE: client_id: {self.client_id}")
        global clients
        clients.pop(self.client_id)

    def allow_draft76(self):
        return False

    def check_origin(self, origin):
        return True


if __name__ == "__main__":
    import tornado.options
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", ExchangeWebSocket),
    ])
    server = httpserver.HTTPServer(application)
    server.listen(9999, "127.0.0.1")
    logging.info("STARTED: Server start listening")
    ioloop.IOLoop.instance().start()
