from random import random

from src.GroundplanFrame import GroundplanFrame


def simulated_annealing(init_state, max_iterations, generateNeighborFunc):
    state = init_state.deepCopy()
    best_state = state

    frame = GroundplanFrame(state)
    bframe = frame

    for i in range(max_iterations):

        frame.repaint(state)
        bframe.repaint(best_state)

        neighbor = generateNeighborFunc(state.deepCopy())
        temperature = float(i + 1) / max_iterations

        print state.getPlanValue(), neighbor.getPlanValue(), best_state.getPlanValue()

        print "t =", temperature, ", i =", i
        if neighbor.getPlanValue() > state.getPlanValue():
            state = neighbor.deepCopy()
            if state.getPlanValue() > best_state.getPlanValue():
                best_state = state.deepCopy()
        elif (state.getPlanValue() - neighbor.getPlanValue()) / temperature > random():
            state = neighbor.deepCopy()
