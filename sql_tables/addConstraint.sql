alter table if exists ambience_test.location
add constraint fk_loc_pi foreign key (pi_ID) references ambience_test.pi (id);