import typing as t
import pandas as pd
from my_model import __version__ as _version
from my_model.config.core import config
from my_model.processing.data_manager import load_pipeline
from my_model.processing.validation import validate_inputs

# cargar el pipeline previamente entrenado
pipeline_file_name = f"{config.app_config.pipeline_save_file}{_version}.pkl"
# nombre del pipe...se pone con _ , por ejemplo _pl_insurance
_pl_insurance = load_pipeline(file_name=pipeline_file_name)


def make_prediction(*, input_data: t.Union[pd.DataFrame, dict]) -> dict:
    """Make a prediction using a saved model pipeline."""

    # cargar datos
    data = pd.DataFrame(input_data)
    # comprobar que la estructura de los datos es correcta
    validated_data, errors = validate_inputs(input_data=data)
    results = {"predictions": None,
               "version": _version,
               "errors": errors}
    if not errors:
        # si los datos son correctos, predecir
        predictions = _pl_insurance.predict(X=validated_data[config.model_config.features])
        results = {"predictions": predictions,
                   "version": _version,
                   "errors": errors}

    return results
