from fastapi import File, UploadFile, Response


def get_paths(app, detector):

    @app.get('/')
    def root():
        """root path for testing """
        return {'message': 'detector API'}

    @app.post('/image')
    def get_image_and_detect(device: str, image: UploadFile = File(...)):
        """Get uploaded image and run detection"""
        contents = image.file.read()
        detector.load_image_from_bytes(contents)
        detector.image_resize()
        detector.image_prepare()
        result = detector.run_detection(device)
        detector.get_result_image()
        image_bytes = detector.save_result_image_to_bytes()
        # return image with labels and bounding boxes
        return Response(content=image_bytes, media_type='image/jpeg')
