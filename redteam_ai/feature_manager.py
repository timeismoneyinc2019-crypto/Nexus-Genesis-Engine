import json
import threading

class FeatureManager:
    def __init__(self, config_path='config.json'):
        self.config_path = config_path
        self._load_config()
        self.lock = threading.Lock()

    def _load_config(self):
        with open(self.config_path, 'r') as f:
            self.config = json.load(f)
        self.features = self.config.get("rd_team", {}).get("feature_flags", {})

    def is_feature_enabled(self, feature_name):
        with self.lock:
            return self.features.get(feature_name, False)

    def enable_feature(self, feature_name):
        with self.lock:
            self.features[feature_name] = True
            self._save_config()

    def disable_feature(self, feature_name):
        with self.lock:
            self.features[feature_name] = False
            self._save_config()

    def _save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=4)