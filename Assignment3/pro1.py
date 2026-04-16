class Simple_Reflex_Agent:
    def __init__(self,environment,start_location):
        self.environment=environment
        self.location=start_location
        self.performance_cost=0
        #rule table
        self.rule_table={
            ("A", "Dirty"): "remove",
            ("A", "Clean"): "move_to_B",
            ("B", "Dirty"): "remove",
            ("B", "Clean"): "move_to_C",
            ("C", "Dirty"): "remove",
            ("C", "Clean"): "move_to_A"
        }

    # this function tells the agent where it is and what is the current state of the room
    def perceive(self):
           current_location=self.location
           current_status=self.environment[current_location]
           percept=(current_location,current_status)
           return percept
    
    def act(self,percept):
         return self.rule_table[percept]
    
    def update_environment(self,action):
         #every action has a cost 1
         self.performance_cost+=1
         if action=="remove":
              self.environment[self.location]="Clean"
         elif action=="move_to_A":
              self.location="A"
         elif action=="move_to_B":
              self.location="B"
         elif action=="move_to_C":
              self.location="C"


#simulation
environment = {
    "A": "Dirty",
    "B": "Dirty",
    "C": "Clean"
}

agent=Simple_Reflex_Agent(environment,"A")
print("Initial Environment:", environment)
print("\nSimulation Output:")
print("No.\tPercept\t\tAction\t\tNew Location")

step = 1
for i in range(6):
    percept = agent.perceive()
    action = agent.act(percept)
    agent.update_environment(action)
    print(f"{step}.\t {percept}\t{action}\t\t{agent.location}")
    step += 1

print("\nFinal Environment:", environment)
print("Total performance Cost:",agent.performance_cost)


