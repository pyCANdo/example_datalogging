from pyrbs import PyRbs, CanMessage, CanSignal, Timer, BusLogger
from datetime import datetime as dt
import numpy as np

rbs = PyRbs(dashboard=True)

@rbs.can_message.on("CAN1.Measurement_01")
def check_measurement_01_limits(self: CanMessage):
    now = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
    for signal in self.signals:
        if "Temperature" in signal.name:
            if signal.phys > 55:
                rbs.buslog.snapshot(f"/limit_violations/overtemp_{signal.name}_{now}.mf4", pre=300, post=300)

        if "Voltage" in signal.name:
            if signal.phys < 3.0:
                rbs.buslog.snapshot(f"/limit_violations/undervolt_{signal.name}_{now}.mf4", pre=300, post=300)

            if signal.phys > 4.2:
                rbs.buslog.snapshot(f"/limit_violations/overvolt_{signal.name}_{now}.mf4", pre=300, post=300)


@rbs.can_signal.on("CAN1.Measurement_01.Temperature_01", np_array=100)
def check_Temperature_01_avg(self: CanSignal):

    avg = np.avg(self.np_array)
    if avg > 52:
        rbs.buslog.snapshot(f"/limit_violations/temp_01_avg_overtemp_{now}.mf4", pre=3600, post=300)