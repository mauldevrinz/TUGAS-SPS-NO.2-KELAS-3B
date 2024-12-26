<?php
$host = "localhost"; // host MySQL
$username = "root";  // username MySQL (default untuk XAMPP)
$password = "";      // password MySQL (default untuk XAMPP)
$database = "sps_suara"; // nama database

// Membuat koneksi ke MySQL
$conn = new mysqli($host, $username, $password, $database);

// Cek koneksi
if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}
?>
