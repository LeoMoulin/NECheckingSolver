"""
   Cette classe modélise les machines de Mealy
   states : liste des états mémoire,
   m0: état mémoire initial,
   updatefunc: f((m,v)) = m' en fonction de l'état mémoire et du sommet lu donne l'état mémoire sur lequel se déplacer dans la machine,
   movefunc: f((m,v)) = v' en fonction de l'état mémoire et du sommet lu donne le sommet sur lequel aller dans le jeu original.
   Ces deux fonctions sont représentées avec des dictionnaires de la forme {(m,v):sortie}
"""


class mealy_machine:
    def __init__(self, states: list, m0: str, updatefunc: dict, movefunc: dict):
        self.states = states
        self.current_state = m0
        self.updatefunc = updatefunc
        self.movefunc = movefunc

    # Entrée v : le sommet à lire, transitionne vers l'état mémoire correspondant et retourne l'output (sommet à "jouer")
    def update(self, v: str):
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
def simulation(super_machine, n_actions):
    #Au début la machine de chaque joueur i est la machine en [i][i] (diagonale) current_machine est la colonne pour chaque joueur en gros
    current_machine = [i for i in range(len(super_machine))]

