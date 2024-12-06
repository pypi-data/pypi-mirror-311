def split_time_frame(
    s: float,
    e: float,
    *,
    max_length: float = 999999.0,
    min_length: float = 0.0,
) -> list[tuple[float, float]]:
    time_d = e - s
    time_frames = [
        (s + i * max_length, min(s + (i + 1) * max_length, e))
        for i in range(
            int(time_d // max_length) + (1 if time_d % max_length > 0 else 0)
        )
    ]
    if len(time_frames) == 0:
        return []
    last_time_d = time_frames[-1][1] - time_frames[-1][0]
    time_frames = time_frames if last_time_d >= min_length else time_frames[:-1]
    return time_frames


def adjust_time_frames_to_keyframes(
    time_frames: list[list[float]], keyframes: list[float]
):
    margin = 0.5
    adjusted_cuts = []
    for i, (start, end) in enumerate(time_frames):
        start_match = None
        end_match = None
        for keyframe in keyframes:
            if abs(keyframe - start) < margin:
                start_match = keyframe
            if abs(keyframe - end) < margin:
                end_match = keyframe
        if start_match is None or end_match is None:
            # print(f"Cut #{i} ({start}-{end}) not matched to keyframes")
            pass
        else:
            adjusted_cuts.append([start_match, end_match])
    return adjusted_cuts


def timestamp_to_str(timestamp: int) -> str:
    hours = timestamp // (60 * 60 * 1000)
    minutes = (timestamp % (60 * 60 * 1000)) // (60 * 1000)
    seconds = (timestamp % (60 * 1000)) // 1000
    milliseconds = timestamp % 1000
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
