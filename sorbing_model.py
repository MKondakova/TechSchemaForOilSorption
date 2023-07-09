class SubstanceState:
    def __init__(self, speed: float, acid: float, impurities: float, water: float):
        self.speed = speed
        self.acid = acid
        self.acid_mass = acid / 56000 * 170 * speed
        self.impurities_mass = impurities * speed
        self.water_mass = water * speed
        self.hydrocarbons = True
        self.oil_mass = speed - (self.acid_mass + self.impurities_mass + self.water_mass)

    acid: float
    acid_mass: float
    impurities_mass: float
    water_mass: float
    hydrocarbons: bool
    oil_mass: float
    speed: float  # kg/min

    def __str__(self):
        self.speed = self.acid_mass + self.impurities_mass + self.water_mass + self.oil_mass
        result = f"Масло: {(1 - (self.water_mass + self.acid_mass + self.impurities_mass) / self.speed) * 100:.4g}%\n"
        result += f"Вода: {self.water_mass / self.speed * 100:.4g}%\n" if abs(self.water_mass) > 10e-5 else ""
        result += f"Мех. примеси: {self.impurities_mass / self.speed:.4g} %\n" if abs(self.impurities_mass) > 10e-9 else ""
        result += f"Нафтеновые кислоты: {self.acid_mass / self.speed:.2g}%\n" if abs(self.acid) > 10e-9 else ""
        result += f"НУВ\n" if self.hydrocarbons else ""
        result += f"{self.speed:.4g} кг/час"
        return result


class Neutralizer:
    def __init__(self, reaction, refuse, reactive, name):
        self.reaction = reaction
        self.refuse = refuse
        self.reactive = reactive
        self.name = name

    reaction: classmethod
    refuse: classmethod
    reactive: classmethod
    name: str


# steps

def filtration_reaction(oil: SubstanceState):
    oil.impurities_mass = 0


def filtration_refuse(oil: SubstanceState):
    return f"Мех. примеси: {oil.impurities_mass:.4g} кг/час" if oil.impurities_mass > 0 else ""


def filtration_reactive(oil: SubstanceState):
    return ""


def drying_reaction(oil: SubstanceState):
    oil.water_mass = 0


def drying_refuse(oil: SubstanceState):
    return f"Цеолит: {oil.speed * 0.10:.4g}кг/час\nВода {oil.water_mass}кг/час"


def drying_reactive(oil: SubstanceState):
    return f"Цеолит: {oil.speed * 0.1:.4g}кг/час"


def oxid_sorb_reaction(oil: SubstanceState):
    oil.acid = 0
    oil.acid_mass = 0


def oxid_sorb_refuse(oil: SubstanceState):
    return f"Силикагель: {oil.speed * 0.04:.4g}кг/час\nБетанит: {oil.speed * 0.05:.4g}кг/час\nMgO: {oil.speed * 0.01:.4g}кг/час\nНафтеновые кислоты: {oil.acid_mass:.2g}кг/час"


def oxid_sorb_reactive(oil: SubstanceState):
    return f"Силикагель: {oil.speed * 0.04:.4g}кг/час\nБетанит: {oil.speed * 0.05:.4g}кг/час\nMgO: {oil.speed * 0.01:.4g}кг/час"


def hydrocarbons_reaction(oil: SubstanceState):
    oil.hydrocarbons = False


def hydrocarbons_refuse(oil: SubstanceState):
    return f"Крупнопористый силикагель: {oil.speed * 0.1:.4g}кг/час\nНУВ много кг/час"


def hydrocarbons_reactive(oil: SubstanceState):
    return f"Крупнопористый силикагель: {oil.speed * 0.1:.4g}кг/час"