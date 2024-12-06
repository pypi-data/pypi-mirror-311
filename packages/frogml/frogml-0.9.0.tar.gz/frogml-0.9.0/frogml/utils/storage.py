import logging
from platform import python_version
from typing import Dict, Optional, List, Callable

from frogml_storage.frog_ml import SerializationMetadata, FrogMLStorage

from frogml.utils.dependencies_tools import _dependency_files_handler
from frogml.utils.files_tools import _zip_model
from frogml.utils.validataions import _validate_load_model

_STORAGE_MODEL_ENTITY_TYPE = "model"
_PYTHON_RUNTIME = "python"

_logger = logging.getLogger(__name__)


def _get_model_metadata(
    model_flavor: str,
    model_flavor_version: str,
    serialization_format: str,
) -> SerializationMetadata:
    return SerializationMetadata(
        framework=model_flavor,
        framework_version=model_flavor_version,
        serialization_format=serialization_format,
        runtime=_PYTHON_RUNTIME,
        runtime_version=python_version(),
    )


def _get_model_info_from_artifactory(
    repository: str,
    model_name: str,
    version: str,
    namespace: Optional[str] = None,
) -> Dict:
    return FrogMLStorage().get_entity_manifest(
        entity_type=_STORAGE_MODEL_ENTITY_TYPE,
        repository=repository,
        namespace=namespace,
        entity_name=model_name,
        version=version,
    )


def _download_model_version_from_artifactory(
    model_flavor: str,
    repository: str,
    model_name: str,
    version: str,
    model_framework: str,
    download_target_path: str,
    deserializer: Callable,
    namespace: Optional[str] = None,
):
    """
    Download model version from artifactory
    :param model_flavor: model flavor files/catbbost etc..
    :param repository: repository name
    :param namespace: namespace name
    :param model_name: the name of the model
    :param version: version of the model
    :param download_target_path: the path to download the model to
    :param model_framework: model framework files/catbbost etc..
    :return: Loaded model
    """
    _validate_load_model(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
        model_framework=model_framework,
        model_flavor=model_flavor,
    )

    FrogMLStorage().download_model_version(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
        target_path=download_target_path,
    )
    return deserializer()


def _log_model_to_artifactory(
    model_name: str,
    target_dir: str,
    model_flavor: str,
    model_version: str,
    full_model_path: str,
    serialization_format: str,
    repository: str,
    namespace: Optional[str] = None,
    version: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
    dependencies: Optional[List[str]] = None,
    code_dir: Optional[str] = None,
) -> None:
    dependencies = _dependency_files_handler(
        dependencies=dependencies, target_dir=target_dir
    )

    zipped_code_path = _zip_model(code_dir_path=code_dir, target_dir=target_dir)

    metadata = _get_model_metadata(
        model_flavor=model_flavor,
        model_flavor_version=model_version,
        serialization_format=serialization_format,
    )

    FrogMLStorage().upload_model_version(
        repository=repository,
        model_name=model_name,
        model_path=full_model_path,
        model_type=metadata,
        namespace=namespace,
        version=version,
        properties=properties,
        dependencies_files_paths=dependencies,
        code_archive_file_path=zipped_code_path,
    )
