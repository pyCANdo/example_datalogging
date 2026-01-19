from pyrbs import PyRbs, CanMessage, Timer, BusLogger

rbs = PyRbs(dashboard=True)

full_trace: BusLogger = rbs.buslog.add("full_trace", "/examples/can_trace.mf4")

timer_100ms: Timer = rbs.timer.add("timer_100ms", 0.1, active_on_start=True )
msg_control_01: CanMessage = rbs.can_message.get("CAN1.Control_01")


@rbs.on_start()
def on_start():
    full_trace.start()


@rbs.on_stop()
def on_stop():
    full_trace.stop()


@rbs.timer.on("timer_100ms")
def on_timer_100ms(self: Timer):
    msg_control_01.send()
