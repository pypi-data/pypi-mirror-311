"""
Based on [scikit-learn's Prediction Intervals for Gradient Boosting Regression](https://scikit-learn.org/1.5/auto_examples/ensemble/plot_gradient_boosting_quantile.html#prediction-intervals-for-gradient-boosting-regression)

A quantile regressor with approximate epistemic uncertainty
through synthetic data and supervised learning.
"""

import os

os.environ["KERAS_BACKEND"] = "jax"
import keras
from keras import layers
import jax.numpy as jnp


import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_pinball_loss
import sklearn.mixture
import sklearn.neighbors


import optuna
import sklearn.model_selection
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import GradientBoostingRegressor, HistGradientBoostingRegressor
from sklearn.metrics import make_scorer

import lightgbm as lgb

from . import sklearn_gbr_tuning
from . import lightgbm_tuning


class EpistemicQuantileRegressor:
    def __init__(
        self,
        synthetic_data_domain,
        N_synth=1000,
        method="gbr",
    ):
        """
        Parameters
        ----------
        synthetic_data_domain, list(2-tuple)
            A list of pairs of numbers understand to be
            the (min, max) values of the domain for this
            dimension. The length of this is the same as the
            number of dimensions.
        N_synth, int
            Number of samples to draw initially when generating
            synthetic data.
        method, std
            Either 'gbr' to use sklearn's GradientBoostingRegressor, 'ann' to use a Keras
            artifical neural network or 'lgb' to use LightGBM
        """
        self.synthetic_data_domain = synthetic_data_domain
        self.N_synth = N_synth
        self.method = method
        assert self.method in ["gbr", "ann", "lgb"], f"unknown {self.method = }"

    def fit(
        self,
        X,
        y,
        alphas=[0.05, 0.5, 0.95],
        **fit_kwargs,
    ):
        """
        Parameters
        ----------
        X, array [n samples, n dim]
            features
        y, array
            target [n_samples]
        alphas, list[float]
            Quantiles
        """

        if self.method == "gbr":
            self.models = self.train_sklearn_gbr(X, y, alphas, **fit_kwargs)
        elif self.method == "ann":
            self.models = self.train_keras_ann(X, y, alphas, **fit_kwargs)
        elif self.method == "lgb":
            self.models, self.study, self.params = self.train_lgb(
                X,
                y,
                alphas,
                fit_kwargs["n_trials"],
                fit_kwargs["fixed_params"],
                fit_kwargs["search_params"],
                fit_kwargs["cv_params"],
            )
        else:
            raise ValueError(f"unknown {self.method = }")
        return self

    def train_keras_ann(
        self,
        X,
        y,
        alphas,
        epochs=100,
        batch_size=32,
        verbose=1,
        units=[64, 64, 64, 64],
        activations=["selu", "selu", "selu", "selu"],
    ):
        models = {}
        for alpha in alphas:
            models[alpha] = self._fit_ann(
                X, y, alpha, epochs, batch_size, verbose, units, activations
            )
        return models

    def tilted_loss(self, q, y, f):
        """
        Keras quantile loss from [here](https://github.com/sachinruk/KerasQuantileModel/blob/master/Keras%20Quantile%20Model.ipynb)
        and [here](https://github.com/cgarciae/quantile-regression)
        """
        e = y - f
        return jnp.mean(jnp.maximum(q * e, (q - 1) * e), axis=-1)

    # def quantile_loss(q, y_true, y_pred):
    #     e = y_true - y_pred
    #     return jnp.maximum(q * e, (q - 1.0) * e)
    #
    def _fit_ann(self, X, y, alpha, epochs, batch_size, verbose, units, activations):
        model = keras.Sequential()
        model.add(layers.Input(shape=(X.shape[1],)))
        for unit, act in zip(units, activations):
            model.add(layers.Dense(unit, activation=act))
        model.add(layers.Dense(1))
        # model = keras.Sequential(
        #     [
        #         layers.Input(shape=(X.shape[1],)),
        #         layers.Dense(64, activation="selu"),
        #         layers.Dense(64, activation="selu"),
        #         layers.Dense(64, activation="selu"),
        #         layers.Dense(64, activation="selu"),
        #         layers.Dense(1),
        #     ]
        # )

        model.compile(loss=lambda y, f: self.tilted_loss(alpha, y, f), optimizer="adam")

        callback = keras.callbacks.EarlyStopping(monitor="loss", patience=100)

        model.fit(
            X,
            y,
            epochs=epochs,
            batch_size=batch_size,
            verbose=verbose,
            callbacks=[callback],
        )
        return model

    def train_lgb(self, X, y, alphas, n_trials, fixed_params, search_params, cv_params):

        models = {}
        study = {}
        params = {}

        for alpha in alphas:
            models[alpha], study[alpha], params[alpha] = (
                lightgbm_tuning.optimise_quantile_regressor(
                    X,
                    y,
                    alpha,
                    n_trials,
                    fixed_params,
                    search_params,
                    cv_params,
                )
            )

        return models, study, params

    def train_sklearn_gbr(self, X, y, alphas, n_trials=100):

        models = {}

        for alpha in alphas:
            models[alpha] = sklearn_gbr_tuning.optimise_quantile_regressor(
                X, y, alpha, n_trials, random_state=42
            )

        return models

    def generate_synthetic_ood_data(
        self,
        X,
        y,
        gm_kwargs={"n_components": 10},
        n_neighbors=1,
        scaling_factor=1,
    ):
        """
        First generate X and then compute y
        gm_kwargs, dict
            options to pass to sklearn's GaussianMixture()
        scaling_factor, number
            factor to scale the distance**2 term by
        """
        # fit generative model to X
        self.gmm = sklearn.mixture.GaussianMixture(**gm_kwargs).fit(X)
        # define threshold log-likelihood
        # log-likelihood values below this will be defined to be out-of-domain
        self.threshold_ll = self.gmm.score_samples(X).min()
        # draw samples uniformly over the whole domain defined by synthetic_data_domain
        D = len(self.synthetic_data_domain)
        min_values = [v[0] for v in self.synthetic_data_domain]
        max_values = [v[1] for v in self.synthetic_data_domain]
        X_synth = np.random.uniform(
            low=min_values, high=max_values, size=(self.N_synth, D)
        )

        ll_synth = self.gmm.score_samples(X_synth)
        mask = ll_synth > self.threshold_ll
        X_synth_in_domain = X_synth[mask]
        X_synth_out_domain = X_synth[~mask]

        # targets
        # TODO: allow n_neighbors to be configurable and
        # so that we are not as sensitive to outliers
        n_neighbors = 1
        # n_neighbors = 10
        nbrs = sklearn.neighbors.NearestNeighbors(
            n_neighbors=n_neighbors, algorithm="ball_tree"
        ).fit(X)
        distances, indices = nbrs.kneighbors(X_synth_out_domain)

        # turn the exponent into a variable?
        sigma_statistical = y.std()
        sigma_systematic = scaling_factor * distances**2
        # sigma_systematic = sigma_statistical * scaling_factor * distances**2
        # use more neighbors to estimate local statistical error?
        # sigma_statistical = y[indices].std()
        sigma_total = sigma_systematic + sigma_statistical

        y_synth_out_domain = np.random.normal(y[indices], sigma_total)[:, 0]

        return X_synth_out_domain, y_synth_out_domain

    def augment_training_data(self, X, y, X_ood, y_ood):
        X_aug = np.r_[X, X_ood]
        y_aug = np.concatenate([y, y_ood])

        return X_aug, y_aug

    def predict(self, X):

        if self.method == "gbr":
            return [model.predict(X)[:, np.newaxis] for k, model in self.models.items()]
        elif self.method == "ann":
            return [model(X) for k, model in self.models.items()]
        if self.method == "lgb":
            return [model.predict(X)[:, np.newaxis] for k, model in self.models.items()]
        else:
            raise ValueError(f"unknown {self.method = }")

        pass
