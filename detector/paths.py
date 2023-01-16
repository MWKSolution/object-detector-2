from fastapi import File, UploadFile, Response


def get_paths(app, detector):

    @app.get('/')
    def root():
        return {'message': 'detector API'}

    @app.post('/image')
    def send_image(image: UploadFile = File(...)):
        contents = image.file.read()
        detector.load_image_from_bytes(contents)
        detector.image_resize()
        detector.image_prepare()
        result = detector.run_detection()
        detector.get_result_image()
        image_bytes = detector.save_result_image_to_bytes()
        # return result
        return Response(content=image_bytes, media_type='image/jpeg')
