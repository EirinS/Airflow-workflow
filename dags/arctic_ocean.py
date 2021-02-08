# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
import base64
import os

DAG_NAME = 'ArcticOcean'
with DAG(
    DAG_NAME,
    description='A DAG decribing the Arctic Ocean flow',
    schedule_interval=None,
    start_date=days_ago(2),
) as ArcticOceanDag:

    get_config = BashOperator(
        task_id="get_config",
        bash_command='echo "{0}"'.format('{{ dag_run.conf }}'),
        dag=ArcticOceanDag
    )

    create_map = BashOperator(
        task_id='create_map',
        bash_command='matlab -batch \
           "cd {{ var.json.ap_cfg.matlab_code_path }}; prepare_paths(); cd map; disp(\'creating map...\');\
            savefig(plot_map( \
            \'{{ dag_run.conf.map.coast_res }}\', \'{{ dag_run.conf.map.color_db }}\', \
            {{ dag_run.conf.map.minlon }}, {{ dag_run.conf.map.maxlon }}, \
            {{ dag_run.conf.map.minlat }}, {{ dag_run.conf.map.maxlat }}, \
            {{ dag_run.conf.map.cenlon }}, {{ dag_run.conf.map.cenlat }}, \
            {{ dag_run.conf.map.radius }}, \'{{ dag_run.conf.map.shape }}\', \
            {{ dag_run.conf.map.depth }}), \
            \'map.fig\'); \
            savefig(plot_rigs(\'map.fig\', base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'), \'magenta\', \'o\'), \'map.fig\'); disp(\'receivers plotted.\'); \
            savefig(plot_rigs(\'map.fig\', base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'), \'white\', \'*\'), \'map.fig\'); disp(\'sources plotted.\'); \
            savefig(plot_paths(\'map.fig\', base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'), base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'), \
            [{{ dag_run.conf.map.minlon }} {{ dag_run.conf.map.maxlon  }} {{ dag_run.conf.map.minlat }} {{ dag_run.conf.map.maxlat }}]), \'map.fig\'); disp(\'paths plotted.\'); disp(\'Done.\');"',
        dag=ArcticOceanDag,
    )


    prepare_input = BashOperator(
        task_id='prepare_input',
        bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd prepareInput; \
        srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
        rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
        prepare_input_files({{ dag_run.conf.model.delR }}, {{ dag_run.conf.model.delC }}, src, rcvr, \'{{ var.json.ap_cfg.database_dir }}\', {{ dag_run.conf.model.ssp_database }}, {{ dag_run.conf.model.profile_type }}, {{ dag_run.conf.model.timestep }});"',
        dag=ArcticOceanDag
    )

    def select_model(**kwargs):
        return('ram_model.prepare_ram')

    branching = BranchPythonOperator(
        task_id='select_models',
        python_callable=select_model,
        dag=ArcticOceanDag
    )

    with TaskGroup('ram_model') as ram_model:
        prepare_ram = BashOperator(
            task_id='prepare_ram',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/RAM; \
            prepare_ram(100, 100, 100, \'ram.in\');"',
            dag=ArcticOceanDag
        )
        move_files = BashOperator(
            task_id='move_ram_files',
            bash_command='mv -f {{ var.json.ap_cfg.matlab_code_path}}/models/RAM/ram.in {{ var.json.ap_cfg.models_code_path}}/RAM/data ',
            dag=ArcticOceanDag
        )
        run_ram = BashOperator(
            task_id='run_ram',
            bash_command='cd {{ var.json.ap_cfg.models_code_path}}/RAM; bash launch_ram.sh ',
            dag=ArcticOceanDag
        )
        prepare_ram >> move_files >> run_ram
        

    with TaskGroup('bellhop_model') as bellhop_model:
        prepare_bellhop = BashOperator(
            task_id='prepare_bellhop',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Bellhop; \
            prepare_bellhop_input(100, 1, 100, 100);"',
            dag=ArcticOceanDag
        )
        
        move_files = BashOperator(
            task_id='move_bellhop_files',
            bash_command='mv -f {{ var.json.ap_cfg.matlab_code_path}}/models/Bellhop/belltemp.* {{ var.json.ap_cfg.models_code_path}}/Bellhop/data',
            dag=ArcticOceanDag
        )
        
        run_bellhop = BashOperator(
            task_id='run_bellhop',
            bash_command='cd {{ var.json.ap_cfg.models_code_path}}/Bellhop; bash launch_bellhop.sh ',
            dag=ArcticOceanDag
        )
        prepare_bellhop >> move_files >> run_bellhop

    with TaskGroup('eigenray_model') as eigenray_model:
        prepare_eigenray = BashOperator(
            task_id='prepare_eigenray',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Eigenray; \
            write_eigenray_input(2500, 0, [-15, 15], 1, 100, 100, 1, \'1e-7\', 3);"',
            dag=ArcticOceanDag
        )

        move_files = BashOperator(
            task_id='move_eigenray_files',
            bash_command='mv -f {{ var.json.ap_cfg.matlab_code_path}}/models/Eigenray/init.ray {{ var.json.ap_cfg.models_code_path}}/eigenraymp/data; \
                          cp {{ var.json.ap_cfg.database_dir}}/temp.* {{ var.json.ap_cfg.models_code_path}}/eigenraymp/data ',
            dag=ArcticOceanDag
        )
        
        run_eigenray = BashOperator(
            task_id='run_eigenray',
            bash_command='cd {{ var.json.ap_cfg.models_code_path}}/eigenraymp; bash launch_eigenray.sh ',
            dag=ArcticOceanDag
        )
        prepare_eigenray >> move_files >> run_eigenray


    with TaskGroup('mpiram_model') as mpiram_model:
        prepare_mpiram = BashOperator(
            task_id='prepare_mpiram',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/mpiRAM; \
            write_mpiram_input(5000, 100, \'temp\', 50, 5, 10);"',
            dag=ArcticOceanDag
        )

        move_files = BashOperator(
            task_id='move_mpiram_files',
            bash_command='mv -f {{ var.json.ap_cfg.matlab_code_path}}/models/mpiRAM/in.pe {{ var.json.ap_cfg.models_code_path}}/mpiramS/data; \
                          cp {{ var.json.ap_cfg.database_dir}}/temp.* {{ var.json.ap_cfg.models_code_path}}/mpiramS/data ',
            dag=ArcticOceanDag
        )
        
        run_mpiram = BashOperator(
            task_id='run_mpiram',
            bash_command='cd {{ var.json.ap_cfg.models_code_path}}/mpiramS; bash launch_mpiram.sh ',
            dag=ArcticOceanDag
        )
        prepare_mpiram >> move_files >> run_mpiram

get_config >> [create_map, prepare_input] 
prepare_input >> branching >> [ram_model, bellhop_model, eigenray_model, mpiram_model]