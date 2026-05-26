import streamlit as st

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="Libraverse",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# CSS CUSTOM
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #F6F8FC;
}

.header-box {
    background: linear-gradient(to right, #6C63FF, #8E7CFF);
    padding: 35px;
    border-radius: 25px;
    color: white;
    margin-bottom: 25px;
}

.header-title {
    font-size: 45px;
    font-weight: bold;
}

.header-subtitle {
    font-size: 18px;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.book-card {
    background: linear-gradient(to right, #ffffff, #f2f5ff);
    padding: 20px;
    border-radius: 20px;
    margin-bottom: 18px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.06);
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LINKED LIST NODE
# =========================================================

class Node:

    def __init__(
        self,
        kode,
        judul,
        penulis,
        kategori,
        tahun,
        rating,
        status
    ):

        self.kode = kode
        self.judul = judul
        self.penulis = penulis
        self.kategori = kategori
        self.tahun = tahun
        self.rating = rating
        self.status = status
        self.next = None


# =========================================================
# LINKED LIST
# =========================================================

class Library:

    def __init__(self):
        self.head = None

    # =====================================================
    # TAMBAH BUKU
    # =====================================================

    def tambah_buku(
        self,
        kode,
        judul,
        penulis,
        kategori,
        tahun,
        rating,
        status
    ):

        buku_baru = Node(
            kode,
            judul,
            penulis,
            kategori,
            tahun,
            rating,
            status
        )

        if self.head is None:
            self.head = buku_baru

        else:

            current = self.head

            while current.next:
                current = current.next

            current.next = buku_baru

    # =====================================================
    # TAMPILKAN BUKU
    # =====================================================

    def tampilkan_buku(self):

        data = []

        current = self.head

        while current:

            data.append({
                "kode": current.kode,
                "judul": current.judul,
                "penulis": current.penulis,
                "kategori": current.kategori,
                "tahun": current.tahun,
                "rating": current.rating,
                "status": current.status
            })

            current = current.next

        return data

    # =====================================================
    # CARI BUKU
    # =====================================================

    def cari_buku(self, keyword):

        hasil = []

        current = self.head

        while current:

            if keyword.lower() in current.judul.lower():

                hasil.append({
                    "kode": current.kode,
                    "judul": current.judul,
                    "penulis": current.penulis,
                    "kategori": current.kategori,
                    "tahun": current.tahun,
                    "rating": current.rating,
                    "status": current.status
                })

            current = current.next

        return hasil

    # =====================================================
    # HAPUS BUKU
    # =====================================================

    def hapus_buku(self, kode):

        current = self.head
        prev = None

        while current:

            if current.kode == kode:

                if prev is None:
                    self.head = current.next

                else:
                    prev.next = current.next

                return True

            prev = current
            current = current.next

        return False


# =========================================================
# SESSION STATE
# =========================================================

if "library" not in st.session_state:

    st.session_state.library = Library()

    library = st.session_state.library

    # =====================================================
    # DATA AWAL
    # =====================================================

    library.tambah_buku(
        "BK001",
        "Atomic Habits",
        "James Clear",
        "Nonfiksi",
        "2018",
        "4.9",
        "Tersedia"
    )

    library.tambah_buku(
        "BK002",
        "Eccedentesiast",
        "itaKRN",
        "Drama Persahabatan",
        "2022",
        "4.9",
        "Dipinjam"
    )

    library.tambah_buku(
        "BK003",
        "Ensiklopedia Sains Modern",
        "National Geographic",
        "Referensi",
        "2022",
        "4.8",
        "Tersedia"
    )

    library.tambah_buku(
        "BK004",
        "Mariposa",
        "Luluk HF",
        "Romance",
        "2018",
        "4.8",
        "Tersedia"
    )

    library.tambah_buku(
        "BK005",
        "The Psychology of Money",
        "Morgan Housel",
        "Self Improvement",
        "2020",
        "4.9",
        "Dipinjam"
    )

else:
    library = st.session_state.library

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("📚 Libraverse")

menu = st.sidebar.selectbox(
    "✨ Pilih Menu",
    [
        "🏠 Home",
        "📚 Koleksi Buku",
        "➕ Tambah Buku",
        "🔍 Cari Buku",
        "🗑️ Hapus Buku",
        "📊 Statistik"
    ]
)

st.sidebar.markdown("---")

st.sidebar.markdown("""
### 📓 Kategori Populer

- Romance  
- Nonfiksi  
- Referensi  
- Emotional Story  
- Self Improvement  

""")

# =========================================================
# HOME
# =========================================================

if menu == "🏠 Home":

    st.markdown("""
    <div class="header-box">

    <div class="header-title">
    📚 Libraverse
    </div>

    <div class="header-subtitle">
    Selamat datang di ruang kecil penuh cerita dan ilmu 🧸
    </div>

    </div>
    """, unsafe_allow_html=True)

    total = len(library.tampilkan_buku())

    tersedia = sum(
        1 for b in library.tampilkan_buku()
        if b["status"] == "Tersedia"
    )

    dipinjam = sum(
        1 for b in library.tampilkan_buku()
        if b["status"] == "Dipinjam"
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📚 Total Buku", total)

    with col2:
        st.metric("🟢 Tersedia", tersedia)

    with col3:
        st.metric("📕 Dipinjam", dipinjam)

    st.markdown("---")

    st.markdown("""
    ### yang bisa kalian lakukan :

    📚 tambahkan koleksi buku favoritmu  
    🔍 cari buku dengan cepat dan mudah  
    ✨ kelola perpustakaan digital dengan lebih rapi  
    📖 jelajahi buku modern dari berbagai kategori
    ☕ nikmati pengalaman perpustakaan digital yang modern  

    """)

    st.markdown("---")

    st.subheader("🔥 Trending Saat Ini")

    st.markdown("""
    <div class="book-card">

    <h3>📖 Atomic Habits</h3>

    <p>✍️ James Clear</p>

    <p>⭐ 4.9 | 🧠 Self Improvement</p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="book-card">

    <h3>📖 Eccedentesiast</h3>

    <p>✍️ Itakrn</p>

    <p>⭐ 4.9 | 🥀 Drama Persahabatan</p>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# KOLEKSI BUKU
# =========================================================

elif menu == "📚 Koleksi Buku":

    st.title("📚 Koleksi Buku")

    data = library.tampilkan_buku()

    kategori_filter = st.selectbox(
        "📖 Pilih Kategori",
        [
            "Semua",
            "Romance",
            "Nonfiksi",
            "Referensi",
            "Drama Persahabatan",
            "Self Improvement"
        ]
    )

    st.markdown("---")

    for buku in data:

        if kategori_filter != "Semua":

            if buku["kategori"] != kategori_filter:
                continue

        warna = "🟢" if buku["status"] == "Tersedia" else "🔴"

        st.markdown(f"""
        <div class="book-card">

        <h3>📖 {buku['judul']}</h3>

        <p>✍️ Penulis : {buku['penulis']}</p>

        <p>📚 Kategori : {buku['kategori']}</p>

        <p>📅 Tahun : {buku['tahun']}</p>

        <p>⭐ Rating : {buku['rating']}</p>

        <p>{warna} Status : {buku['status']}</p>

        <p>🆔 Kode Buku : {buku['kode']}</p>

        </div>
        """, unsafe_allow_html=True)

# =========================================================
# TAMBAH BUKU
# =========================================================

elif menu == "➕ Tambah Buku":

    st.title("➕ Tambahkan Buku Baru")

    kode = st.text_input("🆔 Kode Buku")

    judul = st.text_input("📖 Judul Buku")

    penulis = st.text_input("✍️ Nama Penulis")

    kategori = st.selectbox(
        "📚 Kategori",
        [
            "romance",
            "fiksi",
            "nonfiksi",
            "referensi",
            "drama persahabatan",
            "teknologi"
            "self Improvement"
        ]
    )

    tahun = st.number_input(
        "📅 Tahun Terbit",
        2000,
        2025
    )

    rating = st.slider(
        "⭐ Rating Buku",
        1.0,
        5.0,
        4.0
    )

    status = st.selectbox(
        "📌 Status Buku",
        [
            "Tersedia",
            "Dipinjam"
        ]
    )

    if st.button("✨ Tambahkan Buku"):

        library.tambah_buku(
            kode,
            judul,
            penulis,
            kategori,
            tahun,
            rating,
            status
        )

        st.success(
            f"✅ Buku '{judul}' berhasil ditambahkan!"
        )

        st.balloons()

# =========================================================
# CARI BUKU
# =========================================================

elif menu == "🔍 Cari Buku":

    st.title("🔍 Cari Buku")

    keyword = st.text_input(
        "Masukkan judul buku"
    )

    hasil = library.cari_buku(keyword)

    if keyword:

        if hasil:

            st.success(
                f"✅ Ditemukan {len(hasil)} buku"
            )

            for buku in hasil:

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
# HAPUS BUKU
# =========================================================

elif menu == "🗑️ Hapus Buku":

    st.title("🗑️ Kelola Buku")

    kode = st.text_input(
        "Masukkan kode buku"
    )

    if st.button("❌ Hapus Buku"):

        hasil = library.hapus_buku(kode)

        if hasil:

            st.success(
                "✅ Buku berhasil dihapus"
            )

        else:

            st.error(
                "❌ Buku tidak ditemukan"
            )

# =========================================================
# STATISTIK
# =========================================================

elif menu == "📊 Status Akhir":

    st.title("📊 Status Perpustakaan")

    total = len(library.tampilkan_buku())

    tersedia = sum(
        1 for b in library.tampilkan_buku()
        if b["status"] == "Tersedia"
    )

    dipinjam = sum(
        1 for b in library.tampilkan_buku()
        if b["status"] == "Dipinjam"
    )

    romance = sum(
        1 for b in library.tampilkan_buku()
        if b["kategori"] == "Romance"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total Buku", total)

    with col2:
        st.metric("🟢 Tersedia", tersedia)

    with col3:
        st.metric("📕 Dipinjam", dipinjam)

    with col4:
        st.metric("🌸 Romance", romance)

    st.markdown("---")

    st.info(f"""
        - Total koleksi buku : {total}
        - Buku tersedia : {tersedia}
        - Buku dipinjam : {dipinjam}
        - Buku romance : {romance}
    """)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="footer">

Where code meets books and creativity

</div>
""", unsafe_allow_html=True)
