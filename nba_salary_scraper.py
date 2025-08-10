#!/usr/bin/env python3
"""
NBA Player Salary Web Scraper
=============================

A comprehensive web scraper for NBA player salary data organized by teams.

Data sources:
- HoopsHype.com salary database
- Basketball Reference salary pages
- Spotrac NBA salary data

Features:
- Complete salary data for all NBA players
- Data organized by teams
- Multi-year contract information
- Export to CSV, JSON, Excel formats
- Team payroll summaries

Author: NBA Salary Scraper
Date: 2024
"""

import requests
import pandas as pd
import json
import time
import logging
from datetime import datetime, date
from typing import Dict, List, Optional, Union
import urllib.parse
from bs4 import BeautifulSoup
import os
import re

class NBASalaryScraper:
    """NBA Player Salary Scraper - Focus on salary data organized by teams"""
    
    def __init__(self, delay: float = 2.0):
        """
        Initialize the NBA salary scraper
        
        Args:
            delay: Delay between requests in seconds (respect rate limits)
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Base URLs for salary data sources
        self.hoopshype_url = "https://hoopshype.com"
        self.basketball_ref_url = "https://www.basketball-reference.com"
        self.spotrac_url = "https://www.spotrac.com"
        
        # Current season
        self.current_season = self._get_current_season()
        
        # NBA team abbreviations mapping
        self.team_mapping = {
            'ATL': 'Atlanta Hawks', 'BOS': 'Boston Celtics', 'BRK': 'Brooklyn Nets', 'CHA': 'Charlotte Hornets',
            'CHI': 'Chicago Bulls', 'CLE': 'Cleveland Cavaliers', 'DAL': 'Dallas Mavericks', 'DEN': 'Denver Nuggets',
            'DET': 'Detroit Pistons', 'GSW': 'Golden State Warriors', 'HOU': 'Houston Rockets', 'IND': 'Indiana Pacers',
            'LAC': 'LA Clippers', 'LAL': 'Los Angeles Lakers', 'MEM': 'Memphis Grizzlies', 'MIA': 'Miami Heat',
            'MIL': 'Milwaukee Bucks', 'MIN': 'Minnesota Timberwolves', 'NOP': 'New Orleans Pelicans', 'NYK': 'New York Knicks',
            'OKC': 'Oklahoma City Thunder', 'ORL': 'Orlando Magic', 'PHI': 'Philadelphia 76ers', 'PHX': 'Phoenix Suns',
            'POR': 'Portland Trail Blazers', 'SAC': 'Sacramento Kings', 'SAS': 'San Antonio Spurs', 'TOR': 'Toronto Raptors',
            'UTA': 'Utah Jazz', 'WAS': 'Washington Wizards'
        }
        
    def _get_current_season(self) -> str:
        """Get current NBA season year"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # NBA season runs from October to June
        if current_month >= 10:
            return str(current_year + 1)
        else:
            return str(current_year)
    
    def _make_request(self, url: str, params: Dict = None) -> Optional[requests.Response]:
        """
        Make HTTP request with error handling and rate limiting
        
        Args:
            url: URL to request
            params: Optional query parameters
            
        Returns:
            Response object or None if failed
        """
        try:
            time.sleep(self.delay)  # Rate limiting
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed for {url}: {e}")
            return None
    
    def _clean_salary(self, salary_str: str) -> float:
        """
        Clean and convert salary string to float
        
        Args:
            salary_str: Salary string (e.g., "$59,606,817", "$59.6M")
            
        Returns:
            Float value of salary
        """
        if not salary_str or salary_str.strip() in ['-', 'N/A', '']:
            return 0.0
        
        # Remove currency symbols and commas
        cleaned = re.sub(r'[,$]', '', salary_str.strip())
        
        # Handle millions notation (e.g., "59.6M")
        if 'M' in cleaned.upper():
            cleaned = cleaned.upper().replace('M', '')
            try:
                return float(cleaned) * 1_000_000
            except ValueError:
                return 0.0
        
        # Handle thousands notation (e.g., "500K")
        if 'K' in cleaned.upper():
            cleaned = cleaned.upper().replace('K', '')
            try:
                return float(cleaned) * 1_000
            except ValueError:
                return 0.0
        
        try:
            return float(cleaned)
        except ValueError:
            return 0.0
    
    def get_all_player_salaries(self, season: str = None) -> pd.DataFrame:
        """
        Get salary data for all NBA players
        
        Args:
            season: Season year (e.g., '2025'). Defaults to current season
            
        Returns:
            DataFrame with all player salary information
        """
        if not season:
            season = self.current_season
            
        self.logger.info(f"Fetching all player salaries for {season} season...")
        
        # Try HoopsHype first (most comprehensive salary data)
        salary_data = self._scrape_hoopshype_salaries(season)
        
        if salary_data.empty:
            # Fallback to Basketball Reference
            salary_data = self._scrape_basketball_ref_salaries(season)
        
        return salary_data
    
    def _scrape_hoopshype_salaries(self, season: str) -> pd.DataFrame:
        """Scrape salary data from HoopsHype"""
        url = f"{self.hoopshype_url}/salaries/players/"
        response = self._make_request(url)
        
        if not response:
            return pd.DataFrame()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        salary_data = []
        
        # Find the salary table
        table = soup.find('table') or soup.find('div', class_='table-responsive')
        
        if table:
            rows = table.find_all('tr')[1:]  # Skip header
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:
                    # Extract player name and team
                    player_cell = cells[0] if cells else None
                    if player_cell:
                        player_link = player_cell.find('a')
                        if player_link:
                            player_name = player_link.text.strip()
                            
                            # Extract team from image or text
                            team_img = player_cell.find('img')
                            team_abbr = 'UNK'
                            if team_img and 'alt' in team_img.attrs:
                                team_abbr = team_img['alt'][:3].upper()
                            
                            # Extract salary data
                            current_salary = self._clean_salary(cells[1].text.strip()) if len(cells) > 1 else 0
                            next_year_salary = self._clean_salary(cells[2].text.strip()) if len(cells) > 2 else 0
                            year_3_salary = self._clean_salary(cells[3].text.strip()) if len(cells) > 3 else 0
                            year_4_salary = self._clean_salary(cells[4].text.strip()) if len(cells) > 4 else 0
                            
                            salary_data.append({
                                'player_name': player_name,
                                'team_abbr': team_abbr,
                                'team_name': self.team_mapping.get(team_abbr, 'Unknown'),
                                f'{season}_salary': current_salary,
                                f'{int(season)+1}_salary': next_year_salary,
                                f'{int(season)+2}_salary': year_3_salary,
                                f'{int(season)+3}_salary': year_4_salary,
                                'total_guaranteed': current_salary + next_year_salary + year_3_salary + year_4_salary,
                                'data_source': 'HoopsHype'
                            })
        
        return pd.DataFrame(salary_data)
    
    def _scrape_basketball_ref_salaries(self, season: str) -> pd.DataFrame:
        """Scrape salary data from Basketball Reference"""
        url = f"{self.basketball_ref_url}/contracts/players.html"
        response = self._make_request(url)
        
        if not response:
            return pd.DataFrame()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        salary_data = []
        
        # Find the contracts table
        table = soup.find('table', {'id': 'contracts'})
        
        if table:
            rows = table.find('tbody').find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 4:
                    # Extract player info
                    player_cell = cells[1] if len(cells) > 1 else None
                    team_cell = cells[2] if len(cells) > 2 else None
                    
                    if player_cell and team_cell:
                        player_link = player_cell.find('a')
                        player_name = player_link.text.strip() if player_link else player_cell.text.strip()
                        
                        team_link = team_cell.find('a')
                        team_abbr = team_link.text.strip() if team_link else team_cell.text.strip()
                        
                        # Extract salary columns
                        current_salary = self._clean_salary(cells[3].text.strip()) if len(cells) > 3 else 0
                        next_year_salary = self._clean_salary(cells[4].text.strip()) if len(cells) > 4 else 0
                        year_3_salary = self._clean_salary(cells[5].text.strip()) if len(cells) > 5 else 0
                        year_4_salary = self._clean_salary(cells[6].text.strip()) if len(cells) > 6 else 0
                        guaranteed = self._clean_salary(cells[-1].text.strip()) if len(cells) > 7 else 0
                        
                        salary_data.append({
                            'player_name': player_name,
                            'team_abbr': team_abbr,
                            'team_name': self.team_mapping.get(team_abbr, 'Unknown'),
                            f'{season}_salary': current_salary,
                            f'{int(season)+1}_salary': next_year_salary,
                            f'{int(season)+2}_salary': year_3_salary,
                            f'{int(season)+3}_salary': year_4_salary,
                            'total_guaranteed': guaranteed,
                            'data_source': 'Basketball Reference'
                        })
        
        return pd.DataFrame(salary_data)
    
    def get_team_payroll(self, team_abbr: str = None, season: str = None) -> pd.DataFrame:
        """
        Get payroll information for specific team or all teams
        
        Args:
            team_abbr: Team abbreviation (e.g., 'LAL'). If None, returns all teams
            season: Season year
            
        Returns:
            DataFrame with team payroll data
        """
        if not season:
            season = self.current_season
            
        # Get all player salaries
        all_salaries = self.get_all_player_salaries(season)
        
        if all_salaries.empty:
            return pd.DataFrame()
        
        # Filter by team if specified
        if team_abbr:
            team_salaries = all_salaries[all_salaries['team_abbr'] == team_abbr.upper()]
            self.logger.info(f"Fetching payroll for {team_abbr} ({season} season)...")
        else:
            team_salaries = all_salaries
            self.logger.info(f"Fetching payroll for all teams ({season} season)...")
        
        return team_salaries
    
    def get_salary_by_team(self, season: str = None) -> Dict[str, pd.DataFrame]:
        """
        Get salary data organized by team
        
        Args:
            season: Season year
            
        Returns:
            Dictionary with team abbreviation as key and DataFrame of players as value
        """
        if not season:
            season = self.current_season
            
        self.logger.info(f"Organizing salary data by teams for {season} season...")
        
        all_salaries = self.get_all_player_salaries(season)
        
        if all_salaries.empty:
            return {}
        
        # Group by team
        teams_dict = {}
        for team_abbr in all_salaries['team_abbr'].unique():
            team_data = all_salaries[all_salaries['team_abbr'] == team_abbr].copy()
            team_data = team_data.sort_values(f'{season}_salary', ascending=False)
            teams_dict[team_abbr] = team_data
        
        return teams_dict
    
    def get_team_salary_summary(self, season: str = None) -> pd.DataFrame:
        """
        Get salary summary for all teams
        
        Args:
            season: Season year
            
        Returns:
            DataFrame with team salary summaries
        """
        if not season:
            season = self.current_season
            
        self.logger.info(f"Generating team salary summaries for {season} season...")
        
        all_salaries = self.get_all_player_salaries(season)
        
        if all_salaries.empty:
            return pd.DataFrame()
        
        # Calculate team summaries
        team_summaries = []
        salary_col = f'{season}_salary'
        
        for team_abbr, team_data in all_salaries.groupby('team_abbr'):
            team_name = self.team_mapping.get(team_abbr, 'Unknown')
            
            summary = {
                'team_abbr': team_abbr,
                'team_name': team_name,
                'total_payroll': team_data[salary_col].sum(),
                'average_salary': team_data[salary_col].mean(),
                'median_salary': team_data[salary_col].median(),
                'highest_paid_player': team_data.loc[team_data[salary_col].idxmax(), 'player_name'] if not team_data.empty else 'N/A',
                'highest_salary': team_data[salary_col].max(),
                'lowest_paid_player': team_data.loc[team_data[salary_col].idxmin(), 'player_name'] if not team_data.empty else 'N/A',
                'lowest_salary': team_data[salary_col].min(),
                'num_players': len(team_data),
                'players_over_10m': len(team_data[team_data[salary_col] > 10_000_000]),
                'players_over_20m': len(team_data[team_data[salary_col] > 20_000_000]),
                'players_over_30m': len(team_data[team_data[salary_col] > 30_000_000])
            }
            team_summaries.append(summary)
        
        summary_df = pd.DataFrame(team_summaries)
        return summary_df.sort_values('total_payroll', ascending=False)
    
    def get_highest_paid_players(self, limit: int = 50, season: str = None) -> pd.DataFrame:
        """
        Get highest paid players across the league
        
        Args:
            limit: Number of top players to return
            season: Season year
            
        Returns:
            DataFrame with highest paid players
        """
        if not season:
            season = self.current_season
            
        self.logger.info(f"Fetching top {limit} highest paid players for {season} season...")
        
        all_salaries = self.get_all_player_salaries(season)
        
        if all_salaries.empty:
            return pd.DataFrame()
        
        salary_col = f'{season}_salary'
        top_players = all_salaries.nlargest(limit, salary_col)
        
        return top_players[['player_name', 'team_abbr', 'team_name', salary_col, 'total_guaranteed']]
    
    def export_salary_data(self, data: pd.DataFrame, filename: str, format: str = 'csv') -> bool:
        """
        Export salary data to file
        
        Args:
            data: DataFrame to export
            filename: Output filename
            format: Export format ('csv', 'json', 'excel')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if format.lower() == 'csv':
                data.to_csv(filename, index=False)
            elif format.lower() == 'json':
                data.to_json(filename, orient='records', indent=2)
            elif format.lower() == 'excel':
                data.to_excel(filename, index=False)
            else:
                self.logger.error(f"Unsupported format: {format}")
                return False
            
            self.logger.info(f"Salary data exported to {filename}")
            return True
        except Exception as e:
            self.logger.error(f"Export failed: {e}")
            return False
    
    def export_all_team_salaries(self, season: str = None, output_dir: str = 'nba_salary_data'):
        """
        Export salary data for all teams to separate files
        
        Args:
            season: Season year
            output_dir: Output directory
        """
        if not season:
            season = self.current_season
            
        self.logger.info(f"Exporting salary data for all teams ({season} season)...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Get all salary data organized by team
        teams_salary_data = self.get_salary_by_team(season)
        
        # Export individual team files
        for team_abbr, team_data in teams_salary_data.items():
            team_name = self.team_mapping.get(team_abbr, 'Unknown').replace(' ', '_')
            filename = f"{output_dir}/{team_abbr}_{team_name}_salaries_{season}.csv"
            self.export_salary_data(team_data, filename, 'csv')
        
        # Export combined data
        all_salaries = self.get_all_player_salaries(season)
        if not all_salaries.empty:
            self.export_salary_data(all_salaries, f"{output_dir}/all_nba_salaries_{season}.csv", 'csv')
        
        # Export team summaries
        team_summaries = self.get_team_salary_summary(season)
        if not team_summaries.empty:
            self.export_salary_data(team_summaries, f"{output_dir}/team_salary_summaries_{season}.csv", 'csv')
        
        # Export top paid players
        top_players = self.get_highest_paid_players(100, season)
        if not top_players.empty:
            self.export_salary_data(top_players, f"{output_dir}/top_100_highest_paid_{season}.csv", 'csv')
        
        self.logger.info(f"All salary data exported to {output_dir}/ directory")

def main():
    """Main function demonstrating the salary scraper usage"""
    print("💰 NBA Player Salary Web Scraper")
    print("=" * 50)
    
    # Initialize scraper
    scraper = NBASalaryScraper(delay=2.0)  # 2 second delay between requests
    
    # Create output directory
    output_dir = 'nba_salary_data'
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. Get all player salaries
        print("\n1. Fetching all NBA player salaries...")
        all_salaries = scraper.get_all_player_salaries()
        if not all_salaries.empty:
            print(f"   Found salary data for {len(all_salaries)} players")
            scraper.export_salary_data(all_salaries, f'{output_dir}/all_player_salaries.csv')
            print("   Sample data:")
            print(all_salaries[['player_name', 'team_abbr', f'{scraper.current_season}_salary']].head())
        
        # 2. Get team salary summaries
        print("\n2. Generating team salary summaries...")
        team_summaries = scraper.get_team_salary_summary()
        if not team_summaries.empty:
            print(f"   Generated summaries for {len(team_summaries)} teams")
            scraper.export_salary_data(team_summaries, f'{output_dir}/team_salary_summaries.csv')
            print("   Top 5 team payrolls:")
            print(team_summaries[['team_name', 'total_payroll', 'num_players']].head())
        
        # 3. Get highest paid players
        print("\n3. Finding highest paid players...")
        top_players = scraper.get_highest_paid_players(20)
        if not top_players.empty:
            print(f"   Top 20 highest paid players:")
            scraper.export_salary_data(top_players, f'{output_dir}/top_20_highest_paid.csv')
            for _, player in top_players.head(10).iterrows():
                salary = player[f'{scraper.current_season}_salary']
                print(f"   {player['player_name']} ({player['team_abbr']}) - ${salary:,.0f}")
        
        # 4. Get salary data organized by teams
        print("\n4. Organizing salary data by teams...")
        teams_salary_data = scraper.get_salary_by_team()
        if teams_salary_data:
            print(f"   Organized data for {len(teams_salary_data)} teams")
            
            # Show sample team data (Lakers)
            if 'LAL' in teams_salary_data:
                lakers_data = teams_salary_data['LAL']
                print(f"   Los Angeles Lakers roster ({len(lakers_data)} players):")
                for _, player in lakers_data.head(5).iterrows():
                    salary = player[f'{scraper.current_season}_salary']
                    print(f"     {player['player_name']} - ${salary:,.0f}")
        
        # 5. Export all team data to separate files
        print("\n5. Exporting individual team salary files...")
        scraper.export_all_team_salaries(output_dir=output_dir)
        
        print(f"\n✅ Salary scraping completed!")
        print(f"📁 Check the '{output_dir}' folder for all exported files:")
        print(f"   - Individual team salary files")
        print(f"   - Combined salary database")
        print(f"   - Team payroll summaries")
        print(f"   - Top paid players list")
        
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during scraping: {e}")

if __name__ == "__main__":
    main()