from halc.initialize import get_client


class ImagesGetFailed(Exception):
    pass


def get_images(
    project_id: str,
) -> list[dict]:
    """Get project images
    :param project_id: Id of the project
    :return: list of the images spec in the project
    """
    client = get_client()
    try:
        res = client.get(f"/images/{project_id}")
        images = res.json()
        return images
    except:
        raise ImagesGetFailed(
            f"failed to get images from project with id '{project_id}'"
        )
