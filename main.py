import math
from copy import deepcopy

import streamlit as st
import graphviz

from sorbing_model import SubstanceState, Neutralizer
import sorbing_model as m

from control_block_diagram import ControllerDiagram
from control_block_diagram import Point, Box, Connection

st.set_page_config(layout="wide")

st.title("Технологическая схема")


def get_process_flow(g: graphviz.Digraph, start_state: SubstanceState, process_steps: list[Neutralizer]):
    i = 0
    g.node(str(i), style="invis")
    i += 1
    for s in process_steps:
        oil = deepcopy(start_state)
        g.node(str(i), label=s.name)
        g.node(str(i) + 'u', style="invis")
        g.node(str(i) + 'd', style="invis")
        g.edge(str(i - 1)+':e', str(i)+':w', label=str(oil))

        if len(s.reactive(oil)) > 0:
            g.edge(str(i) + 'd:s', str(i)+':n', label=str(s.reactive(oil)))
        else:
            g.edge(str(i) + 'd:s', str(i)+':n', label="", style="invis")

        if len(s.refuse(oil)) > 0:
            g.edge(str(i)+':s', str(i) + 'u:n', label=str(s.refuse(oil)))
        else:
            g.edge(str(i)+':s', str(i) + 'u:n', label="", style="invis")

        s.reaction(oil)

        start_state = oil
        i += 1
    g.node(str(i), style="invis")
    g.edge(str(i - 1), str(i), label=str(start_state))


# def get_new_process_flow(start_state: SubstanceState, process_steps: list[Neutralizer]):
#     doc = ControllerDiagram()
#
#     i = 0
#     i += 1
#     for s in process_steps:
#         oil = deepcopy(start_state)
#         inputs = dict(left=1, left_text=[str(oil)])
#         if len(s.reactive(oil)) > 0:
#             inputs['bottom'] = 1
#             inputs['bottom_text'] = [s.reactive(oil)]
#         Box(Point(i // 2 * 2, (i % 2) * 2), text=s.name, inputs=inputs)
#
#         # g.node(str(i), label=s.name, shape='box')
#         # g.node(str(i) + 'u', style="invis")
#         # g.node(str(i) + 'd', style="invis")
#         # g.edge(str(i - 1), str(i), label=str(oil))
#         #
#         #
#         # if len(s.refuse(oil)) > 0:
#         #     g.edge( str(i), str(i) + 'u', label=str(s.refuse(oil)))
#         # else:
#         #     g.edge( str(i), str(i) + 'u', label="", style="invis")
#
#         s.reaction(oil)
#
#         start_state = oil
#         i += 1
#     # g.node(str(i), style="invis")
#     # g.edge(str(i - 1), str(i), label=str(start_state))
#     return doc


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
    g.attr(nodesep='1.2', ranksep="1.2")
    g.attr('node', shape='record', margin="0.3")
    g.attr('edge', weight='1')
    steps = [Neutralizer(m.filtration_reaction, m.filtration_refuse, m.filtration_reactive, "Фильтрация"),
             Neutralizer(m.drying_reaction, m.drying_refuse, m.drying_reactive, "Удаление воды"),
             Neutralizer(m.oxid_sorb_reaction, m.oxid_sorb_refuse, m.oxid_sorb_reactive, "Сорбция кислот"),
             Neutralizer(m.hydrocarbons_reaction, m.hydrocarbons_refuse, m.hydrocarbons_reactive, "Сорбция НУВ"),
             Neutralizer(m.filtration_reaction, m.filtration_refuse, m.filtration_reactive, "Фильтрация"),]
    get_process_flow(g, SubstanceState(speed, acid, impurities, water), steps)
    return g


empt = st.empty()

with st.form(key='my_form'):
    speed_input = st.text_input(label='Входной поток, л/ч', key="speed")
    acid_input = st.text_input(label='Кислотное число, мгKOH/г', key="acid")
    impurities_input = st.text_input(label='Содержание механических примесей, г/мл', key="impurities")
    water_input = st.text_input(label='Влагосодержание, %', key="water")
    submit_button = st.form_submit_button(label='Обновить')

with empt:
    empt.write(get_graph(speed_input, acid_input, impurities_input, water_input))
