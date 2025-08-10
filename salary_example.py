#!/usr/bin/env python3
"""
NBA Salary Scraper - Example Usage
==================================

This file demonstrates how to use the NBA salary scraper for collecting 
player salary data organized by teams.
"""

from nba_salary_scraper import NBASalaryScraper
import pandas as pd
import os

def main():
    """Example usage of the NBA salary scraper"""
    
    # Initialize the scraper
    scraper = NBASalaryScraper(delay=2.0)  # 2 second delay between requests
    
    print("💰 NBA Salary Scraper - Example Usage")
    print("=" * 60)
    
    # Create output directory for examples
    os.makedirs('salary_examples', exist_ok=True)
    
    # Example 1: Get all player salaries
    print("\n💸 Example 1: Getting all NBA player salaries")
    all_salaries = scraper.get_all_player_salaries()
    if not all_salaries.empty:
        print(f"Found salary data for {len(all_salaries)} players")
        print("\nTop 10 highest paid players:")
        salary_col = f'{scraper.current_season}_salary'
        top_10 = all_salaries.nlargest(10, salary_col)
        for _, player in top_10.iterrows():
            print(f"  {player['player_name']:25} ({player['team_abbr']}) - ${player[salary_col]:>12,.0f}")
        
        # Export all salaries
        scraper.export_salary_data(all_salaries, 'salary_examples/all_player_salaries.csv')
        print("✅ All player salaries exported to salary_examples/all_player_salaries.csv")
    
    # Example 2: Get team salary summaries
    print("\n🏀 Example 2: Team salary summaries")
    team_summaries = scraper.get_team_salary_summary()
    if not team_summaries.empty:
        print("Top 10 team payrolls:")
        print(f"{'Team':<25} {'Total Payroll':<15} {'Avg Salary':<15} {'Players':<8}")
        print("-" * 70)
        for _, team in team_summaries.head(10).iterrows():
            print(f"{team['team_name']:<25} ${team['total_payroll']:<14,.0f} ${team['average_salary']:<14,.0f} {team['num_players']:<8}")
        
        # Export team summaries
        scraper.export_salary_data(team_summaries, 'salary_examples/team_salary_summaries.csv')
        print("✅ Team summaries exported to salary_examples/team_salary_summaries.csv")
    
    # Example 3: Get specific team payroll (Lakers)
    print("\n🏆 Example 3: Los Angeles Lakers payroll breakdown")
    lakers_payroll = scraper.get_team_payroll('LAL')
    if not lakers_payroll.empty:
        print(f"Lakers have {len(lakers_payroll)} players on payroll:")
        salary_col = f'{scraper.current_season}_salary'
        lakers_sorted = lakers_payroll.sort_values(salary_col, ascending=False)
        
        total_payroll = lakers_sorted[salary_col].sum()
        print(f"Total Lakers payroll: ${total_payroll:,.0f}")
        print("\nLakers roster by salary:")
        for _, player in lakers_sorted.iterrows():
            print(f"  {player['player_name']:25} - ${player[salary_col]:>12,.0f}")
        
        scraper.export_salary_data(lakers_payroll, 'salary_examples/lakers_payroll.csv')
        print("✅ Lakers payroll exported to salary_examples/lakers_payroll.csv")
    
    # Example 4: Get salary data organized by all teams
    print("\n🏀 Example 4: Salary data organized by teams")
    teams_salary_data = scraper.get_salary_by_team()
    if teams_salary_data:
        print(f"Organized salary data for {len(teams_salary_data)} teams")
        
        # Show sample data for a few teams
        sample_teams = ['GSW', 'BOS', 'MIA']  # Warriors, Celtics, Heat
        
        for team_abbr in sample_teams:
            if team_abbr in teams_salary_data:
                team_data = teams_salary_data[team_abbr]
                team_name = scraper.team_mapping.get(team_abbr, 'Unknown')
                salary_col = f'{scraper.current_season}_salary'
                total_payroll = team_data[salary_col].sum()
                
                print(f"\n{team_name} ({team_abbr}):")
                print(f"  Total payroll: ${total_payroll:,.0f}")
                print(f"  Number of players: {len(team_data)}")
                print("  Top 3 paid players:")
                for _, player in team_data.head(3).iterrows():
                    print(f"    {player['player_name']:20} - ${player[salary_col]:>10,.0f}")
    
    # Example 5: Get highest paid players league-wide
    print("\n💎 Example 5: Top 15 highest paid players in the NBA")
    top_players = scraper.get_highest_paid_players(15)
    if not top_players.empty:
        print(f"{'Rank':<4} {'Player':<25} {'Team':<4} {'Salary':<15} {'Total Guaranteed':<15}")
        print("-" * 70)
        salary_col = f'{scraper.current_season}_salary'
        for i, (_, player) in enumerate(top_players.iterrows(), 1):
            print(f"{i:<4} {player['player_name']:<25} {player['team_abbr']:<4} ${player[salary_col]:<14,.0f} ${player['total_guaranteed']:<14,.0f}")
        
        scraper.export_salary_data(top_players, 'salary_examples/top_15_highest_paid.csv')
        print("✅ Top 15 players exported to salary_examples/top_15_highest_paid.csv")
    
    # Example 6: Export all team salary data to separate files
    print("\n📁 Example 6: Exporting individual team salary files")
    scraper.export_all_team_salaries(output_dir='salary_examples/team_files')
    print("✅ Individual team salary files exported to salary_examples/team_files/")
    
    # Example 7: Salary analysis
    print("\n📊 Example 7: Salary analysis")
    if not all_salaries.empty:
        salary_col = f'{scraper.current_season}_salary'
        
        # Basic statistics
        total_league_payroll = all_salaries[salary_col].sum()
        avg_salary = all_salaries[salary_col].mean()
        median_salary = all_salaries[salary_col].median()
        max_salary = all_salaries[salary_col].max()
        min_salary = all_salaries[salary_col].min()
        
        print(f"League-wide salary statistics:")
        print(f"  Total NBA payroll: ${total_league_payroll:,.0f}")
        print(f"  Average salary: ${avg_salary:,.0f}")
        print(f"  Median salary: ${median_salary:,.0f}")
        print(f"  Highest salary: ${max_salary:,.0f}")
        print(f"  Lowest salary: ${min_salary:,.0f}")
        
        # Salary tiers
        over_40m = len(all_salaries[all_salaries[salary_col] > 40_000_000])
        over_30m = len(all_salaries[all_salaries[salary_col] > 30_000_000])
        over_20m = len(all_salaries[all_salaries[salary_col] > 20_000_000])
        over_10m = len(all_salaries[all_salaries[salary_col] > 10_000_000])
        
        print(f"\nSalary tier breakdown:")
        print(f"  Players earning over $40M: {over_40m}")
        print(f"  Players earning over $30M: {over_30m}")
        print(f"  Players earning over $20M: {over_20m}")
        print(f"  Players earning over $10M: {over_10m}")
    
    print(f"\n✅ Example usage completed!")
    print("📁 Check the 'salary_examples' folder for all exported files.")
    print("\n🔍 Files generated:")
    print("   - all_player_salaries.csv (complete salary database)")
    print("   - team_salary_summaries.csv (team payroll summaries)")
    print("   - lakers_payroll.csv (Lakers team example)")
    print("   - top_15_highest_paid.csv (highest paid players)")
    print("   - team_files/ (individual team salary files)")

if __name__ == "__main__":
    main()