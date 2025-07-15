
import streamlit as st
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime  # Perbaikan ditambahkan di sini

# Dummy content untuk demonstrasi (biasanya isi lengkap app)
pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)
pdf.cell(200, 10, txt=f"Tanggal: {datetime.now().strftime('%d-%m-%Y')}", ln=True)
pdf.output("hasil_edso.pdf")
