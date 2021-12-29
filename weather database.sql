#weather data
create database weather
use weather

CREATE TABLE `rainfall` (
  `timestamp` timestamp NOT NULL,
  `station_id` varchar(5) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `reading` double NOT NULL
);

CREATE TABLE `temperature` (
  `timestamp` timestamp NOT NULL,
  `station_id` varchar(5) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `reading` double NOT NULL
);

CREATE TABLE `humidity` (
  `timestamp` timestamp NOT NULL,
  `station_id` varchar(5) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `reading` double NOT NULL
);

CREATE TABLE `windspeed` (
  `timestamp` timestamp NOT NULL,
  `station_id` varchar(5) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `reading` double NOT NULL
);

CREATE TABLE `winddirection` (
  `timestamp` timestamp NOT NULL,
  `station_id` varchar(5) NOT NULL,
  `latitude` double NOT NULL,
  `longitude` double NOT NULL,
  `reading` double NOT NULL
);

#download tables into csv
select * from rainfall where year(`timestamp`)>=2018 order by `timestamp`;
select * from temperature where year(`timestamp`)>=2018 order by `timestamp`;
select * from humidity where year(`timestamp`)>=2018 order by `timestamp`;
select * from winddirection where year(`timestamp`)>=2018 order by `timestamp`;
select * from windspeed where year(`timestamp`)>=2018 order by `timestamp`;