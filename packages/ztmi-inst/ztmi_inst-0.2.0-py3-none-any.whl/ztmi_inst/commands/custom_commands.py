import re
import os
import json
from commands.command import CommandRead, CommandWriteNoValue


""" 使用正则表达式获取‘()’内外的字串 """
extract_args = re.compile(r'(\w+)\((.*?)\)')
""" 以不在中括号内‘,’对字串进行分组 """
remove_commas = re.compile(r',(?![^\[]*])\s*')
""" 去除中括号 """
remove_brackets = re.compile(r'^\[(.*?)]$')


class _CommandOptions:
    """ 自定义命令构建和操作类 """

    def __init__(self, dev):
        self._dev = dev

    @staticmethod
    def __build__(cmd, default_args, *args, **kwargs) -> str:
        """ 命令构建方法 """

        def __argtype_check(_arg_type, _arg_value) -> bool:
            """ 参数类型校验 """
            _type_map ={'int': int, 'float': float, 'str': str,'bool': bool}
            for _type in _arg_type:
                _type = re.sub(r'[^a-z]', '', str(_type).lower())
                if _type in _type_map and isinstance(_arg_value, _type_map[_type]):
                    return True
            return False

        try:
            __cmd = cmd + ' '
            __matches = remove_commas.split(default_args)
            for i in range(len(__matches)):

                if __matches[i] == '':
                    """当前方法不需要传递参数"""
                    break

                t_arg = re.split(r'=', __matches[i], maxsplit=1)
                t_pre_keyword, default_value = (t_arg[0], t_arg[1]) if '=' in __matches[i] else (t_arg[0], '')
                t_keyword = re.split(r':\s*', t_pre_keyword)
                valid_keyword, arg_type = (t_keyword[0], t_keyword[1]) if ':' in t_pre_keyword else (t_keyword[0], '')
                arg_type = re.split(r',\s*', remove_brackets.sub(r'\1', arg_type))
                default_value = (
                    int(default_value) if default_value.isdigit() else float(default_value) if '.' in default_value else
                    str(default_value).strip("\'\"")
                )
                default_value = True if default_value.lower() == 'true' else (
                    False if default_value.lower() == 'false' else default_value
                )

                valid_parameter = kwargs[valid_keyword] if (valid_keyword not in '' and valid_keyword in kwargs) else (
                    args[i] if i < len(args) else default_value
                )

                """ 调用的实参可能为‘None’ """
                valid_parameter = default_value if valid_parameter is None else valid_parameter

                if default_value == '' and valid_parameter == '':
                    """ 参数在json中没有默认值，参数必选 """
                    print(f"\033[33mThe command: '{cmd}' parameters: '{valid_keyword}' is required\033[0m")
                    return ''

                if len(arg_type) > 1 or str(arg_type[0]).strip('\'\"') != '':
                    """ 参数类型json格式有效，启用参数校验 """
                    if not __argtype_check(arg_type, valid_parameter):
                        print(f"\033[33mThe command: '{cmd}' parameters: '{valid_keyword}' type error\033[0m")
                        print(f"\033[33mParameter type only supported {arg_type}\033[0m")
                        return ''

                """ 调用的实参为布尔型时，转换为整型 """
                valid_parameter = int(valid_parameter) if isinstance(valid_parameter, bool) else valid_parameter

                if (cmd_index:= '<' + valid_keyword + '>') in __cmd:
                    __cmd = __cmd.replace(cmd_index, '{}').format(valid_parameter)
                else:
                    __cmd += f'{valid_parameter},'

            if ',,' in __cmd:
                """ 中间可选参数没有默认值 """
                __cmd = __cmd.replace(',,', ',')
            if ' ,' in __cmd:
                """ 第一个可选参数没有默认值 """
                __cmd = __cmd.replace(' ,', ' ')

            return __cmd.rstrip(' ,:')

        except Exception as e:
            print(f"\033[91mError in command build: {e}\033[0m")
            return ''

    def __syntax__(self, cmd):
        return CommandRead(self._dev, cmd).syntax

    def __read__(self, cmd):
        return CommandRead(self._dev, cmd).read() if cmd not in '' else None

    def __write__(self, cmd):
        return CommandWriteNoValue(self._dev, cmd).write() if cmd not in '' else None


def _create_command_builder(name, cmd, default_args):

    def method(self, *args, **kwargs):
        return_syntax = bool(kwargs.pop('return_syntax')) if 'return_syntax' in kwargs else False
        _cmd = self.__build__(cmd, default_args, *args, **kwargs)
        return self.__syntax__(_cmd) if return_syntax else (
            self.__read__(_cmd) if '?' in _cmd else self.__write__(_cmd)
        )

    method.__name__ = name
    return method


def command_builder(dev, json_file_path):
    """ 可供外部调用的命令方法构建函数 """

    if not os.path.isfile(json_file_path):
        print(f"Error: The json file '{json_file_path}' does not exist.")
        return None
    else:
        try:
            if not os.path.abspath(json_file_path).startswith(os.getcwd()):
                raise ValueError(f"Invalid file path: {json_file_path}")

            with open(json_file_path, 'r') as f:
                data_json = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: The json file '{json_file_path}' is not a valid JSON file.")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None

    _cmd_method_dict = {}

    commands_dict = data_json['commands']
    for key in list(commands_dict):
        __matches = extract_args.search(key)
        _cmd_method_name = __matches.group(1)
        _cmd_method_args = __matches.group(2)
        _cmd_body = commands_dict[key]

        if _cmd_method_name not in _cmd_method_dict:
            _cmd_method_dict[_cmd_method_name] = _create_command_builder(
                _cmd_method_name, _cmd_body, _cmd_method_args
            )
        else:
            print(f"\033[33mThe command: '{_cmd_method_name}' has been defined\033[0m")

    return type('CustomCmdClass', (_CommandOptions, ), _cmd_method_dict)(dev)
