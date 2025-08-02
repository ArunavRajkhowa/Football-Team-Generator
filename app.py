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
        animation: scrollQuotes 60s linear infinite;
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
    
    # Player input section
    st.markdown("### Add Players")
    
    with st.form("quick_team_gen", clear_on_submit=False):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            player_name = st.text_input("Player Name", placeholder="Enter player name")
        
        with col2:
            add_player = st.form_submit_button("Add Player", use_container_width=True)
        
        if add_player and player_name:
            # Simple player addition
            st.session_state.temp_players.append({
                'name': player_name,
                'position': 'Any'
            })
            st.success(f"Added {player_name}")
    
    # Show current players
    if st.session_state.temp_players:
        st.markdown("### Current Players")
        
        cols = st.columns(4)
        for i, player in enumerate(st.session_state.temp_players):
            with cols[i % 4]:
                st.markdown(f"""
                <div class="player-line">
                    <span>{player['name']}</span>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown(f"**Total Players:** {len(st.session_state.temp_players)}")
        
        # Generate teams button
        if len(st.session_state.temp_players) >= 10:
            if st.button("🎯 Generate Balanced Teams", type="primary", use_container_width=True):
                # Simple team split
                players = st.session_state.temp_players.copy()
                random.shuffle(players)
                
                mid_point = len(players) // 2
                team_a = players[:mid_point]
                team_b = players[mid_point:]
                
                # Display teams
                st.markdown("### Generated Teams")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="team-display">
                        <h3 class="team-header">🔴 TEAM RED</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for player in team_a:
                        st.markdown(f"• {player['name']}")
                
                with col2:
                    st.markdown("""
                    <div class="team-display">
                        <h3 class="team-header">🔵 TEAM BLUE</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for player in team_b:
                        st.markdown(f"• {player['name']}")
                
                # Save match option
                if st.button("💾 Save This Match", use_container_width=True):
                    match_data = {
                        'date': datetime.now().strftime("%Y-%m-%d"),
                        'team_a': [p['name'] for p in team_a],
                        'team_b': [p['name'] for p in team_b],
                        'score': "0-0"
                    }
                    st.session_state.match_history.append(match_data)
                    st.success("Match saved!")
                    st.session_state.temp_players = []
        
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
            with st.expander(f"Match {len(st.session_state.match_history) - i} - {match['date']}"):
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.markdown("**Team Red:**")
                    for player in match['team_a']:
                        st.markdown(f"• {player}")
                
                with col2:
                    st.markdown(f"### {match['score']}")
                
                with col3:
                    st.markdown("**Team Blue:**")
                    for player in match['team_b']:
                        st.markdown(f"• {player}")
    else:
        st.info("No matches recorded yet. Generate teams and save matches to see them here!")

# Learn Football Section
if st.session_state.show_learn:
    st.markdown("---")
    st.markdown("## 📚 Learn Football")
    
    from football_learning import (
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