"""Define helper functions for model evaluation and artifact management"""
import sys

import dill

from exception import CustomException


def load_object(file_path: str):
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)

    except Exception as e:
        raise CustomException(e, sys)