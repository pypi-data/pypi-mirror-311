from collections import namedtuple
from typing import List
import numpy as np
from SAInT.data_normalizer import Normalizer

NormalizationMeanStdValues = namedtuple('NormalizationMeanStdValues', 'mean_values, std_values')

class MeanStdNormalizer(Normalizer):
    def __init__(self, normalization_values: NormalizationMeanStdValues = None,
                 features_to_normalize: List[str] = None, verbose: bool = False):
        super().__init__(normalization_values=normalization_values,
                 features_to_normalize=features_to_normalize, verbose=verbose)

    def _compute_normalization_values(self, dataframe):
        if self.features_to_normalize is None:
            numeric_columns = dataframe.select_dtypes(include=['number']).columns
        else:
            numeric_columns = self.features_to_normalize
        self.normalization_values = NormalizationMeanStdValues(
                mean_values=dataframe[numeric_columns].mean(skipna=True),
                std_values=dataframe[numeric_columns].std(skipna=True))

    def _perform_normalization(self, dataframe, selected_features):
        column_mean = self.normalization_values.mean_values
        column_std = self.normalization_values.std_values
        selected_column_mean = (column_mean[selected_features]).astype(float)
        selected_column_std = (column_std[selected_features]).astype(float)
        # Check if lengths of selected features, mean and std match
        if len(selected_features) != len(selected_column_mean) or len(selected_features) != len(selected_column_std):
            raise ValueError("Lengths of selected features, mean and std do not match.")
        # Create a temporary normalized dataframe to hold the results
        normalized_values = (
            (dataframe.loc[:, selected_features].astype(np.float64) - selected_column_mean) / selected_column_std
        )
        # Assign normalized values back, ensuring the columns are float64
        for feature in selected_features:
            dataframe[feature] = normalized_values[feature].astype(np.float64)
        return dataframe

    def _perform_denormalization(self, dataframe, selected_features):
        column_mean = self.normalization_values.mean_values
        column_std = self.normalization_values.std_values
        selected_column_mean = (column_mean[selected_features]).astype(float)
        selected_column_std = (column_std[selected_features]).astype(float)
        # Check if lengths of selected features, mean and std match
        if len(selected_features) != len(selected_column_mean) or len(selected_features) != len(selected_column_std):
            raise ValueError("Lengths of selected features, mean and std do not match.")
        denormalized_values = (
            ((dataframe.loc[:, selected_features].astype(np.float64) * selected_column_std) + selected_column_mean)
        )
        # Assign normalized values back, ensuring the columns are float64
        for feature in selected_features:
            dataframe[feature] = denormalized_values[feature].astype(np.float64)
        return dataframe
