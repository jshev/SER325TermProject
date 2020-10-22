DROP DATABASE IF EXISTS SuperbowlDB;
CREATE DATABASE SuperbowlDB;

USE SuperbowlDB;

DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Player;
DROP TABLE IF EXISTS Stadium;
DROP TABLE IF EXISTS Player_Team;
DROP TABLE IF EXISTS Superbowl;

CREATE TABLE Team
(
    Name VARCHAR(500),
	PRIMARY KEY (Name)
);

CREATE TABLE Player
(
    Name VARCHAR(50),
	PRIMARY KEY (Name)
);

CREATE TABLE Stadium
(
    Name VARCHAR(500),
    City VARCHAR(50),
    State VARCHAR(50),
	PRIMARY KEY (Name)
);

CREATE TABLE Player_Team
(
    Player_Name VARCHAR(50),
    Team_Name VARCHAR(500),
	PRIMARY KEY (Player_Name, Team_Name),
    FOREIGN KEY (Player_Name) REFERENCES Player(Name),
    FOREIGN KEY (Team_Name) REFERENCES Team(Name)
);

CREATE TABLE Superbowl
(
	Date date,
    Title VARCHAR(50),
    Winner VARCHAR(500),
    Winner_Pts INT(2),
    Loser VARCHAR(500),
    Loser_Pts INT(2),
    MVP VARCHAR(50),
    Stadium VARCHAR(500),
	PRIMARY KEY (Title),
    FOREIGN KEY (Winner) REFERENCES Team(Name),
    FOREIGN KEY (Loser) REFERENCES Team(Name),
    FOREIGN KEY (MVP) REFERENCES Player(Name),
    FOREIGN KEY (Stadium) REFERENCES Stadium(Name)
);

INSERT INTO Team VALUES
('Kansas City Chiefs'),
('San Francisco 49ers');
INSERT INTO Player VALUES
('Patrick Mahomes');
INSERT INTO Stadium VALUES
('Hard Rock Stadium', 'Miami Gardens', 'Florida');
INSERT INTO Player_Team VALUES
('Patrick Mahomes', 'Kansas City Chiefs');
INSERT INTO Superbowl VALUES
(' 2020-02-02', 'LIV (54)', 'Kansas City Chiefs', 31, 'San Francisco 49ers', 20, 'Patrick Mahomes', 'Hard Rock Stadium');

SELECT *
FROM Player_Team;




