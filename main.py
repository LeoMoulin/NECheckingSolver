from algorithm import *

if __name__ == '__main__':
    #Exemple 1
    pi = wword("v0 ; v2 v3 v5")
    g = Arena()
    g.V = {"v0": (0, None), "v1": (1, None), "v2": (1, None), "v3": (0, None), "v5": (1, None), "v6": (0, None), "v7": (0, None)}

    g.setsucc("v0", ["v1","v2"])
    g.setsucc("v1", ["v7", "v6"])
    g.setsucc("v2", ["v3"])
    g.setsucc("v3", ["v5"])
    g.setsucc("v5", ["v2"])
    g.setsucc("v6",["v6"])
    g.setsucc("v7", ["v7"])

    g.setRelPref(bucicomp(g, "v7"), 0)
    g.setRelPref(bucicomp(g, "v3"), 1)
    res, machine = is_nash_outcome(pi, g)

    print(machine[1][0].movefunc)
    print(machine[0][0].movefunc)
