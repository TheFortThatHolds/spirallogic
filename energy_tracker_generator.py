#!/usr/bin/env python3
"""
SpiralLogic Personal Energy Tracker Generator
Creates the app that everyone wants but nobody builds
"""

import sys
from pathlib import Path
import json
from datetime import datetime, timedelta

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from spirallogic_runtime import SpiralLogic

def auto_consent_handler(request):
    """Auto-consent for energy tracker creation"""
    print(f"ENERGY SPIRIT CONSENT: {request.message}")
    return True

def main():
    print("=== SPIRALLOGIC PERSONAL ENERGY TRACKER ===")
    print("Building the app everyone wants but nobody makes...")
    
    # Load the SpiralLogic ritual
    ritual_file = Path(__file__).parent / "energy_tracker_app.sl"
    with open(ritual_file, 'r') as f:
        energy_ritual = f.read()
    
    # Execute the SpiralLogic ritual
    runtime = SpiralLogic(consent_callback=auto_consent_handler)
    result = runtime.execute(energy_ritual, user_id="energy_optimizer")
    
    if result['success']:
        print("SPIRALLOGIC RITUAL SUCCESSFUL!")
        print("The @healer, @analyst, and @guardian spirits have collaborated...")
        
        # Generate the actual app
        app_content = generate_energy_tracker_app()
        
        # Write the app file
        output_file = Path(__file__).parent / "personal_energy_tracker.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(app_content)
        
        print(f"ENERGY TRACKER APP CREATED: {output_file}")
        print("Finally! The app everyone wants but nobody bothers to build!")
        
        return True
    else:
        print("RITUAL FAILED:")
        print(f"Error: {result.get('error')}")
        return False

def generate_energy_tracker_app():
    """Generate the Personal Energy Tracker app through SpiralLogic magic"""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Energy Tracker - Built with SpiralLogic</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .app-container {
            max-width: 800px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #ff6b6b, #feca57);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .header p {
            opacity: 0.9;
            font-size: 1.1em;
        }
        
        .spirallogic-badge {
            background: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 15px;
            font-size: 0.9em;
            margin-top: 10px;
            display: inline-block;
        }
        
        .main-content {
            padding: 30px;
        }
        
        .energy-input-section {
            background: #f8f9ff;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
        }
        
        .energy-scale {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 20px 0;
        }
        
        .energy-level {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            border: 3px solid #ddd;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            transition: all 0.3s ease;
            font-weight: bold;
        }
        
        .energy-level:hover {
            transform: scale(1.1);
        }
        
        .energy-level.selected {
            border-color: #667eea;
            background: #667eea;
            color: white;
            transform: scale(1.2);
        }
        
        .energy-1 { background: #ff6b6b; }
        .energy-2 { background: #ffa726; }
        .energy-3 { background: #feca57; }
        .energy-4 { background: #48dbfb; }
        .energy-5 { background: #0be881; }
        
        .time-input {
            display: flex;
            gap: 15px;
            align-items: center;
            margin: 20px 0;
        }
        
        .time-input input, .time-input select {
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        
        .activity-input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            margin: 10px 0;
            font-size: 16px;
        }
        
        .btn {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 12px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        
        .insights-section {
            background: #fff5f5;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #ff6b6b;
        }
        
        .schedule-section {
            background: #f0fff4;
            border-radius: 15px;
            padding: 25px;
            margin: 20px 0;
            border-left: 5px solid #0be881;
        }
        
        .energy-chart {
            height: 200px;
            background: #f8f9ff;
            border-radius: 10px;
            margin: 20px 0;
            position: relative;
            overflow: hidden;
        }
        
        .chart-bar {
            position: absolute;
            bottom: 0;
            width: 40px;
            background: linear-gradient(to top, #667eea, #764ba2);
            border-radius: 4px 4px 0 0;
            transition: all 0.3s ease;
        }
        
        .recommendations {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        
        .recommendation-card {
            background: white;
            border: 2px solid #e1e8ed;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .recommendation-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }
        
        .rec-icon {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        .current-time {
            background: #667eea;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 20px;
            font-size: 1.2em;
        }
        
        .energy-history {
            display: flex;
            gap: 10px;
            margin: 20px 0;
            overflow-x: auto;
            padding: 10px 0;
        }
        
        .history-item {
            min-width: 80px;
            text-align: center;
            background: #f8f9ff;
            border-radius: 8px;
            padding: 10px;
            border: 2px solid #ddd;
        }
        
        .history-item.current {
            border-color: #667eea;
            background: #667eea;
            color: white;
        }
        
        .spirits-attribution {
            background: rgba(102, 126, 234, 0.1);
            border-radius: 10px;
            padding: 15px;
            margin-top: 30px;
            text-align: center;
            color: #667eea;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1>⚡ Personal Energy Tracker</h1>
            <p>Finally! The app everyone wants but nobody builds</p>
            <div class="spirallogic-badge">🔮 Powered by SpiralLogic Magic</div>
        </div>
        
        <div class="main-content">
            <div class="current-time" id="currentTime">
                Loading current time...
            </div>
            
            <div class="energy-input-section">
                <h3>How's Your Energy Right Now?</h3>
                <p>Click your current energy level (1 = exhausted, 5 = super energized)</p>
                
                <div class="energy-scale">
                    <div class="energy-level energy-1" data-level="1" onclick="selectEnergy(1)">
                        😴<br>1
                    </div>
                    <div class="energy-level energy-2" data-level="2" onclick="selectEnergy(2)">
                        😐<br>2
                    </div>
                    <div class="energy-level energy-3" data-level="3" onclick="selectEnergy(3)">
                        🙂<br>3
                    </div>
                    <div class="energy-level energy-4" data-level="4" onclick="selectEnergy(4)">
                        😊<br>4
                    </div>
                    <div class="energy-level energy-5" data-level="5" onclick="selectEnergy(5)">
                        🚀<br>5
                    </div>
                </div>
                
                <div class="time-input">
                    <label>Time:</label>
                    <input type="time" id="timeInput" />
                    <label>or</label>
                    <select id="timePreset" onchange="setPresetTime()">
                        <option value="">Choose preset...</option>
                        <option value="now">Right Now</option>
                        <option value="morning">This Morning</option>
                        <option value="afternoon">This Afternoon</option>
                        <option value="evening">This Evening</option>
                    </select>
                </div>
                
                <input type="text" class="activity-input" id="activityInput" 
                       placeholder="What are you doing? (optional - helps with patterns)" />
                
                <button class="btn" onclick="logEnergy()">Log My Energy ⚡</button>
            </div>
            
            <div class="energy-history" id="energyHistory">
                <!-- Energy history will be populated here -->
            </div>
            
            <div class="insights-section">
                <h3>🧠 Your Energy Insights</h3>
                <div id="insights">
                    <p>Start logging your energy to see patterns and insights!</p>
                </div>
            </div>
            
            <div class="schedule-section">
                <h3>📅 Smart Scheduling Suggestions</h3>
                <div class="recommendations" id="recommendations">
                    <div class="recommendation-card">
                        <div class="rec-icon">🌅</div>
                        <h4>Morning Power</h4>
                        <p>Log a few days to see your morning energy patterns</p>
                    </div>
                    <div class="recommendation-card">
                        <div class="rec-icon">🎯</div>
                        <h4>Focus Time</h4>
                        <p>We'll identify your best focus windows</p>
                    </div>
                    <div class="recommendation-card">
                        <div class="rec-icon">😴</div>
                        <h4>Rest Periods</h4>
                        <p>Know when to take breaks for maximum productivity</p>
                    </div>
                </div>
            </div>
            
            <div class="energy-chart" id="energyChart">
                <!-- Chart will be generated here -->
            </div>
            
            <div class="spirits-attribution">
                Created through SpiralLogic ritual magic<br>
                @healer spirit: Wellbeing optimization • @analyst spirit: Pattern recognition • @guardian spirit: Rest boundaries
            </div>
        </div>
    </div>

    <script>
        let energyData = JSON.parse(localStorage.getItem('energyData') || '[]');
        let selectedEnergy = null;
        
        function updateCurrentTime() {
            const now = new Date();
            const timeString = now.toLocaleString('en-US', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: '2-digit',
                hour12: true
            });
            document.getElementById('currentTime').textContent = timeString;
            
            // Set current time in time input
            const timeInput = document.getElementById('timeInput');
            if (!timeInput.value) {
                const hours = now.getHours().toString().padStart(2, '0');
                const minutes = now.getMinutes().toString().padStart(2, '0');
                timeInput.value = `${hours}:${minutes}`;
            }
        }
        
        function selectEnergy(level) {
            selectedEnergy = level;
            document.querySelectorAll('.energy-level').forEach(el => {
                el.classList.remove('selected');
            });
            document.querySelector(`[data-level="${level}"]`).classList.add('selected');
        }
        
        function setPresetTime() {
            const preset = document.getElementById('timePreset').value;
            const now = new Date();
            const timeInput = document.getElementById('timeInput');
            
            switch(preset) {
                case 'now':
                    const hours = now.getHours().toString().padStart(2, '0');
                    const minutes = now.getMinutes().toString().padStart(2, '0');
                    timeInput.value = `${hours}:${minutes}`;
                    break;
                case 'morning':
                    timeInput.value = '09:00';
                    break;
                case 'afternoon':
                    timeInput.value = '14:00';
                    break;
                case 'evening':
                    timeInput.value = '19:00';
                    break;
            }
        }
        
        function logEnergy() {
            if (!selectedEnergy) {
                alert('Please select your energy level first! 😊');
                return;
            }
            
            const timeInput = document.getElementById('timeInput').value;
            const activity = document.getElementById('activityInput').value;
            
            if (!timeInput) {
                alert('Please select a time! ⏰');
                return;
            }
            
            const now = new Date();
            const [hours, minutes] = timeInput.split(':');
            const logTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), 
                                   parseInt(hours), parseInt(minutes));
            
            const entry = {
                timestamp: logTime.toISOString(),
                energy: selectedEnergy,
                activity: activity,
                hour: parseInt(hours)
            };
            
            energyData.push(entry);
            energyData.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            
            localStorage.setItem('energyData', JSON.stringify(energyData));
            
            // Reset form
            selectedEnergy = null;
            document.querySelectorAll('.energy-level').forEach(el => {
                el.classList.remove('selected');
            });
            document.getElementById('activityInput').value = '';
            document.getElementById('timePreset').value = '';
            
            // Update displays
            updateEnergyHistory();
            updateInsights();
            updateRecommendations();
            updateChart();
            
            // Success message
            showSuccessMessage();
        }
        
        function showSuccessMessage() {
            const btn = document.querySelector('.btn');
            const originalText = btn.textContent;
            btn.textContent = '✨ Energy Logged! ✨';
            btn.style.background = 'linear-gradient(135deg, #0be881, #48dbfb)';
            
            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = 'linear-gradient(135deg, #667eea, #764ba2)';
            }, 2000);
        }
        
        function updateEnergyHistory() {
            const historyContainer = document.getElementById('energyHistory');
            const today = new Date().toDateString();
            const todayEntries = energyData.filter(entry => 
                new Date(entry.timestamp).toDateString() === today
            );
            
            if (todayEntries.length === 0) {
                historyContainer.innerHTML = '<p style="text-align: center; color: #666;">No entries for today yet</p>';
                return;
            }
            
            historyContainer.innerHTML = todayEntries.map(entry => {
                const time = new Date(entry.timestamp).toLocaleTimeString('en-US', {
                    hour: 'numeric',
                    minute: '2-digit',
                    hour12: true
                });
                
                const emoji = ['😴', '😐', '🙂', '😊', '🚀'][entry.energy - 1];
                
                return `
                    <div class="history-item">
                        <div style="font-size: 1.5em;">${emoji}</div>
                        <div style="font-size: 0.9em;">${time}</div>
                        <div style="font-size: 0.8em; color: #666;">${entry.energy}/5</div>
                    </div>
                `;
            }).join('');
        }
        
        function updateInsights() {
            const insightsContainer = document.getElementById('insights');
            
            if (energyData.length < 3) {
                insightsContainer.innerHTML = '<p>Keep logging! You need at least 3 entries to see patterns.</p>';
                return;
            }
            
            // Calculate insights
            const avgEnergy = energyData.reduce((sum, entry) => sum + entry.energy, 0) / energyData.length;
            const morningEntries = energyData.filter(entry => entry.hour >= 6 && entry.hour < 12);
            const afternoonEntries = energyData.filter(entry => entry.hour >= 12 && entry.hour < 18);
            const eveningEntries = energyData.filter(entry => entry.hour >= 18 || entry.hour < 6);
            
            const morningAvg = morningEntries.length ? 
                morningEntries.reduce((sum, entry) => sum + entry.energy, 0) / morningEntries.length : 0;
            const afternoonAvg = afternoonEntries.length ? 
                afternoonEntries.reduce((sum, entry) => sum + entry.energy, 0) / afternoonEntries.length : 0;
            const eveningAvg = eveningEntries.length ? 
                eveningEntries.reduce((sum, entry) => sum + entry.energy, 0) / eveningEntries.length : 0;
            
            let bestTime = 'morning';
            let bestAvg = morningAvg;
            if (afternoonAvg > bestAvg) { bestTime = 'afternoon'; bestAvg = afternoonAvg; }
            if (eveningAvg > bestAvg) { bestTime = 'evening'; bestAvg = eveningAvg; }
            
            insightsContainer.innerHTML = `
                <p><strong>Your average energy:</strong> ${avgEnergy.toFixed(1)}/5</p>
                <p><strong>Your best time:</strong> ${bestTime} (${bestAvg.toFixed(1)}/5 average)</p>
                <p><strong>Total logged entries:</strong> ${energyData.length}</p>
                <p><strong>@healer insight:</strong> ${getHealerInsight(avgEnergy, bestTime)}</p>
                <p><strong>@analyst pattern:</strong> ${getAnalystPattern(energyData)}</p>
            `;
        }
        
        function getHealerInsight(avgEnergy, bestTime) {
            if (avgEnergy < 2.5) {
                return "Your energy levels suggest you might benefit from more rest and self-care 💚";
            } else if (avgEnergy > 4) {
                return "Great energy levels! Remember to pace yourself to maintain this vitality ⚡";
            } else {
                return `Your energy flows best in the ${bestTime} - honor this natural rhythm 🌱`;
            }
        }
        
        function getAnalystPattern(data) {
            const recentData = data.slice(-7); // Last 7 entries
            if (recentData.length < 3) return "Need more data to identify patterns";
            
            const trend = recentData[recentData.length - 1].energy - recentData[0].energy;
            if (trend > 0.5) {
                return "Your energy is trending upward - great momentum! 📈";
            } else if (trend < -0.5) {
                return "Your energy is declining - consider what might be draining you 📉";
            } else {
                return "Your energy levels are stable - consistency is valuable 📊";
            }
        }
        
        function updateRecommendations() {
            const recsContainer = document.getElementById('recommendations');
            
            if (energyData.length < 5) {
                return; // Keep default recommendations
            }
            
            // Generate personalized recommendations based on data
            const morningEntries = energyData.filter(entry => entry.hour >= 6 && entry.hour < 12);
            const afternoonEntries = energyData.filter(entry => entry.hour >= 12 && entry.hour < 18);
            const eveningEntries = energyData.filter(entry => entry.hour >= 18 || entry.hour < 6);
            
            const morningAvg = morningEntries.length ? 
                morningEntries.reduce((sum, entry) => sum + entry.energy, 0) / morningEntries.length : 0;
            const afternoonAvg = afternoonEntries.length ? 
                afternoonEntries.reduce((sum, entry) => sum + entry.energy, 0) / afternoonEntries.length : 0;
            const eveningAvg = eveningEntries.length ? 
                eveningEntries.reduce((sum, entry) => sum + entry.energy, 0) / eveningEntries.length : 0;
            
            let recommendations = [];
            
            if (morningAvg >= 4) {
                recommendations.push({
                    icon: '🌅',
                    title: 'Morning Power Hour',
                    text: 'Your mornings are golden! Schedule important tasks between 8-11 AM'
                });
            }
            
            if (afternoonAvg >= 4) {
                recommendations.push({
                    icon: '☀️',
                    title: 'Afternoon Focus',
                    text: 'You shine in the afternoon! Use 1-4 PM for deep work'
                });
            }
            
            if (afternoonAvg < 3) {
                recommendations.push({
                    icon: '🍃',
                    title: 'Afternoon Breaks',
                    text: 'Your energy dips in the afternoon - schedule lighter tasks then'
                });
            }
            
            if (eveningAvg >= 3.5) {
                recommendations.push({
                    icon: '🌙',
                    title: 'Evening Energy',
                    text: 'You have good evening energy! Great time for creative work'
                });
            }
            
            // Always include rest recommendation
            recommendations.push({
                icon: '😴',
                title: '@guardian Reminder',
                text: 'Honor your low energy times - rest is productive too!'
            });
            
            recsContainer.innerHTML = recommendations.map(rec => `
                <div class="recommendation-card">
                    <div class="rec-icon">${rec.icon}</div>
                    <h4>${rec.title}</h4>
                    <p>${rec.text}</p>
                </div>
            `).join('');
        }
        
        function updateChart() {
            const chartContainer = document.getElementById('energyChart');
            
            if (energyData.length === 0) {
                chartContainer.innerHTML = '<p style="text-align: center; padding: 80px; color: #666;">Your energy chart will appear here as you log entries</p>';
                return;
            }
            
            // Group by hour for the chart
            const hourlyData = {};
            energyData.forEach(entry => {
                const hour = entry.hour;
                if (!hourlyData[hour]) hourlyData[hour] = [];
                hourlyData[hour].push(entry.energy);
            });
            
            // Calculate averages
            const hourlyAverages = {};
            Object.keys(hourlyData).forEach(hour => {
                hourlyAverages[hour] = hourlyData[hour].reduce((sum, energy) => sum + energy, 0) / hourlyData[hour].length;
            });
            
            // Generate chart bars
            let chartHTML = '';
            for (let hour = 6; hour < 24; hour++) {
                const avg = hourlyAverages[hour] || 0;
                const height = (avg / 5) * 180; // Scale to chart height
                const left = ((hour - 6) / 18) * 90; // Distribute across chart width
                
                if (avg > 0) {
                    chartHTML += `
                        <div class="chart-bar" style="
                            left: ${left}%;
                            height: ${height}px;
                            opacity: ${avg / 5};
                        " title="${hour}:00 - Average: ${avg.toFixed(1)}/5"></div>
                    `;
                }
            }
            
            chartContainer.innerHTML = chartHTML + `
                <div style="position: absolute; bottom: 5px; left: 10px; font-size: 0.8em; color: #666;">6 AM</div>
                <div style="position: absolute; bottom: 5px; right: 10px; font-size: 0.8em; color: #666;">11 PM</div>
                <div style="position: absolute; top: 10px; left: 50%; transform: translateX(-50%); font-size: 0.9em; color: #667eea;">
                    Your Energy Throughout the Day
                </div>
            `;
        }
        
        // Initialize app
        document.addEventListener('DOMContentLoaded', function() {
            updateCurrentTime();
            setInterval(updateCurrentTime, 60000); // Update every minute
            
            updateEnergyHistory();
            updateInsights();
            updateRecommendations();
            updateChart();
        });
    </script>
</body>
</html>'''

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)