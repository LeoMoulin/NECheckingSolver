import unittest

from algorithm import is_nash_outcome
from games import *
from automatas import *
from mealymachine import mealy_machine

"""
    Implémente les tests unitaires des différentes classes
"""

class TestGames(unittest.TestCase):
    def test_coalitionalsubgame(self):
        arena = Arena()
        arena.vertices = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (1, None), "v4": (0, None), "v5":(1, None)}

        arena.setsucc("v0", ["v1"])
        arena.setsucc("v1", ["v2"])
        arena.setsucc("v2", ["v3"])
        arena.setsucc("v3", ["v4"])
        arena.setsucc("v4", ["v5"])
        arena.setsucc("v5", ["v2"])

        #Le joueur est le joueur 1 la coalition est le joueur 0
        coal = coalitional_game(arena, 1)

        self.assertEqual(["v0", "v2", "v4"], [x[0] for x in coal.V0])
        self.assertEqual(["v1", "v3", "v5"], [x[0] for x in coal.V1])

        subgame = coal.subgame([("v2",0), ("v3",1), ("v4",0), ("v5",1)])

        self.assertEqual([("v2",0), ("v3",1), ("v4",0), ("v5",1)], [x for x in subgame.V0 + subgame.V1])

        self.assertEqual(["v3"], subgame.edges["v2"])
        self.assertEqual(["v4"], subgame.edges["v3"])
        self.assertEqual(["v5"], subgame.edges["v4"])
        self.assertEqual(["v2"], subgame.edges["v5"])


class TestAutomatas(unittest.TestCase):
    def test_wword(self):
        w = wword("v0 v1 v2; v3")
        self.assertEqual(["v0","v1","v2"], w.finiteseg)
        self.assertEqual(["v3"], w.infiniteseg)

        l = ["v0", "v1", "v2", "v3", "v3", "v3", "v3"]

        for i in range(len(l)):
            self.assertEqual(l[i], w.getElementAt(i))

    def test_dpa(self):
        aut = DPA(["q0", "q1", "q2", "q3"], ["a","b","c"], {}, "q0", {"q0":1,"q1":2,"q2":6, "q3":7})

        aut.addtransition("q0", "q1", "a")
        aut.addtransition("q1", "q2", "b")
        aut.addtransition("q2", "q1", "a")
        aut.addtransition("q1", "q3", "c")
        aut.addtransition("q3", "q1", "a")

        w1 = wword("a ; b a")
        w2 = wword("a ; c a")
        w3 = wword("a ; b a c a")

        self.assertEqual(True, aut.run(w1))
        self.assertEqual(False, aut.run(w2))
        self.assertEqual(False, aut.run(w3))


#Teste l'algo général
class TestAlgorithm(unittest.TestCase):
    def test_algo(self):
        # Exemple 1
        pi = wword("v0 v3 ; v4")
        g = Arena()
        g.vertices = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (1, None), "v4": (0, None)}

        g.setsucc("v0", ["v1", "v3"])
        g.setsucc("v1", ["v2"])
        g.setsucc("v2", ["v2"])
        g.setsucc("v3", ["v4"])
        g.setsucc("v4", ["v4"])

        g.setRelPref(bucicomp(g, ["v2"]), 0)
        g.setRelPref(bucicomp(g, ["v4"]), 1)
        self.assertEqual(False, is_nash_outcome(pi, g))

        # Exemple 2
        pi2 = wword("v0 ; v1 v2")
        g2 = Arena()
        g2.vertices = {"v0": (0, None), "v1": (1, None), "v2": (0, None), "v3": (0, None), "v4": (0, None)}
        g2.setsucc("v0", ["v1"])
        g2.setsucc("v1", ["v2", "v3"])
        g2.setsucc("v2", ["v1"])
        g2.setsucc("v3", ["v1", "v4"])
        g2.setsucc("v4", ["v4", "v3"])

        g2.setRelPref(bucicomp(g2, ["v2"]), 0)
        g2.setRelPref(bucicomp(g2, ["v4"]), 1)
        self.assertEqual(True,is_nash_outcome(pi2, g2)[0])

        pi = wword("v0 ; v2 v3 v5")
        g = Arena()
        g.vertices = {"v0": (0, None), "v1": (1, None), "v2": (1, None), "v3": (0, None), "v5": (1, None), "v6": (0, None),
               "v7": (0, None)}

        g.setsucc("v0", ["v1", "v2"])
        g.setsucc("v1", ["v7", "v6"])
        g.setsucc("v2", ["v3"])
        g.setsucc("v3", ["v5"])
        g.setsucc("v5", ["v2"])
        g.setsucc("v6", ["v6"])
        g.setsucc("v7", ["v7"])

        g.setRelPref(bucicomp(g, ["v7"]), 0)
        g.setRelPref(bucicomp(g, ["v3"]), 1)
        self.assertEqual(True, is_nash_outcome(pi, g)[0])

        # On va modifier la super machine pour faire dévier le joueur 0 en v1
        tau0 = mealy_machine([("v0", "u0"), "m1"], ("v0", "u0"), {}, {})
        tau0.updatefunc = {(("v0", "u0"), "v0"): "m1"}
        tau0.movefunc = {(("v0", "u0"), "v0"): "v1"}


