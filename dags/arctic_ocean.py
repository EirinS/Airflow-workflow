# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup

DAG_NAME = 'ArcticOcean'
with DAG(
    DAG_NAME,
    description='A DAG decribing the Arctic Ocean flow',
    schedule_interval=None,
    start_date=days_ago(2),
) as ArcticOceanDag:

    get_config = BashOperator(
        task_id="get_config",
        bash_command='echo "{0}"'.format('{{ var.json.ap_params }}'),
        dag=ArcticOceanDag
    )

    create_map = BashOperator(
        task_id='create_map',
        bash_command='matlab -batch \
            "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd map; disp(\'creating map...\');\
            savefig(plot_map( \
            \'{{ var.json.ap_params.coast_res }}\', \'{{ var.json.ap_params.coloring_db }}\', \
            {{ var.json.ap_params.minlon }}, {{ var.json.ap_params.maxlon }}, \
            {{ var.json.ap_params.minlat }}, {{ var.json.ap_params.maxlat }}, \
            {{ var.json.ap_params.cenlon }}, {{ var.json.ap_params.cenlat }}, \
            {{ var.json.ap_params.radius }}, \'{{ var.json.ap_params.shape }}\', \
            {{ var.json.ap_params.depth }}), \
            \'map.fig\'); \
            savefig(plot_rigs(\'map.fig\', \'{{ var.json.ap_params.receiver_file[0][\'fileName\'] }}\', \'magenta\', \'o\'), \'map.fig\'); disp(\'receivers plotted.\');\
            savefig(plot_rigs(\'map.fig\', \'{{ var.json.ap_params.source_file[0][\'fileName\'] }}\', \'white\', \'*\'), \'map.fig\'); disp(\'sources plotted.\');\
            savefig(plot_paths(\'map.fig\', load(\'{{ var.json.ap_params.source_file[0][\'fileName\'] }}\'), load(\'{{ var.json.ap_params.receiver_file[0][\'fileName\'] }}\'), \
            [{{ var.json.ap_params.minlon }} {{ var.json.ap_params.maxlon }} {{ var.json.ap_params.minlat }} {{ var.json.ap_params.maxlat }}]), \'map.fig\'); disp(\'paths plotted.\'); disp(\'Done.\');"',
        dag=ArcticOceanDag,
    )

    prepare_input = BashOperator(
        task_id='prepare_input',
        bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd prepareInput; \
        srcs = load(\'{{ var.json.ap_params.source_file[0][\'fileName\'] }}\'); src = srcs(1, :); \
        rcvrs = load(\'{{ var.json.ap_params.receiver_file[0][\'fileName\'] }}\'); rcvr = rcvrs(3, :); \
        prepare_input_files(10, 5, src, rcvr, \'{{ var.json.ap_cfg.database_dir }}\', 0, 0, 0);"',
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