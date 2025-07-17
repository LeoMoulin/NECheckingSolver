from tools import *


def notTnotT(elem, goal):
    return elem[0] != goal and elem[1] != goal


def notTbutT(elem, goal):
    return elem[0] != goal and elem[1] == goal


def TbutnotT(elem, goal):
    return elem[0] == goal and elem[1] != goal


def Tandany(elem, goal):
    return elem[0] == goal


if __name__ == '__main__':
    test = wword("v0 v3 ; v4")

    BuchiTest = DPA(["u0", "u1", "u2"], [], {}, "u0", {"u0": 2, "u1": 4, "u2": 3})

    gamestates = ["v0", "v1", "v2", "v3", "v4"]

    g = Game()
    g.V = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (1, None), "v4": (0, None)}

    g.setsucc("v0", ["v1", "v3"])
    g.setsucc("v1", ["v2"])
    g.setsucc("v2", ["v2"])
    g.setsucc("v3", ["v4"])
    g.setsucc("v4", ["v4"])

    BuchiTest.addtransitionset("u0", "u0", notTnotT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u0", "u1", Tandany, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u0", "u2", notTbutT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u1", "u1", Tandany, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u1", "u0", notTnotT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u1", "u2", notTbutT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u2", "u2", notTbutT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u2", "u1", Tandany, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u2", "u0", notTnotT, "v2", cartesianProduct(gamestates, gamestates))

    B_i = BuchiTest.productLasso(test)

    H_i = B_i.productGame(g, "v0")

    print(H_i.E)
    print(H_i.V)