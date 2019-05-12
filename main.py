import datetime
import random

import mysql.connector as connector


# def insert_into_table(database, cursor, table, values, many=False):
#     query = "INSERT INTO {} (user_name) VALUES (%s)".format(table)
#
#     if many:
#         cursor.executemany(query, values)
#     else:
#         cursor.execute(query, values)
#     database.commit()
#     print(cursor.rowcount, "records inserted")
#
#
# def execute_querry(database, cursor, querry):
#     cursor.execute(querry)
#     database.commit()

def create_connector(host, database, user, password):
    db = connector.connect(host=host,
                           database=database,
                           user=user,
                           password=password)
    cursor = db.cursor()
    print("Connected, ready to execute querries")

    return db, cursor


## Create tables
def create_users_table(database, cursor):
    print(" [INFO] : Creating users table")
    query = "CREATE TABLE users (UserID INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY, Username VARCHAR(255))"
    cursor.execute(query)
    database.commit()
    print(" [INFO] : Exiting create users table")


def create_messages_table(database, cursor):
    print(" [INFO] : Creating messages table")
    query = "CREATE TABLE messages (" \
            "MessageID INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY," \
            "AuthorID INT(20) NOT NULL ," \
            "RecepientID INT(20) NOT NULL ," \
            " Subject VARCHAR (255)," \
            " Date DATETIME," \
            " Body LONGTEXT," \
            " CONSTRAINT fk_authorID FOREIGN KEY (AuthorID) REFERENCES users(UserID)," \
            " CONSTRAINT fk_recepientID FOREIGN KEY (RecepientID)REFERENCES users(UserID))"
    cursor.execute(query)
    database.commit()
    print(" [INFO] : Exiting create message table")


## Insert data
def insert_user(database, cursor, username):
    print(" [INFO] : Inside insert user ")

    querry = "INSERT INTO users (Username) VALUES (%s)"
    cursor.execute(querry, (username,))
    database.commit()
    print(cursor.rowcount, "records inserted")
    user_id = get_user_id(cursor, username)
    print(" [INFO] : exiting insert user ")

    return user_id


def insert_message(database, cursor, Message):
    print(" [INFO] : Inside insert message ")
    recepientName = Message['RecepientName']

    recepient_hold = -1
    recepient_hold = get_user_id(cursor, recepientName)

    if recepient_hold != -1:
        recepientID = recepient_hold
    else:
        print("Error : No such recepient")
        return 0

    # should be checked in databse 1st
    authorName = Message['Username']

    author_hold = -1
    author_hold = get_user_id(cursor, authorName)

    if author_hold != -1:
        authorID = author_hold
    else:
        print(" [INFO] : creating new user {}".format(authorName))
        authorID = insert_user(database, cursor, authorName)

    subject = Message['Subject']
    date = Message['Date']
    body = Message['body']

    querry = "INSERT INTO messages(Subject, AuthorID, RecepientID, date, Body) values (%s,%s,%s,%s,%s)"

    cursor.execute(querry, (subject, authorID, recepientID, date, body))
    database.commit()
    print(cursor.rowcount, "records inserted")
    print(" [INFO] :Exiting insert message ")


## getters
def get_user_id(cursor, username):
    print(" [INFO] : Performing search for {} ".format(username))
    querry = "SELECT UserID FROM users WHERE Username = (%s)"
    cursor.execute(querry, (username,))
    result = cursor.fetchall()
    if len(result) > 0:
        print("result: ", result)
        return result[0][0]
    print("No match ")
    print("Exiting get_user_id without success")
    return -1


# Get all messages for a user
# def get_messages_by_id(cursor, authorID):
#     print(" [INFO] : Entering get message by id")
#     querry = "SELECT * FROM messages WHERE AuthorID = (%s)"
#     cursor.execute(querry, (authorID,))
#     result = cursor.fetchall()
#     for message in result:
#         print(message)
#     print("  [INFO] : Exiting get message by id")


def get_messages_by_username(cursor, username):
    print(" [INFO] : Entering get message by username")

    querry = "SELECT * FROM messages WHERE AuthorID = (%s)"
    cursor.execute(querry, (get_user_id(cursor, username),))
    result = cursor.fetchall()
    for message in result:
        print(message)
    print(" [INFO] : Exiting get message by username")


def get_recieved_messages_by_username(cursor, username):
    print(" [INFO] : Entering get recieved message by username")

    querry = "SELECT * FROM messages WHERE RecepientID = (%s)"
    cursor.execute(querry, (get_user_id(cursor, username),))
    result = cursor.fetchall()
    for message in result:
        print(message)
    print(" [INFO] : Exiting get recieved message by username")


def select_messages_for_recepient(cursor, recepientUsername):
    querry = "SELECT a.Username, c.Username, b.Subject, b.date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND c.Username = (%s)"
    cursor.execute(querry, (recepientUsername,))
    result = cursor.fetchall()
    formated_print(result)


# Printer
def formated_print(results):
    for message in results:
        print("-------------")
        print(" Format: [MessageID][Recepient Name][Author Name][Subject][Date][Body]")
        print(message)
        print("-------------")


# Message generator
def message_generator():
    usernames = ["Carlos", "Moncho", "Luke", "Mike", "Atanas", "Megan", "Taylor", "Barry", "Cisco", "Sheldon"]
    subjects = ["Coffe break", "Final assignment", "Project X", "Interview", "Cute cat video", "Meeting schedule",
                "Invoice", "Birthday party", "Congratulations", "Cute dog video"]
    body = ["This is text is for testing purposes 1", "This is text is for testing purposes 2",
            "This is text is for testing purposes 3", "This is text is for testing purposes 4",
            "This is text is for testing purposes 5", "This is text is for testing purposes 6",
            "This is text is for testing purposes 7", "This is text is for testing purposes 8",
            "This is text is for testing purposes 9", "This is text is for testing purposes 10", ]

    message_counter = 0

    while message_counter <= 100:
        random_name_number = random.randint(0, 4)
        random_name = usernames[random_name_number]

        random_recepient_number = random.randint(0, 4)
        if random_recepient_number == random_name_number:
            random_recepient_number = random.randint(0, 4)

        random_recepient = usernames[random_recepient_number]

        random_time = datetime.datetime.now()
        formated_random_time = random_time.strftime('%Y-%m-%d %H:%M:%S')

        random_subject = subjects[random.randint(0, 4)]
        random_body = body[random.randint(0, 4)]

        Message = {
            "RecepientName": random_recepient,
            'Username': random_name,
            'Subject': random_subject,
            'Date': formated_random_time,
            'body': random_body}

        print(" [INFO] : Message {} ".format(Message))

        insert_message(database, cursor, Message)
        message_counter += 1

    print(" [INFO] : Entered {} messages. Exiting".format(message_counter))


def enter_credentials():
    host = input("give host address")
    database_name = input("give database name")
    user = input("give user")
    password = input("give password")

    return host, database_name, user, password


# host='localhost', database="messaging_system"

hst, db_name, usr, passwd = enter_credentials()

database, cursor, = create_connector(host=hst, database=db_name, user=usr,
                                     password=passwd)
