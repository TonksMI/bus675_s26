# Game Design Document: The Legend of Kraken's Cove

## Theme / Setting
Pirate Adventure. The player is a young buccaneer seeking the legendary treasure of Captain Blackbeard, hidden somewhere in the mysterious Kraken's Cove.

## Player's Goal
Navigate through treacherous waters and islands, defeat Blackbeard's ghost and his crew, and claim the Golden Kraken Idol to win the game.

## Locations (11)
1. Port Royal: The bustling naval base where you start.
2. Tortuga Tavern: A rowdy pirate hangout.
3. The Jolly Roger: Your trusty ship.
4. Siren's Reef: Dangerous waters with haunting music.
5. Mermaid's Lagoon: A beautiful but treacherous lagoon.
6. Shipwreck Graveyard: Haunted waters filled with sunken ships.
7. Skull Island: A dark island with thick jungle.
8. Cannibal Island: A dangerous place where the locals are hungry.
9. The Foggy Marsh: A thick, swampy area near the cave.
10. Blackbeard's Cave: The final boss lair.
11. The Hidden Cove: The final victory destination.

### Interconnected Map Connections:
- **Port Royal**: Hub connecting to Tortuga Tavern (W), Jolly Roger (E), Siren's Reef (N), Mermaid's Lagoon (S).
- **Tortuga Tavern**: Connects to Port Royal (E), Shipwreck Graveyard (S).
- **The Jolly Roger**: Connects to Port Royal (W), Shipwreck Graveyard (S).
- **Siren's Reef**: Connects to Port Royal (S), Skull Island (W).
- **Mermaid's Lagoon**: Connects to Port Royal (N), Cannibal Island (W).
- **Shipwreck Graveyard**: Connects to Tortuga Tavern (N), Jolly Roger (E), Cannibal Island (S), Skull Island (W).
- **Skull Island**: Connects to Siren's Reef (E), Shipwreck Graveyard (S), Foggy Marsh (W).
- **Cannibal Island**: Connects to Mermaid's Lagoon (E), Shipwreck Graveyard (N), Foggy Marsh (W).
- **The Foggy Marsh**: Connects to Skull Island (N), Cannibal Island (S), Blackbeard's Cave (W).
- **Blackbeard's Cave**: Connects to Foggy Marsh (E), Hidden Cove (N).
- **The Hidden Cove**: Connects to Blackbeard's Cave (S).

## Enemies (5 types)
1. Scurvy Rat: Fast but weak. (Minion)
2. Drunken Sailor: Low health, low damage. (Minion)
3. Siren: High defense, uses charming songs (high damage). (Elite)
4. Ghost Pirate: High health, hard to hit. (Elite)
5. Captain Blackbeard: The Boss. High health, high damage, high defense.

## Win Condition
Defeat Captain Blackbeard and reach The Hidden Cove with the Golden Kraken Idol.

## Lose Condition
The player's health reaches 0.

## Class Hierarchy
Character (base class)
Player
Enemy
- DrunkenSailor (Minion)
- Siren (Elite)
- GhostPirate (Elite)
- Blackbeard (Boss)
Item
Location
Game

## Functional Items
- Bottle of Rum: Restores 20 health.
- Old Grog: Restores 10 health.
- Scurvy Biscuit: Restores 5 health.
- Golden Kraken Idol: Quest item for victory.
