"""
Simple Team Generator - Focus on Age and Position Balance
"""
from dataclasses import dataclass
from typing import List, Tuple
from enum import Enum
import random

class Position(Enum):
    GOALKEEPER = "GK"
    DEFENDER = "DEF"
    MIDFIELDER = "MID"
    FORWARD = "FWD"

@dataclass
class SimplePlayer:
    name: str
    age: int
    position: Position
    
    def get_age_score(self) -> float:
        """Simple age-based scoring"""
        if 24 <= self.age <= 28:  # Peak age
            return 10
        elif 22 <= self.age <= 30:  # Good age
            return 8
        elif 20 <= self.age <= 32:  # Decent age
            return 6
        else:  # Young or veteran
            return 4

class SimpleTeamGenerator:
    """Simplified team generator focusing on fun and balance"""
    
    def __init__(self, players: List[SimplePlayer]):
        self.players = players
        self.team_size = 7
        
    def generate_balanced_teams(self) -> Tuple[List[SimplePlayer], List[SimplePlayer]]:
        """Generate two balanced teams based on age and position"""
        if len(self.players) < self.team_size * 2:
            raise ValueError(f"Need at least {self.team_size * 2} players!")
        
        # Shuffle for randomness
        available = self.players.copy()
        random.shuffle(available)
        
        team_a = []
        team_b = []
        
        # First, ensure each team gets a goalkeeper
        goalkeepers = [p for p in available if p.position == Position.GOALKEEPER]
        if len(goalkeepers) >= 2:
            team_a.append(goalkeepers[0])
            team_b.append(goalkeepers[1])
            available.remove(goalkeepers[0])
            available.remove(goalkeepers[1])
        elif len(goalkeepers) == 1:
            # Only one GK, randomly assign
            if random.random() > 0.5:
                team_a.append(goalkeepers[0])
            else:
                team_b.append(goalkeepers[0])
            available.remove(goalkeepers[0])
        
        # Sort remaining players by position for balanced distribution
        defenders = [p for p in available if p.position == Position.DEFENDER]
        midfielders = [p for p in available if p.position == Position.MIDFIELDER]
        forwards = [p for p in available if p.position == Position.FORWARD]
        
        # Distribute positions evenly
        for position_group in [defenders, midfielders, forwards]:
            # Sort by age score for fairness
            position_group.sort(key=lambda p: p.get_age_score(), reverse=True)
            
            # Alternate assignment
            for i, player in enumerate(position_group):
                if len(team_a) < self.team_size and len(team_b) < self.team_size:
                    if i % 2 == 0:
                        team_a.append(player)
                    else:
                        team_b.append(player)
                elif len(team_a) < self.team_size:
                    team_a.append(player)
                elif len(team_b) < self.team_size:
                    team_b.append(player)
        
        # Balance teams by swapping if needed
        self._balance_teams(team_a, team_b)
        
        return team_a[:self.team_size], team_b[:self.team_size]
    
    def _balance_teams(self, team_a: List[SimplePlayer], team_b: List[SimplePlayer]):
        """Simple balancing based on average age"""
        if not team_a or not team_b:
            return
            
        avg_age_a = sum(p.age for p in team_a) / len(team_a)
        avg_age_b = sum(p.age for p in team_b) / len(team_b)
        
        # If age difference is too large, try a few swaps
        max_attempts = 5
        while abs(avg_age_a - avg_age_b) > 3 and max_attempts > 0:
            # Find players to swap
            if avg_age_a > avg_age_b:
                # Team A is older, find young player in A and old in B
                young_a = min(team_a, key=lambda p: p.age)
                old_b = max(team_b, key=lambda p: p.age)
                
                # Only swap if it improves balance
                if young_a.age < old_b.age:
                    team_a.remove(young_a)
                    team_b.remove(old_b)
                    team_a.append(old_b)
                    team_b.append(young_a)
            else:
                # Team B is older
                young_b = min(team_b, key=lambda p: p.age)
                old_a = max(team_a, key=lambda p: p.age)
                
                if young_b.age < old_a.age:
                    team_b.remove(young_b)
                    team_a.remove(old_a)
                    team_b.append(old_a)
                    team_a.append(young_b)
            
            # Recalculate averages
            avg_age_a = sum(p.age for p in team_a) / len(team_a)
            avg_age_b = sum(p.age for p in team_b) / len(team_b)
            max_attempts -= 1

    def get_fun_stats(self, team: List[SimplePlayer]) -> dict:
        """Get fun statistics about a team"""
        if not team:
            return {}
            
        avg_age = sum(p.age for p in team) / len(team)
        positions = [p.position.value for p in team]
        
        return {
            'average_age': round(avg_age, 1),
            'youngest': min(team, key=lambda p: p.age),
            'oldest': max(team, key=lambda p: p.age),
            'formation': f"{positions.count('GK')}-{positions.count('DEF')}-{positions.count('MID')}-{positions.count('FWD')}",
            'nickname': self._generate_team_nickname(team)
        }
    
    def _generate_team_nickname(self, team: List[SimplePlayer]) -> str:
        """Generate a fun nickname based on team characteristics"""
        avg_age = sum(p.age for p in team) / len(team)
        
        if avg_age < 24:
            nicknames = ["Young Guns", "Rising Stars", "Future Legends", "The Rookies"]
        elif avg_age < 28:
            nicknames = ["Prime Squad", "The Warriors", "Peak Performers", "The Dynamos"]
        elif avg_age < 32:
            nicknames = ["The Veterans", "Experience XI", "Wise Owls", "The Generals"]
        else:
            nicknames = ["The Legends", "Old Guard", "The Masters", "Vintage XI"]
        
        return random.choice(nicknames)