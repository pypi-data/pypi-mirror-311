from __future__ import annotations

import itertools

import numpy as np

from river import datasets


class AnomalySine(datasets.base.SyntheticDataset):
    """Simulate a stream with anomalies in sine waves.

    The amount of data generated by this generator is finite.

    The data generated corresponds to sine and cosine functions. Anomalies are induced by
    replacing the cosine values with values from a different a sine function. The `contextual`
    flag can be used to introduce contextual anomalies which are values in the normal global
    range, but abnormal compared to the seasonal pattern. Contextual attributes are introduced
    by replacing cosine entries with sine values.

    The target indicates whether or not the instances are anomalous.

    Parameters
    ----------
    n_samples
        The number of samples to generate. This generator creates a batch of data affected
        by contextual anomalies and noise.
    n_anomalies
        Number of anomalies. Can't be larger than `n_samples`.
    contextual
        If True, will add contextual anomalies.
    n_contextual
        Number of contextual anomalies. Can't be larger than `n_samples`.
    shift
        Shift in number of samples applied when retrieving contextual anomalies.
    noise
        Amount of noise.
    replace
        If True, anomalies are randomly sampled with replacement.
    seed
        Random seed for reproducibility.

    Examples
    --------

    >>> from river.datasets import synth

    >>> dataset = synth.AnomalySine(
    ...     seed=12345,
    ...     n_samples=100,
    ...     n_anomalies=25,
    ...     contextual=True,
    ...     n_contextual=10
    ... )

    >>> for x, y in dataset.take(5):
    ...     print(x, y)
    {'sine': -0.7119, 'cosine': 0.8777} False
    {'sine': 0.8792, 'cosine': -0.0290} False
    {'sine': 0.0440, 'cosine': 3.0852} True
    {'sine': 0.5520, 'cosine': 3.4515} True
    {'sine': 0.8037, 'cosine': 0.4027} False

    """

    def __init__(
        self,
        n_samples: int = 10000,
        n_anomalies: int = 2500,
        contextual: bool = False,
        n_contextual: int = 2500,
        shift: int = 4,
        noise: float = 0.5,
        replace: bool = True,
        seed: int | None = None,
    ):
        super().__init__(
            n_features=2,
            n_classes=1,
            n_outputs=1,
            n_samples=n_samples,
            task=datasets.base.BINARY_CLF,
        )
        if n_anomalies > self.n_samples:
            raise ValueError(
                f"n_anomalies ({n_anomalies}) can't be larger "
                f"than n_samples ({self.n_samples})."
            )
        self.n_anomalies = n_anomalies
        self.contextual = contextual
        if contextual and n_contextual > self.n_samples:
            raise ValueError(
                f"n_contextual ({n_contextual}) can't be larger "
                f"than n_samples ({self.n_samples})."
            )
        self.n_contextual = n_contextual
        self.shift = abs(shift)
        self.noise = noise
        self.replace = replace
        self.seed = seed

        # Stream attributes
        self.n_num_features = 2

    def _generate_data(self):
        # Generate anomaly data arrays
        self._rng = np.random.default_rng(self.seed)
        self.y = np.zeros(self.n_samples)
        self.X = np.column_stack(
            [
                np.sin(np.arange(self.n_samples) / 4.0)
                + self._rng.normal(size=self.n_samples) * self.noise,
                np.cos(np.arange(self.n_samples) / 4.0)
                + self._rng.normal(size=self.n_samples) * self.noise,
            ]
        )

        if self.contextual:
            # contextual anomaly indices
            contextual_anomalies = self._rng.choice(
                self.n_samples - self.shift, self.n_contextual, replace=self.replace
            )
            # set contextual anomalies
            contextual_idx = contextual_anomalies + self.shift
            contextual_idx[contextual_idx >= self.n_samples] -= self.n_samples
            self.X[contextual_idx, 1] = self.X[contextual_anomalies, 0]

        # Anomaly indices
        anomalies_idx = self._rng.choice(self.n_samples, self.n_anomalies, replace=self.replace)
        self.X[anomalies_idx, 1] = (
            np.sin(self._rng.choice(self.n_anomalies, replace=self.replace))
            + self._rng.normal(size=self.n_anomalies) * self.noise
            + 2.0
        )
        # Mark sample as anomalous
        self.y[anomalies_idx] = 1

    def __iter__(self):
        self._generate_data()

        for xi, yi in itertools.zip_longest(self.X, self.y if hasattr(self.y, "__iter__") else []):
            yield dict(zip(["sine", "cosine"], xi.tolist())), bool(yi)
