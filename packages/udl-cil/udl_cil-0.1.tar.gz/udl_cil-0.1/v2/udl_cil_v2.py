# GPL License
# Copyright (C) UESTC
# All Rights Reserved
# @Author  : Xiao Wu
# @reference:

import glob
import os
import sys
import subprocess
from rich.console import Console
from rich.theme import Theme
from udl_vis.Basis.config import Config
from os import path as osp
import optuna
from optuna.trial import TrialState
import numpy as np
import select
from functools import partial
from hydra import main
from omegaconf import OmegaConf, DictConfig
from hydra.core.hydra_config import HydraConfig
import GPUtil
import itertools
from optuna.storages import RetryFailedTrialCallback
import random


retry_count = 0
GPUs = GPUtil.getGPUs()
UDLPATH = "/Data2/woo/.cache/udl_vis/udl_vis"
STUDY_NAME = "UDL"

custom_theme = Theme({"info": "dim green", "warning": "magenta", "danger": "bold red"})
console = Console(theme=custom_theme)

# config = os.environ.get("MODEL_CONFIG")
# sys.path.append(osp.dirname(config))


class TRIALSTATE:
    RUNNING = "RUNNING"
    COMPLETE = "COMPLETE"
    PRUNED = "PRUNED"
    FAIL = "FAIL"
    WAITING = "WAITING"


def create_or_load_db(path, gpu_combinations, sampler=None):
    from optuna_pruner import DuplicateIterationPruner

    storage = optuna.storages.RDBStorage(
        url=f"sqlite:///{path}.sqlite3",
        heartbeat_interval=60,
        grace_period=120,
        # failed_trial_callback=RetryFailedTrialCallback(max_retry=len(gpu_combinations)),
    )

    study = optuna.create_study(
        study_name=STUDY_NAME,
        storage=storage,
        load_if_exists=True,
        sampler=sampler,
        pruner=DuplicateIterationPruner(),
    )

    return study


def get_trial_command(trial, opt: Config):
    work_dir = opt.work_dir
    cmd = []
    if opt.config_search:
        cmd = [opt.command]
    else:
        work_dir = f"{work_dir}/{opt.config_name}"
        cmd = [opt.command, opt.run_file]
        cmd.append(f"--config-name={opt.config_name}")
        cmd.append(f"--config-path={opt.config_path}")

    if opt.search_space:
        for key in opt.search_space:
            param = opt.search_space[key]
            method = getattr(trial, param["method"])
            value = method(**param["kwargs"])
            if key == "dir":
                cmd.append(osp.join(opt.config_path, value))
            elif key == "search_dataset":
                cmd.append(f"+{key}={value}")
            else:
                cmd.append(f"args.{key}={value}")
                work_dir += f"_{key}_{value}"

    cmd.append(f"+trial_id={opt.trial_id}")
    cmd.append(f"+work_dir={work_dir}")

    return cmd


def get_search_space(opt: Config):
    cfg = Config()
    for key in opt.search_space:
        param = opt.search_space[key]
        if param["kwargs"].get("choices"):
            cfg[key] = [v for v in param["kwargs"]["choices"]]
    return cfg


def tuple_to_string(tup):
    return ", ".join(str(x) for x in tup)


def objective(trial, opt, failed_trail_id=None):
    global retry_count

    if failed_trail_id:
        opt.trail_id = failed_trail_id
    else:
        opt.trial_id = trial.number

    cmd = get_trial_command(trial, opt)

    if cmd[0] == "python":
        cmd = [
            f"CUDA_VISIBLE_DEVICES={tuple_to_string(opt.gpu_combinations[retry_count])}",
            *cmd,
        ]
        cmd = ["bash", "-c", " ".join(cmd)]

    # 检查是否需要剪枝
    if trial.should_prune():
        raise optuna.TrialPruned()  # 如果被剪枝，抛出异常

    console.log(f"Running Command: [dim cyan]{cmd}[dim cyan]")

    # Run the command with nohup and subprocess
    try:
        with open(os.devnull, "w") as null_output:
            if sys.platform == "win32":
                from subprocess import CREATE_NEW_PROCESS_GROUP

                process = subprocess.Popen(
                    ["nohup", *cmd],
                    stdout=null_output,
                    stderr=null_output,
                    creationflags=CREATE_NEW_PROCESS_GROUP,
                )
            else:
                process = subprocess.Popen(
                    [
                        "nohup",
                        *cmd,
                    ],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    preexec_fn=os.setpgrp,  # Ensures the process is not killed with the terminal
                )

            trial.set_system_attr("pid", process.pid)
            trial.set_system_attr("p_state", TRIALSTATE.RUNNING)

            console.log(
                f"The process pid is [underline]{process.pid}[/underline]",
                style="info",
            )
            console.log("The process started successfully.", style="info")
    except Exception as e:
        retry_count += 1
        console.log(f"Error running shell script: {e}", style="danger")

    if opt.foreground:
        while True:
            reads = [process.stdout.fileno(), process.stderr.fileno()]
            for fd in select.select(reads, [], [])[0]:
                if fd == process.stdout.fileno():
                    output = process.stdout.readline()
                    output = output.decode().strip()
                    if len(output) > 0:
                        print(output)
                elif fd == process.stderr.fileno():
                    error = process.stderr.readline()
                    error = error.decode().strip()
                    if len(error) > 0:
                        print(error)

            # 检查子进程是否结束
            if process.poll() is not None:
                retry_count = 0
                break
    elif opt.n_jobs > 1:
        retry_count = 0
        process.communicate()

    return 0


def build_grid(cfg):
    config = cfg.config_path
    param_dicts = {}

    if cfg.search_space.dir:
        param_dicts.update(
            {"dir": [osp.basename(path) for path in glob.glob(f"{config}/*.sh")]}
        )
        print(
            f"Running all scripts (total: {len(param_dicts['dir'])} found in config: {config})"
        )
    if cfg.search_space.get("search_dataset"):
        if osp.isdir(cfg.search_space.search_dataset):
            param_dicts.update(
                {
                    "search_dataset": [
                        osp.basename(path)
                        for path in glob.glob(f"{cfg.search_space.search_dataset}/*")
                    ]
                }
            )
        else:
            param_dicts.update(
                {
                    "search_dataset": [
                        osp.basename(path)
                        for path in glob.glob(cfg.search_space.search_dataset)
                    ]
                }
            )
        print(
            f"Find the available datasets: {cfg.search_space.search_dataset}.\n"
            f"Running the program in parallel on these dataset (total: {len(param_dicts['search_dataset'])})"
        )

    cfg.search_space = {}
    for key, value in param_dicts.items():
        cfg.search_space.update(
            {
                key: {
                    "method": "suggest_categorical",
                    "kwargs": {"name": key, "choices": value},
                }
            }
        )
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    return cfg, param_dicts


def create(cfg):
    cfg.command = "sh"
    cfg, param_dicts = build_grid(cfg)

    print(cfg.pretty_text)

    study = create_or_load_db(cfg.work_dir, cfg.gpu_combinations)

    print("initialize ...")
    df = study.trials_dataframe(
        attrs=[
            "number",
            "value",
            "params",
            "user_attrs",
            "state",
        ]
    )
    print(df)
    with np.errstate(under="ignore"):
        rerun_fail_trials(study, partial(objective, opt=cfg))

    sampler = optuna.samplers.GridSampler(param_dicts, seed=42)

    print("sampler: ", sampler)

    study = create_or_load_db(cfg.work_dir, cfg.gpu_combinations, sampler=sampler)
    with np.errstate(under="ignore"):
        study.optimize(
            partial(objective, opt=cfg),
            n_jobs=cfg.n_jobs,
            n_trials=sampler._n_min_trials,
            timeout=10,
        )

    df = study.trials_dataframe(
        attrs=[
            "number",
            "value",
            "params",
            "user_attrs",
            "state",
        ]
    )
    print(df)


def create_experiment(cfg):
    sampler = None
    optuna.logging.set_verbosity(optuna.logging.WARNING)

    study = create_or_load_db(
        "/".join([cfg.work_dir, STUDY_NAME]), cfg.gpu_combinations
    )

    print("initialize ...")
    df = study.trials_dataframe(
        attrs=[
            "number",
            "value",
            "params",
            "user_attrs",
            "state",
        ]
    )
    print(df)

    rerun_fail_trials(study, partial(objective, opt=cfg))

    if cfg.search_space:
        param_dict = get_search_space(cfg)
        if cfg.sampler == "GridSampler":
            sampler = optuna.samplers.GridSampler(param_dict, seed=42)
            n_trials = sampler._n_min_trials
        elif cfg.sampler == "TPESampler":
            sampler = optuna.samplers.TPESampler()
            n_trials = cfg.n_trials

    print("sampler: ", sampler)

    study = create_or_load_db(
        "/".join([cfg.work_dir, STUDY_NAME]), cfg.gpu_combinations, sampler
    )

    study.optimize(partial(objective, opt=cfg), n_trials=n_trials, n_jobs=cfg.n_jobs)

    df = study.trials_dataframe(
        attrs=[
            "number",
            "value",
            "params",
            "user_attrs",
            "state",
        ]
    )
    print(df)


# 重新运行 FAIL 状态的实验
def rerun_fail_trials(study, objective):
    trials = study.get_trials()
    for trial in trials:
        if trial.state == optuna.trial.TrialState.FAIL:
            print(f"Rerunning trial {trial.number} with parameters: {trial.params}")
            # 创建一个新的试验并使用相同的参数
            new_trial = study.enqueue_trial(
                trial.params, user_attrs={"trial_id": trial.number}
            )
            # 运行新的试验
            study.optimize(objective, n_trials=1)


def overrides2dict(task):
    result_dict = {}
    for item in task:
        key, value = item.split("=")
        result_dict[key] = float(value)  # 如果需要将值转换为浮点数，可以使用 float()


@main(config_path="config", config_name="config")
def parser_args(cfg: DictConfig):
    if isinstance(cfg, DictConfig):
        cfg = Config(OmegaConf.to_container(cfg, resolve=True))
        hydra_cfg = HydraConfig.get()
        # overrides2dict(hydra_cfg.overrides.task)
        cfg.config_name = hydra_cfg.job.config_name
        cfg.config_path = hydra_cfg.runtime.config_sources[1].path

    cfg.gpu_combinations = list(
        itertools.combinations(range(0, len(GPUs)), len(cfg.gpu_ids))
    )

    if cfg.get("gpu_shuffle"):
        random.shuffle(cfg.gpu_combinations)

    cfg.n_jobs = cfg.get("n_jobs", 1)
    cfg.config_search = cfg.get("config_search")

    if cfg.get("gpu_mode") == "auto":
        cfg.gpu_combinations = random.shuffle(cfg.gpu_combinations)

    if cfg.config_search:
        cfg.func = create
        cfg.work_dir = hydra_cfg.runtime.output_dir
    else:
        cfg.work_dir = osp.join(
            hydra_cfg.runtime.output_dir, osp.basename(cfg.config_name)
        )
        cfg.func = create_experiment
        cfg.merge_from_dict(cfg.args)
        cfg.__delattr__("args")

    print("print args: ", cfg.pretty_text)
    print("Current working directory:", cfg.work_dir)
    os.makedirs(cfg.work_dir, exist_ok=True)

    cfg.func(cfg)


if __name__ == "__main__":
    parser_args()
