import logging
from redteam_ai.redteam_ai import RedTeamAI
from rd_team.feature_manager import FeatureManager
from cybersecurity_ai.cybersecurity_ai import CybersecurityAI

class SystemInterface:
    def __init__(self):
        self.state = {"key1": "value1", "key2": "value2"}
        self.user_roles = {}
        self.request_log = []

    def receive_request(self, request_type):
        self.request_log.append(request_type)

    def get_log_stream(self):
        logs = []
        for req in self.request_log:
            logs.append(f"Request: {req}")
        for key, val in self.state.items():
            logs.append(f"State {key}: {val}")
        for user, role in self.user_roles.items():
            logs.append(f"User {user} role: {role}")
        return logs

def main():
    logging.basicConfig(level=logging.DEBUG)
    system_interface = SystemInterface()

    feature_manager = FeatureManager()

    redteam_ai = RedTeamAI(system_interface)
    if feature_manager.is_feature_enabled("enable_redteam_ai"):
        redteam_ai.simulate_attack()

    cybersecurity_ai = CybersecurityAI(system_interface.get_log_stream())
    cybersecurity_ai.analyze()

if __name__ == "__main__":
    main()
