# code by Julianna Shevchenko & Adam Curley

#import pymysql as ps
import sys
sys.path.insert(0,"/Library/Frameworks/Python.framework/Versions/3.9/lib/python3.9/site-packages")
import pymysql as ps


# name db = database-3
# user_name = admin
# password: admin123
# Make the connection to the db
def make_connection():
    return ps.connect(host='database-3.cykngyhgdi6y.us-east-1.rds.amazonaws.com', user='admin',
                      passwd='admin123',
                      port=3306, autocommit=True)

def query_db(cur):
    #Query db
    cur.execute('SELECT * FROM Superbowl');

    #Print result in terminal
    myresult = cur.fetchall();
    for x in myresult:
        print(x);

cnx = make_connection()
cur = cnx.cursor()

#query_db(cur)

cur.execute('USE SuperbowlDB');

print("Query #1")
cur.execute('SELECT Winner, COUNT(*) FROM Superbowl GROUP BY Winner ORDER BY COUNT(*) DESC');
myresult = cur.fetchall();
for x in myresult:
  print(x);
    
print("Query #2")
cur.execute('SELECT S.State, Count(*) FROM Superbowl SB, Stadium S WHERE SB.Stadium = S.Name GROUP BY S.State ORDER BY COUNT(*) DESC;');
myresult = cur.fetchall();
for x in myresult:
  print(x);

print("Query #3")
cur.execute('SELECT MVP, COUNT(*) FROM Superbowl GROUP BY MVP HAVING COUNT(*) > 1 ORDER BY COUNT(*) DESC;');
myresult = cur.fetchall();
for x in myresult:
  print(x);

print("Query #4")
cur.execute('SELECT Date, Winner_Pts, Loser_Pts FROM Superbowl ORDER BY Date DESC;');
myresult = cur.fetchall();
for x in myresult:
  print(x);

print("Query #5")
cur.execute('SELECT Month(Date), COUNT(*) FROM Superbowl GROUP BY Month(Date) ORDER BY Month(Date);');
myresult = cur.fetchall();
for x in myresult:
  print(x);

cur.close()
cnx.commit()
cnx.close()
