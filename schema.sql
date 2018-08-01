# SQL commands to create database tables.

CREATE TABLE blocks(postal_code INT, address TEXT, town_name TEXT, town_code TEXT, lease_commenced_date DATE, lease_remaining INT, lease_period INT, building_gl INT);
ALTER TABLE blocks ADD PRIMARY KEY(postal_code);

CREATE TABLE resale_transactions(postal_code INT, resale_price DECIMAL, floor_area DECIMAL, floor_min INT, floor_max INT, registration_date DATE, model TEXT, flat_type TEXT, remaining_lease INT);
ALTER TABLE resale_transactions ADD PRIMARY KEY(postal_code, registration_date, resale_price);
