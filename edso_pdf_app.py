
import streamlit as st
from fpdf import FPDF
from datetime import datetime

st.title("EDSO App - Kuesioner dan Analisis")

# Define 40 questions for 4 hormones (10 each)
questions = {
    "Endorfin": [
        "Saya merasa bersemangat menjalani hari ini.",
        "Saya tetap termotivasi meski menghadapi tantangan.",
        "Saya bisa tetap positif walau banyak tekanan.",
        "Saya sering tertawa atau menikmati humor.",
        "Saya mampu menjalani aktivitas fisik tanpa cepat lelah.",
        "Saya merasa puas setelah menyelesaikan tugas berat.",
        "Saya bisa mengatasi rasa sakit atau ketidaknyamanan.",
        "Saya merasa antusias dalam menjalani rutinitas.",
        "Saya merasa kuat secara fisik dan mental.",
        "Saya tetap berenergi meski kurang tidur."
    ],
    "Dopamin": [
        "Saya merasa puas setelah menyelesaikan tugas.",
        "Saya senang membuat daftar dan mencoret yang selesai.",
        "Saya merasa bahagia saat mencapai target kecil.",
        "Saya termotivasi oleh pencapaian pribadi.",
        "Saya mengejar prestasi dengan antusias.",
        "Saya mudah terdorong oleh reward/hadiah.",
        "Saya merasa bangga terhadap pencapaian saya.",
        "Saya fokus mencapai goal jangka pendek maupun panjang.",
        "Saya suka menyelesaikan tantangan.",
        "Saya senang membuat kemajuan terukur."
    ],
    "Serotonin": [
        "Saya merasa dihargai oleh orang di sekitar.",
        "Saya merasa percaya diri dengan diri sendiri.",
        "Saya merasa memiliki status yang dihormati.",
        "Saya merasa menjadi bagian penting dari tim.",
        "Saya merasa diperlakukan adil oleh lingkungan.",
        "Saya merasa damai dan tenang secara emosi.",
        "Saya merasa mampu mengelola stres.",
        "Saya memiliki kontrol atas keputusan saya.",
        "Saya merasa percaya diri dalam menghadapi konflik.",
        "Saya merasa aman secara sosial dan emosional."
    ],
    "Oksitosin": [
        "Saya merasa terhubung dengan orang lain.",
        "Saya memiliki orang yang bisa saya percaya.",
        "Saya suka membantu orang lain.",
        "Saya merasa nyaman berada dalam kelompok.",
        "Saya merasa empati terhadap orang lain.",
        "Saya merasa dicintai dan diterima.",
        "Saya sering menunjukkan kasih sayang.",
        "Saya percaya orang lain peduli pada saya.",
        "Saya suka berbagi cerita atau pengalaman.",
        "Saya merasa penting untuk menjaga hubungan baik."
    ]
}

# Skor tiap pertanyaan: 1 (Tidak Setuju) - 5 (Sangat Setuju)
skor_total = {}
jawaban = {}
for hormon, qs in questions.items():
    st.subheader(hormon)
    total = 0
    jawaban[hormon] = []
    for i, q in enumerate(qs):
        ans = st.slider(f"{i+1}. {q}", 1, 5, 3, key=f"{hormon}_{i}")
        jawaban[hormon].append(ans)
        total += ans
    skor_total[hormon] = total

# Konversi skor ke kategori: Rendah, Sedang, Tinggi
def kategorikan(skor):
    if skor >= 45:
        return "high"
    elif skor >= 30:
        return "medium"
    else:
        return "low"

kategori = {hormon: kategorikan(skor) for hormon, skor in skor_total.items()}

# Gabungan analisis Endorfin dan Oksitosin
gabungan_analysis = {
    ("high", "high"): "🔥 Sangat bersemangat dan penuh empati. Cocok jadi pemimpin tangguh dan hangat.",
    ("high", "medium"): "💪 Semangat dan cukup sosial, tapi perlu membangun kepercayaan emosional.",
    ("high", "low"): "⚠️ Kuat pribadi tapi kurang empati. Waspadai sikap individualis.",
    ("medium", "high"): "😊 Stabil dan sosial. Gaya kepemimpinan kolaboratif.",
    ("medium", "medium"): "📘 Potensial pemimpin seimbang. Bisa ditingkatkan.",
    ("medium", "low"): "😐 Relasi sosial jadi tantangan. Perlu aktif mendengar.",
    ("low", "high"): "❤️ Dicintai orang lain, tapi semangat rendah. Jaga energi emosional.",
    ("low", "medium"): "💤 Kelelahan dan relasi kurang stabil. Risiko burnout.",
    ("low", "low"): "🚨 Waspadai kelelahan emosional dan keterasingan. Mulai aktivitas sosial ringan."
}
gabungan_result = gabungan_analysis.get(
    (kategori["Endorfin"], kategori["Oksitosin"]), "Analisis gabungan tidak tersedia."
)

st.subheader("Hasil Kategori Hormon")
for h, k in kategori.items():
    st.write(f"{h}: {k.capitalize()}")

st.subheader("Analisa Gabungan Endorfin + Oksitosin")
st.info(gabungan_result)

# Simpan ke PDF manual
if st.button("Download Hasil dalam PDF"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hasil Kuisioner EDSO", ln=True, align="C")
    pdf.cell(200, 10, txt=f"Tanggal: {datetime.now().strftime('%d-%m-%Y')}", ln=True)

    for h in ["Endorfin", "Dopamin", "Serotonin", "Oksitosin"]:
        pdf.cell(200, 10, txt=f"{h}: {kategori[h].capitalize()} (Skor: {skor_total[h]})", ln=True)
    pdf.multi_cell(0, 10, txt=f"Analisa Gabungan: {gabungan_result}")

    pdf.output("hasil_edso.pdf")
    st.success("PDF berhasil dibuat! Silakan unduh dari file explorer lokal (jika dijalankan di PC).")
