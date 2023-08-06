import yaml
from typing import Any
import json
from dataclasses import dataclass
from pathlib import Path
import requests
import urllib.parse

_client = None


class ConfigNotFound(Exception):
    pass


class InvalidConfig(Exception):
    pass


class NotInitialized(Exception):
    pass


@dataclass
class HRConfig:
    hr_dir: Path = Path.home() / ".happyrobot"
    hr_file: Path = hr_dir / "config.yaml"

    endpoint: str = "https://app.happyrobot.ai"
    hrid: str = None
    hrinfo: str = None
    token: str = None
    storage: dict = None
    backend: Any = None

    def is_valid(self) -> bool:
        return self.endpoint and self.hrid and self.hrinfo and self.token

    @classmethod
    def from_json(cls, **kwargs) -> "HRConfig":
        return cls(**kwargs)

    @classmethod
    def from_file(cls, file: str) -> "HRConfig":
        with open(file, "r") as f:
            config = yaml.load(f.read(), Loader=yaml.FullLoader)
            return cls.from_json(**config)

    @classmethod
    def update(cls, **kwargs) -> "HRConfig":
        try:
            current = cls.from_file(str(cls.hr_file)).json
            for key, value in kwargs.items():
                if value:
                    current[key] = value
            return cls.from_json(**current)
        except FileNotFoundError:
            return cls(**kwargs)

    @property
    def json(self) -> dict:
        return {
            "endpoint": self.endpoint,
            "hrid": self.hrid,
            "hrinfo": self.hrinfo,
            "token": self.token,
        }

    @property
    def yaml(self) -> str:
        return yaml.dump(self.json)

    def commit(self) -> dict:
        self.hr_dir.mkdir(parents=False, exist_ok=True)
        with self.hr_file.open("w") as f:
            f.write(self.yaml)
        return self.json


@dataclass
class Client:
    config: HRConfig = None

    def __init__(
        self,
        config_file: str = "config.yaml",
        hrid: str = None,
        hrinfo: str = None,
        token: str = None,
        endpoint: str = "https://app.happyrobot.ai",
    ):
        # Use hrid and hrinfo values if the 2 provided
        if any([hrid, hrinfo, token]):
            if all([hrid, hrinfo, token]):
                self.config = HRConfig(
                    endpoint=endpoint, hrid=hrid, hrinfo=hrinfo, token=token
                )
                return
            else:
                raise InvalidConfig(
                    "If you provide one of [hrid, hrinfo, token], you need to provide the 3 of them"
                )

        # Else, use the provided config_file if provided. If not, try ~/.happyrobot/config.yaml
        try:
            self.config = HRConfig.from_file(config_file)
        except FileNotFoundError:
            if config_file != str(HRConfig.hr_file):
                try:
                    self.config = HRConfig.from_file(str(HRConfig.hr_file))
                except FileNotFoundError:
                    raise ConfigNotFound(
                        "Happyrobot Config not found. Run 'halc login' or place a config.yaml file here."
                    )
            else:
                raise ConfigNotFound(
                    "Happyrobot Config not found. Run 'halc login' or place a config.yaml file here."
                )
        except IsADirectoryError:
            raise ConfigNotFound(f"Config file provided [{config_file}] is a directory")

        if not self.config.is_valid():
            raise InvalidConfig(
                "Happyrobot Config is invalid. Run 'halc login' or check the provided hrid, hrinfo, token or endpoint"
            )

    @property
    def base_url(self):
        return f"{self.config.endpoint}/api/v1"

    def get(self, endpoint: str, params: dict = None):
        cookies = {
            "HRID": urllib.parse.quote(self.config.hrid),
            "HRINFO": urllib.parse.quote(self.config.hrinfo),
        }
        headers = {"authorization": f"Bearer {self.config.token}"}

        res = requests.get(
            self.base_url + endpoint,
            params=params,
            headers=headers,
            cookies=cookies,
        )
        res.raise_for_status()

        return res

    def post(
        self,
        endpoint: str,
        data: Any,
        params: dict = None,
    ):
        cookies = {
            "HRID": urllib.parse.quote(self.config.hrid),
            "HRINFO": urllib.parse.quote(self.config.hrinfo),
        }
        headers = {"authorization": f"Bearer {self.config.token}"}

        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)

        res = requests.post(
            self.base_url + endpoint,
            data,
            params=params,
            headers=headers,
            cookies=cookies,
        )
        res.raise_for_status()
        return res

    def delete(self, endpoint: str, params: dict = None):
        cookies = {
            "HRID": urllib.parse.quote(self.config.hrid),
            "HRINFO": urllib.parse.quote(self.config.hrinfo),
        }
        headers = {"authorization": f"Bearer {self.config.token}"}

        res = requests.delete(
            self.base_url + endpoint,
            params=params,
            headers=headers,
            cookies=cookies,
        )
        res.raise_for_status()

        return res


def initialize(**kwargs) -> Client:
    """Initialize the session"""
    global _client
    _client = Client(**kwargs)
    return _client


def get_client() -> Client:
    if _client is None:
        raise NotInitialized(
            "Please initialize the session with halc.initialize() before using any halc functionality."
        )
    return _client


def config() -> HRConfig:
    return _client.config if _client else None
