#  ___         _                          _   _         _    
# |_ _|_ _  __| |_ _ _ _  _ _ __  ___ _ _| |_| |   __ _| |__   InstrumentLab
#  | || ' \(_-<  _| '_| || | '  \/ -_) ' \  _| |__/ _` | '_ \  
# |___|_||_/__/\__|_|  \_,_|_|_|_\___|_||_\__|____\__,_|_.__/  (C) 2024  Marc Van Riet et al.
#
# Licensed under the Apache License Version 2.0. See http://www.apache.org/licenses/LICENSE-2.0

from ..base.psu.simple_psu import SimplePsu
from .korad_slow_serial import KoradSlowSerial

class KoradSimplePSU(SimplePsu):
    ''' Base class to derive instruments from with a given voltage/current range.
    '''

    def __init__(self, name, max_voltage, max_current, **kwargs):
        super().__init__(name, **kwargs)

        self.link = KoradSlowSerial(self)

        self.max_voltage = max_voltage
        self.max_current = max_current
    
    def _set_enabled(self, value:bool):
        with self.link as lnk:
            lnk.write("OUT1" if value else "OUT0")

    # TODO: implement _get_enabled()

    def _set_current(self, value:float):
        value = max(0,min(value,self.max_current))

        with self.link as lnk:
            lnk.write(f"ISET1:{value:05.3f}")

    def _get_current(self) -> float:
        with self.link as lnk:
            return lnk.query_float("ISET1?")

    def _read_current(self) -> float:
        with self.link as lnk:
            return lnk.query_float("IOUT1?") 

    def _set_voltage(self, value:float):
        value = max(0,min(value,self.max_voltage))
            
        with self.link as lnk:
            lnk.write(f"VSET1{value:05.2f}")

    def _get_voltage(self) -> float:
        with self.link as lnk:
            return lnk.query_float("VSET1?")

    def _read_voltage(self) -> float:
        with self.link as lnk:
            return lnk.query_float("VOUT1?")


class KA3005P(KoradSimplePSU):

    def __init__(self, name, **kwargs):
        super().__init__(name, 30, 5, **kwargs)

class KA6003P(KoradSimplePSU):

    def __init__(self, name, **kwargs):
        super().__init__(name, 60, 3, **kwargs)

