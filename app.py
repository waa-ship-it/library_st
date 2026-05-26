import streamlit as st

# =========================================
#           KONFIGURASI HALAMAN
# =========================================

st.set_page_config(
    page_title="Digital Library",
    page_icon="📚",
    layout="wide"
)

# =======================
#       CSS CUSTOM
# =======================

st.markdown("""
<style>

.main {
    background-color: #F5F7FA;
}

.title {
    font-size: 50px;
    font-weight: bold;
    color: #4A148C;
    text-align: center;
}

.subtitle {
    font-size: 20px;
    color: gray;
    text-align: center;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    color: gray;
    padding: 10px;
}

</style>
""", unsafe_allow_html=True)

# ====================
#  CLASS NODE / BUKU
# ====================

class Buku:
    def __init__(self, id_buku, judul, penulis, tahun):

        self.id_buku = id_buku
        self.judul = judul
        self.penulis = penulis
        self.tahun = tahun

        # Pointer ke node berikutnya
        self.next = None


# ========================
#    CLASS LINKED LIST
# ========================

class Perpustakaan:
    def __init__(self):
        self.head = None

    # ========= TAMBAH BUKU ==========
    def tambah_buku(self, id_buku, judul, penulis, tahun):

        buku_baru = Buku(id_buku, judul, penulis, tahun)

        buku_baru = Buku(
            id_buku,
            judul,
            penulis,
            tahun
        )

        # Jika linked list kosong
        if self.head is None:
            self.head = buku_baru

        else:
            current = self.head

            # Cari node terakhir
            while current.next:
                current = current.next

            # Sambungkan node terakhir
            current.next = buku_baru

    # ========= TAMPILKAN BUKU =========
    # TAMPILKAN BUKU
    def tampilkan_buku(self):

        data = []

        current = self.head

        while current:

            data.append({
                "📖 ID Buku": current.id_buku,
                "📚 Judul": current.judul,
                "✍️ Penulis": current.penulis,
                "📅 Tahun": current.tahun
            })

            current = current.next

        return data

    # ======== CARI BUKU =========
    def cari_buku(self, judul):

        current = self.head

        while current:

            if current.judul.lower() == judul.lower():
                return current

            current = current.next

        return None

    # ======= HAPUS BUKU =========
    def hapus_buku(self, judul):

        current = self.head
        prev = None

        while current:

            if current.judul.lower() == judul.lower():

                if prev is None:
                    self.head = current.next

                else:
                    prev.next = current.next

                return True

            prev = current
            current = current.next

        return False

    # ======== TOTAL BUKU =========
    def total_buku(self):

        total = 0
        current = self.head

        while current:
            total += 1
            current = current.next

        return total


# ==============================
#         SESSION STATE
# ==============================

if "perpus" not in st.session_state:
    st.session_state.perpus = Perpustakaan()

perpus = st.session_state.perpus

# ======================
#    DATA AWAL BUKU
# ======================

# ======================================================
# DATA AWAL BUKU
# ======================================================

if perpus.head is None:

    # ====================================
    #           📚 BUKU FIKSI
    # ====================================

    perpus.tambah_buku(
        "BK001",
        "mariposa",
        "Luluk HF",
        "2018"
    )

    perpus.tambah_buku(
        "BK002",
        "janji",
        "Tere liye",
        "2019"
    )

    perpus.tambah_buku(
        "BK003",
        "Itakrn",
        "Eccedentesiast",
        "2023"
    )

    perpus.tambah_buku(
        "BK004",
        "Funiculi Funicula",
        "Toshikazu Kawaguchi",
        "2015"
    )

    # =============================================
    #           🌸 BUKU NONFIKSI
    # =============================================

    perpus.tambah_buku(
        "BK005",
        "Atomic Habits",
        "James Clear",
        "2018"
    )

    perpus.tambah_buku(
        "BK006",
        "The Psychology of Money",
        "Morgan Housel",
        "2020"
    )

    perpus.tambah_buku(
        "BK007",
        "Filosofi Teras",
        "Henry Manampiring",
        "2018"
    )

    perpus.tambah_buku(
        "BK008",
        "Deep Work",
        "Cal Newport",
        "2016"
    )

    # ======================================
    #           📖 BUKU REFERENSI
    # ======================================

    perpus.tambah_buku(
        "BK009",
        "Atlas Dunia Pelajar",
        "Oxford Education",
        "2023"
    )

    perpus.tambah_buku(
        "BK010",
        "Artificial Intelligence Basics",
        "Tom Taulli",
        "2024"
    )

    perpus.tambah_buku(
        "BK011",
        "Ensiklopedia Teknologi Digital",
        "Gramedia Pustaka",
        "2024"
    )

    perpus.tambah_buku(
        "BK012",
        "Data Science for Beginners",
        "Andrew Park",
        "2023"
    )

# ===================
#       HEADER
# ===================

st.markdown("""
<div class="card">

<h1 class="title">
📚 Digital Library
</h1>

<p class="subtitle">
✨ Kelola koleksi bukumu dengan cara yang lebih modern ✨
</p>

</div>
""", unsafe_allow_html=True)

# ==============
#    SIDEBAR
# ==============

st.sidebar.markdown("""
# 🌸 Library Menu
Temukan semua fitur favoritmu di sini 👇
""")

menu = st.sidebar.selectbox(
    "📂 Pilih Menu",
    [
        "🏠 Home",
        "➕ Tambah Buku",
        "📖 Daftar Buku",
        "🔍 Cari Buku",
        "🗑️ Hapus Buku"
    ]
)

# ==============
#     HOME
# ==============

if menu == "🏠 Home":

    st.markdown("""
    <div class="card">
    <h2>🏠 Dashboard</h2>
    <p>Selamat datang di ruang kecil penuh cerita dan ilmu 📚</p>
    </div>
    """, unsafe_allow_html=True)

    # Statistik
    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(f"📚 Total Buku\n\n{perpus.total_buku()}")

    with col2:
        st.info("☕ Built for book lovers")

    with col3:
        st.warning("🌸 Clean and structured library system")

    st.markdown("""
    ---
    ### ✧⁠*⁠。 Yang Bisa Kamu Lakukan ✧⁠*⁠。

    📚 Tambahkan buku favoritmu ke koleksi digital  
    🔍 Cari cerita dan pengetahuan dengan mudah  
    ✨ Susun rak buku agar tetap rapi dan nyaman dilihat  
    📖 Jelajahi berbagai buku fiksi, nonfiksi, dan referensi  
    ☕ Nikmati pengalaman perpustakaan digital yang modern   

    ---
    """)

# =====================
#     TAMBAH BUKU
# =====================

elif menu == "➕ Tambah Buku":

    st.markdown("""
    <div class="card">
    <h2>➕ Tambah Buku Baru</h2>
    </div>
    """, unsafe_allow_html=True)

    id_buku = st.text_input("📖 Masukkan ID Buku")
    judul = st.text_input("📚 Masukkan Judul Buku")
    penulis = st.text_input("✍️ Masukkan Nama Penulis")
    tahun = st.text_input("📅 Masukkan Tahun Terbit")

    if st.button("✨ Tambah Buku"):

        if id_buku and judul and penulis and tahun:

            perpus.tambah_buku(
                id_buku,
                judul,
                penulis,
                tahun
            )

            st.balloons()

            st.success("🎉 Buku berhasil masuk ke koleksi perpustakaan!")

        else:
            st.error("⚠️ Semua data harus diisi!")

# ================================
#         TAMPILKAN BUKU
# ================================

elif menu == "📖 Tampilkan Buku":

    st.markdown("""
    <div class="card">
    <h2>📚 Daftar Buku Perpustakaan</h2>
    </div>
    """, unsafe_allow_html=True)

    data = perpus.tampilkan_buku()

    if data:

        st.dataframe(
            data,
            use_container_width=True
        )

        st.success(f"✅ Total buku: {len(data)}")

    else:
        st.warning("📭 Belum ada buku di perpustakaan")

# ====================
#      CARI BUKU
# ====================

elif menu == "🔍 Cari Buku":

    st.markdown("""
    <div class="card">
    <h2>🔍 Cari Buku</h2>
    </div>
    """, unsafe_allow_html=True)

    cari = st.text_input("📚 Masukkan Judul Buku")

    if st.button("🔎 Cari Sekarang"):

        hasil = perpus.cari_buku(cari)

        if hasil:

            st.success("🎉 Buku ditemukan!")

            st.markdown(f"""
            <div class="card">

            <h3>📖 Detail Buku</h3>

            <p><b>ID Buku:</b> {hasil.id_buku}</p>
            <p><b>Judul:</b> {hasil.judul}</p>
            <p><b>Penulis:</b> {hasil.penulis}</p>
            <p><b>Tahun:</b> {hasil.tahun}</p>

            </div>
            """, unsafe_allow_html=True)

        else:
            st.error("❌ Buku tidak ditemukan.")

# =========================
#        HAPUS BUKU
# =========================

elif menu == "🗑️ Hapus Buku":

    st.markdown("""
    <div class="card">
    <h2>🗑️ Hapus Buku</h2>
    </div>
    """, unsafe_allow_html=True)

    hapus = st.text_input("📚 Masukkan Judul Buku")

    if st.button("❌ Hapus Buku"):
        berhasil = perpus.hapus_buku(hapus)

        if berhasil:
            st.success("🗑️ Buku berhasil dihapus!")

        else:
            st.error("❌ Buku tidak ditemukan.")

# ==================
#      FOOTER
# ==================

st.markdown("""
---
<div class="footer">

✨ Where code meets books and creativity ✨

</div>
""", unsafe_allow_html=True)
