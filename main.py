import pymysql
from database import Database
from action import Action
connection = pymysql.connect(
    host='localhost', user='yunho', db='project_database', password='dbsgh0311', charset='utf8', cursorclass=pymysql.cursors.DictCursor, port=3306)



def select_action(index):
    message = ''
    messages = {1 : "print all buildings" ,
               2 : "print all performances",
               3 : "print all audiences",
               4 : "insert a new building",
               5 : "remove a building",
               6 : ",insert a new performance",
               7 : "remove a building",
               8 : "insert a new audience",
               9: "remove an audience",
               10 : "assign a performance to a building",
               11 : "book a performance",
               12 : "print all performances which assigned at a building",
               13 : "print all audiences who booked a performance",
               14 : "print ticket booking status of a performance",
               15 : "exit",
               16 : "reset database"
               }
    
    try:
        message = messages[index]
    except KeyError:
        print("no action on {}".format(index))
    else:
        print(message)

def load_db():
    db = Database.instance(db="project_database", user="yunho", password="dbsgh0311")
    return db


if __name__ == "__main__":
    print("initial database loading ...")
    db = load_db()
    actions = Action(db)

    while True:
        action_num = int(input("Select your action : "))
        if action_num == 15:
            break
        else:
            actions.perform_action(action_num)
    