# GPL License
# Copyright (C) UESTC
# All Rights Reserved
# @Author  : Xiao Wu
# @reference:

import logging
import sys
import os
import time
import hydra
from omegaconf import DictConfig, OmegaConf
from udl_vis.Basis.option import Config
from udl_cil.utils_log import create_logger
from typing import Union


@hydra.main(config_name="config")
def hydra_run(cfg: Union[DictConfig, Config]) -> None:
    if isinstance(cfg, DictConfig):
        cfg = Config(OmegaConf.to_container(cfg, resolve=True))
    cfg.merge_from_dict(cfg.args)
    cfg.__delattr__("args")

    cfg.experimental_desc = "example"

    logging_path = (
        cfg.work_dir
        + f"/exp_{cfg.trial_id}_{cfg.gpu_ids}_lr_{cfg.lr}_bs{cfg.bs}_{cfg.lam1}"
    )
    os.makedirs(logging_path, exist_ok=True)
    logger = create_logger(cfg, work_dir=logging_path)
    logger.info(cfg.pretty_text)
    logger.info(
        f"Process ID {os.getpid()} trail ID {cfg.trial_id} executing task {cfg.task} ..."
    )


def run():
    cfg = Config(
        dict(
            work_dir=os.path.dirname(__file__) + "/results",
            task="example",
            trial_id=0,
            args=dict(
                bs=1,
                lam1=1,
                lr=1e-1,
            ),
        )
    )
    hydra_run(cfg)


if __name__ == "__main__":
    if sys.gettrace():
        run()
    else:
        hydra_run()
