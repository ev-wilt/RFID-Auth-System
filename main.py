from pirc522 import RFID
import json
import boto3
import datetime

rdr = RFID()
dynamodb = boto3.resource('dynamodb')
sns = boto3.resource('sns')
table = dynamodb.Table('RFID-Users')
topic = sns.Topic('')
                  
def get_card_uid():
    scanning = True
    while scanning:
        rdr.wait_for_tag()
        (error, tag_type) = rdr.request()
        if not error:
            print('Card detected')
            (error, uid) = rdr.anticoll()
            if not error:
                uid_string = ''
                for num in uid:
                    uid_string += str(num)
                return uid_string
                scanning = False

def write():
    name = input('Enter the name of the new user \n')
    print('Scan the new user card')
    uid = get_card_uid()
    payload = {
        'UID': uid,
        'name': name,
        'last_entry': datetime.datetime.now().strftime('%c')
    }
    res = table.put_item(
        Item = payload
    )
    print('User "' + name + '" was added to the database')
    main()

def read():
    print('Scanning for cards...')
    uid = get_card_uid()
    res = table.get_item(
        Key = {
            'UID': uid
        }
    )
    try:
        name = res['Item']['name']
        print('User found \nWelcome ' + name + ', your access has been logged')
        payload = {
            'UID': uid,
            'name': name,
            'last_entry': datetime.datetime.now().strftime('%c')
        }
        res = table.put_item(
            Item = payload
        )
    except:
        print('Unauthorized entry attempted, administrators will be notified')
        res = topic.publish(
            Message = 'An unauthorized user (UID: ' + uid + ') attempted to gain access.',
            Subject = 'Attempted Unauthorized Access'
        )
    main()

def delete():
    print('Scan the card you wish to delete')
    uid = get_card_uid()
    table.delete_item(
        Key = {
            'UID': uid
        }
    )
    print('User deleted from database')
    main()

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
