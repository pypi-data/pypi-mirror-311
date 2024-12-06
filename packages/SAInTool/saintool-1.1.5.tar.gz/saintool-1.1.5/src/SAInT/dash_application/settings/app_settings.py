import os
import json
from collections import namedtuple
import numpy as np
from fastai.tabular.all import Categorify, FillMissing, Normalize

ApplicationSettings = namedtuple(
    'ApplicationSettings',
    'dtype, do_one_hot_encoding, valid_frac, test_frac, procs, \
        ds_for_model_selection, max_epochs, patience, perform_new_grid_search, \
        mlp_hidden_layers, mlp_dropout, \
        resnet_dropout, resnet_layersizes, resnet_blocks, \
        rf_max_depth, rf_n_estimators, rf_criterion, rf_min_samples_leaf, rf_min_samples_split, \
        xgb_max_depth, xgb_n_estimators, \
        svm_degree, \
        dt_criterion, dt_max_depth, dt_min_samples_leaf, dt_min_samples_split, dt_class_weight, \
        num_samples, num_top_features')

DEFAULT_VALUES = {
    "dtype": None,
    "do_one_hot_encoding": True,
    "valid_frac": 0.1,
    "test_frac": 0.2,
    "procs": None,
    "ds_for_model_selection": "valid",
    "max_epochs": 150,
    "patience": 30,
    "perform_new_grid_search": False,
    "mlp_hidden_layers": [[1024, 256, 256, 128, 128, 64, 64, 64, 32, 32, 32]],
    "mlp_dropout": [0.0],
    "resnet_dropout": [0.0],
    "resnet_layersizes": [128],
    "resnet_blocks": [3],
    "rf_max_depth": 6,
    "rf_n_estimators": 100,
    "rf_criterion": "default",
    "rf_min_samples_leaf": 10,
    "rf_min_samples_split": 15,
    "xgb_max_depth": 6,
    "xgb_n_estimators": 100,
    "svm_degree": 3,
    "dt_criterion": "default",
    "dt_max_depth": 8,
    "dt_min_samples_leaf": 10,
    "dt_min_samples_split": 15,
    "dt_class_weight": "balanced",
    "num_samples": 4096,
    "num_top_features": -1
}

def proc_str_to_proc(in_procs):
    if in_procs is None:
        return in_procs
    out_procs = []
    for proc_str in in_procs:
        if proc_str == "Categorify":
            proc = Categorify
        elif proc_str == "Normalize":
            proc = Normalize
        elif proc_str == "FillMissing":
            proc = FillMissing
        else:
            raise RuntimeError(
                f"Preprocessing Error: {proc_str} is unsupported!")
        out_procs.append(proc)
    return out_procs


def proc_to_proc_str(in_procs):
    if in_procs is None:
        return in_procs
    out_proc_strs = []
    for proc in in_procs:
        if proc == Categorify:
            proc_str = "Categorify"
        elif proc == Normalize:
            proc_str = "Normalize"
        elif proc == FillMissing:
            proc_str = "FillMissing"
        else:
            raise RuntimeError(
                f"Preprocessing Error: {proc} is unsupported!")
        out_proc_strs.append(proc_str)
    return out_proc_strs


def dtype_str_to_numpy(in_dtype: str):
    if in_dtype is None:
        return in_dtype
    if in_dtype == "float32":
        return np.float32
    if in_dtype == "float64":
        return np.float64
    if in_dtype == "float128":
        return np.float128
    raise RuntimeError(f"Preprocessing Error: {in_dtype} is unsupported!")


def numpy_to_dtype_str(numpy_input):
    if numpy_input is None:
        return numpy_input
    if numpy_input == np.float32:
        return "float32"
    if numpy_input == np.float64:
        return "float64"
    if numpy_input == np.float128:
        return "float128"
    raise RuntimeError(f"Preprocessing Error: {numpy_input} is unsupported!")


def json_to_app_settings(content):
    if isinstance(content, str):
        content = json.loads(content)
    # Process any specific field transformations
    content["procs"] = proc_str_to_proc(content["procs"]) if "procs" in content else DEFAULT_VALUES["procs"]
    content["dtype"] = dtype_str_to_numpy(content["dtype"]) if "dtype" in content else DEFAULT_VALUES["dtype"]
    # Add missing fields with default values
    for field in ApplicationSettings._fields:
        if field not in content:
            content[field] = DEFAULT_VALUES[field]
    settings = ApplicationSettings(**content)
    return settings


def load_app_settings_file(settings_file):
    if not os.path.exists(settings_file):
        print(f"{settings_file} does not exist! Define app_settings.json file!")
        return None
    with open(settings_file, "r") as file:
        content = json.load(file)
        return json_to_app_settings(content)


def save_app_settings_file(settings, settings_file):
    settings_file = settings_file
    with open(settings_file, "w") as file:
        settings_dict = settings._asdict()
        settings_dict["procs"] = proc_to_proc_str(settings_dict["procs"])
        settings_dict["dtype"] = numpy_to_dtype_str(settings_dict["dtype"])
        json.dump(settings_dict, file, indent=4)


def app_settings_to_json(settings):
    settings_dict = settings._asdict()
    settings_dict["procs"] = proc_to_proc_str(settings_dict["procs"])
    settings_dict["dtype"] = numpy_to_dtype_str(settings_dict["dtype"])
    return json.dumps(settings_dict, indent=4)
