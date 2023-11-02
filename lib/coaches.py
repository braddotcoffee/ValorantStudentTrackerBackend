import json
from os import listdir, path, lstat
import logging

LOG = logging.getLogger(__name__)

COACHES_PATH = "./coaches"


class CoachService:
    def __init__(self):
        self.edit_times: dict[str, float] = dict()
        self._load_coaches()

    @staticmethod
    def _get_configured_coaches():
        return list(map(lambda filename: filename[:-5].lower(), listdir(COACHES_PATH)))

    @staticmethod
    def _get_coach_file(coach_name: str) -> str:
        lowered_name = coach_name.lower()
        return f"{COACHES_PATH}/{lowered_name}.json"

    @staticmethod
    def _read_config_files(valid_coaches: list[str]):
        new_coach_config = dict()
        for coach in valid_coaches:
            new_coach_config[coach] = CoachService._read_config_file(coach)
        return new_coach_config

    @staticmethod
    def _read_config_file(coach_name: str):
        with open(CoachService._get_coach_file(coach_name), "r") as coach_file:
            content = coach_file.read()
            return json.loads(content)

    def _get_loaded_coaches(self):
        return self.coach_config.keys()

    def _delete_coach(self, coach_name: str):
        self.edit_times.pop(coach_name, None)
        self.coach_config.pop(coach_name, None)

    def _should_update(self, coach_name: str) -> bool:
        coach_file = CoachService._get_coach_file(coach_name)
        coach_file_exists = path.exists(coach_file)

        if coach_name not in self.edit_times and coach_file_exists:
            return True

        if not coach_file_exists:
            self._delete_coach(coach_name)
            return False

        edit_time = lstat(coach_file).st_mtime
        return self.edit_times[coach_name] == edit_time

    def _get_coach_names(self):
        return list(map(lambda value: value["name"], self.coach_config.values()))

    def _load_coaches(self):
        valid_coaches = CoachService._get_configured_coaches()
        self.coach_config = CoachService._read_config_files(valid_coaches)
        self.coach_names = self._get_coach_names()

    def list_coaches(self) -> list[str]:
        coaches = set(CoachService._get_configured_coaches())
        coaches = coaches.union(self._get_loaded_coaches())
        for coach in coaches:
            if self._should_update(coach):
                coach_config = CoachService._read_config_file(coach)
                self.coach_config[coach] = coach_config
        self.coach_names = sorted(self._get_coach_names())
        return self.coach_names

    def get_coach(self, name: str) -> dict:
        lower_name = name.lower()
        if self._should_update(name):
            self.coach_config[name] = CoachService._read_config_file(name)
        if lower_name not in self.coach_config:
            return False, {}

        return True, self.coach_config[lower_name]
