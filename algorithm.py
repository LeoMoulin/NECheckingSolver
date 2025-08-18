from automatas import *

"""
    pi : un lasso,
    game : une arène,
    retourne si la partie est un outcome d'un équilibre de Nash
    sinon renvoie le premier joueur trouvé qui à un déviation profitable
"""


def is_nash_outcome(pi: wword, game: Arena):
    players = set([x[0] for x in game.V.values()])

    for p in players:
        # Récupére l'automate A déja complémenté TODO
        a = game.rels[p]

        # Produit entre l'automate et le lasso
        b_p = a.productLasso(pi)

        # Produit entre l'automate et l'arène qu'on transforme en jeu de coalition
        h_p = b_p.productGame(game, pi.getElementAt(0))
        h_p = coalitional_game(h_p, p)

        # Applique zielonka pour récupérer les régions gagnantes
        (W_b, W_a) = h_p.solveparity()

        # Parcours le lasso dans H et regarde si on passe dans la région gagnante du joueur B
        vertex = h_p.V0 + h_p.V1

        start = pi.getElementAt(0)
        current = [v[0] for v in vertex if v[0][0] == start]
        current = current[0]

        for v in (pi.finiteseg + pi.infiniteseg)[1:]:
            if current in W_a:
                print("Player " + str(p) + " is not cool with this")
                return False

            # On avance dans le lasso et dans le jeu
            current = [x for x in h_p.E[current] if x[0] == v]
            current = current[0]

    # Si on est arrivé ici alors c'est bon
    print("Yes we have a NE outcome")
    return True
