from algorithm import *

if __name__ == '__main__':
    #Exemple 1
    pi = wword("v0 v1 ; v2")
    g = Arena()
    g.V = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (1, None), "v4": (0, None)}

    g.setsucc("v0", ["v1", "v3"])
    g.setsucc("v1", ["v2"])
    g.setsucc("v2", ["v2"])
    g.setsucc("v3", ["v4"])
    g.setsucc("v4", ["v4"])

    g.setRelPref(bucicomp(g, "v2"), 0)
    g.setRelPref(bucicomp(g, "v4"), 1)
    is_nash_outcome(pi, g)

    #Exemple 2
    pi2 = wword("v0 ; v1 v2")
    g2 = Arena()
    g2.V = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (0, None), "v4": (0, None)}
    g2.setsucc("v0", ["v1"])
    g2.setsucc("v1", ["v2", "v3"])
    g2.setsucc("v2", ["v1"])
    g2.setsucc("v3", ["v1","v4"])
    g2.setsucc("v4", ["v4", "v3"])

    g2.setRelPref(bucicomp(g2, "v2"), 0)
    g2.setRelPref(bucicomp(g2, "v4"), 1)
    is_nash_outcome(pi2, g2)

