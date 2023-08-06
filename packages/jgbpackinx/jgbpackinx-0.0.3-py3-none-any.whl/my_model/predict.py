import typing as t

import pandas as pd

from my_model import __version__ as _version
from my_model.config.core import config
from my_model.processing.data_manager import load_pipeline
from my_model.processing.validation import validate_inputs




def load_dataset(*, file_name: str) -> pd.DataFrame:
    return pd.read_csv(Path(f"{DATASET_DIR}/{file_name}"))



pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
_calidad_pipe = load_pipeline(file_name=pipeline_file_name)

data = load_dataset(file_name=config.app_config.test_data_file)

x_data = pd.DataFrame(data, columns=['alcohol', 'fixed acidity', 'volatile acidity', 'citric acid', 'residual sugar', 'chlorides', 'free sulfur dioxide', 'total sulfur dioxide', 'density', 'pH', 'sulphates'])

def make_prediction(
    input_data: pd.DataFrame,
):
    """Make a prediction using a saved model pipeline."""
    data = pd.DataFrame(input_data)
    return _calidad_pipe.predict(data)

print("hola")
#'make_prediction(x_data)




