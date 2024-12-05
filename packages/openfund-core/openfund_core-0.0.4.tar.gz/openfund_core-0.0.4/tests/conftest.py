from pathlib import Path
from typing import List

import pytest
from cleo.testers.application_tester import ApplicationTester
from poetry.core.packages.dependency_group import DependencyGroup
from poetry.core.packages.package import Package
from openfund.core.factory import Factory
from poetry.poetry import Poetry
from poetry.pyproject.toml import PyProjectTOML
from pytest import TempPathFactory
from tomlkit.toml_document import TOMLDocument


@pytest.fixture(scope="function")
def openfund(project_path: Path) -> Path:
    return Factory().create_openfund(project_path)


@pytest.fixture(scope="function")
def project_path() -> Path:
    return Path(__file__).parent / "fixtures" / "simple_project"


@pytest.fixture(scope="function")
def pyproject_content(project_path: Path) -> TOMLDocument:
    path = project_path / "pyproject.toml"
    return PyProjectTOML(path).file.read()


@pytest.fixture(scope="function")
def expected_pyproject_content(project_path: Path) -> TOMLDocument:
    path = project_path / "expected_pyproject.toml"
    return PyProjectTOML(path).file.read()


@pytest.fixture(scope="function")
def tmp_pyproject_path(
    tmp_path_factory: TempPathFactory,
    pyproject_content: TOMLDocument,
) -> Path:
    tmp_pyproject_path = tmp_path_factory.mktemp("simple_project") / "pyproject.toml"
    tmp_pyproject_path.write_text(pyproject_content.as_string())
    return tmp_pyproject_path


@pytest.fixture
def poetry(project_path: Path) -> Poetry:
    return Factory().create_poetry(project_path)


@pytest.fixture
def groups(poetry: Poetry) -> List[DependencyGroup]:
    return poetry.package._dependency_groups.values()


@pytest.fixture
def packages() -> List[Package]:
    return [
        Package(name="foo", version="2.2.2"),
        Package(name="bar", version="2.2.2"),
        Package(name="baz", version="2.2.2"),
        Package(name="corge", version="2.2.2"),
        Package(name="grault", version="2.2.2"),
        Package(name="garply", version="2.2.2"),
        Package(name="waldo", version="2.2.2"),
        Package(name="fred", version="2.2.2"),
        Package(name="plugh", version="2.2.2"),
        Package(name="xyzzy", version="2.2.2"),
        Package(name="nacho", version="2.2.2"),
        Package(name="thud", version="2.2.2"),
        Package(name="foobar", version="2.2.2"),
        Package(name="foobaz", version="2.2.2"),
        Package(name="fooqux", version="2.2.2"),
        Package(name="fooquux", version="2.2.2"),
        Package(name="foo-corge", version="2.2.2"),
    ]
