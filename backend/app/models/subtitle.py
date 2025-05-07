class SubtitleModel:
    _subtitles = []

    def __init__(self, video_id, start_time, end_time, text):
        self.subtitle_id = max((subtitle.subtitle_id for subtitle in SubtitleModel._subtitles), default=0) + 1
        self.video_id = video_id
        self.start_time = start_time
        self.end_time = end_time
        self.text = text

        SubtitleModel._subtitle_id += 1
        SubtitleModel._subtitles.append(self)