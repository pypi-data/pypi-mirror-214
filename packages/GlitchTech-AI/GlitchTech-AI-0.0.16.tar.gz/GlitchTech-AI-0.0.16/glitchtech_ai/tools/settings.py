import os
import platform

from configparser import ConfigParser


class ManageSettings:
    def __init__(self, project_name: str):
        self.project_name = project_name

        self.project_path = self._determine_project_path()
        self.settings_file_name = "settings.conf"

        self.settings_file_path = os.path.join(self.project_path, self.settings_file_name)

    def _determine_project_path(self):
        if platform.system() == "Linux":
            return f"{os.environ['HOME']}/.cache/{self.project_name}"

        if platform.system() == "Windows":
            return f"{os.environ['LOCALAPPDATA']}/{self.project_name}"

    def settings_exist(self) -> bool:
        return os.path.exists(self.settings_file_path)

    def store_setting(self, key: str, value: str = None):
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)

        config = ConfigParser()
        config.read(self.settings_file_path)
        config.add_section('main')

        if key and value:
            config.set('main', key, value)

        with open(self.settings_file_path, 'w') as f:
            config.write(f)

    def retrieve_setting(self, key):
        config = ConfigParser()
        config.read(self.settings_file_path)
        return config.get('main', key)


if __name__ == '__main__':
    ls = ManageSettings(project_name="PersonalProject")
    ls.store_setting(key="open_ai_token", value="PRIVATE")
