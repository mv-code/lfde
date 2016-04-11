class UnmountableException(Exception):
    def __init__(self, unmountable_devices):
        self.unmountable_devices = unmountable_devices

        device_list = ""
        for unmountable_device in self.unmountable_devices:
            device_list += unmountable_device.device + "\n"

        self.description = "Error unmounting devices:\n" + device_list


