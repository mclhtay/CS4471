CREATE TABLE customer
(
  customer_id INTEGER NOT NULL PRIMARY KEY
);

CREATE TABLE administrator
(
  administrator_id VARCHAR(10) NOT NULL PRIMARY KEY,
  administrator_password VARCHAR(50) NOT NULL
);

CREATE TABLE room
(
  room_id VARCHAR(20) NOT NULL PRIMARY KEY,
  room_type TEXT CHECK(room_type IN ('SINGLE', 'DOUBLE', 'DELUXE', 'PRESIDENTIAL')) NOT NULL,
  room_status TEXT CHECK(room_status IN('AVAILABLE', 'CHECKED-IN', 'RESERVED')) NOT NULL DEFAULT 'AVAILABLE',
  customer_id INTEGER,
  FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);

CREATE TABLE bill
(
  bill_id INTEGER PRIMARY KEY,
  bill_status TEXT CHECK(bill_status IN ('PAID', 'OUTSTANDING')) NOT NULL DEFAULT "OUTSTANDING",
  bill_amount FLOAT NOT NULL,
  customer_id INTEGER NOT NULL,
  FOREIGN KEY(customer_id) REFERENCES customer(customer_id)
);

INSERT INTO customer(customer_id) VALUES(1);
INSERT INTO customer(customer_id) VALUES(2);
INSERT INTO customer(customer_id) VALUES(3);

INSERT INTO administrator(administrator_id, administrator_password) VALUES("sjin85", "251022168");
INSERT INTO administrator(administrator_id, administrator_password) VALUES("tbuwadi", "251023702");
INSERT INTO administrator(administrator_id, administrator_password) VALUES("jmerri6", "251044518");
INSERT INTO administrator(administrator_id, administrator_password) VALUES("vzhang23", "251029450");

INSERT INTO room(room_id, room_type) VALUES("single1", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single2", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single3", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single4", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single5", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single6", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single7", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single8", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single9", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single10", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single11", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single12", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single13", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single14", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single15", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single16", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single17", "SINGLE");
INSERT INTO room(room_id, room_type) VALUES("single18", "SINGLE");
INSERT INTO room(room_id, room_type, room_status, customer_id) VALUES("single19", "SINGLE", "RESERVED", 1);
INSERT INTO room(room_id, room_type, room_status) VALUES("single20", "SINGLE", "AVAILABLE");

INSERT INTO room(room_id, room_type, room_status) VALUES("double1", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double2", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double3", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double4", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double5", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double6", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double7", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double8", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double9", "DOUBLE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("double10", "DOUBLE", "AVAILABLE");

INSERT INTO room(room_id, room_type, room_status) VALUES("deluxe1", "DELUXE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("deluxe2", "DELUXE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status) VALUES("deluxe3", "DELUXE", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status, customer_id) VALUES("deluxe4", "DELUXE", "CHECKED-IN", 2);
INSERT INTO room(room_id, room_type, room_status) VALUES("deluxe5", "DELUXE", "AVAILABLE");

INSERT INTO room(room_id, room_type, room_status) VALUES("presidential1", "PRESIDENTIAL", "AVAILABLE");
INSERT INTO room(room_id, room_type, room_status, customer_id) VALUES("presidential2", "PRESIDENTIAL", "CHECKED-IN", 3);
INSERT INTO room(room_id, room_type, room_status) VALUES("presidential3", "PRESIDENTIAL", "AVAILABLE");

INSERT INTO bill( bill_status, bill_amount, customer_id) VALUES("PAID", 50.25, 1);
INSERT INTO bill( bill_status, bill_amount, customer_id) VALUES("PAID", 12.25, 1);
INSERT INTO bill( bill_amount, customer_id) VALUES(762.11, 3);