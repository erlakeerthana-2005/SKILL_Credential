import random
import time

class FederatedLearningSimulator:
    def __init__(self):
        # Initial Global Model - weights represent popular skill categories
        # [Web, Data, Cloud, AI, Security]
        self.global_weights = [0.2, 0.2, 0.2, 0.2, 0.2]
        self.skill_map = ["Web Development", "Data Science", "Cloud Computing", "Artificial Intelligence", "Cybersecurity"]
        self.training_round = 0

    def simulate_local_training(self, num_clients=5):
        """Simulates nodes training on local student data and sending updates."""
        local_updates = []
        for _ in range(num_clients):
            # Each client has a slight bias based on their 'local' student population
            bias = [random.uniform(-0.05, 0.1) for _ in range(5)]
            local_weights = [min(1.0, max(0.0, w + b)) for w, b in zip(self.global_weights, bias)]
            local_updates.append(local_weights)
        return local_updates

    def aggregate_updates(self, updates):
        """Standard Federated Averaging (FedAvg) implementation."""
        num_clients = len(updates)
        new_weights = [sum(dim) / num_clients for dim in zip(*updates)]
        
        # Normalize to ensure they sum to roughly 1 (priority scores)
        total = sum(new_weights)
        self.global_weights = [w / total for w in new_weights]
        self.training_round += 1
        return self.global_weights

    def run_federated_round(self):
        """Executes a full cycle of Federated Learning."""
        print(f"--- Federated Learning Round {self.training_round + 1} Starting ---")
        updates = self.simulate_local_training()
        self.aggregate_updates(updates)
        print(f"Global Model Updated: {self.global_weights}")
        return {
            "round": self.training_round,
            "weights": self.global_weights,
            "top_category": self.skill_map[self.global_weights.index(max(self.global_weights))]
        }

    def get_recommendations(self, student_skills=[]):
        """Uses the Global Model to recommend skills not already held by the student."""
        recommendations = []
        
        # Sort skills by weight in global model
        weighted_skills = sorted(
            zip(self.skill_map, self.global_weights), 
            key=lambda x: x[1], 
            reverse=True
        )

        for skill, weight in weighted_skills:
            if skill not in student_skills:
                recommendations.append({
                    "skill": skill,
                    "confidence": f"{int(weight * 100)}%",
                    "reason": "Popular among students in similar domains (FL Model)"
                })
        
        return recommendations[:3] # Return top 3 recommendations

# Global simulator instance
fl_engine = FederatedLearningSimulator()
