# Get Start

## Run docker-compose
Set directory to this folder
```
docker-compose up
```

## Set Superset
After starting the Superset server, initialize the database with an admin user and Superset tables using the superset-init helper script
```
docker exec -it superset superset-init
```

## Set MySQL to create database
- Enter to MySQL Cotainer
```
docker exec -it mysql bash
```
- Enter to MySQL
```
mysql -u superset -p
```
- Create Covid19 database
```
USE superset
CREATE TABLE daily_covid19_reports (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  date DATETIME,
  all_confirmed INT(6),
  all_recovered INT(6),
  all_hospitalized INT(6),
  all_deaths INT(6),
  confirmed INT(6),
  recovered INT(6),
  hospitalized INT(6),
  deaths INT(6)
);
CREATE TABLE daily_covid19_sources (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  date DATETIME,
  source VARCHAR(100),
  dev_by VARCHAR(100),
  server_by VARCHAR(100)
);
CREATE TABLE daily_covid19_percent (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  patient VARCHAR(20)
);
```

## Set Airflow
- Enter to installation directory of Airflow Cotainer
```
docker exec -it -u root airflow bash
```
pip install flask_bcrypt

python
from airflow import models, settings
from airflow.contrib.auth.backends.password_auth import PasswordUser
user = PasswordUser(models.User())
user.username = 'bu_intern'
user.email = 'arissara.piromya@gmail.com'
user.password = 'aaabcd1213'
user.superuser = True
session = settings.Session()
session.add(user)
session.commit()
session.close()
exit()
```
- Connection Airflow
Go to 127.0.0.1:8080 (Web UI)
- Create Connection
    Conn Id*  : Covid19
    Conn Type : MySQL    
    Host      : mysql
    Schema    : superset
    Login     : superset
    Password  : superset  
    Port      : 3306

## Run DAG and check result