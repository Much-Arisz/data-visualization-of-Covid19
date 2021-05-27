import json
from datetime import datetime
from airflow import DAG
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.email_operator import EmailOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.utils import timezone
import requests

def clear_data_from_db():
    mysql_hook = MySqlHook(mysql_conn_id='Covid19')
    conn = mysql_hook.get_conn()
    cursor = conn.cursor()
    cursor.execute("TRUNCATE TABLE daily_covid19_reports")
    cursor.execute("TRUNCATE TABLE daily_covid19_sources")
    cursor.execute("TRUNCATE TABLE daily_covid19_percent")

def get_covid19_report_today():
    url = 'https://covid19.th-stat.com/api/open/timeline'
    response = requests.get(url)
    data = response.json()
    with open('data.json', 'w') as f:
        json.dump(data, f)
    return data
 
def save_data_into_db():
    mysql_hook = MySqlHook(mysql_conn_id='Covid19')
    with open('data.json') as f:
        data = json.load(f)
    for i in range(len(data['Data'])):
        insert = """
            INSERT INTO daily_covid19_reports (
                    date,
                    all_confirmed,
                    all_recovered,
                    all_hospitalized,
                    all_deaths,
                    confirmed,
                    recovered,
                    hospitalized,
                    deaths)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s); """
        mysql_hook.run(insert, parameters=(datetime.strptime(data['Data'][i]['Date'], '%m/%d/%Y'),
                   data['Data'][i]['Confirmed'],
                   data['Data'][i]['Recovered'],
                   data['Data'][i]['Hospitalized'],
                   data['Data'][i]['Deaths'],
                   data['Data'][i]['NewConfirmed'],
                   data['Data'][i]['NewRecovered'],
                   data['Data'][i]['NewHospitalized'],
                   data['Data'][i]['NewDeaths']))

        insert = """
            INSERT INTO daily_covid19_sources (
                date,
                source,
                dev_by,
                server_by)
            VALUES (%s, %s, %s, %s); """
        mysql_hook.run(insert, parameters=(datetime.strptime(data['Data'][i]['Date'], '%m/%d/%Y'),
                   data['Source'],
                   data['DevBy'],
                   data['SeverBy']))

    Recovered = data['Data'][len(data['Data'])-1]['Recovered']
    Hospitalized = data['Data'][len(data['Data'])-1]['Hospitalized']
    Deaths = data['Data'][len(data['Data'])-1]['Deaths']
    for i in range(Recovered):
        insert = """
            INSERT INTO daily_covid19_percent (
                patient)
            VALUES ("recovered"); """
        mysql_hook.run(insert)
    for i in  range(Hospitalized):
        insert = """
            INSERT INTO daily_covid19_percent (
                patient)
            VALUES ("Hospitalized"); """
        mysql_hook.run(insert)
    for i in  range(Deaths):
        insert = """
            INSERT INTO daily_covid19_percent (
                patient)
            VALUES ("deaths"); """
        mysql_hook.run(insert)

default_args = {
    'owner': 'Arissara',
    'start_date': datetime(2020, 9, 1),
    'email': ['arissara@mial.com'],
}
with DAG('covid19_data_pipeline',
         schedule_interval='@daily',
         default_args=default_args,
         description='A simple data pipeline for COVID-19 report',
         catchup=False,) as dag:

    t1 = PythonOperator(
        task_id='clear_data_from_db',
        python_callable=clear_data_from_db

    )

    t2 = PythonOperator(
        task_id='get_covid19_report_today',
        python_callable=get_covid19_report_today

    )
 
    t3 = PythonOperator(
        task_id='save_data_into_db',
        python_callable=save_data_into_db
    )

    t4 = EmailOperator(
        task_id='send_email',
        to=['arissara@mial.com'],
        subject='Your COVID-19 report today is ready',
        html_content='Please check your dashboard. :)'
    )
 
    t1 >> t2 >> t3 >> t4
