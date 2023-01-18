"""Detector engine class"""
from torchvision.models import detection
import numpy as np
import torch
import cv2
from .coco_categories import get_categories
import warnings
import base64
from os import path

# get rid of torch deprecation warnings
warnings.filterwarnings("ignore", category=UserWarning)

PATH = path.dirname(__file__)
torch.hub.set_dir(PATH + '/hub')

# available models for torch.vision
RESNET = detection.fasterrcnn_resnet50_fpn
MOBILENET = detection.fasterrcnn_mobilenet_v3_large_320_fpn
RETINANET = detection.retinanet_resnet50_fpn

# what is considered as a car: car, truck, bus
CARS = [3, 6, 8]

# color for bounding boxes and text - blue
COLOR = [255, 0, 0]


class ImageError(Exception):
    """Exception class for errors when handling jpeg files"""
    pass


class Detector:
    """Detector class"""
    def __init__(self, net_model=RESNET, confidence=0.5):
        """Initialize detection model"""
        # set devices for cpu and gpu
        self.deviceCPU = torch.device("cpu")
        self.deviceGPU = torch.device("cuda") if torch.cuda.is_available() else None
        # get categories from file
        self.categories = get_categories()
        self.confidence = confidence
        self.image = None
        self.orig = None
        self.result = None
        # set models for cpu and gpu
        self.modelCPU = net_model(pretrained=True,
                                  progress=True,
                                  pretrained_backbone=True).to(self.deviceCPU)
        self.modelCPU.eval()
        if self.deviceGPU:
            self.modelGPU = net_model(pretrained=True,
                                      progress=True,
                                      pretrained_backbone=True).to(self.deviceGPU)
            self.modelGPU.eval()

    def load_image_from_file(self, image_path):
        """Load image from file"""
        try:
            self.image = cv2.imread(image_path)
        except AttributeError as e:
            raise ImageError('Input image is missing!') from None

    def load_image_from_bytes(self, image_bytes):
        """Load image from bytes"""
        image_array = np.fromstring(image_bytes, dtype='uint8')
        self.image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    def image_resize(self, width_max=1200):
        """If image is too big - resize it"""
        width, height = self.image.shape[1], self.image.shape[0]
        if width > width_max:
            dim = (width_max, int((width_max / width) * height))
            self.image = cv2.resize(self.image, dim, interpolation=cv2.INTER_AREA)

    def image_prepare(self):
        """Process image for detection"""
        # keep copy of original image - without processing
        self.orig = self.image.copy()
        # convert BGR to RGB
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        # process image for loading to torch
        self.image = self.image.transpose((2, 0, 1))
        self.image = np.expand_dims(self.image, axis=0)
        self.image = self.image / 255.0
        self.image = torch.FloatTensor(self.image)

    def run_detection(self, device='cpu'):
        """Run detection.
         result dict:
        'count': number of detections
        'boxes': list of bounding boxes
        'labels': list of labels for boxes"""
        # send image to the device
        # run detection
        if device == 'gpu' and self.deviceGPU:
            self.image = self.image.to(self.deviceGPU)
            detections = self.modelGPU(self.image)[0]
        else:
            self.image = self.image.to(self.deviceCPU)
            detections = self.modelCPU(self.image)[0]
        # loop over detections
        result = dict(count=0, boxes=[], labels=[])
        count = 0
        for i in range(0, len(detections["boxes"])):
            confidence = detections["scores"][i]
            idx = int(detections["labels"][i])
            # when condition is met append to list of boxes and labels
            if idx in CARS and confidence > self.confidence:
                count += 1
                box = detections["boxes"][i].detach().cpu().numpy()
                result['boxes'].append(box.astype("int").tolist())
                result['labels'].append(f"{self.categories[idx - 1]['name']} {confidence * 100:.2f}%")
        result['count'] = count
        self.result = result
        return result

    def get_result_image(self):
        """Draw boxes and put labels on the result image using result dict."""
        count = self.result['count']
        # loop over boxes and labels and draw them on the orig image
        for box, label in zip(self.result["boxes"], self.result['labels']):
            (startX, startY, endX, endY) = box
            cv2.rectangle(self.orig, (startX, startY), (endX, endY), COLOR, 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(self.orig, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLOR, 2)
        # put boxes count
        title = f'Count: {count}'
        cv2.putText(self.orig, title, (0, 30),
                    cv2.FONT_HERSHEY_DUPLEX, 1, COLOR, 3)

    def save_result_image_to_file(self, image_path):
        """save result to file"""
        cv2.imwrite(image_path, self.orig)

    def save_result_image_to_bytes(self):
        """return result image as bytes"""
        _, encoded_img = cv2.imencode('.jpg', self.orig)
        b64_encoded_img = base64.b64encode(encoded_img)
        return b64_encoded_img


