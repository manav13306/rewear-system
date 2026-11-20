// ReWear - Index/Home Page Script

async function loadGlobalImpact() {
    try {
        const response = await api.getGlobalImpact();
        if (response.success && response.data) {
            const data = response.data;
            const formatter = new Intl.NumberFormat('en-US');
            
            // Update statistics
            document.getElementById('stat-users').textContent = formatter.format(data.total_users);
            document.getElementById('stat-items').textContent = formatter.format(data.total_items_listed || data.total_items_involved);
            document.getElementById('stat-co2').textContent = formatter.format(Math.round(data.total_co2_reduced_kg)) + ' kg';
            document.getElementById('stat-water').textContent = formatter.format(Math.round(data.total_water_saved_liters));
            
            // Display impact details
            const impactDiv = document.getElementById('global-impact');
            const trees = (data.total_co2_reduced_kg / 22).toFixed(1);
            const showers = (data.total_water_saved_liters / 95).toFixed(0);
            
            impactDiv.innerHTML = `
                <h3 style="margin-bottom: 1rem;">Community Environmental Achievement</h3>
                <div style="display: flex; justify-content: center; gap: 3rem; flex-wrap: wrap;">
                    <div class="impact-detail">
                        <span style="font-size: 1.5rem;">🌱</span>
                        <p style="margin: 0;"><strong>${trees}</strong> Trees worth of CO₂</p>
                    </div>
                    <div class="impact-detail">
                        <span style="font-size: 1.5rem;">🚿</span>
                        <p style="margin: 0;"><strong>${showers}</strong> Showers worth of water</p>
                    </div>
                    <div class="impact-detail">
                        <span style="font-size: 1.5rem;">👕</span>
                        <p style="margin: 0;"><strong>${formatter.format(data.total_items_involved)}</strong> Successful swaps</p>
                    </div>
                </div>
            `;
        }
    } catch (error) {
        console.error('Error loading global impact:', error);
    }
}

// Update CTA section based on login status
function updateCTASection() {
    const ctaButtons = document.getElementById('cta-buttons');
    const ctaText = document.getElementById('cta-text');
    if (!ctaButtons || !ctaText) return;

    if (AuthHelper.isLoggedIn()) {
        const user = AuthHelper.getCurrentUser();
        if (user) {
            ctaText.textContent = `Welcome back, ${user.username || 'friend'}. Ready to continue your sustainability journey?`;
            ctaButtons.innerHTML = `
                <a href="dashboard.html" class="btn btn-lg btn-primary">Go to Dashboard</a>
                <a href="upload-item.html" class="btn btn-lg btn-secondary">Upload New Item</a>
                <a href="browse-items.html" class="btn btn-lg btn-outline">Browse Collection</a>
            `;
        }
    }
}

// Load impact data on page load
document.addEventListener('DOMContentLoaded', () => {
    AuthHelper.updateUserMenu();
    updateCTASection();
    loadGlobalImpact();
});
