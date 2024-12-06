import math
import copy


class_map = {}


class Factor:
    def __init__(self, symbol, value, reference=None):
        self.symbol = symbol
        self.value = value
        self.reference = reference

    def __str__(self):
        return f"{self.symbol}={self.value}"

class Load:
    def __init__(
        self,
        symbol,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        self.symbol = symbol
        self.load_factor = load_factor
        self.combination_factor = combination_factor
        self.enabled = enabled
        self.load_factor_symbol = None

    def for_design(self, load_factor=1.0, combination_factor=1.0):
        load = copy.copy(self)
        load.load_factor = load_factor
        load.combination_factor = combination_factor
        return load


class Force(Load):
    def __init__(
        self,
        symbol,
        value,
        contact,
        load_factor=1.0,
        combination_factor=1.0,
            enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.value = value
        self.contact = contact

    def __str__(self):
        return f"<Force {self.symbol} = {self.value}N @ {self.contact[0]}x{self.contact[1]}mm2, LF={self.load_factor}, psi={self.combination_factor}"

class_map["force"] = Force


class Vehicle(Load):
    def __init__(
        self,
        symbol,
        axle_loads,
        track_width,
        wheel_base,
        wheel_contact,
        brake_force=0,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.axle_loads = axle_loads
        self.track_width = track_width
        self.wheel_base = wheel_base
        self.wheel_contact = wheel_contact
        self.brake_force = brake_force

    def __str__(self):
        return f"<Vehicle {self.symbol} = {self.weight}N, LF={self.load_factor}, psi={self.combination_factor}"

    def scale_weight(self, weight):
        # scale axle loads and horizontal (brake) load to weight
        Q = self.weight
        self.brake_force = weight / Q * self.brake_force
        self.axle_loads = [weight * al / Q for al in self.axle_loads]

    @property
    def weight(self):
        return sum(self.axle_loads)

    @property
    def width(self):
        return self.track_width + self.wheel_contact[1]

    @property
    def length(self):
        return self.wheel_base + self.wheel_contact[0]


class_map["vehicle"] = Vehicle


class UDL(Load):
    def __init__(
        self,
        symbol,
        value,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.value = value

    def __str__(self):
        return f"<UDL {self.symbol} = {self.value*1000}kN/m2, LF={self.load_factor}, psi={self.combination_factor}"

class_map["udl"] = UDL


class Traction(Load):
    def __init__(
        self,
        symbol,
        value,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.value = value

    def __str__(self):
        return f"<Traction force {self.symbol} = {self.value}N, LF={self.load_factor}, psi={self.combination_factor}"

class_map["traction"] = Traction


class LinearMass(Load):
    def __init__(
        self,
        symbol,
        value,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.value = value

    def __str__(self):
        return f"<Linear mass {self.symbol} = {self.value*1000000}kg/m, LF={self.load_factor}, psi={self.combination_factor}"

class_map["linear_mass"] = LinearMass


class Temperature(Load):
    def __init__(
        self,
        symbol,
        install=10,
        min=-20,
        max=40,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.install = install
        self.min = min
        self.max = max

    def __str__(self):
        return f"<Temperature {self.symbol} = {self.min}C .. {self.max}C, LF={self.load_factor}, psi={self.combination_factor}"


class Wind(Load):
    def __init__(
        self,
        symbol,
        x=0,
        y=0,
        z=0,
        load_factor=1.0,
        combination_factor=1.0,
        enabled=True,
    ):
        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )
        self.x, self.y, self.z = x, y, z

    def __str__(self):
        return f"<Wind force {self.symbol}, LF={self.load_factor}, psi={self.combination_factor}"

class PedestrianFlow(Load):
    def __init__(
        self,
        symbol,
        people_density=None,
        people_count=None,
        load_factor=1.0,
        combination_factor=1.0,
        person_mass=0.07,
        step_frequency=2.3,
        enabled=True,
    ):
        if people_density is None and people_count is None:
            raise ValueError("Density or fixed count must be set")
        if people_density is not None and people_count is not None:
            raise ValueError("Either density or fixed count must be set, not both")

        super().__init__(
            symbol, load_factor, combination_factor, enabled=enabled
        )

        self.person_mass = person_mass
        self.step_frequency = step_frequency

        self._people_density = people_density
        self._people_count = people_count

    def __str__(self):
        if self._people_count is not None:
            return f"<Pedestrians {self.symbol} = {self._people_count}P, LF={self.load_factor}, psi={self.combination_factor}"
        else:
            return f"<Pedestrians {self.symbol} = {self._people_density}P/m2, LF={self.load_factor}, psi={self.combination_factor}"


    @property
    def people_count(self, A):
        if self._people_count is not None:
            return self._people_count
        return self._people_density * A / 1e6  # density in /m2 -> /mm2

    @property
    def people_density(self, A):
        return self.people_count(A) / A


class_map["pedestrian_flow"] = PedestrianFlow


class DesignLimit:
    def __init__(self, symbol, value, description=None):
        self.symbol = symbol
        self.value = value
        self.description = description


class Deflection(DesignLimit):
    def __init__(self, symbol, value, description=None):
        super().__init__(symbol, value, description)

class_map["deflection"] = Deflection


class Eigenfrequency(DesignLimit):
    def __init__(self, symbol, value, description=None):
        super().__init__(symbol, value, description)


class_map["eigenfrequency"] = Eigenfrequency


class Acceleration(DesignLimit):
    def __init__(self, symbol, value, description=None):
        super().__init__(symbol, value, description)


class_map["acceleration"] = Acceleration


class ThermalExpansion(DesignLimit):
    def __init__(self, symbol, value, description=None):
        super().__init__(symbol, value, description)


class_map["thermal_expansion"] = ThermalExpansion



class Loadcase:
    def __init__(
        self,
        symbol,
        loads,
        limitstate="SLS",
        stiffness_factors=None,
        strength_factors=None,
        enabled=True,
    ):
        self.symbol = symbol
        self.loads = loads
        self.limitstate = limitstate

        self.stiffness_factors = stiffness_factors if stiffness_factors is not None else []
        self.strength_factors = strength_factors if strength_factors is not None else []

        self.enabled = enabled

    @property
    def id(self):
        return f"{self.symbol}_{self.limitstate}"

    def __str__(self):
        return f"<Loadcase '{self.symbol}'>"

    def get_loads_of_type(self, cls):
        return [load for load in self.loads if isinstance(load, cls)]

    @property
    def forces(self):
        return self.get_loads_of_type(Force)

    @property
    def vehicles(self):
        return self.get_loads_of_type(Vehicle)

    @property
    def pressures(self):
        return self.get_loads_of_type(UDL)

    @property
    def linear_masses(self):
        return self.get_loads_of_type(LinearMass)

    @property
    def pedestrian_flows(self):
        return self.get_loads_of_type(PedestrianFlow)

    @property
    def total_stiffness_factor(self):
        return math.prod(f.value for f in self.stiffness_factors)

    @property
    def total_strength_factor(self):
        return math.prod(f.value for f in self.strength_factors)


def _parse_design_limits(data):
    return [class_map[l["class"]](symbol=l["symbol"], value=l["value"], description=l["description"]) for l in data]


def _parse_loads(data):
    loads = []
    for l in data:
        load = None
        symbol = l["symbol"]
        if l["class"] == "vehicle":
            load = Vehicle(
                symbol=symbol,
                axle_loads=l["axle_loads"],
                track_width=l["track_width"],
                wheel_base=l["wheel_base"],
                wheel_contact=l["wheel_contact"],
                brake_force=l["brake_force"],
            )
        elif l["class"] == "udl":
            load = UDL(symbol=symbol, value=l["value"])
        elif l["class"] == "traction":
            load = Traction(symbol=symbol, value=l["value"])
        elif l["class"] == "force":
            load = Force(
                symbol=symbol, value=l["value"], contact=l["contact"]
            )
        elif l["class"] == "linear_mass":
            load = LinearMass(symbol=symbol, value=0)
        elif l["class"] == "pedestrian_flow":
            load = PedestrianFlow(
                symbol=symbol,
                people_count=l["people_count"],
                people_density=l["people_density"],
                step_frequency=l["step_frequency"],
                person_mass=l["person_mass"],
            )
        elif l["class"] == "temperature":
            load = Temperature(
                symbol=symbol, install=10, min=-20, max=40
            )
        elif l["class"] == "wind":
            load = Wind(symbol=symbol, x=0, y=0, z=0)
        if load is not None:
            loads.append(load)
        else:
            raise Exception(f"Unhandled load class '{l['class']}'")

    return loads




def _parse_loadcases(data, loads, load_factors, resistance_factors, design_limits):
    factors = {
        f.symbol: f
        for f in resistance_factors + load_factors
    }
    loads_lookup = {load.symbol: load for load in loads}
    print(factors)
    loadcases = []
    for l in data:
        if l.get("enabled", True):
            lc_loads = []
            for ld_symbol, psi in l["load_combination"].items():
                print(l)
                LF = l["load_factors"].get(ld_symbol)
                load = loads_lookup[ld_symbol].for_design(factors.get(LF, 1), psi)
                lc_loads.append(load)

            loadcases.append(
                Loadcase(
                    l["symbol"],
                    lc_loads,
                    l["limitstate"].upper(),
                    stiffness_factors=[factors[f] for f in l["stiffness_factors"]],
                    strength_factors=[factors[f] for f in l["strength_factors"]],
                )
            )

    return loadcases


def _parse_factors(data, scale=1.0):
    return [Factor(symbol=d["symbol"], value=d["value"] * scale, reference=d.get("reference")) for d in data]


def get_design_code(code, load_scale_factor):
    loads = _parse_loads(code.loads)
    limits = _parse_design_limits(code.design_limits)
    load_factors = _parse_factors(code.load_factors, load_scale_factor)
    resistance_factors = _parse_factors(code.resistance_factors)
    loadcases = _parse_loadcases(code.loadcases, loads, load_factors=load_factors, resistance_factors=resistance_factors, design_limits=limits)
    return loads, loadcases


if __name__ == "__main__":
    import eurocodes.NL

    LSF = 1  # CC1
    loads, loadcases = get_design_code(eurocodes.NL, load_scale_factor=LSF)

    for l in loads:
        print(l)
