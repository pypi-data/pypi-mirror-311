# import json
# from struct import *
# import re
import sys
import socket
from typing import *
from abc import abstractmethod, ABC
from functools import cached_property


class Driver(ABC):
    
    def __init__(self, host, port, json_file_path=None):
        # print('Driver init')
        self.__addr = (host, port)
        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._dev_number: int = -1
        self._dev_name: str = ""
        self._is_open = True
        self._json_file_path = json_file_path
        self._commands: Any = NotImplemented
        try:
            self._s.connect(self.__addr)
            self._s.settimeout(0.2)
        except socket.error:
            print('\033[91mTCP Connection failed\033[0m')
            sys.exit(1)

    def close(self) -> None:
        if self._is_open:
            self._s.close()
        self._is_open = False

    def open(self) -> bool:
        if not self._is_open:
            self._s.connect(self.__addr)
            self._is_open = True
        return self._is_open

    def write(self, cmd):
        if cmd[len(cmd) - 1] != '\n':
            cmd = cmd + '\n'
        self._s.send(cmd.encode('gb2312'))

    def read(self, size, t_out):
        self._s.settimeout(t_out)
        try:
            while True:
                info = self._s.recv(size)
                if b'\n' or b'\x00' in info:
                    break
        except socket.timeout:
            # 返回查询错误
            info = b'timeout error\n'
        self._s.settimeout(0)
        return info

    @cached_property
    @abstractmethod
    def manufacturer(self):
        """返回仪器制造商，需具体仪器类实现"""
        pass

    @cached_property
    @abstractmethod
    def model(self):
        """返回仪器型号，需具体仪器类实现"""
        pass

    @cached_property
    @abstractmethod
    def version(self):
        """返回仪器版本，需具体仪器类实现"""
        pass

    @cached_property
    @abstractmethod
    def serial(self):
        """返回仪器序列号，需具体仪器类实现"""
        pass

    @property
    def dev_name(self):
        return self._dev_name

    @property
    def dev_number(self):
        return self._dev_number

    @property
    def is_open(self):
        return self._is_open
