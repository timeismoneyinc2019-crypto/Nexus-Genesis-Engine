class ReputationManager:
    def __init__(self):
        self.reputations = {}

    def get_reputation(self, user_id):
        return self.reputations.get(user_id, 0)

    def update_reputation(self, user_id, amount):
        if user_id in self.reputations:
            self.reputations[user_id] += amount
        else:
            self.reputations[user_id] = amount

class SlashingManager:
    def __init__(self):
        self.penalties = {}

    def apply_slashing(self, user_id, penalty):
        if user_id in self.penalties:
            self.penalties[user_id] += penalty
        else:
            self.penalties[user_id] = penalty

    def get_penalty(self, user_id):
        return self.penalties.get(user_id, 0)

class StakeManager:
    def __init__(self):
        self.stakes = {}

    def stake(self, user_id, amount):
        if user_id in self.stakes:
            self.stakes[user_id] += amount
        else:
            self.stakes[user_id] = amount

    def get_stake(self, user_id):
        return self.stakes.get(user_id, 0)

class GameTheorySequencer:
    def __init__(self):
        self.actions = []

    def add_action(self, action):
        self.actions.append(action)

    def execute_actions(self):
        for action in self.actions:
            action.execute()  
