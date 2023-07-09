import math
from copy import deepcopy

import streamlit as st
import graphviz

from sorbing_model import SubstanceState, Neutralizer
import sorbing_model as m


st.set_page_config(layout="wide")

st.title("Технологическая схема")


def get_process_flow(g: graphviz.Digraph, start_state: SubstanceState, process_steps: list[Neutralizer]):
    i = -1
    g.node(str(i), shape='plaintext', label=str(start_state), group='2')
    g.node(str(i) + 'r', shape='plaintext', label="", group='1')
    g.node(str(i) + 'l', shape='plaintext', label="", margin='0.0', group='3')
    g.edge(f"{i}l:e", f"{i}:w", label='', style="invis")
    g.edge(f"{i}:e", f"{i}r:w", label='', style="invis")
    i += 1
    oil = deepcopy(start_state)
    for s in process_steps:
        g.node(str(i), label=s.name, group='2')
        reactive = s.reactive(oil)
        refuse = s.refuse(oil)
        g.node(str(i) + 'r', shape='plaintext', label=refuse, group='1')
        g.node(str(i) + 'l', shape='plaintext', label=reactive, margin='0.0', group='3')
        g.edge(f"{i}l:e", f"{i}:w", label='', style="invis" if len(reactive) == 0 else "")
        g.edge(f"{i}:e", f"{i}r:w", label='', style="invis" if len(refuse) == 0 else "")
        g.edge(str(i - 1)+':s', str(i)+':n', label=str(oil))
        s.reaction(oil)
        i += 1
    g.node(str(i), shape='plaintext', label=str(oil))
    g.edge(str(i - 1)+':s', str(i)+':n', label="")



def get_graph(speed, acid, impurities, water):
    try:
        speed = int(speed.strip()) * 0.86
    except ValueError:
        speed = 178 * 0.86
    try:
        acid = int(acid.strip())
    except ValueError:
        acid = 0.03
    try:
        impurities = int(impurities.strip()) * 0.86
    except ValueError:
        impurities = 0.001 * 0.86
    try:
        water = int(water.strip())
    except ValueError:
        water = 0.2 / 100

    g = graphviz.Digraph(format='svg')
    g.attr(nodesep='0.4', ranksep="0.5", fontsize="20")
    g.attr('node', shape='record')
    steps = [Neutralizer(m.filtration_reaction, m.filtration_refuse, m.filtration_reactive, "Фильтрация"),
             Neutralizer(m.drying_reaction, m.drying_refuse, m.drying_reactive, "Удаление воды"),
             Neutralizer(m.oxid_sorb_reaction, m.oxid_sorb_refuse, m.oxid_sorb_reactive, "Сорбция кислот"),
             Neutralizer(m.hydrocarbons_reaction, m.hydrocarbons_refuse, m.hydrocarbons_reactive, "Сорбция НУВ"),
             Neutralizer(m.filtration_reaction, m.filtration_refuse, m.filtration_reactive, "Фильтрация"),]
    get_process_flow(g, SubstanceState(speed, acid, impurities, water), steps)
    return g.render()


empt = st.empty()

with st.form(key='my_form'):
    speed_input = st.text_input(label='Входной поток, л/ч', key="speed")
    acid_input = st.text_input(label='Кислотное число, мгKOH/г', key="acid")
    impurities_input = st.text_input(label='Содержание механических примесей, г/мл', key="impurities")
    water_input = st.text_input(label='Влагосодержание, %', key="water")
    submit_button = st.form_submit_button(label='Обновить')

with empt:
    empt.image(get_graph(speed_input, acid_input, impurities_input, water_input))
