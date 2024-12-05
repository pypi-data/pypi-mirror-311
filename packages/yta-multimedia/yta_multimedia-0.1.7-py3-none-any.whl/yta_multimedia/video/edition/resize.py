from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_general_utils.dimensions import adjust_to_aspect_ratio
from yta_general_utils.programming.enum import YTAEnum as Enum
from moviepy.Clip import Clip
from moviepy import CompositeVideoClip
from moviepy.video.fx import Crop
from typing import Union


class EnlargeMode(Enum):
    """
    Enum class to encapsulate the different strategies to
    enlarge a video.
    """
    RESIZE = 'resize'
    """
    The video is resized to fit the expected larger size.
    """
    BACKGROUND = 'background'
    """
    The video is placed as it is but in the middle of a
    black background with the expected size.
    """

class EnshortMode(Enum):
    """
    Enum class to encapsulate the different strategies to
    enshort a video.
    """
    RESIZE = 'resize'
    """
    The video is resized to fit the expected smaller size.
    This can make the video lose the aspect ratio.
    """
    CROP = 'crop'
    """
    The video is cropped in the center to obtain a region
    of the expected size.
    """

def fit_size(video: Clip, size: tuple, enlarge_mode: EnlargeMode = EnlargeMode.RESIZE, enshort_mode: EnshortMode = EnshortMode.RESIZE):
    """
    Make the provided 'video' fit the also provided 'size' by 
    applying the given 'enlarge_mode' or 'enshort_mode' depending
    of the need.
    """
    # TODO: This generates a cyclic import issue
    #video = VideoParser.to_moviepy(video)

    if not enlarge_mode:
        enlarge_mode = EnlargeMode.default()
    else:
        enlarge_mode = EnlargeMode.to_enum(enlarge_mode)

    if not enshort_mode:
        enshort_mode = EnshortMode.default()
    else:
        enshort_mode = EnshortMode.to_enum(enshort_mode)

    if video.size > size:
        # We need to enshort it
        if enshort_mode == EnshortMode.RESIZE:
            video = video.resize(size)
        elif enshort_mode == EnshortMode.CROP:
            # We need to adjust the video to the AR of the given 'size'
            new_ar = size[0] / size[1]
            video_width, video_height = video.size
            new_video_size = adjust_to_aspect_ratio(video_width, video_height, new_ar)

            # TODO: Is this working (?) Changed when moviepy 2.0.0
            video = video.with_effects([Crop(video, width = new_video_size[0], height = new_video_size[1], x_center = video_width / 2, y_center = video_height / 2)])

            video = video.resized((size[0], size[1]))
    elif video.size < size:
        # We need to enlarge it
        if enlarge_mode == EnlargeMode.RESIZE:
            video = video.resize(size)
        elif enlarge_mode == EnlargeMode.BACKGROUND:
            video = CompositeVideoClip([
                ClipGenerator.get_default_background_video(size, video.duration, False),
                video.with_position(('center', 'center'))
            ])

    return video

# TODO: I think I can deprecate (and remove) this method
# when the one above is working and is confirmed
def resize_video(video: Clip, size, output_filename: Union[str, None] = None):
    """
    Resizes the video to the provided 'size' by cropping a
    region of the given 'video' that fits the 'size' aspect
    ratio and resizing that region to the 'size'.

    This method is using the whole video and then resizing,
    so the quality of the video is preserved and no small
    regions are used. The most part of the video is 
    preserved.

    This method returns the video modified.

    This method will write the video if 'output_filename' is
    provided.
    """
    # TODO: This generates a cyclic import issue
    #video = VideoParser.to_moviepy(video)

    # We need to adjust the video to the AR of the given 'size'
    new_ar = size[0] / size[1]
    video_width, video_height = video.size
    new_video_size = adjust_to_aspect_ratio(video_width, video_height, new_ar)

    # TODO: Is this working (?) Changed when moviepy 2.0.0
    video = video.with_effects([Crop(video, width = new_video_size[0], height = new_video_size[1], x_center = video_width / 2, y_center = video_height / 2)])

    # We resize it (up or down) to the desired 'size'
    video = video.resized((size[0], size[1]))

    if output_filename:
        video.write_videofile(output_filename)

    return video