from dash import Input, Output, State
from requests import post, exceptions
import base64


def get_callbacks_as_tasks(app, end_point):

    # load image and detect callback
    @app.long_callback([Output('upload-data', 'contents'),
                        Output('loading', 'children'),
                        Output('load-info', 'is_open'),
                        Output('load-info-text', 'children'),
                        Output('image', 'src')],
                       Input('upload-data', 'contents'),
                       State('upload-data', 'filename'),
                       running=[(Output('image', 'src'), None, None),
                                (Output('upload-data', 'disabled'), True, False),
                                (Output('cancel-button', 'disabled'), False, True)],
                       cancel=Input('cancel-button', 'n_clicks'))
    def run_detection(content, filename):
        src = None
        if content:
            content_type, content_data = content.split(',')
            # check if image is JPEG and sent to API for detection
            if content_type == 'data:image/jpeg;base64':
                img = base64.b64decode(content_data)
                files = {'image': img}
                params = {'device': 'cpu'}
                try:
                    r = post(end_point, params=params, files=files)
                    r.raise_for_status()
                except exceptions.HTTPError as e:
                    return None, None, True, f'API error! {r.status_code} {r.content.decode()}', src
                except exceptions.RequestException as e:
                    return None, None, True, f'API error! {e}', src

                # get object detection image and show it
                src = f'data:image/jpg;base64,{r.content.decode()}'
                return None, None, False, None, src
            else:
                return None, None, True, 'This should be JPEG file!', None

