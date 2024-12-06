from yta_multimedia.video.generation.manim.utils.dimensions import ManimDimensions
from yta_multimedia.video.generation.manim.constants import HALF_SCENE_HEIGHT, HALF_SCENE_WIDTH, STANDARD_HEIGHT, STANDARD_WIDTH
from yta_general_utils.image.region import Coordinate as BaseCoordinate
from yta_general_utils.programming.enum import YTAEnum as Enum
from yta_general_utils.programming.parameter_validator import PythonValidator, NumberValidator
from yta_general_utils.image.region import NORMALIZATION_MIN_VALUE, NORMALIZATION_MAX_VALUE
from yta_general_utils.math import Math
from typing import Union


class VideoEngine(Enum):
    """
    Enum class to represent the different video engine
    systems we are using in this app.
    """
    MOVIEPY = 'moviepy'
    MANIM = 'manim'

class Coordinate(BaseCoordinate):
    """
    Class to simplify the way to create a Coordinate
    instance by providing one of our pre-defined
    scene positions.
    """
    engine: VideoEngine = None
    """
    The video engine for which this coordinate has
    been created.
    """
    scene_size: tuple = None
    """
    The scene dimensions (for moviepy engine) the
    coordinate has been built for.
    """

    def __init__(self, x: float, y: float, is_normalized: bool = False, engine: Union[VideoEngine, str] = VideoEngine.MOVIEPY, scene_size: tuple = (1920, 1080)):
        super().__init__(x, y, is_normalized)
        engine = VideoEngine.to_enum(engine)

        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            super().validate(scene_size, 'scene_size')
        
        self.type = type
        self.engine = engine
        self.scene_size = scene_size

    def to_moviepy(self):
        """
        Turn this Coordinate instance to a moviepy instance
        by updating 'x', 'y' and 'engine' attributes if
        necessary.
        """
        if self.engine == VideoEngine.MANIM:
            new_coordinate = self.as_moviepy_tuple()

            self.x = new_coordinate[0]
            self.y = new_coordinate[1]
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we force it
            self.scene_size = (1920, 1080)
            self.engine = VideoEngine.MOVIEPY

        return self
    
    def to_manim(self):
        """
        Turn this Coordinate instance to a manim instance
        by updating 'x', 'y' and 'engine' attributes if
        necessary.
        """
        if self.engine == VideoEngine.MOVIEPY:
            new_coordinate = self.as_manim_tuple()

            self.x = new_coordinate[0]
            self.y = new_coordinate[1]
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we force it
            self.scene_size = (1920, 1080)
            self.engine = VideoEngine.MANIM

        return self

    def as_moviepy_tuple(self):
        """
        Return this Coordinate instance as a moviepy coordinate
        tuple. This method will return a value but not update
        any instance attribute.

        This method forces the scene to be (1920, 1080) if Manim
        engine is set.
        """
        x, y = self.x, self.y
        if self.engine == VideoEngine.MANIM:
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we need to make sure
            # it is refering that screen size.
            # TODO: I need to refactor this. When 'x' is 0
            # in moviey in a 1920x1080 scene, the manim value
            # would be -
            x, y = self.to_scene_size((1920, 1080))
            x, y = Coordinate.manim_coordinate_to_moviepy_coordinate((x, y))

        return x, y
    
    def as_manim_tuple(self):
        """
        Return this Coordinate instance as a manim coordinate
        tuple. This method will return a value but not update
        any instance attribute.

        This method forces the scene to be (1920, 1080) if Manim
        engine is set.
        """
        x, y = self.x, self.y
        if self.engine == VideoEngine.MOVIEPY:
            # As we consider our manim scene similar to one
            # moviepy 1920x1080 scene, we need to make sure
            # it is refering that screen size.
            x, y = self.to_scene_size((1920, 1080))
            x, y = Coordinate.moviepy_coordinate_to_manim_coordinate((x, y))

        return x, y

    def update_scene_size(self, scene_size: tuple = (1920, 1080)):
        """
        Update the current scene size and also the coordinate
        values to fit the new scene size. This method updates
        this Coordiante instance attributes.
        """
        x, y = self.to_scene_size(scene_size)

        # TODO: What if Manim (?)
        self.x = x
        self.y = y
        self.scene_size = scene_size

        return self
    
    def to_scene_size(self, scene_size: tuple = (1920, 1080)):
        """
        Recalculate this Coordinate instante to fit in the 
        provided 'scene_size' but it doesn't change any instance
        attribute.

        This method returns the new coordinate (x, y) values.
        """
        if scene_size is None:
            scene_size = (1920, 1080)
        else:
            super().validate(scene_size, 'scene_size')

        x, y = self.x, self.y
        if self.scene_size != scene_size:
            # TODO: Recalculate x and y
            new_coordinate = Coordinate.recalculate_coordinate_on_new_scene_size((x, y), scene_size, self.scene_size)

            x = new_coordinate[0]
            y = new_coordinate[1]

        return x, y

    def get_moviepy_upper_left_corner_tuple(self, video_size: tuple):
        """
        Calculate the upper left corner tuple of this Coordinate
        instance based on its screen_size and the provided
        'video_size'.
        """
        super().validate(video_size, 'video_size')

        # TODO: What about 'self.type' (?) Maybe we
        # should avoid that attribute
        return Coordinate.to_moviepy_position_upper_left_corner(self, video_size)
    
    @staticmethod
    def moviepy_coordinate_to_manim_coordinate(coordinate: tuple):
        """
        Transform the provided moviepy 'coordinate' to
        a manim coordinate. Each of those coordinates 
        must be considered as built in a 1920x1080 scene.

        Please, ensure the provided 'coordinate' is 
        representing a point within a scene of 1920x1080.
        """
        super().validate(coordinate)

        # Scale for moviepy -> manim conversion
        x_scale = (HALF_SCENE_WIDTH * 2) / STANDARD_WIDTH
        y_scale = (HALF_SCENE_HEIGHT * 2) / STANDARD_HEIGHT
        
        x = (coordinate[0] - STANDARD_WIDTH / 2) * x_scale
        y = (STANDARD_HEIGHT / 2 - coordinate[1]) * y_scale

        return x, y
    
    @staticmethod
    def manim_coordinate_to_moviepy_coordinate(coordinate: tuple):
        """
        Transform the provided manim 'coordinate' to
        a moviepy coordinate. Each of those coordinates 
        must be considered as built in a 1920x1080 scene.

        Please, ensure the provided 'coordinate' is 
        representing a point within a scene of 1920x1080.
        """
        super().validate(coordinate)

        # Escala para Manim -> MoviePy (inversa)
        x_scale = STANDARD_WIDTH / (HALF_SCENE_WIDTH * 2)
        y_scale = STANDARD_HEIGHT / (HALF_SCENE_HEIGHT * 2)
        
        # Conversión de Manim a MoviePy
        x = (coordinate[0] * x_scale) + HALF_SCENE_WIDTH
        y = HALF_SCENE_HEIGHT - (coordinate[1] * y_scale)

        return x, y
    
    @staticmethod
    def recalculate_coordinate_on_new_scene_size(coordinate: Union['Coordinate', tuple], new_scene_size: tuple,  original_scene_size: tuple = (1920, 1080)):
        """
        Recalculate the provided 'coordinate' that has been built
        in the provided 'original_scene_size' to fit in the 
        'new_scene_size' provided.
        
        We don't care if 'coordinate' param is a Coordinate with a 
        .scene_size attribute set, we will use the
        'original_scene_size' provided.
        """
        super().validate(coordinate, 'coordinate')

        if original_scene_size is None:
            original_scene_size = (1920, 1080)
        else:
            super().validate(original_scene_size)

        if PythonValidator.is_tuple(coordinate):
            coordinate = Coordinate(coordinate[0], coordinate[1], scene_size = original_scene_size)

        new_coordinate = coordinate.x, coordinate.y
        if original_scene_size != new_scene_size:
            new_coordinate = (
                coordinate.x * (new_scene_size[0] / original_scene_size[0]),
                coordinate.y * (new_scene_size[1] / original_scene_size[1])
            )

        return new_coordinate

    @staticmethod
    def to_moviepy_position_upper_left_corner(coordinate: Union['Coordinate', tuple], video_size: tuple = (1920, 1080)):
        """
        Recalculate the provided 'coordinate' to obtain, by
        applying the 'video_size' given, the upper left
        corner needed by moviepy to position a video.
        """
        super().validate(coordinate, 'coordinate')

        if PythonValidator.is_tuple(coordinate):
            coordinate = Coordinate(coordinate[0], coordinate[1])

        if video_size is None:
            video_size = (1920, 1080)
        else:
            super().validate(video_size, 'video_size')
            
        # TODO: What if Coordinate is type corner (?) Maybe
        # it can be used to limit this method calls and avoid
        # using it again
        return coordinate.x - video_size[0] / 2, coordinate.y - video_size[1] / 2