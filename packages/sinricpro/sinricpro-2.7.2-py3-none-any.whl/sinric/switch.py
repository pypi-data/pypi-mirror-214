from sinric.device import Device


class SinrciProSwitch(Device):
    """
    Represents SinrciProSwitch device
    """

    def __init__(self, device_id: str):
        super().__init__(device_id)

    def on_power_state(self, cb):
        pass
    
    def send_power_state_event(state):
        pass