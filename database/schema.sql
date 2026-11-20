-- ============================================
-- ReWear Clothing System - Database Schema
-- ============================================
-- This SQL schema creates all necessary tables
-- for the ReWear sustainable fashion platform

-- ============================================
-- 1. USERS TABLE
-- ============================================
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    mobile VARCHAR(15),
    address TEXT,
    profile_image_url VARCHAR(255),
    bio TEXT,
    role ENUM('user', 'admin') DEFAULT 'user',
    
    -- Sustainability Metrics
    carbon_saved_kg DECIMAL(10, 2) DEFAULT 0,
    water_saved_liters DECIMAL(15, 2) DEFAULT 0,
    items_reworn INT DEFAULT 0,
    items_rented INT DEFAULT 0,
    items_sold INT DEFAULT 0,
    reputation_score INT DEFAULT 0,
    
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_role (role)
);

-- ============================================
-- 2. CLOTHING_ITEMS TABLE
-- ============================================
CREATE TABLE clothing_items (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    
    -- Item Details
    title VARCHAR(100) NOT NULL,
    description TEXT,
    category ENUM('tops', 'bottoms', 'dresses', 'outerwear', 'footwear', 'accessories') NOT NULL,
    size VARCHAR(10) NOT NULL,
    color VARCHAR(50),
    brand VARCHAR(50),
    
    -- Condition & Status
    condition ENUM('new', 'like_new', 'good', 'fair', 'worn') NOT NULL,
    rewear_count INT DEFAULT 0,
    
    -- Transaction Details
    transaction_type ENUM('rent', 'sell', 'exchange', 'free') NOT NULL,
    price DECIMAL(10, 2),
    rental_price_per_day DECIMAL(8, 2),
    
    -- Media
    image_url VARCHAR(255),
    
    -- Availability
    status ENUM('available', 'rented', 'sold', 'exchanged', 'inactive') DEFAULT 'available',
    
    -- Sustainability Impact
    carbon_impact_kg DECIMAL(8, 2) DEFAULT 0,
    water_impact_liters DECIMAL(12, 2) DEFAULT 0,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_transaction_type (transaction_type),
    FULLTEXT INDEX ftx_search (title, description)
);

-- ============================================
-- 3. REQUESTS TABLE
-- ============================================
CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    item_id INTEGER NOT NULL,
    requester_id INTEGER NOT NULL,
    owner_id INTEGER NOT NULL,
    
    -- Request Type
    request_type ENUM('rent', 'buy', 'exchange', 'gift') NOT NULL,
    
    -- Status Tracking
    status ENUM('pending', 'accepted', 'rejected', 'cancelled', 'completed') DEFAULT 'pending',
    
    -- Details
    message TEXT,
    rental_days INT,
    exchange_item_id INTEGER,
    
    -- Dates
    requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP NULL,
    completed_at TIMESTAMP NULL,
    
    FOREIGN KEY (item_id) REFERENCES clothing_items(id) ON DELETE CASCADE,
    FOREIGN KEY (requester_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (exchange_item_id) REFERENCES clothing_items(id),
    
    INDEX idx_item_id (item_id),
    INDEX idx_requester_id (requester_id),
    INDEX idx_owner_id (owner_id),
    INDEX idx_status (status),
    INDEX idx_request_type (request_type)
);

-- ============================================
-- 4. ORDERS TABLE
-- ============================================
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    request_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    buyer_id INTEGER NOT NULL,
    seller_id INTEGER NOT NULL,
    
    -- Transaction Details
    order_type ENUM('purchase', 'rental', 'exchange') NOT NULL,
    total_amount DECIMAL(10, 2),
    commission DECIMAL(8, 2) DEFAULT 0,
    
    -- Status
    status ENUM('pending', 'confirmed', 'shipped', 'delivered', 'returned', 'cancelled') DEFAULT 'pending',
    
    -- Shipping Details
    delivery_address TEXT NOT NULL,
    tracking_number VARCHAR(50),
    
    -- Dates
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shipped_date TIMESTAMP NULL,
    delivered_date TIMESTAMP NULL,
    return_date TIMESTAMP NULL,
    
    FOREIGN KEY (request_id) REFERENCES requests(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES clothing_items(id),
    FOREIGN KEY (buyer_id) REFERENCES users(id),
    FOREIGN KEY (seller_id) REFERENCES users(id),
    
    INDEX idx_buyer_id (buyer_id),
    INDEX idx_seller_id (seller_id),
    INDEX idx_status (status),
    INDEX idx_order_date (order_date)
);

-- ============================================
-- 5. IMPACT_METRICS TABLE
-- ============================================
CREATE TABLE impact_metrics (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    item_id INTEGER,
    
    -- Action Type
    action_type ENUM('item_reworn', 'item_rented', 'item_sold', 'item_exchanged') NOT NULL,
    
    -- Impact Data
    co2_reduced_kg DECIMAL(8, 2) NOT NULL,
    water_saved_liters DECIMAL(12, 2) NOT NULL,
    textile_waste_prevented_kg DECIMAL(8, 2) DEFAULT 0,
    
    -- Timestamp
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES clothing_items(id) ON DELETE SET NULL,
    
    INDEX idx_user_id (user_id),
    INDEX idx_created_at (created_at)
);

-- ============================================
-- 6. REVIEWS TABLE
-- ============================================
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    reviewer_id INTEGER NOT NULL,
    reviewed_user_id INTEGER NOT NULL,
    order_id INTEGER,
    
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5),
    review_text TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (reviewer_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewed_user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE SET NULL,
    
    INDEX idx_reviewed_user_id (reviewed_user_id),
    INDEX idx_reviewer_id (reviewer_id)
);

-- ============================================
-- 7. WISHLIST TABLE
-- ============================================
CREATE TABLE wishlist (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES clothing_items(id) ON DELETE CASCADE,
    
    UNIQUE KEY unique_wishlist (user_id, item_id),
    INDEX idx_user_id (user_id)
);

-- ============================================
-- 8. NOTIFICATIONS TABLE
-- ============================================
CREATE TABLE notifications (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    notification_type ENUM('order', 'request', 'message', 'system') DEFAULT 'system',
    is_read BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_is_read (is_read)
);

-- ============================================
-- INDEXES FOR PERFORMANCE
-- ============================================
CREATE INDEX idx_items_created ON clothing_items(created_at);
CREATE INDEX idx_requests_created ON requests(requested_at);
CREATE INDEX idx_orders_created ON orders(order_date);
CREATE INDEX idx_impact_created ON impact_metrics(created_at);

-- ============================================
-- VIEW: User Summary Statistics
-- ============================================
CREATE VIEW user_statistics AS
SELECT 
    u.id,
    u.username,
    u.email,
    COUNT(DISTINCT ci.id) as total_items,
    COUNT(DISTINCT CASE WHEN ci.status = 'available' THEN ci.id END) as available_items,
    SUM(CASE WHEN r.status = 'completed' THEN 1 ELSE 0 END) as completed_requests,
    u.carbon_saved_kg,
    u.water_saved_liters,
    u.reputation_score
FROM users u
LEFT JOIN clothing_items ci ON u.id = ci.user_id
LEFT JOIN requests r ON u.id = r.owner_id OR u.id = r.requester_id
GROUP BY u.id;

-- ============================================
-- VIEW: Sustainability Dashboard
-- ============================================
CREATE VIEW sustainability_dashboard AS
SELECT 
    SUM(im.co2_reduced_kg) as total_co2_reduced_kg,
    SUM(im.water_saved_liters) as total_water_saved_liters,
    SUM(im.textile_waste_prevented_kg) as total_textile_waste_prevented_kg,
    COUNT(DISTINCT im.user_id) as active_users,
    COUNT(DISTINCT im.item_id) as items_involved,
    DATE(im.created_at) as date
FROM impact_metrics im
GROUP BY DATE(im.created_at);

-- ============================================
-- SAMPLE DATA FOR TESTING
-- ============================================
-- Insert test users
INSERT INTO users (username, email, password_hash, full_name, mobile, address, role, carbon_saved_kg, water_saved_liters, items_reworn)
VALUES 
    ('john_eco', 'john@rewear.com', 'hashed_password_1', 'John Eco', '9876543210', '123 Green St', 'user', 15.5, 35000, 5),
    ('jane_sustainable', 'jane@rewear.com', 'hashed_password_2', 'Jane Sustainable', '9876543211', '456 Blue Ave', 'user', 22.3, 49000, 7),
    ('admin_rewear', 'admin@rewear.com', 'hashed_password_admin', 'Admin ReWear', '9876543212', '789 Admin Rd', 'admin', 0, 0, 0);

-- Insert test clothing items
INSERT INTO clothing_items (user_id, title, description, category, size, color, brand, condition, rewear_count, transaction_type, price, rental_price_per_day, image_url, status, carbon_impact_kg, water_impact_liters)
VALUES 
    (1, 'Blue Denim Jacket', 'Classic blue denim jacket in excellent condition', 'outerwear', 'M', 'Blue', 'Levi', 'like_new', 2, 'rent', 50.00, 5.00, '/images/jacket1.jpg', 'available', 6.00, 14000),
    (1, 'White Cotton T-Shirt', 'Comfortable white cotton t-shirt', 'tops', 'M', 'White', 'H&M', 'good', 3, 'sell', 15.00, NULL, '/images/tshirt1.jpg', 'available', 9.00, 21000),
    (2, 'Black Formal Pants', 'Professional black formal pants', 'bottoms', 'S', 'Black', 'Zara', 'like_new', 1, 'exchange', NULL, NULL, '/images/pants1.jpg', 'available', 3.00, 7000);
-- Messages table for Peer-to-Peer communication
CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    item_id INTEGER, -- Optional: helps know which item the chat is about
    content TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    FOREIGN KEY (sender_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id),
    FOREIGN KEY (item_id) REFERENCES clothing_items (id)
);