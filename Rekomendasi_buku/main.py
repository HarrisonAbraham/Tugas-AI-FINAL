from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI()

# Mencegah error CORS agar file HTML bisa mengakses API Python ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Di production, batasi hanya ke domain website-mu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Load Model AI (Akan diunduh otomatis saat pertama kali dijalankan)
# Model ini sangat ringan, cepat, dan bagus untuk mencari kemiripan teks biasa
model = SentenceTransformer('all-MiniLM-L6-v2')

# 2. Database Buku Sederhana (Bisa kamu ganti atau perluas nantinya)
books_database = [
    {
        "title": "Matematika untuk SMA/MA Kelas X",
        "author": "Dickay Susanto, dkk.",
        "desc": "Buku ini membahas konsep dasar matematika kelas 10 termasuk eksponen, logaritma, barisan dan deret, trigonometri, serta fungsi kuadrat."
    },
    {
        "title": "Bahasa Indonesia: Cerdas Cergas Berbahasa dan Bersastra Indonesia Kelas X",
        "author": "Fadillah Tri Aulia",
        "desc": "Panduan belajar bahasa Indonesia kelas 10 yang berfokus pada teks laporan hasil observasi, anekdot, hikayat, negosiasi, dan biografi."
    },
    {
        "title": "Bahasa Inggris: Work in Progress untuk SMA/SMK/MA Kelas X",
        "author": "Bima M. Bachtiar",
        "desc": "Buku teks bahasa Inggris kelas 10 yang melatih kemampuan produktif dan reseptif siswa melalui berbagai teks fungsional dan naratif."
    },
    {
        "title": "Ilmu Pengetahuan Alam: Fisika untuk SMA Kelas X",
        "author": "Niketan Utama, dkk.",
        "desc": "Materi fisika dasar kelas 10 yang mencakup pengukuran, energi terbarukan, pemanasan global, dan vektor."
    },
    {
        "title": "Ilmu Pengetahuan Alam: Kimia untuk SMA Kelas X",
        "author": "Anna Permanasari, dkk.",
        "desc": "Membahas konsep dasar kimia, struktur atom, tabel periodik unsur, serta hukum-hukum dasar kimia dalam kehidupan sehari-hari."
    },
    {
        "title": "Ilmu Pengetahuan Alam: Biologi untuk SMA Kelas X",
        "author": "Renni Diastuti",
        "desc": "Buku ini mengeksplorasi keanekaragaman hayati, virus dan peranannya, ekosistem, serta perubahan lingkungan."
    },
    {
        "title": "Ilmu Pengetahuan Sosial: Sejarah untuk SMA Kelas X",
        "author": "Sari Oktafiana",
        "desc": "Pengantar ilmu sejarah yang membahas konsep diakronis, sinkronis, serta asal-usul nenek moyang bangsa Indonesia."
    },
    {
        "title": "Ilmu Pengetahuan Sosial: Geografi untuk SMA Kelas X",
        "author": "Budi Handoyo",
        "desc": "Buku ini mengulas pengantar ilmu geografi, peta, penginderaan jauh, sistem informasi geografis, dan fenomena geosfer."
    },
    {
        "title": "Ilmu Pengetahuan Sosial: Sosiologi untuk SMA Kelas X",
        "author": "Joan Hesti Sukmawati",
        "desc": "Membahas pengantar sosiologi, identitas diri, tindakan sosial, interaksi sosial, serta lembaga sosial di masyarakat."
    },
    {
        "title": "Ilmu Pengetahuan Sosial: Ekonomi untuk SMA Kelas X",
        "author": "Eeni Suprapti",
        "desc": "Materi dasar ekonomi mengenai kelangkaan, konsep pasar, lembaga keuangan, serta manajemen dan koperasi."
    },
    {
        "title": "Pendidikan Pancasila dan Kewarganegaraan Kelas X",
        "author": "Tedi Kholiludin, dkk.",
        "desc": "Buku pegangan siswa yang membahas implementasi nilai Pancasila, Undang-Undang Dasar 1945, Bhinneka Tunggal Ika, dan Negara Kesatuan Republik Indonesia."
    },
    {
        "title": "Informatika untuk SMA Kelas X",
        "author": "Iono Joko, dkk.",
        "desc": "Buku ini memperkenalkan berpikir komputasional, teknologi informasi dan komunikasi, sistem komputer, jaringan komputer, dan analisis data."
    },
    {
        "title": "Pendidikan Jasmani, Olahraga, dan Kesehatan Kelas X",
        "author": "Suherman",
        "desc": "Panduan aktivitas fisik, olahraga permainan, atletik, senam, ketahanan jasmani, serta edukasi pola hidup sehat."
    },
    {
        "title": "Seni Budaya: Seni Rupa untuk SMA Kelas X",
        "author": "M. Fadilah",
        "desc": "Membahas apresiasi seni rupa dua dimensi dan tiga dimensi, kritik seni, serta pameran karya seni rupa sekolah."
    },
    {
        "title": "Sejarah Indonesia untuk SMA Kelas X",
        "author": "Restu Gunawan, dkk.",
        "desc": "Menelusuri sejarah Indonesia sejak zaman praaksara, perkembangan kerajaan Hindu-Buddha, hingga masa kerajaan Islam."
    },
    {
        "title": "Matematika Tingkat Lanjut untuk SMA Kelas XI",
        "author": "Al Azhary Masta, dkk.",
        "desc": "Buku matematika peminatan kelas 11 yang membahas bilangan kompleks, polinomial, matriks, transformasi geometri, dan fungsi."
    },
    {
        "title": "Matematika untuk SMA/MA Kelas XI",
        "author": "Dickay Susanto, dkk.",
        "desc": "Buku matematika wajib kelas 11 yang memuat materi tentang komposisi fungsi dan fungsi invers, lingkaran, serta statistika."
    },
    {
        "title": "Bahasa Indonesia: Cerdas Cergas Berbahasa dan Bersastra Indonesia Kelas XI",
        "author": "Heni Marwati",
        "desc": "Materi bahasa Indonesia kelas 11 yang mencakup teks prosedur, eksplanasi, ceramah, cerpen, novel, dan drama."
    },
    {
        "title": "Bahasa Inggris Kelas XI",
        "author": "Siti Nuraini",
        "desc": "Mengembangkan kemampuan berkomunikasi lewat teks eksposisi, surat pribadi, teks naratif, dan diskusi isu sosial aktual."
    },
    {
        "title": "Fisika untuk SMA/MA Kelas XI",
        "author": "Marianna, dkk.",
        "desc": "Materi mendalam tentang kinematika, dinamika rotasi, kesetimbangan benda tegar, elastisitas, fluida statis dan dinamis, serta suhu dan kalor."
    },
    {
        "title": "Kimia untuk SMA/MA Kelas XI",
        "author": "Munasprianto Ramli, dkk.",
        "desc": "Membahas struktur atom dan ikatan kimia, termokimia, laju reaksi, kesetimbangan kimia, serta asam dan basa."
    },
    {
        "title": "Biologi untuk SMA/MA Kelas XI",
        "author": "Rini Solihat, dkk.",
        "desc": "Menjelajahi struktur dan fungsi sel, jaringan tumbuhan dan hewan, sistem gerak, sistem sirkulasi, serta sistem pencernaan manusia."
    },
    {
        "title": "Sejarah untuk SMA Kelas XI",
        "author": "Mina Elfira, dkk.",
        "desc": "Membahas kolonialisme dan perlawanan bangsa Indonesia, pergerakan nasional, pendudukan Jepang, hingga proklamasi kemerdekaan."
    },
    {
        "title": "Geografi untuk SMA Kelas XI",
        "author": "Budi Handoyo",
        "desc": "Fokus pada posisi strategis Indonesia, keanekaragaman hayati global, pengelolaan sumber daya alam, dan mitigasi bencana alam."
    },
    {
        "title": "Sosiologi untuk SMA Kelas XI",
        "author": "Joan Hesti Sukmawati",
        "desc": "Membahas kelompok sosial, permasalahan sosial akibat eksklusi, konflik sosial, serta upaya resolusi dan integrasi sosial."
    },
    {
        "title": "Ekonomi untuk SMA Kelas XI",
        "author": "Yeni Fitriani",
        "desc": "Membahas pendapatan nasional, pertumbuhan dan pembangunan ekonomi, ketenagakerjaan, indeks harga, inflasi, dan kebijakan moneter."
    },
    {
        "title": "Pendidikan Pancasila Kelas XI",
        "author": "Tedi Kholiludin",
        "desc": "Mengkaji konstitusi Indonesia, produk perundang-undangan, budaya hukum, serta tantangan dalam menjaga keutuhan NKRI."
    },
    {
        "title": "Informatika untuk SMA Kelas XI",
        "author": "Irwanto, dkk.",
        "desc": "Melanjutkan pemrograman prosedural, algoritma dan struktur data dasar, dampak sosial informatika, serta proyek analisis data."
    },
    {
        "title": "Antropologi untuk SMA Kelas XI",
        "author": "Okta Hadi Nurcahyono",
        "desc": "Pengantar ilmu antropologi yang mempelajari konsep kebudayaan, diferensiasi sosial, etnografi, dan keragaman budaya Indonesia."
    },
    {
        "title": "Seni Musik untuk SMA Kelas XI",
        "author": "Ahmad Cahyo",
        "desc": "Buku panduan untuk mengapresiasi musik barat dan tradisional, teknik bernyanyi, bermain alat musik, serta pertunjukan musik."
    },
    {
        "title": "Pendidikan Agama Islam dan Budi Pekerti Kelas XI",
        "author": "Mustahdi",
        "desc": "Pembelajaran keimanan kepada kitab-kitab Allah, perilaku syaja'ah (berani membela kebenaran), hormat orang tua, serta sejarah peradaban Islam."
    },
    {
        "title": "Matematika Tingkat Lanjut untuk SMA Kelas XII",
        "author": "Al Azhary Masta",
        "desc": "Materi matematika tingkat lanjut yang mencakup geometri analitik, kalkulus dasar (limit dan turunan), vektor, dan pemodelan matematika."
    },
    {
        "title": "Matematika untuk SMA/MA Kelas XII",
        "author": "Dickay Susanto",
        "desc": "Buku matematika utama kelas 12 yang berfokus pada materi geometri ruang (dimensi tiga) serta penyajian dan ukuran pemusatan data (statistika)."
    },
    {
        "title": "Bahasa Indonesia: Cerdas Cergas Berbahasa dan Bersastra Indonesia Kelas XII",
        "author": "Maman Suryaman",
        "desc": "Mempersiapkan siswa menguasai teks surat lamaran pekerjaan, teks cerita sejarah, editorial, artikel opini, kritik, dan esai sastra."
    },
    {
        "title": "Bahasa Inggris: Life Today untuk SMA Kelas XII",
        "author": "Yuti Rahmawati",
        "desc": "Materi bahasa Inggris kelas 12 yang menekankan pada teks diskusi, ulasan (review text), tips/prosedur kompleks, dan eksposisi analitis."
    },
    {
        "title": "Fisika untuk SMA/MA Kelas XII",
        "author": "Sunardi",
        "desc": "Membahas listrik statis dan dinamis, medan magnet, induksi elektromagnetik, arus bolak-balik, teori relativitas, dan fisika modern."
    },
    {
        "title": "Kimia untuk SMA/MA Kelas XII",
        "author": "Sentot Budi Rahardjo",
        "desc": "Mempelajari sifat koligatif larutan, reaksi redoks dan elektrokimia, kimia unsur (golongan utama dan transisi), serta senyawa turunan alkana."
    },
    {
        "title": "Biologi untuk SMA/MA Kelas XII",
        "author": "Endah Sulistyowati",
        "desc": "Fokus pada materi pertumbuhan dan perkembangan tumbuhan, metabolisme sel (enzim, katabolisme, anabolisme), genetika, dan bioteknologi."
    },
    {
        "title": "Sejarah untuk SMA Kelas XII",
        "author": "Mina Elfira",
        "desc": "Mengulas dinamika politik dan ekonomi Indonesia pasca kemerdekaan, masa Demokrasi Liberal, Demokrasi Terpimpin, Orde Baru, hingga Reformasi."
    },
    {
        "title": "Geografi untuk SMA Kelas XII",
        "author": "Budi Handoyo",
        "desc": "Membahas konsep wilayah dan tata ruang, interaksi spasial desa dan kota, pemanfaatan peta untuk jaringan transportasi, serta kerja sama negara maju-berkembang."
    },
    {
        "title": "Sociologi untuk SMA Kelas XII",
        "author": "Joan Hesti Sukmawati",
        "desc": "Membahas fenomena perubahan sosial di tengah globalisasi, kearifan lokal, ketimpangan sosial, serta pemberdayaan komunitas lokal."
    },
    {
        "title": "Ekonomi untuk SMA Kelas XII",
        "author": "Yeni Fitriani",
        "desc": "Membahas akuntansi sebagai sistem informasi, siklus akuntansi perusahaan jasa, dan siklus akuntansi perusahaan dagang."
    },
    {
        "title": "Pendidikan Pancasila Kelas XII",
        "author": "Tedi Kholiludin",
        "desc": "Mempelajari tentang kasus pelanggaran hak dan pengingkaran kewajiban warga negara, serta perlindungan dan penegakan hukum di Indonesia."
    },
    {
        "title": "Antropologi untuk SMA Kelas XII",
        "author": "Okta Hadi Nurcahyono",
        "desc": "Membahas perubahan sosial-budaya dalam masyarakat, integrasi nasional, dampak globalisasi, dan penelitian antropologi sederhana."
    },
    {
        "title": "Prakarya dan Kewirausahaan: Kerajinan Kelas XII",
        "author": "Hendriana Werdhaningsih",
        "desc": "Panduan perencanaan, produksi, perhitungan harga jual, dan strategi pemasaran produk kerajinan untuk pasar lokal maupun internasional."
    },
    {
        "title": "Seni Teater untuk SMA Kelas XII",
        "author": "Aditya Tri",
        "desc": "Membahas konsep teater modern, manajemen produksi pementasan teater, penulisan naskah drama, hingga teknik keaktoran."
    },
    {
        "title": "Pendidikan Agama Kristen dan Budi Pekerti Kelas X",
        "author": "Julia Suleeman",
        "desc": "Membahas konsep pertumbuhan diri menjadi dewasa secara rohani, tanggung jawab remaja Kristen dalam keluarga, gereja, dan masyarakat."
    },
    {
        "title": "Sejarah Dunia Modern Kelas XI",
        "author": "I Wayan Badrika",
        "desc": "Buku sejarah peminatan kelas 11 yang mengulas peristiwa besar dunia seperti Renaisans, Revolusi Industri, Revolusi Prancis, dan Perang Dunia."
    },
    {
        "title": "Bahasa dan Sastra Indonesia Kelas XII",
        "author": "Engkos Kosasih",
        "desc": "Buku peminatan kelas 12 yang mendalami karakteristik karya sastra angkatan pujangga baru hingga angkatan reformasi, serta kritik esai."
    },
    {
        "title": "Bahasa Inggris Tingkat Lanjut Kelas XI",
        "author": "Anik Muslikah",
        "desc": "Buku pengayaan bahasa Inggris untuk kelas 11 yang fokus pada teks fabel, legenda, puisi, dan esai eksposisi analitis tingkat mahir."
    }
]

# 3. Ubah semua deskripsi buku menjadi Vektor (Embedding) saat server dinyalakan
book_descriptions = [book['desc'] for book in books_database]
book_embeddings = model.encode(book_descriptions, convert_to_tensor=True)


# Schema untuk data input dari frontend
class SearchQuery(BaseModel):
    text: str

# 4. Membuat Endpoint API untuk Rekomendasi
@app.post("/recommend")
def get_recommendation(query: SearchQuery):
    # Ubah input user menjadi vektor
    user_embedding = model.encode(query.text, convert_to_tensor=True)
    
    # Hitung nilai kemiripan (Cosine Similarity) antara input user dengan semua buku
    cosine_scores = util.cos_sim(user_embedding, book_embeddings)[0]
    
    # Urutkan dari nilai tertinggi ke terendah
    top_results = cosine_scores.argsort(descending=True)
    
    rekomendasi = []
    # Ambil 3 hasil teratas
    for idx in top_results[:3]:
        score = cosine_scores[idx].item()
        
        # Masukkan data buku disertai persentase kemiripannya
        buku = books_database[idx].copy()
        # buku["match"] = f"{int(score * 100)}%"
        buku["match"] = f"{int(score * 100)}%"
        rekomendasi.append(buku)
        
    return {"results": rekomendasi}