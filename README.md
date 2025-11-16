# ⚛️ Fizik Simülatörleri ve Hesaplayıcılar

Kapsamlı, interaktif fizik simülatörleri ve hesaplayıcılar koleksiyonu. Temel fizik ve mühendislik problemlerini çözmek için tasarlanmış, kullanıcı dostu bir web uygulaması.

## 🎯 Özellikler

### 📐 Modül 1: Temel Araçlar ve Vektörler
- **Birim Dönüştürücü**: Uzunluk, kütle, zaman, kuvvet, enerji, hız ve ivme birimleri arası dönüşümler
- **Vektör Hesaplayıcı (2D ve 3D)**:
  - Vektör toplama ve çıkarma (görsel gösterim)
  - Skaler (nokta) çarpım
  - Vektörel (çapraz) çarpım
  - Büyüklük, yön ve birim vektör hesaplama
  - Bileşenlere ayırma ve açı-büyüklük dönüşümleri

### 🏃 Modül 2: Kinematik (Hareket)
- **1D Hareket**: Sabit hız, sabit ivme, serbest düşme
- **2D Atışlar**:
  - Eğik atış simülasyonu (yörünge, maksimum yükseklik, menzil)
  - Yatay atış
  - Nehir problemleri (vektör toplama)
- **Düzgün Dairesel Hareket**: Periyot, frekans, merkezcil kuvvet hesaplamaları

### 💪 Modül 3: Dinamik (Kuvvetler)
- **Newton'un Yasaları**: F = ma hesaplayıcı
- **Sürtünme Kuvveti**: Statik ve kinetik sürtünme
- **Eğik Düzlem Simülasyonu**: Kuvvet analizi ve hareket grafiği
- **Makara Sistemleri**: Atwood düzeneği hesaplayıcı

### ⚡ Modül 4: İş, Güç ve Enerji
- **İş Hesaplayıcı**: W = F·d·cos(θ)
- **Enerji Hesaplayıcıları**: Kinetik, potansiyel (yerçekimsel ve yay)
- **Enerji Korunumu Simülasyonları**:
  - Sarkaç (enerji dönüşümü)
  - Roller coaster (hız treni)
- **Güç Hesaplayıcı**: Watt, kW, beygir gücü dönüşümleri

### 💥 Modül 5: Momentum ve Çarpışmalar
- **Momentum ve İtme Hesaplayıcı**
- **1D Çarpışma Simülasyonları**:
  - Elastik çarpışma
  - Tam inelastik çarpışma
  - Kısmen inelastik çarpışma (restitüsyon katsayısı)
- **2D Çarpışmalar**: Vektörel momentum korunumu

### 🏗️ Modül 6: Statik ve Dönme Hareketi
- **Tork (Moment) Hesaplayıcı**: τ = r × F
- **Statik Denge**: Kiriş problemleri, tepki kuvvetleri
- **Kütle Merkezi Hesaplayıcı**: Nokta kütleler ve geometrik şekiller
- **Eylemsizlik Momenti**: Çubuk, disk, küre, halka
- **Dönme Dinamiği**: τ = Iα, dönme kinetik enerjisi

### 〰️ Modül 7: Salınımlar ve Dalgalar
- **Yay-Kütle Sistemi**: Basit harmonik hareket simülasyonu
  - Konum, hız, ivme grafikleri
  - Enerji dönüşümü (kinetik ↔ potansiyel)
- **Basit Sarkaç**: Periyot, frekans ve enerji analizi

## 🚀 Kurulum ve Çalıştırma

### Yerel Kurulum

1. Repoyu klonlayın:
```bash
git clone https://github.com/alperencanesen/fiziksimulatorleri.git
cd fiziksimulatorleri
```

2. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

3. Uygulamayı çalıştırın:
```bash
streamlit run app.py
```

4. Tarayıcınızda `http://localhost:8501` adresine gidin.

## 🌐 Online Deployment (Streamlit Community Cloud)

### Streamlit Community Cloud'da Yayınlama

Bu uygulama Streamlit Community Cloud'da **ücretsiz** olarak yayınlanabilir.

1. **GitHub Hesabınıza Giriş Yapın**
   - [Streamlit Community Cloud](https://streamlit.io/cloud) sayfasına gidin
   - "Sign in with GitHub" ile giriş yapın

2. **Yeni Uygulama Oluşturun**
   - "New app" butonuna tıklayın
   - Repository: `alperencanesen/fiziksimulatorleri`
   - Branch: `main` veya `claude/physics-simulator-app-01BLbjpButYcD3XrxL3L7ouJ`
   - Main file path: `app.py`
   - "Deploy!" butonuna tıklayın

3. **Uygulama Yayında!**
   - Birkaç dakika içinde uygulamanız `https://fiziksimulatorleri.streamlit.app` benzeri bir adreste yayına girecektir

### Önemli Notlar

- ✅ Streamlit Community Cloud **tamamen ücretsiz**
- ✅ Otomatik HTTPS sertifikası
- ✅ GitHub ile senkronizasyon (her commit'te otomatik güncelleme)
- ⚠️ **GitHub Pages kullanılamaz** (Python backend gerekli)

## 📦 Gereksinimler

- Python 3.8+
- Streamlit 1.31.0
- NumPy 1.24.3
- Matplotlib 3.7.1
- Plotly 5.18.0
- SciPy 1.11.4

## 📖 Kullanım

1. Sol menüden bir modül seçin
2. İlgili sekmeyi açın
3. Parametreleri girin
4. Sonuçları ve görselleştirmeleri inceleyin
5. Simülasyonları interaktif olarak keşfedin!

## 🎓 Eğitim Amaçlı Kullanım

Bu uygulama aşağıdaki amaçlar için idealdir:
- Lise ve üniversite fizik dersleri
- Mühendislik temel dersleri
- Fizik problemlerini görselleştirme
- Öğrenci projeleri ve ödevler
- Öğretmenler için ders materyali

## 🌟 Özellikler

- ✨ Modern ve kullanıcı dostu arayüz
- 📊 Interaktif grafikler ve animasyonlar
- 🎨 Plotly ile profesyonel görselleştirmeler
- 📱 Responsive tasarım (mobil uyumlu)
- 🔢 Gerçek zamanlı hesaplamalar
- 🎯 Türkçe arayüz
- 🔬 7 kapsamlı fizik modülü
- 📐 50+ hesaplayıcı ve simülasyon

## 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz! Lütfen:
1. Fork yapın
2. Feature branch oluşturun (`git checkout -b yeni-ozellik`)
3. Değişikliklerinizi commit edin (`git commit -am 'Yeni özellik ekle'`)
4. Branch'i push edin (`git push origin yeni-ozellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır.

## 👨‍💻 Geliştirici

Temel fizik ve mühendislik hesaplayıcıları - Eğitim amaçlı web uygulaması

## 🐛 Hata Bildirimi

Hata bulursanız veya öneriniz varsa, lütfen [GitHub Issues](https://github.com/alperencanesen/fiziksimulatorleri/issues) sayfasından bildirin.

## 🙏 Teşekkürler

Bu proje fizik ve mühendislik öğrencilerine yardımcı olmak amacıyla geliştirilmiştir.

---

**⭐ Beğendiyseniz yıldız vermeyi unutmayın!**
