from moviepy.Effect import Effect
from moviepy.Clip import Clip


class MEffect(Effect):
    """
    Effect to be applied on a single video without any
    other video dependence.

    This effect cannot be applied as moviepy effects as
    the structure is different.

    TODO: If I want to make my own moviepy effects that
    are able to be applied as moviepy does, I need to
    respect the structure and just manipulate the frames.
    So, those new custom moviepy effects sohuld be placed
    in other folder as this MEffect is my own effect that
    works in a different way.
    """
    # TODO: Is this working (?)
    result_must_replace: bool = False
    """
    This parameter indicates if this effect, when applied,
    must replace the original clip part or, if False, must
    be concatenated.
    """
    def apply_over_video(self, video: Clip, background_video: Clip):
        # TODO: Should I (?)
        pass