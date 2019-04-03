from ConstraintSatisfactionProblem import ConstraintSatisfactionProblem

class MapColoringCSP(ConstraintSatisfactionProblem):
    def __init__(self,locations, colors):
        ConstraintSatisfactionProblem.__init__(self, len(locations),len(colors))

    def __
