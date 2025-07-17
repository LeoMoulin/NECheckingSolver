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

    BuchiTest = DPA(["u0", "u1", "u2"], [], {}, "u0", {"u0": 2, "u1": 3, "u2": 4})

    gamestates = ["v0", "v1", "v2", "v3", "v4"]
    BuchiTest.addtransitionset("u0", "u0", notTnotT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u0", "u1", Tandany, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u0", "u2", notTbutT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u1", "u1", Tandany, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u1", "u0", notTnotT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u1", "u2", notTbutT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u2", "u2", notTbutT, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u2", "u1", Tandany, "v2", cartesianProduct(gamestates, gamestates))
    BuchiTest.addtransitionset("u2", "u0", notTnotT, "v2", cartesianProduct(gamestates, gamestates))

    t = BuchiTest.product(test)
    print(t.states)

    print([x for x in t.transit.items() if x[0][0] == ("v4", "u2")])
