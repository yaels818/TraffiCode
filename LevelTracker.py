"""
Author: Yael Sch
Description: LevelTracker module, contains definitions needed to track the game status
            (current level, time for each level, violations).
Notes: 
    
"""
# Imports
import time
from constants import WIN, CLIP_FONT, DASH_FONT, BLACK, RED, ORANGE, GREEN, CLIP_LEFT, CLIP_TOP, CLIP_CENTER, MIRROR_CENTER,MIRROR_POS, RBT_RIGHT_CENTER
#-------------------------------------------------------------------------
class LevelTracker():
    
    LEVELS = 10

    def __init__(self):
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
        self.level = 1
        self.level_started = False
        self.level_start_time = 0

        self.time_to_add_sprites = 0 

        self.sidewalk_hits = 0
        self.over_solid_lane = 0
        self.against_traffic = 0

        self.roundabout_hits = 0
        self.parking_lot_hits = 0
        self.parking_inaccurate = 0

    def increase_level(self):
        self.level += 1
        self.level_started = False
        self.level_start_time = 0

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

    def increase_time_to_add_sprites(self):
        self.time_to_add_sprites += 1

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
    
    def add_parking_inaccurate(self):
        self.parking_inaccurate += 1

    def reset(self):
        self.level = 1
        self.level_started = False
        self.level_start_time = 0

        self.sidewalk_hits = 0
        self.over_solid_lane = 0
        self.against_traffic = 0

        self.roundabout_hits = 0
        self.parking_lot_hits = 0
        self.parking_inaccurate = 0
    
    def display(self):
        """
        This method will be called automatically to display 
        the current feedback on top of the clipboard at the right side of the game window.
        """

        # generate texts to display
        timer_text = DASH_FONT.render(f"Time: {self.get_level_time()} sec", 1, BLACK)
        level_text = CLIP_FONT.render(f"Level {self.level}", 1, BLACK)

        sidewalk_hits_text = CLIP_FONT.render(f"Sidewalk hits: {self.sidewalk_hits}", 1, RED)
        against_traffic_text = CLIP_FONT.render(f"Wrong direction: {self.against_traffic}", 1, RED)
        over_solid_lane_text = CLIP_FONT.render(f"Over solid lanes: {self.over_solid_lane}", 1, RED)

        rbt_hits_text = CLIP_FONT.render(f"Roundabout hits: {self.roundabout_hits}", 1, RED)
        pl_hits_text = CLIP_FONT.render(f"Parking lot hits: {self.parking_lot_hits}", 1, RED)
        parking_inaccurate_text = CLIP_FONT.render(f"Inaccurate parking: {self.parking_inaccurate}", 1, ORANGE)


        # define position for each text, center by text rect center
        timer_text_pos = (MIRROR_CENTER-timer_text.get_rect().centerx,MIRROR_POS[1]+timer_text.get_rect().centery)
        level_text_pos = (CLIP_LEFT+0.5*level_text.get_rect().centerx,CLIP_TOP+level_text.get_rect().centery)
        
        texts_to_display = [(level_text, level_text_pos), 
                            (timer_text, timer_text_pos)]

        hit_texts = [sidewalk_hits_text, against_traffic_text, over_solid_lane_text,
                    rbt_hits_text, pl_hits_text, parking_inaccurate_text]
                    
        line_space = -3
        for t in hit_texts:
            pos = (CLIP_CENTER-t.get_rect().centerx, RBT_RIGHT_CENTER[1]+line_space*t.get_rect().centery)
            line_space += 2.5
            texts_to_display.append((t,pos))
        
        for txt, pos in texts_to_display:
            # Draw this img in this position
            WIN.blit(txt, pos)  
        