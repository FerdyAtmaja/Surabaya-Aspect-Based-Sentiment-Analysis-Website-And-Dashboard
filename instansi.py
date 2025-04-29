judul_topik = {
    1: "Kualitas Pelayanan Masyarakat",
    2: "Pengaduan dan Penyelesaian Keluhan",
    3: "Masalah Lingkungan di Masyarakat",
    4: "Proses Administrasi dan Informasi Publik",
    5: "Pelaporan dan Tindak Lanjut Masalah",
    6: "Kerusakan Fasilitas dan Infrastruktur",
    7: "Pendidikan dan Sekolah",
    8: "Keluhan Kebutuhan Lapangan Pekerjaan",
    9: "Permohonan Perbaikan Dan Pembaharuan",
    10: "Lamanya Proses Pengajuan",
    11: "Permintaan Dan Pendaftaran Administrasi",
    12: "Durasi dan Efisiensi Layanan",
    13: "Permasalahan Parkir",
    14: "Masalah Pohon dan Gangguan Lingkungan",
    15: "Pemimpin Wilayah yang Bermasalah",
    16: "Kondisi Fisik Lingkungan",
    17: "Permintaan Dan Pendaftaran"
}

instansi_mapping = {
    1: ["Dinas Kependudukan dan Pencatatan Sipil", "Dinas Perhubungan", "Dinas Sosial", "Dinas Pendidikan", "Dinas Lingkungan Hidup"],
    2: ["Dinas Komunikasi dan Informatika"],
    3: ["Dinas Lingkungan Hidup"],
    4: ["Bagian Umum Protokol dan Komunikasi Pimpinan", "Dinas Komunikasi dan Informatika"],
    5: ["Dinas Sosial", "Dinas Perhubungan"],
    6: ["Bagian Pengadaan Barang/Jasa dan Administrasi Pembangunan", "Dinas Perumahan Rakyat dan Kawasan Permukiman serta Pertanahan", "Dinas Sumber Daya Air dan Bina Marga"],
    7: ["Dinas Pendidikan"],
    8: ["Dinas Perindustrian dan Tenaga Kerja"],
    9: ["Bagian Pengadaan Barang/Jasa dan Administrasi Pembangunan", "Dinas Perumahan Rakyat dan Kawasan Permukiman serta Pertanahan"],
    10: ["Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu"],
    11: ["Dinas Komunikasi dan Informatika"],
    12: ["Dinas Penanaman Modal dan Pelayanan Terpadu Satu Pintu"],
    13: ["Dinas Perhubungan"],
    14: ["Dinas Lingkungan Hidup"],
    15: ["Badan Penanggulangan Bencana Daerah", "Dinas Lingkungan Hidup"],
    16: ["Dinas Perhubungan"],
    17: ["Dinas Kependudukan dan Pencatatan Sipil"]
}

def instansi_check(topik_id):
    if topik_id in instansi_mapping:
        return {
            "topik": judul_topik.get(topik_id, "Topik tidak ditemukan"),
            "instansi": instansi_mapping[topik_id]
        }
    else:
        return {"error": "ID topik tidak valid"}

# Contoh penggunaan
result = instansi_check(1)
print(result)
