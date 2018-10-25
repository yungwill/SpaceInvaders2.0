class GameStats:
    """tracks statistics for Alien Invasion"""

    def __init__(self, ai_settings):
        """Initialize statistics"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.score_screen_active = False
        # Start game in an inactive state
        self.game_active = False
        # Flag for if ship is hit
        self.ship_hit = False
        # Flag for if aliens have been hit
        self.alien_hit = {0: False,
                          1: False,
                          2: False}
        # High score should never be reset
        self.high_score = 0
        self.score = 0

        self.count = 0
        self.height = 200

        self.ships_left = None
        self.level = None

    def reset_stats(self):
        """Initializes statistics that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1
