from uuid import uuid4
from enum import IntEnum

from halc.initialize import get_client


class ProjectDeletionFailed(Exception):
    pass


def delete_project(
    project_id: str,
) -> dict:
    """Delete a project project
    :param project_id: Id of the project
    :return: status of the operation
    """

    client = get_client()
    try:
        client.delete(f"/projects/{project_id}")
        return {"status": "ok"}
    except Exception:
        raise ProjectDeletionFailed(f"could not delete project with id '{project_id}'")
