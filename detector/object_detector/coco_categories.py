"""COCO categories"""
import json
from os import path

PATH = path.dirname(__file__)

# list of COCO classes used for labeling, torch is returning numbers which corresponds to indices on that list(tuple)
COCO_NAMES = (
    '__background__', 'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus',
    'train', 'truck', 'boat', 'traffic light', 'fire hydrant', 'N/A', 'stop sign',
    'parking meter', 'bench', 'bird', 'cat', 'dog', 'horse', 'sheep', 'cow',
    'elephant', 'bear', 'zebra', 'giraffe', 'N/A', 'backpack', 'umbrella', 'N/A', 'N/A',
    'handbag', 'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard', 'surfboard', 'tennis racket',
    'bottle', 'N/A', 'wine glass', 'cup', 'fork', 'knife', 'spoon', 'bowl',
    'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'N/A', 'dining table',
    'N/A', 'N/A', 'toilet', 'N/A', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
    'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'N/A', 'book',
    'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush')


class CocoCategoriesError(Exception):
    pass


def get_categories():
    """Get coco categories as dict. File: 'annotations/coco_categories.json' must be present.
    If not, run this scrip directly to create one."""
    try:
        with open(PATH + '/annotations/coco_categories.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise CocoCategoriesError('COCO categories json file is missing.') from None
    except json.decoder.JSONDecodeError as e:
        raise CocoCategoriesError('COCO categories json file is corrupted.') from None


if __name__ == '__main__':
    # Get coco categories from annotations. Save in coco_categories.json for further use.
    print("""If this doesn't work:
    1. Download: > http://images.cocodataset.org/annotations/annotations_trainval2017.zip < ,
    2. From zip file copy: > instances_val2017.json < to annotations directory ,
    3. Run this again.""")
    with open(PATH + '/annotations/instances_val2017.json', 'r') as annotations:
        annotations_json = json.load(annotations)

    categories = annotations_json['categories']

    # show name by id
    print(COCO_NAMES[90])  # toothbrush
    print(COCO_NAMES[59])  # pizza

    with open(PATH + '/annotations/coco_categories.json', 'w') as coco:
        json.dump(categories, coco)

    # Show coco categories
    print('COCO categories: ', json.dumps(get_categories(), indent=True))
