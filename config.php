<?php
// Config for SSKRU Map PHP Application (MySQL / phpMyAdmin Connection)
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type, Authorization');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

$db_host = '127.0.0.1';
$db_port = 3306;
$db_user = 'root';
$db_pass = '';
$db_name = 'sskru_map';

try {
    $pdo = new PDO("mysql:host=$db_host;port=$db_port;charset=utf8mb4", $db_user, $db_pass, [
        PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
        PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC
    ]);
    
    // Ensure database exists
    $pdo->exec("CREATE DATABASE IF NOT EXISTS `$db_name` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;");
    $pdo->exec("USE `$db_name`;");
    
    // Ensure table exists
    $create_table_sql = "
    CREATE TABLE IF NOT EXISTS buildings (
        id INT PRIMARY KEY,
        code VARCHAR(20),
        name VARCHAR(255) NOT NULL,
        nameEn VARCHAR(255),
        category VARCHAR(50),
        coords_y INT,
        coords_x INT,
        real_lat DOUBLE,
        real_lng DOUBLE,
        description TEXT,
        phone VARCHAR(100),
        json_data TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ";
    $pdo->exec($create_table_sql);
} catch (PDOException $e) {
    http_response_code(500);
    echo json_encode(['success' => false, 'message' => 'Database connection failed: ' . $e->getMessage()]);
    exit();
}
