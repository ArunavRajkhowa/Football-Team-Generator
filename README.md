# ⚽ Football Team Generator - Free Web App

Generate balanced 7v7 teams from your player pool with smart weightings!

## 🚀 Quick Start

1. **Upload your player data** (CSV or Excel file)
2. **Click "Generate Teams"** 
3. **Share the link** in your WhatsApp group!

## 📊 Player Data Format

Your CSV/Excel file should have these columns:
- **Name**: Player name
- **Age**: Age (big factor in team balance)
- **Position**: GK, DEF, MID, FWD
- **Skill**: 1-10 rating for their position
- **Fitness**: 1-10 fitness level

### Sample Data
```
Name,Age,Position,Skill,Fitness
Alex Thompson,26,GK,8,9
James Rodriguez,28,DEF,7,8
Lucas Silva,26,MID,9,8
Sergio Martinez,23,FWD,9,8
```

## 🏗️ How to Host for FREE

### Option 1: GitHub Pages (Recommended)

1. **Create GitHub account** (free): github.com
2. **Create new repository** called "football-teams"
3. **Upload files**:
   - `index.html`
   - `players_data.csv` (your sample data)
4. **Enable Pages**: Settings > Pages > Source: "Deploy from branch" > main
5. **Your link**: `https://yourusername.github.io/football-teams`

### Option 2: Netlify (Super Easy)

1. **Go to**: netlify.com
2. **Drag & drop** the `index.html` file
3. **Get instant link**: `https://random-name.netlify.app`
4. **Share in WhatsApp group!**

### Option 3: Vercel

1. **Go to**: vercel.com
2. **Import** your files
3. **Deploy** with one click
4. **Get link**: `https://football-teams.vercel.app`

## 💡 Smart Team Generation

The system uses weighted metrics:
- **Age & Fitness**: 40% combined (peak age 24-28)
- **Skill Level**: 60% (1-10 rating for position)
- **Balanced Distribution**: Snake draft ensures fair teams

## 📱 WhatsApp Sharing

Once hosted, share like this:
```
⚽ Generate our weekly teams here:
https://yourusername.github.io/football-teams

Just upload our player Excel file and click generate!
```

## 🔧 Customization

### Easy Changes:
- **Formation**: Currently 1 GK, 2 DEF, 3 MID, 1 FWD
- **Age Weights**: Peak performance ages
- **Team Names**: Currently "Team A" and "Team B"

### Edit the HTML file to customize:
- Line 400+: Change formation numbers
- Line 350+: Adjust age weights
- Line 100+: Change team names/colors

## 📋 Excel Integration

1. **Create/Edit** your `players_data.csv` file
2. **Upload** via the web interface
3. **Generate teams** instantly
4. **Anyone can edit** the Excel and re-upload

## 🎯 Features

✅ **Two balanced teams** (7v7 each)  
✅ **Smart player ratings** (age + fitness + skill)  
✅ **Position-based selection**  
✅ **Mobile-friendly** interface  
✅ **Excel/CSV support**  
✅ **Instant sharing** via WhatsApp  
✅ **No database needed**  
✅ **100% free hosting**  

## 🔄 Weekly Usage

1. **Team manager** updates Excel with any changes
2. **Upload** updated file to web app
3. **Generate** new teams
4. **Share** teams in group chat
5. **Play football!** ⚽

Perfect for weekend leagues, office teams, or friend groups! 