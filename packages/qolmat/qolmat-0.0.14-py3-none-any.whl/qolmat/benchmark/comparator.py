from functools import partial
from typing import Any, Callable, Dict, List, Optional

import numpy as np
import pandas as pd

from qolmat.benchmark import cross_validation, metrics, utils
from qolmat.benchmark.missing_patterns import _HoleGenerator


class Comparator:
    """
    This class implements a comparator for evaluating different imputation methods.

    Parameters
    ----------
    dict_models: Dict[str, any]
        dictionary of imputation methods
    selected_columns: List[str]
        list of column's names selected (all with at least one null value will be imputed)
    columnwise_evaluation : Optional[bool], optional
        whether the metric should be calculated column-wise or not, by default False
    dict_config_opti: Optional[Dict[str, Dict[str, Union[str, float, int]]]] = {}
        dictionary of search space for each implementation method. By default, the value is set to
        {}.
    n_calls_opt: int = 10
        number of calls of the optimization algorithm
        10.
    """

    dict_metrics: Dict[str, Callable] = {
        "mse": metrics.mean_squared_error,
        "rmse": metrics.root_mean_squared_error,
        "mae": metrics.mean_absolute_error,
        "wmape": metrics.weighted_mean_absolute_percentage_error,
        "wasserstein_columnwise": partial(metrics.wasserstein_distance, method="columnwise"),
        "KL_columnwise": partial(metrics.kl_divergence, method="columnwise"),
        "KL_gaussian": partial(metrics.kl_divergence, method="gaussian"),
        "ks_test": metrics.kolmogorov_smirnov_test,
        "correlation_diff": metrics.mean_difference_correlation_matrix_numerical_features,
        "pairwise_dist": metrics.sum_pairwise_distances,
        "energy": metrics.sum_energy_distances,
        "frechet": metrics.frechet_distance,
    }

    def __init__(
        self,
        dict_models: Dict[str, Any],
        selected_columns: List[str],
        generator_holes: _HoleGenerator,
        metrics: List = ["mae", "wmape", "KL_columnwise"],
        dict_config_opti: Optional[Dict[str, Any]] = {},
        n_calls_opt: int = 10,
    ):
        self.dict_imputers = dict_models
        self.selected_columns = selected_columns
        self.generator_holes = generator_holes
        self.metrics = metrics
        self.dict_config_opti = dict_config_opti
        self.n_calls_opt = n_calls_opt

    def get_errors(
        self,
        df_origin: pd.DataFrame,
        df_imputed: pd.DataFrame,
        df_mask: pd.DataFrame,
    ) -> pd.DataFrame:
        """Functions evaluating the reconstruction's quality

        Parameters
        ----------
        signal_ref : pd.DataFrame
            reference/orginal signal
        signal_imputed : pd.DataFrame
            imputed signal

        Returns
        -------
        dictionary
            dictionay of results obtained via different metrics
        """
        dict_errors = {}
        for name_metric in self.metrics:
            dict_errors[name_metric] = Comparator.dict_metrics[name_metric](
                df_origin, df_imputed, df_mask
            )
        errors = pd.concat(dict_errors.values(), keys=dict_errors.keys())
        return errors

    def evaluate_errors_sample(
        self,
        imputer: Any,
        df: pd.DataFrame,
        dict_config_opti_imputer: Dict[str, Any] = {},
    ) -> pd.Series:
        """Evaluate the errors in the cross-validation

        Parameters
        ----------
        tested_model : any
            imputation model
        df : pd.DataFrame
            dataframe to impute
        dict_config_opti_imputer : Dict
            search space for tested_model's hyperparameters

        Returns
        -------
        pd.DataFrame
            DataFrame with the errors for each metric (in column) and at each fold (in index)
        """
        list_errors = []
        df_origin = df[self.selected_columns].copy()
        for df_mask in self.generator_holes.split(df_origin):
            df_corrupted = df_origin.copy()
            df_corrupted[df_mask] = np.nan
            if dict_config_opti_imputer:
                cv = cross_validation.CrossValidation(
                    imputer,
                    dict_config_opti_imputer=dict_config_opti_imputer,
                    hole_generator=self.generator_holes,
                    n_calls=self.n_calls_opt,
                )
                imputer.hyperparams_optim = cv.optimize_hyperparams(df_corrupted)
            else:
                imputer.hyperparams_optim = {}
            df_imputed = imputer.fit_transform(df_corrupted)
            subset = self.generator_holes.subset
            errors = self.get_errors(df_origin[subset], df_imputed[subset], df_mask[subset])
            list_errors.append(errors)
        df_errors = pd.DataFrame(list_errors)
        errors_mean = df_errors.mean(axis=0)

        return errors_mean

    def compare(
        self,
        df: pd.DataFrame,
    ):
        """Function to compare different imputation methods on dataframe df

        Parameters
        ----------
        df : pd.DataFrame
        verbose : bool, optional
            _description_, by default True
        Returns
        -------
        pd.DataFrame
            dataframe with imputation
        """

        dict_errors = {}

        for name, imputer in self.dict_imputers.items():
            dict_config_opti_imputer = self.dict_config_opti.get(name, {})

            try:
                dict_errors[name] = self.evaluate_errors_sample(
                    imputer, df, dict_config_opti_imputer
                )
                print(f"Tested model: {type(imputer).__name__}")
            except Exception as excp:
                print("Error while testing ", type(imputer).__name__)
                raise excp

        df_errors = pd.DataFrame(dict_errors)

        return df_errors
