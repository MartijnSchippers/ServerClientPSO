from client import Client
import sys

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Error: too few argumetns given!!!")
    else:
        # app.py [(LOCAL) IP ADDRESS] [PORT] [ID (UNIQUE)]
        client = Client(sys.argv[1], sys.argv[2], sys.argv[3])
        client.run()