# Représente un mot infini de la forme v..(w..)^w
# Par exemple v0v1(v2v3)^w serait encodé de la forme v0 v1;v2 v3
import math
from collections import defaultdict


class wword:
    def __init__(self, word: str = ""):
        self.finiteseg = []
        self.infiniteseg = []
        if word != "":
            parts = word.split(";", 1)
            self.finiteseg = parts[0].split(" ")
            self.infiniteseg = parts[1].split(" ")

            # Petite sécu en cas d'erreur sur les espaces
            self.finiteseg = [self.finiteseg[i] for i in range(0, len(self.finiteseg)) if self.finiteseg[i] != ""]
            self.infiniteseg = [self.infiniteseg[i] for i in range(0, len(self.infiniteseg)) if
                                self.infiniteseg[i] != ""]

    # Retourne l'élément à la position index dans le mot infini
    def getElementAt(self, index):
        if index < len(self.finiteseg):
            return self.finiteseg[index]

        return self.infiniteseg[(index - len(self.finiteseg)) % len(self.infiniteseg)]


# Combine deux mots infinis pour les lire en même temps
def combine(w1: wword, w2: wword):
    w3 = wword("")

    # On construit d'abord la partie finie du mot combiné
    for i in range(max(len(w1.finiteseg), len(w2.finiteseg))):
        if len(w1.finiteseg) - 1 < i:
            x = w1.infiniteseg[(i - len(w1.finiteseg)) % len(w1.infiniteseg)]
        else:
            x = w1.finiteseg[i]

        if len(w2.finiteseg) - 1 < i:
            y = w2.infiniteseg[(i - len(w2.finiteseg)) % len(w2.infiniteseg)]
        else:
            y = w2.finiteseg[i]

        w3.finiteseg.append((x, y))

    # Et maintenant la partie infinie
    # c1 et c2 sont les positions auxquelles on s'est arrêté dans les parties infinies des deux mots à l'étape précédente dans les deux mots
    c1 = max(len(w1.finiteseg), len(w2.finiteseg)) - len(w1.finiteseg)
    c2 = max(len(w1.finiteseg), len(w2.finiteseg)) - len(w2.finiteseg)

    for i in range(math.lcm(len(w1.infiniteseg), len(w2.infiniteseg))):
        w3.infiniteseg.append(
            (w1.infiniteseg[(c1 + i) % len(w1.infiniteseg)], (w2.infiniteseg[(c2 + i) % len(w2.infiniteseg)])))

    return w3


class Game():
    def __init__(self):
        # Modélise l'arène
        # E = dico de la forme {noeud : [successeurs]}, V = dico de la forme {noeud:(owner, prio)}
        self.E = {}
        self.V = {}

        # Liste de DPA qui représentent les relations de préférence pour chaque joueur
        self.rels = {}

    def addVertex(self, name, owner, prio):
        self.V[name] = (owner, prio)
        self.E[name] = []

    def addTransition(self, source, destination):
        self.E[source].append(destination)

    def getOwner(self, v):
        return self.V[v][0]

    def setsucc(self, source, succlist):
        self.E[source] = succlist

    #Set la relation de préférence rel comme la relation de préférence associée au joueur player
    def setRelPref(self, rel, player):
        self.rels[player] = rel

class coalitional_game:
    #Transforme un jeu G quelconque en jeu de coalition à deux joueurs ou la coalition joue contre le joueur p
    def __init__(self, G: Game=None, p= None):
        #Transforme un jeu existant en jeu de coalition
        if G is not None and p is not None:
            self.E = G.E

            #Coalition
            self.V0 = [(x[0], x[1][1]) for x in G.V.items() if G.getOwner(x[0]) != p]

            #Joueur
            self.V1 = [(x[0], x[1][1]) for x in G.V.items() if G.getOwner(x[0]) == p]

        #Crée un jeu de coalition vide
        else:
            self.E = {}

            self.V0 = []
            self.V1 = []


    #Retourne la liste de predecesseurs d'un noeud w
    def getPred(self, w):
        l = []

        for k, v in self.E.items():
            if w in v:
                l.append(k)

        return l


    def getOwner(self, v):
        wanted = [x[0] for x in self.V0]
        if v in wanted:
            return 0
        else:
            return 1

    def opponent(self, p):
        if p == 0:
            return 1
        else:
            return 0

    # retourne un sous jeu contenant les éléments elems
    def subgame(self, elems):
        g_prime = coalitional_game()

        for v in elems:
            if v[0] in self.V0:
                g_prime.V0.append(v)
            else:
                g_prime.V1.append(v)

            #initialise la liste des successeurs
            g_prime.E[v[0]] = []

        wanted = [x[0] for x in elems]
        for v in elems:
            for succ in self.E[v[0]]:
                if succ in wanted:
                    g_prime.E[v[0]].append(succ)

        return g_prime

    # Calcule l'attracteur du joueur player dans le jeu de coalition d'objectif d'atteignabilité sur l'ensemble U
    def attractor(self, U, player):
        out = {}

        #On itére sur tous les sommets i.e l'union des deux listes ducoup
        for (v, color) in self.V0+self.V1:
            out[v] = len(self.E[v])

        queue = []
        regions = defaultdict(lambda: -1)

        #Attracteur
        W = []

        opponent = self.opponent(player)

        for node in U:
            queue.append(node)
            regions[node] = player #l'objectif est forcément dans la région gagnante vu que c'est reachability
            W.append(node)

        while queue:
            s = queue.pop(0)

            for sbis in self.getPred(s):
                if regions[sbis] == -1:
                    if self.getOwner(sbis) == player:
                        queue.append(sbis)
                        regions[sbis] = player
                        W.append(sbis)

                    elif self.getOwner(sbis) == opponent:
                        out[sbis] -= 1
                        if out[sbis] == 0:
                            queue.append(sbis)
                            regions[sbis] = player
                            W.append(sbis)

        w_bis = []
        for node in self.V0 + self.V1:
            if regions[node[0]] != player:
                w_bis.append(node)

        return W, w_bis


    #Résous le jeu de coalition de parité et renvoie les régions gagnantes pour les deux joueurs
    def solveparity(self):
        W1 = []
        W2 = []

        if len(self.V0+self.V1) == 0:
            return W1, W2

        else:
            prios = [x[1] for x in self.V0+self.V1]
            i = max(prios)

            if i%2 == 0:
                player = 0
            else:
                player = 1

            op = self.opponent(player)

            #On récupére tous les noeuds de priorité i et c'est la cible de l'attracteur
            U = [x[0] for x in self.V0 + self.V1 if x[1] == i]

            A, d1 = self.attractor(U, player)

            g_a = self.subgame(d1)

            sp_1, sp_2 = g_a.solveparity()

            if player == 0:
                W_player = sp_1
                W_op = sp_2
            else:
                W_player = sp_2
                W_op = sp_1

            if not W_op:
                if player == 0:
                    W1.extend(A)
                    W1.extend(W_player)
                else:
                    W2.extend(A)
                    W2.extend(W_player)
            else:
                B, discard1 = self.attractor(W_op, op)
                g_b = self.subgame(discard1)

                sp_1_, sp_2_ = g_b.solveparity()

                if player == 0:
                    W_playerbis = sp_1_
                    W_opbis = sp_2_
                else:
                    W_playerbis = sp_2_
                    W_opbis = sp_1_

                if player == 0:
                    W1 = W_playerbis

                    W2.extend(W_opbis)
                    W2.extend(B)

                else:
                    W2 = W_playerbis

                    W1.extend(W_opbis)
                    W1.extend(B)
        return W1, W2


# Représente un automate de parité déterministe
class DPA:
    def __init__(self, states: list, alphabet: list, transit: dict, q0, colors: dict):
        self.states = states
        self.alphabet = alphabet
        self.transit = transit
        self.q0 = q0
        self.colors = colors

    # Ajoute un état de label state et de priorité statecolor dans l'automate
    def addstate(self, state, statecolor):
        self.states.append(state)
        self.colors[state] = statecolor

    # Ajoute une transition du noeud source à destination en lisant label dans l'automate
    def addtransition(self, source, destination, label):
        self.transit[(source, label)] = destination

    # func est une fct booléenne et alphabet est l'ensemble des labels possibles pour les transitions
    def addtransitionset(self, source, destination, func, param, alphabet):
        for sym in alphabet:
            if func(sym, param):
                self.addtransition(source, destination, sym)

    # run avec l'automate et un mot infini et retourne si le mot est accepté ou pas
    def run(self, word: wword):
        current = self.q0

        for sym in word.finiteseg:
            current = self.transit[(current, sym)]

        # Calculons les priorités rencontrées infiniment souvent
        infColors = []
        for sym in word.infiniteseg:
            current = self.transit[(current, sym)]
            infColors.append(self.colors[current])

        return (max(infColors) % 2) == 0

    # Retourne un autre automate de parité déterministe étant le produit entre l'automate et le lasso passé en paramètre
    def productLasso(self, lasso: wword):
        initial_state = (lasso.getElementAt(0), self.q0)

        # initialise l'automate qui contiendra le produit avec l'état initial (v0,q0)
        A_prime = DPA([initial_state], [], {}, initial_state, {initial_state: self.colors[initial_state[1]]})

        # On enfile (state, position dans la 1ere composante dans le lasso) pour pouvoir prendre le bon successeur dans le lasso
        queue = [(initial_state, 0)]
        marque = {initial_state: True}

        while queue:
            ((v, u), pos) = queue.pop(0)

            # Element suivant v dans le lasso ...vw...
            succ = lasso.getElementAt(pos + 1)

            # on récupére les transitions de la forme u -> u' en lisant (v, v') avec v' quelconque
            for key, val in self.transit.items():  # Pour rappel une antrée de self.transit est ici de la forme {(u, (v,v')) : u'}
                # Si la transition permet de partir de u en lisant un couple de 1ere composante v
                if key[1][0] == v and key[0] == u:
                    # On ajoute une transition au produit
                    A_prime.addtransition((v, u), (succ, val), key[1][1])

                    if (succ, val) not in marque.keys():
                        A_prime.addstate((succ, val), self.colors[val])
                        queue.append(((succ, val), pos + 1))
                        marque[(succ, val)] = True

        return A_prime

    def productGame(self, game: Game, v0):
        h = Game()

        marque = {(v0, self.q0): True}
        queue = []

        h.addVertex((v0, self.q0), game.getOwner(v0), self.colors[self.q0])

        queue.append((v0, self.q0))

        while queue:
            (v, q) = queue.pop(0)

            q_prime = self.transit[(q, v)]

            # Pour tout successeur de v dans le jeu
            for succ in game.E[v]:
                h.addTransition((v, q), (succ, q_prime))

                if (succ, q_prime) not in marque.keys():
                    h.addVertex((succ, q_prime), game.getOwner(succ), self.colors[q_prime])
                    queue.append((succ, q_prime))
                    marque[(succ, q_prime)] = True

        return h

def cartesianProduct(L1, L2):
    L3 = []

    for e1 in L1:
        for e2 in L2:
            L3.append((e1, e2))

    return L3


def notTnotT(elem, goal):
    return elem[0] != goal and elem[1] != goal


def notTbutT(elem, goal):
    return elem[0] != goal and elem[1] == goal


def TbutnotT(elem, goal):
    return elem[0] == goal and elem[1] != goal


def Tandany(elem, goal):
    return elem[0] == goal


# Selon un jeu et la cible de l'objectif de Buci complementé retourne l'automate de parité déterministe modélisant la relation de préférence correspondante
def bucicomp(game: Game, target):
    A = DPA(["u0", "u1", "u2"], [], {}, "u0", {"u0": 2, "u1": 4, "u2": 3})

    gamestates = [x for x in game.V.keys()]

    A.addtransitionset("u0", "u0", notTnotT, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u0", "u1", Tandany, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u0", "u2", notTbutT, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u1", "u1", Tandany, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u1", "u0", notTnotT, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u1", "u2", notTbutT, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u2", "u2", notTbutT, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u2", "u1", Tandany, target, cartesianProduct(gamestates, gamestates))
    A.addtransitionset("u2", "u0", notTnotT, target, cartesianProduct(gamestates, gamestates))

    return A
