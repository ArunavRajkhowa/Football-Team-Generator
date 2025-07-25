import streamlit as st
from football_team_manager import FootballManager, Player, Position, PlayerStatus

st.set_page_config(
    page_title="⚽ Football Team Generator",
    page_icon="⚽",
    layout="wide"
)

if 'manager' not in st.session_state:
    manager = FootballManager()
    
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
st.markdown("Generate balanced teams with smart player management!")

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📊 Squad Status")
    status = manager.get_squad_status()
    
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Total Players", status['total_players'])
    with metric_col2:
        st.metric("Available", status['available'])
    with metric_col3:
        st.metric("Week", status['week'])
    
    st.subheader("🏆 Top Performers")
    for performer in status['top_performers']:
        st.write(f"• {performer['name']} ({performer['position']}) - Rating: {performer['rating']}, Form: {performer['form']}")

with col2:
    st.header("🎲 Generate Team")
    if st.button("Generate Weekly Team", type="primary"):
        try:
            team, details = manager.generate_weekly_team()
            
            st.success("Team generated successfully!")
            
            st.subheader("Selected Team")
            for player in team:
                rating = player.get_overall_rating()
                st.write(f"**{player.name}** ({player.primary_position.value}) - Rating: {rating:.1f}")
                
                if player.name in details["selection_reasoning"]:
                    reason = details["selection_reasoning"][player.name]
                    st.caption(f"Score: {reason['score']:.1f}, Form: {reason['form']:.1f}, Fatigue: {reason['fatigue']:.1f}")
        except Exception as e:
            st.error(f"Error generating team: {str(e)}")

st.header("👥 Player Management")

tab1, tab2, tab3 = st.tabs(["Add Player", "View All Players", "Record Match"])

with tab1:
    st.subheader("Add New Player")
    
    with st.form("add_player_form"):
        name = st.text_input("Player Name")
        age = st.number_input("Age", min_value=16, max_value=50, value=25)
        
        position = st.selectbox("Primary Position", 
                              ["GK", "DEF", "MID", "FWD"],
                              format_func=lambda x: {"GK": "🥅 Goalkeeper", "DEF": "🛡️ Defender", 
                                                   "MID": "⚽ Midfielder", "FWD": "🎯 Forward"}[x])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            skill = st.slider("Skill Level", 1, 10, 7)
        with col2:
            fitness = st.slider("Fitness", 1, 10, 8)
        with col3:
            consistency = st.slider("Consistency", 1, 10, 5)
        
        submitted = st.form_submit_button("Add Player")
        
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
                st.success(f"Added {name} to the squad!")
                st.rerun()
            except Exception as e:
                st.error(f"Error adding player: {str(e)}")

with tab2:
    st.subheader("All Players")
    
    if manager.players:
        for player in manager.players:
            with st.expander(f"{player.name} ({player.primary_position.value})"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Age:** {player.age}")
                    st.write(f"**Skill:** {player.skill_level}/10")
                    st.write(f"**Fitness:** {player.fitness}/10")
                    st.write(f"**Consistency:** {player.consistency}/10")
                with col2:
                    st.write(f"**Overall Rating:** {player.get_overall_rating():.1f}")
                    st.write(f"**Current Form:** {player.current_form:.1f}")
                    st.write(f"**Morale:** {player.morale:.1f}")
                    st.write(f"**Fatigue:** {player.fatigue:.1f}")
    else:
        st.info("No players in the squad yet.")

with tab3:
    st.subheader("Record Match Results")
    st.info("This feature will be implemented to track player performance over time.")
    st.write("Coming soon: Record match statistics, update player form, and track season history!")

st.markdown("---")
st.markdown("**Note:** This app uses your Football Team Manager backend for advanced team generation algorithms!") 