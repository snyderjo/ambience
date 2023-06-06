from airflow import DAG, macros
#from airflow.macros import ds_add, ds_format
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook
from datetime import timedelta,datetime
import os

#grab the previous day's readings

output_dir = "/home/john/Documents/projects/ambience/sensehatData1/"
pihat_host_name = 'raspberrypihat'
pi_hat_username = 'pi'
pihat_path = '/home/pi/Documents/projects/ambience/output/'

def csvToPostgres(path=output_dir,file=""):
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
    dag_id = 'sensehat1_to_sql'
    ,description = 'this dag moves data from sense hat id 1 to postgres database'
    ,start_date=datetime(2022,12,10)
    ,catchup = True
    ,schedule_interval = '00 3 * * *'
    ,params={
        'PI_USER':pi_hat_username
        ,'PI_HOST':pihat_host_name
        ,'PI_PATH': pihat_path
        ,"LOC_OUT_DIR": output_dir
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
                1
            from ambience.readings_stage;
            """
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
