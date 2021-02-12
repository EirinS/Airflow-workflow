# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
import json

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
            [{{ dag_run.conf.map.minlon }} {{ dag_run.conf.map.maxlon  }} {{ dag_run.conf.map.minlat }} {{ dag_run.conf.map.maxlat }}]), \'map.fig\'); disp(\'paths plotted.\'); disp(\'Done.\'); \
            saveas(gcf, \'{{ var.json.ap_cfg.save_dir }}/map_{{ ts_nodash }}.png\');"',
        dag=ArcticOceanDag,
    )

    prepare_input = BashOperator(
        task_id='prepare_input',
        bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd prepareInput; disp(\'go to prepare input\'); \
        srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); disp(\'loaded sources\'); disp(src); \
        rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); disp(\'loaded receivers\'); disp(rcvr); \
        prepare_input_files({{ dag_run.conf.model.delR }}, {{ dag_run.conf.model.delC }}, src, rcvr, \'{{ var.json.ap_cfg.database_dir }}\', {{ dag_run.conf.model.ssp_database }}, {{ dag_run.conf.model.profile_type }}, {{ dag_run.conf.model.timestep }});"',
        dag=ArcticOceanDag
    )

    def select_model(**context):
        model_selection = context['dag_run'].conf['model']['model_choice']
        branches = []
        if model_selection['run_ram'] == True:
            branches.append('ram_model.prepare_ram')
        if  model_selection['run_mpiram'] == True:
            branches.append('mpiram_model.prepare_mpiram')
        if model_selection['run_bellhop'] == True:
            bellhop_type = model_selection['Bellhop']['simtype']
            for simtype in bellhop_type:
                branches.append(f'bellhop_model_{simtype}.prepare_bellhop')
        if  model_selection['run_eigenray'] == True:
            branches.append('eigenray_model.prepare_eigenray')
        return branches

    branching = BranchPythonOperator(
        task_id='select_models',
        python_callable=select_model,
        dag=ArcticOceanDag
    )

    with TaskGroup('ram_model') as ram_model:
        prepare_ram = BashOperator(
            task_id='prepare_ram',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/RAM; \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            prepare_ram({{ dag_run.conf.model.model_choice.RAM.freq }}, src(3), rcvr(3), \'ram.in\');"',
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

        plot_ram_result = BashOperator(
            task_id='plot_ram_result',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/RAM; \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                r = load(\'{{ var.json.ap_cfg.tmp_dir }}/rangeBath.txt\'); \
                z = load(\'{{ var.json.ap_cfg.tmp_dir }}/depth.txt\'); \
                res = read_ram_result({{ dag_run.conf.model.model_choice.RAM.freq }}, src(3), rcvr(3), r, z, \'{{ var.json.ap_cfg.models_code_path}}/RAM/data/tl.grid\'); \
                fig = figure(\'visible\', \'off\'); \
                plot_ram(res.freq, res.zs, res.zr, res.r, res.z, res.ttRAM, res.rdRAM, res.rrRAM); \
                saveas(fig, \'{{ var.json.ap_cfg.save_dir }}/ram_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag
        )
        prepare_ram >> move_files >> run_ram >> plot_ram_result
        
    for simtype in ["E", "R", "C", "S", "I"]:
        with TaskGroup(f'bellhop_model_{simtype}') as bellhop_model:
            prepare_bellhop = BashOperator(
                task_id='prepare_bellhop',
                bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Bellhop; \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                prepare_bellhop_input({{ dag_run.conf.model.model_choice.Bellhop.freq }}, \'{{ params.simtype }}\', src(3), rcvr(3), \'{{ var.json.ap_cfg.models_code_path}}/Bellhop/data/belltemp_{{ params.simtype }}\');"',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )
            """
            move_files = BashOperator(
                task_id='move_bellhop_files',
                bash_command='mv -f {{ var.json.ap_cfg.matlab_code_path}}/models/Bellhop/belltemp_{{ params.simtype }}.* {{ var.json.ap_cfg.models_code_path}}/Bellhop/data',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )
            """
            run_bellhop = BashOperator(
                task_id='run_bellhop',
                bash_command='cd {{ var.json.ap_cfg.models_code_path}}/Bellhop; bash launch_bellhop.sh belltemp_{{ params.simtype }} ',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )

            plot_bellhop_result = BashOperator(
                task_id='plot_bellhop_result',
                bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Bellhop; addpath(\'Matlab\'); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                r = load(\'{{ var.json.ap_cfg.tmp_dir }}/rangeBath.txt\'); \
                z = load(\'{{ var.json.ap_cfg.tmp_dir }}/depth.txt\'); \
                fig = figure(\'visible\', \'off\'); \
                plot_bellhop({{ dag_run.conf.model.model_choice.Bellhop.freq }}, \'{{ params.simtype }}\', src(3), rcvr(3), r, z, \'{{ var.json.ap_cfg.models_code_path}}/Bellhop/data/belltemp_{{ params.simtype }}\'); \
                saveas(fig, \'{{ var.json.ap_cfg.save_dir }}/bellhop_{{ params.simtype }}_{{ ts_nodash }}.png\')"',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )

            branching >> prepare_bellhop >> run_bellhop >> plot_bellhop_result

    with TaskGroup('eigenray_model') as eigenray_model:
        prepare_eigenray = BashOperator(
            task_id='prepare_eigenray',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Eigenray; \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            write_eigenray_input({{ dag_run.conf.model.model_choice.Eigenray.ray_num }}, {{ dag_run.conf.model.model_choice.Eigenray.run_type }}, [{{ dag_run.conf.model.model_choice.Eigenray.angle_range }}], strcmp(\'{{ dag_run.conf.model.model_choice.Eigenray.save_paths }}\', \'True\'), src(3), rcvr(3), strcmp(\'{{ dag_run.conf.model.model_choice.Eigenray.use_bottom }}\', \'True\'), {{ dag_run.conf.model.model_choice.Eigenray.epsilon }}, {{ dag_run.conf.model.model_choice.Eigenray.bot_reflect }});"',
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

        def select_plot(**context):
            eigenray_model = context['dag_run'].conf['model']['model_choice']['Eigenray']['run_type']
            if eigenray_model == 0:
                return 'eigenray_model.plot_eigenray'
            if eigenray_model == 1:
                return 'eigenray_model.plot_timefront'
            return []

        select_plot = BranchPythonOperator(
            task_id='select_plot',
            python_callable=select_plot,
            dag=ArcticOceanDag
        )

        plot_timefront = BashOperator(
            task_id='plot_timefront',
            bash_command = 'matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Eigenray; \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            r = load(\'{{ var.json.ap_cfg.tmp_dir }}/rangeBath.txt\'); \
            z = load(\'{{ var.json.ap_cfg.tmp_dir }}/depth.txt\'); \
            res = read_eigenray_result(\'timefront\', r, z, src(3), rcvr(3), \'{{ var.json.ap_cfg.models_code_path}}/eigenraymp/data/ray.info\', \'\'); \
            fig = figure(\'visible\', \'off\'); \
            plot_timefront(res.nERays, res.arr_time, res.z_rec, res.blue_tpft, res.blue_tpfa, res.red_tpft, res.red_tpfa); \
            saveas(fig, \'{{ var.json.ap_cfg.save_dir }}/eigenray_timefront_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag,
        )

        plot_eigenray = BashOperator(
            task_id='plot_eigenray',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/Eigenray; \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            r = load(\'{{ var.json.ap_cfg.tmp_dir }}/rangeBath.txt\'); \
            z = load(\'{{ var.json.ap_cfg.tmp_dir }}/depth.txt\'); \
            if strcmp(\'{{ dag_run.conf.model.model_choice.Eigenray.save_paths }}\', \'True\'); rayfile = \'{{ var.json.ap_cfg.models_code_path}}/eigenraymp/data/ray.data\'; else rayfile = \'\'; end; \
            res = read_eigenray_result(\'eigenray\', r, z, src(3), rcvr(3), \'{{ var.json.ap_cfg.models_code_path}}/eigenraymp/data/ray.info\', rayfile); \
            fig = figure(\'visible\', \'off\'); \
            plot_eigenray(res.r, res.z, res.zs, res.zr, res.nERays, res.arr_time, res.arr_angle, res.ray); \
            saveas(fig, \'{{ var.json.ap_cfg.save_dir }}/eigenray_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag,
        )

        prepare_eigenray >> move_files >> run_eigenray >> select_plot >> [plot_eigenray, plot_timefront]


    with TaskGroup('mpiram_model') as mpiram_model:
        prepare_mpiram = BashOperator(
            task_id='prepare_mpiram',
            bash_command='matlab -batch "cd {{ var.json.ap_cfg.matlab_code_path}}; prepare_paths(); cd models/mpiRAM; \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            r = load(\'{{ var.json.ap_cfg.tmp_dir }}/rangeBath.txt\'); r = r(end)*1000; \
            write_mpiram_input(r, src(3), \'temp\', {{ dag_run.conf.model.model_choice.MPIRAM.freq }}, {{ dag_run.conf.model.model_choice.MPIRAM.q_value }}, {{ dag_run.conf.model.model_choice.MPIRAM.time_window }});"',
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

