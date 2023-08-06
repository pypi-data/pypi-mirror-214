import numpy as np
from sklearn.preprocessing import StandardScaler
import mne
import pandas as pd
from sklearn.decomposition import PCA

def reject_bad_channels(raw, signal1, signal2):
    """
    Reject bad channels from the raw data.

    Parameters:
        raw (object): Raw data object.
        signal1 (array-like): Signal 1 data.
        signal2 (array-like): Signal 2 data.

    Returns:
        object: Cleaned raw data object.
    """
    bad_channels = ['E127', 'E128']  # Specify the channels to exclude
    raw.info['bads'] = bad_channels
    clean_raw = raw.copy().drop_channels(bad_channels)
    return clean_raw


def reject_artifacts(epochs):
    """
    Reject epochs containing artifacts.

    Parameters:
        epochs (ndarray): Epochs data of shape (n_epochs, n_channels, n_samples).

    Returns:
        ndarray: Artifact-free epochs data.
    """
    artifact_threshold = 50  # Arbitrary threshold for artifact detection
    artifact_free_epochs = epochs[np.max(np.abs(epochs), axis=1) < artifact_threshold]
    return artifact_free_epochs


def signal_averaging(data):
    """
    Perform signal averaging to remove random noise or artifacts.
    """
    averaged_signal = np.mean(data, axis=0)
    return averaged_signal



def artifact_subspace_reconstruction(data, artifact_components):
    """
    Perform artifact subspace reconstruction to remove artifacts modeled as a subspace.
    """
    artifact_components = StandardScaler().fit_transform(artifact_components)
    data_projected = data - np.dot(np.dot(data, artifact_components.T), artifact_components)
    return data_projected


def regression_based_removal(data, regressor, artifacts):
    """
    Apply regression-based artifact removal by modeling artifacts as a function of other variables.
    """
    predicted_artifacts = regressor.predict(data)
    cleaned_data = data - predicted_artifacts.reshape(-1, 1)
    return cleaned_data

def template_subtraction(data, template):
    """
    Perform template subtraction to remove artifacts with a consistent shape or waveform.
    """
    cleaned_data = data - template
    return cleaned_data

def remove_artifacts(raw):
    ica = mne.preprocessing.ICA(n_components=30, random_state=42)
    ica.fit(raw)
    cleaned_raw = raw.copy()
    ica.apply(cleaned_raw)
    return cleaned_raw

# Access the loading vectors indicating the contribution of each original feature to each principal component
# import pandas as pd

# # Assuming your preprocessed data is stored in the 'pre_preprocessed_data' dataframe

# # Extract the numerical data from the dataframe
# data = pre_preprocessed_data.values

# # Define the number of components to retain
# num_components = len(data)

# # Perform PCA dimension reduction
# reduced_data, pca = perform_pca(data, 128)

# # Access the column names representing each principal component
# component_names = reduced_data.columns

# # Print the component names
# print(component_names)

# # Access the reduced data as a dataframe
# print(reduced_data)

# loading_vectors = pca.components_

# # Map the loading vectors to the original feature names
# original_feature_names = pre_preprocessed_data.columns
# feature_loading_map = {
#     component_names[i]: {original_feature_names[j]: loading_vectors[i, j] for j in range(len(original_feature_names))}
#     for i in range(num_components)
# }

# # Print the loading vectors associated with each component
# for component_name, feature_loadings in feature_loading_map.items():
#     print(f"Component: {component_name}")
#     for feature, loading in feature_loadings.items():
#         print(f"{feature}: {loading}")
#     print()