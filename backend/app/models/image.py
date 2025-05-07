class ImageModel():
    _images = []

    def __init__(self, video_id, image_url):
        self.image_id = max((img.image_id for img in ImageModel._images if img.video_id == video_id), default=0) + 1
            
        self.video_id = video_id
        self.image_url = image_url

        ImageModel._images.append(self)