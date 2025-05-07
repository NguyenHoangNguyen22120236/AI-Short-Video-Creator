class OptionalAdjustmentModel:
    _optional_adjustments = []

    def __init__(self, video_id, name, file_url, start_time, duration):
        self.optional_adjustment_id = max((adj.optional_adjustment_id for adj in OptionalAdjustmentModel._optional_adjustments), default=0) + 1
        self.video_id = video_id
        self.name = name
        self.file_url = file_url
        self.start_time = start_time
        self.duration = duration

        OptionalAdjustmentModel._optional_adjustment_id += 1
        OptionalAdjustmentModel._optional_adjustments.append(self)

    