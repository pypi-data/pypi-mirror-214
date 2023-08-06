import numpy as np
import pandas as pd
from typing import Union, List
from numbers import Number
from . import Result
import inspect


class Combination:
    """Handles a series of criteria assessments.
    for example a number of rolls in an element. 
    """
    def __init__(self, desired: List[List[Number]], criteria=None, scr:str=None):
        self.desired = np.array(desired)
        self.criteria = lambda x : 0.0 if criteria is None else criteria
        self.scr = scr if scr else inspect.getsourcelines(self.criteria)[0][0].split("=")[1].strip()

    def __getitem__(self, value: int):
        return self.desired[value]

    def get_errors(self, values: np.ndarray):
        """get the error between values and desired for all the options"""
        return self.desired - np.array(values)

    def get_option_error(self, option: int, values: np.ndarray) -> np.ndarray:
        """The difference between the values and a given option"""
        return np.array(values) - self.desired[option]

    def check_option(self, values):
        """Given a set of values, return the option id which gives the least error"""
        return np.sum(np.abs(self.get_errors(values)), axis=1).argmin()

    def __call__(self, name: str, values):
        dgs = self.criteria(self.get_option_error(self.check_option(values), values))
        return Result(name, values, dgs)

    def to_dict(self):
        return dict(
            kind = self.__class__.__name__,
            desired = list(self.desired),
            criteria = self.scr
        )

    @staticmethod
    def from_dict(data:dict):
        return Combination(
            desired = np.array(data["desired"]),
            criteria = eval(data["criteria"]),
            scr=data["criteria"]
        )

    @staticmethod
    def rolllist(rolls, reversable=True):
        rolls = [rolls, [-r for r in rolls]] if reversable else [rolls]
        return Combination(rolls)

    @staticmethod
    def rollcombo(rollstring, reversable=True):
        """Convenience constructor to allow Combinations to be built from strings such as 2X4 or 
        1/2"""
        if rollstring[1] == "/":
            rolls = [float(rollstring[0])/float(rollstring[2])]
        elif rollstring[1] in ["X", "x", "*"]:
            rolls = [1/int(rollstring[2]) for _ in range(int(rollstring[0]))]
        rolls = [r*2*np.pi for r in rolls]
        
        return Combination.rolllist(rolls, reversable)