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
            ID_num = line.__getitem__(0)
            sample_ID = line.__getitem__(1)
            primary = line.__getitem__(2)
            secondary = line.__getitem__(3)
            additional_info = line.__getitem__(4)
            # print(ID_num,sample_ID,primary,secondary,additional_info)
            cur.execute(
                'INSERT IGNORE INTO Conditions_Annotations(Condit_ID,PrimaryComponent,SecondaryComponent,Additional_Information) VALUES (%s,%s,%s,%s)',
                (sample_ID, primary, secondary, additional_info))
    # insertions for Yeast-gene and Localization table and Yeast-gene&localization join table
    with open("data/combined_BP_CC_MF.csv", 'r') as r1:
        # skips first line the headers
        next(r1)
        for line in r1:
            line = line.split(',')
            ID_num = int(line.__getitem__(0)) + 1
            ID_num = str(ID_num)
            gene = line.__getitem__(1)
            valid = line.__getitem__(2)
            bp = line.__getitem__(3)
            cc = line.__getitem__(4)
            mf = line.__getitem__(5)
            cur.execute(
                'INSERT IGNORE INTO Yeast_Gene(Gene_ID,Validation, Biological_Process,Cellular_Component,Molecular_Function) VALUES (%s,%s,%s,%s,%s)',
                (gene, valid, bp, cc, mf))
            cur.execute(
                'INSERT IGNORE INTO Localization(Localization_ID,Biological_Process_Loc,Cellular_Component_Loc,Molecular_Function) VALUES (%s,%s,%s,%s)',
                (ID_num, bp, cc, mf))
            cur.execute('INSERT IGNORE INTO YeastGene_Localization(Gene_ID,Localization_ID) VALUES (%s,%s)', (gene, ID_num))
    # insertion for SC expression table
    with open("data/rf_SC_expressions.csv", 'r') as r1:
        next(r1)
        for line in r1:
            line = line.split(',')
            ID_num = int(line.__getitem__(0)) + 1
            ID_num = str(ID_num)
            gene = line.__getitem__(1)
            condit = line.__getitem__(2)
            sc = line.__getitem__(3)
            cur.execute('INSERT IGNORE INTO SC_Expression(Gene_ID,Condit_ID,SC_Expression) VALUES (%s,%s,%s)',
                        (gene, condit, sc))
cnx = make_connection()
cur = cnx.cursor()
setup_dp(cur)
insert_data(cur)
cur.close()
cnx.commit()
cnx.close()
