from algorithm import *
from mealymachine import *

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

    #On va modifier la super machine pour faire dévier le joueur 0 en v1
    tau0 = mealy_machine([("v0", "u0"), "m1"], ("v0", "u0"), {},{})
    tau0.updatefunc = {(("v0", "u0"), "v0"): "m1", ("m1", "v1"): "m2", ("m2", "v7"): "m2", ("m2", "v6"): "m2"}
    tau0.movefunc = {(("v0", "u0"), "v0"): "v1", ("m1", "v1"): "*", ("m2", "v7"): "v7", ("m2", "v6"): "v6"}

    #machine[0][0] = tau0
    simulation(g, machine, 10)
