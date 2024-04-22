alter table if exists ambience.location
add constraint fk_loc_pi foreign key (pi_ID) references ambience.pi (id);