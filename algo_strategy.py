import gamelib
import random
import math
import warnings
from sys import maxsize
import json


"""
Most of the algo code you write will be in this file unless you create new
modules yourself. Start by modifying the 'on_turn' function.
Advanced strategy tips: 
  - You can analyze action frames by modifying on_action_frame function
  - The GameState.map object can be manually manipulated to create hypothetical 
  board states. Though, we recommended making a copy of the map to preserve 
  the actual current map state.
"""

class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('Random seed: {}'.format(seed))

    def on_game_start(self, config):
        """ 
        Read in config and perform any initial setup here 
        """
        gamelib.debug_write('Configuring your custom algo strategy...')
        self.config = config
        global FILTER, ENCRYPTOR, DESTRUCTOR, PING, EMP, SCRAMBLER
        FILTER = config["unitInformation"][0]["shorthand"]
        ENCRYPTOR = config["unitInformation"][1]["shorthand"]
        DESTRUCTOR = config["unitInformation"][2]["shorthand"]
        PING = config["unitInformation"][3]["shorthand"]
        EMP = config["unitInformation"][4]["shorthand"]
        SCRAMBLER = config["unitInformation"][5]["shorthand"]
        # This is a good place to do initial setup
        self.scored_on_locations = []

    
        

    def on_turn(self, turn_state):
        """
        This function is called every turn with the game state wrapper as
        an argument. The wrapper stores the state of the arena and has methods
        for querying its state, allocating your current resources as planned
        unit deployments, and transmitting your intended deployments to the
        game engine.
        """
        game_state = gamelib.GameState(self.config, turn_state)
        gamelib.debug_write('Performing turn {} of your custom algo strategy'.format(game_state.turn_number))
        game_state.suppress_warnings(True)  #Comment or remove this line to enable warnings.

        self.starter_strategy(game_state)

        game_state.submit_turn()


    """
    NOTE: All the methods after this point are part of the sample starter-algo
    strategy and can safely be replaced for your custom algo.
    """


    def starter_strategy(self, game_state):


        blackbeardR1 = False
        blackbeardR2 = False
        blackbeardL1 = False
        blackbeardL2 = False
        hellfire1 = False
        hellfire2 = False

        if self.is_dec_diagonal(game_state, 16, 23, 23, 16):
            blackbeardR1 = True

        if self.is_dec_diagonal(game_state, 16, 22, 23, 15):
            blackbeardR2 = True

        if self.is_inc_diagonal(game_state, 4, 16, 11, 23):
            blackbeardL1 = True

        if self.is_inc_diagonal(game_state, 4, 15, 11, 22):
            blackbeardL2 = True

        if self.is_horizontal(game_state, 5, 16, 16, 16):
            hellfire2 = True

        if self.is_horizontal(game_state, 5, 15, 16, 15):
            hellfire1 = True

        if blackbeardR1 or blackbeardR2:
            self.build_blackbeardR_defences(game_state)

        if blackbeardL1 or blackbeardL2:
            self.build_blackbeardL_defences(game_state)

        if hellfire1 or hellfire2:
            self.build_blackbeardR_defences(game_state)
            self.build_blackbeardL_defences(game_state)

        # strategic attack -- can be changed
        if blackbeardR1 or blackbeardR2:
            game_state.attempt_spawn(PING, [15, 1], 1000)
                
        if blackbeardL1 or blackbeardL2:
            game_state.attempt_spawn(PING, [12, 1], 1000)
                
        self.build_defences(game_state)
        
        self.start_with_scramblers(game_state)

        """
        # Here is the main attack strategy - needs to be improved with removing units then attacking
        if game_state.get_resource(game_state.BITS) >= 5 * game_state.type_cost(EMP) and game_state.turn_number % 2 == 0:
            if blackbeardR1 or blackbeardR2:
                game_state.attempt_spawn(EMP, [15, 1], 1000)
            elif blackbeardL1 or blackbeardL2:
                game_state.attempt_spawn(EMP, [12, 1], 1000)
            else:
                game_state.attempt_spawn(EMP, [15, 1], 1000)
       
        """

        new_filter_locations = [[8, 9]]
        game_state.attempt_spawn(FILTER, new_filter_locations)

        new_filter_locations = [[19, 9]]
        game_state.attempt_spawn(FILTER, new_filter_locations)
        
        new_filter_locations = [[9, 9]]
        game_state.attempt_spawn(FILTER, new_filter_locations)
        
        new_filter_locations = [[18, 9]]
        game_state.attempt_spawn(FILTER, new_filter_locations)

        new_destructor_locations = [[9, 8], [10, 8]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)

        new_destructor_locations = [[18, 8], [17, 8]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)

        new_destructor_locations = [[9, 7], [10, 7]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)

        new_destructor_locations = [[18, 7], [17, 7]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)

        ENCRYPTOR_ON = False
        if game_state.get_resource(game_state.CORES) >= 7 * game_state.type_cost(ENCRYPTOR):
            encryptor_locations = [[4, 11], [5, 10], [6, 9], [7, 8], [8, 7], [9, 6], [10, 5], [11, 4], [4, 12], [3, 13], [5, 11], [6, 10], [7, 9], [10, 6], [11, 6], [11, 5], [12, 6]]
            game_state.attempt_spawn(ENCRYPTOR, encryptor_locations)
            ENCRYPTOR_ON = True

        new_destructor_locations = [[18, 11], [19, 11], [20, 11]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)
        new_destructor_locations = [[18, 11], [19, 10], [20, 10]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)
        new_destructor_locations = [[15, 5], [16, 5], [17, 5]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)
        new_filter_locations = [[16, 6], [17, 6], [18, 6]]
        game_state.attempt_spawn(FILTER, new_filter_locations)
        new_destructor_locations = [[15, 4], [16, 4], [17, 4]]
        game_state.attempt_spawn(DESTRUCTOR, new_destructor_locations)

        # attacking 
        if game_state.turn_number > 7 and game_state.turn_number % 4 == 0:
            self.emp_attack(game_state)
        else:
            self.start_with_scramblers(game_state)


    def build_defences(self, game_state):
        filter_locations = [[0, 13], [1, 13], [2, 13], [3, 12], [4, 13], [5, 12],
                            [27, 13], [26, 13], [25, 13], [24, 12], [23, 13], [22, 12]]
        game_state.attempt_spawn(FILTER, filter_locations)

        destructor_locations = [[8, 8], [19, 8], [11, 7], [16, 7]]
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)

        if game_state.get_resource(game_state.CORES) >= game_state.type_cost(FILTER):
            new_filter_locations = [[6, 11]]
            game_state.attempt_spawn(FILTER, new_filter_locations)

        if game_state.get_resource(game_state.CORES) >= game_state.type_cost(FILTER):
            new_filter_locations = [[21, 11]]
            game_state.attempt_spawn(FILTER, new_filter_locations)

        if game_state.get_resource(game_state.CORES) >= game_state.type_cost(FILTER):
            new_filter_locations = [[7, 10]]
            game_state.attempt_spawn(FILTER, new_filter_locations)

        if game_state.get_resource(game_state.CORES) >= game_state.type_cost(FILTER):
            new_filter_locations = [[20, 10]]
            game_state.attempt_spawn(FILTER, new_filter_locations)

        


    def advanced_build_defences(self, game_state):
        destructor_locations = [[0, 13], [1, 13], [2, 13], [3, 12], [4, 13], [4, 11], [5, 12], [6, 11], [7, 10], [8, 9], [9, 8], [10, 8], [11, 8],
                            [27, 13], [26, 13], [25, 13], [24, 12], [23, 13], [23, 11], [22, 12], [21, 11], [20, 10], [19, 9], [18, 8], [17, 8], [16, 8]]
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)

        filter_locations = [[0, 13], [1, 13], [2, 13], [3, 12], [4, 13], [4, 11], [5, 12], [6, 11], [7, 10], [8, 9], [9, 8], [10, 8], [11, 8],
                            [27, 13], [26, 13], [25, 13], [24, 12], [23, 13], [23, 11], [22, 12], [21, 11], [20, 10], [19, 9], [18, 8], [17, 8], [16, 8]]
        game_state.attempt_spawn(FILTER, filter_locations)

    def build_blackbeardR_defences(self, game_state):
        destructor_locations = [[26, 12], [25, 12], [25, 11], [24, 13], [24, 11]]
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)


    def build_blackbeardL_defences(self, game_state):
        destructor_locations = [[1, 12], [2, 12], [2, 11], [3, 13], [3, 11]]
        game_state.attempt_spawn(DESTRUCTOR, destructor_locations)
    

    def build_reactive_defense(self, game_state):
        """
        This function builds reactive defenses based on where the enemy scored on us from.
        We can track where the opponent scored by looking at events in action frames 
        as shown in the on_action_frame function
        """
        for location in self.scored_on_locations:
            # Build destructor one space above so that it doesn't block our own edge spawn locations
            build_location = [location[0], location[1]+1]
            game_state.attempt_spawn(DESTRUCTOR, build_location)
            build_location = [location[0]+1, location[1]+1]
            game_state.attempt_spawn(DESTRUCTOR, build_location)
            build_location = [location[0]+1, location[1]]
            game_state.attempt_spawn(DESTRUCTOR, build_location)
            build_location = [location[0]-1, location[1]]
            game_state.attempt_spawn(DESTRUCTOR, build_location)


    def is_inc_diagonal(self, game_state, x1, y1, x2, y2):
        # must be valid inputs for this to work
        # x1 < x2, y1 < y2
        num = 0
        check_x = x1
        check_y = y1
        while check_x <= x2:
            if (game_state.game_map[check_x, check_y] != []):
                num += 1
            check_x += 1
            check_y += 1
        if num > 6:
            return True
        else:
            return False


    def is_dec_diagonal(self, game_state, x1, y1, x2, y2):
        # must be valid inputs for this to work
        # x1 < x2, y1 > y2
        num = 0
        check_x = x1
        check_y = y1
        while check_x <= x2:
            if (game_state.game_map[check_x, check_y] != []):
                num += 1
            check_x += 1
            check_y -= 1
        if num > 6:
            return True
        else:
            return False


    def is_horizontal(self, game_state, x1, y1, x2, y2):
        # must be valid inputs for this to work
        # x1 < x2, y1 = y2
        num = 0
        check_x = x1
        check_y = y1
        while check_x <= x2:
            if (game_state.game_map[check_x, check_y] != []):
                num += 1
            check_x += 1
        if num > 8:
            return True
        else:
            return False


    def start_with_scramblers(self, game_state):
      
        deploy_locations = [[5, 8], [22, 8], [11, 2]]     
        game_state.attempt_spawn(SCRAMBLER, deploy_locations)
            

    def emp_attack(self, game_state):
        deploy_locations = [[4, 9]]
        num_EMP = 5
        game_state.attempt_spawn(EMP, deploy_locations, num_EMP)

        deploy_locations = [4, 9]
        num_ping = 1000
        game_state.attempt_spawn(PING, deploy_locations, num_ping)
        
    def emp_line_strategy(self, game_state):
        """
        Build a line of the cheapest stationary unit so our EMP's can attack from long range.
        
        # First let's figure out the cheapest unit
        # We could just check the game rules, but this demonstrates how to use the GameUnit class
        stationary_units = [FILTER, DESTRUCTOR, ENCRYPTOR]
        cheapest_unit = FILTER
        for unit in stationary_units:
            unit_class = gamelib.GameUnit(unit, game_state.config)
            if unit_class.cost < gamelib.GameUnit(cheapest_unit, game_state.config).cost:
                cheapest_unit = unit
        # Now let's build out a line of stationary units. This will prevent our EMPs from running into the enemy base.
        # Instead they will stay at the perfect distance to attack the front two rows of the enemy base.
        for x in range(27, 5, -1):
            game_state.attempt_spawn(cheapest_unit, [x, 11])
        """
        # Now spawn EMPs next to the line
        # By asking attempt_spawn to spawn 1000 units, it will essentially spawn as many as we have resources for
        game_state.attempt_spawn(EMP, [13, 0], 1000)

        
    def least_damage_spawn_location(self, game_state, location_options):
        """
        This function will help us guess which location is the safest to spawn moving units from.
        It gets the path the unit will take then checks locations on that path to 
        estimate the path's damage risk.
        """
        damages = []
        # Get the damage estimate each path will take
        for location in location_options:
            path = game_state.find_path_to_edge(location)
            damage = 0
            for path_location in path:
                # Get number of enemy destructors that can attack the final location and multiply by destructor damage
                damage += len(game_state.get_attackers(path_location, 0)) * gamelib.GameUnit(DESTRUCTOR, game_state.config).damage
            damages.append(damage)
        
        # Now just return the location that takes the least damage
        return location_options[damages.index(min(damages))]

    def detect_enemy_unit(self, game_state, unit_type=None, valid_x = None, valid_y = None):
        total_units = 0
        for location in game_state.game_map:
            if game_state.contains_stationary_unit(location):
                for unit in game_state.game_map[location]:
                    if unit.player_index == 1 and (unit_type is None or unit.unit_type == unit_type) and (valid_x is None or location[0] in valid_x) and (valid_y is None or location[1] in valid_y):
                        total_units += 1
        return total_units
        
    def filter_blocked_locations(self, locations, game_state):
        filtered = []
        for location in locations:
            if not game_state.contains_stationary_unit(location):
                filtered.append(location)
        return filtered

    def on_action_frame(self, turn_string):
        """
        This is the action frame of the game. This function could be called 
        hundreds of times per turn and could slow the algo down so avoid putting slow code here.
        Processing the action frames is complicated so we only suggest it if you have time and experience.
        Full doc on format of a game frame at: https://docs.c1games.com/json-docs.html
        """
        # Let's record at what position we get scored on
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        for breach in breaches:
            location = breach[0]
            unit_owner_self = True if breach[4] == 1 else False
            # When parsing the frame data directly, 
            # 1 is integer for yourself, 2 is opponent (StarterKit code uses 0, 1 as player_index instead)
            if not unit_owner_self:
                gamelib.debug_write("Got scored on at: {}".format(location))
                self.scored_on_locations.append(location)
                gamelib.debug_write("All locations: {}".format(self.scored_on_locations))


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
