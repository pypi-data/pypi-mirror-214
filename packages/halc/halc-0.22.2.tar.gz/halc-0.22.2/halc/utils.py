import random
from typing import List


def get_random_color() -> str:
    r = lambda: random.randint(0, 255)
    return "#%02X%02X%02X" % (r(), r(), r())


def clip_bbox(bbox: dict, size: dict) -> dict:
    x1 = max(bbox["x"], 0)
    y1 = max(bbox["y"], 0)
    x2 = min(bbox["x"] + bbox["width"], size["width"])
    y2 = min(bbox["y"] + bbox["height"], size["height"])
    return {"x": x1, "y": y1, "width": max(x2 - x1, 0), "height": max(y2 - y1, 0)}


def compressed_rle_to_list(counts: bytes) -> List[int]:
    listCounts: List[int] = []
    p = 0
    while p < len(counts):
        x = 0
        k = 0
        more = 1
        while more:
            c = counts[p] - 48
            x |= (c & 0x1F) << (5 * k)
            more = c & 0x20
            p += 1
            k += 1
            if not more and c & 0x10:
                x |= -1 << (5 * k)

        if len(listCounts) > 2:
            x += listCounts[len(listCounts) - 2]
        listCounts.append(x)

    return listCounts
