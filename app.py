# =========================================================
# IMPORT LIBRARY
# =========================================================
import streamlit as st
import pandas as pd
from datetime import datetime

# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Aplikasi Perpustakaan",
    page_icon="📚",
    layout="wide"
)

# =========================================================
# STYLE CSS
# =========================================================
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

h1, h2, h3 {
    color: #1f2937;
}

.stButton>button {
    background-color: #2563eb;
    color: white;
    border-radius: 10px;
    height: 45px;
    width: 100%;
    font-size: 16px;
}

.stButton>button:hover {
    background-color: #1d4ed8;
}

.kotak {
    padding: 20px;
    border-radius: 15px;
    background-color: white;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# CLASS NODE
# =========================================================
class BookNode:
    def __init__(self, kode, nama, buku, penulis,
                 kategori, jumlah, tanggal, waktu):

        self.kode = kode
        self.nama = nama
        self.buku = buku
        self.penulis = penulis
        self.kategori = kategori
        self.jumlah = jumlah
        self.tanggal = tanggal
        self.waktu = waktu
        self.next = None


# =========================================================
# CLASS LINKED LIST
# =========================================================
class LibraryLinkedList:

    def __init__(self):
        self.head = None

    # tambah data
    def tambah_peminjaman(self, kode, nama, buku,
                          penulis, kategori,
                          jumlah, tanggal, waktu):

        node_baru = BookNode(
            kode,
            nama,
            buku,
            penulis,
            kategori,
            jumlah,
            tanggal,
            waktu
        )

        if self.head is None:
            self.head = node_baru

        else:
            current = self.head

            while current.next:
                current = current.next

            current.next = node_baru

    # tampilkan data
    def tampilkan_data(self):

        data = []

        current = self.head

        while current:

            data.append({
                "Kode": current.kode,
                "Nama": current.nama,
                "Judul Buku": current.buku,
                "Penulis": current.penulis,
                "Kategori": current.kategori,
                "Jumlah": current.jumlah,
                "Tanggal Pinjam": current.tanggal,
                "Waktu Input": current.waktu
            })

            current = current.next

        return data

    # hapus data
    def hapus_data(self, kode):

        current = self.head
        prev = None

        while current:

            if current.kode == kode:

                if prev:
                    prev.next = current.next

                else:
                    self.head = current.next

                return True

            prev = current
            current = current.next

        return False


# =========================================================
# SESSION STATE
# =========================================================
if "library" not in st.session_state:
    st.session_state.library = LibraryLinkedList()

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

# =========================================================
# LOGIN ADMIN
# =========================================================
USERNAME = "parkj"
PASSWORD = "0052"

st.sidebar.divider()
st.sidebar.subheader("🔐 Admin Perpustakaan")

admin_user = st.sidebar.text_input("Username Admin")
admin_pass = st.sidebar.text_input(
    "Password Admin",
    type="password"
)

if st.sidebar.button("Login Admin"):

    if admin_user == USERNAME and admin_pass == PASSWORD:

        st.session_state.admin_login = True
        st.sidebar.success("✅ Admin berhasil login")

    else:

        st.sidebar.error("❌ Username / Password salah")

# =========================================================
# DATA BUKU
# =========================================================
buku_data = {

    "Laskar Pelangi": {
        "penulis": "Andrea Hirata",
        "kategori": "Novel",
        "stok": 20
    },

    "Bumi Manusia": {
        "penulis": "Pramoedya Ananta Toer",
        "kategori": "Sejarah",
        "stok": 15
    },

    "Atomic Habits": {
        "penulis": "James Clear",
        "kategori": "Self Improvement",
        "stok": 25
    }

}

# =========================================================
# HEADER
# =========================================================
st.title("📚 Aplikasi Perpustakaan")
st.write("### Project Struktur Data Menggunakan Linked List")
st.write("Aplikasi ini digunakan untuk peminjaman buku perpustakaan secara online.")

st.divider()

# =========================================================
# SIDEBAR PEMINJAMAN
# =========================================================
st.sidebar.header("📝 Form Peminjaman Buku")

nama = st.sidebar.text_input("👤 Nama Peminjam")

buku = st.sidebar.selectbox(
    "📖 Pilih Buku",
    list(buku_data.keys())
)

jumlah = st.sidebar.number_input(
    "🔢 Jumlah Buku",
    min_value=1,
    max_value=5,
    value=1
)

tanggal = st.sidebar.date_input("📅 Tanggal Peminjaman")

submit = st.sidebar.button("📚 Pinjam Buku")

st.sidebar.divider()

st.sidebar.success("""
✅ Fitur Aplikasi:
- Peminjaman buku
- Linked List
- Statistik peminjam
- Riwayat peminjaman
- Login admin
- Search data
- Hapus data
""")

# =========================================================
# TAMPILAN BUKU
# =========================================================
st.header("📚 Daftar Buku")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    st.subheader("Laskar Pelangi")

    st.write("✍️ Penulis : Andrea Hirata")
    st.write("📂 Kategori : Novel")
    st.write("📚 Stok : 20 Buku")

    st.success("Buku tersedia")

    st.markdown('</div>', unsafe_allow_html=True)

with col2:

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    st.subheader("Bumi Manusia")

    st.write("✍️ Penulis : Pramoedya Ananta Toer")
    st.write("📂 Kategori : Sejarah")
    st.write("📚 Stok : 15 Buku")

    st.success("Buku tersedia")

    st.markdown('</div>', unsafe_allow_html=True)

with col3:

    st.markdown('<div class="kotak">', unsafe_allow_html=True)

    st.subheader("Atomic Habits")

    st.write("✍️ Penulis : James Clear")
    st.write("📂 Kategori : Self Improvement")
    st.write("📚 Stok : 25 Buku")

    st.success("Buku tersedia")

    st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# =========================================================
# PROSES PEMINJAMAN
# =========================================================
if submit:

    if nama == "":

        st.error("❌ Nama peminjam wajib diisi!")

    else:

        kode = f"PMJ-{len(st.session_state.library.tampilkan_data()) + 1}"

        waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        st.session_state.library.tambah_peminjaman(
            kode,
            nama,
            buku,
            buku_data[buku]["penulis"],
            buku_data[buku]["kategori"],
            jumlah,
            tanggal,
            waktu
        )

        st.success("✅ Buku berhasil dipinjam!")

        st.balloons()

        st.subheader("🧾 Detail Peminjaman")

        kiri, kanan = st.columns(2)

        with kiri:

            st.write(f"🆔 Kode Peminjaman : {kode}")
            st.write(f"👤 Nama : {nama}")
            st.write(f"📖 Buku : {buku}")
            st.write(f"✍️ Penulis : {buku_data[buku]['penulis']}")

        with kanan:

            st.write(f"📂 Kategori : {buku_data[buku]['kategori']}")
            st.write(f"🔢 Jumlah Buku : {jumlah}")
            st.write(f"📅 Tanggal Pinjam : {tanggal}")
            st.write(f"⏰ Waktu Input : {waktu}")

st.divider()

# =========================================================
# KHUSUS ADMIN
# =========================================================
if st.session_state.admin_login:

    st.header("📊 Data Peminjaman Buku")

    data = st.session_state.library.tampilkan_data()

    if data:

        # =================================================
        # SEARCH DATA
        # =================================================
        cari = st.text_input("🔍 Cari Nama Peminjam")

        if cari:

            hasil = []

            for item in data:

                if cari.lower() in item["Nama"].lower():
                    hasil.append(item)

            df = pd.DataFrame(hasil)

        else:

            df = pd.DataFrame(data)

        st.dataframe(
            df,
            use_container_width=True
        )

        # =================================================
        # STATISTIK
        # =================================================
        total_peminjam = len(data)

        total_buku = 0

        current = st.session_state.library.head

        while current:

            total_buku += current.jumlah

            current = current.next

        st.divider()

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "👥 Total Peminjam",
                total_peminjam
            )

        with col2:

            st.metric(
                "📚 Total Buku Dipinjam",
                total_buku
            )

        with col3:

            rata = total_buku / total_peminjam

            st.metric(
                "📈 Rata-rata Pinjaman",
                f"{int(rata)} Buku"
            )

        # =================================================
        # HAPUS DATA
        # =================================================
        st.divider()

        st.subheader("🗑️ Hapus Data Peminjaman")

        kode_hapus = st.text_input("Masukkan Kode Peminjaman")

        if st.button("Hapus Data"):

            hasil = st.session_state.library.hapus_data(kode_hapus)

            if hasil:

                st.success("✅ Data berhasil dihapus!")
                st.rerun()

            else:

                st.error("❌ Kode peminjaman tidak ditemukan!")

    else:

        st.warning("⚠️ Belum ada data peminjaman buku.")

else:

    st.info("👤 User hanya dapat melakukan peminjaman buku.")

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.caption("© 2026 | Project UAS Struktur Data - Perpustakaan")
