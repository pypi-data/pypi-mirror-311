import logging
import tempfile
from pathlib import Path
from typing import Dict, List, Optional

from frogml_storage.frog_ml import FrogMLStorage

from frogml.utils.files_tools import _get_file_extension
from frogml.utils.storage import (
    _get_model_info_from_artifactory,
    _log_model_to_artifactory,
)
from frogml.utils.storge_helper import _get_model_framework
from frogml.utils.validataions import _validate_load_model, _validate_log_files_model

_logger = logging.getLogger(__name__)

_FILES_MODEL_FLAVOR = "files"


def log_model(
    source_path: str,
    repository: str,
    model_name: str,
    namespace: Optional[str] = None,
    version: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
    dependencies: Optional[List[str]] = None,
    code_dir: Optional[str] = None,
) -> None:
    """
    todo: Add doc example
    Log model to a repository in Artifactory.
    :param source_path: Path to the model to be logged`
    :param repository: Repository to log the model to
    :param model_name: Name of the model
    :param namespace: Namespace of the model
    :param version: Version of the model
    :param properties: Model properties
    :param dependencies: Model dependencies path
    :param code_dir: Model code directory path
    :return: None
    """

    _logger.info(f"Logging model {model_name} to {repository} in {namespace} namespace")

    _validate_log_files_model(
        source_path=source_path,
        repository=repository,
        model_name=model_name,
        namespace=namespace,
        version=version,
        properties=properties,
        dependencies=dependencies,
        code_dir=code_dir,
    )

    with tempfile.TemporaryDirectory() as target_dir:
        _log_model_to_artifactory(
            model_name=model_name,
            target_dir=target_dir,
            model_flavor=_FILES_MODEL_FLAVOR,
            model_version="",
            full_model_path=source_path,
            serialization_format=_get_file_extension(source_path),
            repository=repository,
            namespace=namespace,
            version=version,
            properties=properties,
            dependencies=dependencies,
            code_dir=code_dir,
        )


def load_model(
    repository: str,
    model_name: str,
    version: str,
    namespace: Optional[str] = None,
    target_path: Optional[str] = None,
) -> Path:
    """
    Load model from Artifactory.
    :param repository: Repository to load the model from
    :param namespace: Namespace of the model
    :param model_name: Name of the model
    :param version: Version of the model
    :param target_path: Path to save the model
    :return: Path to the model file
    """

    _logger.info(
        f"Loading model {model_name} from {repository} in {namespace} namespace"
    )

    model_info = get_model_info(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
    )
    model_framework = _get_model_framework(model_info)

    _validate_load_model(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
        model_framework=model_framework,
        model_flavor=_FILES_MODEL_FLAVOR,
    )

    target_path = target_path if target_path else tempfile.mkdtemp()

    FrogMLStorage().download_model_version(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
        target_path=target_path,
    )

    return Path(target_path)


def get_model_info(
    repository: str, model_name: str, version: str, namespace: Optional[str] = None
) -> Dict:
    """
    Get model information
    :param repository: Repository to get the model from
    :param namespace: Namespace of the model
    :param model_name: Requested model name
    :param version: Version of the model
    :return: Model information
    """

    _logger.info(
        f"Getting model {model_name} information from {repository} in {namespace} namespace"
    )
    return _get_model_info_from_artifactory(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
    )
