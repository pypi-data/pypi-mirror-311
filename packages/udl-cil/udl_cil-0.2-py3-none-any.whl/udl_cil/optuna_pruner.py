# GPL License
# Copyright (C) UESTC
# All Rights Reserved
# @Author  : Xiao Wu
# @reference:

import optuna
from optuna import logging
from optuna.pruners import BasePruner

_logger = logging.get_logger(__name__)


class DuplicateIterationPruner(BasePruner):
    """
    DuplicatePruner

    Pruner to detect duplicate trials based on the parameters.

    This pruner is used to identify and prune trials that have the same set of parameters
    as a previously completed trial.
    """

    def prune(
        self, study: "optuna.study.Study", trial: "optuna.trial.FrozenTrial"
    ) -> bool:
        completed_trials = study.get_trials(
            deepcopy=False, states=[optuna.trial.TrialState.COMPLETE]
        )
        for completed_trial in completed_trials:
            if completed_trial.params == trial.params:
                print(
                    f"Duplicated trial: {trial.params}, return {completed_trial.value}"
                )
                return True
        print(f"running trial: {trial.params}")
        return False
