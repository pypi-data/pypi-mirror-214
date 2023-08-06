# %% -*- coding: utf-8 -*-
"""
This module holds the class for movement tools based on Primitiv.

Classes:
    Primitiv (Gantry)
"""
# Standard library imports
from __future__ import annotations
import time
from typing import Optional

# Local application imports
from ...misc import Helper
from .cartesian_utils import Gantry
print(f"Import: OK <{__name__}>")

class Primitiv(Gantry):
    """
    Primitiv provides controls for the Primitv platform

    ### Constructor
    Args:
        `port` (str): COM port address
        `limits` (tuple[tuple[float]], optional): lower and upper limits of gantry. Defaults to ((-410,-290,-120), (0,0,0)).
        `safe_height` (float, optional): height at which obstacles can be avoided. Defaults to -80.
        `max_speed` (float, optional): maximum travel speed. Defaults to 250.
    
    ### Methods
    - `home`: make the robot go home
    """
    def __init__(self, 
        port: str, 
        limits: tuple[tuple[float]] = ((-410,-290,-120), (0,0,0)), 
        safe_height: float = -80, 
        max_speed: float = 250, # [mm/s] (i.e. 15,000 mm/min)
        **kwargs
    ):
        """
        Instantiate the class

        Args:
            port (str): COM port address
            limits (tuple[tuple[float]], optional): lower and upper limits of gantry. Defaults to ((-410,-290,-120), (0,0,0)).
            safe_height (float, optional): height at which obstacles can be avoided. Defaults to -80.
            max_speed (float, optional): maximum travel speed. Defaults to 250.
        """
        super().__init__(port=port, limits=limits, safe_height=safe_height, max_speed=max_speed, **kwargs)
        return
    
    @Helper.safety_measures
    def home(self) -> bool:
        """Make the robot go home"""
        self._query("$H\n")
        self.coordinates = self.home_coordinates
        print("Homed")
        return True
    
    def setSpeed(self, speed: int):
        print("`setSpeed` method not available in `Primitiv` class")
        return super().setSpeed(speed)

    # Protected method(s)
    def _connect(self, port:str, baudrate:int = 115200, timeout:Optional[int] = None):
        """
        Connection procedure for tool

        Args:
            port (str): COM port address
            baudrate (int, optional): baudrate. Defaults to 115200.
            timeout (int, optional): timeout in seconds. Defaults to 1.
        """
        super()._connect(port, baudrate, timeout)
        try:
            self.device.close()
        except Exception as e:
            if self.verbose:
                print(e)
        else:
            self.device.open()
            # Start grbl 
            self._write("\r\n\r\n")
            time.sleep(2)
            self.device.flushInput()
        return
