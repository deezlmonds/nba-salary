#!/usr/bin/env python3
"""
NBA Salary Dashboard - Flask Backend
===================================

Flask web application that serves the NBA salary dashboard and provides
API endpoints for the salary data scraped from various sources.
"""

from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import os
import logging
from datetime import datetime
import pandas as pd

# Import our NBA salary scraper
from nba_salary_scraper import NBASalaryScraper

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
salary_scraper = None
cached_data = {}
last_update = None

def initialize_scraper():
    """Initialize the NBA salary scraper"""
    global salary_scraper
    try:
        salary_scraper = NBASalaryScraper(delay=2.0)
        logger.info("NBA salary scraper initialized successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to initialize scraper: {e}")
        return False

def load_salary_data(season='2025', force_refresh=False):
    """Load salary data from scraper or cache"""
    global cached_data, last_update
    
    cache_key = f"salary_data_{season}"
    
    # Check if we have cached data and it's recent (less than 1 hour old)
    if not force_refresh and cache_key in cached_data and last_update:
        time_diff = datetime.now() - last_update
        if time_diff.total_seconds() < 3600:  # 1 hour
            logger.info(f"Using cached salary data for season {season}")
            return cached_data[cache_key]
    
    # Load fresh data from scraper
    logger.info(f"Loading fresh salary data for season {season}")
    
    if not salary_scraper:
        if not initialize_scraper():
            return None
    
    try:
        # Get all player salaries
        all_salaries = salary_scraper.get_all_player_salaries(season)
        
        # Get team summaries
        team_summaries = salary_scraper.get_team_salary_summary(season)
        
        # Get top paid players
        top_players = salary_scraper.get_highest_paid_players(100, season)
        
        # Prepare data for frontend
        data = {
            'players': all_salaries.to_dict('records') if not all_salaries.empty else [],
            'team_summaries': team_summaries.to_dict('records') if not team_summaries.empty else [],
            'top_players': top_players.to_dict('records') if not top_players.empty else [],
            'season': season,
            'last_updated': datetime.now().isoformat()
        }
        
        # Cache the data
        cached_data[cache_key] = data
        last_update = datetime.now()
        
        logger.info(f"Successfully loaded salary data: {len(data['players'])} players, {len(data['team_summaries'])} teams")
        return data
        
    except Exception as e:
        logger.error(f"Error loading salary data: {e}")
        return None

# Routes

@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS, etc.)"""
    return send_from_directory('.', filename)

@app.route('/api/salary-data')
def get_salary_data():
    """API endpoint to get all salary data"""
    season = request.args.get('season', '2025')
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    try:
        data = load_salary_data(season, force_refresh)
        
        if data is None:
            return jsonify({
                'error': 'Failed to load salary data',
                'message': 'Unable to scrape salary data from sources'
            }), 500
        
        return jsonify(data)
        
    except Exception as e:
        logger.error(f"Error in salary data API: {e}")
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/team-payroll/<team_abbr>')
def get_team_payroll(team_abbr):
    """API endpoint to get specific team payroll"""
    season = request.args.get('season', '2025')
    
    try:
        if not salary_scraper:
            if not initialize_scraper():
                return jsonify({'error': 'Scraper initialization failed'}), 500
        
        team_payroll = salary_scraper.get_team_payroll(team_abbr.upper(), season)
        
        if team_payroll.empty:
            return jsonify({
                'error': 'Team not found',
                'message': f'No payroll data found for team {team_abbr}'
            }), 404
        
        return jsonify({
            'team': team_abbr.upper(),
            'season': season,
            'players': team_payroll.to_dict('records'),
            'total_payroll': team_payroll[f'{season}_salary'].sum(),
            'player_count': len(team_payroll)
        })
        
    except Exception as e:
        logger.error(f"Error getting team payroll for {team_abbr}: {e}")
        return jsonify({
            'error': 'Failed to get team payroll',
            'message': str(e)
        }), 500

@app.route('/api/player-search')
def search_players():
    """API endpoint to search for players"""
    query = request.args.get('q', '').strip()
    season = request.args.get('season', '2025')
    limit = int(request.args.get('limit', 20))
    
    if not query:
        return jsonify({'error': 'Search query required'}), 400
    
    try:
        data = load_salary_data(season)
        if not data or not data['players']:
            return jsonify({'error': 'No salary data available'}), 500
        
        # Filter players by search query
        matching_players = []
        query_lower = query.lower()
        
        for player in data['players']:
            player_name = player.get('player_name', '').lower()
            team_name = player.get('team_name', '').lower()
            team_abbr = player.get('team_abbr', '').lower()
            
            if (query_lower in player_name or 
                query_lower in team_name or 
                query_lower in team_abbr):
                matching_players.append(player)
        
        # Sort by salary (highest first) and limit results
        matching_players.sort(key=lambda x: x.get(f'{season}_salary', 0), reverse=True)
        matching_players = matching_players[:limit]
        
        return jsonify({
            'query': query,
            'results': matching_players,
            'count': len(matching_players)
        })
        
    except Exception as e:
        logger.error(f"Error searching players: {e}")
        return jsonify({
            'error': 'Search failed',
            'message': str(e)
        }), 500

@app.route('/api/salary-distribution')
def get_salary_distribution():
    """API endpoint to get salary distribution data"""
    season = request.args.get('season', '2025')
    
    try:
        data = load_salary_data(season)
        if not data or not data['players']:
            return jsonify({'error': 'No salary data available'}), 500
        
        # Calculate salary distribution
        salaries = [player.get(f'{season}_salary', 0) for player in data['players']]
        
        ranges = [
            {'label': 'Under $5M', 'min': 0, 'max': 5000000},
            {'label': '$5M - $10M', 'min': 5000000, 'max': 10000000},
            {'label': '$10M - $20M', 'min': 10000000, 'max': 20000000},
            {'label': '$20M - $30M', 'min': 20000000, 'max': 30000000},
            {'label': '$30M - $40M', 'min': 30000000, 'max': 40000000},
            {'label': 'Over $40M', 'min': 40000000, 'max': float('inf')}
        ]
        
        distribution = []
        for range_info in ranges:
            count = len([s for s in salaries if range_info['min'] <= s < range_info['max']])
            percentage = (count / len(salaries)) * 100 if salaries else 0
            
            distribution.append({
                'label': range_info['label'],
                'count': count,
                'percentage': round(percentage, 1)
            })
        
        return jsonify({
            'distribution': distribution,
            'total_players': len(salaries),
            'season': season
        })
        
    except Exception as e:
        logger.error(f"Error calculating salary distribution: {e}")
        return jsonify({
            'error': 'Failed to calculate distribution',
            'message': str(e)
        }), 500

@app.route('/api/export-data')
def export_data():
    """API endpoint to export salary data"""
    season = request.args.get('season', '2025')
    format_type = request.args.get('format', 'csv').lower()
    data_type = request.args.get('type', 'all')  # all, players, teams
    
    try:
        if not salary_scraper:
            if not initialize_scraper():
                return jsonify({'error': 'Scraper initialization failed'}), 500
        
        # Create export directory
        export_dir = 'exports'
        os.makedirs(export_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if data_type == 'players':
            # Export all players
            all_salaries = salary_scraper.get_all_player_salaries(season)
            filename = f'{export_dir}/nba_players_{season}_{timestamp}.{format_type}'
            
        elif data_type == 'teams':
            # Export team summaries
            team_summaries = salary_scraper.get_team_salary_summary(season)
            filename = f'{export_dir}/nba_teams_{season}_{timestamp}.{format_type}'
            all_salaries = team_summaries
            
        else:
            # Export all data to separate files
            salary_scraper.export_all_team_salaries(season, export_dir)
            return jsonify({
                'success': True,
                'message': 'All team salary data exported successfully',
                'directory': export_dir
            })
        
        # Export single file
        success = salary_scraper.export_salary_data(all_salaries, filename, format_type)
        
        if success:
            return jsonify({
                'success': True,
                'filename': filename,
                'message': f'Data exported successfully as {format_type.upper()}'
            })
        else:
            return jsonify({
                'error': 'Export failed',
                'message': 'Unable to export data'
            }), 500
            
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        return jsonify({
            'error': 'Export failed',
            'message': str(e)
        }), 500

@app.route('/api/refresh-data')
def refresh_data():
    """API endpoint to refresh salary data"""
    season = request.args.get('season', '2025')
    
    try:
        logger.info(f"Refreshing salary data for season {season}")
        data = load_salary_data(season, force_refresh=True)
        
        if data is None:
            return jsonify({
                'error': 'Failed to refresh data',
                'message': 'Unable to scrape fresh salary data'
            }), 500
        
        return jsonify({
            'success': True,
            'message': 'Data refreshed successfully',
            'last_updated': data['last_updated'],
            'player_count': len(data['players']),
            'team_count': len(data['team_summaries'])
        })
        
    except Exception as e:
        logger.error(f"Error refreshing data: {e}")
        return jsonify({
            'error': 'Refresh failed',
            'message': str(e)
        }), 500

@app.route('/api/health')
def health_check():
    """API endpoint for health check"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'scraper_initialized': salary_scraper is not None,
        'cached_seasons': list(cached_data.keys()) if cached_data else []
    })

# Error handlers

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize scraper on startup
def startup():
    """Initialize scraper when app starts"""
    logger.info("Initializing NBA Salary Dashboard...")
    initialize_scraper()

# Call startup function when module is imported
startup()

if __name__ == '__main__':
    # Initialize scraper
    initialize_scraper()
    
    # Use port 3005 as default
    port = int(os.environ.get('PORT', 3005))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting NBA Salary Dashboard on port {port}")
    logger.info(f"Dashboard will be available at: http://localhost:{port}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)