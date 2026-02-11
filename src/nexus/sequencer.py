class Sequencer:
    def __init__(self):
        self.users = {}
        self.reputation_scores = {}

    def register_user(self, user_id):
        if user_id not in self.users:
            self.users[user_id] = {
                'stake': 0,
                'stake_history': [],        # Track all stake changes
                'malicious_behaviors': 0
            }
            self.reputation_scores[user_id] = 100

    def stake_tokens(self, user_id, amount):
        if user_id in self.users:
            # Save current stake before changing it
            old_stake = self.users[user_id]['stake']
            self.users[user_id]['stake_history'].append(old_stake)

            # Apply the new stake
            self.users[user_id]['stake'] += amount

    def slash_user(self, user_id):
        if user_id in self.users:
            # Save current stake before slashing
            old_stake = self.users[user_id]['stake']
            self.users[user_id]['stake_history'].append(old_stake)

            # Halve the stake
            self.users[user_id]['stake'] = old_stake * 0.5

            # Record malicious behavior
            self.users[user_id]['malicious_behaviors'] += 1

            # Update reputation
            self.update_reputation(user_id)

    def update_reputation(self, user_id):
        if self.users[user_id]['malicious_behaviors'] > 0:
            self.reputation_scores[user_id] = max(
                0,
                self.reputation_scores[user_id] - (10 * self.users[user_id]['malicious_behaviors'])
            )

    def compete(self):
        # Users with higher reputation win
        winners = sorted(self.reputation_scores.items(), key=lambda item: item[1], reverse=True)
        return [user[0] for user in winners[:3]]

    def display_scores(self):
        return self.reputation_scores

    def display_stake_history(self, user_id):
        # New helper method to see full stake history
        if user_id in self.users:
            return self.users[user_id]['stake_history']
        return []


if __name__ == '__main__':
    sequencer = Sequencer()
    sequencer.register_user('user1')
    sequencer.stake_tokens('user1', 100)
    sequencer.register_user('user2')
    sequencer.stake_tokens('user2', 200)
    sequencer.slash_user('user1')
    sequencer.stake_tokens('user1', 50)  # Added to test Landauer-friendly stake history

    print('Reputation Scores:', sequencer.display_scores())
    print('Competition Winners:', sequencer.compete())
    print('User1 Stake History:', sequencer.display_stake_history('user1'))
