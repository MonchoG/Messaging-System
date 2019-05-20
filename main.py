import datetime
import random

import mysql.connector as connector

#################################
# Utils
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
    host = input("give host address: ")
    database_name = input("give database name: ")
    user = input("give user: ")
    password = input("give password: ")

    return host, database_name, user, password


def create_connector(host, database, user, password):
    db = connector.connect(host=host,
                           database=database,
                           user=user,
                           password=password)
    cursor = db.cursor()
    print("Connected, ready to execute querries")

    return db, cursor
#################################


#################################
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
#################################


#################################
### Insert data

## insert user
# @params
#   database conn,
#   db cursor,
#   username : name to insert
###
def insert_user(database, cursor, username):
    print(" [INFO] : Inside insert user ")

    querry = "INSERT INTO users (Username) VALUES (%s)"
    cursor.execute(querry, (username,))
    database.commit()
    print(cursor.rowcount, "records inserted")
    user_id = get_user_id(cursor, username)
    print(" [INFO] : exiting insert user ")

    return user_id

### insert message
#   @params:
#   database conn,
#   db cursor,

#   Message = {
#   "RecepientName": random_recepient,
#   'Username': 'name sender,
#   'Subject': 'subject,
#   'body': 'message'
#   }
###
def insert_message(database, cursor, Message):
    print(" [INFO] : Inside insert message ")
    recepientName = Message['RecepientName']

    recepient_hold = -1
    recepient_hold = get_user_id(cursor, recepientName)
    # Check if recepient is in db
    if recepient_hold != -1:
        recepientID = recepient_hold
    else:
        # else return from the method
        print("Error : No such recepient")
        return 0

    # should be checked in databse 1st
    authorName = Message['Username']

    author_hold = -1
    author_hold = get_user_id(cursor, authorName)
    # if sender is not present in db, insert him
    if author_hold != -1:
        authorID = author_hold
    else:
        print(" [INFO] : creating new user {}".format(authorName))
        authorID = insert_user(database, cursor, authorName)

    subject = Message['Subject']
    date = Message['Date']
    body = Message['body']

    # querry to execute
    querry = "INSERT INTO messages(Subject, AuthorID, RecepientID, date, Body) values (%s,%s,%s,%s,%s)"
    # execute the query, with the parameters from the message
    cursor.execute(querry, (subject, authorID, recepientID, date, body))
    database.commit()

    print(cursor.rowcount, "records inserted")
    print(" [INFO] :Exiting insert message ")
#################################

#################################
## select all for user
def select_all_for_usr(cursor, username):
    print(" [INFO] : Entering select_all_for_usr")
    querry="SELECT a.Username, c.Username, b.Subject, b.date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND c.Username = (%s) OR a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND a.Username = (%s)"
    cursor.execute(querry, (username, username))
    result = cursor.fetchall()
    formated_print(result)
    print(" [INFO] : Exiting get recieved message by username")




#################################


#################################
## for sender
# selects all the messages send by user
def select_sent_messages_by_username(cursor, senderUsername):
    print(" [INFO] : Entering get recieved message by username")
    querry="SELECT a.Username, c.Username, b.Subject, b.date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND c.Username = (%s)"
    cursor.execute(querry, (senderUsername,))
    result = cursor.fetchall()
    formated_print(result)
    print(" [INFO] : Exiting get recieved message by username")

# selects all the messages received by user date ascending
def select_sent_messages_by_username_asc(cursor, senderUsername):
    print(" [INFO] : Entering get sent message by username date ascending")
    querry="SELECT a.Username, c.Username, b.Subject, b.date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND c.Username = (%s)ORDER by b.Date ASC"
    cursor.execute(querry, (senderUsername,))
    result = cursor.fetchall()
    formated_print(result)
    print(" [INFO] : Exiting get recieved message by username")
# selects all the messages received by user date descending

def select_sent_messages_by_username_desc(cursor, senderUsername):
    print(" [INFO] : Entering get sent message by username date descending")
    querry="SELECT a.Username, c.Username, b.Subject, b.date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND c.Username = (%s)ORDER by b.Date DESC"
    cursor.execute(querry, (senderUsername,))
    result = cursor.fetchall()
    formated_print(result)
    print(" [INFO] : Exiting get recieved message by username")

#################################

#################################
## for recepient
# selects all the messages received by user
def select_messages_for_recepient(cursor, recepientUsername):
    querry = "SELECT a.Username,c.Username, b.Subject,  b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND a.Username = (%s)"
    cursor.execute(querry, (recepientUsername,))
    result = cursor.fetchall()
    formated_print(result)

# selects all the messages received by user date ascending
def select_messages_for_recepient_date_asc(cursor, recepientUsername):
    print(" [INFO] : Entering get recieved message by Recepient date ascending")
    querry = "SELECT a.Username,c.Username, b.Subject,  b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND a.Username = (%s) ORDER by b.Date ASC"
    cursor.execute(querry, (recepientUsername,))
    result = cursor.fetchall()
    formated_print(result)

# selects all the messages received by user date descenging
def select_messages_for_recepient_date_desc(cursor, recepientUsername):
    print(" [INFO] : Entering get recieved message by Recepient date descending")
    querry = "SELECT a.Username,c.Username, b.Subject,  b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND a.Username = (%s) ORDER by b.Date DESC"
    cursor.execute(querry, (recepientUsername,))
    result = cursor.fetchall()
    formated_print(result)
#################################


#################################
## Find message by subject
# Selects all the messages with the subject
def select_messages_by_subject(cursor, subject):
    print(" [INFO] : select_messages_by_subject")
    querry = "SELECT a.Username,c.Username, b.Subject,  b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND b.Subject = (%s)"
    cursor.execute(querry, (subject,))
    result = cursor.fetchall()
    formated_print(result)

# selects all the messages with the said subject, date ascending
def select_messages_by_subject_date_asc(cursor, subject):
    print(" [INFO] : Entering get recieved message by Recepient date ascending")
    querry = "SELECT a.Username,c.Username, b.Subject,  b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND b.Subject = (%s) ORDER by b.Date ASC"
    cursor.execute(querry, (subject,))
    result = cursor.fetchall()
    formated_print(result)

# selects all the messages with the said subject, date descending
def select_messages_by_subject_date_desc(cursor, subject):
    print(" [INFO] : Entering get recieved message by Recepient date descending")
    querry = "SELECT a.Username,c.Username, b.Subject,  b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND b.Subject = (%s) ORDER by b.Date DESC"
    cursor.execute(querry, (subject,))
    result = cursor.fetchall()
    formated_print(result)

#################################

#################################
## Select messages by user and subject
def select_messages_by_username_subject(cursor, username, subject):
    print(" [INFO] : Entering get recieved message by Recepient date descending")
    querry = "SELECT a.Username,c.Username, b.Subject, b.Date, b.Body FROM users as a, messages as b, users as c WHERE a.UserID = b.RecepientID AND c.UserID = b.AuthorID AND b.Subject = (%s) AND a.Username=(%s)"
    cursor.execute(querry, (subject, username,))
    result = cursor.fetchall()
    formated_print(result)
#################################


# Printer
def formated_print(results):
    for message in results:
        print("-------------")
        str = "[Recepient name] : {recepeintName}\n[Sender name] : {senderName}\n[Subject] : {subject}\n[Date] : {date}\n[Body] : {body}".format(recepeintName=message[0], senderName= message[1], subject=message[2], date=message[3], body=message[4])
        print(str)
        print("-------------\n")




#hst, db_name, usr, passwd = enter_credentials()
hst='localhost'
db_name="messaging_system"
usr='root'
passwd=''

database, cursor = create_connector(host=hst, database=db_name, user=usr,password=passwd)

#print(" [INFO] : select_all_for_usr  : \n")
#select_all_for_usr(cursor, 'Moncho')
#print("=====================================================")

#print(" [INFO] : select_messages_by_subject  : \n")
#select_messages_by_subject(cursor, 'Cute cat video')
#print("=====================================================")

#print(" [INFO] : select_messages_by_subjectt_date_asc  : \n")
#select_messages_by_subject_date_asc(cursor, 'Cute cat video')
#print("=====================================================")

#print(" [INFO] : select_messages_by_subjectt_date_desc  : \n")
#select_messages_by_subject_date_desc(cursor, 'Cute cat video')
#print("=====================================================")

#print(" [INFO] : select_sent_messages_by_username  : \n")
#select_sent_messages_by_username(cursor, 'Moncho')
#print("=====================================================")

#print(" [INFO] : select_sent_messages_by_username_asc  : \n")
#select_sent_messages_by_username_asc(cursor, 'Moncho')
#print("=====================================================")

#print(" [INFO] : select_sent_messages_by_username_desc  : \n")
#select_sent_messages_by_username_desc(cursor, 'Moncho')
#print("=====================================================")

#print(" [INFO] : select_messages_for_recepient  : \n")
#select_messages_for_recepient(cursor, 'Moncho')
#print("=====================================================")

#print(" [INFO] : select_messages_for_recepient_date_asc  : \n")
#select_messages_for_recepient_date_asc(cursor, 'Moncho')
#print("=====================================================")

#print(" [INFO] : select_messages_for_recepient_date_desc  : \n")
#select_messages_for_recepient_date_desc(cursor, 'Moncho')
#print("=====================================================")