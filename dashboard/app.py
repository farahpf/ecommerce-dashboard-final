import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("main_data.csv", encoding = "latin-1")
        return df
    except Exception as e:
        st.error(f"Gagal memuat data: {e}")
        return None
#Muat Data 
df = load_data()

if df is None:
    st.error("Data tidak dapat dimuat!. Periksa file main_data.csv dan encodingnya.")
    st.stop()

#Judul
st.title("Dashboard Analisis E-Commerce")
st.write(f"Dataset memuat **{df.shape[0]} baris** dan **{df.shape[1]} kolom**.")
st.write("---")

#Sidebar
st.sidebar.header("Filter")
selected_state = st.sidebar.selectbox("Pilih Negara Bagian:", df["customer_state"].dropna().unique())

#Filtered Data 
filtered_df = df[df["customer_state"] == selected_state]

# Layout
st.subheader(f"Jumlah Pelanggan dan Penjual di {selected_state}")
col1, col2 = st.columns(2)

with col1:
    customer_counts = filtered_df["customer_state"].value_counts()
    st.metric(label="Jumlah Pelanggan", value=customer_counts.sum())

with col2:
    seller_counts = filtered_df["seller_state"].value_counts()
    st.metric(label="Jumlah Penjual", value=seller_counts.sum())

# Analisis Pertanyaan 1: Negara bagian dengan pelanggan dan penjual terbanyak
st.subheader(f"Jumlah Pelanggan & Penjual di {selected_state}")
customer_counts = filtered_df["customer_state"].value_counts()
seller_counts = filtered_df["seller_state"].value_counts()
fig, ax = plt.subplots(figsize=(10, 5))
customer_counts.plot(kind="bar", color='blue', alpha=0.7, label='Pelanggan', ax=ax)
seller_counts.plot(kind="bar", color='red', alpha=0.7, label='Penjual', ax=ax)
ax.set_xlabel("Negara Bagian")
ax.set_ylabel("Jumlah")
ax.set_title("Jumlah Pelanggan & Penjual")
ax.legend()
st.pyplot(fig)
# Insight Analisis Pertanyaan 1
st.markdown(
    f"**Insight Analisis Pertanyaan 1 :** Di {selected_state}, perbandingan jumlah pelanggan dan penjual menunjukkan \"{'lebih banyak penjual daripada pelanggan' if seller_counts.sum() > customer_counts.sum() else 'lebih banyak pelanggan daripada penjual'}\". Hal ini dapat mengindikasikan potensi persaingan pasar yang {'ketat' if seller_counts.sum() > customer_counts.sum() else 'rendah'} di wilayah tersebut."
)
# Analisis Pertanyaan 2: Distribusi jumlah pesanan berdasarkan status pesanan
st.subheader("Distribusi Status Pesanan")
status_counts = df["order_status"].value_counts()
fig2, ax2 = plt.subplots()
sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis', ax=ax2)
ax2.set_xlabel("Status Pesanan")
ax2.set_ylabel("Jumlah Pesanan")
st.pyplot(fig2)

st.write("---")

# Insight Analisis Pertanyaan 2
total_orders = status_counts.sum()
most_common = status_counts.idxmax()
percentage = status_counts.max() / total_orders * 100
st.markdown(
    f"**Insight Analisis Pertanyaan 2 :** Dari total {total_orders:,} pesanan, status **{most_common}** mendominasi sekitar {percentage:.1f}% dari keseluruhan. Ini menandakan tingkat keberhasilan pengiriman yang tinggi, namun perlu diperhatikan juga bahwa ada sekitar {100 - percentage:.1f}% pesanan dengan status lain, termasuk dibatalkan atau tertunda."
)

# Analisis Pertanyaan 3: Pola transaksi harian berdasarkan pesanan yang disetujui
st.subheader("Pola Transaksi Harian")
df["order_approved_at"] = pd.to_datetime(df["order_approved_at"], errors='coerce')
daily_orders = df.groupby(df["order_approved_at"].dt.date).size()
st.line_chart(daily_orders)
st.write("---")

#Insight Analisis Pertanyaan 3
peak_date = daily_orders.idxmax()
peak_value = daily_orders.max()
avg_orders = daily_orders.mean()
st.markdown(
    f"**Insight Analisis Pertanyaan 3 :** Puncak transaksi harian terjadi pada **{peak_date}** dengan {peak_value} pesanan. Rata-rata transaksi harian adalah sekitar {avg_orders:.0f} pesanan, menunjukkan fluktuasi yang perlu dipantau untuk mengatur kapasitas logistik dan layanan pelanggan."
)

# Menutup aplikasi
st.write("---")
st.write("Dashboard ini dibuat oleh Farah Putri Firdausa A278XAF155")
