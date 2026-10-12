# Datalogging and error snapshots

`rbs/main.py` records a full CAN trace between simulation start and stop and
creates a separate MF4 snapshot when `CAN1.Status_01.Error` changes to `1`.
The 100 ms timer sends `CAN1.HeartBeat` (CAN ID `0x101`, one data byte).
The fictional `Status_01` message is defined in `config/rbs_simple.dbc`:

- CAN ID: `0x300`, one data byte.
- `Error`: bit 0, `0` = OK and `1` = fault.

Each snapshot includes 180 seconds before and 180 seconds after the trigger.
`on_change` avoids retriggering on every received frame while the error stays
active. Clearing the error to `0` allows the next change to `1` to create a new
snapshot. Filenames include the trigger timestamp with microseconds.

Use a pyCANdo installation with pyrbs 0.3.4 or later in the 0.3 series and its
compatible pyrbs-core dependency. Configure CAN1 for your interface; the included
configuration uses a PCAN channel at 500 kbit/s and loads the example DBC.
`PyRbs()` enables the time-series database by default.

To try the trigger, start the project and send `0x300` with payload `00` followed
by `01` from another CAN node. Repeated `01` frames do not trigger new snapshots.
Send `00` then `01` again to trigger another snapshot.

Allow three minutes of incoming traffic before the error to collect the full
pre-trigger context, and leave the simulation running for three minutes after
the error. Export is queued when the post-trigger window ends; stopping earlier
exports the available window and marks it as truncated.

Trace paths are relative to the project's trace directory. Full traces appear
under `examples/can_trace_*.mf4`, and snapshots under
`examples/status_error_*.mf4`.
