# Starting Airflow
1. Install Apache Airflow: ``pip install apache-airflow``
2. Initialize the database: ``Airflow db init``
3. Create a user: 
```
    airflow users create \
        --username <username> \
        --firstname <your firstname> \
        --lastname <your lastname> \
        --role <Admin, Public, Viewer, User, or OP> \
        --email <your-email>
```
4. Start the webserver: `` airflow webserver --port 8080 ``
5. Start the scheduler: `` airflow scheduler ``
6. Go to localhost:8080 and log in with your newly created user.

# Testing tasks
* Run `` python <your file>.py `` and check for errors
* Print dags: ``airflow dags list``
* Print tasks: ``airflow tasks list <dag>``
* Test a task: ``airflow tasks test <dag> <task> <date>``

# Add variables from .json files

``airflow variables -i dags/settings.json``
