"""
Author: @yaels818
Description: LevelTracker module, contains definitions needed to track the game status
            (current level, time for each level, violations, good behavior).
Notes: 
    
"""
# Imports
import time
from constants import WIN, CLIP_FONT, DASH_FONT, BLACK, RED, ORANGE, GREEN, GRAY, \
    CLIP_LEFT, CLIP_TOP, CLIP_CENTER, MIRROR_CENTER,MIRROR_POS, RBT_RIGHT_CENTER
#-------------------------------------------------------------------------
class LevelTracker():
    
    LEVELS = 10

    def __init__(self, start_level = 1, sprites_vel = 0.5, time_bet_peds = 5, time_bet_cars = 6):
        """
        Parameters
        ----------
        level : int
            The current level of the game (default is 1)
        level_started : bool
            If the current level started (default is False)
        level_start_time : int
            How many seconds passed since the level started (default is 0)
        time_to_add_sprites : int
            Keeps track of when to add new sprites like peds and other cars to the game
            (increases every seconds)
        
        """
        self.level = start_level
        self.level_started = False
        self.level_start_time = 0

        self.timer_to_add_sprites = 0 
        self.peds_vel = sprites_vel
        self.cars_vel = sprites_vel + 0.2
        self.time_between_peds = time_bet_peds
        self.time_between_cars = time_bet_cars

        self.peds_hits = 0
        self.cars_hits = 0

        self.sidewalk_hits = 0
        self.over_solid_lane = 0
        self.against_traffic = 0

        self.roundabout_hits = 0
        self.parking_lot_hits = 0
        
        self.accurate_parking = 0

        self.tracking_table = []

    def increase_level(self):

        if self.tracking_table == []:
            self.tracking_table.append(["Level", 
                                    "Time (Seconds)",
                                    "Peds hits", 
                                    "Cars hits", 
                                    "Sidewalk hits", 
                                    "Over solid lane", 
                                    "Against traffic",
                                    "Roundabout hits", 
                                    "Parking lot hits", 
                                    "Accurate parking ( /4)"])

        self.tracking_table.append([self.level, 
                                    self.get_level_time(),
                                    self.peds_hits, 
                                    self.cars_hits, 
                                    self.sidewalk_hits, 
                                    self.over_solid_lane, 
                                    self.against_traffic,
                                    self.roundabout_hits, 
                                    self.parking_lot_hits, 
                                    self.accurate_parking])

        self.level += 1
        self.level_started = False
        self.level_start_time = 0

        # If this is an even-number level (2, 4, 6, 8, 10, etc..)
        if self.level % 2 == 0:
            # Increase the peds and other cars velocity
            self.peds_vel += 0.1
            self.cars_vel += 0.1
        else:
            # Decrease time between generating peds and cars sprites
            if self.time_between_peds > 2:
                self.time_between_peds -= 1
            if self.time_between_cars > 2:
                self.time_between_cars -= 1

    def start_level(self):
        self.level_started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.level_started:
            return 0
        else:
            # round to a whole number
            return round(time.time() - self.level_start_time) 

    def game_finished(self):
        return self.level > self.LEVELS

    def increase_timer_to_add_sprites(self):
        self.timer_to_add_sprites += 1

    def add_ped_hit(self):
        self.peds_hits += 1

    def add_car_hit(self):
        self.cars_hits += 1

    def add_sidewalk_hit(self):
        self.sidewalk_hits += 1

    def add_over_solid_lane(self):
        self.over_solid_lane += 1

    def add_driving_against_traffic(self):
        self.against_traffic += 1

    def add_roundabout_hit(self):
        self.roundabout_hits += 1
    
    def add_parking_lot_hit(self):
        self.parking_lot_hits += 1
    
    def add_accurate_parking(self):
        self.accurate_parking += 1

    def reset(self, start_level = 1, sprites_vel = 0.5, time_bet_peds = 5, time_bet_cars = 6):
        self.level = start_level
        self.level_started = False
        self.level_start_time = 0

        self.timer_to_add_sprites = 0 
        self.peds_vel = sprites_vel
        self.cars_vel = sprites_vel + 0.2
        self.time_between_peds = time_bet_peds
        self.time_between_cars = time_bet_cars

        self.peds_hits = 0
        self.cars_hits = 0

        self.sidewalk_hits = 0
        self.over_solid_lane = 0
        self.against_traffic = 0

        self.roundabout_hits = 0
        self.parking_lot_hits = 0
        self.accurate_parking = 0

        self.tracking_table = []
    
    def display_score(self):
        """
        This method will be called to display the current score 
        (on top of the clipboard at the right side of the game window).
        """

        # generate texts to display
        timer_text = DASH_FONT.render(f"Time: {self.get_level_time()} sec", 1, BLACK)
        level_text = CLIP_FONT.render(f"Level {self.level}", 1, BLACK)

        peds_hits_text = CLIP_FONT.render(f"Pedestrians hits: {self.peds_hits}", 1, RED)
        cars_hits_text = CLIP_FONT.render(f"Other cars hits: {self.cars_hits}", 1, RED)

        sidewalk_hits_text = CLIP_FONT.render(f"Sidewalk hits: {self.sidewalk_hits}", 1, ORANGE)
        over_solid_lane_text = CLIP_FONT.render(f"Over solid lanes: {self.over_solid_lane}", 1, ORANGE)
        against_traffic_text = CLIP_FONT.render(f"Wrong direction: {self.against_traffic}", 1, ORANGE)

        rbt_hits_text = CLIP_FONT.render(f"Roundabout hits: {self.roundabout_hits}", 1, ORANGE)
        pl_hits_text = CLIP_FONT.render(f"Parking lot hits: {self.parking_lot_hits}", 1, ORANGE)
        
        accurate_parking_text = CLIP_FONT.render(f"Accurate parking: {self.accurate_parking}", 1, GREEN)

        # define position for each text, center by text rect center
        timer_text_pos = (MIRROR_CENTER-timer_text.get_rect().centerx,MIRROR_POS[1]+timer_text.get_rect().centery)
        level_text_pos = (CLIP_LEFT+0.5*level_text.get_rect().centerx,CLIP_TOP+level_text.get_rect().centery/8)
        
        texts_to_display = [(level_text, level_text_pos), 
                            (timer_text, timer_text_pos)]

        accident_texts = [peds_hits_text, cars_hits_text]
        
        hit_texts = [sidewalk_hits_text, over_solid_lane_text, 
                    against_traffic_text,
                    rbt_hits_text, pl_hits_text]

        bonus_texts = [accurate_parking_text]

        line_space = -4
        for t in accident_texts:
            pos = (CLIP_CENTER-t.get_rect().centerx, RBT_RIGHT_CENTER[1]+line_space*t.get_rect().centery)
            line_space += 2.5
            texts_to_display.append((t,pos))
        
        line_space += 3
        for t in hit_texts:
            pos = (CLIP_CENTER-t.get_rect().centerx, RBT_RIGHT_CENTER[1]+line_space*t.get_rect().centery)
            line_space += 2.5
            texts_to_display.append((t,pos))
        
        line_space += 3
        for t in bonus_texts:
            pos = (CLIP_CENTER-t.get_rect().centerx, RBT_RIGHT_CENTER[1]+line_space*t.get_rect().centery)
            line_space += 2.5
            texts_to_display.append((t,pos))

        for txt, pos in texts_to_display:
            # Draw this img in this position
            WIN.blit(txt, pos)  
        
    def display_instructions(self):
        """
        This method will be called to display the instructions for the current level
        (on top of the clipboard at the right side of the game window).
        """

        TEXT_LINES = [  "Cross the finish line.", 
                        "Mind the traffic codes.",
                        "Try not to drive ",
                        "against traffic."]

        PARK_LINES = [  "Park in the orange spot.",
                        "Press P when ",
                        "you are done."]
        
        # generate texts to display
        timer_text = DASH_FONT.render(f"Time: {self.get_level_time()} sec", 1, BLACK)
        level_text = CLIP_FONT.render(f"Level {self.level}", 1, BLACK)

        # define position for each text, center by text rect center
        timer_text_pos = (MIRROR_CENTER-timer_text.get_rect().centerx,MIRROR_POS[1]+timer_text.get_rect().centery)
        level_text_pos = (CLIP_LEFT+0.5*level_text.get_rect().centerx,CLIP_TOP+level_text.get_rect().centery/8)
        
        texts_to_display = [(level_text, level_text_pos),
                            (timer_text, timer_text_pos)]

        line_space = -2

        if self.level in [4,7,9,10]:
            lines = PARK_LINES
            if self.level == 4:
                lines.append("")
                lines.append("No need to park")
                lines.append("in reverse.")
            elif self.level == 10:
                lines.append("")
                lines.append("Park in reverse.")
        else:
            lines = TEXT_LINES
        
        for line in lines:
            t = CLIP_FONT.render(line, 1, GRAY)
            pos = (CLIP_CENTER-t.get_rect().centerx, RBT_RIGHT_CENTER[1]+line_space*t.get_rect().centery)
            line_space += 2.5
            texts_to_display.append((t,pos))
            

        for txt, pos in texts_to_display:
            # Draw this img in this position
            WIN.blit(txt, pos)  