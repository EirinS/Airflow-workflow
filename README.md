# Airflow Arctic Ocean Workflow

# Requirements
* MATLAB, tested with R2020
* Python, tested with 3.6
* Docker
* Node >= 10.16 and npm >= 5.6 
* Airflow >= 2.0

* The MATLAB source code repository
* The AcousticModel repository
* A folder containig rig files
* A folder containing database files

# Set up Airflow
1. Set airflow home to be the folder of this repository: ``export AIRFLOW_HOME=~/Airflow-workflow``
1. Install Apache Airflow: 
```
AIRFLOW_VERSION=2.0.1
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.0.1/constraints-3.6.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```
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

## Testing tasks
* Run `` python <your file>.py `` and check for errors
* Print dags: ``airflow dags list``
* Print tasks: ``airflow tasks list <dag>``

# Set up GUI
* Run `` npm start `` to launch the GUI in development mode, alternatively use `` npm run build `` to create a produvtion build of the app.
* Go to localhost:3000 and the GUI should appear.

# Running the workflow
1. Clone the repositories to a folder, for example into ~/ArcticOcean
2. Add the folders containing the database files and rig files to the folder containing the repositories
3. Check that the folder names match with the config in ``settings.json`` or change the settings to point to the correct folders:
```
{
    "ap_cfg":{
        "project_dir": "~/ArcticOcean",
        "matlab_lib":"Arctic.Ocean-v2",
        "models_dir":"AcousticModels",
        "database_dir":"dataBase",
        "save_dir": "savedResults"      
    }
}
```
For example, the workflow will look for the MATLAB source code under ``~/ArcticOcean/Arctic.Ocean-v2``.

4. Import the settings in settings.json to Airflow, either by copying the content to Admin -> Variables or by importing it through the CLI: ``airflow variables import settings.json``
5. Trigger the workflow through filling out the GUI at localhost:3000, and watch the progress at localhost:3000. Your results are saved as .png images in the specified ``save_dir`` from the settings.json file.
