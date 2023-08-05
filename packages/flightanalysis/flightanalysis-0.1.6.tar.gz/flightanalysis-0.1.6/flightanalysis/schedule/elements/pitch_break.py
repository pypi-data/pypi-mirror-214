import numpy as np
from geometry import Transformation, Point, Quaternion, PX, PY, PZ
from flightanalysis.state import State
from flightanalysis.base.table import Time
from . import El, Loop, DownGrades, DownGrade, Elements
from flightanalysis.criteria import *
from . import Line



class PitchBreak(El):
    parameters = El.parameters + "length,break_angle".split(",")
    def __init__(self, speed: float, length: float, break_angle: float, uid: str=None):
        super().__init__(uid, speed)
        self.length=length
        self.break_angle = break_angle

    def to_dict(self):
        return dict(
            kind=self.__class__.__name__,
            speed=self.speed,
            length=self.length,
            break_angle=self.break_angle,
            uid=self.uid
        )


    def create_template(self, istate: State, time: Time=None):

        return Line(self.speed, self.length).create_template(
            istate, 
            time
        ).superimpose_rotation(
            PY(),
            self.break_angle
        ).label(element=self.uid)

    def describe(self):
        return "pitch break"
    
    def match_intention(self, transform: Transformation, flown: State):
        jit = flown.judging_itrans(transform)

        _speed = abs(flown.vel).mean()

        alphas = np.arctan2(flown.vel.z, flown.vel.x)

        return self.set_parms(
            speed = _speed,
            length = max(
                jit.att.inverse().transform_point(flown.pos - jit.pos).x[-1],
                5
            ) ,
            break_angle = alphas[-1]
        )
