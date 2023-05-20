from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.postgres import PostgresOperator
from datetime import timedelta,date
import os

#grab the previous day's readings
filename = 'readings_' + {{ ds_add(ds,-1) }}.replace('-','_') + '.csv'
print(filename)

os.chdir("/home/john/Documents/projects/ambience/sensehatData1")
pihat_host_name = 'raspberrypihat'
pi_hat_username = 'pi'
pihat_path = '/home/pi/Documents/projects/ambience/output/'


default_args = {
    'owner' : 'john'
    ,'retries' : 5
    ,'retry_delay': timedelta(minutes=1)
}


with DAG(
    dag_id = 'senshat1_to_sql'
    ,description = 'this dag moves data from sense hat id 1 to postgres database'
    ,start_date=date(2022,12,10)
    ,scheduler_interval = '00 3 * * *'
    ,params={'PI_USER':pi_hat_username,'PI_HOST':pihat_host_name,'PI_PATH': pihat_path, 'READINGS_FILE': filename}
) as dag:
    copy_task = BashOperator(
        task_id = 'scp_cmd'
        ,bash_command='scp ${{ params.PI_USER }}@${{ params.PI_HOST }}:${{ params.PI_PATH }}${{ params.READINGS_FILE }} ./'
    )

    staging_load = PostgresOperator(
        task_id='csv_to_stage'
        ,postgres_conn_id = 'ambience'
        ,sql = """
                \copy ambience.readings_stage (reading_dttm,temp,pressure,humidity,pitch,roll,yaw,accel_x,accel_y,accel_z) 
                from {{ params.READINGS_FILE }} with (format csv);
            """
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

