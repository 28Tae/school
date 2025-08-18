# We are going to create a Pokemon game.
# a spell is a move that a pokemon can cast
# A Pokemon is a character with a name, hp, mp, atk, and type.
# A player is also a character with a name, hp, mp, and atk.
# A player can catch pokemons.
# If the player already has a pokemon of the same type, the player can choose to replace the old pokemon with the new one.
# Otherwise, the player can catch the new pokemon.
# Create a Pokemon class and a Player class which are subclasses of the Char class.


# Your code here

class Spell:
    def __init__(self, name: str, mp_cost: int, damage: int):
        self._name: str = name
        self._mp_cost: int = mp_cost
        self._damage: int = damage

    def __str__(self):
        return f"name: {self._name}, mp_cost: {self._mp_cost}, damage: {self._damage}"
    
    def get_name(self) -> str:
        return self._name
    def get_mp_cost(self) -> int:
        return self._mp_cost
    def get_damage(self) -> int:
        return self._damage
    
class Character:
    def __init__(self, name: str, hp: int, mp: int, atk: int):
        self._name: str = name
        self._hp: int = hp
        self._mp: int = mp
        self._atk: int = atk
        self._alive: bool = True

    def __str__(self):
        return f"Name: {self._name}, hp: {self._hp}, mp: {self._mp}, atk: {self._atk}"
    
    def get_name(self) -> str:
        return self._name
    def get_hp(self) -> int:
        return self._hp
    def get_mp(self) -> int:
        return self._mp
    def get_atk(self) -> int:
        return self._atk
    
    def update_hp(self, hp: int):
        self._hp += hp
    def update_mp(self, mp: int):
        self._mp += mp
    
    def get_status(self) -> bool:
        return self._alive
    def update_status(self):
        self._alive = bool(self._hp > 0)

    # Would have typehinted Character directly, but it's self-referential
    def attack(self, target: "Character"):
        """Attacks the character target"""
        if not target.get_status():
            return print(f"[x] {target.get_name()} is already dead.")
        
        init_hp: int = target.get_hp()
        target.update_hp(-self.get_atk())
        target.update_status()
        print(f"[!] {self._name} attacks {target.get_name()}.\n{target.get_name()} is hit, hp changes from {init_hp} to {target.get_hp()}.\n")


class Pokemon(Character):
    def __init__(self, name: str, hp: int, mp: int, atk: int, p_type: str, spell: Spell):
        super().__init__(name, hp, mp, atk)
        self._p_type: str = p_type
        self._spell: Spell = spell
    
    def __str__(self):
        return f"{super().__str__()}, type: {self._p_type}.\nSpell details: {self._spell}."
    
    def get_type(self) -> str:
        return self._p_type
    def get_spell(self) -> Spell:
        return self._spell
    def update_spell(self, nspell: Spell):
        self._spell = nspell

    def cast_spell(self, target: Character):
        """Casts a spell which attacks, and drains MP"""
        spell = self.get_spell()
        if not self.get_status():
            return print(f"[x] {self.get_name()} is already dead.")
        
        if self.get_mp() < spell.get_mp_cost():
            return print(f"[x] {self.get_name()} lacks MP to cast {spell.get_name()}.")
        
        # Attacks player, drains MP
        init_hp: int = target.get_hp()
        target.update_hp(-spell.get_damage())
        target.update_status()
        self.update_mp(-spell.get_mp_cost())
        print(f"[!] {self.get_name()} casts {spell.get_name()} on {target.get_name()}.\n{target.get_name()} is hit, hp changes from {init_hp} to {target.get_hp()}.\n")


class Player(Character):
    def __init__(self, name: str, hp: int, mp: int, atk: int):
        super().__init__(name, hp, mp, atk)
        self._pokemons: list = []
    
    def get_pokemons(self) -> list:
        return self._pokemons

    def display_pokemons(self):
        """Displays the pokemons in the player's team"""
        if not self._pokemons:
            return print(f"> {self._name}, you have not caught any pokemons yet.")
        
        print(f"\n>> Here are the pokemons in {self._name}'s team:")
        [print(p) for p in self._pokemons]
        print()

    def catch_pokemon(self, pokemon: Pokemon):
        """Catches pokemon and adds to team, or replace if same type"""
        
        # Check for overlaps
        conflicted_pokemon: list[Pokemon] = [p for p in self._pokemons if p.get_type() == pokemon.get_type()]

        # If new type, catch it
        if conflicted_pokemon == []:
            self._pokemons.append(pokemon)
            return print(f"> {self._name} has caught {pokemon.get_name()}.")

        # If same type, ask to replace
        conflicted_pokemon: Pokemon = conflicted_pokemon[0]
        print(f">> {self._name}, you already have:")
        print(conflicted_pokemon)
        print(f"Now you meet:")
        print(pokemon)
        inp = input("Would you like to replace the pokemon of the same type? [Y/N] ").upper().strip()

        if inp == "Y":
            self._pokemons.remove(conflicted_pokemon)
            self._pokemons.append(pokemon)
            return print(f"> {self._name} has released {conflicted_pokemon.get_name()}, and caught {pokemon.get_name()}.")
        elif inp == "N":
            return print(f"> You choose not to catch {pokemon.get_name()}.")


# below are test functions and their expected outputs
# dmg spells (electric, fire, water)
fireball = Spell("Fireball", 12, 25)
fireblast = Spell("Fireblast", 15, 30)
thunderbolt = Spell("Thunderbolt", 10, 20)
frostbolt = Spell("Frostbolt", 8, 16)

# healing spells (grass)
heal = Spell("Heal", 10, -20)


def test_01():
    print("--- Test 01: test cataching different types of pokemons ---")
    player = Player("Ash Ketchum", 100, 100, 20)
    pokemon_01 = Pokemon("Charmander", 50, 60, 18, "Fire", fireball)
    pokemon_02 = Pokemon("Squirtle", 55, 60, 15, "Water", frostbolt)
    pokemon_03 = Pokemon("Bulbasaur", 80, 60, 12, "Grass", heal)
    pokemon_04 = Pokemon("Pikachu", 60, 60, 15, "Electric", thunderbolt)
    pokemon_05 = Pokemon("Ponyta", 60, 60, 18, "Fire", fireblast)

    print(player)

    player.display_pokemons()
    player.catch_pokemon(pokemon_01)
    player.catch_pokemon(pokemon_02)
    player.catch_pokemon(pokemon_03)
    player.catch_pokemon(pokemon_04)
    player.display_pokemons()
    player.catch_pokemon(pokemon_05)
    player.display_pokemons()

    print("--- End of Test 01 ---\n")


test_01()


def test_02():
    print("--- Test 02: test attacking between players and pokemons ---")

    # pokemons with various types and slightly different stats
    pikachu = Pokemon("Pikachu", 120, 100, 10, "Electric", thunderbolt)
    charmander = Pokemon("Charmander", 80, 120, 10, "Fire", fireball)
    squirtle = Pokemon("Squirtle", 100, 90, 10, "Water", frostbolt)
    bulbasaur = Pokemon("Bulbasaur", 120, 100, 10, "Grass", heal)

    # two players
    p1 = Player("Ash", 100, 100, 10)
    p2 = Player("Misty", 100, 100, 10)

    # p1 catches pikachu and charmander
    p1.catch_pokemon(pikachu)
    p1.catch_pokemon(charmander)
    p1.display_pokemons()

    # p2 catches squirtle and bulbasaur
    p2.catch_pokemon(squirtle)
    p2.catch_pokemon(bulbasaur)
    p2.display_pokemons()

    # player take turns to attack
    # player can attack
    # each pokemon can cast 1 spell

    # p1's turn
    p1.attack(p2)
    p1.get_pokemons()[0].cast_spell(p2.get_pokemons()[0])
    p1.get_pokemons()[1].cast_spell(p2.get_pokemons()[0])

    # p2's turn
    p2.attack(p1)
    p2.get_pokemons()[0].cast_spell(p1.get_pokemons()[0])
    p2.get_pokemons()[1].cast_spell(p2.get_pokemons()[0])  # heal

    # display status
    p1.display_pokemons()
    p2.display_pokemons()

    print("--- End of Test 02 ---\n")


test_02()


"""
--- Test 01: test cataching different types of pokemons ---
Name: Ash Ketchum, hp: 100, mp: 100, atk: 20.
Ash Ketchum, you have not caught any pokemons yet.

Ash Ketchum have caught Charmander.
Ash Ketchum have caught Squirtle.
Ash Ketchum have caught Bulbasaur.
Ash Ketchum have caught Pikachu.
Here are the pokemons in Ash Ketchum's team:
Name: Charmander, hp: 50, mp: 60, atk: 18. type: Fire.
Spell details: name: Fireball, mp_cost: 12, damage: 25.
Name: Squirtle, hp: 55, mp: 60, atk: 15. type: Water.
Spell details: name: Frostbolt, mp_cost: 8, damage: 16.
Name: Bulbasaur, hp: 80, mp: 60, atk: 12. type: Grass.
Spell details: name: Heal, mp_cost: 10, damage: -20.
Name: Pikachu, hp: 60, mp: 60, atk: 15. type: Electric.
Spell details: name: Thunderbolt, mp_cost: 10, damage: 20.

Ash Ketchum, you already have:
Name: Charmander, hp: 50, mp: 60, atk: 18. type: Fire.
Spell details: name: Fireball, mp_cost: 12, damage: 25.
Now you meet:
Name: Ponyta, hp: 60, mp: 60, atk: 18. type: Fire.
Spell details: name: Fireblast, mp_cost: 15, damage: 30.
Would you like to replace the pokemon of the same type? [Y/N]y
Ash Ketchum have released Charmander, and caught Ponyta.
Here are the pokemons in Ash Ketchum's team:
Name: Squirtle, hp: 55, mp: 60, atk: 15. type: Water.
Spell details: name: Frostbolt, mp_cost: 8, damage: 16.
Name: Bulbasaur, hp: 80, mp: 60, atk: 12. type: Grass.
Spell details: name: Heal, mp_cost: 10, damage: -20.
Name: Pikachu, hp: 60, mp: 60, atk: 15. type: Electric.
Spell details: name: Thunderbolt, mp_cost: 10, damage: 20.
Name: Ponyta, hp: 60, mp: 60, atk: 18. type: Fire.
Spell details: name: Fireblast, mp_cost: 15, damage: 30.

--- End of Test 01 ---

--- Test 02: test attacking between players and pokemons ---
Ash have caught Pikachu.
Ash have caught Charmander.
Here are the pokemons in Ash's team:
Name: Pikachu, hp: 120, mp: 100, atk: 10. type: Electric.
Spell details: name: Thunderbolt, mp_cost: 10, damage: 20.
Name: Charmander, hp: 80, mp: 120, atk: 10. type: Fire.
Spell details: name: Fireball, mp_cost: 12, damage: 25.

Misty have caught Squirtle.
Misty have caught Bulbasaur.
Here are the pokemons in Misty's team:
Name: Squirtle, hp: 100, mp: 90, atk: 10. type: Water.
Spell details: name: Frostbolt, mp_cost: 8, damage: 16.
Name: Bulbasaur, hp: 120, mp: 100, atk: 10. type: Grass.
Spell details: name: Heal, mp_cost: 10, damage: -20.

Ash attacks Misty.
Misty is hit, hp changes from 100 to 90.

Pikachu casts Thunderbolt on Squirtle.
Squirtle is hit, hp changes from 100 to 80.

Charmander casts Fireball on Squirtle.
Squirtle is hit, hp changes from 80 to 55.

Misty attacks Ash.
Ash is hit, hp changes from 100 to 90.

Squirtle casts Frostbolt on Pikachu.
Pikachu is hit, hp changes from 120 to 104.

Bulbasaur casts Heal on Squirtle.
Squirtle is hit, hp changes from 55 to 75.

Here are the pokemons in Ash's team:
Name: Pikachu, hp: 104, mp: 90, atk: 10. type: Electric.
Spell details: name: Thunderbolt, mp_cost: 10, damage: 20.
Name: Charmander, hp: 80, mp: 108, atk: 10. type: Fire.
Spell details: name: Fireball, mp_cost: 12, damage: 25.

Here are the pokemons in Misty's team:
Name: Squirtle, hp: 75, mp: 82, atk: 10. type: Water.
Spell details: name: Frostbolt, mp_cost: 8, damage: 16.
Name: Bulbasaur, hp: 120, mp: 90, atk: 10. type: Grass.
Spell details: name: Heal, mp_cost: 10, damage: -20.

--- End of Test 02 ---

"""
