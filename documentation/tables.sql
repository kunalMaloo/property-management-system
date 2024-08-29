-- Active: 1677761336126@@127.0.0.1@3306@RE

--ENTITY SETS

CREATE TABLE
    Clients(
        Client_ID INTEGER AUTO_INCREMENT,
        Name VARCHAR(255),
        Phone_no NUMERIC(10, 0),
        Password VARCHAR(255),
        PRIMARY KEY (Client_ID)
    );

CREATE TABLE
    Properties(
        P_ID INTEGER AUTO_INCREMENT,
        Address VARCHAR(255),
        Locality VARCHAR(255),
        Area INTEGER,
        Price INTEGER,
        Rent BOOLEAN,
        Date_Of_Construction DATE,
        No_Of_Bedrooms SMALLINT,
        Status VARCHAR(255),
        Sell_Date DATE,
        Sell_Price INTEGER,
        PRIMARY KEY (P_ID)
    );

CREATE TABLE
    Sellers(
        Seller_ID INTEGER AUTO_INCREMENT,
        Name VARCHAR(255),
        Phone_no NUMERIC(10, 0),
        Password VARCHAR(255)
        PRIMARY KEY (Seller_ID)
    );

CREATE TABLE
    Brokers(
        License_ID INTEGER AUTO_INCREMENT,
        Name VARCHAR(255),
        Phone_no NUMERIC(10, 0),
        Brokerage INTEGER,
        Locality VARCHAR(255),
        Password VARCHAR(255)
        PRIMARY KEY (License_ID)
    );

--RELATIONSHIP SETS

CREATE TABLE
    Holds(
        Client_ID INTEGER,
        P_ID INTEGER,
        FOREIGN KEY (Client_ID) REFERENCES Clients(Client_ID),
        FOREIGN KEY (P_ID) REFERENCES Properties(P_ID),
        PRIMARY KEY (Client_ID, P_ID)
    );

CREATE TABLE
    Sells(
        Seller_ID INTEGER,
        P_ID INTEGER,
        FOREIGN KEY (Seller_ID) REFERENCES Sellers(Seller_ID),
        FOREIGN KEY (P_ID) REFERENCES Properties(P_ID),
        PRIMARY KEY (P_ID)
    );

DROP TABLE Sells;

CREATE TABLE
    Shows(
        License_ID INTEGER,
        P_ID INTEGER,
        FOREIGN KEY (License_ID) REFERENCES Brokers(License_ID),
        FOREIGN KEY (P_ID) REFERENCES Properties(P_ID),
        PRIMARY KEY (License_ID, P_ID)
    );

CREATE TABLE
    Photos(
        P_ID INTEGER,
        Photo_URL VARCHAR(255),
        FOREIGN KEY (P_ID) REFERENCES Properties(P_ID),
        PRIMARY KEY (P_ID, Photo_URL)
    );

DELIMITER //

CREATE TRIGGER add_show AFTER INSERT ON `Properties` 
FOR EACH ROW BEGIN 
	INSERT INTO
	    Shows (License_ID, P_ID)
	SELECT License_ID, NEW.P_ID
	FROM Brokers
	WHERE Locality = NEW.Locality;
	END // 

DELIMITER ;

SELECT * FROM `Clients`;

CREATE INDEX Recently_Sold_Properties ON `Properties` (Sell_Date);

ALTER TABLE `Brokers` ADD COLUMN Password VARCHAR(255);

ALTER TABLE Brokers
ADD COLUMN Photo VARCHAR(255);



