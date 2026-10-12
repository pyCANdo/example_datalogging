from pyrbs import PyRbs, CanMessage, CanSignal, Timer, BusLogger
from datetime import datetime as dt

now = dt.now().strftime('%Y-%m-%d_%H-%M-%S')
rbs = PyRbs()

full_trace: BusLogger = rbs.buslog.add("full_trace", f"examples/can_trace_{now}.mf4")
timer_100ms: Timer = rbs.timer.add("timer_100ms", 0.1, active_on_start=True)
msg_heartbeat: CanMessage = rbs.can_message.get("CAN1.HeartBeat")


@rbs.on_start()
def on_start():
    full_trace.start()


@rbs.on_stop()
def on_stop():
    full_trace.stop()


@rbs.timer.on("timer_100ms")
def on_timer_100ms(self: Timer):
    msg_heartbeat.send()


# Create a snapshot when Status_01.Error changes to 1.
@rbs.can_signal.on_change("CAN1.Status_01.Error")
def on_status_error(self: CanSignal):
    if self.raw == 1:
        trigger_time = dt.now().strftime('%Y-%m-%d_%H-%M-%S_%f')
        rbs.buslog.snapshot(
            "status_error",
            f"examples/status_error_{trigger_time}.mf4",
            pre_trigger=180,  # Three minutes before the error.
            post_trigger=180,  # Three minutes after the error.
        )
