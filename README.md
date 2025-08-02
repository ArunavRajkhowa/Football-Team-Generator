# ⚽ Weekend Football Squad

A personal, engaging football team generator that makes organizing weekend matches fun and fair!

## 🚀 Live App

**Use it now:** [https://football-team-generator-lachitfc.streamlit.app/](https://football-team-generator-lachitfc.streamlit.app/)

## ✨ Features

- 🎯 **Daily Football Quotes** - Get inspired by legends like Pelé, Messi, and Cruyff
- 👥 **Simple Player Management** - Just name, age, and position needed
- ⚖️ **Smart Team Generation** - Balanced teams based on age and position
- 🎭 **Player Personalities** - Auto-generated fun nicknames and squad analysis
- 📱 **Mobile Friendly** - Works perfectly on phones for WhatsApp groups
- 🎉 **Fun First** - Focus on enjoyment rather than complex statistics

## 🏃 How to Run Locally

### Option 1: Quick Start (Recommended)
```bash
# Clone the repository
git clone https://github.com/ArunavRajkhowa/Football-Team-Generator.git
cd Football-Team-Generator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Option 2: Using Virtual Environment (Recommended for development)
```bash
# Clone the repository
git clone https://github.com/ArunavRajkhowa/Football-Team-Generator.git
cd Football-Team-Generator

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📁 Project Structure

```
Football-Team-Generator/
├── app.py                      # Main Streamlit application
├── football_team_manager.py    # Core team management logic
├── football_personality.py     # Personality and motivational features
├── simple_team_generator.py    # Simplified team generation algorithm
├── requirements.txt            # Python dependencies
└── README.md                  # This file
```

## 🎯 How to Use

1. **Add Players** - Click "Add Player" and enter name, age, and position
2. **Import Squad** - Upload a CSV with your team (Name, Age, Position format)
3. **Generate Teams** - Hit the big button once you have 14+ players
4. **Share & Play** - Copy teams to WhatsApp and enjoy your match!

## 📊 CSV Import Format

Your CSV file should have these columns:
```csv
Name,Age,Position
John Smith,25,GK
Mike Johnson,28,DEF
Tom Wilson,23,MID
Sam Roberts,26,FWD
```

**Positions:** Use GK (Goalkeeper), DEF (Defender), MID (Midfielder), FWD (Forward)

## 🌟 What Makes This Special

- **Personal Touch** - Every action has a personalized, motivational response
- **Time-Based Greetings** - Different welcome messages for morning/afternoon/evening
- **Squad Personality** - Your team gets analyzed and given a unique personality
- **Fun Team Names** - Teams get nicknames like "Young Guns" or "The Veterans"
- **Match Day Facts** - Interesting comparisons between the generated teams
- **Daily Motivation** - Random football tips and quotes to keep you inspired

## 🔧 Dependencies

- `streamlit` - Web app framework
- `pandas` - Data manipulation
- `openpyxl` - Excel file support
- `xlrd` - Additional Excel support

## 🚀 Deploy Your Own

### Deploy to Streamlit Cloud (Free)
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your forked repository
5. Set main file as `app.py`
6. Deploy!

### Deploy to Heroku
1. Fork this repository
2. Create a new Heroku app
3. Connect your GitHub repository
4. Deploy from the main branch

## 🎮 Perfect For

- Weekend football leagues
- Office team matches
- Friend group games
- Youth team organization
- Casual pickup games
- WhatsApp football groups

## 💝 Philosophy

This app is built for people who love football for the pure joy of playing. No complex statistics, no overwhelming features - just balanced teams and good vibes. Every weekend warrior deserves fair, fun matches with their friends!

## 🤝 Contributing

Feel free to fork, improve, and submit pull requests! This project is all about making weekend football more enjoyable for everyone.

## 📄 License

Open source and free to use for all football enthusiasts!

---

**Made with ❤️ for weekend warriors everywhere** ⚽