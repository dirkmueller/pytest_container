# pylint: disable=missing-function-docstring,missing-module-docstring
from pytest import Config

from .images import LEAP_URL
from pytest_container import DerivedContainer
from pytest_container.container import ContainerData


LEAP_WITH_CONFIG_FILE = DerivedContainer(
    base=LEAP_URL,
    containerfile="""WORKDIR /opt/app/
COPY pyproject.toml /opt/app/pyproject.toml""",
)

CONTAINER_IMAGES = [LEAP_WITH_CONFIG_FILE]


def test_config_file_present(
    auto_container: ContainerData, pytestconfig: Config
):
    assert auto_container.connection.file("/opt/app/pyproject.toml").exists
    with open(
        pytestconfig.rootpath / "pyproject.toml", encoding="utf-8"
    ) as pyproject:
        assert auto_container.connection.file(
            "/opt/app/pyproject.toml"
        ).content_string == pyproject.read(-1)
