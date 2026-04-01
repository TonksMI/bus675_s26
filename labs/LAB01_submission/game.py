"""
Lab 1: Text-Based Adventure RPG
================================
Matthew Tonks

Build your game here! This file contains all the starter code from the lab notebook.
Fill in the TODOs, add your own classes, and make it your own.

Run with: python game.py
"""

import random


# =============================================================================
# Dice Utilities
# =============================================================================

def roll_d20():
    """Roll a 20-sided die."""
    return random.randint(1, 20)


def roll_dice(num_dice, sides):
    """Roll multiple dice and return the total. E.g., roll_dice(2, 6) for 2d6."""
    return sum(random.randint(1, sides) for _ in range(num_dice))


# =============================================================================
# Item Class
# =============================================================================

class Item:
    """An item that can be picked up and used."""

    def __init__(self, name, description, healing_value=0, is_quest_item=False):
        self.name = name
        self.description = description
        self.healing_value = healing_value
        self.is_quest_item = is_quest_item

    def __str__(self):
        return f"{self.name} - {self.description}"


# =============================================================================
# Character Classes
# =============================================================================

class Character:
    """Base class for all characters in the game."""

    def __init__(self, name, health, strength, defense):
        self.name = name
        self.health = health
        self.max_health = health
        self.strength = strength
        self.defense = defense

    def is_alive(self):
        """Return True if health > 0"""
        return self.health > 0

    def take_damage(self, amount):
        """Reduce health, but don't go below 0"""
        self.health = max(0, self.health - amount)
        print(f"BAM! {self.name} takes {amount} damage! (HP: {self.health}/{self.max_health})")

    def attack(self, target):
        """Implement d20 combat"""
        roll = roll_d20()
        attack_score = roll + self.strength
        print(f"CLASH! {self.name} attacks {target.name}! (Roll: {roll} + Str: {self.strength} = {attack_score})")
        
        if attack_score >= target.defense:
            damage = roll_dice(1, 6) + (self.strength // 2)
            print(f"HIT!")
            target.take_damage(damage)
        else:
            print(f"MISS!")

    def __str__(self):
        return f"{self.name} (HP: {self.health}/{self.max_health})"


class Player(Character):
    """The player character."""

    def __init__(self, name):
        super().__init__(name, health=50, strength=5, defense=12)
        self.inventory = []

    def pick_up(self, item):
        """Add item to inventory"""
        self.inventory.append(item)
        print(f"INVENTORY: You picked up: {item.name}")

    def use_item(self, item_name):
        """Use an item from the inventory"""
        for item in self.inventory:
            if item_name.lower() in item.name.lower():
                if item.healing_value > 0:
                    old_hp = self.health
                    self.health = min(self.max_health, self.health + item.healing_value)
                    healed = self.health - old_hp
                    print(f"USE: You used {item.name}. It restored {healed} health!")
                    self.inventory.remove(item)
                    return True
                else:
                    print(f"USE: You can't use {item.name} right now.")
                    return False
        
        print(f"USE: You don't have '{item_name}' in your inventory.")
        return False

    def show_inventory(self):
        """Display all items in inventory"""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("\nINVENTORY:")
            for item in self.inventory:
                print(f"- {item}")


class Enemy(Character):
    """Base class for enemies."""

    def __init__(self, name, health, strength, defense, xp_value=10):
        super().__init__(name, health, strength, defense)
        self.xp_value = xp_value


# Specific enemy types
class DrunkenSailor(Enemy):
    def __init__(self):
        super().__init__("Drunken Sailor", health=15, strength=2, defense=8, xp_value=5)

class ScurvyRat(Enemy):
    def __init__(self):
        super().__init__("Scurvy Rat", health=10, strength=1, defense=10, xp_value=3)

class Siren(Enemy):
    def __init__(self):
        super().__init__("Siren", health=30, strength=4, defense=13, xp_value=20)

class GhostPirate(Enemy):
    def __init__(self):
        super().__init__("Ghost Pirate", health=35, strength=5, defense=14, xp_value=25)

class Blackbeard(Enemy):
    def __init__(self):
        super().__init__("Captain Blackbeard", health=60, strength=8, defense=15, xp_value=100)


# =============================================================================
# Location Class
# =============================================================================

class Location:
    """A location in the game world."""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}  # {"north": Location, "south": Location, etc.}
        self.enemies = []      # List of enemies in this location
        self.items = []        # List of Item objects in this location

    def describe(self):
        """Print a full description of the location."""
        print(f"\n{'='*50}")
        print(f"LOCATION: {self.name}")
        print(f"{'='*50}")
        print(self.description)

        if self.enemies:
            print("\nENEMIES PRESENT:")
            for enemy in self.enemies:
                print(f"- {enemy.name}")

        if self.items:
            print("\nITEMS HERE:")
            for item in self.items:
                print(f"- {item.name}")

        exits = self.get_exits()
        if exits:
            print(f"\nEXITS: {', '.join(exits)}")

    def get_exits(self):
        """Return a list of available directions."""
        return list(self.connections.keys())

    def add_connection(self, direction, location):
        """Connect this location to another."""
        self.connections[direction] = location


# =============================================================================
# World Builder
# =============================================================================

def create_world():
    """Create and connect all locations. Returns the starting location."""

    # Create locations
    port = Location(
        "Port Royal",
        "The bustling naval base of the Caribbean. The British Navy's flags fly high."
    )
    tavern = Location(
        "Tortuga Tavern",
        "A rowdy tavern filled with the smell of rum and salt. Pirates are singing shanties."
    )
    ship = Location(
        "The Jolly Roger",
        "Your trusty ship. The sails are flapping in the wind, ready for adventure."
    )
    reef = Location(
        "Siren's Reef",
        "The water is crystal clear, but jagged rocks lurk beneath. You hear faint, haunting music."
    )
    lagoon = Location(
        "Mermaid's Lagoon",
        "A beautiful lagoon with glowing water. Be careful, mermaids can be deadly."
    )
    graveyard = Location(
        "Shipwreck Graveyard",
        "The remains of dozens of ships litter the seabed. Ghosts of sailors roam here."
    )
    island = Location(
        "Skull Island",
        "A dark, foreboding island. The jungle is thick and you feel watched from the shadows."
    )
    cannibal = Location(
        "Cannibal Island",
        "A tropical paradise with a dark secret. The local tribe is looking for dinner."
    )
    marsh = Location(
        "The Foggy Marsh",
        "A thick, swampy area filled with mist. It's hard to see where you're going."
    )
    cave = Location(
        "Blackbeard's Cave",
        "A massive cave dripping with water. Gold glints in the darkness, but a cold presence looms."
    )
    hidden_cove = Location(
        "The Hidden Cove",
        "A peaceful, secret beach. The perfect place to stash a legendary treasure."
    )

    # Interconnected Graph Connections
    # Port Royal Hub
    port.add_connection("west", tavern)
    tavern.add_connection("east", port)
    
    port.add_connection("east", ship)
    ship.add_connection("west", port)
    
    port.add_connection("north", reef)
    reef.add_connection("south", port)
    
    port.add_connection("south", lagoon)
    lagoon.add_connection("north", port)
    
    # Outer Ring and Cross-connections
    tavern.add_connection("south", graveyard)
    graveyard.add_connection("north", tavern)
    
    ship.add_connection("south", graveyard)
    graveyard.add_connection("east", ship)
    
    reef.add_connection("west", island)
    island.add_connection("east", reef)
    
    lagoon.add_connection("west", cannibal)
    cannibal.add_connection("east", lagoon)
    
    graveyard.add_connection("south", cannibal)
    cannibal.add_connection("north", graveyard)
    
    graveyard.add_connection("west", island)
    island.add_connection("south", graveyard)
    
    # Path to the End
    island.add_connection("west", marsh)
    marsh.add_connection("north", island)
    
    cannibal.add_connection("west", marsh)
    marsh.add_connection("south", cannibal)
    
    marsh.add_connection("west", cave)
    cave.add_connection("east", marsh)
    
    cave.add_connection("north", hidden_cove)
    hidden_cove.add_connection("south", cave)

    # Add enemies
    port.enemies.append(ScurvyRat())
    tavern.enemies.append(DrunkenSailor())
    reef.enemies.append(Siren())
    graveyard.enemies.append(GhostPirate())
    cannibal.enemies.append(DrunkenSailor()) 
    cave.enemies.append(Blackbeard())

    # Add items
    port.items.append(Item("Scurvy Biscuit", "A hard, dry biscuit. Better than nothing.", healing_value=5))
    tavern.items.append(Item("Bottle of Rum", "Fine Caribbean rum. Restores your spirit.", healing_value=20))
    lagoon.items.append(Item("Old Grog", "Watered down rum. Still does the trick.", healing_value=10))
    cave.items.append(Item("Golden Kraken Idol", "The legendary treasure of Blackbeard.", is_quest_item=True))

    return port


# =============================================================================
# Combat System
# =============================================================================

class Combat:
    """Manages turn-based combat between player and enemy."""

    # Combat states
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    COMBAT_END = "combat_end"

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.state = Combat.PLAYER_TURN
        self.combat_log = []

    def start(self):
        """Begin combat and run until someone wins/loses/flees."""
        print(f"\nCOMBAT BEGINS!")
        print(f"{self.player.name} vs {self.enemy.name}!")

        while self.state != Combat.COMBAT_END:
            if self.state == Combat.PLAYER_TURN:
                self.player_turn()
            elif self.state == Combat.ENEMY_TURN:
                self.enemy_turn()

        return self.get_result()

    def player_turn(self):
        """Handle player's turn in combat."""
        print(f"\n{self.player} | {self.enemy}")
        print("What do you do? (attack / use [item] / run)")

        action_input = input("> ").lower().strip()
        parts = action_input.split()
        if not parts: return
        
        action = parts[0]

        if action == "attack":
            self.player.attack(self.enemy)
            if not self.enemy.is_alive():
                print(f"\nVICTORY! {self.enemy.name} has been defeated!")
                self.state = Combat.COMBAT_END
            else:
                self.state = Combat.ENEMY_TURN

        elif action == "use" and len(parts) > 1:
            item_name = " ".join(parts[1:])
            if self.player.use_item(item_name):
                self.state = Combat.ENEMY_TURN

        elif action == "run":
            # 50% chance to escape
            if random.random() < 0.5:
                print("You successfully fled!")
                self.state = Combat.COMBAT_END
            else:
                print("Couldn't escape!")
                self.state = Combat.ENEMY_TURN

        else:
            print("Invalid action. Try 'attack', 'use [item]', or 'run'.")

    def enemy_turn(self):
        """Handle enemy's turn in combat."""
        print(f"\n{self.enemy.name}'s turn...")
        self.enemy.attack(self.player)

        if not self.player.is_alive():
            print(f"\nDEFEAT! {self.player.name} has fallen!")
            self.state = Combat.COMBAT_END
        else:
            self.state = Combat.PLAYER_TURN

    def get_result(self):
        """Return the combat result: 'victory', 'defeat', or 'fled'."""
        if not self.enemy.is_alive():
            return "victory"
        elif not self.player.is_alive():
            return "defeat"
        else:
            return "fled"


# =============================================================================
# Main Game Class
# =============================================================================

class Game:
    """Main game controller."""

    # Game states
    EXPLORING = "exploring"
    IN_COMBAT = "in_combat"
    GAME_OVER = "game_over"
    VICTORY = "victory"

    def __init__(self):
        self.player = None
        self.current_location = None
        self.state = Game.EXPLORING
        self.game_running = True

    def start(self):
        """Initialize and start the game."""
        self.show_intro()
        self.create_player()
        self.current_location = create_world()  # Your function from earlier
        self.current_location.describe()

        # Main game loop
        while self.game_running:
            if self.state == Game.EXPLORING:
                self.exploration_loop()
            elif self.state == Game.GAME_OVER:
                self.show_game_over()
                break
            elif self.state == Game.VICTORY:
                self.show_victory()
                break

    def show_intro(self):
        """Display the game introduction."""
        print("\n" + "="*60)
        print("         THE LEGEND OF KRAKEN'S COVE")
        print("="*60)
        print("\nYou are a young buccaneer who has just arrived at Port Royal.")
        print("You've heard whispers of Captain Blackbeard's legendary treasure,")
        print("the Golden Kraken Idol, hidden somewhere in the mysterious Kraken's Cove.")
        print("Your journey will take you across the high seas, through Siren's Reef,")
        print("and eventually to the dark Skull Island.")
        print("\nCan you defeat the ghost of Blackbeard and claim the treasure?")
        print("\n" + "="*60)

    def create_player(self):
        """Create the player character."""
        print("\nWhat is your name, buccaneer?")
        name = input("> ")
        self.player = Player(name)
        print(f"\nWelcome, {name}! Your adventure begins...")

    def exploration_loop(self):
        """Handle player input during exploration."""
        print("\nWhat do you do? (type 'help' for commands)")
        command = input("> ").lower().strip()

        # Parse the command
        parts = command.split()
        if not parts:
            return

        action = parts[0]

        if action == "help":
            self.show_help()

        elif action == "look":
            self.current_location.describe()

        elif action == "go" and len(parts) > 1:
            direction = parts[1]
            self.move(direction)

        elif action in ["north", "south", "east", "west", "up", "down"]:
            self.move(action)

        elif action in ["fight", "attack"]:
            self.initiate_combat()

        elif action in ["take", "get", "pick"] and len(parts) > 1:
            item_name = " ".join(parts[1:])
            self.take_item(item_name)

        elif action in ["use"] and len(parts) > 1:
            item_name = " ".join(parts[1:])
            self.player.use_item(item_name)
            # Re-check victory condition after using item (if it's the idol)
            self.check_victory()

        elif action in ["inventory", "i"]:
            self.player.show_inventory()

        elif action == "quit":
            print("Thanks for playing!")
            self.game_running = False

        else:
            print("I don't understand that command. Type 'help' for options.")

    def take_item(self, item_name):
        """Pick up an item from the current location."""
        found_item = None
        for item in self.current_location.items:
            if item_name.lower() in item.name.lower():
                found_item = item
                break
        
        if found_item:
            self.current_location.items.remove(found_item)
            self.player.pick_up(found_item)
            self.check_victory()
        else:
            print(f"There's no '{item_name}' here.")

    def check_victory(self):
        """Check if victory conditions are met."""
        has_idol = any(item.name == "Golden Kraken Idol" for item in self.player.inventory)
        if has_idol and self.current_location.name == "The Hidden Cove":
            self.state = Game.VICTORY

    def move(self, direction):
        """Move the player in the specified direction."""
        if direction in self.current_location.connections:
            self.current_location = self.current_location.connections[direction]
            self.current_location.describe()
            self.check_victory()
        else:
            print(f"You can't go {direction} from here.")

    def initiate_combat(self):
        """Start combat with an enemy in the current location."""
        if not self.current_location.enemies:
            print("There's nothing to fight here.")
            return

        enemy = self.current_location.enemies[0]  # Fight first enemy
        battle = Combat(self.player, enemy)
        result = battle.start()

        if result == "victory":
            self.current_location.enemies.remove(enemy)
        elif result == "defeat":
            self.state = Game.GAME_OVER

    def show_help(self):
        """Display available commands."""
        print("\nAVAILABLE COMMANDS:")
        print("  go [direction] - Move (north, south, east, west)")
        print("  look          - Examine surroundings")
        print("  fight         - Attack enemy")
        print("  take [item]   - Pick up an item")
        print("  use [item]    - Use an item from inventory")
        print("  inventory     - Check inventory")
        print("  help          - Show this help message")
        print("  quit          - Exit the game")

    def show_game_over(self):
        """Display game over message."""
        print("\n" + "="*60)
        print("                    GAME OVER")
        print("="*60)
        print("\nYou have been defeated. Your bones will bleach on the sands of Kraken's Cove.")
        print("\n(But you can always try again!)")

    def show_victory(self):
        """Display victory message."""
        print("\n" + "="*60)
        print("                    VICTORY!")
        print("="*60)
        print("\nYou have reclaimed the Golden Kraken Idol and brought it to the Hidden Cove!")
        print("Your name will be sung in pirate shanties for generations to come.")
        print("\nCongratulations, Pirate Lord!")


# =============================================================================
# Run the Game
# =============================================================================

if __name__ == "__main__":
    game = Game()
    game.start()
