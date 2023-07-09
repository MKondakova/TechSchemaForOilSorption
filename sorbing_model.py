class SubstanceState:
    def __init__(self, speed: float, acid: float, impurities: float, water: float):
        self.speed = speed
        self.speed_of_components = {'Вода': water * speed,
                                    'Кисл. число': acid * speed,
                                    'Мех. примеси': impurities * speed,
                                    'Масло': (1 - (water + acid + impurities)) * speed
                                    }
        print(self.speed_of_components)

    speed_of_components: dict[str, float]
    speed: float  # kg/min

    def __str__(self):
        result = "".join([f"{key}:{value / self.speed * 100:.3f}%\n" for key, value in self.speed_of_components.items()])
        result += f"{self.speed} кг/мин"
        return result


class Neutralizer:
    def __init__(self, label, concentrations):
        self.label = label
        self.concentrations = concentrations
        self.speed = None

    label: str
    concentrations: dict[str, float]  # -1 < n < 1
    speed: float

    def __str__(self):
        return f"{self.label} \nspeed:{self.speed}"


def flow_calculation(admixture: SubstanceState, neutralizer: Neutralizer):
    neutralizers = neutralizer.concentrations
    for subst in neutralizers:
        if neutralizer.speed is None and subst in admixture.speed_of_components:
            neutralizer.speed = admixture.speed_of_components[subst] / neutralizers[subst]
        else:
            continue
        if subst in admixture.speed_of_components:
            admixture.speed_of_components[subst] += neutralizer.speed * neutralizers[subst]
    admixture.speed = sum(admixture.speed_of_components.values())
