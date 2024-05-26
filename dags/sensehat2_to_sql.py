from sqlalchemy import create_engine, URL, text
from credentials import Username, password
from airflow import DAG, macros
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import timedelta,datetime
import pendulum
import os

#query the necessary metadata
ROOM = "living"
OUTPUT_DIR = "/home/john/Documents/projects/ambience/sensehatData2/"

# create a URL string

url_str = URL.create(
    "postgresql+psycopg2"
    ,host = "woadamsj-All-Series"
    ,username = Username
    ,password = password
    ,database = "johnsdb"
)

# create a database engine
query_string = text(
    """
    select a.id, a.timezone, a.startrecorddt, b.hostname, b.username, b.pathname
    from ambience.location a
    left join ambience.pi b on a.pi_id = b.id
    where 1 = 1
        and a.active
        and a.room = :roomName
    """
    )

engine = create_engine(url_str)

with engine.connect() as conn:
    result = conn.execute(query_string,{"roomName":ROOM})
    pihat_loc_id, pihat_timezone, pihat_start_dt, pihat_hostname, pihat_username, pihat_path  =  result.fetchone()


local_tz = pendulum.timezone(pihat_timezone)
DAG_start = datetime(pihat_start_dt.year,pihat_start_dt.month,pihat_start_dt.day, tzinfo=local_tz)

#grab the previous day's readings

def csvToPostgres(path=OUTPUT_DIR,file=""):
    #Open Postgres Connection
    pg_hook = PostgresHook(postgres_conn_id='ambience')
    #get_postgres_conn = PostgresHook(postgres_conn_id='ambience').get_conn()
    pg_hook.copy_expert(
        sql="""
        COPY ambience.readings_stage (reading_dttm,temp,pressure,humidity,pitch,roll,yaw,accel_x,accel_y,accel_z) 
        from STDIN WITH CSV DELIMITER as ','
        """
        ,filename=path+file
        )

default_args = {
    'owner' : 'john'
    ,'retries' : 5
    ,'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id = 'sensehat2_to_sql'
    ,description = 'this dag moves data from sense hat id 2 to postgres database'
    ,start_date=DAG_start
    ,catchup = True
    ,schedule_interval = '10 3 * * *'
    ,params={
        'PI_USER':pihat_username
        ,'PI_HOST':pihat_hostname
        ,'PI_PATH': pihat_path
        ,'LOC_OUT_DIR': OUTPUT_DIR
        ,'LOC_ID': pihat_loc_id
        }
) as dag:
    
 #   filename = 'readings_' + {{ ds_add(ds, -1) }}.replace('-','_') + '.csv'
 #   print(filename)
 #   params_dict = {'READINGS_FILE': 'readings_' + {{ ds_add(ds, -1) }}.replace('-','_') + '.csv'}

    copy_task = BashOperator(
        task_id = 'scp_cmd'
        ,bash_command = "scp {{ params.PI_USER }}@{{ params.PI_HOST }}:{{ params.PI_PATH }}readings_$filedate.csv {{ params.LOC_OUT_DIR}}"
        ,env = {"filedate": '{{ macros.ds_format(macros.ds_add(ds,-1),"%Y-%m-%d","%Y_%m_%d") }}'}
    )

    stage_load = PythonOperator(
        task_id='csv_to_stage'
        ,python_callable=csvToPostgres
        ,op_kwargs = {'file': 'readings_{{ macros.ds_format(macros.ds_add(ds,-1),"%Y-%m-%d","%Y_%m_%d") }}.csv' }
    )

    stage_to_table = PostgresOperator(
        task_id = 'stage_data_to_table'
        ,postgres_conn_id = 'ambience'
        ,sql = """
            insert into ambience.readings(
                reading_dttm,
                temp, 
                pressure,
                humidity,
                pitch,
                roll,
                yaw,
                accel_x,
                accel_y,
                accel_z,
                location_id)
            select 
                reading_dttm,
                temp, 
                pressure,
                humidity,
                pitch,
                roll,
                yaw,
                accel_x,
                accel_y,
                accel_z,
                %(val)s
            from ambience.readings_stage;
            """
           ,parameters={"val": {{ params.LOC_ID }} }
    )

    clear_stage = PostgresOperator(
        task_id = 'clear_stage'
        ,postgres_conn_id = 'ambience'
        ,sql = 'delete from ambience.readings_stage where 1 = 1;'
    )

    zip_csv = BashOperator(
        task_id = 'zip_csv_file'
        ,bash_command="zip -ur {{ params.LOC_OUT_DIR }}old_readings.zip {{ params.LOC_OUT_DIR }}readings_$filedate.csv"
        ,env = {"filedate": '{{ macros.ds_format(macros.ds_add(ds,-1),"%Y-%m-%d","%Y_%m_%d") }}'}
    )

    rm_csv = BashOperator(
        task_id = 'remove_local_csv'
        ,bash_command="rm {{ params.LOC_OUT_DIR }}readings_$filedate.csv"
        ,env = {"filedate": '{{ macros.ds_format(macros.ds_add(ds,-1),"%Y-%m-%d","%Y_%m_%d") }}'}
    )

    copy_task >> stage_load >> stage_to_table >> clear_stage >> zip_csv >> rm_csv
