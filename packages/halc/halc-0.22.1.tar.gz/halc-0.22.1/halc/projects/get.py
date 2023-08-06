from halc.initialize import get_client


class ProjectNotFound(Exception):
    pass


def get_project(
    project_id: str,
) -> dict:
    """Get project spect from id
    :param project_id: Id of the project
    :return: project spec
    """
    client = get_client()
    try:
        res = client.get(f"/projects/by_id/{project_id}")
        project = res.json()
        return project
    except Exception as e:
        print(e)
        raise ProjectNotFound(f"Project with id '{project_id}' not found")
