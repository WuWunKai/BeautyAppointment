-- 創建資料庫
CREATE DATABASE IF NOT EXISTS BeautyAppointmentSystem;

-- 使用資料庫
USE BeautyAppointmentSystem;

-- 使用者資料表
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `line_user_id` varchar(50) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `line_user_id` (`line_user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- 店家資料表
CREATE TABLE `Stores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `store_name` varchar(100) NOT NULL,
  `ig` varchar(100) DEFAULT NULL,
  `facebook` varchar(100) DEFAULT NULL,
  `tiktok` varchar(100) DEFAULT NULL,
  `description` text,
  `channel_id` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `channel_secret` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
  `channel_access_token` varchar(255) DEFAULT NULL,
  `liff_id` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

CREATE TABLE `user_store_memberships` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `store_id` int NOT NULL,
  `is_blacklisted` tinyint(1) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  KEY `store_id` (`store_id`),
  CONSTRAINT `user_store_memberships_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  CONSTRAINT `user_store_memberships_ibfk_2` FOREIGN KEY (`store_id`) REFERENCES `stores` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 服務資料表
CREATE TABLE Services (
    ServiceID INT PRIMARY KEY AUTO_INCREMENT COMMENT '服務ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    ServiceName VARCHAR(100) NOT NULL COMMENT '服務名稱',
    Description TEXT COMMENT '服務描述',
    Price DECIMAL(10, 2) NOT NULL COMMENT '服務價格',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '服務創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
) COMMENT '店家提供的服務';


-- 預約資料表
CREATE TABLE Appointments (
    AppointmentID INT PRIMARY KEY AUTO_INCREMENT COMMENT '預約ID',
    UserID INT NOT NULL COMMENT '使用者ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    ServiceID INT NOT NULL COMMENT '服務ID',
    AppointmentTime DATETIME NOT NULL COMMENT '預約時間',
    Status ENUM('已預約', '已完成', '取消') DEFAULT '已預約' COMMENT '預約狀態',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '預約創建時間',
    FOREIGN KEY (UserID) REFERENCES Users(UserID),
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (ServiceID) REFERENCES Services(ServiceID)
) COMMENT '預約資料';

-- 商品分類資料表
CREATE TABLE ProductCategories (
    CategoryID INT PRIMARY KEY AUTO_INCREMENT COMMENT '類別ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    CategoryName VARCHAR(100) NOT NULL COMMENT '類別名稱',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '類別創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
) COMMENT '商品分類資料';

-- 商品資料表
CREATE TABLE Products (
    ProductID INT PRIMARY KEY AUTO_INCREMENT COMMENT '商品ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    ProductName VARCHAR(100) NOT NULL COMMENT '商品名稱',
    Description TEXT COMMENT '商品描述',
    Price DECIMAL(10, 2) NOT NULL COMMENT '商品價格',
    CategoryID INT COMMENT '商品類別ID',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '商品創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (CategoryID) REFERENCES ProductCategories(CategoryID)
) COMMENT '店家商品資料';



-- 服務人員資料表
CREATE TABLE Staff (
    StaffID INT PRIMARY KEY AUTO_INCREMENT COMMENT '服務人員ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    Name VARCHAR(100) NOT NULL COMMENT '服務人員名稱',
    Position VARCHAR(100) COMMENT '職位',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '服務人員創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
) COMMENT '店家服務人員資料';

-- 每日預約資料表
CREATE TABLE DailyAppointments (
    DailyAppointmentID INT PRIMARY KEY AUTO_INCREMENT COMMENT '每日預約ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    AppointmentDate DATE NOT NULL COMMENT '預約日期',
    AvailableSlots INT NOT NULL COMMENT '可用時段',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '每日預約創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
) COMMENT '每日預約資料';

-- 會員資料表
CREATE TABLE Members (
    MemberID INT PRIMARY KEY AUTO_INCREMENT COMMENT '會員ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    UserID INT NOT NULL COMMENT '使用者ID',
    IsBlacklisted BOOLEAN DEFAULT FALSE COMMENT '是否列入黑名單',
    Birthday DATE COMMENT '生日',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '會員創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
) COMMENT '會員資料';

-- 店家休假日資料表
CREATE TABLE StoreHolidays (
    HolidayID INT PRIMARY KEY AUTO_INCREMENT COMMENT '休假日ID',
    StoreID INT NOT NULL COMMENT '店家ID',
    HolidayDate DATE NOT NULL COMMENT '休假日期',
    Description VARCHAR(255) COMMENT '休假描述',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '休假日創建時間',
    FOREIGN KEY (StoreID) REFERENCES Stores(StoreID)
) COMMENT '店家休假日資料';

-- 平台管理員資料表
CREATE TABLE Admins (
    AdminID INT PRIMARY KEY AUTO_INCREMENT COMMENT '管理員ID',
    Username VARCHAR(50) NOT NULL UNIQUE COMMENT '管理員用戶名',
    PasswordHash VARCHAR(255) NOT NULL COMMENT '密碼哈希值',
    CreatedAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '管理員創建時間'
) COMMENT '平台管理員資料';