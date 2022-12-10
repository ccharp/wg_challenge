from pydantic import BaseSettings

import os
from typing import Any, List


class Settings(BaseSettings):
    app_name: str = "File Browser"
    active_path: str

    class Config:
        # TODO: couldn't get this working in time. Ideally, we convert path sugar to
        #       a concrete path when reading in the configuration.
        # @classmethod
        # def parse_env_file(cls, field_name: str, raw_value: str) -> Any:
        #     if field_name == "active_path":
        #         return os.path.realpath(raw_value)
        #     return super().parse_env_file(field_name, raw_value)

        env_file = ".env"