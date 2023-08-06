from halc.initialize import get_client


class ProjectNotFound(Exception):
    pass


class ProjectsListFailed(Exception):
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
    except Exception:
        raise ProjectNotFound(f"project with id '{project_id}' not found")


def list_projects(
    organization_id: str,
) -> list:
    """List projects in organization
    :param organization_id: Id of the organization
    :return: list of project specs
    """
    client = get_client()
    try:
        res = client.get(f"/projects/{organization_id}")
        project = res.json()
        return project
    except Exception:
        raise ProjectsListFailed(
            f"failed to list projects in organization with id '{organization_id}'"
        )
