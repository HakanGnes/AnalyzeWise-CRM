import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from crm_Project import create_rfm, create_cltv_c, create_cltv_p, check_id, arl_recommender, create_rules

# --- Genel Ayarlar ---
st.set_page_config(page_title="AnalyzeWise CRM", page_icon=":bar_chart:", layout="wide")

# --- Data Yükleme ---
df = pd.read_excel("./CrmData.xlsx")
rfm_df = create_rfm(df)
rfm_df.reset_index(inplace=True)
cltv_p_df = create_cltv_p(df)
cltv_c_df = create_cltv_c(df)
rules = create_rules(df)

# --- Modern Tasarım için Stil ---
st.markdown("""
    <style>
    body { background-color: #f5f7fa; }
    .css-1v0mbdj {background-color: #2368b8;}
    .css-1d391kg {color: #2368b8;}
    .stButton>button { background-color: #23c486; color: white;}
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/CRM-logo.png/600px-CRM-logo.png", width=90)
st.sidebar.title("🔍 Analiz Menüsü")
secenek = st.sidebar.radio(
    "Lütfen bir analiz seçin:",
    (
        "Giriş / Hakkında",
        "RFM Analizi",
        "CLTV - Satın Alma Tahmini",
        "CLTV - Kâr ve Değer Tahmini",
        "CLTV-C Analizi",
        "Ürün Öneri Sistemi"
    )
)

# --- Akademik Giriş Sayfası ---
if secenek == "Giriş / Hakkında":
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/CRM-logo.png/600px-CRM-logo.png", width=120)
    st.title("AnalyzeWise CRM")
    st.markdown("""
    ### Yönetim Bilişim Sistemleri Yüksek Lisans Dönem Projesi

    Bu uygulama, küçük ve orta ölçekli işletmeler için müşteri ilişkileri yönetimi (CRM) süreçlerini analiz etmek ve veri odaklı stratejik kararlar almak amacıyla geliştirilmiştir.  
    Müşteri verilerinin analiz edilmesiyle daha doğru segmentasyon, yaşam boyu değer (CLTV) tahmini, kâr analizi ve ürün öneri sistemi sağlanmaktadır.

    **Başlıca Analiz Modülleri:**
    - 📈 **RFM Analizi:** Müşterileri alışveriş sıklığı, son alışveriş zamanı ve harcama tutarına göre segmentlere ayırır.
    - 💡 **CLTV Analizi:** Müşteri yaşam boyu değerini tahmin ederek, en değerli müşterilere odaklanmanızı sağlar.
    - 💰 **Beklenen Satın Alma & Kâr Tahminleri:** Müşteriler bazında gelecekteki satın alma ve kâr beklentilerini sunar.
    - 🎯 **Ürün Öneri Sistemi:** Birlikte satın alınan ürünlere göre çapraz satış fırsatlarını analiz eder.

    ---

    **Proje Sahibi:** Hakan Güneş  
    **Danışman:** [Danışman İsmi]  
    **Tarih:** 2025  
    """)
    st.info("Sol menüden analiz türünü seçerek uygulamayı kullanmaya başlayabilirsiniz.")

# --- RFM Analizi ---
elif secenek == "RFM Analizi":
    st.header('📈 RFM Analizi')
    secili_segment = st.selectbox('Segment Seçiniz:', rfm_df['segment'].unique())
    filtreli_musteriler = rfm_df[rfm_df['segment'] == secili_segment]['CustomerNo']
    st.write(f"**{secili_segment}** segmentindeki müşteri numaraları (**{len(filtreli_musteriler)}** müşteri):")
    st.write(list(filtreli_musteriler))

    # Segment dağılım grafiği
    segment_sayilari = rfm_df['segment'].value_counts()
    segment_yuzdeleri = segment_sayilari / segment_sayilari.sum() * 100
    secili_segment_yuzde = segment_yuzdeleri[secili_segment]
    diger_segmentler_yuzde = segment_yuzdeleri.drop(index=secili_segment)

    labels = diger_segmentler_yuzde.index.tolist() + [secili_segment]
    sizes = diger_segmentler_yuzde.values.tolist() + [secili_segment_yuzde]
    explode = [0.1 if label == secili_segment else 0 for label in labels]

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')
    st.subheader(f"Seçili Segmentin Dağılımı")
    st.pyplot(fig1)

# --- CLTV - Satın Alma Tahmini ---
elif secenek == "CLTV - Satın Alma Tahmini":
    st.header('💡 CLTV - Beklenen Satın Alma Tahmini')
    secili_segment = st.selectbox('Segment Seçiniz:', cltv_p_df['segment'].unique())
    filtreli_musteriler = cltv_p_df[cltv_p_df['segment'] == secili_segment]['CustomerNo']
    musteri_1 = st.selectbox('Müşteri 1 Seçiniz:', filtreli_musteriler)
    musteri_2 = st.selectbox('Müşteri 2 Seçiniz:', filtreli_musteriler)

    data_1 = cltv_p_df[cltv_p_df['CustomerNo'] == musteri_1]
    data_2 = cltv_p_df[cltv_p_df['CustomerNo'] == musteri_2]
    st.write(f"**{musteri_1}** için Beklenen Satın Alma:")
    st.write("1 hafta:", data_1['expected_purc_1_week'].values[0])
    st.write("1 ay:", data_1['expected_purc_1_month'].values[0])
    st.write("3 ay:", data_1['expected_purc_3_month'].values[0])
    st.write("6 ay:", data_1['expected_purc_6_month'].values[0])
    st.write("9 ay:", data_1['expected_purc_9_month'].values[0])
    st.write("12 ay:", data_1['expected_purc_12_month'].values[0])

    st.write(f"**{musteri_2}** için Beklenen Satın Alma:")
    st.write("1 hafta:", data_2['expected_purc_1_week'].values[0])
    st.write("1 ay:", data_2['expected_purc_1_month'].values[0])
    st.write("3 ay:", data_2['expected_purc_3_month'].values[0])
    st.write("6 ay:", data_2['expected_purc_6_month'].values[0])
    st.write("9 ay:", data_2['expected_purc_9_month'].values[0])
    st.write("12 ay:", data_2['expected_purc_12_month'].values[0])

    karsilastirma = pd.DataFrame({
        'Aylar': ['1 Hafta', '1 Ay', '3 Ay', '6 Ay', '9 Ay', '12 Ay'],
        f'{musteri_1}': [
            data_1['expected_purc_1_week'].values[0],
            data_1['expected_purc_1_month'].values[0],
            data_1['expected_purc_3_month'].values[0],
            data_1['expected_purc_6_month'].values[0],
            data_1['expected_purc_9_month'].values[0],
            data_1['expected_purc_12_month'].values[0],
        ],
        f'{musteri_2}': [
            data_2['expected_purc_1_week'].values[0],
            data_2['expected_purc_1_month'].values[0],
            data_2['expected_purc_3_month'].values[0],
            data_2['expected_purc_6_month'].values[0],
            data_2['expected_purc_9_month'].values[0],
            data_2['expected_purc_12_month'].values[0],
        ]
    })
    karsilastirma['Ortalama'] = karsilastirma.iloc[:, 1:].mean(axis=1)
    karsilastirma = karsilastirma.sort_values(by='Ortalama')
    st.bar_chart(karsilastirma.set_index('Aylar'))

# --- CLTV - Kâr ve Değer Tahmini ---
elif secenek == "CLTV - Kâr ve Değer Tahmini":
    st.header('💰 CLTV - Beklenen Kâr ve Yaşam Boyu Değer')
    secili_segment = st.selectbox('Segment Seçiniz:', cltv_p_df['segment'].unique())
    filtreli_musteriler = cltv_p_df[cltv_p_df['segment'] == secili_segment]['CustomerNo']
    musteri_1 = st.selectbox('Müşteri 1 Seçiniz:', filtreli_musteriler)
    musteri_2 = st.selectbox('Müşteri 2 Seçiniz:', filtreli_musteriler)
    data_1 = cltv_p_df[cltv_p_df['CustomerNo'] == musteri_1]
    data_2 = cltv_p_df[cltv_p_df['CustomerNo'] == musteri_2]
    st.write(f"**{musteri_1}** Bilgileri:")
    st.write("Beklenen Ortalama Kâr:", data_1['expected_average_profit'].values[0])
    st.write("Müşteri Yaşam Boyu Değeri (CLV):", data_1['clv'].values[0])
    st.write("Segment:", data_1['segment'].values[0])

    st.write(f"**{musteri_2}** Bilgileri:")
    st.write("Beklenen Ortalama Kâr:", data_2['expected_average_profit'].values[0])
    st.write("Müşteri Yaşam Boyu Değeri (CLV):", data_2['clv'].values[0])
    st.write("Segment:", data_2['segment'].values[0])

# --- CLTV-C Analizi ---
elif secenek == "CLTV-C Analizi":
    st.header('📊 CLTV-C Analizi')
    secili_segment = st.selectbox('Segment Seçiniz:', cltv_c_df['segment'].unique())
    filtreli_musteriler = cltv_c_df[cltv_c_df['segment'] == secili_segment].index
    musteri = st.selectbox('Müşteri Seçiniz:', filtreli_musteriler)
    data = cltv_c_df.loc[musteri]
    st.write(f"**{musteri}** müşterisinin CLTV-C Analizi:")
    st.write("Toplam İşlem Sayısı:", data['total_transaction'])
    st.write("Toplam Ürün Adedi:", data['total_unit'])
    st.write("Toplam Tutar:", data['total_price'])
    st.write("Ortalama Sipariş Tutarı:", data['avg_order_value'])
    st.write("Satın Alma Sıklığı:", data['purchase_frequency'])
    st.write("Kâr Marjı:", data['profit_margin'])
    st.write("Müşteri Değeri:", data['customer_value'])
    st.write("CLTV-C Değeri:", data['cltv'])
    st.bar_chart({'Seçili Müşteri': data['cltv'], 'Ortalama CLTV': cltv_c_df['cltv'].mean()})

# --- Ürün Öneri Sistemi ---
elif secenek == "Ürün Öneri Sistemi":
    st.header('🎯 Ürün Öneri Sistemi')
    secili_urun = st.selectbox('Ürün Seçiniz:', df['ProductNo'].unique())
    onerilecek_adet = st.slider('Kaç ürün önerisi yapılacak?', 1, 10, 5)
    if st.button('Önerileri Gör'):
        oneriler = arl_recommender(rules, secili_urun, onerilecek_adet)
        st.success(f"**{secili_urun}** için önerilen ürünler:")
        for i, urun in enumerate(oneriler, start=1):
            st.write(f"{i}. Öneri: {urun}")

# --- Alt Bilgi ---
st.markdown("""
---
:bar_chart: AnalyzeWise CRM | © 2025 Hakan Güneş  
Yönetim Bilişim Sistemleri Yüksek Lisans Dönem Projesi
""")




