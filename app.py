import streamlit as st
import pandas as pd
import io
from football_team_manager import FootballManager, Player, Position, PlayerStatus

st.set_page_config(
    page_title="⚽ Football Team Generator",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .player-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #007bff;
        margin: 0.5rem 0;
    }
    .stButton > button {
        background: linear-gradient(45deg, #28a745, #20c997);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #218838, #1e7e34);
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# Initialize manager without sample players
if 'manager' not in st.session_state:
    manager = FootballManager()
    st.session_state.manager = manager

manager = st.session_state.manager

# Main header
st.markdown("""
<div class="main-header">
    <h1>⚽ Football Team Generator</h1>
    <p>Generate balanced teams with smart player management!</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for file upload
with st.sidebar:
    st.header("📁 Import Players")
    
    # File upload section
    uploaded_file = st.file_uploader(
        "Upload CSV or Excel file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload a file with columns: Name, Age, Position, Skill, Fitness"
    )
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            st.success(f"✅ File uploaded successfully! Found {len(df)} players.")
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(), use_container_width=True)
            
            if st.button("🚀 Import Players", type="primary"):
                # Clear existing players
                manager.players = []
                
                # Process each row
                for index, row in df.iterrows():
                    try:
                        # Map column names (case-insensitive)
                        name_col = None
                        age_col = None
                        position_col = None
                        skill_col = None
                        fitness_col = None
                        
                        for col in df.columns:
                            col_lower = col.lower()
                            if 'name' in col_lower:
                                name_col = col
                            elif 'age' in col_lower:
                                age_col = col
                            elif 'position' in col_lower or 'pos' in col_lower:
                                position_col = col
                            elif 'skill' in col_lower or 'rating' in col_lower:
                                skill_col = col
                            elif 'fitness' in col_lower or 'stamina' in col_lower:
                                fitness_col = col
                        
                        if name_col is None:
                            st.error("Could not find 'Name' column in the file")
                            break
                        
                        # Extract values with defaults
                        name = str(row[name_col]).strip()
                        age = int(row[age_col]) if age_col and pd.notna(row[age_col]) else 25
                        position_str = str(row[position_col]).upper() if position_col and pd.notna(row[position_col]) else 'MID'
                        skill = int(row[skill_col]) if skill_col and pd.notna(row[skill_col]) else 7
                        fitness = int(row[fitness_col]) if fitness_col and pd.notna(row[fitness_col]) else 7
                        
                        # Normalize position
                        if 'GK' in position_str or 'GOAL' in position_str:
                            position = Position.GOALKEEPER
                        elif 'DEF' in position_str or 'BACK' in position_str:
                            position = Position.DEFENDER
                        elif 'MID' in position_str or 'CENT' in position_str:
                            position = Position.MIDFIELDER
                        elif 'FWD' in position_str or 'FOR' in position_str or 'ATT' in position_str:
                            position = Position.FORWARD
                        else:
                            position = Position.MIDFIELDER
                        
                        # Create player
                        player = Player(
                            id=index + 1,
                            name=name,
                            age=age,
                            primary_position=position,
                            skill_level=skill,
                            fitness=fitness,
                            consistency=7
                        )
                        manager.add_player(player)
                        
                    except Exception as e:
                        st.warning(f"Error processing row {index + 1}: {str(e)}")
                        continue
                
                st.success(f"✅ Successfully imported {len(manager.players)} players!")
                st.rerun()
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")
    
    # Sample data download
    st.markdown("---")
    st.subheader("📥 Sample Data")
    
    # Create sample CSV
    sample_data = {
        'Name': ['Alex Thompson', 'James Rodriguez', 'Lucas Silva', 'Sergio Martinez', 'Mike Johnson'],
        'Age': [26, 28, 26, 23, 25],
        'Position': ['GK', 'DEF', 'MID', 'FWD', 'DEF'],
        'Skill': [8, 7, 9, 9, 6],
        'Fitness': [9, 8, 8, 8, 7]
    }
    sample_df = pd.DataFrame(sample_data)
    
    csv = sample_df.to_csv(index=False)
    st.download_button(
        label="📄 Download Sample CSV",
        data=csv,
        file_name="sample_players.csv",
        mime="text/csv"
    )

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Squad Status")
    
    if manager.players:
        status = manager.get_squad_status()
        
        # Metrics in cards
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        with metric_col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{status['total_players']}</h3>
                <p>Total Players</p>
            </div>
            """, unsafe_allow_html=True)
        with metric_col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{status['available']}</h3>
                <p>Available</p>
            </div>
            """, unsafe_allow_html=True)
        with metric_col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>{status['week']}</h3>
                <p>Current Week</p>
            </div>
            """, unsafe_allow_html=True)
        with metric_col4:
            avg_rating = sum(p.get_overall_rating() for p in manager.players) / len(manager.players) if manager.players else 0
            st.markdown(f"""
            <div class="metric-card">
                <h3>{avg_rating:.1f}</h3>
                <p>Avg Rating</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Top performers
        st.subheader("🏆 Top Performers")
        for performer in status['top_performers']:
            st.markdown(f"""
            <div class="player-card">
                <strong>{performer['name']}</strong> ({performer['position']})<br>
                Rating: {performer['rating']} | Form: {performer['form']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👥 No players in the squad yet. Upload a file or add players manually!")

with col2:
    st.header("🎲 Generate Team")
    
    if manager.players and len(manager.players) >= 7:
        if st.button("⚽ Generate Weekly Team", type="primary", use_container_width=True):
            try:
                team, details = manager.generate_weekly_team()
                
                st.success("✅ Team generated successfully!")
                
                st.subheader("Selected Team")
                for player in team:
                    rating = player.get_overall_rating()
                    st.markdown(f"""
                    <div class="player-card">
                        <strong>{player.name}</strong> ({player.primary_position.value})<br>
                        Rating: {rating:.1f}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if player.name in details["selection_reasoning"]:
                        reason = details["selection_reasoning"][player.name]
                        st.caption(f"Score: {reason['score']:.1f} | Form: {reason['form']:.1f} | Fatigue: {reason['fatigue']:.1f}")
            except Exception as e:
                st.error(f"❌ Error generating team: {str(e)}")
    else:
        st.warning("⚠️ Need at least 7 players to generate a team!")

# Player Management Section
st.header("👥 Player Management")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add Player", "👀 View All Players", "📊 Team Stats", "⚽ Match Analysis"])

with tab1:
    st.subheader("Add New Player")
    
    with st.form("add_player_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Player Name", placeholder="Enter full name")
            age = st.number_input("Age", min_value=16, max_value=50, value=25)
            position = st.selectbox("Primary Position", 
                                  ["GK", "DEF", "MID", "FWD"],
                                  format_func=lambda x: {"GK": "🥅 Goalkeeper", "DEF": "🛡️ Defender", 
                                                       "MID": "⚽ Midfielder", "FWD": "🎯 Forward"}[x])
        
        with col2:
            skill = st.slider("Skill Level", 1, 10, 7, help="Player's skill in their position")
            fitness = st.slider("Fitness", 1, 10, 8, help="Current fitness level")
            consistency = st.slider("Consistency", 1, 10, 5, help="How reliable they are")
        
        submitted = st.form_submit_button("➕ Add Player", use_container_width=True)
        
        if submitted and name:
            try:
                position_enum = Position(position)
                new_player = Player(
                    id=len(manager.players) + 1,
                    name=name,
                    age=age,
                    primary_position=position_enum,
                    skill_level=skill,
                    fitness=fitness,
                    consistency=consistency
                )
                manager.add_player(new_player)
                st.success(f"✅ Added {name} to the squad!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error adding player: {str(e)}")

with tab2:
    st.subheader("All Players")
    
    if manager.players:
        # Search and filter
        search = st.text_input("🔍 Search players", placeholder="Type player name...")
        
        filtered_players = manager.players
        if search:
            filtered_players = [p for p in manager.players if search.lower() in p.name.lower()]
        
        if filtered_players:
            for player in filtered_players:
                with st.expander(f"👤 {player.name} ({player.primary_position.value})"):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write("**Basic Info:**")
                        st.write(f"Age: {player.age}")
                        st.write(f"Position: {player.primary_position.value}")
                        st.write(f"Status: {player.status.value}")
                    with col2:
                        st.write("**Attributes:**")
                        st.write(f"Skill: {player.skill_level}/10")
                        st.write(f"Fitness: {player.fitness}/10")
                        st.write(f"Consistency: {player.consistency}/10")
                    with col3:
                        st.write("**Performance:**")
                        st.write(f"Overall Rating: {player.get_overall_rating():.1f}")
                        st.write(f"Current Form: {player.current_form:.1f}")
                        st.write(f"Morale: {player.morale:.1f}")
                        st.write(f"Fatigue: {player.fatigue:.1f}")
                    
                    # Remove player button
                    if st.button(f"🗑️ Remove {player.name}", key=f"remove_{player.id}"):
                        manager.players.remove(player)
                        st.success(f"✅ Removed {player.name}")
                        st.rerun()
        else:
            st.info("No players found matching your search.")
    else:
        st.info("👥 No players in the squad yet. Add some players to get started!")

with tab3:
    st.subheader("Team Statistics")
    
    if manager.players:
        # Position distribution
        positions = [p.primary_position.value for p in manager.players]
        position_counts = pd.Series(positions).value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Position Distribution:**")
            for pos, count in position_counts.items():
                st.write(f"{pos}: {count} players")
        
        with col2:
            st.write("**Age Distribution:**")
            ages = [p.age for p in manager.players]
            avg_age = sum(ages) / len(ages)
            st.write(f"Average Age: {avg_age:.1f}")
            st.write(f"Oldest: {max(ages)}")
            st.write(f"Youngest: {min(ages)}")
        
        # Performance metrics
        st.write("**Performance Metrics:**")
        ratings = [p.get_overall_rating() for p in manager.players]
        st.write(f"Average Rating: {sum(ratings)/len(ratings):.1f}")
        st.write(f"Highest Rating: {max(ratings):.1f}")
        st.write(f"Lowest Rating: {min(ratings):.1f}")
    else:
        st.info("No players to display statistics for.")

with tab4:
    st.subheader("⚽ Match Analysis")
    
    st.markdown("""
    <div style="text-align: center; padding: 3rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 15px; color: white;">
        <h2>🚧 Coming Soon! 🚧</h2>
        <p style="font-size: 1.2em; margin: 1rem 0;">Stay tuned for advanced match analysis features!</p>
        <div style="margin: 2rem 0;">
            <p><strong>📊 What's coming:</strong></p>
            <ul style="text-align: left; display: inline-block; margin: 1rem 0;">
                <li>Match performance tracking</li>
                <li>Player form analysis</li>
                <li>Team chemistry insights</li>
                <li>Historical match data</li>
                <li>Performance trends</li>
                <li>Advanced statistics</li>
            </ul>
        </div>
        <p style="font-style: italic;">We're working hard to bring you the best football team management experience!</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** This feature will allow you to track player performance over time, analyze team chemistry, and make data-driven decisions for team selection!")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666;">
    <p>⚽ Football Team Generator - Powered by Advanced AI Algorithms</p>
    <p>Upload CSV/Excel files or add players manually to generate balanced teams!</p>
</div>
""", unsafe_allow_html=True) 