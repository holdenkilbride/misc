core_rules = ["child1", "child2"]
append_rules = ["a1","a2"]
class GenerateRule():
    def __init__(self, name):
        self.name = name
        self.rules_to_create = []

class SubRule(GenerateRule):
    def __init__(self, name):
        super().__init__(self)
