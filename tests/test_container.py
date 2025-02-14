# pylint: disable=missing-function-docstring,missing-module-docstring
from pathlib import Path

import pytest

from . import images
from pytest_container import Container
from pytest_container import DerivedContainer
from pytest_container.container import ImageFormat


def test_derived_container_fails_without_base() -> None:
    """Ensure that a DerivedContainer cannot be instantiated without providing
    the base parameter.

    """
    with pytest.raises(ValueError) as val_err_ctx:
        DerivedContainer()

    assert str(val_err_ctx.value) == "A base container must be provided"


def test_get_base_of_derived_container() -> None:
    """Ensure that :py:meth:`~pytest_container.DerivedContainer.get_base`
    returns a :py:class:`Container` with the correct url.

    """
    url = "registry.foobar.org/my_img:latest"
    assert DerivedContainer(base=url).get_base() == Container(url=url)


def test_image_format() -> None:
    """Check that the string representation of the ImageFormat enum is correct."""
    assert str(ImageFormat.DOCKER) == "docker"
    assert str(ImageFormat.OCIv1) == "oci"


def test_local_image_url() -> None:
    url = "docker.io/library/iDontExistHopefully/bazbarf/something"
    cont = Container(url=f"containers-storage:{url}")
    assert cont.local_image
    assert cont.url == url
    # prepare must not call `$runtime pull` as that would fail
    cont.prepare_container(Path("."), [])


def test_lockfile_path(pytestconfig: pytest.Config) -> None:
    """Check that the attribute
    :py:attr:`~pytest_container.ContainerBase.lockfile_filename` does change by
    the container having the attribute
    :py:attr:`~pytest_container.ContainerBase.container_id` set.

    """
    cont = DerivedContainer(base=images.OPENSUSE_BUSYBOX_URL, containerfile="")
    original_lock_fname = cont.filelock_filename

    cont.prepare_container(pytestconfig.rootpath)
    assert cont.container_id, "container_id must not be empty"
    assert cont.filelock_filename == original_lock_fname


def test_lockfile_unique() -> None:
    cont1 = DerivedContainer(
        base=images.OPENSUSE_BUSYBOX_URL, containerfile=""
    )
    cont2 = DerivedContainer(
        base=images.OPENSUSE_BUSYBOX_URL, containerfile="ENV foobar=1"
    )
    assert cont1.filelock_filename != cont2.filelock_filename
