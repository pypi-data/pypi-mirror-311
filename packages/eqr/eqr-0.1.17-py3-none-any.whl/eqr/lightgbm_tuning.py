from typing import DefaultDict
import lightgbm as lgb

import optuna

DEFAULT_FIXED_PARAMS = {
    "objective": "quantile",
    "metric": "quantile",
    "num_iterations": 100,
    "max_depth": -1,
    "learning_rate": 0.1,
    "verbose": -1,
    "min_data_in_leaf": 1,
    "seed": 5093840343,
    "num_threads": 0,
}

DEFAULT_SEARCH_PARAMS = [["num_leaves", "int", 31, 310]]


def update_params_dict(user_dict, default_dict):
    if user_dict is None:
        # if no user_dict given then use default
        user_dict = default_dict.copy()
    else:
        # if at least some fixed params given then update
        tmp = default_dict.copy()
        tmp.update(user_dict)
        user_dict = tmp.copy()
    return user_dict


def objective(
    trial,
    train_data,
    fixed_params,
    search_params,
    cv_params,
):

    params = fixed_params.copy()
    # then we update params with the search_params

    for search_param in search_params:
        name, dtype, low, high = search_param
        if dtype == "int":
            f_ = trial.suggest_int
        elif dtype == "float":
            f_ = trial.suggest_float
        else:
            raise ValueError(f"unknown {dtype = } given for {search_param = }")
        params[name] = f_(name, low, high)

    cv_results = lgb.cv(
        params=params,
        train_set=train_data,
        stratified=False,
        **cv_params,
    )

    score = cv_results["valid quantile-mean"][-1]  # is this correct?

    return score


def optimise_quantile_regressor(
    X,
    y,
    alpha,
    n_trials,
    fixed_params=None,
    search_params=None,
    cv_params={"nfold": 5},
):
    """
    fixed_params, dict | None
        A dictionary of lightgbm parameters.
        These values are not optimised.
    search_params, list[list] | None
        A list of lists that define the search space.
        Each list has 4 elements which are the name, dtype, low and high values.
        e.g. ['num_leaves', 'int', 31, 310]
    """

    fixed_params = update_params_dict(fixed_params, DEFAULT_FIXED_PARAMS)
    # update alpha
    fixed_params["alpha"] = alpha

    if search_params is None:
        search_params = DEFAULT_SEARCH_PARAMS

    # Create a study object
    study = optuna.create_study(direction="minimize")

    # Run the optimization process
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    train_data = lgb.Dataset(X, label=y)
    study.optimize(
        lambda trial: objective(
            trial,
            train_data,
            fixed_params,
            search_params,
            cv_params,
        ),
        n_trials=n_trials,
        show_progress_bar=True,
        # n_jobs=4,
    )

    # Print the best hyperparameters and score
    # print("Best hyperparameters:", study.best_params)
    # print("Best score:", study.best_value)

    # train model with all data and best parameters
    # update the fixed_params with the best_params
    params = fixed_params.copy()
    params.update(study.best_params.copy())

    # Train the model
    model = lgb.train(
        params=params,
        train_set=train_data,
    )

    return model, study, params
