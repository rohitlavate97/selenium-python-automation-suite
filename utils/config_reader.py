import yaml

class ConfigReader:

    _config = None

    @staticmethod
    def load(env):
        with open(f"config/{env}.yaml") as f:
            ConfigReader._config = yaml.safe_load(f)
        return ConfigReader._config   # ✅ THIS IS THE FIX

    @staticmethod
    def get(key):
        if ConfigReader._config is None:
            raise Exception("Config not loaded. Call ConfigReader.load(env) first.")
        return ConfigReader._config.get(key)
