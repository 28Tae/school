###
# Guardian of the Galaxy
###

# Your answer here.

class Spaceship:
    def __init__(self, name: str, location: str):
        self._name: str = name
        self._location: str = location
        # Guardians onboard
        self._guardians: list = []

    def get_location(self) -> str:
        return self._location
    
    def go_to(self, planet: str) -> str:
        if self.contains() == []:
            return f"{self._name} does not have any guardians on board"
        # Checks if any planet is known
        if not any(
            [planet in g.known_planets() for g in self._guardians]
        ):
            return f"{planet} is not a known location"
        # Teleport there
        self._location = planet
        return f"{self._name} travels to {planet}"
    
    def share_knowledge(self):
        """Share the known planets with all the guardians"""
        new_planets = set([
            p for g in self._guardians for p in g.known_planets()
        ])
        for g in self._guardians:
            g._known_planets = list(new_planets)

    def contains(self) -> list:
        return [g._name for g in self._guardians]

class Guardian:
    # Accepts any arbitrary optional number of planets
    def __init__(self, name: str, planet: str, *other_planets: str):
        self._name: str = name
        self._location: str = planet
        self._known_planets: list = [planet] + list(other_planets)
        # Assume they do not appear in any ship
        self._ship: Spaceship = None
    
    def known_planets(self) -> list:
        """Returns a list of known planets"""
        return self._known_planets
    
    def board(self, ship: Spaceship) -> str:
        if self._location != ship.get_location():
            return f"{self._name} cannot board the {ship._name}"
        
        # Remove from previous ship
        if self._ship is not None:
            self._ship._guardians.remove(self)

        # Board the ship
        self._ship = ship
        self._ship._guardians.append(self)
        ship.share_knowledge()

        return f"{self._name} boards the {ship._name}"
    
    def get_location(self) -> str:
        if self._ship:
            return f"{self._name} is on the ship {self._ship._name} at the planet {self._location}"
        return f"{self._name} is on the planet {self._location}"
