import streamlit as st
import pandas as pd
import random
from datetime import datetime
from football_team_manager import FootballManager, Player, Position, PlayerStatus
from simple_team_generator import SimplePlayer, SimpleTeamGenerator, Position as SimplePosition
from football_personality import FootballPersonality

# Football quotes for daily inspiration
FOOTBALL_QUOTES = [
    {"quote": "Football is a simple game. Twenty-two men chase a ball for 90 minutes and at the end, the Germans always win.", "author": "Gary Lineker"},
    {"quote": "Some people think football is a matter of life and death. I assure you, it's much more serious than that.", "author": "Bill Shankly"},
    {"quote": "The ball is round, the game lasts ninety minutes, and everything else is just theory.", "author": "Sepp Herberger"},
    {"quote": "Football is like life - it requires perseverance, self-denial, hard work, sacrifice, dedication and respect for authority.", "author": "Vince Lombardi"},
    {"quote": "In football, the worst blindness is only seeing the ball.", "author": "Nelson Falcão Rodrigues"},
    {"quote": "Take the ball, pass the ball.", "author": "Pep Guardiola"},
    {"quote": "Football is the ballet of the masses.", "author": "Dmitri Shostakovich"},
    {"quote": "I learned all about life with a ball at my feet.", "author": "Ronaldinho"},
    {"quote": "Football is played with the head. Your feet are just the tools.", "author": "Andrea Pirlo"},
    {"quote": "The more difficult the victory, the greater the happiness in winning.", "author": "Pelé"},
    {"quote": "Without football, my life is worth nothing.", "author": "Cristiano Ronaldo"},
    {"quote": "When people succeed, it is because of hard work. Luck has nothing to do with success.", "author": "Diego Maradona"},
    {"quote": "Every disadvantage has its advantage.", "author": "Johan Cruyff"},
    {"quote": "Football is a game about feelings and intelligence.", "author": "Jose Mourinho"},
    {"quote": "You have to fight to reach your dream. You have to sacrifice and work hard for it.", "author": "Lionel Messi"}
]

st.set_page_config(
    page_title="Weekend Football Squad",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern, clean CSS with football field inspiration
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;500;700&display=swap');
    
    /* Reset and base styles */
    .main {
        background: #f0f4f0;
    }
    
    /* Hero section with football field gradient */
    .hero-section {
        background: linear-gradient(180deg, #1a5f3f 0%, #2d7a4f 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 120px;
        height: 120px;
        border: 3px solid rgba(255,255,255,0.1);
        border-radius: 50%;
        transform: translate(-50%, -50%);
    }
    
    .hero-title {
        font-family: 'Bebas Neue', cursive;
        font-size: 4rem;
        margin: 0;
        letter-spacing: 2px;
        position: relative;
        z-index: 1;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        position: relative;
        z-index: 1;
    }
    
    /* Sliding Quote Banner */
    .quote-slider {
        background: linear-gradient(90deg, #f8f9fa, #e9ecef);
        border-radius: 10px;
        overflow: hidden;
        margin: 1rem 0;
        height: 50px;
        display: flex;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .quote-content {
        animation: slideLeft 30s linear infinite;
        white-space: nowrap;
        color: #495057;
        font-size: 0.95rem;
        font-style: italic;
        padding-left: 100%;
    }
    
    @keyframes slideLeft {
        0% { transform: translateX(0); }
        100% { transform: translateX(-100%); }
    }
    
    .quote-slider:hover .quote-content {
        animation-play-state: paused;
    }
    
    /* Player card redesign */
    .player-card-new {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
        border-left: 4px solid transparent;
    }
    
    .player-card-new:hover {
        transform: translateY(-3px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.15);
        border-left-color: #ff6b6b;
    }
    
    .position-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .badge-gk { background: #ffd93d; color: #333; }
    .badge-def { background: #6bcf7f; color: white; }
    .badge-mid { background: #4ecdc4; color: white; }
    .badge-fwd { background: #ff6b6b; color: white; }
    
    /* Team display */
    .team-display {
        background: linear-gradient(180deg, #2d7a4f 0%, #1a5f3f 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        position: relative;
        overflow: hidden;
    }
    
    .team-display::after {
        content: '';
        position: absolute;
        top: 50%;
        left: 0;
        right: 0;
        height: 2px;
        background: rgba(255,255,255,0.2);
    }
    
    /* Quick action buttons */
    .quick-action-btn {
        background: white;
        color: #2d7a4f;
        padding: 1rem 2rem;
        border-radius: 30px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        margin: 0.5rem;
        transition: all 0.3s ease;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .quick-action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(0,0,0,0.2);
        background: #2d7a4f;
        color: white;
    }
    
    /* Fun stats */
    .fun-stat {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
    }
    
    .fun-stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2d7a4f;
        margin: 0;
    }
    
    .fun-stat-label {
        color: #7f8c8d;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom buttons */
    .stButton > button {
        background: linear-gradient(45deg, #ff6b6b, #ff8787);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        font-weight: 600;
        border-radius: 30px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
    }
    
    /* Personality message */
    .personality-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    
    /* Welcome card */
    .welcome-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session states and services
if 'manager' not in st.session_state:
    st.session_state.manager = FootballManager()
if 'personality' not in st.session_state:
    st.session_state.personality = FootballPersonality()
if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False
if 'daily_quote' not in st.session_state:
    # Get a quote based on the day
    day_index = datetime.now().day % len(FOOTBALL_QUOTES)
    st.session_state.daily_quote = FOOTBALL_QUOTES[day_index]
if 'show_add_player' not in st.session_state:
    st.session_state.show_add_player = False
if 'show_import' not in st.session_state:
    st.session_state.show_import = False
if 'show_teams' not in st.session_state:
    st.session_state.show_teams = False

manager = st.session_state.manager
personality = st.session_state.personality

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">⚽ WEEKEND SQUAD</h1>
    <p class="hero-subtitle">Where every player gets their moment to shine</p>
</div>
""", unsafe_allow_html=True)

# Welcome message based on time (more subtle)
welcome_msg = personality.get_welcome_message()
st.markdown(f"<div style='text-align: center; color: #666; padding: 0.5rem; font-size: 0.9rem;'>{welcome_msg}</div>", unsafe_allow_html=True)

# Sliding Quote Banner
st.markdown(f"""
<div class="quote-slider">
    <div class="quote-content">
        💬 "{st.session_state.daily_quote['quote']}" - {st.session_state.daily_quote['author']}
    </div>
</div>
""", unsafe_allow_html=True)

# Quick Stats Row
if manager.players:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="fun-stat">
            <h2 class="fun-stat-number">{len(manager.players)}</h2>
            <p class="fun-stat-label">Squad Size</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_age = sum(p.age for p in manager.players) / len(manager.players)
        st.markdown(f"""
        <div class="fun-stat">
            <h2 class="fun-stat-number">{int(avg_age)}</h2>
            <p class="fun-stat-label">Average Age</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        # Fun stat: Most common position
        positions = [p.primary_position.value for p in manager.players]
        most_common = max(set(positions), key=positions.count) if positions else "N/A"
        st.markdown(f"""
        <div class="fun-stat">
            <h2 class="fun-stat-number">{most_common}</h2>
            <p class="fun-stat-label">Popular Position</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Games played this month (simulated)
        games_played = st.session_state.manager.week_number - 1
        st.markdown(f"""
        <div class="fun-stat">
            <h2 class="fun-stat-number">{games_played}</h2>
            <p class="fun-stat-label">Games Played</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Squad personality (subtle)
    squad_data = [{'age': p.age, 'position': p.primary_position.value} for p in manager.players]
    squad_personality = personality.get_squad_personality(squad_data)
    st.markdown(f"<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 0.5rem; font-style: italic;'>🎯 {squad_personality}</div>", unsafe_allow_html=True)

# Main Action Section
st.markdown("### 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add Player", use_container_width=True):
        st.session_state.show_add_player = not st.session_state.show_add_player
        st.session_state.show_import = False
        st.session_state.show_teams = False

with col2:
    if st.button("📋 Import Squad", use_container_width=True):
        st.session_state.show_import = not st.session_state.show_import
        st.session_state.show_add_player = False
        st.session_state.show_teams = False

with col3:
    if manager.players and len(manager.players) >= 14:
        if st.button("⚡ Generate Teams", use_container_width=True, type="primary"):
            st.session_state.show_teams = True
            st.session_state.show_add_player = False
            st.session_state.show_import = False
    else:
        st.button(f"⚡ Need {14 - len(manager.players)} more players", disabled=True, use_container_width=True)

# Random tip
tip = personality.get_random_tip()
st.info(tip)

# Add Player Section (Simplified)
if st.session_state.show_add_player:
    st.markdown("### 🆕 Add New Player")
    
    with st.form("quick_add_player", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Player Name", placeholder="e.g., John Smith")
            age = st.number_input("Age", min_value=16, max_value=60, value=25)
        
        with col2:
            position = st.selectbox(
                "Position",
                ["GK", "DEF", "MID", "FWD"],
                format_func=lambda x: {
                    "GK": "🥅 Goalkeeper",
                    "DEF": "🛡️ Defender",
                    "MID": "⚽ Midfielder",
                    "FWD": "⚡ Forward"
                }[x]
            )
            
            # Show advanced options toggle
            show_more = st.checkbox("Show more options (optional)")
        
        # Optional fields
        if show_more:
            col3, col4 = st.columns(2)
            with col3:
                skill = st.slider("Skill Level", 1, 10, 7)
            with col4:
                fitness = st.slider("Current Fitness", 1, 10, 8)
        else:
            skill = 7  # Default values
            fitness = 8
        
        submitted = st.form_submit_button("Add to Squad", use_container_width=True)
        
        if submitted and name:
            position_enum = Position(position)
            new_player = Player(
                id=len(manager.players) + 1,
                name=name,
                age=age,
                primary_position=position_enum,
                skill_level=skill,
                fitness=fitness,
                consistency=7
            )
            manager.add_player(new_player)
            
            # Personalized welcome message
            welcome = personality.get_player_welcome(name, age, position)
            st.success(welcome)
            
            st.session_state.show_add_player = False
            st.rerun()

# Import Section (Simplified)
if st.session_state.show_import:
    st.markdown("### 📁 Import Your Squad")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose your file",
            type=['csv', 'xlsx'],
            help="Simple format: Name, Age, Position (GK/DEF/MID/FWD)"
        )
        
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                
                st.success(f"Found {len(df)} players!")
                
                if st.button("Import All Players", type="primary"):
                    manager.players = []  # Clear existing
                    
                    for _, row in df.iterrows():
                        # Simple parsing - just need name, age, position
                        name = str(row.iloc[0]).strip() if len(row) > 0 else "Unknown"
                        age = int(row.iloc[1]) if len(row) > 1 and pd.notna(row.iloc[1]) else 25
                        pos_str = str(row.iloc[2]).upper() if len(row) > 2 and pd.notna(row.iloc[2]) else 'MID'
                        
                        # Map position
                        if 'GK' in pos_str or 'GOAL' in pos_str:
                            position = Position.GOALKEEPER
                        elif 'DEF' in pos_str:
                            position = Position.DEFENDER
                        elif 'MID' in pos_str:
                            position = Position.MIDFIELDER
                        elif 'FWD' in pos_str or 'FOR' in pos_str:
                            position = Position.FORWARD
                        else:
                            position = Position.MIDFIELDER
                        
                        player = Player(
                            id=len(manager.players) + 1,
                            name=name,
                            age=age,
                            primary_position=position,
                            skill_level=7,
                            fitness=8,
                            consistency=7
                        )
                        manager.add_player(player)
                    
                    st.success(f"✅ Imported {len(manager.players)} players!")
                    st.balloons()
                    st.session_state.show_import = False
                    st.rerun()
                    
            except Exception as e:
                st.error("Oops! Check your file format. Need: Name, Age, Position")
    
    with col2:
        st.markdown("#### 📝 Example Format")
        st.code("""Name,Age,Position
John Smith,25,GK
Mike Johnson,28,DEF
Tom Wilson,23,MID
Sam Roberts,26,FWD""")

# Current Squad Display
if manager.players:
    st.markdown("### 👥 Your Squad")
    
    # Group by position
    positions_order = ['GK', 'DEF', 'MID', 'FWD']
    
    for pos in positions_order:
        players_in_pos = [p for p in manager.players if p.primary_position.value == pos]
        if players_in_pos:
            pos_names = {"GK": "🥅 Goalkeepers", "DEF": "🛡️ Defenders", 
                        "MID": "⚽ Midfielders", "FWD": "⚡ Forwards"}
            st.markdown(f"**{pos_names[pos]}**")
            
            cols = st.columns(3)
            for i, player in enumerate(players_in_pos):
                with cols[i % 3]:
                    age_emoji = "🌟" if player.age < 23 else "⚡" if player.age < 30 else "👑"
                    nickname = personality.generate_player_nickname(player.name, pos, player.age)
                    st.markdown(f"""
                    <div class="player-card-new">
                        <strong>{player.name}</strong> {age_emoji}<br>
                        <small style="color: #7f8c8d;">{nickname}</small>
                        <span class="position-badge badge-{pos.lower()}">{player.age} yrs</span>
                    </div>
                    """, unsafe_allow_html=True)

# Team Generation Display
if st.session_state.show_teams and manager.players and len(manager.players) >= 14:
    st.markdown("---")
    st.markdown("### ⚡ This Week's Teams")
    
    try:
        # Use simple team generator for better balance
        simple_players = [
            SimplePlayer(
                name=p.name,
                age=p.age,
                position=SimplePosition(p.primary_position.value)
            ) for p in manager.players
        ]
        
        generator = SimpleTeamGenerator(simple_players)
        team_a, team_b = generator.generate_balanced_teams()
        
        # Pre-match message (subtle)
        pre_match = random.choice(personality.motivational_messages['pre_match'])
        st.markdown(f"<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 0.5rem;'>🎯 {pre_match}</div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            stats_a = generator.get_fun_stats(team_a)
            st.markdown(f"""
            <div class="team-display">
                <h3 style="text-align: center; margin-bottom: 1rem;">🔴 {stats_a['nickname'].upper()}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for player in team_a:
                pos_emoji = {"GK": "🥅", "DEF": "🛡️", "MID": "⚽", "FWD": "⚡"}
                st.markdown(f"{pos_emoji.get(player.position.value, '⚽')} **{player.name}** ({player.age})")
            
            # Team stats
            st.caption(f"Average age: {stats_a['average_age']} | Formation: {stats_a['formation']}")
        
        with col2:
            stats_b = generator.get_fun_stats(team_b)
            st.markdown(f"""
            <div class="team-display">
                <h3 style="text-align: center; margin-bottom: 1rem;">🔵 {stats_b['nickname'].upper()}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for player in team_b:
                pos_emoji = {"GK": "🥅", "DEF": "🛡️", "MID": "⚽", "FWD": "⚡"}
                st.markdown(f"{pos_emoji.get(player.position.value, '⚽')} **{player.name}** ({player.age})")
            
            # Team stats
            st.caption(f"Average age: {stats_b['average_age']} | Formation: {stats_b['formation']}")
        
        # Team ready message (subtle)
        team_ready = random.choice(personality.motivational_messages['team_ready'])
        st.markdown(f"<div style='text-align: center; color: #666; font-size: 0.9rem; padding: 0.5rem;'>⚽ {team_ready}</div>", unsafe_allow_html=True)
        
        # Fun team facts
        st.markdown("### 🎉 Match Day Facts")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"👶 Youngest: {stats_a['youngest'].name} ({stats_a['youngest'].age}) vs {stats_b['youngest'].name} ({stats_b['youngest'].age})")
        
        with col2:
            st.info(f"👴 Veterans: {stats_a['oldest'].name} ({stats_a['oldest'].age}) vs {stats_b['oldest'].name} ({stats_b['oldest'].age})")
        
        with col3:
            age_diff = abs(stats_a['average_age'] - stats_b['average_age'])
            st.info(f"⚖️ Age balance: {age_diff:.1f} years difference")
        
        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 Regenerate Teams", use_container_width=True):
                st.rerun()
        with col2:
            if st.button("💾 Save These Teams", use_container_width=True):
                st.success("Teams saved! Good luck in your match! 🏆")
            
    except Exception as e:
        st.error(f"Need at least 14 players to make two teams! Currently have {len(manager.players)}")

else:
    # Welcome message for new users
    if not manager.players:
        st.markdown("""
        <div class="welcome-card">
            <h3>👋 Welcome to Weekend Squad!</h3>
            <p style="font-size: 1.1rem; margin: 1rem 0;">
                Ready to organize your next football match? Let's get started!
            </p>
            <div style="text-align: left; display: inline-block; margin: 1rem 0;">
                <p>✅ Add your players - Just name, age, and position</p>
                <p>✅ Generate balanced teams automatically</p>
                <p>✅ Get motivated with daily football quotes</p>
                <p>✅ Track your weekend football journey</p>
            </div>
            <p style="font-size: 1.2rem; margin-top: 1rem;">
                No complicated stats. Just pure football fun! ⚽
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer with motivation
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #7f8c8d;">
    <p style="font-size: 1.1rem; margin-bottom: 0.5rem;">
        "The beautiful game brings us together"
    </p>
    <p style="font-size: 0.9rem;">
        Made with ❤️ for weekend warriors everywhere
    </p>
</div>
""", unsafe_allow_html=True)