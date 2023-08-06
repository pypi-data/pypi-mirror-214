from halc import get_client
from halc.projects import get_project


class VersionNotFound(Exception):
    pass


class VersionsListFailed(Exception):
    pass


def get_version_by_id(
    project_id: str,
    version_id: str,
) -> dict:
    """Get version from the id
    :param project_id: Id of the project
    :param version_id: Id of the version
    :return: spec of the version
    """
    # Assert the project
    get_project(project_id)

    # Get the client
    client = get_client()

    # Get the version
    try:
        res = client.get(f"/projects/versions/{project_id}/{version_id}")
        version = res.json()
        return version
    except:
        raise VersionNotFound(f"version with id '{version_id}' not found")


def get_version_by_name(
    project_id: str,
    version_name: str,
) -> dict:
    """Get version from the name
    :param project_id: Id of the project
    :param version_name: Name of the version
    :return: spec of the version
    """
    # Assert the project
    get_project(project_id)

    # Get the client
    client = get_client()

    # Get the version
    try:
        res = client.get(f"/projects/versions/by_name/{project_id}/{version_name}")
        version = res.json()
        return version
    except:
        raise VersionNotFound(f"version with name '{version_name}' not found")


def list_versions(
    project_id: str,
) -> list:
    """List versions in project
    :param project_id: Id of the project
    :return: list of versions specs
    """
    # Get project
    project = get_project(project_id)
    return project["versions"]
