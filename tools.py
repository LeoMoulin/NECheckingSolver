# Représente un mot infini de la forme v..(w..)^w
# Par exemple v0v1(v2v3)^w serait encodé de la forme v0 v1;v2 v3
import math

class wword:
    def __init__(self, word: str=""):
        self.finiteseg = []
        self.infiniteseg = []
        if word != "":
            parts = word.split(";", 1)
            self.finiteseg = parts[0].split(" ")
            self.infiniteseg = parts[1].split(" ")

            # Petite sécu en cas d'erreur sur les espaces
            self.finiteseg = [self.finiteseg[i] for i in range(0, len(self.finiteseg)) if self.finiteseg[i] != ""]
            self.infiniteseg = [self.infiniteseg[i] for i in range(0, len(self.infiniteseg)) if self.infiniteseg[i] != ""]

#Combine deux mots infinis pour les lire en même temps
def combine(w1:wword, w2:wword):
    w3 = wword("")

    #On construit d'abord la partie finie du mot combiné
    for i in range(max(len(w1.finiteseg), len(w2.finiteseg))):
            if len(w1.finiteseg)-1 < i:
                x = w1.infiniteseg[i-len(w1.finiteseg)%len(w1.infiniteseg)]
            else:
                x = w1.finiteseg[i]

            if len(w2.finiteseg)-1 < i:
                y = w2.infiniteseg[i-len(w2.finiteseg)%len(w2.infiniteseg)]
            else:
                y = w2.finiteseg[i]

            w3.finiteseg.append((x,y))

    #Et maintenant la partie infinie
    #c1 et c2 sont les positions auxquelles on s'est arrêté dans les parties infinies des deux mots à l'étape précédente dans les deux mots
    c1 = max(len(w1.finiteseg), len(w2.finiteseg))-len(w1.finiteseg)
    c2 = max(len(w1.finiteseg), len(w2.finiteseg))-len(w2.finiteseg)

    for i in range(math.lcm(len(w1.infiniteseg),len(w2.infiniteseg))):
        w3.infiniteseg.append((w1.infiniteseg[(c1+i)%len(w1.infiniteseg)], (w2.infiniteseg[(c2+i)%len(w2.infiniteseg)])))

    return w3


# Représente un automate de parité déterministe
class DPA:
    def __init__(self, states: list, alphabet: list, transit: dict, q0, colors: dict):
        self.states = states
        self.alphabet = alphabet
        self.transit = transit
        self.q0 = q0
        self.colors = colors

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
