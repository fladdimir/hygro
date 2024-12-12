import threading

import stream_listener
import web_server


def run():

    stream_listener_thread = threading.Thread(target=stream_listener.run)
    stream_listener_thread.start()

    web_server_thread = threading.Thread(target=web_server.run)
    web_server_thread.start()

    web_server_thread.join()
    stream_listener_thread.join()


if __name__ == "__main__":
    run()
