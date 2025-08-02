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
        animation: scrollQuotes 300s linear infinite;
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
    
    /* Football Field Styling */
    .football-field {
        background: linear-gradient(90deg, #2d5016 0%, #4a7c22 50%, #2d5016 100%);
        border: 3px solid #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        position: relative;
        min-height: 400px;
        display: flex;
        background-image: 
            linear-gradient(0deg, transparent 49%, rgba(255,255,255,0.3) 50%, transparent 51%),
            linear-gradient(90deg, transparent 49%, rgba(255,255,255,0.3) 50%, transparent 51%);
        background-size: 40px 40px;
    }
    
    .field-half {
        width: 50%;
        height: 100%;
        display: flex;
        flex-direction: column;
        align-items: center;
        position: relative;
        padding: 20px 10px;
    }
    
    .team-name {
        background: rgba(255,255,255,0.9);
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: bold;
        margin-bottom: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }
    
    .team-red .team-name {
        background: linear-gradient(135deg, #ff4444, #cc0000);
        color: white;
    }
    
    .team-blue .team-name {
        background: linear-gradient(135deg, #4444ff, #0000cc);
        color: white;
    }
    
    .player-icon {
        background: #ffffff;
        border: 2px solid #333;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 10px;
        font-weight: bold;
        margin: 5px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.4);
        cursor: pointer;
        transition: all 0.3s ease;
        position: relative;
        text-align: center;
        line-height: 1.1;
    }
    
    .player-icon:hover {
        transform: scale(1.1);
        box-shadow: 0 4px 12px rgba(0,0,0,0.6);
    }
    
    .player-gk {
        background: linear-gradient(135deg, #ffff00, #e6e600);
        border-color: #b3b300;
        color: #333;
    }
    
    .player-def {
        background: linear-gradient(135deg, #4169e1, #1e3a8a);
        color: white;
        border-color: #1e3a8a;
    }
    
    .player-mid {
        background: linear-gradient(135deg, #32cd32, #228b22);
        color: white;
        border-color: #228b22;
    }
    
    .player-fwd {
        background: linear-gradient(135deg, #ff6347, #dc143c);
        color: white;
        border-color: #dc143c;
    }
    
    .player-any {
        background: linear-gradient(135deg, #9370db, #663399);
        color: white;
        border-color: #663399;
    }
    
    .formation-line {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        margin: 10px 0;
        gap: 10px;
    }
    
    .substitute-area {
        background: rgba(255,255,255,0.1);
        border: 2px dashed rgba(255,255,255,0.5);
        border-radius: 8px;
        padding: 15px;
        margin: 15px 0;
        text-align: center;
    }
    
    .substitute-title {
        color: #ffffff;
        font-weight: bold;
        margin-bottom: 10px;
        font-size: 16px;
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
    st.markdown('<p style="color: #7fafdf; font-size: 14px; margin-bottom: 15px;">Fill in player details below and click "Add Player" to add them to your team</p>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
    
    with col1:
        st.markdown('<p style="color: #a0a0a0; font-size: 12px; margin-bottom: 2px;">👤 Player Name</p>', unsafe_allow_html=True)
        player_name = st.text_input("Player Name", placeholder="Enter player's full name", label_visibility="collapsed")
    
    with col2:
        st.markdown('<p style="color: #a0a0a0; font-size: 12px; margin-bottom: 2px;">🎂 Age Range</p>', unsafe_allow_html=True)
        age_bracket = st.selectbox("Age", ["20-25", "25-30", "30-35", "35-50", "50-60"], key="age_select", label_visibility="collapsed", help="Select the player's age bracket")
    
    with col3:
        st.markdown('<p style="color: #a0a0a0; font-size: 12px; margin-bottom: 2px;">⚽ Position</p>', unsafe_allow_html=True)
        position = st.selectbox("Position", ["Any", "GK", "DEF", "MID", "FWD"], key="position_select", label_visibility="collapsed", 
                               help="GK=Goalkeeper, DEF=Defender, MID=Midfielder, FWD=Forward")
    
    with col4:
        st.markdown('<p style="color: #a0a0a0; font-size: 12px; margin-bottom: 2px;">⭐ Skill Level</p>', unsafe_allow_html=True)
        skill = st.selectbox("Skill", ["NA"] + list(range(1, 11)), key="skill_select", label_visibility="collapsed",
                           help="Rate player skill from 1 (beginner) to 10 (professional), or NA if unknown")
    
    # Add player button
    if st.button("➕ Add Player", type="primary", use_container_width=True):
        if player_name:
            st.session_state.temp_players.append({
                'name': player_name,
                'age_bracket': age_bracket,
                'position': position,
                'skill': skill
            })
            st.success(f"Added {player_name}")
            st.rerun()
    
    # Initialize with sample players if empty - St Xavier's School Aug 2nd'25 Teams
    if not st.session_state.temp_players:
        st.session_state.temp_players = [
            # Team A Green Players
            {'name': 'Subhram', 'age_bracket': '20-25', 'position': 'GK', 'skill': 7},
            {'name': 'Chandan', 'age_bracket': '20-25', 'position': 'DEF', 'skill': 8},
            {'name': 'Deepankar B', 'age_bracket': '20-25', 'position': 'DEF', 'skill': 7},
            {'name': 'Dhun', 'age_bracket': '20-25', 'position': 'MID', 'skill': 8},
            {'name': 'Paldeep', 'age_bracket': '20-25', 'position': 'MID', 'skill': 7},
            {'name': 'Nikhil (Deepankar Friend)', 'age_bracket': '20-25', 'position': 'FWD', 'skill': 7},
            {'name': 'Shovans', 'age_bracket': '20-25', 'position': 'FWD', 'skill': 8},
            
            # Team B Orange Players
            {'name': 'Arunav', 'age_bracket': '20-25', 'position': 'GK', 'skill': 8},
            {'name': 'Priyam', 'age_bracket': '20-25', 'position': 'DEF', 'skill': 7},
            {'name': 'Gautam', 'age_bracket': '20-25', 'position': 'DEF', 'skill': 8},
            {'name': 'Dheeraj', 'age_bracket': '20-25', 'position': 'MID', 'skill': 7},
            {'name': 'Randeep', 'age_bracket': '20-25', 'position': 'MID', 'skill': 8},
            {'name': 'Abhishek', 'age_bracket': '20-25', 'position': 'FWD', 'skill': 7},
            {'name': 'Pallab', 'age_bracket': '20-25', 'position': 'FWD', 'skill': 8},
            {'name': 'Suraj', 'age_bracket': '20-25', 'position': 'Any', 'skill': 7}
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
                    # Handle both age_bracket (string) and age (int) formats
                    age_info = player.get('age_bracket', player.get('age', 'Unknown'))
                    player_display = f"**{player['name']}** | {age_info} | {player['position']}"
                    if player.get('skill', 'NA') != 'NA':
                        player_display += f" | Skill: {player['skill']}"
                    st.markdown(player_display)
                
                with col2:
                    if st.button("❌", key=f"remove_{i}", help=f"Remove {player['name']}"):
                        st.session_state.temp_players.pop(i)
                        st.rerun()
        
        st.markdown(f"**Total Players:** {len(st.session_state.temp_players)}")
        
        # Generate teams button
        if len(st.session_state.temp_players) >= 14:
            if st.button("⚽ Generate 7v7 Teams", type="primary", use_container_width=True):
                # Enhanced 7v7 team generation with position consideration
                players = st.session_state.temp_players.copy()
                random.shuffle(players)
                
                # Separate by position
                gks = [p for p in players if p['position'] == 'GK']
                defs = [p for p in players if p['position'] == 'DEF']
                mids = [p for p in players if p['position'] == 'MID']
                fwds = [p for p in players if p['position'] == 'FWD']
                others = [p for p in players if p['position'] == 'Any']
                
                # Shuffle each position group
                for group in [gks, defs, mids, fwds, others]:
                    random.shuffle(group)
                
                # Distribute players for 7v7 (1 GK + 6 outfield players each)
                team_a, team_b = [], []
                substitutes = []
                
                # Distribute goalkeepers (1 per team)
                for i, gk in enumerate(gks[:2]):  # Take first 2 GKs
                    if i % 2 == 0:
                        team_a.append(gk)
                    else:
                        team_b.append(gk)
                
                # Combine outfield players
                outfield_players = defs + mids + fwds + others
                random.shuffle(outfield_players)
                
                # Distribute outfield players (6 per team for 7v7)
                for i, player in enumerate(outfield_players[:12]):  # Take first 12 outfield players
                    if i % 2 == 0:
                        team_a.append(player)
                    else:
                        team_b.append(player)
                
                # Remaining players become substitutes
                substitutes = gks[2:] + outfield_players[12:]
                
                # Display teams with visual football field
                st.markdown("### 🏟️ 7v7 Football Field Formation")
                
                def create_player_icon(player, team_side=""):
                    """Create HTML for a player icon"""
                    pos_class = f"player-{player['position'].lower()}"
                    name_short = player['name'][:8] if len(player['name']) > 8 else player['name']
                    skill_indicator = f"⭐{player['skill']}" if player.get('skill', 'NA') != 'NA' else ""
                    
                    return f"""
                    <div class="player-icon {pos_class}" title="{player['name']} - {player['position']} - Age: {player.get('age_bracket', 'Unknown')} - Skill: {player.get('skill', 'NA')}">
                        <div style="font-size: 8px; line-height: 1.1;">
                            {name_short}<br/>
                            <span style="font-size: 6px;">{skill_indicator}</span>
                        </div>
                    </div>
                    """
                
                def organize_7v7_formation(team_players):
                    """Organize players into 7v7 formation (1-2-3-1 or 1-2-2-2)"""
                    formation = {"GK": [], "DEF": [], "MID": [], "FWD": [], "Any": []}
                    
                    for player in team_players:
                        formation[player['position']].append(player)
                    
                    # Arrange in formation lines for visual display
                    lines = []
                    
                    # Goalkeeper line
                    if formation["GK"]:
                        lines.append(formation["GK"][:1])  # Max 1 GK
                    
                    # Defense line (2 players)
                    defense_line = formation["DEF"][:2]
                    if len(defense_line) < 2 and formation["Any"]:
                        defense_line.extend(formation["Any"][:2-len(defense_line)])
                        formation["Any"] = formation["Any"][2-len(defense_line):]
                    lines.append(defense_line)
                    
                    # Midfield line (2-3 players)
                    mid_line = formation["MID"][:3]
                    if len(mid_line) < 2 and formation["Any"]:
                        mid_line.extend(formation["Any"][:2-len(mid_line)])
                        formation["Any"] = formation["Any"][2-len(mid_line):]
                    lines.append(mid_line)
                    
                    # Forward line (1-2 players)
                    fwd_line = formation["FWD"][:2]
                    if len(fwd_line) < 1 and formation["Any"]:
                        fwd_line.extend(formation["Any"][:1])
                        formation["Any"] = formation["Any"][1:]
                    lines.append(fwd_line)
                    
                    return lines
                
                # Create the visual football field
                st.markdown(f"""
                <div class="football-field">
                    <div class="field-half team-red">
                        <div class="team-name">🔴 TEAM RED</div>
                """, unsafe_allow_html=True)
                
                # Team A formation
                team_a_formation = organize_7v7_formation(team_a)
                for line in reversed(team_a_formation):  # Reverse to show from front to back
                    if line:
                        st.markdown('<div class="formation-line">', unsafe_allow_html=True)
                        for player in line:
                            st.markdown(create_player_icon(player, "red"), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("""
                    </div>
                    <div class="field-half team-blue">
                        <div class="team-name">🔵 TEAM BLUE</div>
                """, unsafe_allow_html=True)
                
                # Team B formation
                team_b_formation = organize_7v7_formation(team_b)
                for line in team_b_formation:  # Normal order for opposing team
                    if line:
                        st.markdown('<div class="formation-line">', unsafe_allow_html=True)
                        for player in line:
                            st.markdown(create_player_icon(player, "blue"), unsafe_allow_html=True)
                        st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown('</div></div>', unsafe_allow_html=True)
                
                # Show substitutes if any
                if substitutes:
                    st.markdown(f"""
                    <div class="substitute-area">
                        <div class="substitute-title">⚽ Substitutes ({len(substitutes)} players)</div>
                        <div style="display: flex; justify-content: center; flex-wrap: wrap; gap: 10px;">
                    """, unsafe_allow_html=True)
                    
                    for sub in substitutes:
                        st.markdown(create_player_icon(sub), unsafe_allow_html=True)
                    
                    st.markdown('</div></div>', unsafe_allow_html=True)
                
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
            st.warning(f"Need at least 14 players to generate 7v7 teams. Currently have {len(st.session_state.temp_players)}")
        
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
    st.markdown("## 📚 Complete Football Guide")
    
    from football_learning_engaging import (
        GOALKEEPER_CONTENT, DEFENDER_CONTENT, MIDFIELDER_CONTENT,
        FORWARD_CONTENT, TACTICS_CONTENT, FITNESS_CONTENT, PHILOSOPHY_CONTENT
    )
    
    # Main format selection
    st.markdown('<div style="text-align: center; margin: 20px 0;"><h3>Choose Your Football Format</h3></div>', unsafe_allow_html=True)
    
    format_col1, format_col2 = st.columns(2)
    
    with format_col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e40af, #3b82f6); padding: 25px; border-radius: 15px; text-align: center; margin: 10px;">
            <h2 style="color: white; margin: 0;">⚽ 11v11 Football</h2>
            <p style="color: #e2e8f0; margin: 10px 0 0 0;">Traditional full-field football with 11 players per team</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🏟️ Learn 11v11 Football", use_container_width=True, type="primary"):
            st.session_state.selected_format = "11v11"
    
    with format_col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #059669, #10b981); padding: 25px; border-radius: 15px; text-align: center; margin: 10px;">
            <h2 style="color: white; margin: 0;">🏃 7v7 Turf Football</h2>
            <p style="color: #e2e8f0; margin: 10px 0 0 0;">Fast-paced smaller format perfect for turf fields</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🌱 Learn 7v7 Football", use_container_width=True, type="secondary"):
            st.session_state.selected_format = "7v7"
    
    # Initialize selected format if not set
    if 'selected_format' not in st.session_state:
        st.session_state.selected_format = "7v7"  # Default to 7v7 since that's what we're focusing on
    
    st.markdown("---")
    
    # Display content based on selected format
    if st.session_state.selected_format == "11v11":
        st.markdown("## 🏟️ 11v11 Traditional Football Guide")
        st.markdown("""
        <div style="background: rgba(30, 64, 175, 0.1); padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #3b82f6;">
            <h4 style="color: #3b82f6; margin-top: 0;">Traditional 11v11 Formation</h4>
            <p><strong>Team Size:</strong> 11 players (1 GK + 10 outfield)</p>
            <p><strong>Field Size:</strong> 100-130 yards long, 50-100 yards wide</p>
            <p><strong>Popular Formations:</strong> 4-4-2, 4-3-3, 3-5-2, 4-2-3-1</p>
            <p><strong>Match Duration:</strong> 90 minutes (2x 45 min halves)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Position-specific training for 11v11
        position_tabs = st.tabs(["🥅 Goalkeeper", "🛡️ Defender", "⚽ Midfielder", "⚡ Forward", "📋 11v11 Tactics"])
        
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
    
    else:  # 7v7 format
        st.markdown("## 🌱 7v7 Turf Football Guide")
        st.markdown("""
        <div style="background: rgba(5, 150, 105, 0.1); padding: 20px; border-radius: 10px; margin: 15px 0; border-left: 4px solid #10b981;">
            <h4 style="color: #10b981; margin-top: 0;">Modern 7v7 Formation</h4>
            <p><strong>Team Size:</strong> 7 players (1 GK + 6 outfield)</p>
            <p><strong>Field Size:</strong> 50-70 yards long, 30-50 yards wide</p>
            <p><strong>Popular Formations:</strong> 1-2-2-2, 1-2-3-1, 1-3-2-1</p>
            <p><strong>Match Duration:</strong> 60 minutes (2x 30 min halves)</p>
        </div>
        """, unsafe_allow_html=True)
        
        # 7v7 specific content
        turf_tabs = st.tabs(["🥅 7v7 Goalkeeper", "🛡️ 7v7 Defense", "⚡ 7v7 Midfield", "🔥 7v7 Attack", "📋 7v7 Tactics"])
        
        with turf_tabs[0]:
            st.markdown("""
            ## 🥅 7v7 Goalkeeper Guide
            
            ### Key Differences from 11v11:
            - **Smaller Goal**: Usually 16ft x 7ft vs 24ft x 8ft
            - **More Action**: Constant involvement due to smaller field
            - **Quick Distribution**: Fast transitions are crucial
            - **Sweeper Role**: Often acts as extra defender
            
            ### Essential Skills:
            ✅ **Quick Reflexes** - Shots come faster and closer  
            ✅ **Distribution** - Accurate throws and kicks to start attacks  
            ✅ **Positioning** - Narrow angles, stay alert for through balls  
            ✅ **Communication** - Direct your defense constantly  
            
            ### 7v7 Goalkeeper Tips:
            🎯 Stay on your toes - quick reactions needed  
            🎯 Use hands for distribution when possible  
            🎯 Come off line to support defense  
            🎯 Practice throwing to wide players
            """)
        
        with turf_tabs[1]:
            st.markdown("""
            ## 🛡️ 7v7 Defense Guide
            
            ### Formation Options:
            - **2 Defenders**: Traditional back line
            - **3 Defenders**: Extra security with wing-backs
            - **1 Sweeper + 1 Marker**: Continental style
            
            ### Key Responsibilities:
            ✅ **Compact Defense** - Stay close together, minimal gaps  
            ✅ **Quick Transitions** - From defense to attack instantly  
            ✅ **Pressing** - Higher pressure due to smaller space  
            ✅ **Communication** - Organize your compact team  
            
            ### 7v7 Defensive Tips:
            🛡️ Always have one player covering  
            🛡️ Force play to the sides  
            🛡️ Win the ball and look forward immediately  
            🛡️ Use the shorter field to your advantage
            """)
        
        with turf_tabs[2]:
            st.markdown("""
            ## ⚡ 7v7 Midfield Guide
            
            ### The Engine Room:
            In 7v7, midfielders are the most important players - they must:
            - **Box-to-Box Play**: Defend and attack constantly
            - **Quick Passing**: Keep possession in tight spaces
            - **Transition Play**: Speed up or slow down the game
            
            ### Essential Skills:
            ✅ **First Touch** - Crucial in tight spaces  
            ✅ **Vision** - Find the killer pass quickly  
            ✅ **Stamina** - Cover more ground per player  
            ✅ **Pressing** - High energy defensive work  
            
            ### 7v7 Midfield Tips:
            ⚡ Always show for the ball  
            ⚡ Play one or two touch when under pressure  
            ⚡ Switch play to create space  
            ⚡ Track runners from deep
            """)
        
        with turf_tabs[3]:
            st.markdown("""
            ## 🔥 7v7 Attack Guide
            
            ### Attacking Philosophy:
            - **Quick Combinations**: 1-2 passes in tight areas
            - **Width**: Use the full width of the smaller field
            - **Pace**: Speed of thought over speed of foot
            - **Finishing**: Every chance counts more
            
            ### Forward Roles:
            ✅ **Target Player** - Hold up play and bring others in  
            ✅ **Pace Merchant** - Run in behind the defense  
            ✅ **Playmaker** - Drop deep and create chances  
            ✅ **Finisher** - Clinical in front of goal  
            
            ### 7v7 Attacking Tips:
            🔥 Make quick runs off the ball  
            🔥 Use the smaller goal to your advantage  
            🔥 Create overloads in wide areas  
            🔥 Be ready for rebounds and loose balls
            """)
        
        with turf_tabs[4]:
            st.markdown("""
            ## 📋 7v7 Tactical Guide
            
            ### Popular 7v7 Formations:
            
            #### 🔹 1-2-2-2 (Balanced)
            - **Best for**: Balanced teams
            - **Strengths**: Equal attack/defense
            - **Weaknesses**: Can be outnumbered in midfield
            
            #### 🔹 1-2-3-1 (Midfield Control)
            - **Best for**: Technical teams
            - **Strengths**: Dominates possession
            - **Weaknesses**: Less direct attacking threat
            
            #### 🔹 1-3-2-1 (Defensive)
            - **Best for**: Counter-attacking
            - **Strengths**: Solid defensively
            - **Weaknesses**: Limited creative options
            
            ### Key Tactical Principles:
            📋 **Compactness** - Keep players close together  
            📋 **Quick Transitions** - Switch between attack/defense rapidly  
            📋 **Overloads** - Create numerical advantages in key areas  
            📋 **Pressing** - Win the ball back quickly  
            
            ### Game Management:
            ⏱️ **Early Goals**: Try to score first  
            ⏱️ **Tempo Control**: Speed up when ahead, slow down when behind  
            ⏱️ **Substitutions**: Fresh legs are crucial  
            ⏱️ **Set Pieces**: Every corner/free kick is valuable
            """)
    
    # Additional sections (available for both formats)
    st.markdown("---")
    st.markdown("### 💪 Additional Resources")
    
    resource_col1, resource_col2 = st.columns(2)
    
    with resource_col1:
        with st.expander("💪 Complete Football Fitness Guide"):
            st.markdown(FITNESS_CONTENT)
    
    with resource_col2:
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