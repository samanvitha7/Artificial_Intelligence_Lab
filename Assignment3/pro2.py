
class Level_Crossing_Agent:

    def __init__(self):
        pass

    def get_action(self, track, obstacle, emergency):
        """
        track: 0/1  -> Train detected or not
        obstacle: 0/1 -> Vehicle stuck or not
        emergency: 0/1 -> Manual emergency lever
        """

        # RULE 1: Emergency Override
        if emergency == 1:
            return {
                "Gate": "Lower",
                "Siren": "ON",
                "TrainSignal": "RED",
                "Reason": "Emergency Lever Activated"
            }

        # RULE 2: Obstacle Detected
        if obstacle == 1:
            return {
                "Gate": "Lower",
                "Siren": "ON",
                "TrainSignal": "RED",
                "Reason": "Obstacle Detected"
            }

        # RULE 3: Train Approaching
        if track == 1:
            return {
                "Gate": "Lower",
                "Siren": "ON",
                "TrainSignal": "RED",
                "Reason": "Train Approaching"
            }

        # RULE 4: Safe Condition
        return {
            "Gate": "Raise",
            "Siren": "OFF",
            "TrainSignal": "GREEN",
            "Reason": "Safe Condition"
        }



# SIMULATION


agent = Level_Crossing_Agent()

# Test all combinations (T, O, E)
test_inputs = [
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (1, 1, 0),
    (0, 0, 1),
    (1, 0, 1),
    (0, 1, 1),
    (1, 1, 1)
]

print("T O E  ->  Gate | Siren | Train Signal | Reason")
print("--------------------------------------------------------")

for t, o, e in test_inputs:
    action = agent.get_action(t, o, e)
    print(f"{t} {o} {e}  ->  {action['Gate']} | {action['Siren']} | {action['TrainSignal']} | {action['Reason']}")
