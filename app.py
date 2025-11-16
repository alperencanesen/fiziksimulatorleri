import streamlit as st
import sys
from pathlib import Path

# Modül yolunu ekle
sys.path.append(str(Path(__file__).parent))

# Sayfa yapılandırması
st.set_page_config(
    page_title="Fizik Simülatörleri",
    page_icon="⚛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS ile özel stil
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .module-header {
        font-size: 2rem;
        font-weight: bold;
        color: #2ca02c;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Ana başlık
st.markdown('<h1 class="main-header">⚛️ Fizik Simülatörleri ve Hesaplayıcılar</h1>', unsafe_allow_html=True)

# Sidebar - Modül seçimi
st.sidebar.title("📚 Modül Seçimi")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Bir modül seçin:",
    [
        "🏠 Ana Sayfa",
        "📐 Modül 1: Temel Araçlar ve Vektörler",
        "🏃 Modül 2: Kinematik (Hareket)",
        "💪 Modül 3: Dinamik (Kuvvetler)",
        "⚡ Modül 4: İş, Güç ve Enerji",
        "💥 Modül 5: Momentum ve Çarpışmalar",
        "🏗️ Modül 6: Statik ve Dönme Hareketi",
        "〰️ Modül 7: Salınımlar ve Dalgalar"
    ]
)

# Modül içeriklerini yükle
if module == "🏠 Ana Sayfa":
    st.markdown("""
    ## Hoş Geldiniz! 👋

    Bu uygulama, temel fizik ve mühendislik problemlerini çözmek için kapsamlı bir araç setidir.

    ### 📋 İçerik:

    - **📐 Modül 1: Temel Araçlar ve Vektörler**
      - Birim dönüştürücü (uzunluk, kütle, zaman, kuvvet, enerji)
      - 2D ve 3D vektör hesaplayıcı (toplama, çıkarma, nokta çarpım, çapraz çarpım)

    - **🏃 Modül 2: Kinematik**
      - 1D hareket (sabit hız, sabit ivme, serbest düşme)
      - 2D hareket (eğik atış, yatay atış, nehir problemleri)
      - Düzgün dairesel hareket

    - **💪 Modül 3: Dinamik**
      - Newton yasaları
      - Sürtünme kuvveti
      - Eğik düzlem simülasyonu
      - Makara sistemleri (Atwood düzeneği)

    - **⚡ Modül 4: İş, Güç ve Enerji**
      - İş hesaplayıcı
      - Kinetik ve potansiyel enerji
      - Sarkaç simülasyonu
      - Roller coaster simülasyonu
      - Güç hesaplayıcı

    - **💥 Modül 5: Momentum ve Çarpışmalar**
      - Momentum ve itme hesaplayıcı
      - Elastik ve inelastik çarpışma simülasyonları
      - Balistik sarkaç

    - **🏗️ Modül 6: Statik ve Dönme**
      - Tork (moment) hesaplayıcı
      - Denge problemleri
      - Kütle merkezi hesaplayıcı
      - Eylemsizlik momenti
      - Dönme hareketi dinamiği

    - **〰️ Modül 7: Salınımlar ve Dalgalar**
      - Basit harmonik hareket
      - Yay-kütle sistemi simülasyonu
      - Basit sarkaç

    ### 🚀 Kullanım

    Sol taraftaki menüden bir modül seçerek başlayın!

    ### 💡 İpucu

    Tüm simülasyonlarda parametreleri değiştirerek sonuçların nasıl değiştiğini gözlemleyebilirsiniz.
    """)

elif module == "📐 Modül 1: Temel Araçlar ve Vektörler":
    from modules import module1_vectors
    module1_vectors.show()

elif module == "🏃 Modül 2: Kinematik (Hareket)":
    from modules import module2_kinematics
    module2_kinematics.show()

elif module == "💪 Modül 3: Dinamik (Kuvvetler)":
    from modules import module3_dynamics
    module3_dynamics.show()

elif module == "⚡ Modül 4: İş, Güç ve Enerji":
    from modules import module4_energy
    module4_energy.show()

elif module == "💥 Modül 5: Momentum ve Çarpışmalar":
    from modules import module5_momentum
    module5_momentum.show()

elif module == "🏗️ Modül 6: Statik ve Dönme Hareketi":
    from modules import module6_statics
    module6_statics.show()

elif module == "〰️ Modül 7: Salınımlar ve Dalgalar":
    from modules import module7_oscillations
    module7_oscillations.show()

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='text-align: center'>
    <p><b>Fizik Simülatörleri v1.0</b></p>
    <p>Temel fizik ve mühendislik hesaplayıcıları</p>
</div>
""", unsafe_allow_html=True)
