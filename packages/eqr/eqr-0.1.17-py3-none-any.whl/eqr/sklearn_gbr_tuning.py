def objective(trial, X, y, alpha, scoring_fn, random_state):
    # Define hyperparameter search space
    # params = {
    #     'n_estimators':...
    # }
    n_estimators = trial.suggest_int("n_estimators", 1, 100)
    # max_iter = trial.suggest_int("max_iter", 50, 200)
    max_depth = trial.suggest_int("max_depth", 3, 10)
    learning_rate = trial.suggest_float("learning_rate", 0.01, 0.2)

    # Create Gradient Boosting Regressor with the suggested hyperparameters
    model = GradientBoostingRegressor(
        loss="quantile",
        alpha=alpha,
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        random_state=random_state,
        # **params
    )
    # model = HistGradientBoostingRegressor(
    #     loss="quantile",
    #     quantile=alpha,
    #     max_iter=max_iter,
    #     max_depth=max_depth,
    #     learning_rate=learning_rate,
    #     random_state=42,
    # )

    # Evaluate the model using cross-validation
    # I think the mean is taken across k-folds
    score = cross_val_score(model, X, y, cv=5, scoring=scoring_fn).mean()

    return -score  # We are minimising with Optuna


def optimise_quantile_regressor(X, y, alpha, n_trials, random_state=42):
    neg_mean_pinball_loss_alpha = make_scorer(
        mean_pinball_loss, alpha=alpha, greater_is_better=False
    )

    # Create a study object
    study = optuna.create_study(direction="minimize")

    # Run the optimization process
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study.optimize(
        lambda trial: objective(
            trial, X, y, alpha, neg_mean_pinball_loss_alpha, random_state
        ),
        n_trials=n_trials,
        show_progress_bar=True,
        # n_jobs=4,
    )

    # Print the best hyperparameters and score
    print("Best hyperparameters:", study.best_params)
    print("Best score:", study.best_value)

    # Create the final model with the best hyperparameters
    best_model = GradientBoostingRegressor(
        random_state=random_state, loss="quantile", alpha=alpha, **study.best_params
    )
    # best_model = HistGradientBoostingRegressor(
    #     random_state=random_state, loss="quantile", quantile=alpha, **study.best_params
    # )
    best_model.fit(X, y)
    return best_model
