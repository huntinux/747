CREATE TABLE planes 
(
	id integer NOT NULL,
	name text,
	in_flight_amenities text,
	overview text,
	seatmap text, 
	seatmapkey text,
	CONSTRAINT planes_pkey PRIMARY KEY (id)
);

CREATE TABLE seating_detail 
(
	planeid integer REFERENCES planes(id),
	id integer NOT NULL,
	cls text,
	pitch text,
	width text, 
	details text,
	CONSTRAINT sd_pkey PRIMARY KEY (planeid,id)
);

CREATE TABLE seats
(
	planeid integer REFERENCES planes(id),
	id integer NOT NULL,
	seatnum text,
	cls text,
	seattype text,
	video text,
	ACpower text,
	descpt text,
	CONSTRAINT seats_pkey PRIMARY KEY (planeid,id)
);

