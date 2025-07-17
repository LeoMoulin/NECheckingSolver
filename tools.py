# Représente un mot infini de la forme v..(w..)^w
# Par exemple v0v1(v2v3)^w serait encodé de la forme v0 v1;v2 v3
import math


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
    def product(self, lasso: wword):
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


class Game():
    def __init__(self, V: dict, E: dict, rels: list):
        # Modélise l'arène
        # E = dico de la forme {noeud : [successeurs]}, V = dico de la forme {noeud:(owner, prio)}
        self.E = E
        self.V = V

        # Liste de DPA qui représentent les relations de préférence pour chaque joueur
        self.rels = rels


def cartesianProduct(L1,L2):
    L3 = []

    for e1 in L1:
        for e2 in L2:
            L3.append((e1, e2))

    return L3