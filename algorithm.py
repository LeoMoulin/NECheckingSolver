from automatas import *
from mealymachine import *
"""
    pi : un lasso,
    game : une arène,
    retourne si la partie est un outcome d'un équilibre de Nash
    sinon renvoie le premier joueur trouvé qui à un déviation profitable
"""


def is_nash_outcome(pi: wword, game: Arena):
    players = set([x[0] for x in game.V.values()])

    #Pour l'instant, on suppose que le jeu démarre en "v0" donc par construction l'état initial de h_p aura comme seconde composante (v0, q0)
    super_mealy_machine = [[mealy_machine([], ("v0", "u0"), {}, {}) for p in players] for p in players]

    for p in players:
        # Récupére l'automate A déja complémenté TODO
        a = game.rels[p]

        # Produit entre l'automate et le lasso
        b_p = a.productLasso(pi)

        # Produit entre l'automate et l'arène qu'on transforme en jeu de coalition
        h_p = b_p.productGame(game, pi.getElementAt(0))
        h_p = coalitional_game(h_p, p)

        # Applique zielonka pour récupérer les régions gagnantes (b = coalition, a = joueur)
        (W_b, sigb), (W_a, siga) = h_p.solveparity()

        #Utilise h_p pour construire les machines de Mealy permettant aux autres joueurs de punir le joueur p
        for (v,q), desc in h_p.E.items():
            for (v_prime, q_prime) in desc:
                x = game.getOwner(v)

                #Gére le bug au cas ou la clé n'existe pas dans le dico
                if ((v,q) in sigb.keys()):
                    opt_move = sigb[(v,q)]
                else:
                    opt_move = -1

                if ((v,q) in W_b) and (opt_move == (v_prime, q_prime)):
                    super_mealy_machine[x][p].add_state(q)
                    super_mealy_machine[x][p].add_state(q_prime)
                    super_mealy_machine[x][p].add_transition(v, v_prime, q, q_prime)

                # On update aussi les machines de punition des autres joueurs
                others = [o for o in players if o != x]
                for y in others:
                    super_mealy_machine[y][p].add_state(q)
                    super_mealy_machine[y][p].add_state(q_prime)
                    super_mealy_machine[y][p].add_transition(v, "*", q, q_prime)


        # Parcours le lasso dans H et regarde si on passe dans la région gagnante du joueur B tout en actualisant les machines de Mealy
        vertex = h_p.V0 + h_p.V1

        start = pi.getElementAt(0)
        current = [v[0] for v in vertex if v[0][0] == start]
        current = current[0] #v,q

        #On parcours deux fois la partie infinie et une deuxième fois le premier élément pour que le programme puisse construire ce qu'il faut dans  (sinon il a pas le temps vu que ca boucle et il manque des états)
        for v in (pi.finiteseg + pi.infiniteseg*2 + [pi.infiniteseg[0]])[1:]:
            if current in W_a:
                print("Player " + str(p) + " is not cool with this")
                return False

            # On avance dans le lasso et dans le jeu
            next = [x for x in h_p.E[current] if x[0] == v] #v',q'

            # Update la machine de Mealy correspondant
            if game.getOwner(current[0]) == p:
                super_mealy_machine[p][p].add_transition(current[0], next[0][0], current[1], next[0][1])
            else:
                super_mealy_machine[p][p].add_transition(current[0], "*", current[1], next[0][1])

            current = next[0]

    # Si on est arrivé ici alors c'est bon
    print("Yes we have a NE outcome")
    return True, super_mealy_machine
