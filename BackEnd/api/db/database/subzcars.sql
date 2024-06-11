-- Users & Security Layer
CREATE TABLE UserType (
    user_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
);

CREATE TABLE User (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_type_id INTEGER,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    password TEXT,
    reset_token TEXT,
    first_name TEXT,
    last_name TEXT,
    birth_date DATETIME
);

CREATE TABLE Address(
	address_id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER,
	address_type TEXT,
	street TEXT,
	city TEXT,
	state TEXT,
	postal_code TEXT,
	FOREIGN KEY (user_id) REFERENCES Users(user_id)
);

-- Vehicles
CREATE TABLE VehicleManufacturer (
    vehicle_manufacturer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    country TEXT
);

CREATE TABLE VehicleModel (
    vehicle_model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_manufacturer_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    FOREIGN KEY (vehicle_manufacturer_id) REFERENCES VehicleManufacturers(vehicle_manufacturer_id)
);

CREATE TABLE VehicleType (
    vehicle_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE VehicleColor (
    vehicle_color_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

-- Subscription Models
CREATE TABLE PriceModel (
    price_model_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL
);

CREATE TABLE Vehicle (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_model_id INTEGER NOT NULL,
    vehicle_type_id INTEGER NOT NULL,
    vehicle_color_id INTEGER,
    price_model_id INTEGER,
    vin TEXT UNIQUE NOT NULL,
    year INTEGER,
    status TEXT,
    images TEXT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME,
    FOREIGN KEY (vehicle_model_id) REFERENCES VehicleModels(vehicle_model_id),
    FOREIGN KEY (vehicle_type_id) REFERENCES VehicleTypes(vehicle_type_id),
    FOREIGN KEY (vehicle_color_id) REFERENCES VehicleColors(vehicle_color_id),
    FOREIGN KEY (price_model_id) REFERENCES PriceModels(price_model_id)
);

-- Payment Gateways
CREATE TABLE PaymentGateway (
    gateway_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    implementation_details TEXT NOT NULL
);

-- Orders
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vehicle_id INTEGER,
    price REAL,
    status TEXT NOT NULL,
    gateway_id INTEGER,
    payment_status TEXT NOT NULL,
    start_date DATETIME NOT NULL,
    end_date DATETIME NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

CREATE TABLE CreditApplication(
 credit_id INTEGER PRIMARY KEY AUTOINCREMENT,
 order_id INTEGER NOT NULL,
 address_id INTEGER,
 first_name TEXT,
 last_name TEXT,
 birth_date DATETIME,
 marital_status TEXT,
 email TEXT,
 phone TEXT,
 TIN TEXT,
 FOREIGN KEY (order_id) REFERENCES Orders(order_id),
 FOREIGN KEY (address_id) REFERENCES Address(address_id)
);

CREATE TABLE Policy (
    policy_id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    policy_type TEXT,
    created_date DATETIME NOT NULL
);

-- Contracts & E-Sign
CREATE TABLE Contract (
    contract_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    order_id INTEGER NOT NULL,
    e_sign TEXT,
    sign_date DATETIME NOT NULL,
    status TEXT NOT NULL,
    policy_id INTEGER,
    policy TEXT,
    FOREIGN KEY (policy_id) REFERENCES Policy(policy_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Wishes
CREATE TABLE Wish(
    wish_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    vehicle_id INTEGER NOT NULL,
    created_at DATETIME NOT NULL,
    status TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);

-- Add any additional indexes or constraints as needed
-- For example, to speed up searches on commonly queried fields
CREATE INDEX idx_vehicle_vin ON Vehicle(vin);
CREATE INDEX idx_order_user ON Orders(user_id);
CREATE INDEX idx_wish_user_vehicle ON Wish(user_id, vehicle_id);