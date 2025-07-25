"""
import streamlit as st
st.write("Debug: Streamlit imported successfully")

from football_team_manager import FootballManager, Player, Position, PlayerStatus
st.write("Debug: Imports from football_team_manager successful")

# Initialize manager
st.write("Debug: Initializing manager")
if 'manager' not in st.session_state:
    manager = FootballManager()
    
    # Add sample players from the script
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
    for player in sample_players:
        manager.add_player(player)
    st.session_state.manager = manager

manager = st.session_state.manager

st.title("⚽ Football Team Generator")

# Display squad status
status = manager.get_squad_status()
st.header("Squad Status")
st.write(f"Total Players: {status['total_players']}")
st.write(f"Available: {status['available']}")

# Generate team
if st.button("Generate Weekly Team"):
    team, details = manager.generate_weekly_team()
    st.header("Selected Team")
    for player in team:
        st.write(f"{player.name} ({player.primary_position.value}) - Rating: {player.get_overall_rating():.1f}")
    
    # You can add more UI for adding players, recording matches, etc.

# To make it full, add forms for adding players, etc.
""" 