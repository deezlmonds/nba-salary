# 💰 NBA Player Salary Dashboard

A comprehensive web application for visualizing NBA player salary data organized by teams. Features an interactive dashboard with charts, tables, and analytics, powered by a Python web scraper that collects salary data from multiple sources.

## 🎯 Features

### 💸 Salary Data Sources
- **HoopsHype.com**: Most comprehensive salary database
- **Basketball Reference**: Contract and salary information
- **Spotrac**: Detailed contract breakdowns

### 📊 Data Organization
- **By Team**: Complete payroll for each NBA team
- **By Player**: Individual salary and contract details
- **Multi-Year**: Current and future year salary projections
- **Contract Analysis**: Total guaranteed money and contract length

### 📈 Analytics & Insights
- Team payroll summaries and rankings
- Highest paid players league-wide
- Salary distribution analysis
- Contract tier breakdowns ($10M+, $20M+, $30M+, $40M+)

### 📁 Export Formats
- **CSV**: Excel-compatible spreadsheets
- **JSON**: Structured data format
- **Excel**: Native Excel files with formatting

## 🚀 Quick Start

### 🌐 Web Dashboard (Recommended)

**Easiest way to get started:**

1. **Quick Setup & Launch:**
```bash
python run_dashboard.py
```

This script will:
- Check Python version compatibility
- Install all dependencies automatically  
- Verify all required files are present
- Launch the web dashboard
- Open your browser to http://localhost:5000

2. **Manual Setup:**
```bash
# Install dependencies
pip install -r requirements.txt

# Start the web dashboard
python app.py
```

3. **Open your browser and go to:** `http://localhost:5000`

### 📊 Dashboard Features

✅ **Interactive Visualizations:**
- Salary distribution pie charts
- Team payroll bar charts  
- Player salary rankings
- Salary trend analysis

✅ **Data Exploration:**
- Search and filter players
- Team-by-team salary breakdowns
- Salary tier analysis ($10M+, $20M+, etc.)
- Export data to CSV/JSON/Excel

✅ **Real-time Data:**
- Fresh salary data from web scraping
- Automatic data caching
- Refresh data on demand

### 🐍 Python API Usage

```python
from nba_salary_scraper import NBASalaryScraper

# Initialize scraper
scraper = NBASalaryScraper(delay=2.0)

# Get all player salaries
all_salaries = scraper.get_all_player_salaries()
print(f"Found salary data for {len(all_salaries)} players")

# Get team payroll summaries
team_summaries = scraper.get_team_salary_summary()
print("Top 5 team payrolls:")
print(team_summaries[['team_name', 'total_payroll']].head())

# Export data
scraper.export_salary_data(all_salaries, 'nba_salaries.csv')
```

### 📁 Command Line Usage

```bash
# Run the salary scraper directly
python nba_salary_scraper.py

# Run usage examples
python salary_example.py

# Start the web dashboard
python app.py
```

## 📊 Available Methods

### `NBASalaryScraper` Class Methods

#### `get_all_player_salaries(season=None)` → DataFrame
Get comprehensive salary data for all NBA players.

**Returns:** DataFrame with columns:
- `player_name`: Full player name
- `team_abbr`: Team abbreviation (e.g., 'LAL', 'GSW')
- `team_name`: Full team name
- `{year}_salary`: Salary for each contract year
- `total_guaranteed`: Total guaranteed contract value
- `data_source`: Source of the data

#### `get_team_payroll(team_abbr, season=None)` → DataFrame
Get complete payroll information for a specific team.

**Parameters:**
- `team_abbr`: Team abbreviation ('LAL', 'GSW', 'BOS', etc.)
- `season`: Season year (defaults to current)

#### `get_salary_by_team(season=None)` → Dict[str, DataFrame]
Get salary data organized by team.

**Returns:** Dictionary with team abbreviations as keys and player DataFrames as values.

#### `get_team_salary_summary(season=None)` → DataFrame
Get salary summary statistics for all teams.

**Returns:** DataFrame with:
- Total payroll, average salary, median salary
- Highest/lowest paid players per team
- Player count and salary tier breakdowns

#### `get_highest_paid_players(limit=50, season=None)` → DataFrame
Get the highest paid players league-wide.

**Parameters:**
- `limit`: Number of top players to return
- `season`: Season year

#### `export_salary_data(data, filename, format='csv')` → bool
Export salary data to file.

**Parameters:**
- `data`: DataFrame to export
- `filename`: Output filename
- `format`: Export format ('csv', 'json', 'excel')

#### `export_all_team_salaries(season=None, output_dir='nba_salary_data')`
Export salary data for all teams to separate files.

## 📁 File Structure

```
nba-salary-scraper/
├── nba_salary_scraper.py    # Main salary scraper class
├── salary_example.py        # Usage examples
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── nba_salary_data/        # Output directory (created automatically)
    ├── all_nba_salaries_2025.csv
    ├── team_salary_summaries_2025.csv
    ├── top_100_highest_paid_2025.csv
    └── individual_teams/
        ├── LAL_Los_Angeles_Lakers_salaries_2025.csv
        ├── GSW_Golden_State_Warriors_salaries_2025.csv
        └── ...
```

## 💰 Example Data Output

### All Player Salaries
```csv
player_name,team_abbr,team_name,2025_salary,2026_salary,total_guaranteed
Stephen Curry,GSW,Golden State Warriors,59606817,62587158,244387948
Joel Embiid,PHI,Philadelphia 76ers,55224526,57985752,283097362
Nikola Jokic,DEN,Denver Nuggets,55224526,59033114,177099342
```

### Team Salary Summary
```csv
team_name,total_payroll,average_salary,highest_paid_player,num_players
Golden State Warriors,187543210,12502881,Stephen Curry,15
Philadelphia 76ers,178932156,11928810,Joel Embiid,15
Denver Nuggets,176234891,11748993,Nikola Jokic,15
```

### Highest Paid Players
```csv
player_name,team_abbr,team_name,2025_salary,total_guaranteed
Stephen Curry,GSW,Golden State Warriors,59606817,244387948
Joel Embiid,PHI,Philadelphia 76ers,55224526,283097362
Nikola Jokic,DEN,Denver Nuggets,55224526,177099342
```

## 🏀 NBA Team Abbreviations

| Abbr | Team Name | Abbr | Team Name |
|------|-----------|------|-----------|
| ATL | Atlanta Hawks | MIA | Miami Heat |
| BOS | Boston Celtics | MIL | Milwaukee Bucks |
| BRK | Brooklyn Nets | MIN | Minnesota Timberwolves |
| CHA | Charlotte Hornets | NOP | New Orleans Pelicans |
| CHI | Chicago Bulls | NYK | New York Knicks |
| CLE | Cleveland Cavaliers | OKC | Oklahoma City Thunder |
| DAL | Dallas Mavericks | ORL | Orlando Magic |
| DEN | Denver Nuggets | PHI | Philadelphia 76ers |
| DET | Detroit Pistons | PHX | Phoenix Suns |
| GSW | Golden State Warriors | POR | Portland Trail Blazers |
| HOU | Houston Rockets | SAC | Sacramento Kings |
| IND | Indiana Pacers | SAS | San Antonio Spurs |
| LAC | LA Clippers | TOR | Toronto Raptors |
| LAL | Los Angeles Lakers | UTA | Utah Jazz |
| MEM | Memphis Grizzlies | WAS | Washington Wizards |

## ⚙️ Configuration

### Rate Limiting
```python
# Adjust delay between requests (in seconds)
scraper = NBASalaryScraper(delay=3.0)  # 3 second delay
```

### Season Selection
```python
# Get salary data for specific season
salaries_2024 = scraper.get_all_player_salaries('2024')
salaries_2025 = scraper.get_all_player_salaries('2025')
```

## 🔍 Advanced Usage Examples

### Team Payroll Analysis
```python
# Compare team payrolls
team_summaries = scraper.get_team_salary_summary()
highest_payroll = team_summaries.iloc[0]
print(f"Highest payroll: {highest_payroll['team_name']} - ${highest_payroll['total_payroll']:,.0f}")

# Find teams with most players over $20M
big_contracts = team_summaries.sort_values('players_over_20m', ascending=False)
print("Teams with most $20M+ players:")
print(big_contracts[['team_name', 'players_over_20m']].head())
```

### Player Salary Analysis
```python
# Find all players earning over $40M
all_salaries = scraper.get_all_player_salaries()
supermaxes = all_salaries[all_salaries['2025_salary'] > 40_000_000]
print(f"Players earning over $40M: {len(supermaxes)}")

# Average salary by team
team_avg_salaries = all_salaries.groupby('team_name')['2025_salary'].mean().sort_values(ascending=False)
print("Teams by average salary:")
print(team_avg_salaries.head())
```

### Export Team-Specific Data
```python
# Export data for specific teams
teams_of_interest = ['LAL', 'GSW', 'BOS', 'MIA']
for team in teams_of_interest:
    team_data = scraper.get_team_payroll(team)
    scraper.export_salary_data(team_data, f'{team}_salaries.csv')
```

## ⚠️ Important Notes

### Rate Limiting & Ethics
- **Built-in delays**: 2-second default delay between requests
- **Respect robots.txt**: Always check website policies
- **Don't overload servers**: Use reasonable delays
- **Cache results**: Store data locally to minimize requests

### Data Accuracy
- Salary data is scraped from public websites
- Contract details may change frequently during season
- Always verify critical information from official sources
- Some contract details (incentives, options) may not be captured

### Legal Considerations
- **Personal use only**: This scraper is for educational purposes
- **Respect terms of service**: Don't violate website policies  
- **No commercial use**: Don't use scraped data commercially without permission
- **Official APIs**: Consider using official NBA APIs when available

## 🛠️ Troubleshooting

### Common Issues

**1. Empty DataFrames**
```python
# Check if data was scraped successfully
if all_salaries.empty:
    print("No salary data found - check website structure or increase delay")
```

**2. Rate Limiting**
```python
# Increase delay if getting blocked
scraper = NBASalaryScraper(delay=5.0)  # 5 second delay
```

**3. Team Not Found**
```python
# Check valid team abbreviations
print(scraper.team_mapping.keys())
```

**4. Export Errors**
```python
# Ensure output directory exists
import os
os.makedirs('output', exist_ok=True)
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Sample Analysis Scripts

### Payroll Inequality Analysis
```python
team_summaries = scraper.get_team_salary_summary()
payroll_range = team_summaries['total_payroll'].max() - team_summaries['total_payroll'].min()
print(f"Payroll inequality: ${payroll_range:,.0f} difference between highest and lowest")
```

### Contract Length Analysis
```python
all_salaries = scraper.get_all_player_salaries()
# Calculate average contract length based on guaranteed money vs annual salary
all_salaries['est_contract_years'] = all_salaries['total_guaranteed'] / all_salaries['2025_salary']
avg_contract_length = all_salaries['est_contract_years'].mean()
print(f"Average estimated contract length: {avg_contract_length:.1f} years")
```

## 🤝 Contributing

Potential improvements:
- Add more salary data sources
- Include salary cap analysis
- Add luxury tax calculations
- Implement historical salary trends
- Add contract option tracking
- Include rookie scale contracts

---

**Happy salary analysis! 💰🏀📊**