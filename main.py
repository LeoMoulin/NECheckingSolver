from algorithm import *
from mealymachine import *

if __name__ == '__main__':
    #Exemple 1
    pi = wword("v0 ; v2")
    g = Arena()
    g.vertices = {"v0": (0, None), "v1": (1, None), "v2": (1, None), "v3": (0, None), "v4": (2, None),
                  "v5": (1, None)}

    g.setsucc("v0", ["v1", "v2"])
    g.setsucc("v1", ["v3", "v4"])
    g.setsucc("v2", ["v2"])
    g.setsucc("v3", ["v3", "v4"])
    g.setsucc("v4", ["v3", "v5"])
    g.setsucc("v5", ["v5"])

    g.setRelPref(buci_complemented(g, ["v3"]), 0)
    g.setRelPref(buci_complemented(g, ["v2"]), 1)
    g.setRelPref(buci_complemented(g, ["v2", "v3"]), 2)

    print(is_nash_outcome(pi, g))
