import streamlit as st
import sqlite3
import pandas as pd

from datetime import datetime, timedelta

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Libraverse Ultimate",
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
# TABEL USER
# =========================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT

)
""")

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
    username TEXT,
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
# DATA USER DEFAULT
# =========================================================

cursor.execute("SELECT COUNT(*) FROM users")

if cursor.fetchone()[0] == 0:

    users = [

        ("admin", "admin123", "admin"),
        ("rafly", "123", "user"),
        ("dina", "123", "user")

    ]

    cursor.executemany(
        "INSERT INTO users VALUES (?, ?, ?)",
        users
    )

    conn.commit()

# =========================================================
# DATA BUKU DEFAULT
# =========================================================

cursor.execute("SELECT COUNT(*) FROM books")

if cursor.fetchone()[0] == 0:

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
            "Harry Potter",
            "J.K Rowling",
            "Fantasi",
            2001,
            4.9,
            "Tersedia"
        ),

        (
            "BK003",
            "Laskar Pelangi",
            "Andrea Hirata",
            "Pendidikan",
            2005,
            4.8,
            "Tersedia"
        ),

        (
            "BK004",
            "Bumi",
            "Tere Liye",
            "Fantasi",
            2014,
            4.8,
            "Tersedia"
        ),

        (
            "BK005",
            "Sherlock Holmes",
            "Arthur Conan Doyle",
            "Misteri",
            1892,
            4.9,
            "Tersedia"
        )

    ]

    cursor.executemany(
        "INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?)",
        books
    )

    conn.commit()

# =========================================================
# SESSION LOGIN
# =========================================================

if "login" not in st.session_state:

    st.session_state.login = False
    st.session_state.username = ""
    st.session_state.role = ""

# =========================================================
# LOGIN PAGE
# =========================================================

if not st.session_state.login:

    st.markdown("""
    <div class="header-box">

    <h1>📚 Libraverse Ultimate</h1>

    <p>Digital Library Modern System</p>

    </div>
    """, unsafe_allow_html=True)

    st.title("🔐 Login")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        cursor.execute("""
        SELECT * FROM users

        WHERE username=?
        AND password=?
        """, (

            username,
            password

        ))

        user = cursor.fetchone()

        if user:
            st.session_state.login = True
            st.session_state.username = user[0]
            st.session_state.role = user[2]

            st.success("✅ Login berhasil")
            st.rerun()

        else:
            st.error("❌ Username/password salah")

# =========================================================
# SETELAH LOGIN
# =========================================================

else:
    username = st.session_state.username
    role = st.session_state.role

    st.sidebar.title("📚 Libraverse")

    st.sidebar.success(
        f"Login sebagai: {username}"
    )

    st.sidebar.info(
        f"Role: {role}"
    )

    # =====================================================
    # MENU ADMIN
    # =====================================================

    if role == "admin":

        menu = st.sidebar.selectbox(
            "Menu",
            [

                "🏠 Dashboard",
                "📚 Koleksi Buku",
                "➕ Tambah Buku",
                "✏️ Update Buku",
                "🗑️ Hapus Buku",
                "📋 Data Peminjaman",
                "📊 Statistik"

            ]
        )

    # =====================================================
    # MENU USER
    # =====================================================

    else:
        menu = st.sidebar.selectbox(
            "Menu",
            [

                "🏠 Home",
                "📚 Koleksi Buku",
                "📖 Pinjam Buku",
                "📥 Kembalikan Buku",
                "📋 Buku Saya"

            ]
        )

    # =====================================================
    # LOGOUT
    # =====================================================

    if st.sidebar.button("🚪 Logout"):

        st.session_state.login = False

        st.rerun()

    # =====================================================
    # DASHBOARD ADMIN
    # =====================================================

    if menu == "🏠 Dashboard":

        st.title("📊 Dashboard Admin")

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
                "📖 Dipinjam",
                len(total_pinjam)
            )

        with col3:
            st.metric(
                "🟢 Tersedia",
                len(tersedia)
            )

    # =====================================================
    # HOME USER
    # =====================================================

    elif menu == "🏠 Home":

        st.markdown(f"""
        <div class="header-box">

        <h1>📚 Selamat Datang {username}</h1>

        <p>
        Jelajahi berbagai koleksi buku favoritmu
        </p>

        </div>
        """, unsafe_allow_html=True)

    # =====================================================
    # KOLEKSI BUKU
    # =====================================================

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

            <p>✍️ {buku['penulis']}</p>
            <p>📚 {buku['kategori']}</p>
            <p>⭐ {buku['rating']}</p>
            <p>{warna} {buku['status']}</p>
            <p>🆔 {buku['kode']}</p>

            </div>
            """, unsafe_allow_html=True)

    # =====================================================
    # TAMBAH BUKU
    # =====================================================

    elif menu == "➕ Tambah Buku":

        st.title("➕ Tambah Buku")

        kode = st.text_input("Kode Buku")
        judul = st.text_input("Judul")
        penulis = st.text_input("Penulis")
        kategori = st.text_input("Kategori")
        tahun = st.number_input(
            "Tahun",
            1900,
            2030
        )

        rating = st.slider(
            "Rating",
            1.0,
            5.0,
            4.0
        )

        if st.button("Tambah"):

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

    elif menu == "✏️ Update Buku":

        st.title("✏️ Update Buku")

        kode = st.text_input("Kode Buku")
        judul = st.text_input("Judul Baru")
        penulis = st.text_input("Penulis Baru")
        kategori = st.text_input("Kategori Baru")
        tahun = st.number_input(
            "Tahun Baru",
            1900,
            2030
        )

        rating = st.slider(
            "Rating Baru",
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

    # =====================================================
    # HAPUS BUKU
    # =====================================================

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

    # =====================================================
    # PINJAM BUKU
    # =====================================================

    elif menu == "📖 Pinjam Buku":

        st.title("📖 Pinjam Buku")

        kode = st.text_input("Kode Buku")

        lama = st.number_input(
            "Lama Pinjam (hari)",
            1,
            30
        )

        if st.button("Pinjam"):

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

                        username,
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

                        username,
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

    # =====================================================
    # KEMBALIKAN BUKU
    # =====================================================

    elif menu == "📥 Kembalikan Buku":

        st.title("📥 Kembalikan Buku")

        kode = st.text_input("Kode Buku")

        if st.button("Kembalikan"):

            cursor.execute("""
            SELECT * FROM peminjaman

            WHERE kode_buku=?
            AND username=?
            AND status='Dipinjam'
            """, (

                kode,
                username

            ))

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
                        f"⚠️ Denda : Rp {denda}"
                    )

                else:
                    st.success("🎉 Tidak ada denda")

    # =====================================================
    # BUKU SAYA
    # =====================================================

    elif menu == "📋 Buku Saya":

        st.title("📋 Buku Saya")

        data = pd.read_sql_query(f"""

        SELECT * FROM peminjaman

        WHERE username='{username}'

        """, conn)

        st.dataframe(
            data,
            use_container_width=True
        )

    # =====================================================
    # DATA PEMINJAMAN ADMIN
    # =====================================================

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

    # =====================================================
    # STATISTIK
    # =====================================================

    elif menu == "📊 Statistik":

        st.title("📊 Statistik")

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
