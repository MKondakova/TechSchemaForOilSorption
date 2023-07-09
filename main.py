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
    g.node(str(i), shape='plaintext', label="")
    # g.node(str(i) + 'r', shape='plaintext', label="")
    # g.node(str(i) + 'l', shape='plaintext', label="", margin='0.0')
    # g.edge(f"{i}l:e", f"{i}:w", label='', style="invis")
    # g.edge(f"{i}:e", f"{i}r:w", label='', style="invis")
    i += 1
    oil = deepcopy(start_state)
    for s in process_steps:
        g.node(str(i), label=s.name)
        reactive = s.reactive(oil)
        refuse = s.refuse(oil)
        g.node(str(i) + 'r', shape='plaintext', label=refuse)
        g.node(str(i) + 'l', shape='plaintext', label=reactive, margin='0.0')
        g.edge(f"{i}l:e", f"{i}:w", label='', style="invis" if len(reactive) == 0 else "")
        g.edge(f"{i}:e", f"{i}r:w", label='', style="invis" if len(refuse) == 0 else "")
        g.edge(str(i - 1)+':s', str(i)+':n', label=str(oil))
        s.reaction(oil)
        i += 1
    g.node(str(i), shape='plaintext', label=str(oil))
    g.edge(str(i - 1)+':s', str(i)+':n', label="")


DEFAULT_SPEED = 178
DEFAULT_ACID = 0.03
DEFAULT_IMPURITIES = 0.001
DEFAULT_WATER = 0.2
g = graphviz.Digraph(format='svg')

def get_graph(g, speed, acid, impurities, water):
    density = 0.86
    errors = []
    try:
        speed = float(speed.strip()) * 0.86
    except ValueError:
        errors.append("Значение поля \"Входной поток\" не корректно")
        speed = DEFAULT_SPEED * density
    try:
        acid = float(acid.strip())
    except ValueError:
        errors.append("Значение поля \"Кислотное число\" не корректно")
        acid = DEFAULT_ACID
    try:
        impurities = float(impurities.strip()) * density
    except ValueError:
        errors.append("Значение поля \"Содержание механических примесей\" не корректно")
        impurities = DEFAULT_IMPURITIES * density
    try:
        water = float(water.strip())/100
    except ValueError:
        errors.append("Значение поля \"Влагосодержание\" не корректно")
        water = DEFAULT_WATER / 100

    if not (0 <= water <= 2):
        errors.append("Для масла с введенным значением влагосодержания установка не подходит")
    if not (0 <= acid <= 1):
        errors.append("Для масла с введенным значением кислотного числа установка не подходит")
    if not (0 <= impurities <= 0.01):
        errors.append("Для масла с введенным значением механических примесей установка не подходит")
    if speed <= 0:
        errors.append("Поток должен быть положительным")

    if len(errors) > 0:
        status_textfield.error(". ".join(errors))
        return g.render()
    else:
        status_textfield.success("Все хорошо")

    g = graphviz.Digraph(format='svg')
    g.attr(nodesep='0.4', ranksep="0.5", fontsize="20", rank='same')
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
    speed_input = st.text_input(value=str(DEFAULT_SPEED), label='Входной поток, л/ч', key="speed")
    acid_input = st.text_input(value=str(DEFAULT_ACID), label='Кислотное число, мгKOH/г', key="acid")
    impurities_input = st.text_input(value=str(DEFAULT_IMPURITIES), label='Содержание механических примесей, г/мл', key="impurities")
    water_input = st.text_input(value=str(DEFAULT_WATER), label='Влагосодержание, %', key="water")
    submit_button = st.form_submit_button(label='Обновить')

status_textfield = st.empty()
with empt:
    empt.image(get_graph(g, speed_input, acid_input, impurities_input, water_input))


