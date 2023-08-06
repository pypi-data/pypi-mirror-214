import numpy as np
import pandas as pd
import joblib
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from my_model.config.core import config

# preprocesador de las variables numéricas: reescalado de las variables
numeric_transformer = Pipeline(steps=[('scaler', StandardScaler())])

# preprocesador de las variables categóricas: one hot encoder
categorical_transformer = Pipeline(steps=[('encoder', OneHotEncoder(handle_unknown='ignore'))])

# unir ambos preprocesos en un solo transformador
preprocessor = ColumnTransformer(transformers=[('numeric', numeric_transformer, config.model_config.numerical_features),
                                               ('categorical', categorical_transformer, config.model_config.categorical_features)])

# definir el pipeline del modelo: preproceso + regresor
pl_insurance = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', SGDRegressor(max_iter=1000, penalty='elasticnet', tol=1e-3, random_state=config.model_config.random_state))])