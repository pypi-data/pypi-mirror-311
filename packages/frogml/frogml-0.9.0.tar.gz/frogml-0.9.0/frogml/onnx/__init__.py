import logging
import os.path
import tempfile
from functools import partial
from typing import Dict, List, Optional

from frogml.exceptions import FrogMlException
from frogml.utils.files_tools import _get_full_model_path
from frogml.utils.storage import (
    _log_model_to_artifactory,
    _get_model_info_from_artifactory,
    _download_model_version_from_artifactory,
)
from frogml.utils.storge_helper import (
    _get_model_framework,
    _get_model_serialization_format,
    _get_model_framework_version,
)
from frogml.utils.validataions import _validate_load_model, _validate_typed_log_model

_logger = logging.getLogger(__name__)
_DEFAULT_ONNX_SERIALIZED_TYPE = "onnx"
_ONNX_MODEL_FLAVOR = "onnx"


def log_model(
    model,
    model_name: str,
    repository: str,
    namespace: Optional[str] = None,
    version: Optional[str] = None,
    properties: Optional[Dict[str, str]] = None,
    dependencies: Optional[List[str]] = None,
    code_dir: Optional[str] = None,
) -> None:
    _logger.info(f"Logging model {model_name} to {repository} in {namespace} namespace")

    _validate_typed_log_model(
        repository=repository,
        model_name=model_name,
        namespace=namespace,
        version=version,
        properties=properties,
        dependencies=dependencies,
        code_dir=code_dir,
    )

    with tempfile.TemporaryDirectory() as target_dir:
        full_model_path = _get_full_model_path(
            target_dir=target_dir,
            model_name=model_name,
            serialized_type=_DEFAULT_ONNX_SERIALIZED_TYPE,
        )
        try:
            import onnx

            model_version = onnx.__version__
            onnx.save_model(model, full_model_path)
        except Exception as e:
            raise FrogMlException(f"Failed to save model: {e}")

        _log_model_to_artifactory(
            model_name=model_name,
            target_dir=target_dir,
            model_flavor=_ONNX_MODEL_FLAVOR,
            model_version=model_version,
            full_model_path=full_model_path,
            serialization_format=_DEFAULT_ONNX_SERIALIZED_TYPE,
            repository=repository,
            namespace=namespace,
            version=version,
            properties=properties,
            dependencies=dependencies,
            code_dir=code_dir,
        )


def get_model_info(
    repository: str, model_name: str, version: str, namespace: Optional[str] = None
) -> Dict:
    """
    Get model information
    :param repository:
    :param namespace:
    :param model_name:
    :param version:
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


def load_model(
    repository: str,
    model_name: str,
    version: str,
    namespace: Optional[str] = None,
):
    """
    Load model from Artifactory.
    :param repository: Repository to load the model from
    :param model_name: Name of the model
    :param version: Version of the model
    :param namespace: Namespace of the model
    :return: loaded model
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
    serialization_format = _get_model_serialization_format(model_info)
    framework_runtime_version = _get_model_framework_version(model_info)

    _validate_load_model(
        repository=repository,
        namespace=namespace,
        model_name=model_name,
        version=version,
        model_framework=model_framework,
        model_flavor=_ONNX_MODEL_FLAVOR,
    )

    with tempfile.TemporaryDirectory() as download_target_path:
        full_model_path = os.path.join(
            download_target_path, f"{model_name}.{serialization_format}"
        )

        def deserializer_model(model_path):
            import onnx

            model = onnx.load(model_path)
            onnx.checker.check_model(model)
            return model

        try:
            return _download_model_version_from_artifactory(
                model_flavor=_ONNX_MODEL_FLAVOR,
                repository=repository,
                namespace=namespace,
                model_name=model_name,
                version=version,
                model_framework=model_framework,
                download_target_path=download_target_path,
                deserializer=partial(deserializer_model, full_model_path),
            )
        except Exception as e:
            logging.error(
                f"Failed to load Model. Model was serialized with onnx version: {framework_runtime_version}"
            )
            raise FrogMlException(f"Failed to deserialized model: {e}")
