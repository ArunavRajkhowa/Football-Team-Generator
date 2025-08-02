import streamlit as st
import pandas as pd
import random
import json
from datetime import datetime
from football_team_manager import FootballManager, Player, Position, PlayerStatus
from simple_team_generator import SimplePlayer, SimpleTeamGenerator, Position as SimplePosition
from football_personality import FootballPersonality

# Master quotes from football legends
FOOTBALL_QUOTES = [
    {"quote": "Football is a simple game. Twenty-two men chase a ball for 90 minutes and at the end, the Germans always win.", "author": "Gary Lineker"},
    {"quote": "I learned all about life with a ball at my feet.", "author": "Ronaldinho"},
    {"quote": "Football is played with the head. Your feet are just the tools.", "author": "Andrea Pirlo"},
    {"quote": "In football, the worst blindness is only seeing the ball.", "author": "Nelson Falcão Rodrigues"},
    {"quote": "Without the ball, you can't win.", "author": "Johan Cruyff"},
    {"quote": "The ball is round, the game lasts ninety minutes, and everything else is just theory.", "author": "Sepp Herberger"},
    {"quote": "Football is like chess, only without the dice.", "author": "Lukas Podolski"},
    {"quote": "Some people think football is a matter of life and death. I assure you, it's much more serious than that.", "author": "Bill Shankly"},
    {"quote": "Take the ball, pass the ball.", "author": "Pep Guardiola"},
    {"quote": "Playing football is very simple, but playing simple football is the hardest thing there is.", "author": "Johan Cruyff"},
    {"quote": "The first 90 minutes are the most important.", "author": "Bobby Robson"},
    {"quote": "Football is a game of mistakes. Whoever makes the fewest mistakes wins.", "author": "Johan Cruyff"},
    {"quote": "When you win, you don't get carried away. But you also don't get carried away when you lose.", "author": "Carlo Ancelotti"},
    {"quote": "The secret is to believe in your dreams; in your potential that you can be like your star, keep searching, keep believing and don't lose faith in yourself.", "author": "Neymar"},
    {"quote": "Talent without working hard is nothing.", "author": "Cristiano Ronaldo"},
    {"quote": "Every disadvantage has its advantage.", "author": "Johan Cruyff"},
    {"quote": "I don't have to show anything to anyone. There is nothing to prove.", "author": "Zlatan Ibrahimović"},
    {"quote": "Success is no accident. It is hard work, perseverance, learning, studying, sacrifice and most of all, love of what you are doing.", "author": "Pelé"},
    {"quote": "You have to fight to reach your dream. You have to sacrifice and work hard for it.", "author": "Lionel Messi"},
    {"quote": "The more difficult the victory, the greater the happiness in winning.", "author": "Pelé"},
    {"quote": "Quality without results is pointless. Results without quality is boring.", "author": "Johan Cruyff"},
    {"quote": "If you have the ball you must make the field as big as possible, and if you don't have the ball you must make it as small as possible.", "author": "Johan Cruyff"},
    {"quote": "The goalkeeper is the jewel in the crown and getting at him should be almost impossible.", "author": "Gordon Banks"},
    {"quote": "A penalty is a cowardly way to score.", "author": "Pelé"},
    {"quote": "Football is a game about feelings and intelligence.", "author": "Jose Mourinho"}
]

st.set_page_config(
    page_title="Weekend Football Squad",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Professional color palette and modern CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* CSS Variables for consistent theming */
    :root {
        --primary-dark: #0a0e27;
        --primary-blue: #1e3a8a;
        --accent-blue: #3b82f6;
        --accent-teal: #14b8a6;
        --surface-dark: #1e293b;
        --surface-light: #334155;
        --text-primary: #f1f5f9;
        --text-secondary: #94a3b8;
        --gradient-primary: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        --gradient-dark: linear-gradient(180deg, #0a0e27 0%, #1e293b 100%);
        --gradient-accent: linear-gradient(135deg, #3b82f6 0%, #14b8a6 100%);
    }
    
    /* Reset and base styles */
    .main {
        background: #0f172a;
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section */
    .hero-section {
        background: var(--gradient-dark);
        color: var(--text-primary);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        border: 1px solid rgba(59, 130, 246, 0.2);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(59, 130, 246, 0.1) 0%, transparent 70%);
        animation: pulse 10s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.3; }
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: -1px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.1rem;
        color: var(--text-secondary);
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Sliding Quote Banner */
    .quote-slider {
        background: var(--surface-dark);
        border-radius: 12px;
        overflow: hidden;
        margin: 1.5rem 0;
        height: 60px;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        border: 1px solid rgba(59, 130, 246, 0.1);
        position: relative;
    }
    
    .quotes-container {
        display: flex;
        animation: scrollQuotes 120s linear infinite;
        padding-left: 100%;
    }
    
    .quote-item {
        white-space: nowrap;
        color: var(--text-primary);
        font-size: 0.95rem;
        padding: 0 3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .quote-author {
        color: var(--accent-blue);
        font-weight: 500;
    }
    
    @keyframes scrollQuotes {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    
    .quote-slider:hover .quotes-container {
        animation-play-state: paused;
    }
    
    /* Welcome Card */
    .welcome-card {
        background: var(--gradient-primary);
        color: var(--text-primary);
        padding: 2.5rem;
        border-radius: 16px;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(59, 130, 246, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .welcome-card::after {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent 30%, rgba(255,255,255,0.1) 50%, transparent 70%);
        animation: shimmer 3s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    /* Team Display */
    .team-display {
        background: var(--surface-dark);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(59, 130, 246, 0.2);
        margin: 1rem 0;
    }
    
    .team-header {
        text-align: center;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        color: var(--text-primary);
    }
    
    .player-line {
        background: var(--surface-light);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
        transition: all 0.2s ease;
    }
    
    .player-line:hover {
        background: rgba(59, 130, 246, 0.1);
        transform: translateX(5px);
    }
    
    /* Custom buttons */
    .stButton > button {
        background: var(--gradient-accent);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        font-weight: 600;
        border-radius: 8px;
        transition: all 0.3s ease;
        font-size: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(59, 130, 246, 0.4);
    }
    
    /* Hide Streamlit defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--surface-dark);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--accent-blue);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-teal);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'manager' not in st.session_state:
    st.session_state.manager = FootballManager()
if 'personality' not in st.session_state:
    st.session_state.personality = FootballPersonality()
if 'show_team_gen' not in st.session_state:
    st.session_state.show_team_gen = False
if 'show_learn' not in st.session_state:
    st.session_state.show_learn = False
if 'show_matches' not in st.session_state:
    st.session_state.show_matches = False
if 'match_history' not in st.session_state:
    st.session_state.match_history = []
if 'temp_players' not in st.session_state:
    st.session_state.temp_players = []

manager = st.session_state.manager
personality = st.session_state.personality

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">⚽ WEEKEND SQUAD</h1>
    <p class="hero-subtitle">Professional Football Team Management</p>
</div>
""", unsafe_allow_html=True)

# Multiple Quotes Sliding Banner
quotes_html = ""
for quote in FOOTBALL_QUOTES:
    quotes_html += f'<div class="quote-item">💬 "{quote["quote"]}" <span class="quote-author">- {quote["author"]}</span></div>'

st.markdown(f"""
<div class="quote-slider">
    <div class="quotes-container">
        {quotes_html}
    </div>
</div>
""", unsafe_allow_html=True)

# Welcome Section
st.markdown("""
<div class="welcome-card">
    <h2>Welcome to Weekend Squad</h2>
    <p style="font-size: 1.1rem; margin: 1rem 0;">
        Organize balanced teams, track your matches, and learn from the masters.
    </p>
    <p style="font-size: 0.95rem; opacity: 0.9;">
        Professional team generation with tactical insights
    </p>
</div>
""", unsafe_allow_html=True)

# Quick Actions Section
st.markdown("## 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⚡ Generate Teams", use_container_width=True, key="gen_teams_btn"):
        st.session_state.show_team_gen = True
        st.session_state.show_matches = False
        st.session_state.show_learn = False

with col2:
    if st.button("📊 Previous Matches", use_container_width=True, key="prev_matches_btn"):
        st.session_state.show_matches = True
        st.session_state.show_team_gen = False
        st.session_state.show_learn = False

with col3:
    if st.button("📚 Learn Football", use_container_width=True, key="learn_btn"):
        st.session_state.show_learn = True
        st.session_state.show_team_gen = False
        st.session_state.show_matches = False

# Team Generation Section
if st.session_state.show_team_gen:
    st.markdown("---")
    st.markdown("## ⚡ Team Generator")
    
    # Enhanced CSS for team generator
    st.markdown("""
    <style>
        .player-input-row {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 1rem;
        }
        .player-card-enhanced {
            background: var(--surface-light);
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.3rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: all 0.2s ease;
            position: relative;
        }
        .player-card-enhanced:hover {
            background: rgba(59, 130, 246, 0.1);
            transform: translateX(3px);
        }
        .player-info {
            display: flex;
            gap: 1rem;
            align-items: center;
        }
        .remove-player {
            cursor: pointer;
            color: #ef4444;
            font-size: 1.2rem;
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
        }
        .formation-display {
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 150"><rect x="10" y="10" width="80" height="130" fill="none" stroke="%2314b8a6" stroke-width="0.5"/><circle cx="50" cy="75" r="15" fill="none" stroke="%2314b8a6" stroke-width="0.5"/><line x1="10" y1="75" x2="90" y2="75" stroke="%2314b8a6" stroke-width="0.5"/></svg>') no-repeat center;
            background-size: contain;
            min-height: 400px;
            position: relative;
            margin: 2rem 0;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Player input section with enhanced UI
    st.markdown("### Add Players")
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        player_name = st.text_input("Player Name", placeholder="Enter name and press Enter", key="player_name_input", label_visibility="collapsed")
    
    with col2:
        age_bracket = st.selectbox("Age", ["20-25", "25-30", "30-35", "35-50", "50-60"], key="age_select", label_visibility="collapsed")
    
    with col3:
        position = st.selectbox("Position", ["Any", "GK", "DEF", "MID", "FWD"], key="position_select", label_visibility="collapsed")
    
    with col4:
        skill = st.selectbox("Skill", ["NA"] + list(range(1, 11)), key="skill_select", label_visibility="collapsed")
    
    # Add player on Enter key
    if player_name and st.session_state.get('player_name_input'):
        st.session_state.temp_players.append({
            'name': player_name,
            'age_bracket': age_bracket,
            'position': position,
            'skill': skill
        })
        st.success(f"Added {player_name}")
        # Clear the input
        st.session_state.player_name_input = ""
        st.rerun()
    
    # Initialize with sample players if empty
    if not st.session_state.temp_players:
        st.session_state.temp_players = [
            {'name': 'Arunav', 'age_bracket': '25-30', 'position': 'MID', 'skill': 8},
            {'name': 'Rohit', 'age_bracket': '30-35', 'position': 'DEF', 'skill': 7},
            {'name': 'Amit', 'age_bracket': '25-30', 'position': 'FWD', 'skill': 9},
            {'name': 'Vikram', 'age_bracket': '20-25', 'position': 'GK', 'skill': 6},
            {'name': 'Sandeep', 'age_bracket': '30-35', 'position': 'MID', 'skill': 7},
            {'name': 'Karthik', 'age_bracket': '25-30', 'position': 'DEF', 'skill': 8},
            {'name': 'Pranav', 'age_bracket': '20-25', 'position': 'FWD', 'skill': 8},
            {'name': 'Deepak', 'age_bracket': '35-50', 'position': 'MID', 'skill': 6},
            {'name': 'Nikhil', 'age_bracket': '25-30', 'position': 'DEF', 'skill': 7},
            {'name': 'Arjun', 'age_bracket': '30-35', 'position': 'FWD', 'skill': 7}
        ]
    
    # Show current players with remove option
    if st.session_state.temp_players:
        st.markdown("### Current Players")
        
        # Create a container for players
        player_container = st.container()
        
        with player_container:
            for i, player in enumerate(st.session_state.temp_players):
                col1, col2 = st.columns([10, 1])
                
                with col1:
                    player_display = f"**{player['name']}** | {player['age_bracket']} | {player['position']}"
                    if player['skill'] != 'NA':
                        player_display += f" | Skill: {player['skill']}"
                    st.markdown(player_display)
                
                with col2:
                    if st.button("❌", key=f"remove_{i}", help=f"Remove {player['name']}"):
                        st.session_state.temp_players.pop(i)
                        st.rerun()
        
        st.markdown(f"**Total Players:** {len(st.session_state.temp_players)}")
        
        # Generate teams button
        if len(st.session_state.temp_players) >= 10:
            if st.button("⚽ Generate Balanced Teams", type="primary", use_container_width=True):
                # Enhanced team generation with position consideration
                players = st.session_state.temp_players.copy()
                
                # Separate by position
                gks = [p for p in players if p['position'] == 'GK']
                defs = [p for p in players if p['position'] == 'DEF']
                mids = [p for p in players if p['position'] == 'MID']
                fwds = [p for p in players if p['position'] == 'FWD']
                others = [p for p in players if p['position'] == 'Any']
                
                # Shuffle each position group
                for group in [gks, defs, mids, fwds, others]:
                    random.shuffle(group)
                
                # Distribute players
                team_a, team_b = [], []
                
                # Distribute goalkeepers
                for i, gk in enumerate(gks):
                    if i % 2 == 0:
                        team_a.append(gk)
                    else:
                        team_b.append(gk)
                
                # Distribute other positions
                for group in [defs, mids, fwds]:
                    for i, player in enumerate(group):
                        if i % 2 == 0:
                            team_a.append(player)
                        else:
                            team_b.append(player)
                
                # Distribute 'Any' position players
                for i, player in enumerate(others):
                    if len(team_a) <= len(team_b):
                        team_a.append(player)
                    else:
                        team_b.append(player)
                
                # Display teams with formation
                st.markdown("### Generated Teams")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="team-display">
                        <h3 class="team-header">🔴 TEAM RED</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Group by position for display
                    red_formation = {"GK": [], "DEF": [], "MID": [], "FWD": [], "Any": []}
                    for player in team_a:
                        red_formation[player['position']].append(player)
                    
                    for pos in ["GK", "DEF", "MID", "FWD", "Any"]:
                        if red_formation[pos]:
                            st.markdown(f"**{pos}:**")
                            for player in red_formation[pos]:
                                st.markdown(f"• {player['name']} ({player['age_bracket']})")
                
                with col2:
                    st.markdown("""
                    <div class="team-display">
                        <h3 class="team-header">🔵 TEAM BLUE</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Group by position for display
                    blue_formation = {"GK": [], "DEF": [], "MID": [], "FWD": [], "Any": []}
                    for player in team_b:
                        blue_formation[player['position']].append(player)
                    
                    for pos in ["GK", "DEF", "MID", "FWD", "Any"]:
                        if blue_formation[pos]:
                            st.markdown(f"**{pos}:**")
                            for player in blue_formation[pos]:
                                st.markdown(f"• {player['name']} ({player['age_bracket']})")
                
                # Show formation visualization
                st.markdown("### Formation View")
                formation_col1, formation_col2 = st.columns(2)
                
                with formation_col1:
                    st.markdown("**Team Red Formation**")
                    st.info(f"GK: {len(red_formation['GK'])} | DEF: {len(red_formation['DEF'])} | MID: {len(red_formation['MID'])} | FWD: {len(red_formation['FWD'])}")
                
                with formation_col2:
                    st.markdown("**Team Blue Formation**")
                    st.info(f"GK: {len(blue_formation['GK'])} | DEF: {len(blue_formation['DEF'])} | MID: {len(blue_formation['MID'])} | FWD: {len(blue_formation['FWD'])}")
                
                # Save match option
                if st.button("💾 Save This Match", use_container_width=True):
                    match_data = {
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'team_a': team_a,
                        'team_b': team_b,
                        'score': "0-0"
                    }
                    st.session_state.match_history.append(match_data)
                    st.success("Match saved!")
        else:
            st.warning(f"Need at least 10 players to generate teams. Currently have {len(st.session_state.temp_players)}")
        
        # Clear players button
        if st.button("🗑️ Clear All Players", use_container_width=True):
            st.session_state.temp_players = []
            st.rerun()

# Previous Matches Section
if st.session_state.show_matches:
    st.markdown("---")
    st.markdown("## 📊 Previous Matches")
    
    if st.session_state.match_history:
        for i, match in enumerate(reversed(st.session_state.match_history)):
            with st.expander(f"Match {len(st.session_state.match_history) - i} - {match['date']} | Score: {match.get('score', '0-0')}"):
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.markdown("**🔴 Team Red:**")
                    for player in match['team_a']:
                        if isinstance(player, dict):
                            st.markdown(f"• {player['name']} ({player['position']})")
                        else:
                            st.markdown(f"• {player}")
                
                with col2:
                    st.markdown(f"### {match.get('score', '0-0')}")
                    # Option to update score
                    new_score = st.text_input("Update Score", value=match.get('score', '0-0'), key=f"score_{i}")
                    if new_score != match.get('score', '0-0'):
                        match['score'] = new_score
                        st.success("Score updated!")
                
                with col3:
                    st.markdown("**🔵 Team Blue:**")
                    for player in match['team_b']:
                        if isinstance(player, dict):
                            st.markdown(f"• {player['name']} ({player['position']})")
                        else:
                            st.markdown(f"• {player}")
    else:
        st.info("No matches recorded yet. Generate teams and save matches to see them here!")

# Learn Football Section
if st.session_state.show_learn:
    st.markdown("---")
    st.markdown("## 📚 Learn Football")
    
    from football_learning_engaging import (
        GOALKEEPER_CONTENT, DEFENDER_CONTENT, MIDFIELDER_CONTENT,
        FORWARD_CONTENT, TACTICS_CONTENT, FITNESS_CONTENT, PHILOSOPHY_CONTENT
    )
    
    # Position-specific training
    st.markdown("### Position Masterclass")
    
    position_tabs = st.tabs(["🥅 Goalkeeper", "🛡️ Defender", "⚽ Midfielder", "⚡ Forward", "📋 Tactics"])
    
    with position_tabs[0]:
        st.markdown(GOALKEEPER_CONTENT)
    
    with position_tabs[1]:
        st.markdown(DEFENDER_CONTENT)
    
    with position_tabs[2]:
        st.markdown(MIDFIELDER_CONTENT)
    
    with position_tabs[3]:
        st.markdown(FORWARD_CONTENT)
    
    with position_tabs[4]:
        st.markdown(TACTICS_CONTENT)
    
    # Additional sections
    with st.expander("💪 Complete Football Fitness Guide"):
        st.markdown(FITNESS_CONTENT)
    
    with st.expander("🧠 Football Philosophy & Styles"):
        st.markdown(PHILOSOPHY_CONTENT)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #94a3b8;">
    <p style="font-size: 0.9rem;">
        Weekend Squad - Where passion meets strategy
    </p>
</div>
""", unsafe_allow_html=True)