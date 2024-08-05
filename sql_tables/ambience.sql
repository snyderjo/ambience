create schema if not exists ambience;

create table if not exists ambience.location
(
    id serial PRIMARY KEY,
    house_nbr int NOT NULL,
    street_nm text NOT NULL,
    city_nm text NOT NULL,
    state_abbr text NOT NULL,
    zip int NOT NULL,
    room text NOT NULL
);

create table if not exists ambience.pi
(
    id serial PRIMARY KEY,
    hostname text NOT NULL,
    username text NOT NULL,
    pathname text Not NULL DEFAULT '/home/pi/Documents/projects/ambience/output'
);

alter table if exists ambience.location
add if not exists active boolean DEFAULT true,
add if not exists timezone text DEFAULT 'America/Denver',
add if not exists startRecordDt date DEFAULT '2022-12-22',
add if not exists endRecordDt date DEFAULT null,
add if not exists pi_ID int DEFAULT 1;


create table if not exists ambience.readings
(
    reading_id uuid DEFAULT gen_random_uuid () PRIMARY KEY,
    reading_dttm timestamptz NOT NULL,
    temp float,
    pressure float,
    humidity float,
    pitch float,
    roll float,
    yaw float,
    accel_x float,
    accel_y float,
    accel_z float,
    location_id int references ambience.location (id)
);

create table if not exists ambience.readings_stage
(
    reading_dttm timestamp with time zone NOT NULL,
    temp float,
    pressure float,
    humidity float,
    pitch float,
    roll float,
    yaw float,
    accel_x float,
    accel_y float,
    accel_z float
);

create table if not exists ambience.readings_stage2
(
    reading_dttm timestamp with time zone NOT NULL,
    temp float,
    pressure float,
    humidity float,
    pitch float,
    roll float,
    yaw float,
    accel_x float,
    accel_y float,
    accel_z float
);

alter table if exists ambience.location
alter active DROP DEFAULT,
alter active set not null,
alter timezone DROP DEFAULT,
alter timezone set not null,
alter startRecordDt DROP DEFAULT,
alter startRecordDt set not null,
alter pi_ID DROP DEFAULT,
alter pi_ID set not NULL;
