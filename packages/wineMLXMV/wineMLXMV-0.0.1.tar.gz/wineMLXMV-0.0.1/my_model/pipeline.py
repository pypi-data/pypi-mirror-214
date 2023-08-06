# PONER TODOS LOS IMPORTS AQUÍ:
from feature_engine.selection import DropFeatures
from feature_engine.wrappers import SklearnTransformerWrapper
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from my_model.config.core import config

numeric_transformer = StandardScaler()
preprocessor_num = SklearnTransformerWrapper(
    transformer=numeric_transformer, variables=config.model_config.num_features
)

LRwine = Pipeline(
    [
        (
            "preproc",
            preprocessor_num,
        ),
        (
            "drop_features",
            DropFeatures(features_to_drop=config.model_config.drop_features),
        ),
        ("LogisticR", LogisticRegression()),
    ]
)
