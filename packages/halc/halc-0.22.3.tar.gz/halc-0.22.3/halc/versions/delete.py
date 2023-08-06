from halc import get_client
from .get import VersionNotFound


class VersionDeletionFailed(Exception):
    pass


def delete_version(
    project_id: str,
    version_id: str,
) -> dict:
    """Delete a version
    :param project_id: Id of the project
    :param version_id: Id of the version
    :return: status of the operation
    """
    client = get_client()
    try:
        res = client.delete(f"/projects/versions/{project_id}/{version_id}")
        if res.status_code == 204:
            return VersionNotFound(f"version with id '{version_id}' not found")
        return {"status": "ok"}
    except Exception:
        raise VersionDeletionFailed(f"could not delete version with id '{version_id}'")
