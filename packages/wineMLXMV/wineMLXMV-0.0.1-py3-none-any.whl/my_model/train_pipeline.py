import pandas as pd
from config.core import config

# nombre pipe en el archivo
from pipeline import LRwine
from processing.data_manager import load_dataset, save_pipeline
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)
    # divide train and test
    X_train, X_test, Y_train, Y_test = train_test_split(
        data[config.model_config.features],
        data[config.model_config.target],
        test_size=config.model_config.test_size,
        # we are setting the random seed here
        # for reproducibility
        random_state=config.model_config.random_state,
    )

    X_train = pd.DataFrame(
        X_train,
        columns=[
            "alcohol",
            "fixed acidity",
            "volatile acidity",
            "citric acid",
            "residual sugar",
            "chlorides",
            "free sulfur dioxide",
            "total sulfur dioxide",
            "density",
            "pH",
            "sulphates",
        ],
    )
    X_test = pd.DataFrame(
        X_test,
        columns=[
            "alcohol",
            "fixed acidity",
            "volatile acidity",
            "citric acid",
            "residual sugar",
            "chlorides",
            "free sulfur dioxide",
            "total sulfur dioxide",
            "density",
            "pH",
            "sulphates",
        ],
    )
    Y_train = pd.DataFrame(Y_train, columns=["quality"])
    Y_test = pd.DataFrame(Y_test, columns=["quality"])

    label_encoder = LabelEncoder()
    Y_train_encoded = label_encoder.fit_transform(Y_train.values.ravel())

    # fit model

    # DataConversionWarning: A column-vector y was passed when a 1d array was expected.
    # Please change the shape of y to (n_samples, ), for example using ravel().
    # nombre pipe
    LRwine.fit(X_train, Y_train_encoded)

    # persist trained model
    save_pipeline(pipeline_to_persist=LRwine)


if __name__ == "__main__":
    run_training()
