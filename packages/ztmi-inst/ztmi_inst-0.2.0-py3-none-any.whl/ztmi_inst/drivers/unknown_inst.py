import re
from drivers.driver import Driver
from functools import cached_property
from commands.custom_commands import command_builder


class UnknownCommands:

    def __init__(self, dev, json_file_path):
        self._custom_cmd = command_builder(dev, json_file_path)

    @property
    def custom_cmd(self):
        return self._custom_cmd


class _UnknownDriver(Driver):
    """
    Driver for unknown devices.
    """

    def __init__(self, host, port, json_file_path=None):
        super().__init__(host, port, json_file_path)
        dev = self if isinstance(self, Driver) else None
        self._commands = UnknownCommands(dev, json_file_path)
        self.write("*IDN?")
        self.__idn_string = self.read(1024, 2).decode("gb2312").rstrip('\r\n\x00')
        self._dev_name = self.model

    @property
    def json_file_path(self):
        return self._json_file_path

    @property
    def commands(self) -> UnknownCommands:
        return self._commands

    @cached_property
    def manufacturer(self):
        return self.__idn_string.split(" ")[0].strip()

    @cached_property
    def model(self):
        return self.__idn_string.split(" ")[1].strip()

    @cached_property
    def serial(self):
        return self.__idn_string.split(" ")[2].strip()

    @cached_property
    def version(self):
        _version = ''
        for item in iter(re.split(r'[,\s]', self.__idn_string)[3:]):
            _version += item.strip()
        return _version


class UnknownDevice(_UnknownDriver):
    pass
