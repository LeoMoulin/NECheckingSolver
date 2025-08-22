from algorithm import *
from mealymachine import *

if __name__ == '__main__':
    #Exemple 1
    pi = wword("v0 ; v2")
    g = Arena()
    g.vertices = {"v0": (0, None), "v1": (1, None), "v2": (1, None), "v3": (0, None), "v4": (2, None), "v5": (1, None)}

    g.setsucc("v0", ["v1","v2"])
    g.setsucc("v1", ["v3", "v4"])
    g.setsucc("v2", ["v2"])
    g.setsucc("v3", ["v3", "v4"])
    g.setsucc("v4", ["v3", "v5"])
    g.setsucc("v5",["v5"])

    g.setRelPref(bucicomp(g, ["v3"]), 0)
    g.setRelPref(bucicomp(g, ["v2"]), 1)
    g.setRelPref(bucicomp(g, ["v2", "v3"]), 2)
    res, machine = is_nash_outcome(pi, g)

    #On va modifier la super machine pour faire dévier le joueur 0 en v1
    tau0 = mealy_machine([("v0", "u0"), "m1"], ("v0", "u0"), {}, {})
    tau0.updatefunc = {(("v0", "u0"), "v0"): "m1"}
    tau0.movefunc = {(("v0", "u0"), "v0"): "v1"}

    machine[0][0] = tau0
    simulation(g, machine, 10)
