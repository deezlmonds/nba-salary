// NBA Salary Dashboard JavaScript

class NBASalaryDashboard {
    constructor() {
        this.data = {
            players: [],
            teams: [],
            teamSummaries: []
        };
        this.charts = {};
        this.currentSeason = '2025';
        this.init();
    }

    async init() {
        this.setupEventListeners();
        this.showLoading();
        await this.loadData();
        this.hideLoading();
        this.renderDashboard();
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchTab(e.target.dataset.tab));
        });

        // Season selector
        document.getElementById('season-select').addEventListener('change', (e) => {
            this.currentSeason = e.target.value;
            this.loadData();
        });

        // Refresh data button
        document.getElementById('refresh-data').addEventListener('click', () => {
            this.loadData();
        });

        // Search and filter controls
        document.getElementById('player-search').addEventListener('input', (e) => {
            this.filterPlayers();
        });

        document.getElementById('team-filter').addEventListener('change', () => {
            this.filterPlayers();
        });

        document.getElementById('salary-range-filter').addEventListener('change', () => {
            this.filterPlayers();
        });

        document.getElementById('team-search').addEventListener('input', (e) => {
            this.filterTeams(e.target.value);
        });

        // Export functionality
        document.getElementById('export-players').addEventListener('click', () => {
            this.exportPlayersData();
        });

        // Modal controls
        document.getElementById('about-link').addEventListener('click', (e) => {
            e.preventDefault();
            this.showModal('about-modal');
        });

        document.querySelectorAll('.close').forEach(close => {
            close.addEventListener('click', (e) => {
                this.hideModal(e.target.closest('.modal').id);
            });
        });

        // Chart controls
        document.getElementById('payroll-sort').addEventListener('change', () => {
            this.updateTeamPayrollChart();
        });

        document.getElementById('top-players-count').addEventListener('change', () => {
            this.updateTopEarners();
        });
    }

    showLoading() {
        document.getElementById('loading').classList.remove('hidden');
    }

    hideLoading() {
        document.getElementById('loading').classList.add('hidden');
    }

    async loadData() {
        this.showLoading();
        
        try {
            // In a real implementation, this would fetch from your Python backend
            // For demo purposes, we'll generate sample data
            await this.generateSampleData();
            this.updateHeaderStats();
            this.renderDashboard();
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Failed to load NBA salary data');
        } finally {
            this.hideLoading();
        }
    }

    async generateSampleData() {
        // Generate realistic NBA salary data for demonstration
        const teams = [
            { abbr: 'LAL', name: 'Los Angeles Lakers' },
            { abbr: 'GSW', name: 'Golden State Warriors' },
            { abbr: 'BOS', name: 'Boston Celtics' },
            { abbr: 'MIA', name: 'Miami Heat' },
            { abbr: 'PHI', name: 'Philadelphia 76ers' },
            { abbr: 'DEN', name: 'Denver Nuggets' },
            { abbr: 'MIL', name: 'Milwaukee Bucks' },
            { abbr: 'NYK', name: 'New York Knicks' },
            { abbr: 'DAL', name: 'Dallas Mavericks' },
            { abbr: 'PHX', name: 'Phoenix Suns' },
            { abbr: 'CLE', name: 'Cleveland Cavaliers' },
            { abbr: 'ATL', name: 'Atlanta Hawks' },
            { abbr: 'TOR', name: 'Toronto Raptors' },
            { abbr: 'CHI', name: 'Chicago Bulls' },
            { abbr: 'SAC', name: 'Sacramento Kings' },
            { abbr: 'OKC', name: 'Oklahoma City Thunder' },
            { abbr: 'MIN', name: 'Minnesota Timberwolves' },
            { abbr: 'NOP', name: 'New Orleans Pelicans' },
            { abbr: 'IND', name: 'Indiana Pacers' },
            { abbr: 'ORL', name: 'Orlando Magic' },
            { abbr: 'WAS', name: 'Washington Wizards' },
            { abbr: 'CHA', name: 'Charlotte Hornets' },
            { abbr: 'POR', name: 'Portland Trail Blazers' },
            { abbr: 'UTA', name: 'Utah Jazz' },
            { abbr: 'BRK', name: 'Brooklyn Nets' },
            { abbr: 'DET', name: 'Detroit Pistons' },
            { abbr: 'HOU', name: 'Houston Rockets' },
            { abbr: 'MEM', name: 'Memphis Grizzlies' },
            { abbr: 'SAS', name: 'San Antonio Spurs' },
            { abbr: 'LAC', name: 'LA Clippers' }
        ];

        const starPlayers = [
            { name: 'Stephen Curry', team: 'GSW', salary: 59606817 },
            { name: 'Joel Embiid', team: 'PHI', salary: 55224526 },
            { name: 'Nikola Jokic', team: 'DEN', salary: 55224526 },
            { name: 'Kevin Durant', team: 'PHX', salary: 54708608 },
            { name: 'Jayson Tatum', team: 'BOS', salary: 54126450 },
            { name: 'Giannis Antetokounmpo', team: 'MIL', salary: 54126450 },
            { name: 'Anthony Davis', team: 'LAL', salary: 54126450 },
            { name: 'Jimmy Butler', team: 'MIA', salary: 54126450 },
            { name: 'Jaylen Brown', team: 'BOS', salary: 53142264 },
            { name: 'Devin Booker', team: 'PHX', salary: 53142264 },
            { name: 'Karl-Anthony Towns', team: 'NYK', salary: 53142264 },
            { name: 'LeBron James', team: 'LAL', salary: 52627153 },
            { name: 'Paul George', team: 'PHI', salary: 51666090 },
            { name: 'Kawhi Leonard', team: 'LAC', salary: 50000000 },
            { name: 'Zach LaVine', team: 'CHI', salary: 47499660 }
        ];

        // Generate players data
        this.data.players = [];
        teams.forEach(team => {
            const teamStars = starPlayers.filter(p => p.team === team.abbr);
            const playersPerTeam = 15;
            
            for (let i = 0; i < playersPerTeam; i++) {
                let salary;
                let playerName;
                
                if (i < teamStars.length) {
                    // Use star player data
                    salary = teamStars[i].salary;
                    playerName = teamStars[i].name;
                } else {
                    // Generate role players with realistic salaries
                    const salaryTiers = [
                        { min: 25000000, max: 40000000, weight: 0.1 },  // Star players
                        { min: 15000000, max: 25000000, weight: 0.2 },  // Solid starters
                        { min: 8000000, max: 15000000, weight: 0.3 },   // Role players
                        { min: 3000000, max: 8000000, weight: 0.3 },    // Bench players
                        { min: 1000000, max: 3000000, weight: 0.1 }     // Minimum contracts
                    ];
                    
                    const tier = this.getRandomTier(salaryTiers);
                    salary = Math.floor(Math.random() * (tier.max - tier.min) + tier.min);
                    playerName = this.generatePlayerName();
                }

                this.data.players.push({
                    player_name: playerName,
                    team_abbr: team.abbr,
                    team_name: team.name,
                    [`${this.currentSeason}_salary`]: salary,
                    total_guaranteed: salary * (2 + Math.random() * 3) // 2-5 year contracts
                });
            }
        });

        // Generate team summaries
        this.data.teamSummaries = teams.map(team => {
            const teamPlayers = this.data.players.filter(p => p.team_abbr === team.abbr);
            const salaries = teamPlayers.map(p => p[`${this.currentSeason}_salary`]);
            const totalPayroll = salaries.reduce((sum, salary) => sum + salary, 0);
            
            return {
                team_abbr: team.abbr,
                team_name: team.name,
                total_payroll: totalPayroll,
                average_salary: totalPayroll / teamPlayers.length,
                median_salary: this.median(salaries),
                highest_paid_player: teamPlayers.reduce((max, p) => 
                    p[`${this.currentSeason}_salary`] > max[`${this.currentSeason}_salary`] ? p : max
                ).player_name,
                highest_salary: Math.max(...salaries),
                lowest_salary: Math.min(...salaries),
                num_players: teamPlayers.length,
                players_over_10m: salaries.filter(s => s > 10000000).length,
                players_over_20m: salaries.filter(s => s > 20000000).length,
                players_over_30m: salaries.filter(s => s > 30000000).length
            };
        });

        // Sort team summaries by total payroll
        this.data.teamSummaries.sort((a, b) => b.total_payroll - a.total_payroll);
    }

    getRandomTier(tiers) {
        const totalWeight = tiers.reduce((sum, tier) => sum + tier.weight, 0);
        let random = Math.random() * totalWeight;
        
        for (const tier of tiers) {
            random -= tier.weight;
            if (random <= 0) return tier;
        }
        
        return tiers[tiers.length - 1];
    }

    generatePlayerName() {
        const firstNames = ['Marcus', 'Tyler', 'Jordan', 'Chris', 'Alex', 'Brandon', 'Kevin', 'James', 'Michael', 'David', 'Anthony', 'Robert', 'Daniel', 'Matthew', 'Ryan'];
        const lastNames = ['Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas'];
        
        const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
        const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
        
        return `${firstName} ${lastName}`;
    }

    median(arr) {
        const sorted = [...arr].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 === 0 
            ? (sorted[mid - 1] + sorted[mid]) / 2 
            : sorted[mid];
    }

    updateHeaderStats() {
        const totalPlayers = this.data.players.length;
        const totalPayroll = this.data.players.reduce((sum, p) => sum + p[`${this.currentSeason}_salary`], 0);
        const avgSalary = totalPayroll / totalPlayers;

        document.getElementById('total-players').textContent = totalPlayers.toLocaleString();
        document.getElementById('total-payroll').textContent = this.formatCurrency(totalPayroll);
        document.getElementById('avg-salary').textContent = this.formatCurrency(avgSalary);
    }

    renderDashboard() {
        this.renderOverviewTab();
        this.renderTeamsTab();
        this.renderPlayersTab();
        this.renderAnalysisTab();
    }

    renderOverviewTab() {
        this.createSalaryDistributionChart();
        this.createTeamPayrollChart();
        this.updateTopEarners();
        this.updateLeagueStats();
    }

    createSalaryDistributionChart() {
        const ctx = document.getElementById('salary-distribution-chart').getContext('2d');
        
        // Create salary distribution data
        const salaries = this.data.players.map(p => p[`${this.currentSeason}_salary`]);
        const ranges = [
            { label: 'Under $5M', min: 0, max: 5000000, color: '#3b82f6' },
            { label: '$5M - $10M', min: 5000000, max: 10000000, color: '#10b981' },
            { label: '$10M - $20M', min: 10000000, max: 20000000, color: '#f59e0b' },
            { label: '$20M - $30M', min: 20000000, max: 30000000, color: '#ef4444' },
            { label: '$30M - $40M', min: 30000000, max: 40000000, color: '#8b5cf6' },
            { label: 'Over $40M', min: 40000000, max: Infinity, color: '#ec4899' }
        ];

        const data = ranges.map(range => ({
            label: range.label,
            count: salaries.filter(s => s >= range.min && s < range.max).length,
            color: range.color
        }));

        this.charts.salaryDistribution = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: data.map(d => d.label),
                datasets: [{
                    data: data.map(d => d.count),
                    backgroundColor: data.map(d => d.color),
                    borderWidth: 2,
                    borderColor: '#1e293b'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#f8fafc',
                            padding: 20
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const percentage = ((context.raw / salaries.length) * 100).toFixed(1);
                                return `${context.label}: ${context.raw} players (${percentage}%)`;
                            }
                        }
                    }
                }
            }
        });
    }

    createTeamPayrollChart() {
        const ctx = document.getElementById('team-payroll-chart').getContext('2d');
        
        const sortedTeams = [...this.data.teamSummaries].slice(0, 15); // Top 15 teams
        
        this.charts.teamPayroll = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: sortedTeams.map(t => t.team_abbr),
                datasets: [{
                    label: 'Total Payroll',
                    data: sortedTeams.map(t => t.total_payroll / 1000000), // Convert to millions
                    backgroundColor: '#3b82f6',
                    borderColor: '#1d4ed8',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#f8fafc'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `Payroll: ${this.formatCurrency(context.raw * 1000000)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#cbd5e1'
                        },
                        grid: {
                            color: '#334155'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#cbd5e1',
                            callback: (value) => `$${value}M`
                        },
                        grid: {
                            color: '#334155'
                        }
                    }
                }
            }
        });
    }

    updateTeamPayrollChart() {
        const sortBy = document.getElementById('payroll-sort').value;
        let sortedTeams = [...this.data.teamSummaries];
        
        switch (sortBy) {
            case 'average':
                sortedTeams.sort((a, b) => b.average_salary - a.average_salary);
                break;
            case 'players':
                sortedTeams.sort((a, b) => b.num_players - a.num_players);
                break;
            default:
                sortedTeams.sort((a, b) => b.total_payroll - a.total_payroll);
        }
        
        sortedTeams = sortedTeams.slice(0, 15);
        
        if (this.charts.teamPayroll) {
            this.charts.teamPayroll.data.labels = sortedTeams.map(t => t.team_abbr);
            this.charts.teamPayroll.data.datasets[0].data = sortedTeams.map(t => 
                sortBy === 'average' ? t.average_salary / 1000000 : 
                sortBy === 'players' ? t.num_players :
                t.total_payroll / 1000000
            );
            this.charts.teamPayroll.data.datasets[0].label = 
                sortBy === 'average' ? 'Average Salary' :
                sortBy === 'players' ? 'Number of Players' :
                'Total Payroll';
            this.charts.teamPayroll.update();
        }
    }

    updateTopEarners() {
        const count = parseInt(document.getElementById('top-players-count').value);
        const topPlayers = [...this.data.players]
            .sort((a, b) => b[`${this.currentSeason}_salary`] - a[`${this.currentSeason}_salary`])
            .slice(0, count);
        
        const container = document.getElementById('top-earners-list');
        container.innerHTML = '';
        
        topPlayers.forEach((player, index) => {
            const playerItem = document.createElement('div');
            playerItem.className = 'player-item fade-in';
            playerItem.innerHTML = `
                <div class="player-info">
                    <div class="player-name">${index + 1}. ${player.player_name}</div>
                    <div class="player-team">${player.team_name}</div>
                </div>
                <div class="player-salary">${this.formatCurrency(player[`${this.currentSeason}_salary`])}</div>
            `;
            container.appendChild(playerItem);
        });
    }

    updateLeagueStats() {
        const salaries = this.data.players.map(p => p[`${this.currentSeason}_salary`]);
        
        const medianSalary = this.median(salaries);
        const maxSalary = Math.max(...salaries);
        const minSalary = Math.min(...salaries);
        const playersOver20M = salaries.filter(s => s > 20000000).length;
        
        document.getElementById('median-salary').textContent = this.formatCurrency(medianSalary);
        document.getElementById('max-salary').textContent = this.formatCurrency(maxSalary);
        document.getElementById('min-salary').textContent = this.formatCurrency(minSalary);
        document.getElementById('players-over-20m').textContent = playersOver20M;
    }

    renderTeamsTab() {
        this.renderTeamRankings();
        this.populateTeamFilter();
    }

    renderTeamRankings() {
        const container = document.getElementById('team-rankings');
        container.innerHTML = '';
        
        this.data.teamSummaries.forEach((team, index) => {
            const teamItem = document.createElement('div');
            teamItem.className = 'team-item';
            teamItem.innerHTML = `
                <div class="team-rank">${index + 1}</div>
                <div class="team-info">
                    <div class="team-name">${team.team_name}</div>
                    <div>${team.num_players} players</div>
                </div>
                <div class="team-payroll">${this.formatCurrency(team.total_payroll)}</div>
            `;
            
            teamItem.addEventListener('click', () => {
                this.selectTeam(team, teamItem);
            });
            
            container.appendChild(teamItem);
        });
    }

    selectTeam(team, element) {
        // Remove previous selection
        document.querySelectorAll('.team-item').forEach(item => {
            item.classList.remove('selected');
        });
        
        // Add selection to current item
        element.classList.add('selected');
        
        // Show team details
        this.showTeamDetails(team);
    }

    showTeamDetails(team) {
        const teamPlayers = this.data.players.filter(p => p.team_abbr === team.team_abbr);
        teamPlayers.sort((a, b) => b[`${this.currentSeason}_salary`] - a[`${this.currentSeason}_salary`]);
        
        const container = document.getElementById('team-details');
        container.innerHTML = `
            <div class="team-detail-header">
                <h4>${team.team_name} (${team.team_abbr})</h4>
                <div class="team-stats">
                    <div class="stat-item">
                        <span class="stat-number">${this.formatCurrency(team.total_payroll)}</span>
                        <span class="stat-title">Total Payroll</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${this.formatCurrency(team.average_salary)}</span>
                        <span class="stat-title">Average Salary</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-number">${team.players_over_20m}</span>
                        <span class="stat-title">Players > $20M</span>
                    </div>
                </div>
            </div>
            <div class="team-roster">
                <h5>Roster (${team.num_players} players)</h5>
                <div class="player-list">
                    ${teamPlayers.map(player => `
                        <div class="player-item">
                            <div class="player-info">
                                <div class="player-name">${player.player_name}</div>
                            </div>
                            <div class="player-salary">${this.formatCurrency(player[`${this.currentSeason}_salary`])}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    renderPlayersTab() {
        this.renderPlayersTable();
    }

    populateTeamFilter() {
        const teamFilter = document.getElementById('team-filter');
        teamFilter.innerHTML = '<option value="">All Teams</option>';
        
        this.data.teamSummaries.forEach(team => {
            const option = document.createElement('option');
            option.value = team.team_abbr;
            option.textContent = team.team_name;
            teamFilter.appendChild(option);
        });
    }

    renderPlayersTable() {
        const container = document.getElementById('players-table');
        const players = this.getFilteredPlayers();
        
        container.innerHTML = `
            <table class="players-table">
                <thead>
                    <tr>
                        <th>Rank</th>
                        <th>Player</th>
                        <th>Team</th>
                        <th>Salary</th>
                        <th>Total Guaranteed</th>
                    </tr>
                </thead>
                <tbody>
                    ${players.map((player, index) => `
                        <tr>
                            <td>${index + 1}</td>
                            <td>${player.player_name}</td>
                            <td>${player.team_abbr}</td>
                            <td class="salary-cell">${this.formatCurrency(player[`${this.currentSeason}_salary`])}</td>
                            <td class="salary-cell">${this.formatCurrency(player.total_guaranteed)}</td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    getFilteredPlayers() {
        let players = [...this.data.players];
        
        // Filter by search term
        const searchTerm = document.getElementById('player-search').value.toLowerCase();
        if (searchTerm) {
            players = players.filter(p => 
                p.player_name.toLowerCase().includes(searchTerm) ||
                p.team_name.toLowerCase().includes(searchTerm)
            );
        }
        
        // Filter by team
        const teamFilter = document.getElementById('team-filter').value;
        if (teamFilter) {
            players = players.filter(p => p.team_abbr === teamFilter);
        }
        
        // Filter by salary range
        const salaryRange = document.getElementById('salary-range-filter').value;
        if (salaryRange) {
            const salary = players.map(p => p[`${this.currentSeason}_salary`]);
            if (salaryRange.includes('+')) {
                const threshold = parseInt(salaryRange.replace('+', ''));
                players = players.filter(p => p[`${this.currentSeason}_salary`] >= threshold);
            } else if (salaryRange.includes('-')) {
                const [min, max] = salaryRange.split('-').map(s => parseInt(s));
                players = players.filter(p => {
                    const salary = p[`${this.currentSeason}_salary`];
                    return salary >= min && salary <= max;
                });
            }
        }
        
        // Sort by salary (highest first)
        players.sort((a, b) => b[`${this.currentSeason}_salary`] - a[`${this.currentSeason}_salary`]);
        
        return players;
    }

    filterPlayers() {
        this.renderPlayersTable();
    }

    filterTeams(searchTerm) {
        const teams = document.querySelectorAll('.team-item');
        teams.forEach(team => {
            const teamName = team.querySelector('.team-name').textContent.toLowerCase();
            if (teamName.includes(searchTerm.toLowerCase())) {
                team.style.display = 'flex';
            } else {
                team.style.display = 'none';
            }
        });
    }

    renderAnalysisTab() {
        this.createSalaryTrendsChart();
        this.createTeamComparisonChart();
        this.generateInsights();
    }

    createSalaryTrendsChart() {
        const ctx = document.getElementById('salary-trends-chart').getContext('2d');
        
        // Generate trend data (simulated multi-year data)
        const years = ['2021', '2022', '2023', '2024', '2025'];
        const avgSalaries = years.map(year => {
            const baseAvg = 12000000; // Base average salary
            const growth = (parseInt(year) - 2021) * 0.05; // 5% annual growth
            return baseAvg * (1 + growth);
        });
        
        const medianSalaries = avgSalaries.map(avg => avg * 0.7); // Median typically lower
        const maxSalaries = avgSalaries.map(avg => avg * 4.5); // Max salaries much higher
        
        this.charts.salaryTrends = new Chart(ctx, {
            type: 'line',
            data: {
                labels: years,
                datasets: [
                    {
                        label: 'Average Salary',
                        data: avgSalaries,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Median Salary',
                        data: medianSalaries,
                        borderColor: '#10b981',
                        backgroundColor: 'rgba(16, 185, 129, 0.1)',
                        tension: 0.4
                    },
                    {
                        label: 'Maximum Salary',
                        data: maxSalaries,
                        borderColor: '#f59e0b',
                        backgroundColor: 'rgba(245, 158, 11, 0.1)',
                        tension: 0.4
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#f8fafc'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                return `${context.dataset.label}: ${this.formatCurrency(context.raw)}`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: {
                            color: '#cbd5e1'
                        },
                        grid: {
                            color: '#334155'
                        }
                    },
                    y: {
                        ticks: {
                            color: '#cbd5e1',
                            callback: (value) => this.formatCurrency(value, true)
                        },
                        grid: {
                            color: '#334155'
                        }
                    }
                }
            }
        });
    }

    createTeamComparisonChart() {
        const ctx = document.getElementById('team-comparison-chart').getContext('2d');
        
        const teams = this.data.teamSummaries.slice(0, 10); // Top 10 teams
        
        this.charts.teamComparison = new Chart(ctx, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Teams',
                    data: teams.map(team => ({
                        x: team.average_salary / 1000000,
                        y: team.players_over_20m,
                        team: team.team_abbr
                    })),
                    backgroundColor: '#3b82f6',
                    borderColor: '#1d4ed8',
                    pointRadius: 8,
                    pointHoverRadius: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        labels: {
                            color: '#f8fafc'
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const point = context.raw;
                                return [
                                    `Team: ${point.team}`,
                                    `Avg Salary: ${this.formatCurrency(point.x * 1000000)}`,
                                    `Players > $20M: ${point.y}`
                                ];
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        title: {
                            display: true,
                            text: 'Average Salary (Millions)',
                            color: '#f8fafc'
                        },
                        ticks: {
                            color: '#cbd5e1',
                            callback: (value) => `$${value}M`
                        },
                        grid: {
                            color: '#334155'
                        }
                    },
                    y: {
                        title: {
                            display: true,
                            text: 'Players Earning > $20M',
                            color: '#f8fafc'
                        },
                        ticks: {
                            color: '#cbd5e1'
                        },
                        grid: {
                            color: '#334155'
                        }
                    }
                }
            }
        });
    }

    generateInsights() {
        const container = document.getElementById('salary-insights');
        const salaries = this.data.players.map(p => p[`${this.currentSeason}_salary`]);
        const totalPayroll = salaries.reduce((sum, salary) => sum + salary, 0);
        const avgSalary = totalPayroll / salaries.length;
        
        const insights = [
            {
                title: 'Salary Cap Impact',
                description: `The average NBA team spends ${this.formatCurrency(totalPayroll / 30)} on player salaries, with significant variation between teams.`
            },
            {
                title: 'Star Player Premium',
                description: `Players earning over $40M represent ${((salaries.filter(s => s > 40000000).length / salaries.length) * 100).toFixed(1)}% of all players but consume a disproportionate share of team budgets.`
            },
            {
                title: 'Middle Class Squeeze',
                description: `The salary distribution shows a clear divide between star players and role players, with fewer mid-tier contracts.`
            },
            {
                title: 'Team Building Strategy',
                description: `Teams with multiple max contracts must rely heavily on minimum salary players and draft picks to fill out their rosters.`
            }
        ];
        
        container.innerHTML = insights.map(insight => `
            <div class="insight-item fade-in">
                <div class="insight-title">${insight.title}</div>
                <div class="insight-description">${insight.description}</div>
            </div>
        `).join('');
    }

    switchTab(tabName) {
        // Update tab buttons
        document.querySelectorAll('.nav-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');
        
        // Update tab content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(`${tabName}-tab`).classList.add('active');
    }

    showModal(modalId) {
        document.getElementById(modalId).style.display = 'block';
    }

    hideModal(modalId) {
        document.getElementById(modalId).style.display = 'none';
    }

    exportPlayersData() {
        const players = this.getFilteredPlayers();
        const csvContent = this.convertToCSV(players);
        this.downloadCSV(csvContent, `nba_players_${this.currentSeason}.csv`);
    }

    convertToCSV(data) {
        const headers = ['Player Name', 'Team', 'Team Name', 'Salary', 'Total Guaranteed'];
        const csvRows = [headers.join(',')];
        
        data.forEach(player => {
            const row = [
                `"${player.player_name}"`,
                player.team_abbr,
                `"${player.team_name}"`,
                player[`${this.currentSeason}_salary`],
                player.total_guaranteed
            ];
            csvRows.push(row.join(','));
        });
        
        return csvRows.join('\n');
    }

    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    formatCurrency(amount, short = false) {
        if (short && amount >= 1000000) {
            return `$${(amount / 1000000).toFixed(1)}M`;
        }
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(amount);
    }

    showError(message) {
        // Simple error display - in production, you'd want a more sophisticated error handling
        alert(`Error: ${message}`);
    }
}

// Initialize the dashboard when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new NBASalaryDashboard();
});

// Handle window click events for modals
window.addEventListener('click', (event) => {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
});