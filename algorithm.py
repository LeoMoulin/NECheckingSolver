from tools import *

#Soit un lasso, retourne True si la partie est outcome d'un profil de stratégie étant un équilibre de Nash
def isNashOutcome(pi:wword, game:Game):
    players = set([x[0] for x in game.V.values()])

    #On répéte l'algorithme pour chaque joueur
    for p in players:
        #Récupére l'automate A déja compémenté TODO
        a = game.rels[p]

        #Constructions
        b_p = a.productLasso(pi)

        h_p = b_p.productGame(game, pi.getElementAt(0))
        h_p = coalitional_game(h_p, p)

        #Récupére les région gagnantes (inversé car la coalition a l'objectif pair dans le jeu)
        (W_b, W_a) = h_p.solveparity()

        #Parcours le lasso dans H et regarde si on passe dans la région gagnante du joueur B
        vertex = h_p.V0+h_p.V1
        current = [v[0] for v in vertex if v[0][0] == pi.getElementAt(0)]
        current = current[0]

        for v in (pi.finiteseg+pi.infiniteseg)[1:]:
            if current in W_a:
                print("Player " + str(p) + " is not cool with this")
                return False

            #On avance dans le lasso et dans le jeu
            current = [x for x in h_p.E[current] if x[0] == v]
            current = current[0]

    #Si on est arrivé ici alors c'est bon
    print("Yes we have a NE outcome")
    return True