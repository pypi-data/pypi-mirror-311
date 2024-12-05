from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.objects import validate_position
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWith
from yta_general_utils.math.rate_functions import RateFunction
from moviepy import Clip, CompositeVideoClip
from typing import Union


class MoveTestMoviepyEffect(Effect):
    """
    Effect of moving the element from one place in the screen (or outside
    of bounds) to another, linearly.
    """

    # TODO: This must inherit from an abstract class I think
    def apply(self, video: Clip, initial_position: Union[Position, VideoPosition], final_position: Union[Position, VideoPosition], arc_is_bottom: bool = False, max_arc_height: float = 300.0):
        """
        Applies the effect to the 'video' provided when initializing this
        effect class, and puts the video over a static black background
        image of 1920x1080.
        """
        return self.apply_over_video(video, ClipGenerator.get_default_background_video(duration = video.duration), initial_position, final_position, arc_is_bottom, max_arc_height)
    
    @classmethod
    def apply_over_video(cls, video: Clip, background_video: Clip, initial_position: Union[Position, VideoPosition] = Position.OUT_LEFT, final_position: Union[Position, VideoPosition] = Position.CENTER, arc_is_bottom: bool = False, max_arc_height: float = 300):
        video = VideoParser.to_moviepy(video)
        background_video = VideoParser.to_moviepy(background_video)

        validate_position(initial_position)
        validate_position(final_position)
        
        # TODO: TFunction methods must have the same receiving values
        # so we should create '.arc_top' and '.arc_bottom' to choose
        # the method and let the method be the one who is built with
        # the arc position
        # TODO: We also have to pay attention to the moment in which 
        # we process the positions to adapt to the background because
        # we need to make sure we are not doing it twice or more
        # times than only one
        arg = MoviepyArgument(initial_position, final_position, TFunctionSetPosition.arc, RateFunction.linear)
        video = MoviepyWith().apply_over_video(video, background_video, arg)

        return CompositeVideoClip([
            background_video,
            video
        ])