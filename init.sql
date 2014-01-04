-- Database: test

--DROP DATABASE test;

--CREATE DATABASE test
--  WITH OWNER = "postgres"
--      ENCODING = 'UTF8'
--       LC_COLLATE = 'zh_CN.utf8'
--       LC_CTYPE = 'zh_CN.utf8'
--       CONNECTION LIMIT = -1;


-- Table: seats

--DROP TABLE seats;

CREATE TABLE seats
(
  id integer NOT NULL,
  seatnum text,
  cls text,
  seattype text,
  video text,
  power text,
  desct text,
  planetype text,
  CONSTRAINT seats_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE seats OWNER TO postgres;


-- Table: seating_detail

--DROP TABLE seating_detail;

CREATE TABLE seating_detail
(
  c_id integer NOT NULL,
  c_class text,
  c_pitch text,
  c_width text,
  c_details text,
  planetype text,
  CONSTRAINT seating_detail_pkey PRIMARY KEY (c_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE seating_detail OWNER TO postgres;

