import streamlit as st
import numpy as np
from knapsackBB import Knapsack
import pandas as pd

img = "https://raw.githubusercontent.com/malikbf5/ORSC-Knapsack/main/png1.png"
knapsackimage = "https://raw.githubusercontent.com/malikbf5/ORSC-Knapsack/main/1200px-Knapsack.svg.png"



st.write(""" 
# 0/1 Knapsack problem 
The 0/1 Knapsack problem is a classic Optimization Problem in which 
we have to find an optimal answer among all the possible combinations. In this problem, 
we are given a set of items having different weights and profits. We have to find 
the optimal solution considering all the given items.
""")
col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:
    st.image(knapsackimage,width = 250)

with col3:
    st.write(' ')


W = 25
n = 10
p = [40,30,50,10,25,48,17,22,2,11]
p_2 = [40,30,50,10,25,48,17,22,2,11]
w = [2,5,10,5,3,8,7,4,3,5]
w_2 = [2,5,10,5,3,8,7,4,3,5]
d, e = [], []
##########################################################################################
st.write("""In this example we have **n = 10** objects with different profits and weights and the maximum weight of our knapsack is **W = 25**

Your challenge is to find a combination of objects that maximizes your profit while respecting the maximum weight condition""")
##########################################################################################
#main page
table = {'Profit':p,'Weight':w}
df = pd.DataFrame(table)
st.write(""" ##### Objects profit and weight""")
st.dataframe(df.transpose())
#####################################################################################################
#User input
with st.sidebar:
    user_solution = st.multiselect("Select the solution from here", [0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
#####################################################################################################
#fonction user score
def user_score(solution):
    weight = 0
    profit = 0
    for i in range(len(solution)):
        weight = weight + w_2[solution[i]]
        profit = profit + p_2[solution[i]]
    if weight > W:
        st.write("Your solution surpassed the maximum weight")
    else :
        st.write("You have chosen the objects: ",str(solution))
        st.write("Your profit is = ", profit)
        st.write("The weight of your solution is = ", weight)
#####################################################################################################

st.write(""" ##### You can compare your results with those of an optimization algorithm used for this problem called Branch & Bound
""")
#####################################################################################################

# classifying objects in descending order of value(i)/weight(i) (Best first)
def score(i): return p[i] / w[i]
items = sorted(range(n), key=score, reverse=True)
for i in range(len(items)):
    j = items[i]
    d.append(p[j])
    e.append(w[j])
p = d
w = e
p_per_weight = [i / j for i, j in zip(p, w)]

# creating a list to extract classified objects  with their initial index using their ranking
realitems = []
for i in range(len(items)):
    realitems.append([i, items[i]])
#####################################################################################################

#####################################################################################################
col1, col2 = st.columns(2)

def stateful_button(*args, key=None, **kwargs):
    if key is None:
        raise ValueError("Must pass key")

    if key not in st.session_state:
        st.session_state[key] = False

    if st.button(*args, **kwargs):
        st.session_state[key] = not st.session_state[key]

    return st.session_state[key]

with col1:
    if stateful_button('Show my score', key="my_score"):
        user_score(user_solution)
with col2:
    if stateful_button("Show optimal solution", key="optimal_solution"):
        Knapsack(n, W, p, w, p_per_weight, realitems)

st.write("""
Branch & Bound is an approach based on the principle that the total set of feasible solutions can be partitioned into smaller subsets of solutions. These smaller subsets can then be evaluated systematically until the exact best solution is found.""")

st.write(""" It is important to note that while this problem seems simple, it becomes exponentially more complex when the number of objects(**n**) goes higher, which makes the knapsack problem an **NP** complete problem""")

st.write(""" Knapsack problems appear in real-world decision-making processes in a wide variety of fields, such as: 
- finding the least wasteful way to cut raw materials 
- selection of investments and portfolios, selection of assets for asset-backed securitization 
- container ship and aircraft loading 
- generating keys for the Merkle–Hellman and other knapsack cryptosystems""")
st.image(img)

