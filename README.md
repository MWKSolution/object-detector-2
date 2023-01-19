# Detecting common objects on JPEG images   

---

This is an example of using pretrained **PyTorch** NN model for detecting objects on provided images.  

It uses standard **resnet50_fpn** model from **torchvision** library of **PyTorch**.  It can detect people, animals and  common objects defined in COCO classes:  
>*person, bicycle, car, motorcycle, airplane, bus, train, truck, boat, traffic light, fire hydrant,
stop sign, parking meter, bench, bird, cat, dog, horse, sheep, cow, elephant, bear, zebra, giraffe,
backpack, umbrella, handbag, tie, suitcase, frisbee, skis, snowboard, sports ball, kite, baseball bat,
baseball glove, skateboard, surfboard, tennis racket, bottle, wine glass, cup, fork, knife, spoon, bowl,
banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake, chair, couch, potted plant,
bed, dining table, toilet, tv, laptop, mouse, remote, keyboard, cell phone, microwave, oven, toaster,
sink, refrigerator, book, clock, vase, scissors, teddy bear, hair drier, toothbrush*

The **resnet50_fpn** was chosen over the other, available on **torchvision**, pre-trained models due to its low detection error rate.  
Although it has longer detection times especially when using *cpu* device.  
Result of using **resnet50_fpn** model for objects detection are presented below on set of example images that are present in COCO classes: 

![result](https://user-images.githubusercontent.com/105928466/213688844-ce084d01-0179-4f1f-89e9-f6b40a787578.jpg)  
>Image source: *Bourouis, S., Channoufi, I., Alroobaea, R. et al. Color object segmentation and tracking using flexible statistical model and level-set. Multimed Tools Appl 80, 5809–5831 (2021). https://doi.org/10.1007/s11042-020-09809-2*  

---

## Implementation

It consists of four services which could be run on **Docker**.
 1. **detapi** - **FastAPI** objects detection API service receiving JPEG images and returning images with labels and bounding boxes of detected objects on them.
 2. **worker** - **celery** worker for queueing detection tasks for **detapi**
 3. **redis** - redis database as a broker and backed for celery **worker**
 4. **detapp** - frontend **Dash** application for uploading JPEG images and viewing detection results. It sends detection tasks to **detapi** via celery task queue.

---