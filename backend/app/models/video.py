class VideoModel:
    _videos = []

    def __init__(self, user_id, topic, title, script, audio, subtitles, images):
        self.video_id = max((video.video_id for video in VideoModel._videos), default=0) + 1
        self.user_id = user_id
        self.topic = topic
        self.title = title
        self.script = script
        self.audio = audio
        self.subtitles = subtitles
        self.images = images

        VideoModel._video_id += 1

    def add_video(self):
        VideoModel._videos.append(self)

    def delete_video(self):
        VideoModel._videos.remove(self)