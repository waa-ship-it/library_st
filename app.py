import streamlit as st

# =========================================================
#                    KONFIGURASI HALAMAN
# =========================================================

st.set_page_config(
    page_title="📚 Digital Library",
    page_icon="📖",
    layout="wide"
)

# =========================================================
#                     CSS AESTHETIC
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f8f6ff;
}

.big-title {
    font-size: 45px;
    font-weight: bold;
    color: #6c63ff;
}

.subtitle {
    font-size: 18px;
    color: #555;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.book-card {
    background: linear-gradient(to right, #fdfbfb, #ebedee);
    padding: 18px;
    border-radius: 18px;
    margin-bottom: 15px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.08);
}

.sidebar .sidebar-content {
    background-color: #f4f0ff;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
#                     LINKED LIST NODE
# =========================================================

class Node:
    def __init__(self, kode, judul, penulis, kategori, tahun, status):
        self.kode = kode
        self.judul = judul
        self.penulis = penulis
        self.kategori = kategori
        self.tahun = tahun
        self.status = status
        self.next = None


# =========================================================
#                 LINKED LIST PERPUSTAKAAN
# =========================================================

class LinkedListPerpus:
    def __init__(self):
        self.head = None

    # Tambah buku
    def tambah_buku(self, kode, judul, penulis, kategori, tahun, status):

        buku_baru = Node(
            kode,
            judul,
            penulis,
            kategori,
            tahun,
            status
        )

        if self.head is None:
            self.head = buku_baru

        else:
            temp = self.head

            while temp.next:
                temp = temp.next

            temp.next = buku_baru

    # Tampilkan semua buku
    def tampilkan_buku(self):

        data = []

        temp = self.head

        while temp:

            data.append({
                "kode": temp.kode,
                "judul": temp.judul,
                "penulis": temp.penulis,
                "kategori": temp.kategori,
                "tahun": temp.tahun,
                "status": temp.status
            })

            temp = temp.next

        return data

    # Cari buku
    def cari_buku(self, keyword):

        hasil = []

        temp = self.head

        while temp:

            if keyword.lower() in temp.judul.lower():

                hasil.append({
                    "kode": temp.kode,
                    "judul": temp.judul,
                    "penulis": temp.penulis,
                    "kategori": temp.kategori,
                    "tahun": temp.tahun,
                    "status": temp.status
                })

            temp = temp.next

        return hasil

    # Hapus buku
    def hapus_buku(self, kode):

        temp = self.head

        prev = None

        if temp and temp.kode == kode:
            self.head = temp.next
            return True

        while temp and temp.kode != kode:
            prev = temp
            temp = temp.next

        if temp is None:
            return False

        prev.next = temp.next
        return True


# =========================================================
#                     SESSION STATE
# =========================================================

if "perpus" not in st.session_state:

    st.session_state.perpus = LinkedListPerpus()

    perpus = st.session_state.perpus

    # =====================================================
    #                  DATA AWAL BUKU
    # =====================================================

    perpus.tambah_buku(
        "BK001",
        "Laut bercerita",
        "Leila S. Chudori",
        "Fiksi",
        "2017",
        "Tersedia"
    )

    perpus.tambah_buku(
        "BK002",
        "Atomic Habits",
        "James Clear",
        "Nonfiksi",
        "2018",
        "Dipinjam"
    )

    perpus.tambah_buku(
        "BK003",
        "Ensiklopedia Sains Modern",
        "National Geographic",
        "Referensi",
        "2022",
        "Tersedia"
    )

    perpus.tambah_buku(
        "BK004",
        "The Psychology of Money",
        "Morgan Housel",
        "Nonfiksi",
        "2020",
        "Tersedia"
    )

    perpus.tambah_buku(
        "BK005",
        "Itakrn",
        "Eccedentesiat",
        "Fiksi",
        "2023",
        "Dipinjam"
    )

else:
    perpus = st.session_state.perpus


# =========================================================
#                         SIDEBAR
# =========================================================

st.sidebar.title("📚 Digital Library")

st.sidebar.markdown("""
# 🌸 Library Menu
Temukan semua fitur favoritmu di sini 👇
""")

menu = st.sidebar.radio(
    "Pilih Menu :",
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
### 🌈 Kategori Buku

📖 Fiksi  
🧠 Nonfiksi  
📚 Referensi  
✨ Self Improvement  
☕ Novel Modern  

""")

# =========================================================
#                         HOME
# =========================================================

if menu == "🏠 Home":

    st.markdown(
        '<div class="big-title">📚 Digital Library</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">✨ Kelola koleksi bukumu dengan cara yang lebih modern ✨</div>',
        unsafe_allow_html=True
    )

    st.markdown("---")

    total = len(perpus.tampilkan_buku())

    tersedia = sum(
        1 for b in perpus.tampilkan_buku()
        if b["status"] == "Tersedia"
    )

    dipinjam = sum(
        1 for b in perpus.tampilkan_buku()
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
    ✨ kelola perpustakaan digital dengan rapi  
    📖 jelajahi berbagai kategori buku modern  
    ☕ nikmati pengalaman perpustakaan digital yang modern  

    """)

    st.markdown("---")

    st.subheader("🔥 Buku Trending Minggu Ini")

    st.markdown("""
    <div class="book-card">
    <h4>📖 Atomic Habits</h4>
    <p>✍️ James Clear</p>
    <p>⭐ 4.8 | 🧠 Self Improvement</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="book-card">
    <h4>📖 Eccedentesiast</h4>
    <p>✍️ Itakrn</p>
    <p>⭐ 4.9 | 🤝 Friendship Story</p>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
#                     KOLEKSI BUKU
# =========================================================

elif menu == "📚 Koleksi Buku":

    st.title("📚 Koleksi Buku")

    data = perpus.tampilkan_buku()

    if data:
        for buku in data:
            warna = "🟢" if buku["status"] == "Tersedia" else "🔴"

            st.markdown(f"""
            <div class="book-card">

            <h3>📖 {buku['judul']}</h3>

            <p>✍️ Penulis : {buku['penulis']}</p>
            <p>📚 Kategori : {buku['kategori']}</p>
            <p>📅 Tahun : {buku['tahun']}</p>
            <p>{warna} Status : {buku['status']}</p>
            <p>🆔 Kode : {buku['kode']}</p>

            </div>
            """, unsafe_allow_html=True)

    else:
        st.warning("⚠️ Belum ada buku !")

# =========================================================
#                     TAMBAH BUKU
# =========================================================

elif menu == "➕ Tambah Buku":

    st.title("➕ Tambah Buku Baru")

    kode = st.text_input("🆔 Kode Buku")
    judul = st.text_input("📖 Judul Buku")
    penulis = st.text_input("✍️ Nama Penulis")
    
    kategori = st.selectbox(
        "📚 Pilih Kategori",
        [
            "Fiksi",
            "Nonfiksi",
            "Referensi",
            "Self Improvement",
            "Novel"
        ]
    )

    tahun = st.number_input(
        "📅 Tahun Terbit",
        2000,
        2025
    )

    status = st.selectbox(
        "📌 Status Buku",
        [
            "Tersedia",
            "Dipinjam"
        ]
    )

    if st.button("✨ Tambahkan Buku"):

        perpus.tambah_buku(
            kode,
            judul,
            penulis,
            kategori,
            tahun,
            status
        )

        st.success(f"✅ Buku '{judul}' berhasil ditambahkan!")

# =========================================================
#                       CARI BUKU
# =========================================================

elif menu == "🔍 Cari Buku":

    st.title("🔍 Cari Buku")

    keyword = st.text_input(
        "Cari berdasarkan judul buku"
    )

    if keyword:
        hasil = perpus.cari_buku(keyword)

        if hasil:
            st.success(f"✅ Ditemukan {len(hasil)} buku")

            for buku in hasil:
                st.markdown(f"""
                <div class="book-card">

                <h3>📖 {buku['judul']}</h3>
                
                <p>✍️ {buku['penulis']}</p>
                <p>📚 {buku['kategori']}</p>
                <p>📅 {buku['tahun']}</p>
                
                </div>
                """, unsafe_allow_html=True)

        else:
            st.error("❌ Buku tidak ditemukan")

# =========================================================
#                        HAPUS BUKU
# =========================================================

elif menu == "🗑️ Hapus Buku":

    st.title("🗑️ Kelola Koleksi Buku")

    kode = st.text_input("Masukkan kode buku")

    if st.button("❌ Hapus Buku"):
        hasil = perpus.hapus_buku(kode)
        if hasil:
            st.success("✅ Buku berhasil dihapus")
        else:
            st.error("❌ Buku tidak ditemukan")

# =========================================================
# STATISTIK
# =========================================================

elif menu == "📊 Statistik":

    st.title("📊 Statistik Perpustakaan")

    total = len(perpus.tampilkan_buku())

    tersedia = sum(
        1 for b in perpus.tampilkan_buku()
        if b["status"] == "Tersedia"
    )

    dipinjam = sum(
        1 for b in perpus.tampilkan_buku()
        if b["status"] == "Dipinjam"
    )

    fiksi = sum(
        1 for b in perpus.tampilkan_buku()
        if b["kategori"] == "Fiksi"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("📚 Total", total)

    with col2:
        st.metric("🟢 Tersedia", tersedia)

    with col3:
        st.metric("📕 Dipinjam", dipinjam)

    with col4:
        st.metric("🌸 Fiksi", fiksi)

    st.markdown("---")

    st.subheader("✨ Ringkasan Perpustakaan")

    st.info(f"""
    📚 Total koleksi buku : {total}
    🟢 Buku tersedia : {tersedia}
    📕 Buku dipinjam : {dipinjam}
    🌸 Buku kategori fiksi : {fiksi}
    """)
