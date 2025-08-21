from games import *

"""
   Cette classe modélise les machines de Mealy
   states : liste des états mémoire,
   m0: état mémoire initial,
   updatefunc: f((m,v)) = m' en fonction de l'état mémoire et du sommet lu donne l'état mémoire sur lequel se déplacer dans la machine,
   movefunc: f((m,v)) = v' en fonction de l'état mémoire et du sommet lu donne le sommet sur lequel aller dans le jeu original.
   Ces deux fonctions sont représentées avec des dictionnaires de la forme {(m,v):sortie}
"""


class mealy_machine:
    def __init__(self, states: list, m0, updatefunc: dict, movefunc: dict):
        self.states = states
        self.current_state = m0
        self.updatefunc = updatefunc
        self.movefunc = movefunc

    # Entrée v : le sommet à lire, transitionne vers l'état mémoire correspondant et retourne l'output (sommet à "jouer")
    def update(self, v: str):
        #Permet de fix le bug de l'actualisation de toutes les machines de Mealy dans simulation() si y a déviation
        if (self.current_state, v) in self.movefunc.keys():
            output = self.movefunc[(self.current_state, v)]
            self.current_state = self.updatefunc[(self.current_state, v)]
            return output

    def add_state(self, state: str):
        if state not in self.states:
            self.states.append(state)

    #Ajoute une transition de m à m_prime en lisant v avec output v'
    def add_transition(self, v, v_prime, m, m_prime):
        self.updatefunc[(m,v)] = m_prime
        self.movefunc[(m,v)] = v_prime



#Given a super mealy machine simulate what happens in each machine simultaneously (the game runs) for n actions
def simulation(g:Arena, super_machine, n_tours):
    #Au début la machine de chaque joueur i est la machine en [i][i] (diagonale) current_machine est la colonne pour chaque joueur en gros
    current_machine = [i for i in range(len(super_machine))]

    #au début on démarre en v0
    current_node = "v0"

    playing = g.getOwner(current_node)

    ref_machine = super_machine[playing][current_machine[playing]]
    next_node = ref_machine.movefunc[(ref_machine.current_state, current_node)]

    print("game is at " + current_node)
    for i in range(n_tours):
        # Update les machines en sachant qu'on lit current_node
        for x in range(len(super_machine)):
            for y in range(len(super_machine[x])):
                super_machine[x][y].update(current_node)
                #print("machine " + str(x) + str(y) + " updating to " + str(super_machine[x][y].current_state))

        print("player " + str(playing) + " plays " + current_node + " -> " + next_node)

        #Update le noeud courant et continue le jeu
        current_node = next_node

        previous_player = playing
        playing = g.getOwner(current_node)

        ref_machine = super_machine[playing][current_machine[playing]]

        # Détecte si le joueur précédent à dévié cad la nouvelle machine référente ne sait rien faire
        if (ref_machine.current_state, current_node) not in ref_machine.movefunc.keys():
            #On passe en mode punition pour punir previous_player qui a dévié
            ref_machine = super_machine[playing][previous_player]

            current_machine = [previous_player for i in range(len(super_machine))]

        next_node = ref_machine.movefunc[(ref_machine.current_state, current_node)]
