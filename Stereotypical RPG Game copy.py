import json
import random
import copy

default_player = {
    'inventory': {
        'sword': 1,
        'potion': 5,
        'gold': 150
    },
    'stats': {
        'health': 250,
        'max_health': 250,
        'attack': 15,
        'defense': 15,
    },
    'equipment': {
        'helmet': None,
        'chestplate': None,
        'boots': None,
        'shield': None
    }
}

shop_prices = {
    'sword': 50,
    'potion': 10,
}

sell_prices = {
    'sword': 25,
    'potion': 5
}

armour_sell_prices = {
    'bronze': 10,
    'chainmail': 15,
    'silver': 25,
    'gold': 60
}

armour_stats = {
    'bronze': 1,
    'chainmail': 2,
    'silver': 3,
    'gold': 6
}

slot_multiplier = {
    'helmet': 2,
    'chestplate': 3,
    'boots': 1,
    'shield': 3
}

tier_rank = {
    'bronze': 1,
    'chainmail' : 2,
    'silver': 3,
    'gold': 4
}

sword_stats = {
    'bronze': 5,
    'chainmail': 10,
    'silver': 20,
    'gold': 40
    }

enemies = {
    'goblin': {
        'name': 'Goblin',
        'health': 50,
        'attack': 10,
        'defense': 7,
        'gold_reward': (7,12),
        'loot': {
            'potion': 0.1,
            'sword': 0.05,
            'shield': {
                'bronze': 0.25
            },
            'helmet': {
                'bronze': 0.3
            },
            'chestplate': {
                'bronze': 0.3
            },
            'boots': {
                'bronze': 0.3
            }
        }
    },

    'troll': {
        'name': 'Troll',
        'health': 100,
        'attack': 40,
        'defense': 12,
        'gold_reward': (20,30),
        'loot': {
            'potion': 0.25,
            'sword': 0.15,
            'shield': {
                'bronze': 0.4,
                'chainmail': 0.2
            },
            'helmet': {
                'bronze': 0.4,
                'chainmail': 0.2
            },
            'chestplate': {
                'bronze': 0.4,
                'chainmail': 0.2
            },
            'boots': {
                'bronze': 0.4,
                'chainmail': 0.2
            }
        }
    },

    'dragon': {
        'name': 'Dragon',
        'health': 300,
        'attack': 150,
        'defense': 25,
        'gold_reward': (30,60),
        'loot': {
            'potion': 0.75,
            'sword': 0.5,
            'shield': {
                'bronze': 0.625,
                'chainmail': 0.5,
                'silver': 0.25
            },
            'helmet': {
                'bronze': 0.625,
                'chainmail': 0.5,
                'silver': 0.25
            },
            'chestplate': {
                'bronze': 0.625,
                'chainmail': 0.5,
                'silver': 0.25
            },
            'boots': {
                'bronze': 0.625,
                'chainmail': 0.5,
                'silver': 0.25
            }
        }
    },
    'ancient_dragon': {
        'name': 'Ancient Dragon',
        'health': 550,
        'attack': 250,
        'defense': 100,
        'gold_reward': (100,200),
        'loot': {
            'potion': 0.9,
            'sword': 0.75,
            'shield': {
                'bronze': 0.9,
                'chainmail': 0.8,
                'silver': 0.5,
                'gold': 0.05
            },
            'helmet': {
                'bronze': 0.9,
                'chainmail': 0.8,
                'silver': 0.5,
                'gold': 0.05
            },
            'chestplate': {
                'bronze': 0.9,
                'chainmail': 0.8,
                'silver': 0.5,
                'gold': 0.05
            },
            'boots': {
                'bronze': 0.9,
                'chainmail': 0.8,
                'silver': 0.5,
                'gold': 0.05
            }
        }
    }
}

def save_player(player):
    with open('player.json', 'w') as file:
        json.dump(player, file)
    print('File successfully saved!')

def load_player():
    try:
        with open('player.json', 'r') as file:
            player = json.load(file)
        print('File successfully loaded!')
        return player
    except FileNotFoundError:
        print('No save file found! Starting fresh...')
        return copy.deepcopy(default_player)



def display(player):
    print('\n==INVENTORY==')
    for item in player['inventory']:
        print(f'{item} : {player["inventory"][item]}')

    print('\n==STATS==')
    print(f'Health : {player["stats"]["health"]}/{player["stats"]["max_health"]}')
    print(f'Attack : {player["stats"]["attack"]}')
    print(f'Defense: {player["stats"]["defense"]}')

    print('\n==EQUIPMENT==')
    for slot, item in player['equipment'].items():
        print(f'{slot} : {item}')

def heal(player):
    quantity = input('How many potions do you want to use?')

    if type(quantity) != int:
        print('Not an integer')
    else:
        quantity_int = int(quantity)

    if 'potion' not in player['inventory']:
        print('You do not have a potion')
        return

    player['inventory']['potion'] -= quantity_int

    
    heal = 30 * quantity_int
    player['stats']['health'] = min(
        player['stats']['health'] + heal,
        player['stats']['max_health']
    )
    print(f'Healed {heal} HP!')


    if player['inventory']['potion'] <= 0:
        del player['inventory']['potion']

    display(player)

def equip(player):
    display(player)

    item = input('What do you want to equip? ')

    if player['inventory'].get(item, 0) <= 0:
        print('You do not have that item.')
        return

    if '_' not in item:
        print('Not equippable.')
        return

    tier, slot = item.split('_', 1)

    if slot not in player['equipment']:
        print('Invalid slot.')
        return

    old = player['equipment'][slot]
    if old:
        player['inventory'][old] = player['inventory'].get(old, 0) + 1

    player['equipment'][slot] = item
    player['inventory'][item] -= 1

    if player['inventory'][item] <= 0:
        del player['inventory'][item]

    display(player)

def buy(player, shop_prices):
    display(player)

    item = input('Buy what? ')
    quantity = input('How many?')

    if type(quantity) != int:
        print('That is not a number')
        return
    else:
        quantity_int = int(quantity)

    if item not in shop_prices:
        print('Not sold here.')
        return

    cost = shop_prices[item] * quantity_int

    if player['inventory'].get('gold', 0) < cost:
        print('Not enough gold.')
        return

    player['inventory'][item] = player['inventory'].get(item, 0) + quantity_int
    player['inventory']['gold'] -= cost * quantity_int

    print(f'Bought {quantity_int} {item}!')



def sell(player, sell_prices, armour_sell_prices):
    display(player)

    item = input('Sell what? ')

    if item not in player['inventory']:
        print('You do not have that.')
        return

    quantity = input('How many? ')

    if type(quantity) != int:
        print('Not an integer')
        return
    else:
        quantity_int = int(quantity)

    if quantity_int > player['inventory'][item]:
        print('Not enough items.')
        return

    if '_' in item:
        tier = item.split('_')[0]
        price = armour_sell_prices.get(tier, 0)
    else:
        price = sell_prices.get(item, 0)

    player['inventory'][item] -= quantity_int
    player['inventory']['gold'] += price * quantity_int

    if player['inventory'][item] <= 0:
        del player['inventory'][item]

    print(f'Sold {quantity_int} {item}!')



def get_enemy(enemies):
    name_of_enemy_random = random.choice(['goblin', 'goblin',  'goblin', 'troll', 'troll', 'troll', 'dragon', 'dragon', 'ancient_dragon'])
    enemy = enemies[name_of_enemy_random].copy()
    return enemy

def get_total_defense(player):
    defense = player['stats']['defense']

    for slot in player['equipment']:
        item = player['equipment'][slot]

        if item:
            tier, item_slot = item.split('_', 1)

            base = armour_stats.get(tier, 0)
            multiplier = slot_multiplier.get(item_slot, 1)

            defense += base * multiplier

    return defense

def calculate_damage(atk, defence):
    return max(0, atk - defence)

def get_total_attack(player):
    base_attack = player['stats']['attack']
    sword_count = player['inventory'].get('sword', 0)

    bonus = sword_count * 5

    return base_attack + bonus

def enemy_attack(player, enemy):
    dmg = calculate_damage(enemy['attack'], get_total_defense(player))
    player['stats']['health'] -= dmg
    print(f'{enemy["name"]} hits for {dmg}')

def player_attack(player, enemy):
    dmg = calculate_damage(get_total_attack(player), enemy['defense'])
    enemy['health'] -= dmg
    print(f'You hit for {dmg}')

def roll_loot(loot_table, player):
    dropped = False

    for item, value in loot_table.items():

        if isinstance(value, float) or isinstance(value, int):
            if random.random() < value:
                player['inventory'][item] = player['inventory'].get(item, 0) + 1
                print(f'{item} dropped!')
                dropped = True

        elif isinstance(value, dict):
            for tier, chance in value.items():
                if random.random() < chance:
                    full_item = f'{tier}_{item}'
                    player['inventory'][full_item] = player['inventory'].get(full_item, 0) + 1
                    print(f'{full_item} dropped!')
                    dropped = True

    if not dropped:
        print('No loot dropped this time.')

    auto_equip_best_armor(player)

def respawn(player):
    player['stats']['health'] = player['stats']['max_health']
    player['inventory']['gold'] -= 25

def combat(player, enemy):
    print(f'A wild {enemy["name"]} appears!')

    while player['stats']['health'] > 0 and enemy['health'] > 0:

        player_attack(player, enemy)
        if enemy['health'] <= 0:
            print('YOU WIN!')
            gold = get_gold_reward(enemy)
            print(f'{enemy["name"]} dropped {gold} gold!')
            player['inventory']['gold'] += gold
            roll_loot(enemy['loot'], player)
            return True

        enemy_attack(player, enemy)
        if player['stats']['health'] <= 0:
            print('YOU DIED')
            respawn(player)
            return False

def get_gold_reward(enemy):
    reward = enemy['gold_reward']

    if isinstance(reward, tuple):
        return random.randint(reward[0], reward[1])

    return reward

def get_armor_value(item):
    tier = item.split('_')[0]
    return tier_rank.get(tier, 0)

def auto_equip_best_armor(player):
    best = {
        'helmet': None,
        'chestplate': None,
        'boots': None,
        'shield': None
    }

    for item, qty in player['inventory'].items():

        if '_' not in item:
            continue

        tier, slot = item.split('_', 1)

        if slot not in best:
            continue


        if best[slot] is None:
            best[slot] = item
        else:
            current_best_tier = best[slot].split('_')[0]
            if tier_rank[tier] > tier_rank[current_best_tier]:
                best[slot] = item

    for slot, new_item in best.items():

        if not new_item:
            continue

        old_item = player['equipment'][slot]

        if old_item:
            player['inventory'][old_item] = player['inventory'].get(old_item, 0) + 1

        player['inventory'][new_item] -= 1
        if player['inventory'][new_item] <= 0:
            del player['inventory'][new_item]

        player['equipment'][slot] = new_item

    print('Auto-equipped best armor!')

def main_menu(player, shop_prices, sell_prices, enemies, armour_sell_prices):
    while True:
        print('\n==MAIN MENU==')
        choice = input('1. Inventory\n2. Heal\n3. Buy\n4. Sell\n5. Fight\n6. Equip\n7. Exit\n')

        if choice == '1':
            display(player)

        elif choice == '2':
            heal(player)

        elif choice == '3':
            buy(player, shop_prices)

        elif choice == '4':
            sell(player, sell_prices, armour_sell_prices)

        elif choice == '5':
            enemy = get_enemy(enemies)
            combat(player, enemy)

        elif choice == '6':
            equip(player)

        elif choice == '7':
            save_player(player)
            print('Bye!')
            break

player = load_player()
main_menu(player, shop_prices, sell_prices, enemies, armour_sell_prices)
