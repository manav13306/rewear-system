// ReWear - Sustainability Impact Script

async function loadGlobalStats() {
    try {
        const response = await api.getGlobalImpact();
        
        if (response.success && response.data) {
            const data = response.data;
            const formatter = new Intl.NumberFormat('en-US');
            
            document.getElementById('global-items-count').textContent = formatter.format(data.total_items_involved);
            document.getElementById('global-co2-val').textContent = formatter.format(Math.round(data.total_co2_reduced_kg)) + ' kg';
            document.getElementById('global-water-val').textContent = formatter.format(Math.round(data.total_water_saved_liters));
            
            // Add Equivalents as cards
            const equivalentsHtml = `
                <div class="elite-card bento-wide">
                    <div class="elite-label">Eco-Equivalents</div>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">
                        <div>
                            <span style="font-size: 1.5rem;">🌱</span> <strong>${data.co2_equivalents.trees_equivalent}</strong>
                            <div class="small text-muted">Trees Planted</div>
                        </div>
                        <div>
                            <span style="font-size: 1.5rem;">🚿</span> <strong>${formatter.format(data.water_equivalents.showers)}</strong>
                            <div class="small text-muted">Showers Saved</div>
                        </div>
                    </div>
                </div>
            `;
            
            const grid = document.getElementById('impact-grid');
            // Remove existing equivalents if any to prevent duplicates on refresh
            const existingEq = document.getElementById('global-eq-card');
            if (existingEq) existingEq.remove();
            
            const eqDiv = document.createElement('div');
            eqDiv.id = 'global-eq-card';
            eqDiv.className = 'bento-wide'; // Wrapped in div to match elite-card if needed
            eqDiv.innerHTML = equivalentsHtml;
            grid.appendChild(eqDiv.firstElementChild);
        }
    } catch (error) {
        console.error('Error loading global stats:', error);
    }
}

async function loadPersonalStats() {
    if (!AuthHelper.isLoggedIn()) {
        document.getElementById('personal-impact').style.display = 'none';
        return;
    }
    
    try {
        const user = AuthHelper.getCurrentUser();
        const response = await api.getUserImpact(user.id);
        
        if (response.success && response.data) {
            const data = response.data;
            const formatter = new Intl.NumberFormat('en-US');
            
            const personalHtml = `
                <div class="elite-card bento-large" id="personal-impact-card">
                    <div class="elite-label">Your Contribution</div>
                    <div class="elite-title" style="font-size: 3rem;">${Math.round(data.impact_score)}</div>
                    <div style="color: var(--accent-green); font-weight: 700; letter-spacing: 0.15em; margin-bottom: 2rem;">ECO-SCORE</div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem;">
                        <div>
                            <div class="elite-label" style="font-size: 0.7rem;">CO₂ Saved</div>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #2ecc71;">${formatter.format(Math.round(data.carbon_saved_kg))} kg</div>
                        </div>
                        <div>
                            <div class="elite-label" style="font-size: 0.7rem;">Water Saved</div>
                            <div style="font-size: 1.5rem; font-weight: 800; color: #3498db;">${formatter.format(Math.round(data.water_saved_liters))} L</div>
                        </div>
                    </div>
                    <div class="rank-badge-elite">✨</div>
                </div>
                <div class="elite-card bento-tall" id="personal-rank-card">
                    <div class="elite-label">Reputation</div>
                    <div style="font-size: 2.5rem; font-weight: 900; color: #f1c40f; margin-top: 1rem;">${data.reputation_score}</div>
                    <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">Commendations</div>
                    <div class="rank-badge-elite" style="opacity: 0.1;">👑</div>
                </div>
            `;
            
            const grid = document.getElementById('impact-grid');
            // Prepend personal stats to grid
            const personalContainer = document.createElement('div');
            personalContainer.innerHTML = personalHtml;
            
            // Cleanup existing personal cards
            const oldP1 = document.getElementById('personal-impact-card');
            if (oldP1) oldP1.remove();
            const oldP2 = document.getElementById('personal-rank-card');
            if (oldP2) oldP2.remove();
            
            // Insert cards at the beginning of the grid
            const children = Array.from(personalContainer.children);
            children.reverse().forEach(child => grid.prepend(child));
        }
    } catch (error) {
        console.error('Error loading personal stats:', error);
    }
}

async function loadLeaderboard() {
    try {
        const response = await api.getLeaderboard(1);
        
        if (response.success && response.data.leaderboard) {
            const leaderboard = response.data.leaderboard.slice(0, 10);
            const formatter = new Intl.NumberFormat('en-US');
            const currentUser = AuthHelper.getCurrentUser();
            
            const html = `
                <table class="leaderboard-table">
                    <thead>
                        <tr>
                            <th style="width: 80px;">Rank</th>
                            <th>Eco-Champion</th>
                            <th style="text-align: center;">CO₂ Saved</th>
                            <th style="text-align: center;">Items</th>
                            <th style="text-align: center; width: 120px;">Eco-Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${leaderboard.map((user, idx) => {
                            const isMe = currentUser && (user.user_id === currentUser.id || user.user_id === currentUser._id);
                            const rank = idx + 1;
                            const rankClass = rank <= 3 ? `rank-${rank}` : '';
                            
                            return `
                                <tr class="leaderboard-row ${isMe ? 'current-user' : ''}">
                                    <td>
                                        <span class="rank-badge ${rankClass}">${rank <= 3 ? (rank === 1 ? '🥇' : rank === 2 ? '🥈' : '🥉') : rank}</span>
                                    </td>
                                    <td>
                                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                                            <div style="width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, var(--accent-green), var(--accent-blue)); display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 1.1rem; color: white;">
                                                ${user.username.charAt(0).toUpperCase()}
                                            </div>
                                            <div>
                                                <div style="font-weight: 700;">${user.username} ${isMe ? '<span style="color: var(--accent-green); font-size: 0.7rem; margin-left: 4px;">(YOU)</span>' : ''}</div>
                                                <div style="font-size: 0.75rem; color: var(--text-muted);">${user.reputation_score} reputation</div>
                                            </div>
                                        </div>
                                    </td>
                                    <td style="text-align: center; color: var(--accent-green); font-weight: 700;">
                                        ${formatter.format(Math.round(user.carbon_saved_kg))} kg
                                    </td>
                                    <td style="text-align: center;">
                                        <span style="font-weight: 600;">${user.total_items_reworn + user.total_items_rented + user.total_items_sold + user.total_items_exchanged}</span>
                                    </td>
                                    <td style="text-align: center;">
                                        <div style="display: inline-block; padding: 4px 12px; border-radius: 20px; background: rgba(46, 204, 113, 0.1); color: var(--accent-green); font-weight: 800;">
                                            ${Math.round(user.impact_score)}
                                        </div>
                                    </td>
                                </tr>
                            `;
                        }).join('')}
                    </tbody>
                </table>
                ${leaderboard.length === 0 ? '<div style="padding: 3rem; text-align: center; color: var(--text-muted);">No eco-champions found yet. Start rewearing to climb the ranks!</div>' : ''}
            `;
            
            document.getElementById('leaderboard-container').innerHTML = html;
        }
    } catch (error) {
        console.error('Error loading leaderboard:', error);
    }
}

// Load data on page load
document.addEventListener('DOMContentLoaded', async () => {
    await AuthHelper.redirectIfNotLoggedIn();
    AuthHelper.updateUserMenu();
    loadGlobalStats();
    loadPersonalStats();
    loadLeaderboard();
});

// Check auth on page show (handles browser back button)
window.addEventListener('pageshow', async (event) => {
    await AuthHelper.redirectIfNotLoggedIn();
    AuthHelper.updateUserMenu();
});
