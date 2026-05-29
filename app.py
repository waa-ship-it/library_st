import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime, timedelta

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Libraverse Pro",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# CSS MODERN
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #F5F7FB;
}

.header-box {
    background: linear-gradient(to right, #667eea, #764ba2);
    padding: 35px;
    border-radius: 25px;
    color: white;
    margin-bottom: 30px;
}

.book-card {
    background: white;
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# DATABASE
# =========================================================

conn = sqlite3.connect(
    "library.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================================
# TABEL BUKU
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (

    kode TEXT PRIMARY KEY,
    judul TEXT,
    penulis TEXT,
    kategori TEXT,
    tahun INTEGER,
    rating REAL,
    status TEXT

)
""")

# =========================================================
# TABEL PEMINJAMAN
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS peminjaman (

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT,
    kode_buku TEXT,
    judul TEXT,
    tanggal_pinjam TEXT,
    batas_kembali TEXT,
    tanggal_kembali TEXT,
    status TEXT,
    denda INTEGER

)
""")

conn.commit()

# =========================================================
# DATA AWAL
# =========================================================

def insert_default_books():

    cursor.execute("SELECT COUNT(*) FROM books")

    total = cursor.fetchone()[0]

    if total == 0:

        books = [

            (
                "BK001",
                "Atomic Habits",
                "James Clear",
                "Self Improvement",
                2018,
                4.9,
                "Tersedia"
            ),

            (
                "BK002",
                "Mariposa",
                "Luluk HF",
                "Romance",
                2018,
                4.8,
                "Tersedia"
            ),

            (
                "BK003",
                "The Psychology of Money",
                "Morgan Housel",
                "Nonfiksi",
                2020,
                4.9,
                "Tersedia"
            ),

            (
                "BK004",
                "Eccedentesiast",
                "itakrn",
                "Fiksi",
                2022,
                4.9,
                "Tersedia"
            )

        ]

        cursor.executemany(
            "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
            books
        )

        conn.commit()

insert_default_books()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Libraverse Pro")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [

        "🏠 Home",
        "📚 Koleksi Buku",
        "➕ Tambah Buku",
        "✏️ Update Buku",
        "🗑️ Hapus Buku",
        "📖 Pinjam Buku",
        "📥 Kembalikan Buku",
        "📋 Data Peminjaman",
        "🔍 Cari Buku",
        "📊 Statistik"

    ]
)

# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.markdown("""
    <div class="header-box">

    <h1>📚 Libraverse Pro</h1>

    <p>
    Sistem Manajemen Perpustakaan Modern
    </p>

    </div>
    """, unsafe_allow_html=True)

    total_buku = pd.read_sql_query(
        "SELECT * FROM books",
        conn
    )

    total_pinjam = pd.read_sql_query(
        "SELECT * FROM peminjaman WHERE status='Dipinjam'",
        conn
    )

    tersedia = pd.read_sql_query(
        "SELECT * FROM books WHERE status='Tersedia'",
        conn
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Total Buku",
            len(total_buku)
        )

    with col2:
        st.metric(
            "📖 Sedang Dipinjam",
            len(total_pinjam)
        )

    with col3:
        st.metric(
            "🟢 Buku Tersedia",
            len(tersedia)
        )

    st.markdown("---")

    st.subheader("🔥 Buku Populer")

    st.markdown("""
    <div class="book-card">

    <h3>📖 Atomic Habits</h3>

    <p>✍️ James Clear</p>

    <p>⭐ 4.9</p>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# KOLEKSI BUKU
# =========================================================

elif menu == "📚 Koleksi Buku":

    st.title("📚 Koleksi Buku")

    data = pd.read_sql_query(
        "SELECT * FROM books",
        conn
    )

    kategori = st.selectbox(
        "Filter Kategori",
        [
            "Semua",
            "Romance",
            "Fiksi",
            "Nonfiksi",
            "Self Improvement"
        ]
    )

    if kategori != "Semua":

        data = data[
            data["kategori"] == kategori
        ]

    for _, buku in data.iterrows():

        warna = "🟢" if buku["status"] == "Tersedia" else "🔴"

        st.markdown(f"""
        <div class="book-card">

        <h3>📖 {buku['judul']}</h3>

        <p>✍️ {buku['penulis']}</p>

        <p>📚 {buku['kategori']}</p>

        <p>📅 {buku['tahun']}</p>

        <p>⭐ {buku['rating']}</p>

        <p>{warna} {buku['status']}</p>

        <p>🆔 {buku['kode']}</p>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAMBAH BUKU
# =========================================================

elif menu == "➕ Tambah Buku":

    st.title("➕ Tambah Buku")

    kode = st.text_input("Kode Buku")

    judul = st.text_input("Judul Buku")

    penulis = st.text_input("Penulis")

    kategori = st.selectbox(
        "Kategori",
        [
            "Romance",
            "Fiksi",
            "Nonfiksi",
            "Self Improvement"
        ]
    )

    tahun = st.number_input(
        "Tahun",
        2000,
        2030
    )

    rating = st.slider(
        "Rating",
        1.0,
        5.0,
        4.0
    )

    if st.button("Tambah Buku"):

        try:

            cursor.execute("""
            INSERT INTO books
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (

                kode,
                judul,
                penulis,
                kategori,
                tahun,
                rating,
                "Tersedia"

            ))

            conn.commit()

            st.success("✅ Buku berhasil ditambahkan")

            st.balloons()

        except:
            st.error("❌ Kode buku sudah ada")

# =========================================================
# UPDATE BUKU
# =========================================================

elif menu == "✏️ Update Buku":

    st.title("✏️ Update Buku")

    kode = st.text_input("Masukkan kode buku")

    judul = st.text_input("Judul baru")

    penulis = st.text_input("Penulis baru")

    kategori = st.selectbox(
        "Kategori baru",
        [
            "Romance",
            "Fiksi",
            "Nonfiksi",
            "Self Improvement"
        ]
    )

    tahun = st.number_input(
        "Tahun baru",
        2000,
        2030
    )

    rating = st.slider(
        "Rating baru",
        1.0,
        5.0,
        4.0
    )

    if st.button("Update"):

        cursor.execute("""
        UPDATE books
        SET

            judul=?,
            penulis=?,
            kategori=?,
            tahun=?,
            rating=?

        WHERE kode=?
        """, (

            judul,
            penulis,
            kategori,
            tahun,
            rating,
            kode

        ))

        conn.commit()

        st.success("✅ Buku berhasil diupdate")

# =========================================================
# HAPUS BUKU
# =========================================================

elif menu == "🗑️ Hapus Buku":

    st.title("🗑️ Hapus Buku")

    kode = st.text_input("Kode Buku")

    if st.button("Hapus"):

        cursor.execute(
            "DELETE FROM books WHERE kode=?",
            (kode,)
        )

        conn.commit()

        st.success("✅ Buku berhasil dihapus")

# =========================================================
# PINJAM BUKU
# =========================================================

elif menu == "📖 Pinjam Buku":

    st.title("📖 Pinjam Buku")

    nama = st.text_input("Nama Peminjam")

    kode = st.text_input("Kode Buku")

    lama = st.number_input(
        "Lama Pinjam (hari)",
        1,
        30
    )

    if st.button("Pinjam Buku"):

        cursor.execute(
            "SELECT * FROM books WHERE kode=?",
            (kode,)
        )

        buku = cursor.fetchone()

        if buku:

            if buku[6] == "Dipinjam":

                st.error("❌ Buku sedang dipinjam")

            else:

                tanggal_pinjam = datetime.now()

                batas_kembali = (
                    tanggal_pinjam
                    + timedelta(days=lama)
                )

                cursor.execute("""
                INSERT INTO peminjaman (

                    nama,
                    kode_buku,
                    judul,
                    tanggal_pinjam,
                    batas_kembali,
                    tanggal_kembali,
                    status,
                    denda

                )

                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (

                    nama,
                    kode,
                    buku[1],
                    tanggal_pinjam.strftime("%Y-%m-%d"),
                    batas_kembali.strftime("%Y-%m-%d"),
                    "-",
                    "Dipinjam",
                    0

                ))

                cursor.execute("""
                UPDATE books
                SET status='Dipinjam'
                WHERE kode=?
                """, (kode,))

                conn.commit()

                st.success("✅ Buku berhasil dipinjam")

                st.info(
                    f"Batas pengembalian: "
                    f"{batas_kembali.strftime('%d-%m-%Y')}"
                )

# =========================================================
# KEMBALIKAN BUKU
# =========================================================

elif menu == "📥 Kembalikan Buku":

    st.title("📥 Kembalikan Buku")

    kode = st.text_input("Kode Buku")

    if st.button("Kembalikan Buku"):

        cursor.execute("""
        SELECT * FROM peminjaman

        WHERE kode_buku=?
        AND status='Dipinjam'
        """, (kode,))

        data = cursor.fetchone()

        if data:

            batas = datetime.strptime(
                data[5],
                "%Y-%m-%d"
            )

            hari_ini = datetime.now()

            telat = (hari_ini - batas).days

            denda = 0

            if telat > 0:

                denda = telat * 5000

            cursor.execute("""
            UPDATE peminjaman

            SET

                tanggal_kembali=?,
                status='Dikembalikan',
                denda=?

            WHERE id=?
            """, (

                hari_ini.strftime("%Y-%m-%d"),
                denda,
                data[0]

            ))

            cursor.execute("""
            UPDATE books

            SET status='Tersedia'

            WHERE kode=?
            """, (kode,))

            conn.commit()

            st.success("✅ Buku berhasil dikembalikan")

            if denda > 0:

                st.error(
                    f"⚠️ Terlambat {telat} hari\n"
                    f"Denda: Rp {denda}"
                )

            else:

                st.success("🎉 Tidak ada denda")

        else:

            st.error("❌ Data peminjaman tidak ditemukan")

# =========================================================
# DATA PEMINJAMAN
# =========================================================

elif menu == "📋 Data Peminjaman":

    st.title("📋 Data Peminjaman")

    data = pd.read_sql_query(
        "SELECT * FROM peminjaman",
        conn
    )

    st.dataframe(
        data,
        use_container_width=True
    )

# =========================================================
# CARI BUKU
# =========================================================

elif menu == "🔍 Cari Buku":

    st.title("🔍 Cari Buku")

    keyword = st.text_input(
        "Masukkan judul buku"
    )

    if keyword:

        query = f"""
        SELECT * FROM books

        WHERE judul LIKE '%{keyword}%'
        """

        data = pd.read_sql_query(
            query,
            conn
        )

        if len(data) > 0:

            for _, buku in data.iterrows():

                st.markdown(f"""
                <div class="book-card">

                <h3>📖 {buku['judul']}</h3>

                <p>✍️ {buku['penulis']}</p>

                <p>📚 {buku['kategori']}</p>

                <p>⭐ {buku['rating']}</p>

                </div>
                """, unsafe_allow_html=True)

        else:

            st.error("❌ Buku tidak ditemukan")

# =========================================================
# STATISTIK
# =========================================================

elif menu == "📊 Statistik":

    st.title("📊 Statistik Perpustakaan")

    total = pd.read_sql_query(
        "SELECT * FROM books",
        conn
    )

    tersedia = pd.read_sql_query(
        "SELECT * FROM books WHERE status='Tersedia'",
        conn
    )

    dipinjam = pd.read_sql_query(
        "SELECT * FROM books WHERE status='Dipinjam'",
        conn
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "📚 Total Buku",
            len(total)
        )

    with col2:
        st.metric(
            "🟢 Tersedia",
            len(tersedia)
        )

    with col3:
        st.metric(
            "📕 Dipinjam",
            len(dipinjam)
        )

    st.markdown("---")

    st.bar_chart(
        {

            "Jumlah": [

                len(total),
                len(tersedia),
                len(dipinjam)

            ]

        }
    )

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

📚 Libraverse Pro — Modern Library System

</div>
""", unsafe_allow_html=True)
