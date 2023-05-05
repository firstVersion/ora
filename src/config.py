import json
import os
import re

err_validation_failed: str = "Validation Error: invalid pattern. Need pattern: {}"
err_undefined_key: str = "Undefined key."


class ConfigValue:
    def __init__(self, key: str, default: str = "", pattern: str = r"^.*$"):
        self.key = key
        self.default = default
        self.pattern = pattern
        self.validate(self.default)

    def validate(self, value) -> bool:
        assert re.match(self.pattern, value) is not None, err_validation_failed.format(self.pattern)
        return True


class Config:
    def __init__(self, config_path: str = os.path.expanduser("~/.config"), default: list[ConfigValue] = []):
        self.__config_path: str = config_path
        self.__default: list[ConfigValue] = default
        self.__values: dict = {}

        os.makedirs(config_path, mode=0o777, exist_ok=True)

        if not os.path.isfile(f"{config_path}/config.json"):
            self.__create_config()
        self.__load_config()

    def __create_config(self):
        with open(f"{self.__config_path}/config.json", "w", encoding="utf-8") as f:
            json.dump(
                {d.key: d.default for d in self.__default},
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )

    def __update_config(self):
        with open(f"{self.__config_path}/config.json", "w", encoding="utf-8") as f:
            json.dump(
                self.__values,
                f,
                ensure_ascii=False,
                indent=4,
                sort_keys=True,
                separators=(",", ": "),
            )

    def __load_config(self):
        result: dict = {}
        with open(f"{self.__config_path}/config.json", "r", encoding="utf-8") as f:
            try:
                result = json.load(f)
                for d in self.__default:
                    try:
                        d.validate(result.get(d.key, d.default))
                        self.__values[d.key] = result.get(d.key, d.default)
                    except AssertionError as e:
                        print(e)
            except json.decoder.JSONDecodeError:
                os.rename(f"{self.__config_path}/config.json", f"{self.__config_path}/config.json.backup")
                self.__create_config()

    def get(self, key: str):
        assert key in self.__values.keys(), err_undefined_key
        return self.__values[key]

    def set(self, key: str, value: str):
        assert key in self.__values.keys(), err_undefined_key
        if len([d for d in self.__default if d.key == key and d.validate(value)]) == 1:
            self.__values[key] = value
            self.__update_config()

    def show(self):
        return self.__values
