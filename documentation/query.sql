-- Active: 1677761336126@@127.0.0.1@3306@RE

--1

SELECT *
FROM `Properties`
WHERE
    YEAR(`Date_Of_Construction`) > 2018
    AND `Rent` IS TRUE;

--2

SELECT `Address`
FROM `Properties`
WHERE
    `Rent` = FALSE
    AND `Price` BETWEEN 300000 AND 500000;

--3

SELECT `Address`, `Price`
FROM `Properties`
WHERE
    `Locality` LIKE 'Suburbia'
    AND `No_Of_Bedrooms` > 2
    AND `Price` < 770000;

--4

WITH soldProperties AS (
        SELECT *
        FROM `Properties`
        WHERE
            YEAR(`Sell_Date`) = 2022
    ),
    agentProfit AS (
        SELECT
            `Name`,
            SUM(`Price`) as Profit
        FROM `Brokers`
            NATURAL JOIN `Shows`
            NATURAL JOIN soldProperties
        GROUP BY `Name`
    )
SELECT `Name`
FROM agentProfit
WHERE Profit = (
        SELECT MAX(Profit)
        FROM agentProfit
    );

--5

WITH soldProperties AS (
        SELECT *
        FROM `Properties`
        WHERE
            YEAR(`Sell_Date`) = 2020
    )
SELECT
    `Name`,
    AVG(`Sell_Price`) AS AvgSellingPrice,
    AVG(
        DATEDIFF(
            `Sell_Date`,
            `Date_Of_Construction`
        )
    ) AS AvgTimeOnMarket
FROM `Brokers`
    JOIN `Shows` ON `Brokers`.`License_ID` = `Shows`.`License_ID`
    JOIN soldProperties ON `Shows`.`P_ID` = soldProperties.`P_ID`
GROUP BY
    `Brokers`.`License_ID`;

--6

SELECT *
FROM Properties
WHERE Price = (
        SELECT MAX(Price)
        FROM Properties
        WHERE
            `Rent` IS FALSE
    )
    AND `Rent` IS FALSE
UNION
SELECT *
FROM Properties
WHERE Price = (
        SELECT MAX(Price)
        FROM Properties
        WHERE
            `Rent` IS TRUE
    )
    AND `Rent` IS TRUE;

SELECT * FROM `Properties`;