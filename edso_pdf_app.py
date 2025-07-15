
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF
import tempfile
import base64
from datetime import datetime

st.title("📋 Kuesioner E.D.S.O dan Laporan PDF")

name = st.text_input("Nama lengkap")
email = st.text_input("Alamat Email")

st.markdown("Jawab 40 pertanyaan berikut dengan skala 1 = Tidak Setuju sampai 5 = Sangat Setuju")

def ask_questions(hormon, questions):
    st.subheader(hormon)
    scores = []
    for i, q in enumerate(questions):
        scores.append(st.slider(f"{hormon} {i+1}. {q}", 1, 5, 3))
    return scores

endorfin_qs = ["Saya merasa lebih baik setelah tertawa.",
    "Saya rutin berolahraga untuk meningkatkan mood.",
    "Saya bisa tetap tenang saat mengalami rasa sakit.",
    "Saya menikmati aktivitas yang memicu keringat.",
    "Saya merasa segar setelah aktivitas fisik.",
    "Saya suka mencari hiburan untuk menghilangkan stres.",
    "Saya merasa lega setelah menangis.",
    "Saya suka suasana ceria.",
    "Saya bisa melihat sisi lucu dalam situasi sulit.",
    "Saya mudah tertawa bersama orang lain."]

dopamin_qs = ["Saya merasa puas setelah menyelesaikan target.",
    "Saya termotivasi dengan tantangan.",
    "Saya merasa senang mencentang to-do list.",
    "Saya suka membuat rencana kerja.",
    "Saya sering memecah tugas besar menjadi tugas kecil.",
    "Saya fokus pada pencapaian.",
    "Saya punya semangat tinggi saat mengejar tujuan.",
    "Saya merasa senang saat mendapat pengakuan.",
    "Saya merasa terdorong saat melihat progres kerja.",
    "Saya suka mengevaluasi pencapaian saya."]

serotonin_qs = ["Saya merasa dihargai oleh rekan kerja.",
    "Saya merasa dipercaya oleh orang-orang sekitar saya.",
    "Saya merasa bangga jika memberi kontribusi positif.",
    "Saya merasa senang saat nama saya disebut secara positif.",
    "Saya suka memberi dukungan kepada orang lain.",
    "Saya bangga jika bisa memimpin dengan adil.",
    "Saya merasa nyaman saat ide saya diterima.",
    "Saya berusaha membuat orang merasa dihargai.",
    "Saya merasa senang saat dipercaya memegang tanggung jawab.",
    "Saya suka menjadi bagian dari sesuatu yang lebih besar."]

oksitosin_qs = ["Saya nyaman membangun hubungan yang tulus.",
    "Saya suka membantu tanpa pamrih.",
    "Saya merasa tenang berada di dekat orang yang saya percaya.",
    "Saya terbuka terhadap perasaan orang lain.",
    "Saya suka menyapa atau menyemangati orang lain.",
    "Saya menikmati kerja tim yang harmonis.",
    "Saya sering berempati terhadap kesulitan orang lain.",
    "Saya suka suasana kerja yang hangat.",
    "Saya merasa senang saat ada kontak emosional yang kuat.",
    "Saya merasa puas jika bisa membuat orang lain nyaman."]

end_scores = ask_questions("Endorfin", endorfin_qs)
dop_scores = ask_questions("Dopamin", dopamin_qs)
ser_scores = ask_questions("Serotonin", serotonin_qs)
oks_scores = ask_questions("Oksitosin", oksitosin_qs)

avg_end = np.mean(end_scores)
avg_dop = np.mean(dop_scores)
avg_ser = np.mean(ser_scores)
avg_oks = np.mean(oks_scores)

def classify(score):
    if score >= 8:
        return "high"
    elif score >= 6:
        return "medium"
    else:
        return "low"

# Radar chart
labels = ['Endorfin', 'Dopamin', 'Serotonin', 'Oksitosin']
values = [avg_end, avg_dop, avg_ser, avg_oks]
values += values[:1]
angles = [n / float(len(labels)) * 2 * np.pi for n in range(len(labels))]
angles += angles[:1]

fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
ax.plot(angles, values, linewidth=2)
ax.fill(angles, values, alpha=0.3)
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)
ax.set_yticklabels(["1", "2", "3", "4", "5"])
ax.set_title("Diagram Keseimbangan Hormon E.D.S.O")
chart_path = tempfile.NamedTemporaryFile(suffix=".png", delete=False).name
plt.savefig(chart_path)
st.pyplot(fig)

# Template rekomendasi
recommendation_template = {
    "Endorfin": {
        "high": ("Tinggi", "Kamu memiliki daya tahan mental yang kuat dan mampu mengelola stres dengan baik."),
        "medium": ("Cukup", "Kamu cukup tangguh, namun bisa ditingkatkan dengan olahraga dan menjaga semangat."),
        "low": ("Rendah", "Tingkatkan endorfin dengan berolahraga dan banyak tertawa.")
    },
    "Dopamin": {
        "high": ("Tinggi", "Kamu sangat termotivasi oleh target dan pencapaian."),
        "medium": ("Cukup", "Motivasi pribadi cukup baik, gunakan sistem reward."),
        "low": ("Rendah", "Perkuat motivasi dengan membuat tujuan jangka pendek.")
    },
    "Serotonin": {
        "high": ("Tinggi", "Kamu percaya diri dan dihargai."),
        "medium": ("Cukup", "Cukup dihargai, bisa lebih baik dengan meningkatkan apresiasi."),
        "low": ("Rendah", "Bangun rasa percaya diri dan minta umpan balik positif.")
    },
    "Oksitosin": {
        "high": ("Tinggi", "Kamu punya koneksi sosial yang kuat."),
        "medium": ("Cukup", "Hubungan sosial cukup, pertahankan dan tingkatkan."),
        "low": ("Rendah", "Bangun empati dan lingkungan kerja yang terbuka.")
    }
}

def analyze_score(name, score):
    level = classify(score)
    return recommendation_template[name][level]

# Gabungan endorfin + oksitosin
eo_combo = (classify(avg_end), classify(avg_oks))
combined_notes = {('high', 'high'): '🔥 Kamu adalah sosok yang sangat bersemangat dan penuh empati. Pemimpin tangguh yang peduli pada tim. Cocok untuk peran yang intensif dan berbasis hubungan.', ('high', 'medium'): '💪 Kamu semangat dan cukup sosial, tapi perlu lebih banyak membangun kepercayaan emosional.', ('high', 'low'): '⚠️ Sangat kuat secara pribadi, namun kurang empati. Waspadai sikap individualis. Coba hadir lebih untuk tim.', ('medium', 'high'): '😊 Stabil dan sosial. Gaya kepemimpinan mendukung dan kolaboratif.', ('medium', 'medium'): '📘 Berada di tengah. Potensial menjadi pemimpin seimbang, masih bisa ditingkatkan.', ('medium', 'low'): '😐 Relasi sosial jadi tantangan. Perlu lebih aktif mendengar dan empati.', ('low', 'high'): '❤️ Dicintai dan dipercaya orang lain, tapi semangat rendah. Jaga energi emosionalmu.', ('low', 'medium'): '💤 Kelelahan dan relasi sosial kurang stabil. Berisiko burnout.', ('low', 'low'): '🚨 Waspadai kelelahan emosional dan keterasingan. Mulailah dari aktivitas menyenangkan bersama orang lain.'}
    ("high", "high"): "🔥 Sangat bersemangat dan penuh empati. Cocok jadi pemimpin tangguh dan hangat.",
    ("high", "medium"): "💪 Semangat tinggi, cukup sosial. Tingkatkan koneksi emosional.",
    ("high", "low"): "⚠️ Tangguh tapi cenderung individualis. Perlu bangun hubungan sosial.",
    ("medium", "high"): "😊 Stabil dan hangat. Pemimpin kolaboratif.",
    ("medium", "medium"): "📘 Seimbang, masih bisa ditingkatkan.",
    ("medium", "low"): "😐 Sosial jadi tantangan. Perlu aktif membangun empati.",
    ("low", "high"): "❤️ Dicintai tapi kurang energi. Jaga stamina emosional.",
    ("low", "medium"): "😴 Kurang semangat dan kurang relasi sosial.",
    ("low", "low"): "🚨 Rentan burnout dan keterasingan. Mulai dari aktivitas menyenangkan."
}

# Tampilkan hasil
if st.button("Download Hasil dalam PDF"):
    hasil = {
        "Endorfin": analyze_score("Endorfin", avg_end),
        "Dopamin": analyze_score("Dopamin", avg_dop),
        "Serotonin": analyze_score("Serotonin", avg_ser),
        "Oksitosin": analyze_score("Oksitosin", avg_oks)
    }

    st.subheader("📊 Hasil Ringkasan")
    for k, v in hasil.items():
        st.markdown(f"**{k}** – {v[0]}: {v[1]}")
    st.markdown("### 🔄 Analisis Gabungan Endorfin + Oksitosin")
    st.info(combined_notes[eo_combo])

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hasil Kuisioner E.D.S.O", ln=True, align='C')
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Nama: {name}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True)
    pdf.cell(200, 10, txt=f"Tanggal: {datetime.now().strftime('%d-%m-%Y')}", ln=True)
    pdf.ln(5)
    for k, v in hasil.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, f"{k} – {v[0]}", ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 10, v[1])
    pdf.ln(3)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Analisis Gabungan (Endorfin + Oksitosin):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 10, combined_notes[eo_combo])
    pdf.image(chart_path, x=10, y=None, w=180)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf.output(tmp.name)
        with open(tmp.name, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="Laporan_EDSO_{name}.pdf">📥 Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
