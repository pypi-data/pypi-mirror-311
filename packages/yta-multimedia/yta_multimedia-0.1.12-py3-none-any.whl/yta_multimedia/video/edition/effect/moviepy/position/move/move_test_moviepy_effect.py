from yta_multimedia.video.edition.effect.moviepy.position.objects.video_position import VideoPosition
from yta_multimedia.video.position import Position
from yta_multimedia.video.edition.effect.moviepy.t_function import TFunctionSetPosition
from yta_multimedia.video.edition.effect.m_effect import MEffect as Effect
from yta_multimedia.video.edition.effect.moviepy.mask import ClipGenerator
from yta_multimedia.video.parser import VideoParser
from yta_multimedia.video.edition.effect.moviepy.objects import validate_position
from yta_multimedia.video.edition.effect.moviepy.position.utils.position import get_moviepy_position
from yta_multimedia.video.edition.effect.moviepy.objects import MoviepyArgument, MoviepyWith
from yta_multimedia.audio.channels import synchronize_audio_pan_with_video_by_position
from yta_general_utils.math.rate_functions import RateFunction
from moviepy import CompositeVideoClip
from moviepy.Clip import Clip
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
    def apply_over_video(cls, video: Clip, background_video: Clip, initial_position: Union[Position, VideoPosition, tuple] = Position.OUT_LEFT, final_position: Union[Position, VideoPosition, tuple] = Position.CENTER):
        video = VideoParser.to_moviepy(video)
        background_video = VideoParser.to_moviepy(background_video)

        validate_position(initial_position)
        validate_position(final_position)
        
        # We need the tuple position for the MoviepyArgument
        initial_position = get_moviepy_position(video, background_video, initial_position) 
        final_position = get_moviepy_position(video, background_video, final_position)

        arg = MoviepyArgument(initial_position, final_position, TFunctionSetPosition.arc, RateFunction.linear)
        video = MoviepyWith().apply_over_video(video, background_video, arg)

        # We pan the video audio by position
        video = synchronize_audio_pan_with_video_by_position(video.audio, video)

        return CompositeVideoClip([
            background_video,
            video
        ])