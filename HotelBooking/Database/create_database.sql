CREATE TABLE customer
(
  customerId INTEGER PRIMARY KEY
);

CREATE TABLE administrator
(
  administratorId VARCHAR(10) NOT NULL PRIMARY KEY,
  administratorPassword VARCHAR(50) NOT NULL
);

CREATE TABLE room
(
  roomId VARCHAR(20) NOT NULL PRIMARY KEY,
  roomType TEXT CHECK(roomType IN ('SINGLE', 'DOUBLE', 'DELUXE', 'PRESIDENTIAL')) NOT NULL,
  roomStatus TEXT CHECK(roomStatus IN('AVAILABLE', 'CHECKED-IN', 'RESERVED')) NOT NULL DEFAULT 'AVAILABLE',
  customerId INTEGER,
  FOREIGN KEY(customerId) REFERENCES customer(customerId)
);

CREATE TABLE bill
(
  billId VARCHAR(20) NOT NULL PRIMARY KEY,
  billStatus TEXT CHECK(billStatus IN ('PAID', 'OUTSTANDING')) NOT NULL DEFAULT "OUTSTANDING",
  billAmount FLOAT NOT NULL,
  customerId INTEGER NOT NULL,
  FOREIGN KEY(customerId) REFERENCES customer(customerId)
);

INSERT INTO customer(customerId) VALUES(1);
INSERT INTO customer(customerId) VALUES(2);
INSERT INTO customer(customerId) VALUES(3);

INSERT INTO administrator(administratorId, administratorPassword) VALUES("sjin85", "251022168");
INSERT INTO administrator(administratorId, administratorPassword) VALUES("tbuwadi", "251023702");
INSERT INTO administrator(administratorId, administratorPassword) VALUES("jmerri6", "251044518");
INSERT INTO administrator(administratorId, administratorPassword) VALUES("vzhang23", "251029450");

INSERT INTO room(roomId, roomType) VALUES("single1", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single2", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single3", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single4", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single5", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single6", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single7", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single8", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single9", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single10", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single11", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single12", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single13", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single14", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single15", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single16", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single17", "SINGLE");
INSERT INTO room(roomId, roomType) VALUES("single18", "SINGLE");
INSERT INTO room(roomId, roomType, roomStatus, customerId) VALUES("single19", "SINGLE", "RESERVED", 1);
INSERT INTO room(roomId, roomType, roomStatus) VALUES("single20", "SINGLE", "AVAILABLE");

INSERT INTO room(roomId, roomType, roomStatus) VALUES("double1", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double2", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double3", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double4", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double5", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double6", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double7", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double8", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double9", "DOUBLE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("double10", "DOUBLE", "AVAILABLE");

INSERT INTO room(roomId, roomType, roomStatus) VALUES("deluxe1", "DELUXE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("deluxe2", "DELUXE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus) VALUES("deluxe3", "DELUXE", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus, customerId) VALUES("deluxe4", "DELUXE", "CHECKED-IN", 2);
INSERT INTO room(roomId, roomType, roomStatus) VALUES("deluxe5", "DELUXE", "AVAILABLE");

INSERT INTO room(roomId, roomType, roomStatus) VALUES("presidential1", "PRESIDENTIAL", "AVAILABLE");
INSERT INTO room(roomId, roomType, roomStatus, customerId) VALUES("presidential2", "PRESIDENTIAL", "CHECKED-IN", 3);
INSERT INTO room(roomId, roomType, roomStatus) VALUES("presidential3", "PRESIDENTIAL", "AVAILABLE");

INSERT INTO bill(billId, billStatus, billAmount, customerId) VALUES("asd456", "PAID", 50.25, 1);
INSERT INTO bill(billId, billStatus, billAmount, customerId) VALUES("xuasd13cx", "PAID", 12.25, 1);
INSERT INTO bill(billId, billAmount, customerId) VALUES("778asdc", 762.11, 3);