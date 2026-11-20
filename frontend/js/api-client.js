// ============================================
// ReWear Clothing System - API Client
// ============================================

class APIClient {
    constructor(baseURL = "http://localhost:5000/api") {
        this.baseURL = baseURL;
        this.token = localStorage.getItem("access_token");
    }

    _getToken() {
        this.token = this.token || localStorage.getItem("access_token");
        return this.token;
    }

    _buildHeaders(includeJson = true) {
        const headers = {};
        if (includeJson) headers["Content-Type"] = "application/json";

        const token = this._getToken();
        if (token) headers.Authorization = `Bearer ${token}`;
        return headers;
    }

    _buildUrl(path, params = null) {
        const url = new URL(`${this.baseURL}${path}`);
        if (params) {
            Object.entries(params).forEach(([key, value]) => {
                if (value === undefined || value === null || value === "") return;
                url.searchParams.set(key, value);
            });
        }
        return url.toString();
    }

    async _request(path, options = {}, queryParams = null) {
        const url = this._buildUrl(path, queryParams);
        try {
            const response = await fetch(url, options);
            const data = await response.json().catch(() => null);

            if (!response.ok) {
                return {
                    success: false,
                    message: data?.message || `Request failed with status ${response.status}`,
                    data: data?.data ?? null,
                };
            }

            return data ?? { success: true, data: null, message: "Success" };
        } catch (error) {
            return { success: false, message: error.message, data: null };
        }
    }

    // ===== AUTHENTICATION =====

    async register(username, email, password, fullName) {
        return this._request("/auth/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                username,
                email,
                password,
                full_name: fullName,
            }),
        });
    }

    async login(email, password) {
        const data = await this._request("/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
        });

        if (data.success && data.data?.access_token) {
            localStorage.setItem("access_token", data.data.access_token);
            localStorage.setItem("user", JSON.stringify(data.data.user));
            this.token = data.data.access_token;
        }

        return data;
    }

    logout() {
        localStorage.removeItem("access_token");
        localStorage.removeItem("user");
        this.token = null;
    }

    // ===== ITEMS =====

    async getItems(page = 1, filters = {}) {
        return this._request("/items", { method: "GET" }, { page, ...filters });
    }

    async getUserItems(userId, page = 1, perPage = 50) {
        return this._request(`/items/user/${userId}`, { method: "GET" }, { page, per_page: perPage });
    }

    async searchItems(query, page = 1) {
        return this._request("/items", { method: "GET" }, { search: query, page });
    }

    async getItemById(itemId) {
        const response = await this._request(`/items/${itemId}`, { method: "GET" });
        if (!response.success) return null;
        return response.data;
    }

    async uploadItem(itemData) {
        return this._request("/items", {
            method: "POST",
            headers: this._buildHeaders(true),
            body: JSON.stringify(itemData),
        });
    }

    // ===== USER PROFILE =====

    async getCurrentUser() {
        return this._request("/users/me", {
            headers: this._buildHeaders(false),
        });
    }

    async getUserProfile(userId) {
        return this._request(`/users/${userId}`, { method: "GET" });
    }

    async updateProfile(userId, data) {
        return this._request(`/users/${userId}`, {
            method: "PUT",
            headers: this._buildHeaders(true),
            body: JSON.stringify(data),
        });
    }

    // ===== SUSTAINABILITY IMPACT =====

    async getUserImpact(userId) {
        return this._request(`/impact/user/${userId}`, { method: "GET" });
    }

    async getGlobalImpact() {
        return this._request("/impact/summary", { method: "GET" });
    }

    async getLeaderboard(page = 1) {
        return this._request("/impact/leaderboard", { method: "GET" }, { page });
    }

    // ===== REQUESTS =====

    async createRequest(itemId, requestType, message = "", rentalDays = null, exchangeItemId = null) {
        return this._request("/requests", {
            method: "POST",
            headers: this._buildHeaders(true),
            body: JSON.stringify({
                item_id: itemId,
                request_type: requestType,
                message,
                rental_days: rentalDays,
                exchange_item_id: exchangeItemId,
            }),
        });
    }

    async getUserRequests(sortType = "sent", page = 1) {
        return this._request(
            `/requests/user/${sortType}`,
            { headers: this._buildHeaders(false) },
            { page }
        );
    }

    async updateRequest(requestId, status) {
        return this._request(`/requests/${requestId}`, {
            method: "PUT",
            headers: this._buildHeaders(true),
            body: JSON.stringify({ status }),
        });
    }

    // ===== ADMIN METHODS =====

    async getAdminDashboard() {
        return this._request("/admin/dashboard", {
            headers: this._buildHeaders(false),
        });
    }

    async moderateItem(itemId, action, reason = "") {
        return this._request(`/admin/items/${itemId}/moderate`, {
            method: "PUT",
            headers: this._buildHeaders(true),
            body: JSON.stringify({ action, reason }),
        });
    }

    async getReportedItems(page = 1) {
        return this._request("/admin/reported-items", {
            headers: this._buildHeaders(false),
        }, { page });
    }

    async manageUser(userId, action, reason = "") {
        return this._request(`/admin/users/${userId}/manage`, {
            method: "PUT",
            headers: this._buildHeaders(true),
            body: JSON.stringify({ action, reason }),
        });
    }

    async getAllRequests(page = 1, status = "", type = "") {
        return this._request("/admin/requests", {
            headers: this._buildHeaders(false),
        }, { page, status, request_type: type });
    }

    async getAllOrders(page = 1, status = "", type = "") {
        return this._request("/admin/orders", {
            headers: this._buildHeaders(false),
        }, { page, status, order_type: type });
    }

    // ===== UTILITY =====

    isAuthenticated() {
        return !!this._getToken();
    }

    getCurrentUserData() {
        const userData = localStorage.getItem("user");
        try {
            return userData ? JSON.parse(userData) : null;
        } catch (_error) {
            return null;
        }
    }

    async validateToken() {
        if (!this._getToken()) return false;
        const currentUser = this.getCurrentUserData();
        if (!currentUser) return false;

        const response = await this._request("/users/me", {
            method: "GET",
            headers: this._buildHeaders(false),
        });

        return !!response.success;
    }

    async checkAuthStatus() {
        if (!this.isAuthenticated()) return false;

        const isValid = await this.validateToken();
        if (!isValid) {
            this.logout();
            return false;
        }
        return true;
    }

    getHeaders() {
        return this._buildHeaders(true);
    }
}

const api = new APIClient();
