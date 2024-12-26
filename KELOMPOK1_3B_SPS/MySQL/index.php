<?php
// Koneksi ke database
$host = "localhost";
$user = "root";
$password = ""; // Ganti dengan password MySQL Anda
$database = "sps_suara";

// Membuat koneksi
$conn = new mysqli($host, $user, $password, $database);

// Periksa koneksi
if ($conn->connect_error) {
    die("Koneksi gagal: " . $conn->connect_error);
}

// Query untuk mendapatkan data dari tabel uploads
$sql = "SELECT * FROM uploads ORDER BY tanggal DESC";
$result = $conn->query($sql);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Uploads</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 20px;
        }
        table th, table td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }
        table th {
            background-color: #f2f2f2;
        }
        audio {
            margin: 5px 0;
        }
        img {
            max-width: 200px;
            height: auto;
        }
    </style>
</head>
<body>
    <h1>Daftar Uploads</h1>

    <?php if ($result->num_rows > 0): ?>
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Tanggal</th>
                    <th>Nama</th>
                    <th>Voice Recording</th>
                    <th>Realtime Grafik</th>
                    <th>DFT Grafik</th>
                </tr>
            </thead>
            <tbody>
                <?php while ($row = $result->fetch_assoc()): ?>
                    <tr>
                        <td><?php echo htmlspecialchars($row['id']); ?></td>
                        <td><?php echo htmlspecialchars($row['tanggal']); ?></td>
                        <td><?php echo htmlspecialchars($row['nama']); ?></td>
                        <td>
                            <audio controls>
                                <!-- Menampilkan file audio dengan jalur relatif -->
                                <source src="AUDIO RECORDER/<?php echo htmlspecialchars($row['voice_recording']); ?>.wav" type="audio/wav">
                                Your browser does not support the audio element.
                            </audio>
                        </td>
                        <td>
                            <!-- Menampilkan grafik realtime dengan jalur relatif -->
                            <img src="REALTIME GRAFIK/<?php echo htmlspecialchars($row['realtime_grafik']); ?>.png" alt="Realtime Grafik">
                        </td>
                        <td>
                            <!-- Menampilkan grafik DFT dengan jalur relatif -->
                            <img src="DFT GRAFIK/<?php echo htmlspecialchars($row['dft_grafik']); ?>.png" alt="DFT Grafik">
                        </td>
                    </tr>
                <?php endwhile; ?>
            </tbody>
        </table>
    <?php else: ?>
        <p>Tidak ada data tersedia.</p>
    <?php endif; ?>

    <?php $conn->close(); ?>
</body>
</html>
