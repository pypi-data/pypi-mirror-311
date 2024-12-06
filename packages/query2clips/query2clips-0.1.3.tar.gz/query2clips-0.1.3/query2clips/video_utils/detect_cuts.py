"""
cut detection subsampler detects cuts in a video
"""

import numpy as np
from scenedetect import ContentDetector, SceneManager, open_video


# TODO: this can be done more elegantly:
# from scenedetect import scene_manager and set that in correct namespace
# best solution is just figure out best value for them and submit PR
DEFAULT_MIN_WIDTH = 64


def get_scenes_from_scene_manager(scene_manager, cut_detection_mode):
    """
    Returns a list of cuts from a scene manager given a cut detection mode
    """
    scene_list = scene_manager.get_scene_list(start_in_scene=True)
    scene = []

    for clip in scene_list:
        scene.append([clip[0].get_frames(), clip[1].get_frames()])

    if cut_detection_mode == "longest":  # we have multiple cuts, pick the longest
        longest_clip = np.argmax([clip[1] - clip[0] for clip in scene])
        scene = [scene[longest_clip]]

    return scene


def detect_cuts(
    video_path,
    cut_detection_mode="all",
    framerates=None,
    threshold=27,
    min_scene_len=15,
):
    video = open_video(video_path)

    detector = ContentDetector(threshold=threshold, min_scene_len=min_scene_len)
    scene_manager = SceneManager()
    scene_manager.add_detector(detector)
    scene_manager.auto_downscale = False
    scene_manager.downscale = video.frame_size[0] // DEFAULT_MIN_WIDTH

    cuts = {}
    original_fps = video.frame_rate
    cuts["original_fps"] = original_fps

    scene_manager.detect_scenes(video=video)
    cuts["cuts_original_fps"] = get_scenes_from_scene_manager(
        scene_manager, cut_detection_mode
    )
    if framerates is not None:
        for target_fps in framerates:
            video.reset()

            detector = ContentDetector(threshold=threshold, min_scene_len=min_scene_len)
            scene_manager = SceneManager()
            scene_manager.add_detector(detector)
            frame_skip = max(
                int(original_fps // target_fps) - 1, 0
            )  # if we take 1 frame and skip N frames we're sampling 1/N+1 % of the video
            # so if we desire to sample 1/N of the video, we need to subtract one when doing frame skipping

            scene_manager.detect_scenes(video=video, frame_skip=frame_skip)
            cuts[f"cuts_{target_fps}"] = get_scenes_from_scene_manager(
                scene_manager, cut_detection_mode
            )
            scene_manager.clear()
    cuts["cuts_time_frames"] = (
        (np.array(cuts["cuts_original_fps"]) / original_fps)
    ).tolist()

    return cuts
