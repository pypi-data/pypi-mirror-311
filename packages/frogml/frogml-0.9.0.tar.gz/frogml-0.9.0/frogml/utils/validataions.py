import os
import re
from typing import Dict, List, Optional

from frogml.exceptions import FrogMlException


def _validate_existing_path(path: str) -> None:
    """
    validating if path is existing
    :param path:
    :return: None if validation pass successfully else rase error
    """

    if not os.path.exists(path):
        raise FrogMlException(f"Path {path} does not exist")


def _validate_string(s: str) -> None:
    """
    Validate if string is not empty
    :param s: string
    :return: None if validation pass successfully else raise error
    """
    if not s:
        raise FrogMlException("String is empty")


def _validate_model_name(name: str) -> None:
    """
    Validate if model name is not empty, if the model name is shorter than 60 characters and if the model name match the regex pattern: ^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*$ # noqa
    :param name: model name
    :return: None if validation pass successfully else raise error
    """
    _validate_string(name)
    pattern = r"^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*$"

    if not re.fullmatch(pattern, name):
        raise FrogMlException(
            """Invalid input: The string must follow these rules:
        1. Only letters (A-Z, a-z), numbers (0-9), underscores (_), and hyphens (-) are allowed.
        2. Dot-separated segments are allowed, but:
           - The string cannot start or end with a dot.
           - Consecutive dots (..) are not allowed.
            Please modify your input to meet these requirements."""
        )
    if len(name) > 60:
        raise FrogMlException("Model name should be shorter than 60 characters")


def _validate_properties(properties: Dict[str, str]) -> None:
    """
    Validate if properties is dictionary and if all keys and values are string
    :param properties: dictionary of properties
    :return: None if validation pass successfully else raise error
    """
    if not isinstance(properties, dict):
        raise ValueError("Properties should be dictionary")
    for key, value in properties.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise FrogMlException("Properties keys and values should be string")


def _validate_dependencies(dependencies: List[str]) -> None:
    """
    Validate if dependencies is list of strings
    :param dependencies: list of strings
    :return: None if validation pass successfully else raise error
    """
    if not isinstance(dependencies, list):
        raise ValueError("Dependencies should be list")
    for dependency in dependencies:
        if not isinstance(dependency, str):
            raise FrogMlException(
                "Dependencies should be list of files paths or list of explicit dependencies"
            )


def _validate_load_model(
    repository: str,
    namespace: str,
    model_name: str,
    version: str,
    model_framework: str,
    model_flavor: str,
) -> None:
    """
    Private method that validate user input
    :param repository: repository name
    :param namespace: namespace name
    :param model_name: the name of the model
    :param version: version of the model
    :param model_framework: model framework files/catbbost etc..
    :param model_flavor: model flavor files/catboost etc..
    :return: None if validation passed successfully
    """

    _validate_string(repository)
    _validate_string(namespace)
    _validate_string(model_name)
    _validate_string(version)
    if model_framework != model_flavor:
        raise FrogMlException(
            f"The Model: {model_name} in Repository: {repository} in Namespace: {namespace} - is not a {model_flavor} model"
        )


def _validate_log_files_model(
    source_path: str,
    repository: str,
    model_name: str,
    namespace: str,
    version: Optional[str],
    properties: Optional[Dict[str, str]],
    dependencies: Optional[List[str]],
    code_dir: Optional[str],
):
    """
    Private method that validate user input
    :param source_path: path to serialized model
    :param repository: repository name
    :param model_name: the name of the model
    :param namespace : namespace name
    :param version: version of the model
    :param properties: model properties
    :param dependencies: list of dependencies
    :param code_dir: directory path containing the code
    :return: None if validation passed successfully
    """

    _validate_existing_path(source_path)
    _validate_string(repository)
    _validate_string(model_name)
    _validate_string(namespace)
    if version:
        _validate_string(version)
    if code_dir:
        _validate_existing_path(code_dir)
    if properties:
        _validate_properties(properties)
    if dependencies:
        _validate_dependencies(dependencies)


def _validate_typed_log_model(
    repository: str,
    model_name: str,
    namespace: Optional[str],
    version: Optional[str],
    properties: Optional[Dict[str, str]],
    dependencies: Optional[List[str]],
    code_dir: Optional[str],
):

    _validate_string(repository)

    _validate_model_name(model_name)

    if namespace:
        _validate_string(namespace)

    if version:
        _validate_string(version)

    if properties:
        _validate_properties(properties)

    if dependencies:
        for dependency in dependencies:
            _validate_string(dependency)

    if code_dir:
        _validate_existing_path(code_dir)
