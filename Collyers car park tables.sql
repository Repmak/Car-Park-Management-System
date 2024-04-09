CREATE TABLE CollyersMembers(
MemberID varchar(30) PRIMARY KEY NOT NULL,
Fname varchar(20) NOT NULL,
Lname varchar(20) NOT NULL,
DOB date NOT NULL,
MemberType varchar(7) NOT NULL);

CREATE TABLE CollyersParking(
RegistrationNumber varchar(7) PRIMARY KEY NOT NULL,
Make varchar(30) NOT NULL,
Model varchar(30) NOT NULL,
PermitStartDate date NOT NULL,
PermitEndDate date NOT NULL,
MemberID varchar(30) FOREIGN KEY REFERENCES CollyersMembers(MemberID) NOT NULL);

INSERT INTO CollyersMembers
VALUES('22student295', 'studentfname', 'studentlname', '2005/09/27', 'Student')
INSERT INTO CollyersParking
VALUES('HT69VUK', 'VOLKSWAGEN', 'GOLF MATCH EDITION TSI EVO S-A', '2024/01/31', '2025/02/07', '22student295')

INSERT INTO CollyersMembers
VALUES('22student954', 'Arjun', 'Anish', '2005/11/08', 'Student')
INSERT INTO CollyersParking
VALUES('EN11LLG', 'BMW', '118D', '2023/02/03', '2023/02/14','22student954')

INSERT INTO CollyersMembers
VALUES('22student191', 'Kaiser', 'IP', '2005/06/07', 'Student')
INSERT INTO CollyersParking
VALUES('HT69NUV', 'RENAULT', 'CLIO ICONIC TCE', '2023/02/09', '2023/02/15', '22student191')

INSERT INTO CollyersMembers
VALUES('22student769', 'Oliver', 'Faulkner', '2005/02/07', 'Student')
INSERT INTO CollyersParking
VALUES('FM08BTU', 'FORD', 'FIESTA STYLE CLIMATE 16V', '2023/05/09', '2023/07/09', '22student769')

INSERT INTO CollyersMembers
VALUES('22student068', 'Viktor', 'Rozovits', '2006/02/25', 'Student')
INSERT INTO CollyersParking
VALUES('VA61CYW', 'FORD', 'FIESTA ZETEC TDCI', '2023/02/09', '2023/03/28', '22student068')

INSERT INTO CollyersMembers
VALUES('22student431', 'Alex', 'Jones', '2002/06/07', 'Visitor')
INSERT INTO CollyersParking
VALUES('DK20CXD', 'PEUGEOT', '308 BLUEHDI S/S SW ALLURE', '2023/03/09', '2023/03/10', '22student431')

INSERT INTO CollyersMembers
VALUES('teacher', 'teacherfname', 'teacherlname', '1980/06/07', 'Teacher')
INSERT INTO CollyersParking
VALUES('YY64VKE', 'BMW', '116D M SPORT AUTO', '2022/01/01', '2023/01/01', 'teacher')
