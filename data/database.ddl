CREATE TABLE roles (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	access_level INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (name)
);
CREATE TABLE logins (
	id INTEGER NOT NULL, 
	username VARCHAR NOT NULL, 
	password VARCHAR NOT NULL, 
	role_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (username), 
	FOREIGN KEY(role_id) REFERENCES roles (id)
);
CREATE TABLE address (
	id INTEGER NOT NULL, 
	street VARCHAR NOT NULL, 
	zip VARCHAR NOT NULL, 
	city VARCHAR NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE guest (
	id INTEGER NOT NULL, 
	firstname VARCHAR NOT NULL, 
	lastname VARCHAR NOT NULL, 
	email VARCHAR NOT NULL, 
	address_id INTEGER NOT NULL, 
	type VARCHAR NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(address_id) REFERENCES address (id)
);
CREATE TABLE registered_guest (
	id INTEGER NOT NULL, 
	login_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(id) REFERENCES guest (id), 
	FOREIGN KEY(login_id) REFERENCES logins (id)
);
CREATE TABLE hotel (
	id INTEGER NOT NULL, 
	name VARCHAR NOT NULL, 
	stars INTEGER NOT NULL, 
	address_id INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(address_id) REFERENCES address (id)
);
CREATE TABLE room (
	hotel_id INTEGER NOT NULL, 
	number VARCHAR NOT NULL, 
	type VARCHAR, 
	max_guests INTEGER NOT NULL, 
	description VARCHAR, 
	amenities VARCHAR, 
	price FLOAT NOT NULL, 
	is_available BOOLEAN NOT NULL, 
	PRIMARY KEY (hotel_id, number), 
	FOREIGN KEY(hotel_id) REFERENCES hotel (id)
);
CREATE TABLE booking (
	id INTEGER NOT NULL, 
	room_hotel_id INTEGER NOT NULL, 
	room_number VARCHAR NOT NULL, 
	guest_id INTEGER NOT NULL, 
	number_of_guests INTEGER NOT NULL, 
	start_date DATE NOT NULL, 
	end_date DATE NOT NULL, 
	comment VARCHAR, 
	PRIMARY KEY (id), 
	FOREIGN KEY(room_hotel_id, room_number) REFERENCES room (hotel_id, number), 
	FOREIGN KEY(guest_id) REFERENCES guest (id)
);
