from dash.dependencies import Input, Output, State
import base64
from requests import post, exceptions


def get_callbacks(app, end_point):

    # load image and detect callback
    @app.callback([Output('upload-data', 'contents'),
                   Output('loading', 'children'),
                   Output('load-info', 'is_open'),
                   Output('load-info-text', 'children'),
                   Output('image', 'src')],
                  Input('upload-data', 'contents'),
                  State('upload-data', 'filename'))
    def upload_data(content, filename):
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

