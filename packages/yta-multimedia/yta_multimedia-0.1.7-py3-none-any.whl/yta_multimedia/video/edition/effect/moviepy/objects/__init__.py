from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition, TFunctionResize, TFunctionRotate
from yta_multimedia.video.edition.effect.moviepy.position.objects.base_position_moviepy_effect import BasePositionMoviepyEffect
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.duration import set_video_duration
from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.edition.effect.moviepy.position import Position
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
from yta_general_utils.math.rate_functions import RateFunction
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy.Clip import Clip
from typing import Union

import numpy as np
# TODO: Maybe unify all these to a MoviepyArgument (?) as
# they are very similar: 'start', 'end', 'rate_func'
# TODO: Maybe rename to MoviepyResize

class MoviepyResize:
    def __init__(self, initial_size: float, final_size: float, t_function: type = TFunctionResize.resize_from_to, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.initial_size = initial_size
        self.final_size = final_size
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

class MoviepySetPosition:
    initial_position: VideoPosition = None
    final_position: VideoPosition = None

    def __init__(self, initial_position: tuple, final_position: float, t_function: type = TFunctionSetPosition.linear, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.initial_position = initial_position
        self.final_position = final_position
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

    def apply(self, video):
        BasePositionMoviepyEffect.validate_position(self.initial_position)
        BasePositionMoviepyEffect.validate_position(self.final_position)

        background_video = ClipGenerator.get_default_background_video(duration = video.duration)

        video = video.with_position(lambda t: self.t_function(t, video.duration, get_moviepy_position(video, background_video, self.initial_position), get_moviepy_position(video, background_video, self.final_position), self.rate_func))

        return video
    
class MoviepyWithPosition:
    initial_position: VideoPosition = None
    final_position: VideoPosition = None

    def __init__(self, initial_position: tuple, final_position: float, t_function: type = TFunctionSetPosition.linear, rate_func: type = RateFunction.linear, *args, **kwargs):
        # TODO: Check that all params are provided and valid
        self.initial_position = initial_position
        self.final_position = final_position
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

    def apply(self, video: Clip):
        if not PythonValidator.is_instance(self.initial_position, [Position, VideoPosition]):
            raise Exception('Provided "position" is not a valid Position or VideoPosition.')
        
        if not PythonValidator.is_instance(self.final_position, [Position, VideoPosition]):
            raise Exception('Provided "position" is not a valid Position or VideoPosition.')
        
        background_video = ClipGenerator.get_default_background_video(duration = video.duration)

        frame_duration = video.duration / (video.duration * video.fps)
        ts = np.linspace(0, video.duration, int(video.duration * video.fps))

        sizes = [TFunctionResize.resize_from_to(t, video.duration, 0.1, 0.5, RateFunction.rush_into) for t in ts]
        positions = [TFunctionSetPosition.at_position(t, (500, 500), (video.w * sizes[i], video.h * sizes[i])) for i, t in enumerate(ts)]

        video = video.with_position(lambda t: self.t_function(t, video.duration, get_moviepy_position(video, background_video, self.initial_position), get_moviepy_position(video, background_video, self.final_position), self.rate_func))

        video = video.resized(lambda t: sizes[int(t // frame_duration)])
        video = video.with_position(lambda t: positions[int(t // frame_duration)])

        return video

class MoviepyRotate:
    # TODO: Check that all params are provided and valid
    def __init__(self, initial_rotation: int, final_rotation: int, t_function: type = TFunctionRotate.rotate_from_to, rate_func: type = RateFunction.linear, *args, **kwargs):
        self.initial_rotation = initial_rotation
        self.final_rotation = final_rotation
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: Set '*args' and '**kwargs'

# TODO: Keep this below and remove cod from above
class MoviepyArgument:
    """
    Arguments used for 'with_position', 'resized' and 'rotated'
    """
    def __init__(self, start: Union[int, tuple, float], end: Union[int, tuple, float], t_function: type, rate_func: RateFunction = RateFunction.linear):
        # TODO: 'start' and 'end' must be pure values which
        # means tuples if positions or numbers if resize or
        # rotate
        # TODO: Validate parameters
        self.start = start
        self.end = end
        self.t_function = t_function
        self.rate_func = rate_func
        # TODO: *args or **kwargs should be avoided as we must
        # define the 't_function' with the only parameters 
        # needed and make as much as we need. For example, we
        # should have '.arc_bottom' and '.arc_top' to avoid
        # passing a 'is_bottom' parameter because it would 
        # lost the common structure.

# TODO: Rename to MoviepyWithProcess or something more clear
class MoviepyWith:
    """
    Class to encapsulate the 'resized', 'with_position' and
    'rotated' functionality and to be able to make one depend
    on the other by pre-calculating the values and then using
    them when positioning, resizing and rotating.

    You should use the same RateFunction if you are planning
    to move and resize the clip at the same time.
    """
    @staticmethod
    def apply(video: Clip, with_position: Union[MoviepyArgument, None] = None, resized: Union[MoviepyArgument, None] = None, rotated: Union[MoviepyArgument, None] = None):
        """
        Apply the property effects on the provided 'video'. This
        method will use a default background video to apply the
        effect.

        Default background is 1920x1080.

        :param MoviepyArgument with_position: The position to apply (as a lambda t function).

        :param MoviepyArgument resized: The resize effect to apply (as a lambda t function).

        :param MoviepyArgument rotated: The rotation effect to apply (as a lambda t function).
        """
        return MoviepyWith.apply_over_video(video, ClipGenerator.get_default_background_video(duration = video.duration), with_position, resized, rotated)

    @staticmethod
    def apply_over_video(video: Clip, background_video: Clip, with_position: Union[MoviepyArgument, None] = None, resized: Union[MoviepyArgument, None] = None, rotated: Union[MoviepyArgument, None] = None):
        """
        Apply the property effects on the provided 'video'. This
        method will use the provided 'background_video' and 
        recalculate the position according to it.

        Background can be different to default scene of 1920x1080
        so positions will be adjusted to it.

        :param MoviepyArgument with_position: The position to apply (as a lambda t function).

        :param MoviepyArgument resized: The resize effect to apply (as a lambda t function).

        :param MoviepyArgument rotated: The rotation effect to apply (as a lambda t function).
        """
        video = VideoParser.to_moviepy(video, do_include_mask = True)
        background_video = VideoParser.to_moviepy(background_video, True)
        background_video = BasePositionMoviepyEffect.prepare_background_clip(background_video, video)

        # Prepare data for pre-calculations
        frame_duration = video.duration / (video.duration * video.fps)
        ts = np.linspace(0, video.duration, int(video.duration * video.fps))

        if resized:
            resizes = [resized.t_function(t, video.duration, resized.start, resized.end, resized.rate_func) for t in ts]
        else:
            # We build always this array because position calculation 
            # depends on it to be able to handle movement and resizing
            # at the same time
            resizes = [1 for _ in ts]

        positions = None
        if with_position:
            initial_position = get_moviepy_position(video, background_video, with_position.start)
            final_position = get_moviepy_position(video, background_video, with_position.end)
            positions = []
            for i, t in enumerate(ts):
                # Calculate each frame position based on each frame size
                initial_position = (initial_position[0] * resizes[i], initial_position[1] * resizes[i])
                final_position = (final_position[0] * resizes[i], final_position[1] * resizes[1])

                # TODO: This 'with_position.t_function' can have different
                # parameters to be able to work, so I don't know how to
                # dynamically handle this. For example, the 'at_position'
                # needs the video.size to be able to calculate where to
                # be centered...
                positions.append(with_position.t_function(t, video.duration, initial_position, final_position))
                
        rotations = None
        if rotated:
            rotations = [rotated.t_function(t, video.duration, rotated.start, rotated.end, rotated.rate_func) for t in ts]

        # I add frame_duration * 0.1 to make sure it fits the
        # next index
        video = video.resized(lambda t: resizes[int((t + frame_duration * 0.1) // frame_duration)])
        if positions:
            video = video.with_position(lambda t: positions[int((t + frame_duration * 0.1) // frame_duration)])
        if rotated:
            video = video.rotated(lambda t: rotations[int((t + frame_duration * 0.1) // frame_duration)])
        
        return video

# TODO: Maybe relocate these 2 methods from below
def validate_position(position: Union[Position, VideoPosition, tuple]):
    """
    Validates that the provided 'position' is an Position 
    or a VideoPosition, or raises an Exception if not.
    """
    if not PythonValidator.is_instance(position, [Position, VideoPosition, tuple]):
        raise Exception('Provided "position" is not a valid Position or VideoPosition.')
    
    if PythonValidator.is_tuple(position) and len(position) != 2:
        # TODO: Maybe apply the normalization limits as limits
        # here for each position tuple element
        raise Exception('Provided "position" is a tuple but does not have 2 values.')
    
def prepare_background_clip(background_video: Clip, video: Clip):
    """
    Prepares the provided 'background_video' by setting its duration to the same
    as the also provided 'video'. By default, the strategy is looping the 
    'background_video' if the 'video' duration is longer, or cropping it if it is
    shorter. This method returns the background_clip modified according to the
    provided 'video'.

    This method will raise an Exception if the provided 'video' or the provided
    'background_video' are not valid videos.
    """
    VideoParser.to_moviepy(background_video)
    VideoParser.to_moviepy(video)

    background_video = set_video_duration(background_video, video.duration)

    return background_video