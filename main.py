from tools import *
from algorithm import *

if __name__ == '__main__':
    pi = wword("v0 v1 ; v2")
    g = Game()
    g.V = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (1, None), "v4": (0, None)}

    g.setsucc("v0", ["v1", "v3"])
    g.setsucc("v1", ["v2"])
    g.setsucc("v2", ["v2"])
    g.setsucc("v3", ["v4"])
    g.setsucc("v4", ["v4"])

    g.setRelPref(bucicomp(g, "v2"), 0)
    g.setRelPref(bucicomp(g, "v4"), 1)

    isNashOutcome(pi, g)

