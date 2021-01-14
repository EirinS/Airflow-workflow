# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable

dag = DAG(
    'ArcticOcean',
    description='A DAG decribing the Arctic Ocean flow',
    schedule_interval=None,
    start_date=days_ago(2),
)

get_config = BashOperator(
    task_id="get_config",
    bash_command='echo "{0}"'.format('{{ var.json.map_params }}'),
    dag=dag
)

create_map = BashOperator(
    task_id='create_map',
    bash_command='matlab -batch \
        "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd map; \
        savefig(plot_map( \
        \'{{ var.json.map_params.coast_res }}\', \'{{ var.json.map_params.coloring_db }}\', \
        {{ var.json.map_params.minlon }}, {{ var.json.map_params.maxlon }}, \
        {{ var.json.map_params.minlat }}, {{ var.json.map_params.maxlat }}, \
        {{ var.json.map_params.cenlon }}, {{ var.json.map_params.cenlat }}, \
        {{ var.json.map_params.radius }}, \'{{ var.json.map_params.shape }}\', \
        {{ var.json.map_params.depth }}), \
        \'map.fig\')"',
    dag = dag,
)

show_map = BashOperator(
    task_id='show_map',
    bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}/map; fig = openfig(\'map.fig\'); set(fig, \'visible\', \'on\');"',
    dag=dag
)

get_config >> create_map >> show_map
