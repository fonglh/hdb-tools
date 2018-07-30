# SQL commands to create database tables.

CREATE TABLE blocks(postal_code INT, address TEXT, town_name TEXT, town_code TEXT, lease_commenced_date DATE, lease_remaining INT, lease_period INT, building_gl INT);
ALTER TABLE blocks ADD PRIMARY KEY(postal_code);
