from tools import *

if __name__ == '__main__':
    pi = wword("v0 v3 ; v4")
    g = Game()
    g.V = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (1, None), "v4": (0, None)}

    g.setsucc("v0", ["v1", "v3"])
    g.setsucc("v1", ["v2"])
    g.setsucc("v2", ["v2"])
    g.setsucc("v3", ["v4"])
    g.setsucc("v4", ["v4"])

    a_comp = bucicomp(g, "v2")

    b_i = a_comp.productLasso(pi)

    h_i = b_i.productGame(g, "v0")

    print(h_i.E)
