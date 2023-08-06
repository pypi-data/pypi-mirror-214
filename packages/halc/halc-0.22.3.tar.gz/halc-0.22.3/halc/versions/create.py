from uuid import uuid4

from halc.initialize import get_client
from halc.projects import get_project


class VersionCreationFailed(Exception):
    pass


def create_version(
    project_id: str,
    name: str,
) -> dict:
    """Create a new version
    :param project_id: Id of the project
    :param name: name of the version
    :return: version spec
    """

    # Assert the name
    name = name.strip()
    if name == "":
        raise VersionCreationFailed(f"name {name} is invalid")

    # Get project
    client = get_client()
    project = get_project(project_id)

    try:
        # Define hotkey
        hotkey = len(project["versions"]) + 1 if len(project["versions"]) < 10 else None
        if hotkey and hotkey >= 10:
            hotkey = 0

        version = {
            "id": str(uuid4()),
        	"name": name,
        	"hotkey": hotkey,
        	"is_mutable": False,
        }
        res = client.post(f"/projects/versions/{project['id']}", version)
        version = res.json()
        return version
    except Exception:
        raise VersionCreationFailed(
            f"could not create version with name '{name}' in project with id '{project_id}'"
        )
