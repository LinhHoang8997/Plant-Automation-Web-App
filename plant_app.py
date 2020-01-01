from flaskr.routes import start_server
from threading import Thread
import webview
import sys

if __name__ == '__main__':
    t = Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window('CESCERE', 'http://127.0.0.1:5000/', width=1200, height=1200)
    webview.start(gui="cef", debug=True)
    sys.exit()
