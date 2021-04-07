from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python import BranchPythonOperator
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow.utils.task_group import TaskGroup
from airflow.utils.trigger_rule import TriggerRule
from airflow.models.baseoperator import cross_downstream

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
        bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
           "addpath(genpath(pwd)); \
            plot_map( \
            \'{{ dag_run.conf.map.data_selection.coast_res }}\', \'{{ dag_run.conf.map.data_selection.color_db }}\', \
            {{ dag_run.conf.map.minlon }}, {{ dag_run.conf.map.maxlon }}, \
            {{ dag_run.conf.map.minlat }}, {{ dag_run.conf.map.maxlat }}, \
            {{ dag_run.conf.map.cenlon }}, {{ dag_run.conf.map.cenlat }}, \
            {{ dag_run.conf.map.radius }}, \'{{ dag_run.conf.map.shape }}\', \
            {{ dag_run.conf.map.data_selection.depth }}); \
            rcv = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); \
            src = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); \
            plot_rigs(rcv, \'magenta\', \'o\'); \
            plot_rigs(src, \'white\', \'*\'); \
            plot_paths(src, rcv, [{{ dag_run.conf.map.minlon }} {{ dag_run.conf.map.maxlon }} {{ dag_run.conf.map.minlat }} {{ dag_run.conf.map.maxlat }}]); \
            h = zeros(2, 1); \
            h(1) = plot(NaN,NaN,\'om\', \'MarkerFaceColor\', \'m\'); h(2) = plot(NaN,NaN,\'*w\'); \
            lgd = legend(h, \'receivers\', \'sources\', \'TextColor\', \'white\'); \
            set(lgd,\'color\',\'black\'); \
            frame = getframe(gcf); \
            imwrite(frame.cdata, \'{{ var.json.ap_cfg.save_dir }}/map_{{ dag_run.conf.map.data_selection.color_db }}_{{ dag_run.conf.map.data_selection.depth }}m_{{ ts_nodash }}.png\', \'png\');"',
        dag=ArcticOceanDag,
    )
    
    prepare_input = BashOperator(
        task_id='prepare_input',
        bash_command='matlab -sd {{ var.json.ap_cfg.project_dir }} -batch \
            "addpath(genpath(pwd)); \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            prepare_input_files({{ dag_run.conf.model.delR }}, {{ dag_run.conf.model.delC }}, src, rcvr, \'{{ var.json.ap_cfg.database_dir }}\', {{ dag_run.conf.model.ssp_database }}, {{ dag_run.conf.model.profile_type }}, {{ dag_run.conf.model.timestep }});"',
        dag=ArcticOceanDag
    )

    plot_bath_ssp = BashOperator(
        task_id='plot_bath_ssp',
        bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
            "addpath(genpath(pwd)); \
            load(\'ssp_bath.mat\'); \
            fig = plot_ssp_bath(res.r, res.z, res.src, res.rcv, res.typeVAR, res.stdDpts, res.plotSSPs); \
            saveas(fig, \'{{ var.json.ap_cfg.save_dir }}/ssp_bath_{{ ts_nodash }}.png\');"',
    )

    def select_model(**context):
        model_selection = context['dag_run'].conf['model']['model_choice']
        branches = []
        if model_selection['run_ram'] == True:
            branches.append('ram.prepare')
        if  model_selection['run_mpiram'] == True:
            branches.append('mpiram.prepare')
        if model_selection['run_bellhop'] == True:
            bellhop_type = model_selection['Bellhop']['simtype']
            for simtype in bellhop_type:
                branches.append(f'bellhop_{simtype}.prepare')
        if  model_selection['run_eigenray'] == True:
            branches.append('eigenray.prepare')
        return branches

    branching = BranchPythonOperator(
        task_id='select_models',
        python_callable=select_model,
        dag=ArcticOceanDag
    )

    remove_generated_files = BashOperator(
        task_id = "remove_generated_files",
        bash_command = "rm {{ var.json.ap_cfg.project_dir }}/* ; \
            echo 'removed files' ; \
            cd {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }} ; \
            echo 'removing model files' ; \
            rm -f RAM/data/* ; \
            rm -f mpiramS/data/* ; \
            rm -f Bellhop/data/* ; \
            rm -f eigenrayamp/data/* ",
            trigger_rule='none_failed',
        dag=ArcticOceanDag
    )


    with TaskGroup('ram') as ram_model:
        prepare_ram = BashOperator(
            task_id='prepare',
            bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch "addpath(genpath(pwd)); \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            prepare_ram({{ dag_run.conf.model.model_choice.RAM.freq }}, src(3), rcvr(3), \'ram.in\');"',
            dag=ArcticOceanDag
        )

        move_files = BashOperator(
            task_id='move_files',
            bash_command='mv -f {{ var.json.ap_cfg.project_dir }}/ram.in {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/RAM/data/ ',
            dag=ArcticOceanDag
        )

        run_ram = BashOperator(
            task_id='run',
            bash_command='cd {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/RAM; bash launch_ram.sh ',
            dag=ArcticOceanDag
        )

        plot_ram_result = BashOperator(
            task_id='plot_result',
            bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch "addpath(genpath(pwd)); \
            srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
            rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
            r = load(\'rangeBath.txt\'); \
            z = load(\'depth.txt\'); \
            res = read_ram_result({{ dag_run.conf.model.model_choice.RAM.freq }}, src(3), rcvr(3), r, z, \'{{ var.json.ap_cfg.models_dir }}/RAM/data/tl.grid\'); \
            plot_ram(res.freq, res.zs, res.zr, res.r, res.z, res.ttRAM, res.rdRAM, res.rrRAM); \
            saveas(gcf, \'{{ var.json.ap_cfg.save_dir }}/ram_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag
        )
        prepare_ram >> move_files >> run_ram >> plot_ram_result
        
    for simtype in ["E", "R", "C", "S", "I"]:
        with TaskGroup(f'bellhop_{simtype}') as bellhop_model:
            prepare_bellhop = BashOperator(
                task_id='prepare',
                bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch "addpath(genpath(pwd)); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                if strcmp(\'{{ params.simtype }}\', \'E\'); nrays = {{ dag_run.conf.model.model_choice.Bellhop.nerays }}; elseif strcmp(\'{{ params.simtype }}\', \'R\'); nrays = {{ dag_run.conf.model.model_choice.Bellhop.nrays }}; else; nrays = 0; end; \
                prepare_bellhop_input({{ dag_run.conf.model.model_choice.Bellhop.freq }}, \'{{ params.simtype }}\', src(3), rcvr(3), nrays, \'{{ var.json.ap_cfg.models_dir }}/Bellhop/data/belltemp_{{ params.simtype }}\');"',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )

            run_bellhop = BashOperator(
                task_id='run',
                bash_command='cd {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/Bellhop; bash launch_bellhop.sh belltemp_{{ params.simtype }} ',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )

            plot_bellhop_result = BashOperator(
                task_id='plot_result',
                bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch "addpath(genpath(pwd)); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                r = load(\'rangeBath.txt\'); \
                z = load(\'depth.txt\'); \
                plot_bellhop({{ dag_run.conf.model.model_choice.Bellhop.freq }}, \'{{ params.simtype }}\', src(3), rcvr(3), r, z, \'{{ var.json.ap_cfg.models_dir }}/Bellhop/data/belltemp_{{ params.simtype }}\'); \
                saveas(gcf, \'{{ var.json.ap_cfg.save_dir }}/bellhop_{{ params.simtype }}_{{ ts_nodash }}.png\')"',
                params={'simtype': simtype},
                dag=ArcticOceanDag
            )

            branching >> prepare_bellhop >> run_bellhop >> plot_bellhop_result

    with TaskGroup('eigenray') as eigenray_model:
        prepare_eigenray = BashOperator(
            task_id='prepare',
            bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
                "addpath(genpath(pwd)); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                write_eigenray_input({{ dag_run.conf.model.model_choice.Eigenray.ray_num }}, {{ dag_run.conf.model.model_choice.Eigenray.run_type }}, [{{ dag_run.conf.model.model_choice.Eigenray.angle_range }}], strcmp(\'{{ dag_run.conf.model.model_choice.Eigenray.save_paths }}\', \'True\'), src(3), rcvr(3), strcmp(\'{{ dag_run.conf.model.model_choice.Eigenray.use_bottom }}\', \'True\'), \'1e-5\', {{ dag_run.conf.model.model_choice.Eigenray.bot_reflect }});"',
            dag=ArcticOceanDag
        )

        move_files = BashOperator(
            task_id='move_files',
            bash_command='mv -f {{ var.json.ap_cfg.project_dir }}/init.ray {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/eigenraymp/data; \
            cp {{ var.json.ap_cfg.project_dir }}/temp.* {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/eigenraymp/data ',
            dag=ArcticOceanDag
        )
        
        run_eigenray = BashOperator(
            task_id='run',
            bash_command='cd {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/eigenraymp; bash launch_eigenray.sh ',
            dag=ArcticOceanDag
        )

        def select_plot(**context):
            eigenray_model = context['dag_run'].conf['model']['model_choice']['Eigenray']['run_type']
            if eigenray_model == 0:
                return 'eigenray.plot_eigenray'
            if eigenray_model == 1:
                return 'eigenray.plot_timefront'
            return []

        select_plot = BranchPythonOperator(
            task_id='select_plot',
            python_callable=select_plot,
            dag=ArcticOceanDag
        )

        plot_timefront = BashOperator(
            task_id='plot_timefront',
            bash_command = 'matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
                "addpath(genpath(pwd)); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                r = load(\'rangeBath.txt\'); \
                z = load(\'depth.txt\'); \
                res = read_eigenray_result(\'timefront\', r, z, src(3), rcvr(3), \'{{ var.json.ap_cfg.models_dir }}/eigenraymp/data/ray.info\', \'\'); \
                plot_timefront(res.nERays, res.arr_time, res.z_rec, res.blue_tpft, res.blue_tpfa, res.red_tpft, res.red_tpfa); \
                saveas(gcf, \'{{ var.json.ap_cfg.save_dir }}/eigenray_timefront_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag,
        )

        plot_eigenray = BashOperator(
            task_id='plot_eigenray',
            bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
                "addpath(genpath(pwd)); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                rcvrs = base64_to_mat(\'{{ dag_run.conf.map.receiver_file }}\'); rcvr = rcvrs({{ dag_run.conf.model.receiver }}, :); \
                r = load(\'rangeBath.txt\'); \
                z = load(\'depth.txt\'); \
                if strcmp(\'{{ dag_run.conf.model.model_choice.Eigenray.save_paths }}\', \'True\'); rayfile = \'{{ var.json.ap_cfg.models_dir }}/eigenraymp/data/ray.data\'; else rayfile = \'\'; end; \
                res = read_eigenray_result(\'eigenray\', r, z, src(3), rcvr(3), \'{{ var.json.ap_cfg.models_dir }}/eigenraymp/data/ray.info\', rayfile); \
                plot_eigenray(res.r, res.z, res.zs, res.zr, res.nERays, res.arr_time, res.arr_angle, res.ray); \
                saveas(gcf, \'{{ var.json.ap_cfg.save_dir }}/eigenray_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag,
        )

        prepare_eigenray >> move_files >> run_eigenray >> select_plot >> [plot_eigenray, plot_timefront]


    with TaskGroup('mpiram') as mpiram_model:
        prepare_mpiram = BashOperator(
            task_id='prepare',
            bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
                "addpath(genpath(pwd)); \
                srcs = base64_to_mat(\'{{ dag_run.conf.map.source_file }}\'); src = srcs({{ dag_run.conf.model.source }}, :); \
                r = load(\'rangeBath.txt\'); r = r(end)*1000; \
                write_mpiram_input(r, src(3), \'temp\', {{ dag_run.conf.model.model_choice.MPIRAM.freq }}, {{ dag_run.conf.model.model_choice.MPIRAM.q_value }}, {{ dag_run.conf.model.model_choice.MPIRAM.time_window }});"',
            dag=ArcticOceanDag
        )

        move_files = BashOperator(
            task_id='move_files',
            bash_command='mv -f {{ var.json.ap_cfg.project_dir }}/in.pe {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/mpiramS/data; \
            cp {{ var.json.ap_cfg.project_dir }}/temp.* {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/mpiramS/data ',
            dag=ArcticOceanDag
        )
        
        run_mpiram = BashOperator(
            task_id='run',
            bash_command='cd {{ var.json.ap_cfg.project_dir }}/{{ var.json.ap_cfg.models_dir }}/mpiramS; bash launch_mpiram.sh ',
            dag=ArcticOceanDag
        )

        plot_mpiram = BashOperator(
            task_id='plot_result',
            bash_command='matlab -noFigureWindows -sd {{ var.json.ap_cfg.project_dir }} -batch \
                "addpath(genpath(pwd)); \
                res = read_mpiram_result({{ dag_run.conf.model.model_choice.MPIRAM.freq }}, \'{{ var.json.ap_cfg.models_dir }}/mpiramS/data/psif.dat\', \'{{ var.json.ap_cfg.models_dir }}/mpiramS/data/recl.dat\'); \
                plot_mpiram(res.freq, res.cti, res.stt, res.taxis, res.zg, res.data, res.threshold, res.zrcv, res.data2, res.sangle, res.data3); \
                saveas(gcf, \'{{ var.json.ap_cfg.save_dir }}/mpiram_{{ ts_nodash }}.png\')"',
            dag=ArcticOceanDag
        )
        prepare_mpiram >> move_files >> run_mpiram >> plot_mpiram
        
    get_config >> remove_generated_files >> [create_map, prepare_input]
    prepare_input >> [plot_bath_ssp, branching]
    branching >> [ram_model, eigenray_model, mpiram_model]