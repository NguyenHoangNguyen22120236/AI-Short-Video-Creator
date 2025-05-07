class AudioModel:
    _audios = []

    def __init__(self, video_id, voice_id, language, file_url, sence):
        self.audio_id = max((audio.audio_id for audio in AudioModel._audios), default=0) + 1
        self.video_id = video_id
        self.voice_id = voice_id
        self.language = language
        self.file_url = file_url
        self.sence = sence

        AudioModel._audios.append(self)
