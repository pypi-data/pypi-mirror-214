import typing as t

import pandas as pd

from my_model import __version__ as _version
from my_model.config.core import config
from my_model.processing.data_manager import load_pipeline

pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
# nombre del pipe...se pone con _ , por ejemplo _genero_pipe
_wineLR = load_pipeline(file_name=pipeline_file_name)


def make_prediction(
    *,
    input_data: t.Union[pd.DataFrame, dict],
) -> dict:
    """Make a prediction using a saved model pipeline."""
    data = pd.DataFrame(input_data)
    results = {"predictions": None, "version": _version}

    predictions = _wineLR.predict(X=data[config.model_config.features])
    results = {
        "predictions": predictions,
        "version": _version,
    }

    return results
