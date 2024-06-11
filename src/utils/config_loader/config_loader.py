import os
import yaml
from pathlib import Path
from src.utils.config_loader.models import ConfigModel
from exceptions.exceptions import ConfigLoadException


class Config(ConfigModel):

    @classmethod
    def from_yaml(self, file: str):
        file = Path(file)
        if not os.path.exists(str(file)):
            raise ConfigLoadException('Некорректный путь к yaml файлу.\n'
                                      'Пожалуйста, убедитесь что файл существует.')

        with open(file, encoding='utf-8') as f:
            config = yaml.safe_load(f)

        return self.parse_obj(config)
