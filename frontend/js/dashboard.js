// ReWear - Dashboard Script

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

async function loadUserProfile() {
    try {
        const user = AuthHelper.getCurrentUser();
        if (!user) return;

        const profileCard = document.getElementById("profile-card");

        profileCard.innerHTML = `
            <div style="text-align: center; margin-bottom: 1rem;">
                <h3>${escapeHtml(user.full_name || "User")}</h3>
                <p style="color: #7f8c8d;">@${escapeHtml(user.username || "-")}</p>
                <p>${escapeHtml(user.email || "-")}</p>
            </div>
            <div style="text-align: center;">
                <a href="edit-profile.html" class="btn btn-sm btn-primary">Edit Profile</a>
                <button onclick="AuthHelper.logout()" class="btn btn-sm btn-outline">Logout</button>
            </div>
        `;
    } catch (_error) {
        UIUtils.showAlert("Error loading profile", "error");
    }
}

async function loadImpactSummary() {
    try {
        const user = AuthHelper.getCurrentUser();
        if (!user) return;

        const userId = user.id || user._id;
        const response = await api.getUserImpact(userId);

        if (response.success && response.data) {
            const data = response.data;
            const formatter = new Intl.NumberFormat("en-US");

            document.getElementById("impact-co2").textContent = `${formatter.format(Math.round(data.carbon_saved_kg || 0))} kg`;
            document.getElementById("impact-water").textContent = formatter.format(Math.round(data.water_saved_liters || 0));
            document.getElementById("impact-items").textContent =
                (data.total_items_reworn || 0) +
                (data.total_items_rented || 0) +
                (data.total_items_sold || 0) +
                (data.total_items_exchanged || 0);

            const scoreEl = document.getElementById("impact-points");
            if (scoreEl) scoreEl.textContent = Math.round(data.impact_score || 0);
        }
    } catch (error) {
        console.error("Error loading impact summary:", error);
    }
}

async function loadMyItems() {
    try {
        const user = AuthHelper.getCurrentUser();
        if (!user) return;

        const response = await api.getUserItems(user.id);

        if (response.success && response.data?.items) {
            const container = document.getElementById("my-items-list");
            const items = response.data.items.slice(0, 5);

            if (items.length === 0) {
                container.innerHTML = '<p style="color: #7f8c8d;">No items uploaded yet.</p>';
                return;
            }

            container.innerHTML = items
                .map(
                    (item) => `
                <div style="padding: 1rem; border-bottom: 1px solid #ecf0f1;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4>${escapeHtml(item.title || "Untitled")}</h4>
                            <p style="font-size: 0.9rem; color: #7f8c8d;">
                                ${escapeHtml(formatConditionBadge(item.condition))} • ${escapeHtml(item.category || "-")}
                            </p>
                        </div>
                        <div style="text-align: right;">
                            <span class="badge badge-info">${escapeHtml(item.status || "-")}</span>
                            ${item.price ? `<p style="color: #2ecc71; font-weight: bold;">${UIUtils.formatCurrency(item.price)}</p>` : ""}
                        </div>
                    </div>
                </div>
            `
                )
                .join("");
        }
    } catch (error) {
        console.error("Error loading items:", error);
    }
}

async function loadMyRequests() {
    try {
        const response = await api.getUserRequests("sent", 1);

        if (response.success && response.data?.requests) {
            const container = document.getElementById("my-requests-list");
            const requests = response.data.requests.slice(0, 5);

            if (requests.length === 0) {
                container.innerHTML = '<p style="color: #7f8c8d;">No requests made yet.</p>';
                return;
            }

            container.innerHTML = requests
                .map(
                    (req) => `
                <div style="padding: 1rem; border-bottom: 1px solid #ecf0f1;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="margin-bottom: 0.25rem;">${escapeHtml(req.item?.title || "Item")}</h4>
                            <p style="font-size: 0.9rem; color: #7f8c8d;">
                                ${escapeHtml(req.request_type || "-")} • ${UIUtils.formatDate(req.requested_at)}
                                ${req.exchange_item ? `<br><span style="color: var(--accent-green);">Offered: ${escapeHtml(req.exchange_item.title)}</span>` : ""}
                            </p>
                        </div>
                        <span class="badge" 
                              style="background-color: ${getStatusColor(req.status)}; color: white; padding: 0.2rem 0.5rem; border-radius: 4px;">
                            ${escapeHtml(req.status || "-")}
                        </span>
                    </div>
                </div>
            `
                )
                .join("");
        }
    } catch (error) {
        console.error("Error loading requests:", error);
    }
}

async function loadReceivedRequests() {
    try {
        const response = await api.getUserRequests("received", 1);

        if (response.success && response.data?.requests) {
            const container = document.getElementById("received-requests-list");
            const requests = response.data.requests.slice(0, 10);

            if (requests.length === 0) {
                container.innerHTML = '<p style="color: #7f8c8d;">No requests received yet.</p>';
                return;
            }

            container.innerHTML = requests
                .map(
                    (req) => `
                <div style="padding: 1rem; border-bottom: 1px solid #ecf0f1;">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div>
                            <h4 style="margin-bottom: 0.25rem;">${escapeHtml(req.item?.title || "Item")}</h4>
                            <p style="font-size: 0.9rem; color: #7f8c8d;">
                                From: <strong>${escapeHtml(req.requester?.username || "Unknown")}</strong>
                                ${req.exchange_item ? `<br><span style="color: var(--accent-green);">Offering: ${escapeHtml(req.exchange_item.title)}</span>` : ""}
                            </p>
                            <p style="font-size: 0.9rem; color: #7f8c8d;">
                                ${escapeHtml(req.request_type || "-")} • ${UIUtils.formatDate(req.requested_at)}
                            </p>
                            ${req.message ? `<p style="font-size: 0.9rem; margin-top: 0.5rem;">"${escapeHtml(req.message)}"</p>` : ""}
                        </div>
                        <div style="display: flex; gap: 0.5rem; flex-direction: column;">
                            ${
                                req.status === "pending"
                                    ? `
                                <button onclick="respondToRequest('${req.id}', 'accepted')" class="btn btn-sm btn-primary">Accept</button>
                                <button onclick="respondToRequest('${req.id}', 'rejected')" class="btn btn-sm btn-outline">Reject</button>
                            `
                                    : `<span class="badge badge-info">${escapeHtml(req.status || "-")}</span>`
                            }
                        </div>
                    </div>
                </div>
            `
                )
                .join("");
        }
    } catch (error) {
        console.error("Error loading received requests:", error);
    }
}

async function respondToRequest(requestId, action) {
    try {
        const response = await api.updateRequest(requestId, action);

        if (response.success) {
            UIUtils.showAlert(`Request ${action} successfully!`, "success");
            loadReceivedRequests();
            loadImpactSummary();
        } else {
            UIUtils.showAlert(response.message || "Error updating request", "error");
        }
    } catch (error) {
        UIUtils.showAlert("Error updating request", "error");
        console.error(error);
    }
}

function getStatusColor(status) {
    const colors = {
        pending: "#f39c12",
        accepted: "#2ecc71",
        rejected: "#e74c3c",
        completed: "#3498db",
        cancelled: "#95a5a6",
    };
    return colors[status] || "#bdc3c7";
}

document.addEventListener("DOMContentLoaded", async () => {
    await AuthHelper.redirectIfNotLoggedIn();
    AuthHelper.updateUserMenu();

    loadUserProfile();
    loadImpactSummary();
    loadMyItems();
    loadMyRequests();
    loadReceivedRequests();
});
