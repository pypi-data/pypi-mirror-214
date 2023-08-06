import json
from uuid import uuid4
from pathlib import Path
import math

from halc import get_client
from halc.utils import get_random_color, clip_bbox, compressed_rle_to_list
from halc.projects import get_project
from halc.images import get_images


class PathNotFound(Exception):
    pass


class CategoriesNotFound(Exception):
    pass


class ImagesNotFound(Exception):
    pass


class AnnotationsNotFound(Exception):
    pass


class NoAnnotationToUpload(Exception):
    pass


def tokenize(string: str) -> str:
    """Lowercase, remove spaces and underscores from the given string
    :param name: string to process
    :return: processed string
    """
    return string.lower().replace(r"[\s_]", "")


def upload_labels(
    ds: dict,
    project_id: str,
    version_id: str,
) -> None:
    """Upload labels from a COCO json
    :param ds: COCO datasource with categories, images and annotations
    :param project_id: Id of the project
    :param version_id: Id of the version
    """

    # Get project
    project = get_project(project_id)

    # Get all the images in the project
    images = get_images(project_id)

    # Create a list of images with empty annotations
    images_with_annotations = [{"image": image, "annotations": []} for image in images]

    # Map image names to images
    image_name_to_image = {
        image["image"]["name"]: image for image in images_with_annotations
    }

    # Parse classes in project
    classes = {
        tokenize(cls["name"]): {"is_new": False, "count": 0, **cls}
        for cls in project["classes"]
    }

    # Parse categories in datasource
    categories = ds.get("categories")
    if categories is None:
        raise CategoriesNotFound()

    # Map datasource category id to project class
    category_id_to_class = {}
    for category in categories:
        name = tokenize(category["name"])
        if name not in classes:
            classes[name] = {
                "is_new": True,
                "count": 0,
                "id": str(uuid4()),
                "name": category["name"],
                "color": get_random_color(),
            }
        category_id_to_class[category["id"]] = classes[name]

    # TODO: parse tags

    # Parse images in datasource
    ds_images = ds.get("images")
    if ds_images is None:
        raise ImagesNotFound()

    # Map datasource image id to project image
    image_mapping = {}
    for image in ds_images:
        if image["file_name"] in image_name_to_image:
            image_mapping[image["id"]] = image_name_to_image[image["file_name"]]

    # Parse annotations in datasource
    ds_annotations = ds.get("annotations")
    if ds_annotations is None:
        raise AnnotationsNotFound()

    # Process annotations
    for ann in ds_annotations:
        # Get project image
        image_with_annotations = image_mapping[ann["image_id"]]

        # Get class
        cls = category_id_to_class[ann["category_id"]]

        # Assert image or class
        if image is None or cls is None:
            continue

        # Get actual image
        image = image_with_annotations["image"]

        # Assert and round bounding box
        ann_bbox = ann["bbox"]
        bbox = {
            "x": round(ann_bbox[0]),
            "y": round(ann_bbox[1]),
            "width": round(ann_bbox[2]),
            "height": round(ann_bbox[3]),
        }
        if bbox["width"] == 0 or bbox["height"] == 0:
            continue

        if len(ann_bbox) == 5:
            # Bounding box has rotation
            angle = ann_bbox[4]
            cx = bbox["width"] / 2
            cy = bbox["height"] / 2
            bbox["x"] -= math.cos(angle) * cx - math.sin(angle) * cy
            bbox["y"] -= math.sin(angle) * cx + math.cos(angle) * cy
            bbox["rotation"] = angle * 180 / math.pi
        else:
            # Clip the bbox
            bbox = clip_bbox(bbox, {"width": image["width"], "height": image["height"]})

        # Create annotation
        annotation = {
            "id": str(uuid4()),
            "image_id": image["id"],
            "version_id": version_id,
            "class_id": cls["id"],
            "bbox": bbox,
            "color": get_random_color(),
        }

        # Process segmentation, if any
        if "segmentation" in ann:
            seg = ann["segmentation"]
            if isinstance(seg, list) and len(seg) > 0:
                # TODO: Convert polygons to rle
                continue
            elif "counts" in seg:
                if isinstance(seg["counts"], list):
                    # RLE is a list of ints
                    if len(seg["counts"]) < 2:
                        # Discard RLEs with less than 2 elements
                        continue
                    rle = seg["counts"]
                else:
                    # Rle is coco compressed string. Convert to list of ints.
                    rle = compressed_rle_to_list(seg["counts"])
                annotation["segmentation"] = {"rle": rle}

        # Add annotation to list
        image_with_annotations["annotations"].append(annotation)
        cls["count"] += 1

    # Discard classes without annotations
    classes = [cls for cls in classes.values() if cls["count"] > 0]

    # Discard images without annotations
    annotations = [
        {"image_id": image["image"]["id"], "annotations": image["annotations"]}
        for image in images_with_annotations
        if len(image["annotations"]) > 0
    ]

    # Assert there's annotations to upload
    n_annotations = sum([len(image["annotations"]) for image in annotations])
    if n_annotations == 0:
        raise NoAnnotationToUpload()

    # Upload the annotations
    client = get_client()
    client.post(
        f"/label/annotations/{project_id}",
        {"annotations": annotations, "classes": classes},
    )
    print(f"Uploaded {n_annotations} annotations to project '{project['name']}'")


def upload_labels_from_file(
    path: str,
    project_id: str,
    version_id: str,
) -> None:
    """Upload labels from a COCO json file
    :param path: path to the COCO file
    :param project_id: Id of the project
    :param version_id: Id of the version
    """

    # Assert path
    _path = Path(path)
    if not _path.is_file():
        raise PathNotFound(f"File '{path}' not found")

    # Open file
    with _path.open("r") as f:
        ds = json.load(f)

    # Upload labels
    upload_labels(ds, project_id, version_id)
