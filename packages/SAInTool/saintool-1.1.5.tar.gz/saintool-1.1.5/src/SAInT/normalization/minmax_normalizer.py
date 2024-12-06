from collections import namedtuple
import numpy as np
from typing import List
from SAInT.data_normalizer import Normalizer

NormalizationMinMaxValues = namedtuple('NormalizationMinMaxValues', 'min_values, max_values')

class MinMaxNormalizer(Normalizer):
    def __init__(self, normalization_values: NormalizationMinMaxValues = None,
                 features_to_normalize: List[str] = None, verbose: bool = False):
        super().__init__(normalization_values=normalization_values,
                 features_to_normalize=features_to_normalize, verbose=verbose)

    def _compute_normalization_values(self, dataframe):
        if self.features_to_normalize is None:
            numeric_columns = dataframe.select_dtypes(include=['number']).columns
        else:
            numeric_columns = self.features_to_normalize
        self.normalization_values = NormalizationMinMaxValues(
                min_values=dataframe[numeric_columns].min(skipna=True),
                max_values=dataframe[numeric_columns].max(skipna=True))

    def _perform_normalization(self, dataframe, selected_features):
        column_min = self.normalization_values.min_values
        column_max = self.normalization_values.max_values
        selected_column_min = column_min[selected_features].astype(np.float64)
        selected_column_max = column_max[selected_features].astype(np.float64)
        # Check if lengths of selected features, min and max match
        if len(selected_features) != len(selected_column_min) or len(selected_features) != len(selected_column_max):
            raise ValueError("Lengths of selected features, min and max do not match.")
        # Create a temporary normalized dataframe to hold the results
        selected_column_diff = selected_column_max - selected_column_min
        normalized_values = (
            (dataframe.loc[:, selected_features].astype(np.float64) - selected_column_min) / selected_column_diff
        )
        # Assign normalized values back, ensuring the columns are float64
        for feature in selected_features:
            dataframe[feature] = normalized_values[feature].astype(np.float64)
        return dataframe

    def _perform_denormalization(self, dataframe, selected_features):
        column_min = self.normalization_values.min_values.astype(np.float64)
        column_max = self.normalization_values.max_values.astype(np.float64)
        selected_column_min = column_min[selected_features]
        selected_column_max = column_max[selected_features]
        # Check if lengths of selected features, min and max match
        if len(selected_features) != len(selected_column_min) or len(selected_features) != len(selected_column_max):
            raise ValueError("Lengths of selected features, min and max do not match.")
        # Create a temporary denormalized dataframe to hold the results
        selected_column_diff = selected_column_max - selected_column_min
        denormalized_values = (
            ((dataframe.loc[:, selected_features].astype(np.float64) * selected_column_diff) + selected_column_min)
        )
        # Assign normalized values back, ensuring the columns are float64
        for feature in selected_features:
            dataframe[feature] = denormalized_values[feature].astype(np.float64)
        return dataframe
