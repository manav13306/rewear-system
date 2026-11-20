// ReWear - Admin Dashboard Script

async function loadAdminStats() {
    try {
        const response = await api.getAdminDashboard();
        if (response.success && response.data) {
            const data = response.data;
            document.getElementById('total-users').textContent = data.users.total;
            document.getElementById('active-users').textContent = data.users.active;
            document.getElementById('total-items').textContent = data.items.total;
            document.getElementById('available-items').textContent = data.items.available;
            document.getElementById('total-requests').textContent = data.requests.total || 0;
            document.getElementById('pending-requests').textContent = data.requests.pending;
            document.getElementById('total-orders').textContent = data.orders.total;
        }
    } catch (error) {
        console.error('Error loading admin stats:', error);
    }
}

async function loadItemsTable(page = 1) {
    try {
        const response = await api.getReportedItems(page);
        const tbody = document.getElementById('items-table-body');
        
        if (response.success && response.data.items) {
            const items = response.data.items;
            if (items.length === 0) {
                tbody.innerHTML = '<tr><td colspan="5" class="text-center" style="padding: 2rem;">No items requiring moderation found.</td></tr>';
                return;
            }

            tbody.innerHTML = items.map(item => `
                <tr>
                    <td>
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div style="width: 40px; height: 40px; border-radius: 8px; background: #eee; overflow: hidden;">
                                <img src="${item.image_url || '../images/placeholder.svg'}" style="width: 100%; height: 100%; object-fit: cover;">
                            </div>
                            <div>
                                <div style="font-weight: 600;">${item.title}</div>
                                <div style="font-size: 0.8rem; color: var(--text-muted);">${item.id.substring(0, 8)}...</div>
                            </div>
                        </div>
                    </td>
                    <td>${item.owner ? item.owner.username : 'Unknown'}</td>
                    <td><span class="badge badge-info">${item.category}</span></td>
                    <td><span class="badge" style="background: ${getStatusColor(item.status)}; color: white;">${item.status}</span></td>
                    <td>
                        <div class="action-btns">
                            ${item.status !== 'available' ? `<button onclick="moderateItem('${item.id}', 'approve')" class="btn btn-sm btn-primary">Approve</button>` : ''}
                            <button onclick="moderateItem('${item.id}', 'remove')" class="btn btn-sm btn-outline" style="color: var(--accent-red); border-color: var(--accent-red);">Remove</button>
                        </div>
                    </td>
                </tr>
            `).join('');
            
            document.getElementById('items-pagination-info').textContent = `Page ${response.data.pagination.current_page} of ${response.data.pagination.pages}`;
        }
    } catch (error) {
        console.error('Error loading items table:', error);
    }
}

async function loadUsersTable(page = 1) {
    try {
        // We use the search endpoint with empty query to list all if list_users is not available
        // But backend/routes/users.py HAS list_users at GET /api/users
        const response = await fetch(`${api.baseURL}/users?page=${page}`, {
            headers: api.getHeaders()
        });
        const data = await response.json();
        const tbody = document.getElementById('users-table-body');
        
        if (data.success && data.data.users) {
            const users = data.data.users;
            tbody.innerHTML = users.map(user => `
                <tr>
                    <td>
                        <div style="font-weight: 600;">${user.full_name}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted);">@${user.username}</div>
                    </td>
                    <td>${user.email}</td>
                    <td><span class="badge ${user.role === 'admin' ? 'badge-primary' : 'badge-secondary'}">${user.role}</span></td>
                    <td>
                        <span class="badge" style="background: ${user.is_active ? 'var(--accent-green)' : 'var(--accent-red)'}; color: white;">
                            ${user.is_active ? 'Active' : 'Disabled'}
                        </span>
                    </td>
                    <td>
                        <div class="action-btns">
                            <button onclick="manageUser('${user.id}', '${user.is_active ? 'disable' : 'enable'}')" class="btn btn-sm btn-outline">
                                ${user.is_active ? 'Disable' : 'Enable'}
                            </button>
                            ${user.role !== 'admin' ? `<button onclick="manageUser('${user.id}', 'delete')" class="btn btn-sm btn-outline" style="color: var(--accent-red);">Delete</button>` : ''}
                        </div>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading users table:', error);
    }
}

async function loadRequestsTable() {
    try {
        const response = await api.getAllRequests();
        const tbody = document.getElementById('requests-table-body');
        
        if (response.success && response.data.requests) {
            const requests = response.data.requests;
            tbody.innerHTML = requests.map(req => `
                <tr>
                    <td>${req.item ? req.item.title : 'Deleted Item'}</td>
                    <td>${req.requester ? req.requester.username : 'Unknown'}</td>
                    <td>${req.owner ? req.owner.username : 'Unknown'}</td>
                    <td><span class="badge badge-info">${req.request_type}</span></td>
                    <td><span class="badge" style="background: ${getRequestStatusColor(req.status)}; color: white;">${req.status}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading requests table:', error);
    }
}

async function moderateItem(itemId, action) {
    if (!confirm(`Are you sure you want to ${action} this item?`)) return;
    
    try {
        const response = await api.moderateItem(itemId, action);
        if (response.success) {
            UIUtils.showAlert(`Item ${action}ed successfully`, 'success');
            loadItemsTable();
            loadAdminStats();
        } else {
            UIUtils.showAlert(response.message, 'error');
        }
    } catch (error) {
        UIUtils.showAlert('Action failed', 'error');
    }
}

async function manageUser(userId, action) {
    if (!confirm(`Are you sure you want to ${action} this user?`)) return;
    
    try {
        const response = await api.manageUser(userId, action);
        if (response.success) {
            UIUtils.showAlert(`User ${action}d successfully`, 'success');
            loadUsersTable();
            loadAdminStats();
        } else {
            UIUtils.showAlert(response.message, 'error');
        }
    } catch (error) {
        UIUtils.showAlert('Action failed', 'error');
    }
}

function switchTab(tab, buttonEl = null) {
    // Update buttons
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    if (buttonEl) buttonEl.classList.add('active');
    
    // Update sections
    document.querySelectorAll('.admin-section').forEach(sec => sec.style.display = 'none');
    document.getElementById(`section-${tab}`).style.display = 'block';
    
    // Load data for the tab
    if (tab === 'items') loadItemsTable();
    if (tab === 'users') loadUsersTable();
    if (tab === 'requests') loadRequestsTable();
}

function getRequestStatusColor(status) {
    const colors = {
        'pending': '#f39c12',
        'accepted': '#2ecc71',
        'rejected': '#e74c3c',
        'completed': '#3498db',
        'cancelled': '#95a5a6'
    };
    return colors[status] || '#bdc3c7';
}

function getStatusColor(status) {
    const colors = {
        'available': '#2ecc71',
        'rented': '#3498db',
        'sold': '#95a5a6',
        'pending': '#f39c12',
        'inactive': '#e74c3c'
    };
    return colors[status] || '#7f8c8d';
}

// Check admin permission and load data
document.addEventListener('DOMContentLoaded', async () => {
    const isAuth = await api.checkAuthStatus();
    if (!isAuth) {
        window.location.href = '../login.html';
        return;
    }
    
    const user = AuthHelper.getCurrentUser();
    if (user.role !== 'admin') {
        UIUtils.showAlert('Admin access required', 'error');
        setTimeout(() => window.location.href = '../dashboard.html', 2000);
        return;
    }
    
    AuthHelper.updateUserMenu();
    loadAdminStats();
    loadItemsTable();
});
