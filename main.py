from algorithm import *
from mealymachine import *

if __name__ == '__main__':
    #Exemple 1
    pi = wword("v0 v1 v2 v3 v7;v5 v4")
    g = Arena()
    g.vertices = {"v0": (0, None), "v1": (1, None), "v2": (3, None), "v3": (2, None), "v4": (2, None), "v5": (1, None), "v6": (3, None),"v7": (0, None),"v8": (3, None),"v9": (1, None)}

    g.setsucc("v0", ["v1"])
    g.setsucc("v1", ["v2", "v3"])
    g.setsucc("v2", ["v3", "v9"])
    g.setsucc("v3", ["v7"])
    g.setsucc("v4", ["v0", "v5"])
    g.setsucc("v5",["v4", "v6"])
    g.setsucc("v6", ["v6", "v7"])
    g.setsucc("v7", ["v5", "v8"])
    g.setsucc("v8", ["v9"])
    g.setsucc("v9", ["v9"])

    g.setRelPref(buci_complemented(g, ["v7"]), 0)
    g.setRelPref(buci_complemented(g, ["v6"]), 1)
    g.setRelPref(buci_complemented(g, ["v2"]), 2)
    g.setRelPref(buci_complemented(g, ["v9"]), 3)
    print(is_nash_outcome(pi, g))

    #On va modifier la super machine pour faire dévier le joueur 0 en v1
    tau0 = mealy_machine([("v0", "u0"), "m1"], ("v0", "u0"), {}, {})
    tau0.updatefunc = {(("v0", "u0"), "v0"): "m1"}
    tau0.movefunc = {(("v0", "u0"), "v0"): "v1"}

    #machine[0][0] = tau0
    #simulation(g, machine, 10)
