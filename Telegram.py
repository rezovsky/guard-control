import os


class Telegram:
    def get_images(self, groups, base_url):

        folder_path = 'images'

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        for group in groups:
            url = f"{base_url}/group/{group}"

            output_path = f"{folder_path}/{group}.png"

            options = {
                'format': 'png',
                'width': 1024,
                'height': 768,
            }


        return 'ok'
