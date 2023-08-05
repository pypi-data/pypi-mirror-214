from geometry import Point, Quaternion, Transformation, PX, PY, PZ, P0, Q0

import numpy as np
import pandas as pd
from typing import Union

from flightanalysis.base.table import Table, Constructs, SVar, Time


def make_bvel(sec) -> Point:
    if len(sec) > 1:
        wvel = sec.pos.diff(sec.dt)
        return sec.att.inverse().transform_point(wvel)
    else:
        return P0()

def make_rvel(sec) -> Point:
    if len(sec) > 1:
        return sec.att.body_diff(sec.dt).remove_outliers(3) 
    else:
        return P0()

def make_bacc(sec) -> Point:
    if len(sec) > 1:
        wacc = sec.att.transform_point(sec.vel).diff(sec.dt) + PZ(9.81, len(sec)) # assumes world Z is up
        return sec.att.inverse().transform_point(wacc)
    else:
        return P0()

def make_racc(sec) -> Point:
    if len(sec) > 1:
        return sec.rvel.diff(sec.dt)
    else:
        return P0()


class State(Table):
    constructs = Table.constructs + Constructs([
        SVar("pos", Point,       ["x", "y", "z"]           , lambda self: P0(len(self))       ), 
        SVar("att", Quaternion,  ["rw", "rx", "ry", "rz"]  , lambda self : Q0(len(self))       ),
        SVar("vel", Point,       ["u", "v", "w"]           , make_bvel  ),
        SVar("rvel", Point,       ["p", "q", "r"]           , make_rvel ),
        SVar("acc", Point,       ["du", "dv", "dw"]        , make_bacc  ),
        SVar("racc", Point,       ["dp", "dq", "dr"]        , make_racc ),
    ])
    _construct_freq = 30

    @property
    def transform(self):
        return Transformation.build(self.pos, self.att)
    
    @property
    def back_transform(self):
        return Transformation(-self.pos, self.att.inverse())
     
    @staticmethod
    def from_transform(transform: Transformation, **kwargs):
        if not "time" in kwargs: 
            kwargs["time"] = Time.from_t(np.linspace(0, State._construct_freq*len(transform), len(transform)))
        return State.from_constructs(pos=transform.p, att=transform.q, **kwargs)

    def body_to_world(self, pin: Point, rotation_only=False) -> Point:
        """Rotate a point in the body frame to a point in the data frame

        Args:
            pin (Point): Point on the aircraft

        Returns:
            Point: Point in the world
        """
        if rotation_only:
            return self.transform.rotate(pin)
        else:
            return self.transform.point(pin)

    def world_to_body(self, pin: Point, rotation_only=False) -> Point:
        if rotation_only:
            self.back_transform.rotate(pin)
        else:
            return self.back_transform.point(pin)