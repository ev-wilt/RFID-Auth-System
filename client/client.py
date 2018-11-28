from coapthon.client.helperclient import HelperClient

host = '127.0.0.1'
port = 5683
client = HelperClient(server=(host, port))

def write():
    name = input('Enter the name of the new user')
    print('Scan the new user card')


def read():
    print('Scanning for cards...')

def delete():
    print('Scan the card you wish to delete')

def main():
    res = ''
    while res != '1' and res != '2' and res != '3':
        res = input('Welcome to RFID-Auth-Sytem. \n Press 1 to read cards \n Press 2 to write cards \n Press 3 to delete cards \n')
        if res == '1':
            read()
        elif res == '2':
            write()
        elif res == '3':
            delete()

if __name__ == "__main__":
    main()