from finance_track import app
import socket

host = socket.gethostbyname(socket.gethostname())

if __name__ == "__main__":
    app.run(host=host, port=5000, debug=True)
