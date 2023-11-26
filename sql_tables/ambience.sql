create schema if not exists ambience_test;

create table if not exists ambience_test.location
(
    id serial PRIMARY KEY,
    house_nbr int NOT NULL,
    street_nm text NOT NULL,
    city_nm text NOT NULL,
    state_abbr text NOT NULL,
    zip int NOT NULL,
    room text NOT NULL 
);

create table if not exists ambience_test.pi
(
    id serial PRIMARY KEY,
    hostname text not null,
    pathname text default "/home/pi/Documents/projects/ambience/output"
)

alter table if exists ambience_test.location
add if not exists active boolean DEFAULT true,
add if not exists timezone text default "MST",
add if not exists endRecordDt date DEFAULT null,
add if not exists pi_ID int DEFAULT 1;


create table if not exists ambience_test.readings
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
    location_id int references ambience_test.location (id)
);

create table if not exists ambience_test.readings_stage
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