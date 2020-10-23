#import pymysql as ps
import sys
sys.path.insert(0,"/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
import pymysql as ps


# name db = database-2
# user_name = admin
# password: admin123
# make the connection to the db
def make_connection():
    return ps.connect(host='database-2.cykngyhgdi6y.us-east-1.rds.amazonaws.com', user='admin',
                      passwd='admin123',
                      port=3306, autocommit=True)

def setup_dp(cur):
    
    # Set up db
    cur.execute('DROP DATABASE IF EXISTS SuperbowlDB');
    cur.execute('CREATE DATABASE SuperbowlDB');
    cur.execute('USE SuperbowlDB');

    # Drop Existing Tables
    cur.execute('DROP TABLE IF EXISTS Team');
    cur.execute('DROP TABLE IF EXISTS Player');
    cur.execute('DROP TABLE IF EXISTS Stadium');
    cur.execute('DROP TABLE IF EXISTS Player_Team');
    cur.execute('DROP TABLE IF EXISTS Superbowl');
    # Create Tables
    cur.execute(
        '''CREATE TABLE Team(Name VARCHAR(500), PRIMARY KEY (Name));''')
    cur.execute(
        '''CREATE TABLE Player(Name VARCHAR(50), PRIMARY KEY (Name));''')
    cur.execute(
        '''CREATE TABLE Stadium(Name VARCHAR(500), City VARCHAR(50), State VARCHAR(50), PRIMARY KEY (Name));''')
    # Create Join Tables
    cur.execute(
        '''CREATE TABLE Player_Team(Player_Name VARCHAR(50), Team_Name VARCHAR(500), PRIMARY KEY (Player_Name, Team_Name), FOREIGN KEY (Player_Name) REFERENCES Player(Name), FOREIGN KEY (Team_Name) REFERENCES Team(Name));''')
    cur.execute(
        '''CREATE TABLE Superbowl(Date date, Title VARCHAR(50), Winner VARCHAR(500), Winner_Pts INT(2), Loser VARCHAR(500), Loser_Pts INT(2), MVP VARCHAR(50), Stadium VARCHAR(500), PRIMARY KEY (Title), FOREIGN KEY (Winner) REFERENCES Team(Name), FOREIGN KEY (Loser) REFERENCES Team(Name), FOREIGN KEY (MVP) REFERENCES Player(Name), FOREIGN KEY (Stadium) REFERENCES Stadium(Name));''')


def insert_data(cur):
        # Insertions for conditions table
    with open("superbowlPLUS.csv", 'r') as r1:
        # skips first line the headers
        next(r1)
        for line in r1:
            line = line.split(',')
            date = line.__getitem__(0)
            sbTitle = line.__getitem__(1)
            winner = line.__getitem__(2)
            winnerPts = line.__getitem__(3)
            loser = line.__getitem__(4)
            loserPts = line.__getitem__(5)
            MVP = line.__getitem__(6)
            stadium = line.__getitem__(7)
            city = line.__getitem__(8)
            state = line.__getitem__(9)
            # print(date,sbTitle,winner,winnerPts,loser,loserPts,MVP,stadium,city,state)
            cur.execute(
                'INSERT IGNORE INTO Team(Name) VALUES (%s)',
                (winner))
            cur.execute(
                'INSERT IGNORE INTO Team(Name) VALUES (%s)',
                (loser))
            cur.execute(
                'INSERT IGNORE INTO Player(Name) VALUES (%s)',
                (MVP))
            cur.execute(
                'INSERT IGNORE INTO Stadium(Name, City, State) VALUES (%s,%s,%s)',
                (stadium, city, state))
            cur.execute(
                'INSERT IGNORE INTO Player_Team(Player_Name, Team_Name) VALUES (%s,%s)',
                (MVP, winner))
            cur.execute(
                'INSERT IGNORE INTO Superbowl(date, sbTitle, winner, winnerPts, loser, loserPts, MVP, stadium) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',
                (date, sbTitle, winner, winnerPts, loser, loserPts, MVP, stadium))
cnx = make_connection()
cur = cnx.cursor()
setup_dp(cur)
insert_data(cur)
cur.close()
cnx.commit()
cnx.close()
