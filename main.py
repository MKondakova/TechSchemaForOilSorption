from copy import deepcopy

import streamlit as st
import graphviz

from sorbing_model import SubstanceState, Neutralizer, flow_calculation

st.title("Технологическая схема")

class Step:
    def __init__(self, reactive, refuse, name):
        self.reactive = reactive
        self.refuse = refuse
        self.name = name

    oil: SubstanceState
    reactive: Neutralizer
    refuse: str
    name: str

def get_process_flow(g: graphviz.Digraph, start_state: SubstanceState, process_steps: list[Step]):
    i = 0
    g.node(str(i), style="invis")
    i += 1
    for s in process_steps:
        s.oil = deepcopy(start_state)
        g.node(str(i), label=s.name, shape='box')
        g.node(str(i)+'u', style="invis")
        g.node(str(i)+'d', style="invis")
        g.edge(str(i-1), str(i), label=str(s.oil))
        flow_calculation(s.oil, s.reactive)
        if len(s.reactive.label) > 0:
            g.edge(str(i)+'d', str(i), label=str(s.reactive))
        g.edge(str(i), str(i)+'u', label=s.refuse)
        start_state = s.oil
        i += 1
    g.node(str(i), style="invis")
    g.edge(str(i-1), str(i), label=str(start_state))

def get_graph(acid, impurities, water):
    density = 0.86
    try:
        acid = int(acid.strip())
        impurities = int(impurities.strip())
        water = int(water.strip())
    except ValueError:
        acid = 0.03
        impurities = 0.001
        water = 0.2
    g = graphviz.Digraph(format='JPG')
    g.attr(splines='ortho', nodesep='0.4')
    steps = [Step(Neutralizer('KOH/H2O 40%', { 'Кисл. числ': -0.01, 'Вода': 0.2 }), 'Остаток', 'Декислоция'),
             Step(Neutralizer('', { 'Boда': -0.6 }), 'H20', 'Цеолит')]
    get_process_flow(g, SubstanceState(500, acid, impurities, water), steps)
    return g.render()


empt = st.empty()

with st.form(key='my_form'):
    acid_input = st.text_input(label='Кислотное число, мгKOH/г', key="acid") #0.86 г/мл
    impurities_input = st.text_input(label='Содержание механических примесей, г/мл', key="impurities")
    water_input = st.text_input(label='Влагосодержание, %', key="water")
    submit_button = st.form_submit_button(label='Обновить')

with empt:
    empt.image(get_graph(acid_input, impurities_input, water_input), use_column_width=False)
