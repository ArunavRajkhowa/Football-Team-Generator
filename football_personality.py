"""
Football Personality Module - Makes the app feel personal and engaging
"""
import random
from datetime import datetime
from typing import List, Dict

class FootballPersonality:
    """Adds personality and motivation to the football app"""
    
    def __init__(self):
        self.motivational_messages = {
            'pre_match': [
                "Time to lace up those boots! ⚽",
                "Another weekend, another game!",
                "The pitch is calling!",
                "Let's have some fun today!",
                "Weekend football time!",
                "Ready for kick-off?",
                "The beautiful game awaits!",
                "Time to play some football!",
                "Should be a good match!",
                "Perfect day for football!"
            ],
            'team_ready': [
                "Teams are set! Should be fun!",
                "Nicely balanced teams!",
                "Good lineups on both sides!",
                "Teams look even - should be close!",
                "Fair split, let's play!",
                "Both sides look good!",
                "Teams are ready!",
                "Even match-up today!",
                "Let's kick off!",
                "Good teams, good game ahead!"
            ],
            'player_joined': [
                "{name} is ready to dominate!",
                "Welcome to the squad, {name}!",
                "{name} joins the weekend warriors!",
                "Great to have {name} on board!",
                "{name} is here to make a difference!",
                "The squad just got stronger with {name}!",
                "{name} brings the energy!",
                "Can't wait to see {name} in action!",
                "{name} completes the puzzle!",
                "Squad goals with {name} joining!"
            ],
            'young_player': [
                "{name} bringing that youthful energy!",
                "The future is bright with {name}!",
                "Watch out for {name} - young and hungry!",
                "{name} has legs for days!",
                "Speed demon {name} is here!"
            ],
            'veteran_player': [
                "{name} - experience speaks volumes!",
                "The wise head of {name} joins us!",
                "{name} brings the know-how!",
                "Class is permanent - welcome {name}!",
                "{name} - still got it!"
            ]
        }
        
        self.position_personalities = {
            'GK': [
                "The last line of defense!",
                "Guardian of the goal!",
                "Safe hands between the sticks!",
                "The wall at the back!",
                "Shot-stopper supreme!"
            ],
            'DEF': [
                "Rock at the back!",
                "Defensive masterclass incoming!",
                "No way through!",
                "The shield of the team!",
                "Brick wall mode: ON!"
            ],
            'MID': [
                "Engine room operator!",
                "Pulling the strings!",
                "Box-to-box warrior!",
                "The heartbeat of the team!",
                "Midfield maestro!"
            ],
            'FWD': [
                "Goal machine activated!",
                "Danger man up front!",
                "Clinical finisher!",
                "Speed and precision!",
                "Ready to terrorize defenses!"
            ]
        }
        
        self.weather_messages = {
            'sunny': [
                "Perfect football weather! ☀️",
                "The sun is shining, the pitch is calling!",
                "Vitamin D and football - perfect combo!"
            ],
            'cloudy': [
                "Classic football weather! ☁️",
                "No excuses today - perfect conditions!",
                "Cloudy skies, clear minds!"
            ],
            'rainy': [
                "Real players love the rain! 🌧️",
                "Time to channel your inner warrior!",
                "Muddy boots, happy hearts!"
            ]
        }
        
        self.celebration_emojis = ["⚽", "🎯", "🔥", "💪", "🏃", "🥅", "⚡", "🌟", "🎉", "🙌"]
    
    def get_welcome_message(self) -> str:
        """Get a personalized welcome message based on time of day"""
        hour = datetime.now().hour
        
        if hour < 12:
            greetings = [
                "Good morning! ☀️",
                "Morning kick-off time! ⚽",
                "Ready for some football?",
                "Early game today!",
                "Coffee ☕ and football!"
            ]
        elif hour < 17:
            greetings = [
                "Good afternoon! 🌞",
                "Perfect time for football!",
                "Ready for a match?",
                "Afternoon football time!",
                "Let's get this started!"
            ]
        else:
            greetings = [
                "Good evening! ✨",
                "Evening football time!",
                "Ready to play?",
                "After-work football!",
                "Let's kick off!"
            ]
        
        return random.choice(greetings)
    
    def get_player_welcome(self, name: str, age: int, position: str) -> str:
        """Get personalized message when adding a player"""
        if age < 23:
            messages = self.motivational_messages['young_player']
        elif age > 32:
            messages = self.motivational_messages['veteran_player']
        else:
            messages = self.motivational_messages['player_joined']
        
        message = random.choice(messages).format(name=name)
        position_msg = random.choice(self.position_personalities.get(position, ["Ready to play!"]))
        
        return f"{message} {position_msg}"
    
    def get_team_motivation(self, team_stats: dict) -> str:
        """Get motivational message based on team composition"""
        avg_age = team_stats.get('average_age', 25)
        
        if avg_age < 24:
            return "⚡ Young, fast, and fearless! This team will run all day!"
        elif avg_age < 28:
            return "💪 Perfect blend of youth and experience. Balanced and dangerous!"
        elif avg_age < 32:
            return "🧠 Experience and wisdom. They'll outsmart the opposition!"
        else:
            return "👑 Legends on the pitch! Class and composure will shine through!"
    
    def get_match_countdown(self, days_until_match: int) -> str:
        """Get countdown message for upcoming match"""
        if days_until_match == 0:
            return "🔥 IT'S MATCH DAY! Time to show what you've got!"
        elif days_until_match == 1:
            return "⏰ Tomorrow we play! Rest well, warriors!"
        elif days_until_match <= 3:
            return f"📅 {days_until_match} days to go! The excitement is building!"
        else:
            return f"📆 {days_until_match} days until we meet on the pitch!"
    
    def get_random_tip(self) -> str:
        """Get a random football tip"""
        tips = [
            "💡 Tip: Warm up properly - your body will thank you!",
            "💡 Tip: Communication is key - talk to your teammates!",
            "💡 Tip: Stay hydrated - bring extra water!",
            "💡 Tip: First touch matters - control before you pass!",
            "💡 Tip: Have fun - that's why we play!",
            "💡 Tip: Respect all players - we're all here for the love of the game!",
            "💡 Tip: Stretch after the game - recovery is important!",
            "💡 Tip: Encourage your teammates - positivity wins games!",
            "💡 Tip: Play simple - the best players make it look easy!",
            "💡 Tip: Enjoy every moment - these are the good times!"
        ]
        return random.choice(tips)
    
    def generate_player_nickname(self, name: str, position: str, age: int) -> str:
        """Generate a fun nickname for a player"""
        first_name = name.split()[0] if name else "Player"
        
        position_nicknames = {
            'GK': ["The Wall", "Safe Hands", "The Cat", "Guardian"],
            'DEF': ["The Rock", "Iron Man", "The Shield", "Defender"],
            'MID': ["The Engine", "Maestro", "The General", "Playmaker"],
            'FWD': ["The Rocket", "Goal Machine", "The Flash", "Striker"]
        }
        
        if age < 23:
            age_prefix = ["Young", "Rising", "Future"]
        elif age > 32:
            age_prefix = ["Veteran", "Master", "Legend"]
        else:
            age_prefix = ["Prime", "Peak", "Star"]
        
        nickname_style = random.choice([1, 2, 3])
        
        if nickname_style == 1:
            # Style: "The [Nickname]"
            return f"The {random.choice(position_nicknames.get(position, ['Player']))}"
        elif nickname_style == 2:
            # Style: "[Age Prefix] [First Name]"
            return f"{random.choice(age_prefix)} {first_name}"
        else:
            # Style: "[First Name] the [Position Nickname]"
            return f"{first_name} the {random.choice(position_nicknames.get(position, ['Great']))}"
    
    def get_squad_personality(self, players: List[Dict]) -> str:
        """Analyze squad and give it a personality"""
        if not players:
            return "Build your squad to discover its personality!"
        
        avg_age = sum(p['age'] for p in players) / len(players)
        positions = [p['position'] for p in players]
        
        # Age-based personality
        if avg_age < 24:
            age_personality = "Young and Fearless"
        elif avg_age < 28:
            age_personality = "Prime Warriors"
        elif avg_age < 32:
            age_personality = "Experienced Campaigners"
        else:
            age_personality = "Veteran Legends"
        
        # Position-based style
        if positions.count('FWD') >= positions.count('DEF'):
            style = "Attack-Minded"
        else:
            style = "Defensive Solid"
        
        personalities = [
            f"You've built a {age_personality} squad with an {style} approach!",
            f"This {age_personality} team loves to play {style} football!",
            f"A {style} squad of {age_personality} - exciting times ahead!"
        ]
        
        return random.choice(personalities)