// ReWear - Browse Items Script

let currentPage = 1;
let currentFilters = {};

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

async function loadItems(page = 1) {
    try {
        UIUtils.showLoader(document.getElementById("items-container"));

        const response = await api.getItems(page, currentFilters);

        if (response.success && response.data?.items) {
            displayItems(response.data.items);
            updatePagination(response.data.pagination || { pages: 1 }, page);
            currentPage = page;
            return;
        }

        document.getElementById("items-container").innerHTML =
            '<p class="text-center" style="grid-column: 1/-1; margin-top: 2rem;">No items found.</p>';
        const paginationDiv = document.getElementById("pagination");
        if (paginationDiv) paginationDiv.innerHTML = "";
    } catch (error) {
        UIUtils.showAlert("Error loading items", "error");
        console.error("Frontend Error:", error);
    }
}

function displayItems(items) {
    const container = document.getElementById("items-container");

    if (!items || items.length === 0) {
        container.innerHTML = '<p class="text-center" style="grid-column: 1/-1;">No items found.</p>';
        return;
    }

    container.innerHTML = items
        .map((item) => {
            const title = escapeHtml(UIUtils.truncateText(item.title || "Untitled", 50));
            const category = escapeHtml((item.category || "other").toUpperCase());
            const imageUrl = escapeHtml(item.image_url || "https://via.placeholder.com/250x200?text=No+Image");
            const alt = escapeHtml(item.title || "Item image");

            return `
        <div class="item-card" onclick="viewItem('${item.id}')">
            <div style="height: 200px; background-color: #ecf0f1; display: flex; align-items: center; justify-content: center;">
                <img src="${imageUrl}" 
                     alt="${alt}" 
                     style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <div class="item-content">
                <h3 class="item-title">${title}</h3>
                <span class="item-category">${category}</span>
                ${item.price ? `<div class="item-price">${UIUtils.formatCurrency(item.price)}</div>` : ""}
                <p class="item-condition">${formatConditionBadge(item.condition)}</p>
                <div class="item-actions">
                    <button class="btn btn-sm btn-primary" onclick="event.stopPropagation(); viewItem('${item.id}')">View Details</button>
                    <button class="btn btn-sm btn-secondary" onclick="event.stopPropagation(); requestItem('${item.id}')">Request</button>
                </div>
            </div>
        </div>
    `;
        })
        .join("");
}

function updatePagination(pagination, page) {
    const paginationDiv = document.getElementById("pagination");

    if (!pagination?.pages || pagination.pages <= 1) {
        paginationDiv.innerHTML = "";
        return;
    }

    let html = "";

    if (pagination.has_prev) {
        html += `<button onclick="loadItems(${page - 1})">&larr; Previous</button>`;
    }

    for (let i = 1; i <= pagination.pages && i <= 5; i += 1) {
        if (i === page) {
            html += `<span class="active">${i}</span>`;
        } else {
            html += `<button onclick="loadItems(${i})">${i}</button>`;
        }
    }

    if (pagination.has_next) {
        html += `<button onclick="loadItems(${page + 1})">Next &rarr;</button>`;
    }

    paginationDiv.innerHTML = html;
}

function applyFilters() {
    currentFilters = {
        category: document.getElementById("filter-category").value,
        condition: document.getElementById("filter-condition").value,
        transaction_type: document.getElementById("filter-type").value,
    };

    loadItems(1);
}

async function searchItems() {
    const query = document.getElementById("search-input").value.trim();

    if (query.length < 2) {
        UIUtils.showAlert("Enter at least 2 characters to search", "warning");
        return;
    }

    try {
        UIUtils.showLoader(document.getElementById("items-container"));

        const response = await api.searchItems(query, 1);

        if (response.success && response.data?.items) {
            displayItems(response.data.items);
            updatePagination(response.data.pagination || { pages: 1 }, 1);
        } else {
            document.getElementById("items-container").innerHTML =
                '<p class="text-center">No items found matching your search.</p>';
        }
    } catch (error) {
        UIUtils.showAlert("Error searching items", "error");
        console.error(error);
    }
}

async function viewItem(itemId) {
    try {
        const item = await api.getItemById(itemId);

        if (item && item.id) {
            const modalBody = document.getElementById("modal-body");
            const isExchange = item.transaction_type === "exchange";

            modalBody.innerHTML = `
                <div class="row">
                    <div class="col-6">
                        <img src="${escapeHtml(item.image_url || "https://via.placeholder.com/400x400?text=No+Image")}" 
                             alt="${escapeHtml(item.title || "Item image")}" 
                             style="width: 100%; border-radius: 8px;">
                    </div>
                    <div class="col-6">
                        <h3>${escapeHtml(item.title || "Untitled")}</h3>
                        <p><strong>Category:</strong> ${escapeHtml(item.category || "-")}</p>
                        <p><strong>Size:</strong> ${escapeHtml(item.size || "-")}</p>
                        <p><strong>Condition:</strong> ${formatConditionBadge(item.condition)}</p>
                        <p><strong>Brand:</strong> ${escapeHtml(item.brand || "Unknown")}</p>
                        ${item.price ? `<p><strong>Price:</strong> ${UIUtils.formatCurrency(item.price)}</p>` : ""}
                        <div class="mt-3">
                            <p><strong>Seller ID:</strong> ${escapeHtml(item.owner_id || "-")}</p>
                        </div>
                        <div style="margin-top: 1.5rem;">
                            ${AuthHelper.isLoggedIn() ? `
                                ${isExchange ? `
                                    <div id="exchange-offer-wrapper" style="margin-bottom: 0.75rem;">
                                        <label for="offered-item" style="display: block; margin-bottom: 0.35rem; font-weight: 600;">
                                            Offer Your Item
                                        </label>
                                        <select id="offered-item">
                                            <option value="">Loading your items...</option>
                                        </select>
                                        <small id="exchange-offer-help" style="color: var(--text-secondary); display: block; margin-top: 0.3rem;"></small>
                                    </div>
                                ` : ""}
                                <button onclick="makeRequest('${item.id}', '${item.transaction_type}')" class="btn btn-primary btn-block">
                                    Send ${(item.transaction_type || "request").toUpperCase()} Request
                                </button>
                            ` : `
                                <p class="text-center"><a href="/login.html" class="btn btn-primary">Login to contact seller</a></p>
                            `}
                        </div>
                    </div>
                </div>
                <div class="mt-4">
                    <h4>Description</h4>
                    <p style="color: var(--text-secondary);">${escapeHtml(item.description || "No description provided.")}</p>
                </div>
            `;

            document.getElementById("item-modal").classList.add("active");

            if (isExchange && AuthHelper.isLoggedIn()) {
                await loadExchangeOfferOptions(item.id);
            }
        } else {
            UIUtils.showAlert("Item details not found", "error");
        }
    } catch (error) {
        UIUtils.showAlert("Error loading item details", "error");
        console.error("View Details Error:", error);
    }
}

async function loadExchangeOfferOptions(targetItemId) {
    const select = document.getElementById("offered-item");
    const helpText = document.getElementById("exchange-offer-help");
    const currentUser = AuthHelper.getCurrentUser();

    if (!select || !currentUser) return;

    const response = await api.getUserItems(currentUser.id, 1, 100);
    if (!response.success || !response.data?.items) {
        select.innerHTML = '<option value="">Unable to load your items</option>';
        if (helpText) helpText.textContent = "Could not load your available items.";
        return;
    }

    const availableItems = response.data.items.filter(
        (userItem) => userItem.status === "available" && userItem.id !== targetItemId
    );

    if (availableItems.length === 0) {
        select.innerHTML = '<option value="">No available items to offer</option>';
        if (helpText) helpText.textContent = "Upload an available item first to make an exchange request.";
        return;
    }

    select.innerHTML =
        '<option value="">Select an item to offer</option>' +
        availableItems
            .map(
                (userItem) =>
                    `<option value="${userItem.id}">${escapeHtml(userItem.title || "Untitled")} (${escapeHtml(userItem.category || "item")})</option>`
            )
            .join("");

    if (helpText) helpText.textContent = `${availableItems.length} available item(s) found.`;
}

function toggleContactForm() {
    const form = document.getElementById("contact-owner-form");
    form.style.display = form.style.display === "none" ? "block" : "none";
}

async function sendInitialMessage(ownerId, itemId) {
    const content = document.getElementById("quick-msg-input").value.trim();
    if (!content) {
        UIUtils.showAlert("Please type a message first.", "warning");
        return;
    }

    try {
        const response = await fetch(`${api.baseURL}/messages`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${localStorage.getItem("access_token")}`,
            },
            body: JSON.stringify({
                receiver_id: ownerId,
                item_id: itemId,
                content,
            }),
        });

        if (response.ok) {
            UIUtils.showAlert("Message sent! Redirecting to your inbox...", "success");
            setTimeout(() => {
                window.location.href = "dashboard.html";
            }, 1000);
        } else {
            UIUtils.showAlert("Failed to send message. Please try again.", "error");
        }
    } catch (error) {
        console.error("Messaging error:", error);
        UIUtils.showAlert("An error occurred while sending the message.", "error");
    }
}

function closeModal() {
    document.getElementById("item-modal").classList.remove("active");
}

function requestItem(itemId) {
    if (!AuthHelper.isLoggedIn()) {
        UIUtils.showAlert("Please login to make a request", "info");
        return;
    }
    viewItem(itemId);
}

async function makeRequest(itemId, requestType) {
    if (!AuthHelper.isLoggedIn()) {
        UIUtils.showAlert("Please login first", "warning");
        return;
    }

    try {
        const message = prompt(`Enter a message for your ${requestType} request (optional):`);
        let rentalDays = null;

        if (requestType === "rent") {
            rentalDays = parseInt(prompt("How many days would you like to rent?", "7"), 10);
            if (!rentalDays || rentalDays < 1) {
                UIUtils.showAlert("Invalid number of days", "error");
                return;
            }
        }

        let exchangeItemId = null;
        if (requestType === "exchange") {
            const select = document.getElementById("offered-item");
            exchangeItemId = select ? select.value : null;
            if (!exchangeItemId) {
                UIUtils.showAlert("Please select an item to offer in exchange", "warning");
                return;
            }
        }

        const response = await api.createRequest(itemId, requestType, message || "", rentalDays, exchangeItemId);

        if (response.success) {
            UIUtils.showAlert(`${requestType.charAt(0).toUpperCase() + requestType.slice(1)} request created successfully!`, "success");
            closeModal();
            setTimeout(() => {
                window.location.href = "/dashboard.html";
            }, 1500);
        } else {
            UIUtils.showAlert(response.message || "Error creating request", "error");
        }
    } catch (error) {
        UIUtils.showAlert("Error creating request", "error");
        console.error(error);
    }
}

document.addEventListener("DOMContentLoaded", () => {
    if (typeof AuthHelper !== "undefined") AuthHelper.updateUserMenu();
    loadItems(1);
});

const modal = document.getElementById("item-modal");
if (modal) {
    modal.addEventListener("click", (e) => {
        if (e.target.id === "item-modal") {
            closeModal();
        }
    });
}

function formatConditionBadge(condition) {
    const normalized = (condition || "unknown").toLowerCase();
    const colors = {
        new: "#2ecc71",
        like_new: "#3498db",
        good: "#f1c40f",
        fair: "#e67e22",
        worn: "#e74c3c",
    };
    const color = colors[normalized] || "#95a5a6";
    const label = escapeHtml(normalized.replace("_", " ").toUpperCase());
    return `<span style="background-color: ${color}; color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem;">${label}</span>`;
}
