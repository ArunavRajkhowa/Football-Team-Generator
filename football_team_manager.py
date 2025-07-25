from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple
from enum import Enum
import random
import json
from datetime import datetime, timedelta
import statistics

class Position(Enum):
    GOALKEEPER = "GK"
    DEFENDER = "DEF"
    MIDFIELDER = "MID"
    FORWARD = "FWD"

class PlayerStatus(Enum):
    AVAILABLE = "available"
    INJURED = "injured"
    UNAVAILABLE = "unavailable"
    SUSPENDED = "suspended"

@dataclass
class MatchPerformance:
    """Individual match performance data"""
    date: str
    position_played: Position
    minutes_played: int
    goals: int = 0
    assists: int = 0
    saves: int = 0  # For goalkeepers
    rating: float = 5.0  # Match rating out of 10
    yellow_cards: int = 0
    red_cards: int = 0
    key_passes: int = 0
    tackles_won: int = 0
    
@dataclass
class Player:
    """Enhanced player model with comprehensive attributes"""
    # Basic Info
    id: int
    name: str
    age: int
    primary_position: Position
    secondary_positions: List[Position] = field(default_factory=list)
    
    # Core Attributes
    skill_level: int = 5  # 1-10
    fitness: int = 8  # 1-10, affects stamina and injury risk
    leadership: int = 5  # 1-10, captain potential
    consistency: int = 5  # 1-10, how reliable they are week to week
    
    # Physical Attributes
    pace: int = 5  # 1-10
    strength: int = 5  # 1-10
    height: int = 175  # cm
    preferred_foot: str = "right"  # "left", "right", "both"
    
    # Status & Availability
    status: PlayerStatus = PlayerStatus.AVAILABLE
    injury_return_date: Optional[str] = None
    
    # Performance Tracking
    recent_performances: List[MatchPerformance] = field(default_factory=list)
    total_appearances: int = 0
    goals_scored: int = 0
    assists_made: int = 0
    
    # Form & Morale
    current_form: float = 5.0  # 1-10, based on recent performances
    morale: float = 7.0  # 1-10, affected by playing time and results
    fatigue: float = 0.0  # 0-10, increases with consecutive games
    
    # Team Chemistry
    preferred_partners: List[int] = field(default_factory=list)  # Player IDs they work well with
    
    def add_performance(self, performance: MatchPerformance):
        """Add a match performance and update stats"""
        self.recent_performances.append(performance)
        # Keep only last 5 performances for form calculation
        if len(self.recent_performances) > 5:
            self.recent_performances.pop(0)
        
        self.total_appearances += 1
        self.goals_scored += performance.goals
        self.assists_made += performance.assists
        self._update_form()
        self._update_fatigue(performance.minutes_played)
    
    def _update_form(self):
        """Calculate current form based on recent performances"""
        if not self.recent_performances:
            return
        
        recent_ratings = [p.rating for p in self.recent_performances[-3:]]
        self.current_form = statistics.mean(recent_ratings)
    
    def _update_fatigue(self, minutes_played: int):
        """Update fatigue based on playing time"""
        if minutes_played >= 60:  # Full match
            self.fatigue = min(10, self.fatigue + 1.5)
        elif minutes_played >= 30:  # Significant time
            self.fatigue = min(10, self.fatigue + 1.0)
        else:
            self.fatigue = min(10, self.fatigue + 0.5)
    
    def rest(self):
        """Reduce fatigue when player doesn't play"""
        self.fatigue = max(0, self.fatigue - 2.0)
        # Slight morale decrease if not playing regularly
        if self.status == PlayerStatus.AVAILABLE:
            self.morale = max(1, self.morale - 0.2)
    
    def get_overall_rating(self) -> float:
        """Calculate overall player rating considering all factors"""
        base_rating = self.skill_level
        form_modifier = (self.current_form - 5) * 0.5
        fitness_modifier = (self.fitness - 5) * 0.2
        fatigue_penalty = self.fatigue * 0.3
        morale_modifier = (self.morale - 5) * 0.2
        
        return max(1, min(10, base_rating + form_modifier + fitness_modifier - fatigue_penalty + morale_modifier))
    
    def can_play_position(self, position: Position) -> bool:
        """Check if player can play in given position"""
        return position == self.primary_position or position in self.secondary_positions
    
    def get_position_suitability(self, position: Position) -> float:
        """Get how suitable player is for a position (0-1)"""
        if position == self.primary_position:
            return 1.0
        elif position in self.secondary_positions:
            return 0.7
        else:
            return 0.3  # Can play out of position with penalty

class TeamGenerator:
    """Generates balanced teams considering multiple factors"""
    
    def __init__(self, players: List[Player]):
        self.players = players
        self.formation = {
            Position.GOALKEEPER: 1,
            Position.DEFENDER: 2,
            Position.MIDFIELDER: 3,
            Position.FORWARD: 1
        }
    
    def generate_team(self, week_number: int = 1, prioritize_rotation: bool = True) -> Tuple[List[Player], Dict]:
        """Generate optimal team considering all factors"""
        available_players = [p for p in self.players if p.status == PlayerStatus.AVAILABLE]
        
        if len(available_players) < 7:
            raise ValueError(f"Not enough available players. Need 7, have {len(available_players)}")
        
        # Score each player for selection
        player_scores = []
        for player in available_players:
            score = self._calculate_selection_score(player, week_number, prioritize_rotation)
            player_scores.append((player, score))
        
        # Generate team by position
        selected_team = []
        selection_details = {"selection_reasoning": {}}
        
        for position, count in self.formation.items():
            position_candidates = [
                (player, score) for player, score in player_scores 
                if player.can_play_position(position) and player not in selected_team
            ]
            
            # Sort by score (descending) and select best available
            position_candidates.sort(key=lambda x: x[1], reverse=True)
            
            for i in range(min(count, len(position_candidates))):
                player = position_candidates[i][0]
                selected_team.append(player)
                selection_details["selection_reasoning"][player.name] = {
                    "position": position.value,
                    "score": position_candidates[i][1],
                    "rating": player.get_overall_rating(),
                    "form": player.current_form,
                    "fatigue": player.fatigue
                }
        
        # Fill remaining spots if needed
        while len(selected_team) < 7:
            remaining_candidates = [
                (player, score) for player, score in player_scores 
                if player not in selected_team
            ]
            if not remaining_candidates:
                break
            
            remaining_candidates.sort(key=lambda x: x[1], reverse=True)
            selected_team.append(remaining_candidates[0][0])
        
        return selected_team, selection_details
    
    def _calculate_selection_score(self, player: Player, week_number: int, prioritize_rotation: bool) -> float:
        """Calculate comprehensive selection score"""
        base_score = player.get_overall_rating()
        
        # Rotation bonus - reward players who haven't played recently
        if prioritize_rotation:
            games_since_last_appearance = self._games_since_last_appearance(player)
            rotation_bonus = min(2, games_since_last_appearance * 0.5)
            base_score += rotation_bonus
        
        # Fatigue penalty
        fatigue_penalty = player.fatigue * 0.4
        base_score -= fatigue_penalty
        
        # Consistency bonus
        consistency_bonus = (player.consistency - 5) * 0.2
        base_score += consistency_bonus
        
        # Form consideration
        form_modifier = (player.current_form - 5) * 0.3
        base_score += form_modifier
        
        return max(0, base_score)
    
    def _games_since_last_appearance(self, player: Player) -> int:
        """Calculate games since player last played"""
        if not player.recent_performances:
            return 5  # Assume hasn't played recently
        
        # Simple simulation - in real app would track actual game history
        return random.randint(0, 3)

class FootballManager:
    """Main manager class that coordinates everything"""
    
    def __init__(self):
        self.players: List[Player] = []
        self.team_generator = None
        self.week_number = 1
        self.season_history: List[Dict] = []
    
    def add_player(self, player: Player):
        """Add a player to the squad"""
        self.players.append(player)
        self._update_team_generator()
    
    def _update_team_generator(self):
        """Update team generator when players change"""
        if self.players:
            self.team_generator = TeamGenerator(self.players)
    
    def generate_weekly_team(self, prioritize_rotation: bool = True) -> Tuple[List[Player], Dict]:
        """Generate team for the current week"""
        if not self.team_generator:
            raise ValueError("No players available for team generation")
        
        team, details = self.team_generator.generate_team(self.week_number, prioritize_rotation)
        
        # Update player morale based on selection
        for player in self.players:
            if player in team:
                player.morale = min(10, player.morale + 0.5)  # Boost for selected players
            else:
                player.rest()  # Rest unselected players
        
        return team, details
    
    def record_match_results(self, team: List[Player], match_performances: List[MatchPerformance]):
        """Record match results and update player stats"""
        for i, player in enumerate(team):
            if i < len(match_performances):
                player.add_performance(match_performances[i])
        
        # Store week history
        week_data = {
            "week": self.week_number,
            "team": [p.name for p in team],
            "performances": [
                {
                    "player": team[i].name if i < len(team) else "Unknown",
                    "rating": perf.rating,
                    "goals": perf.goals,
                    "assists": perf.assists
                }
                for i, perf in enumerate(match_performances)
            ]
        }
        self.season_history.append(week_data)
        
        self.week_number += 1
    
    def get_squad_status(self) -> Dict:
        """Get comprehensive squad status"""
        available = len([p for p in self.players if p.status == PlayerStatus.AVAILABLE])
        injured = len([p for p in self.players if p.status == PlayerStatus.INJURED])
        
        top_performers = sorted(self.players, key=lambda p: p.get_overall_rating(), reverse=True)[:5]
        
        return {
            "total_players": len(self.players),
            "available": available,
            "injured": injured,
            "week": self.week_number,
            "top_performers": [
                {
                    "name": p.name,
                    "position": p.primary_position.value,
                    "rating": round(p.get_overall_rating(), 1),
                    "form": round(p.current_form, 1)
                }
                for p in top_performers
            ]
        }
    
    def save_to_file(self, filename: str):
        """Save manager state to JSON file"""
        data = {
            "week_number": self.week_number,
            "players": [self._player_to_dict(p) for p in self.players],
            "season_history": self.season_history
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2, default=str)
    
    def load_from_file(self, filename: str):
        """Load manager state from JSON file"""
        with open(filename, 'r') as f:
            data = json.load(f)
        
        self.week_number = data["week_number"]
        self.players = [self._dict_to_player(p_data) for p_data in data["players"]]
        self.season_history = data.get("season_history", [])
        self._update_team_generator()
    
    def _player_to_dict(self, player: Player) -> Dict:
        """Convert player to dictionary for JSON serialization"""
        return {
            "id": player.id,
            "name": player.name,
            "age": player.age,
            "primary_position": player.primary_position.value,
            "secondary_positions": [pos.value for pos in player.secondary_positions],
            "skill_level": player.skill_level,
            "fitness": player.fitness,
            "leadership": player.leadership,
            "consistency": player.consistency,
            "pace": player.pace,
            "strength": player.strength,
            "height": player.height,
            "preferred_foot": player.preferred_foot,
            "status": player.status.value,
            "current_form": player.current_form,
            "morale": player.morale,
            "fatigue": player.fatigue,
            "total_appearances": player.total_appearances,
            "goals_scored": player.goals_scored,
            "assists_made": player.assists_made,
            "recent_performances": [
                {
                    "date": perf.date,
                    "position_played": perf.position_played.value,
                    "minutes_played": perf.minutes_played,
                    "goals": perf.goals,
                    "assists": perf.assists,
                    "saves": perf.saves,
                    "rating": perf.rating,
                    "yellow_cards": perf.yellow_cards,
                    "red_cards": perf.red_cards
                }
                for perf in player.recent_performances
            ]
        }
    
    def _dict_to_player(self, data: Dict) -> Player:
        """Convert dictionary to Player object"""
        player = Player(
            id=data["id"],
            name=data["name"],
            age=data["age"],
            primary_position=Position(data["primary_position"]),
            secondary_positions=[Position(pos) for pos in data.get("secondary_positions", [])],
            skill_level=data["skill_level"],
            fitness=data.get("fitness", 8),
            leadership=data.get("leadership", 5),
            consistency=data.get("consistency", 5),
            pace=data.get("pace", 5),
            strength=data.get("strength", 5),
            height=data.get("height", 175),
            preferred_foot=data.get("preferred_foot", "right"),
            status=PlayerStatus(data.get("status", "available")),
            current_form=data.get("current_form", 5.0),
            morale=data.get("morale", 7.0),
            fatigue=data.get("fatigue", 0.0),
            total_appearances=data.get("total_appearances", 0),
            goals_scored=data.get("goals_scored", 0),
            assists_made=data.get("assists_made", 0)
        )
        
        # Reconstruct recent performances
        for perf_data in data.get("recent_performances", []):
            performance = MatchPerformance(
                date=perf_data["date"],
                position_played=Position(perf_data["position_played"]),
                minutes_played=perf_data["minutes_played"],
                goals=perf_data["goals"],
                assists=perf_data["assists"],
                saves=perf_data.get("saves", 0),
                rating=perf_data["rating"],
                yellow_cards=perf_data.get("yellow_cards", 0),
                red_cards=perf_data.get("red_cards", 0)
            )
            player.recent_performances.append(performance)
        
        return player

# Example usage and testing
if __name__ == "__main__":
    # Create sample players
    sample_players = [
        Player(1, "John Smith", 25, Position.GOALKEEPER, skill_level=8, fitness=9, consistency=7),
        Player(2, "Mike Johnson", 28, Position.DEFENDER, [Position.MIDFIELDER], skill_level=7, pace=6, strength=8),
        Player(3, "David Wilson", 24, Position.DEFENDER, skill_level=6, strength=7, leadership=8),
        Player(4, "Chris Brown", 26, Position.MIDFIELDER, [Position.FORWARD], skill_level=8, pace=8, consistency=6),
        Player(5, "Tom Davis", 23, Position.MIDFIELDER, skill_level=7, fitness=8, pace=7),
        Player(6, "Alex Taylor", 27, Position.MIDFIELDER, [Position.DEFENDER], skill_level=6, leadership=7),
        Player(7, "Sam Wilson", 22, Position.FORWARD, skill_level=9, pace=9, consistency=5),
        Player(8, "Jake Miller", 29, Position.FORWARD, [Position.MIDFIELDER], skill_level=7, strength=6),
        Player(9, "Ryan Clark", 25, Position.DEFENDER, skill_level=5, strength=8, consistency=8),
        Player(10, "Luke White", 24, Position.GOALKEEPER, skill_level=6, fitness=7, consistency=7)
    ]
    
    # Initialize manager
    manager = FootballManager()
    for player in sample_players:
        manager.add_player(player)
    
    print("=== Football Team Manager Demo ===\n")
    
    # Show initial squad status
    status = manager.get_squad_status()
    print(f"Squad Status - Week {status['week']}")
    print(f"Total Players: {status['total_players']}")
    print(f"Available: {status['available']}")
    print(f"Top Performers:")
    for performer in status['top_performers']:
        print(f"  {performer['name']} ({performer['position']}) - Rating: {performer['rating']}, Form: {performer['form']}")
    
    # Generate first team
    print(f"\n=== Week {manager.week_number} Team Selection ===")
    team, details = manager.generate_weekly_team()
    
    print("Selected Team:")
    for player in team:
        print(f"  {player.name} ({player.primary_position.value}) - Rating: {player.get_overall_rating():.1f}")
    
    print("\nSelection Details:")
    for name, info in details["selection_reasoning"].items():
        print(f"  {name}: Score {info['score']:.1f}, Form {info['form']:.1f}, Fatigue {info['fatigue']:.1f}") 