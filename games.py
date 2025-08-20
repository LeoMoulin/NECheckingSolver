from collections import defaultdict
#Contiens les classes représentant les jeux en général

#Modélise une arène
class Arena():
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

    #Définit la relation de préférence rel comme la relation de préférence associée au joueur player
    def setRelPref(self, rel, player):
        self.rels[player] = rel

#Modélise un jeu de coalition
class coalitional_game:
    """
        Permet de créer un jeu de coallition vide ou de
        créer un jeu de coallition à partir d'une arène.

        Ici le joueur 0 est la coalition et le joueur 1 est le joueur
    """
    def __init__(self, G: Arena=None, p= None):
        # Création à partir d'une arène
        if G is not None and p is not None:
            self.E = G.E

            nodes = G.V.items()
            # coalition
            self.V0 = [(x[0], x[1][1]) for x in nodes if G.getOwner(x[0]) != p]

            # joueur
            self.V1 = [(x[0], x[1][1]) for x in nodes if G.getOwner(x[0]) == p]

        # Création d'un jeu vide
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

    # Retourne le joueur qui posséde le noeud v
    def getOwner(self, v):
        owned_list = [x[0] for x in self.V0]

        if v in owned_list:
            return 0
        else:
            return 1

    def opponent(self, p):
        if p == 0:
            return 1
        else:
            return 0

    # Retourne un sous jeu (de coalition) contenant les sommets de la liste elems
    def subgame(self, elems):
        g_prime = coalitional_game()

        for v in elems:
            if v in self.V0:
                g_prime.V0.append(v)
            else:
                g_prime.V1.append(v)

            #initialise la liste des successeurs
            g_prime.E[v[0]] = []

        wanted_vertex = [x[0] for x in elems]

        #Si (v,v') est dans E et que v' est aussi a extraire pour le sous jeu on peut ajouter l'arc (v,v') au sous jeu
        for v in elems:
            for succ in self.E[v[0]]:
                if succ in wanted_vertex:
                    g_prime.E[v[0]].append(succ)

        return g_prime

    # Calcule l'attracteur du joueur player dans le jeu de coalition d'objectif d'atteignabilité sur l'ensemble U
    def reachability_solver(self, U, player):
        out = {}

        #Union des listes de sommets des deux joueurs
        V = self.V0+self.V1

        for (v, color) in V:
            out[v] = len(self.E[v])

        queue = []
        regions = defaultdict(lambda: -1)

        strat_player = {}
        strat_opponent = {}

        region_player = []
        region_opponent = []

        opponent = self.opponent(player)

        for node in U:
            queue.append(node)
            regions[node] = player
            region_player.append(node)

            if self.getOwner(node) == player:
                strat_player[node] = self.E[node][0]

        while queue:
            s = queue.pop(0)

            for sbis in self.getPred(s):
                if regions[sbis] == -1:
                    if self.getOwner(sbis) == player:
                        queue.append(sbis)
                        regions[sbis] = player
                        region_player.append(sbis)
                        strat_player[sbis] = s

                    elif self.getOwner(sbis) == opponent:
                        out[sbis] -= 1

                        if out[sbis] == 0:
                            queue.append(sbis)
                            regions[sbis] = player
                            region_player.append(sbis)

        for node in V:
            if regions[node[0]] != player:
                regions[node] = opponent
                region_opponent.append(node)

                if self.getOwner(node[0]) == opponent:
                    for succ in self.E[node[0]]:
                        if regions[succ] != player:
                            strat_opponent[node[0]] = succ

        return (region_player, strat_player), (region_opponent, strat_opponent)


    #Résous le jeu de coalition de parité et renvoie les régions gagnantes pour les deux joueurs
    def solveparity(self):
        #Région gagnante et strat de la coalition
        W1 = []
        strat1 = {}

        #Région gagnante et strat du joueur
        W2 = []
        strat2 = {}

        V = self.V0 + self.V1

        if len(V) == 0:
            return (W1, strat1), (W2,strat2)

        else:
            prios = [x[1] for x in V]
            i = max(prios)

            #Le joueur 0 est la coalition car c'est celui qui a l'objectif pair
            if i%2 == 0:
                player = 0
            else:
                player = 1

            op = self.opponent(player)

            #On récupére tous les noeuds de priorité i et c'est la cible de l'attracteur
            U = [x[0] for x in V if x[1] == i]

            (A, tau1), (d1, d2) = self.reachability_solver(U, player)

            g_a = self.subgame(d1)

            sp_1, sp_2 = g_a.solveparity()

            if player == 0:
                W_player, sig_player = sp_1
                W_op, sig_op = sp_2
            else:
                W_player, sig_player = sp_2
                W_op, sig_op = sp_1

            if not W_op:
                if player == 0:
                    W1.extend(A)
                    W1.extend(W_player)
                    strat1.update(tau1)
                    strat1.update(sig_player)
                else:
                    W2.extend(A)
                    W2.extend(W_player)
                    strat2.update(tau1)
                    strat2.update(sig_player)
            else:
                (B, mu), (d1, d2) = self.reachability_solver(W_op, op)
                g_b = self.subgame(d1)

                sp_1_, sp_2_ = g_b.solveparity()

                if player == 0:
                    W_playerbis, sig_playerbis = sp_1_
                    W_opbis, sig_opbis = sp_2_
                else:
                    W_playerbis, sig_playerbis = sp_2_
                    W_opbis, sig_opbis = sp_1_

                if player == 0:
                    W1 = W_playerbis
                    strat1 = sig_playerbis

                    W2.extend(W_opbis)
                    W2.extend(B)

                    strat2.update(mu)
                    strat2.update(sig_opbis)
                    strat2.update(sig_op)
                else:
                    W2 = W_playerbis

                    strat2 = sig_playerbis

                    W1.extend(W_opbis)
                    W1.extend(B)

                    strat1.update(mu)
                    strat1.update(sig_opbis)
                    strat1.update(sig_op)

        return (W1,strat1), (W2,strat2)