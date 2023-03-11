import streamlit as st
# Knapsack function
def Knapsack(n, W, p, w, p_per_weight, realitems):
    # Creating a priority queue
    class Priority_Queue:
        def __init__(self):
            self.pqueue = []
            self.length = 0

        # insert node in the list in ascending order
        def insert(self, node):
            for i in self.pqueue:
                get_bound(i)
            i = 0
            while i < len(self.pqueue):
                if self.pqueue[i].bound > node.bound:
                    break
                i += 1
            self.pqueue.insert(i, node)
            self.length += 1

        # show list
        def print_pqueue(self):
            for i in list(range(len(self.pqueue))):
                print("pqueue", i, "=", self.pqueue[i].bound)

        # delete node from list
        def remove(self):
            try:
                result = self.pqueue.pop()
                self.length -= 1
            except:
                print("The node list is empty")
            else:
                return result

    # Creating node class with: level, profit, weight.
    class Node:
        def __init__(self, level, profit, weight):
            self.level = level
            self.profit = profit
            self.weight = weight
            self.items = []

        def parent(self, parent):
            self.parent = parent

    # Calculating the upper bound of a node
    def get_bound(node):
        if node.weight >= W:
            return 0
        else:
            result = node.profit
            j = node.level + 1
            totweight = node.weight
            while j <= n - 1 and totweight + w[j] <= W:
                totweight = totweight + w[j]
                result = result + p[j]
                j += 1
            k = j
            if k <= n - 1:
                result = result + (W - totweight) * p_per_weight[k]
            return result

    # Priority queue with 0 nodes
    nodes_generated = 0
    pq = Priority_Queue()

    nodes = []

    # creating artificial node at level-1, profit = 0, weight = 0
    v = Node(-1, 0, 0)
    nodes_generated += 1
    nodes.append(v)

    maxprofit = 0
    v.bound = get_bound(v)

    pq.insert(v)
    v.label = "0"

    #  Branch&Bound procedure while priority queue isn't empty
    while pq.length != 0:

        # take node with best upper bound
        v = pq.remove()

        # check if node shows promise
        if v.bound > maxprofit:
            # branch from node "v" with a new node which contains the next object in the knapsack
            u = Node(0, 0, 0)
            nodes_generated += 1
            nodes.append(u)
            u.level = v.level + 1
            u.profit = v.profit + p[u.level]
            u.weight = v.weight + w[u.level]
            u.items = v.items.copy()

            # Associate node to its predecessor and added label "Y" as in "Yes" to taking the next object
            u.parent(v)
            u.label = "Y" + str(realitems[u.level][1] + 1)

            # add object with the same index as the node's level
            u.items.append(u.level)

            # update items in the knapsack and maxprofit
            if u.weight <= W and u.profit > maxprofit:
                maxprofit = u.profit
                bestitems = u.items

            # update upper bound
            u.bound = get_bound(u)

            # check if node shows promise to branch from
            if u.bound > maxprofit:
                # add node in priority queue in ascending order
                pq.insert(u)

            # branch from node "v" with a new node which doesn't contain the next object in the knapsack
            u2 = Node(u.level, v.profit, v.weight)
            nodes_generated += 1
            nodes.append(u2)
            u2.bound = get_bound(u2)
            u2.items = v.items.copy()

            # Associate node to its predecessor and added label "N" as in "No" to taking the next object
            u2.parent(v)
            u2.label = "N" + str(realitems[u2.level][1] + 1)

            # check if node shows promise to branch from
            if u2.bound > maxprofit:
                # add node in priority queue in ascending order
                pq.insert(u2)

    # recover initial index of objects
    for i in range(len(bestitems)):
        bestitems[i] = realitems[bestitems[i]][1]
    st.write("Optimal solution :",str(bestitems))
    st.write("Maximum profit = ",maxprofit)

        