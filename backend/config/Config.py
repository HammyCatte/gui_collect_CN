import os
import json
from dataclasses import asdict

from .structs import ConfigData
from .exceptions import InvalidConfigData


class Config():
    __instance = None

    def __init__(self, config_directory:str = '.'):
        if Config.__instance != None:
            raise Exception('配置已创建。')
        Config.__instance = self

        print('初始化配置')

        self.temp_data = {}
        self._config_directory = config_directory
        self._config_filename = 'config.json'
        self._config_filepath = os.path.join(config_directory, self._config_filename)

        if not self._check_config_exists():
            self._create_config()
            print('\t- 创建配置：', self._config_filepath)
        else:
            print('\t- 读取配置：', self._config_filepath)

        self._load_config()
        print('\t- 加载完成')
    

    @staticmethod
    def get_instance():
        if Config.__instance == None:
            raise Exception('配置尚未初始化。')
        return Config.__instance

    def _check_config_exists(self):
        files = os.listdir(self._config_directory)
        return self._config_filename in files

    def _create_config(self):
        with open(self._config_filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(ConfigData()), f, indent=4)

    def _load_config(self) -> dict:
        with open(self._config_filepath, 'r', encoding='utf-8') as f:
            try:
                d = json.load(f)
                ConfigData.validate_config_data(d)
                self.data = ConfigData(**d)
            except json.decoder.JSONDecodeError:
                print('\tconfig：JSON 解码错误。config.json 不是有效的 json 文件。')
                self.prompt_config_refresh()
            except InvalidConfigData:
                pass

    def save_config(self):
        with open(self._config_filepath, 'w', encoding='utf-8') as f:
            json.dump(asdict(self.data), f, indent=4)

    def prompt_config_refresh(self):
        ans = ''
        while ans not in ['y', 'n']:
            ans = input('\t是否使用默认配置覆盖 config.json？ (y/n): ').lower()

        if ans == 'y':
            self._create_config()
            return self._load_config()
        else:
            exit('\tconfig.json 配置无效，即将退出。')
