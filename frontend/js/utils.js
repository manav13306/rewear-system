// ============================================
// ReWear Clothing System - Utility Functions
// ============================================

class UIUtils {
    static escapeHtml(value) {
        return String(value ?? '')
            .replaceAll('&', '&amp;')
            .replaceAll('<', '&lt;')
            .replaceAll('>', '&gt;')
            .replaceAll('"', '&quot;')
            .replaceAll("'", '&#39;');
    }

    // Show notification alert
    static showAlert(message, type = 'info') {
        const alertDiv = document.createElement('div');
        alertDiv.className = `alert alert-${type}`;
        alertDiv.textContent = message;
        
        const container = document.querySelector('.container') || document.body;
        container.insertBefore(alertDiv, container.firstChild);
        
        // Auto-remove after 5 seconds
        setTimeout(() => alertDiv.remove(), 5000);
    }

    // Format currency
    static formatCurrency(amount) {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: 'USD'
        }).format(amount);
    }

    // Format date
    static formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    // Format date and time
    static formatDateTime(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    // Show loading spinner
    static showLoader(element) {
        element.innerHTML = '<div class="loading"></div>';
    }

    // Get query parameter
    static getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    // Validate email
    static validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    // Truncate text
    static truncateText(text, length = 100) {
        if (text.length > length) {
            return text.substring(0, length) + '...';
        }
        return text;
    }

    // Generate random color
    static getRandomColor() {
        const colors = ['#2ecc71', '#3498db', '#e74c3c', '#f39c12', '#9b59b6'];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    // Format large numbers
    static formatNumber(num) {
        if (num >= 1000000) return (num / 1000000).toFixed(1) + 'M';
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }
}

// Authentication helper
class AuthHelper {
    static isLoggedIn() {
        return api.isAuthenticated();
    }

    static getCurrentUser() {
        return api.getCurrentUserData();
    }

    static async redirectIfNotLoggedIn() {
        const isAuth = await api.checkAuthStatus();
        if (!isAuth) {
            window.location.href = '/login.html';
        }
    }

    static redirectIfLoggedIn() {
        if (this.isLoggedIn()) {
            window.location.href = '/dashboard.html';
        }
    }

    static logout() {
        api.logout();
        // Clear any cached data and prevent back button login
        sessionStorage.clear();
        window.location.replace('/index.html');
    }

    static updateUserMenu() {
        const userMenu = document.querySelector('.user-menu');
        if (!userMenu) return;

        if (this.isLoggedIn()) {
            const user = this.getCurrentUser();
            const isAdmin = user && user.role === 'admin';
            const safeUsername = UIUtils.escapeHtml(user?.username || 'User');
            
            userMenu.innerHTML = `
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <span style="color: var(--text-secondary); font-size: 0.9rem;">Welcome, <strong>${safeUsername}</strong></span>
                    ${isAdmin ? `<a href="/admin/dashboard.html" class="btn btn-sm btn-secondary" style="background: var(--accent-purple-dim); color: var(--accent-purple);">Admin Panel</a>` : ''}
                    <a href="/dashboard.html" class="btn btn-sm btn-primary">Dashboard</a>
                    <button onclick="AuthHelper.logout()" class="btn btn-sm btn-outline">Logout</button>
                </div>
            `;
        } else {
            userMenu.innerHTML = `
                <a href="/login.html" class="btn btn-sm btn-primary">Login</a>
                <a href="/register.html" class="btn btn-sm btn-outline">Register</a>
            `;
        }
    }
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    AuthHelper.updateUserMenu();
});

// Common page functions
function formatConditionBadge(condition) {
    const conditionMap = {
        'new': 'New',
        'like_new': 'Like New',
        'good': 'Good',
        'fair': 'Fair',
        'worn': 'Worn'
    };
    return conditionMap[condition] || condition;
}

function getStatusColor(status) {
    const colors = {
        'available': '#2ecc71',
        'rented': '#3498db',
        'sold': '#95a5a6',
        'pending': '#f39c12',
        'completed': '#27ae60'
    };
    return colors[status] || '#7f8c8d';
}

function formatImpactMetrics(metrics) {
    const formatter = new Intl.NumberFormat('en-US');
    return {
        co2: formatter.format(Math.round(metrics.carbon_saved_kg)),
        water: formatter.format(Math.round(metrics.water_saved_liters)),
        trees: (metrics.carbon_saved_kg / 22).toFixed(1),
        showers: (metrics.water_saved_liters / 95).toFixed(0)
    };
}
