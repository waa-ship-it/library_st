import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime, timedelta

# =========================================================
# KONFIGURASI PAGE
# =========================================================

st.set_page_config(
    page_title="Libraverse",
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

.stButton button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
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
    status TEXT,
    denda INTEGER

)
""")

conn.commit()

# =========================================================
# DATA BUKU DEFAULT
# =========================================================

cursor.execute("SELECT COUNT(*) FROM books")

if cursor.fetchone()[0] == 0:

    books = [

        ("BK001", "Atomic Habits", "James Clear", "Self Improvement", 2018, 4.9, "Tersedia"),
        ("BK002", "Harry Potter", "J.K Rowling", "Fantasi", 2001, 4.9, "Tersedia"),
        ("BK003", "Laskar Pelangi", "Andrea Hirata", "Pendidikan", 2005, 4.8, "Tersedia"),
        ("BK004", "Bumi", "Tere Liye", "Fantasi", 2014, 4.8, "Tersedia"),
        ("BK005", "Sherlock Holmes", "Arthur Conan Doyle", "Misteri", 1892, 4.9, "Tersedia"),
        ("BK006", "Laut Bercerita", "Leila S Chudori", "Fiksi", 2017, 4.9, "Tersedia"),
        ("BK007", "Mariposa", "Luluk HF", "Romance", 2018, 4.7, "Tersedia"),
        ("BK008", "Filosofi Teras", "Henry Manampiring", "Self Improvement", 2019, 4.8, "Tersedia"),
        ("BK009", "One Piece Vol 1", "Eiichiro Oda", "Komik", 1997, 4.9, "Tersedia"),
        ("BK010", "Naruto Vol 1", "Masashi Kishimoto", "Komik", 1999, 4.8, "Tersedia")

    ]

    cursor.executemany(
        "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
        books
    )

    conn.commit()

# =========================================================
# LOGIN ADMIN
# =========================================================

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Libraverse")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [

        "🏠 Home",
        "📚 Koleksi Buku",
        "📖 Pinjam Buku",
        "✏️ Update Peminjaman",
        "❌ Batalkan Peminjaman",
        "📥 Kembalikan Buku",
        "📋 Riwayat Peminjaman",
        "🔍 Cari Buku",
        "🔐 Admin Login"

    ]
)

# =========================================================
# MENU ADMIN
# =========================================================

if st.session_state.admin_login:

    st.sidebar.markdown("---")

    admin_menu = st.sidebar.selectbox(
        "Menu Admin",
        [

            "➕ Tambah Buku",
            "✏️ Update Buku",
            "🗑️ Hapus Buku",
            "📊 Statistik"

        ]
    )

    if st.sidebar.button("🚪 Logout Admin"):

        st.session_state.admin_login = False
        st.rerun()

# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.markdown("""
    <div class="header-box">

    <h1>📚 Libraverse</h1>

    <p>
    Sistem Perpustakaan Modern dan Interaktif
    </p>

    </div>
    """, unsafe_allow_html=True)

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
        st.metric("📚 Total Buku", len(total))

    with col2:
        st.metric("🟢 Tersedia", len(tersedia))

    with col3:
        st.metric("📕 Dipinjam", len(dipinjam))

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

    for _, buku in data.iterrows():

        warna = "🟢" if buku["status"] == "Tersedia" else "🔴"

        st.markdown(f"""
        <div class="book-card">

        <h3>📖 {buku['judul']}</h3>

        <p>✍️ Penulis : {buku['penulis']}</p>
        <p>📚 Kategori : {buku['kategori']}</p>
        <p>📅 Tahun : {buku['tahun']}</p>
        <p>⭐ Rating : {buku['rating']}</p>
        <p>{warna} {buku['status']}</p>
        <p>🆔 {buku['kode']}</p>

        </div>
        """, unsafe_allow_html=True)

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

    if st.button("Konfirmasi Pinjam"):

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
                    status,
                    denda

                )

                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (

                    nama,
                    kode,
                    buku[1],
                    tanggal_pinjam.strftime("%Y-%m-%d"),
                    batas_kembali.strftime("%Y-%m-%d"),
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

                st.info(f"""
                📖 Judul Buku : {buku[1]}

                📅 Tanggal Pinjam :
                {tanggal_pinjam.strftime('%d-%m-%Y')}

                ⏰ Batas Kembali :
                {batas_kembali.strftime('%d-%m-%Y')}
                """)

# =========================================================
# UPDATE PEMINJAMAN
# =========================================================

elif menu == "✏️ Update Peminjaman":

    st.title("✏️ Update Peminjaman")

    id_pinjam = st.number_input(
        "ID Peminjaman",
        1
    )

    lama_baru = st.number_input(
        "Tambah Lama Pinjam",
        1,
        30
    )

    if st.button("Update Peminjaman"):

        cursor.execute("""
        SELECT * FROM peminjaman

        WHERE id=?
        AND status='Dipinjam'
        """, (id_pinjam,))

        data = cursor.fetchone()

        if data:

            batas_lama = datetime.strptime(
                data[5],
                "%Y-%m-%d"
            )

            batas_baru = (
                batas_lama
                + timedelta(days=lama_baru)
            )

            cursor.execute("""
            UPDATE peminjaman

            SET batas_kembali=?

            WHERE id=?
            """, (

                batas_baru.strftime("%Y-%m-%d"),
                id_pinjam

            ))

            conn.commit()

            st.success("✅ Peminjaman berhasil diperpanjang")

            st.info(
                f"Batas kembali baru : "
                f"{batas_baru.strftime('%d-%m-%Y')}"
            )

        else:

            st.error("❌ Data tidak ditemukan")

# =========================================================
# BATALKAN PEMINJAMAN
# =========================================================

elif menu == "❌ Batalkan Peminjaman":

    st.title("❌ Batalkan Peminjaman")

    id_pinjam = st.number_input(
        "ID Peminjaman",
        1
    )

    if st.button("Batalkan"):

        cursor.execute("""
        SELECT * FROM peminjaman

        WHERE id=?
        AND status='Dipinjam'
        """, (id_pinjam,))

        data = cursor.fetchone()

        if data:

            cursor.execute("""
            UPDATE peminjaman

            SET status='Dibatalkan'

            WHERE id=?
            """, (id_pinjam,))

            cursor.execute("""
            UPDATE books

            SET status='Tersedia'

            WHERE kode=?
            """, (data[2],))

            conn.commit()

            st.success("✅ Peminjaman dibatalkan")

        else:

            st.error("❌ Data tidak ditemukan")

# =========================================================
# KEMBALIKAN BUKU
# =========================================================

elif menu == "📥 Kembalikan Buku":

    st.title("📥 Kembalikan Buku")

    id_pinjam = st.number_input(
        "ID Peminjaman",
        1
    )

    if st.button("Kembalikan Buku"):

        cursor.execute("""
        SELECT * FROM peminjaman

        WHERE id=?
        AND status='Dipinjam'
        """, (id_pinjam,))

        data = cursor.fetchone()

        if data:

            batas = datetime.strptime(
                data[5],
                "%Y-%m-%d"
            )

            hari_ini = datetime.now()

            telat = (
                hari_ini - batas
            ).days

            denda = 0

            if telat > 0:
                denda = telat * 5000

            cursor.execute("""
            UPDATE peminjaman

            SET

                status='Dikembalikan',
                denda=?

            WHERE id=?
            """, (

                denda,
                id_pinjam

            ))

            cursor.execute("""
            UPDATE books

            SET status='Tersedia'

            WHERE kode=?
            """, (data[2],))

            conn.commit()

            st.success("✅ Buku berhasil dikembalikan")

            if denda > 0:

                st.error(
                    f"⚠️ Terlambat {telat} hari\n"
                    f"Denda : Rp {denda}"
                )

            else:
                st.success("🎉 Tidak ada denda")

        else:
            st.error("❌ Data tidak ditemukan")

# =========================================================
# RIWAYAT PEMINJAMAN
# =========================================================

elif menu == "📋 Riwayat Peminjaman":

    st.title("📋 Riwayat Peminjaman")

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

        query = """
        SELECT * FROM books

        WHERE judul LIKE ?
        """

        data = pd.read_sql_query(
            query,
            conn,
            params=(f"%{keyword}%",)
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
# LOGIN ADMIN
# =========================================================

elif menu == "🔐 Admin Login":

    st.title("🔐 Login Admin")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if username == "parkj" and password == "0052":

            st.session_state.admin_login = True

            st.success("✅ Login admin berhasil")

            st.rerun()

        else:
            st.error("❌ Username/password salah")

# =========================================================
# MENU ADMIN
# =========================================================

if st.session_state.admin_login:

    # =====================================================
    # TAMBAH BUKU
    # =====================================================

    if admin_menu == "➕ Tambah Buku":

        st.title("➕ Tambah Buku")

        kode = st.text_input("Kode Buku")
        judul = st.text_input("Judul Buku")
        penulis = st.text_input("Penulis")
        kategori = st.text_input("Kategori")

        tahun = st.number_input(
            "Tahun",
            1800,
            2030
        )

        rating = st.slider(
            "Rating",
            1.0,
            5.0,
            4.0
        )

        if st.button("Tambah Buku"):

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

    # =====================================================
    # UPDATE BUKU
    # =====================================================

    elif admin_menu == "✏️ Update Buku":

        st.title("✏️ Update Buku")

        kode = st.text_input("Kode Buku")
        judul = st.text_input("Judul Baru")
        penulis = st.text_input("Penulis Baru")
        kategori = st.text_input("Kategori Baru")

        tahun = st.number_input(
            "Tahun Baru",
            1800,
            2030
        )

        rating = st.slider(
            "Rating Baru",
            1.0,
            5.0,
            4.0
        )

        if st.button("Update Buku"):

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

    # =====================================================
    # HAPUS BUKU
    # =====================================================

    elif admin_menu == "🗑️ Hapus Buku":

        st.title("🗑️ Hapus Buku")

        kode = st.text_input("Kode Buku")

        if st.button("Hapus Buku"):

            cursor.execute(
                "DELETE FROM books WHERE kode=?",
                (kode,)
            )

            conn.commit()

            st.success("✅ Buku berhasil dihapus")

    # =====================================================
    # STATISTIK
    # =====================================================

    elif admin_menu == "📊 Statistik":

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

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

📚 Libraverse — Library System

</div>
""", unsafe_allow_html=True)
