# -*- coding: utf-8 -*-

""" Validators associated with Mosaic-AI-Client """
from .constants import DeployFeasibility
# from .utils import get_deployment_data
import pickle
import json
import joblib
from pypmml import Model
import pandas as pd
import importlib
import os
import subprocess


def check_if_model_is_alredy_deployed(model_data, version_id, strategy="default"):
    """
    Validates if version is already deployed
    :param data:

    """
    for item in model_data["versions"]:
        if item.get("id") == version_id:
            if len(item.get("deployments")) != 0:
                if strategy == "promote":
                    for data in item.get("deployments"):
                        if (
                                data.get("deployment_info").get("deployment_type")
                                != "Default"
                        ):
                            return
                raise Exception(
                    "Version already deployed. Kindly stop that version deployment or try with another version !"
                )


def check_deployment_feasibility(model_data):
    count = 0
    deployments = list()
    for item in model_data["versions"]:
        if len(item.get("deployments")) != 0:
            for data in item.get("deployments"):
                deployments.append(
                    {
                        "deployment_id": data.get("id"),
                        "version_id": data.get("id"),
                        "deployment_type": data.get("deployment_info").get(
                            "deployment_type"
                        ),
                        "cpu_utilization": data.get("deployment_info").get(
                            "cpu_utilization"
                        ),
                        "resource_id": data.get("resource_id"),
                    }
                )
            count = count + 1
    if count == 0:
        return deployments, DeployFeasibility.default
    if count == 1:
        return deployments, DeployFeasibility.apply_strategy
    if count == 2:
        return deployments, DeployFeasibility.no_deploy


def fetch_promotion_key(deployment_type):
    if deployment_type == "AB-Testing":
        return "Confirm-AB"
    if deployment_type == "Canary":
        return "Confirm-Canary"
    if deployment_type == "PreProd":
        return "Confirm-PreProd"


# def validate_details_for_deployment(model_data, version_id, strategy="default"):
#     if bool(model_data):
#         # Check if Model Version is already deployed
#         check_if_model_is_alredy_deployed(model_data, version_id, strategy)

#         # Check Deployment Feasibility
#         deployments, deployment_feasibility = check_deployment_feasibility(model_data)
#         if strategy == "apply_strategy":
#             # Block to be executed with proper exceptions in case of Applying Strategy
#             if deployment_feasibility == DeployFeasibility.apply_strategy:
#                 deployment_data = get_deployment_data(deployments)
#                 return deployment_data
#             if deployment_feasibility == DeployFeasibility.default:
#                 raise Exception(
#                     "Strategy cannot be applied to this model as there is no Model Version currently in production"
#                 )
#             if deployment_feasibility == DeployFeasibility.no_deploy:
#                 raise Exception(
#                     "Strategy cannot be applied to this model as there are already versions in Production and in Strategy."
#                 )
#         if strategy == "default":
#             # Block to be executed with proper exceptions in case of Default Deployment
#             if deployment_feasibility == DeployFeasibility.default:
#                 return "Default"
#             if deployment_feasibility == DeployFeasibility.no_deploy:
#                 raise Exception(
#                     "Strategy cannot be applied to this model as there are already versions in Production and in Strategy."
#                 )
#             if deployment_feasibility == DeployFeasibility.apply_strategy:
#                 raise Exception(
#                     "A version is already in Production, kindly try applying a strategy or stop the existing Version and try again"
#                 )
#         if strategy == "promote":
#             # Block to be executed with proper exceptions in case of Promoting Models
#             if deployment_feasibility == DeployFeasibility.default:
#                 raise Exception("Unable to promote as no models have been deployed.")
#             if deployment_feasibility == DeployFeasibility.apply_strategy:
#                 raise Exception(
#                     "A version in Production, kindly try applying a strategy and then try promoting the version !"
#                 )
#             if deployment_feasibility == DeployFeasibility.no_deploy:
#                 deployment_data = get_deployment_data(deployments)
#                 promotion_key = fetch_promotion_key(
#                     deployment_data.get("deployment_type")
#                 )
#                 deployment_data.update({"promotion_key": promotion_key})
#                 return deployment_data

#     raise Exception(
#         "The Model ID provided is invalid. Kindly provide a valid Model ID !"
#     )


def stop_model_validations(model_data, version_id):
    if bool(model_data):
        for item in model_data["versions"]:
            if item.get("id") == version_id:
                if len(item.get("deployments")) != 0:
                    for data in item.get("deployments"):
                        deployment_id = data.get("id")
                        return deployment_id
                raise Exception("No deployment found for the specified Version ID.")
        raise Exception(
            "Kindly provide valid Version ID for the deployed models to stop !"
        )
    raise Exception(
        "The Model ID provided is invalid. Kindly provide a valid Model ID !"
    )


def validate_model_id_version_id(model_data, version_id):
    if not bool(model_data):
        raise Exception("The Model ID provided is invalid. Kindly provide a valid Model ID !")
    for item in model_data.get("versions"):
        if item.get("id") == version_id:
            return
    raise Exception("The Version ID provided is invalid. Kindly provide a valid Version ID !")

class BYOMValidations:
    @staticmethod
    def load_validate_model(file_path, flavour, conda_packages_list=None):
        if conda_packages_list:
            BYOMValidations.install_conda_packages(conda_packages_list)
        if file_path.endswith('.pkl'):
            with open(file_path, 'rb') as file:
                model = pickle.load(file)
        elif file_path.endswith('.json'):
            with open(file_path, 'r') as file:
                model = json.load(file)
        elif file_path.endswith('.joblib'):
            model = joblib.load(file_path)
        elif file_path.endswith('.pmml'):
            model = Model.load(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_path}")
        if flavour.lower() not in str(type(model)).lower():
            raise ValueError(f"Model validation failed, loaded model is not {flavour} model: {file_path}")
        return model


    @staticmethod
    def validate_score_format(function):
        # Validation: Check function name
        if function.__name__ != 'score_func':
            return False, f"Function name should be 'score_func', found '{function.__name__}'."

        # Extract arguments
        args = function.__code__.co_varnames
        print(args)
        num_args = function.__code__.co_argcount
        print(num_args)
        num_defaults = len(function.__defaults__) if function.__defaults__ else 0
        print(num_defaults)

        # Ensure there are at least two positional arguments
        if num_args < 2:
            return False, "Function should have at least two positional arguments."

        # Ensure the first two arguments are positional (without default values)
        if num_args - num_defaults != 2:
            return False, "The first two arguments should be positional (without default values)."
        return True, "Function format is valid."


    @staticmethod
    def load_validate_score_function(file_path, conda_packages_list=None):
        if conda_packages_list:
            BYOMValidations.install_conda_packages(conda_packages_list)

        module_name = os.path.splitext(os.path.basename(file_path))[0]
        spec = importlib.util.spec_from_file_location(module_name, file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        functions = [getattr(module, attr) for attr in dir(module) if callable(getattr(module, attr))]
        if len(functions) != 1:
            return False, "The file must contain exactly one function."
        function = functions[0]
        # Validate the function format
        is_valid, message = BYOMValidations.validate_score_format(function)
        return is_valid, message, function


    @staticmethod
    def extract_features(model):
        features = {
            'input_features': None,
            'output_features': None,
            'reference_features': None
        }   
        # Check for scikit-learn models
        if hasattr(model, 'feature_names_in_'):
            features['input_features'] = model.feature_names_in_
        elif hasattr(model, 'get_booster'):
            # Check for XGBoost models
            booster = model.get_booster()
            features['input_features'] = booster.feature_names
        elif hasattr(model, 'feature_name'):
            # Check for LightGBM models
            features['input_features'] = model.feature_name()
        elif hasattr(model, 'input_features'):
            # Check for Snowflake models
            features['input_features'] = model.input_features
            features['output_features'] = model.output_features
            features['reference_features'] = model.reference_features
        elif hasattr(model, 'exog_names'):
            # Check for statsmodels
            features['input_features'] = model.exog_names
        elif hasattr(model, 'train_holiday_names'):
            # Check for Prophet models
            features['input_features'] = model.train_holiday_names
        elif hasattr(model, 'model_'):
            # Check for pmdarima models
            features['input_features'] = model.model_.exog_names
        else:
            raise ValueError("Unsupported model type or model does not have feature information.")
        return features


    @staticmethod
    def install_conda_packages(packages):
        for package in packages:
            subprocess.run(['pip', 'install', '-q', package], check=True)


def validate_byom_dataset(df):
    if not isinstance(df, pd.DataFrame):
        raise ValueError("Input data should be a pandas DataFrame.")
    if df.empty or df.iloc[0].isnull().any():
        raise ValueError("Input data should not be empty and the first row should not contain null values.")
    