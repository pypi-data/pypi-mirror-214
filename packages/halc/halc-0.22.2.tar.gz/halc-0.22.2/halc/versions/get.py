from halc import get_client
from halc.projects import get_project


class VersionNotFound(Exception):
    pass


def get_version(
    project_id: str,
    version_id: str,
) -> dict:
    """Get version spec from the id
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
        raise VersionNotFound(f"Version with id '{version_id}' not found")


def get_ground_truth_version(
    project_id: str,
) -> dict:
    """Get ground truth version spec for the given project
    :param project_id: Id of the project
    :return: spec of the version
    """
    return get_version(project_id, "gt")
