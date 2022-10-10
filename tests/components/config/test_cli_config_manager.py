# QUANTCONNECT.COM - Democratizing Finance, Empowering Individuals.
# Lean CLI v1.0. Copyright 2021 QuantConnect Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tempfile
from pathlib import Path

import pytest

from lean.components.config.cli_config_manager import CLIConfigManager
from lean.components.config.storage import Storage
from lean.constants import DEFAULT_ENGINE_IMAGE, DEFAULT_RESEARCH_IMAGE, DEFAULT_ENGINE_IMAGE_BASE_NAME, \
    DEFAULT_RESEARCH_IMAGE_BASE_NAME, DEFAULT_IMAGE_VERSION
from lean.models.docker import DockerImage


def create_storage() -> Storage:
    return Storage(str(Path(tempfile.mkdtemp()) / "storage"))


def test_get_option_by_key_returns_option_with_matching_key() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    for key in ["user-id", "api-token", "default-language"]:
        assert cli_config_manager.get_option_by_key(key).key == key


def test_get_option_by_key_raises_error_when_no_option_with_matching_key_exists() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    with pytest.raises(Exception):
        cli_config_manager.get_option_by_key("this-option-does-not-exist")


def test_get_engine_image_returns_default_image_when_nothing_is_passed() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    assert cli_config_manager.get_engine_image() == DockerImage.parse(DEFAULT_ENGINE_IMAGE)


def test_get_engine_image_returns_image_from_passed_name() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    assert cli_config_manager.get_engine_image("custom/engine:3") == DockerImage(name="custom/engine", tag="3")


def test_get_research_image_returns_default_image_when_nothing_is_passed() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    assert cli_config_manager.get_research_image() == DockerImage.parse(DEFAULT_RESEARCH_IMAGE)


def test_get_research_image_returns_image_from_passed_name() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    assert cli_config_manager.get_research_image("custom/research:3") == DockerImage(name="custom/research", tag="3")


def test_get_engine_image_name_with_custom_tag() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    expected_image_name = f"{DEFAULT_ENGINE_IMAGE_BASE_NAME}:3.5.1"
    assert cli_config_manager.get_engine_image_name_from_version("3.5.1") == expected_image_name


def test_get_engine_image_name_with_default_tag() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    expected_image_name = f"{DEFAULT_ENGINE_IMAGE_BASE_NAME}:{DEFAULT_IMAGE_VERSION}"
    assert cli_config_manager.get_engine_image_name_from_version() == expected_image_name


def test_get_research_image_name_with_custom_tag() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    expected_image_name = f"{DEFAULT_RESEARCH_IMAGE_BASE_NAME}:3.5.1"
    assert cli_config_manager.get_research_image_name_from_version("3.5.1") == expected_image_name


def test_get_research_image_name_with_default_tag() -> None:
    cli_config_manager = CLIConfigManager(create_storage(), create_storage())

    expected_image_name = f"{DEFAULT_RESEARCH_IMAGE_BASE_NAME}:{DEFAULT_IMAGE_VERSION}"
    assert cli_config_manager.get_research_image_name_from_version() == expected_image_name

