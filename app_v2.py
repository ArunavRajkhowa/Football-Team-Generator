import streamlit as st
import pandas as pd
import random
from datetime import datetime
from football_team_manager import FootballManager, Player, Position, PlayerStatus

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
    
    /* Quote card */
    .quote-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin: 2rem 0;
        border-left: 5px solid #ff6b6b;
        position: relative;
    }
    
    .quote-text {
        font-size: 1.3rem;
        font-style: italic;
        color: #2c3e50;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    .quote-author {
        text-align: right;
        color: #7f8c8d;
        font-weight: 500;
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
</style>
""", unsafe_allow_html=True)

# Initialize session states
if 'manager' not in st.session_state:
    st.session_state.manager = FootballManager()
if 'show_advanced' not in st.session_state:
    st.session_state.show_advanced = False
if 'daily_quote' not in st.session_state:
    # Get a quote based on the day
    day_index = datetime.now().day % len(FOOTBALL_QUOTES)
    st.session_state.daily_quote = FOOTBALL_QUOTES[day_index]

manager = st.session_state.manager

# Hero Section
st.markdown("""
<div class="hero-section">
    <h1 class="hero-title">⚽ WEEKEND SQUAD</h1>
    <p class="hero-subtitle">Where every player gets their moment to shine</p>
</div>
""", unsafe_allow_html=True)

# Daily Quote
st.markdown(f"""
<div class="quote-card">
    <div class="quote-text">"{st.session_state.daily_quote['quote']}"</div>
    <div class="quote-author">- {st.session_state.daily_quote['author']}</div>
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

# Main Action Section
st.markdown("### 🎯 Quick Actions")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Add Player", use_container_width=True):
        st.session_state.show_add_player = True

with col2:
    if st.button("📋 Import Squad", use_container_width=True):
        st.session_state.show_import = True

with col3:
    if manager.players and len(manager.players) >= 14:
        if st.button("⚡ Generate Teams", use_container_width=True, type="primary"):
            st.session_state.show_teams = True

# Add Player Section (Simplified)
if 'show_add_player' in st.session_state and st.session_state.show_add_player:
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
            st.success(f"✅ {name} joined the squad!")
            st.session_state.show_add_player = False
            st.rerun()

# Import Section (Simplified)
if 'show_import' in st.session_state and st.session_state.show_import:
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
                        name = str(row.iloc[0]).strip()
                        age = int(row.iloc[1]) if len(row) > 1 else 25
                        pos_str = str(row.iloc[2]).upper() if len(row) > 2 else 'MID'
                        
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
                    st.markdown(f"""
                    <div class="player-card-new">
                        <strong>{player.name}</strong> {age_emoji}
                        <span class="position-badge badge-{pos.lower()}">{player.age} yrs</span>
                    </div>
                    """, unsafe_allow_html=True)

# Team Generation Display
if 'show_teams' in st.session_state and st.session_state.show_teams:
    st.markdown("---")
    st.markdown("### ⚡ This Week's Teams")
    
    try:
        team, details = manager.generate_weekly_team()
        
        # Split into two teams
        team_a = team[:7]
        team_b = team[7:14] if len(team) >= 14 else []
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="team-display">
                <h3 style="text-align: center; margin-bottom: 1rem;">🔴 RED TEAM</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for player in team_a:
                pos_emoji = {"GK": "🥅", "DEF": "🛡️", "MID": "⚽", "FWD": "⚡"}
                st.markdown(f"{pos_emoji.get(player.primary_position.value, '⚽')} **{player.name}** ({player.age})")
        
        with col2:
            st.markdown("""
            <div class="team-display">
                <h3 style="text-align: center; margin-bottom: 1rem;">🔵 BLUE TEAM</h3>
            </div>
            """, unsafe_allow_html=True)
            
            for player in team_b:
                pos_emoji = {"GK": "🥅", "DEF": "🛡️", "MID": "⚽", "FWD": "⚡"}
                st.markdown(f"{pos_emoji.get(player.primary_position.value, '⚽')} **{player.name}** ({player.age})")
        
        # Fun team facts
        st.markdown("### 🎉 Fun Facts")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            youngest = min(team, key=lambda p: p.age)
            st.info(f"👶 Youngest: {youngest.name} ({youngest.age})")
        
        with col2:
            oldest = max(team, key=lambda p: p.age)
            st.info(f"👴 Most Experienced: {oldest.name} ({oldest.age})")
        
        with col3:
            avg_age_team = sum(p.age for p in team) / len(team)
            st.info(f"📊 Average Age: {avg_age_team:.1f} years")
            
    except Exception as e:
        st.error("Need at least 14 players to make two teams!")

else:
    # Welcome message for new users
    if not manager.players:
        st.markdown("""
        ### 👋 Welcome to Weekend Squad!
        
        Ready to organize your next football match? Let's get started:
        
        1. **Add your players** - Just need their name, age, and position
        2. **Generate teams** - We'll create balanced squads automatically
        3. **Play football!** - Enjoy your weekend match
        
        No complicated stats, no complex forms. Just pure football fun! ⚽
        """)

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