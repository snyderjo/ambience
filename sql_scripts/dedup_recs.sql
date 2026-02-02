with tempdata as 
(
	select 
		*
		, row_number() over (partition by reading_dttm, location_id) as rownum 
		from ambience.readings
)
,dup_ids as 
(select reading_id from tempdata where rownum>1)
delete from ambience.readings where reading_id in (select reading_id  from dup_ids);
