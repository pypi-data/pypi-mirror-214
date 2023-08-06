from uuid import uuid4
from enum import IntEnum

from halc.initialize import get_client


class ProjectCreationFailed(Exception):
    pass


class ProjectType(IntEnum):
    BoundingBoxes = 1
    Segmentation = 2


def create_project(
    name: str,
    organization_id: str,
    type: ProjectType = ProjectType.Segmentation,
) -> dict:
    """Create a new project
    :param name: name of the project
    :param organization_id: Id of the organization
    :param type: type of the project
    :return: project spec
    """

    # Assert the name
    name = name.strip()
    if name == "":
        raise ProjectCreationFailed(f"name {name} is invalid")

    client = get_client()
    try:
        project = {
            "id": str(uuid4()),
            "name": name,
            "type": type,
            "organization_id": organization_id,
            "classes": [],
            "versions": [
                {
                    "id": str(uuid4()),
                    "name": "Ground Truth",
                    "is_mutable": True,
                    "hotkey": 1,
                }
            ],
        }
        res = client.post("/projects", project)
        project = res.json()
        return project
    except Exception as e:
        raise ProjectCreationFailed(
            f"could not create project with name '{name}' in organization with id '{organization_id}'"
        )
