from fastapi import FastAPI, File, UploadFile
from object_detector import Detector
from paths import get_paths

# Detector configuration
detector = Detector()

# API
app = FastAPI()

# import paths
get_paths(app, detector)
