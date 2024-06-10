-- Tabel Seller
CREATE TABLE Seller (
    seller_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    seller_name VARCHAR(255),
    seller_description TEXT,
    seller_location POINT, -- Gunakan tipe data geometri untuk koordinat lokasi
    seller_address VARCHAR(255),
    seller_cuisine VARCHAR(255),
    seller_specialty TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);

-- Tabel Product (Sesuaikan dengan kebutuhan "Global Bites")
CREATE TABLE Product (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    seller_id INT,
    product_name VARCHAR(255),
    product_description TEXT,
    product_category VARCHAR(255),
    product_price DECIMAL(10,2),
    product_stock INT,
    product_unit VARCHAR(20),
    product_image VARCHAR(255),
    product_recipe TEXT,
    product_ingredients TEXT,
    product_allergies TEXT,
    product_availability JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (seller_id) REFERENCES Seller(seller_id)
);

-- Tabel lainnya (Order, Order_Item, Payment, Shipping, Review, Promo, Courier) 
-- Sama seperti yang dibuat di skema database untuk "Fresh & Local" 
