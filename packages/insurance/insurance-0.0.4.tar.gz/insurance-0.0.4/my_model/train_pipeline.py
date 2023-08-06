import pandas as pd
from sklearn.model_selection import train_test_split
from config.core import config
from pipeline import pl_insurance
from processing.data_manager import load_dataset, save_pipeline

def run_training() -> None:
    """Train the model."""

    # read training data
    data = load_dataset(file_name=config.app_config.training_data_file)

    # divide train and test
    X_train, X_test, y_train, y_test = train_test_split(data[config.model_config.features],
                                                        data[config.model_config.target],
                                                        test_size=config.model_config.test_size,
                                                        random_state=config.model_config.random_state)

    #X_train = pd.DataFrame(X_train, columns=["Height", "Weight", "Age", "Country"])
    #X_test = pd.DataFrame(X_test, columns=["Height", "Weight", "Age", "Country"])
    #Y_train = pd.DataFrame(Y_train, columns=["Male"])
    #Y_test = pd.DataFrame(Y_test, columns=["Male"])

    # fit model

    # DataConversionWarning: A column-vector y was passed when a 1d array was expected.
    # Please change the shape of y to (n_samples, ), for example using ravel().
    # nombre pipe
    pl_insurance.fit(X_train, y_train)

    # save trained model
    save_pipeline(pipeline_to_persist=pl_insurance)


if __name__ == "__main__":
    run_training()