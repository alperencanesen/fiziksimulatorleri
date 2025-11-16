import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def show():
    st.markdown('<h2 class="module-header">📐 Modül 1: Temel Araçlar ve Vektörler</h2>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔄 Birim Dönüştürücü", "📊 Vektör Hesaplayıcı"])

    # TAB 1: Birim Dönüştürücü
    with tab1:
        st.subheader("🔄 Birim Dönüştürücü")

        birim_kategorisi = st.selectbox(
            "Kategori seçin:",
            ["Uzunluk", "Kütle", "Zaman", "Kuvvet", "Enerji", "Hız", "İvme"]
        )

        # Birim dönüşüm tanımları (her şey SI birimine göre)
        birimler = {
            "Uzunluk": {
                "metre (m)": 1,
                "kilometre (km)": 1000,
                "santimetre (cm)": 0.01,
                "milimetre (mm)": 0.001,
                "feet (ft)": 0.3048,
                "inç (in)": 0.0254,
                "mil (mi)": 1609.34
            },
            "Kütle": {
                "kilogram (kg)": 1,
                "gram (g)": 0.001,
                "ton": 1000,
                "pound (lb)": 0.453592,
                "ons (oz)": 0.0283495
            },
            "Zaman": {
                "saniye (s)": 1,
                "dakika (dk)": 60,
                "saat (sa)": 3600,
                "gün": 86400,
                "yıl": 31536000
            },
            "Kuvvet": {
                "Newton (N)": 1,
                "kilonewton (kN)": 1000,
                "pound-force (lbf)": 4.44822,
                "dyne": 1e-5
            },
            "Enerji": {
                "Joule (J)": 1,
                "kilojoule (kJ)": 1000,
                "kalori (cal)": 4.184,
                "kilokalori (kcal)": 4184,
                "kilowatt-saat (kWh)": 3.6e6,
                "elektron-volt (eV)": 1.602e-19
            },
            "Hız": {
                "metre/saniye (m/s)": 1,
                "kilometre/saat (km/h)": 0.277778,
                "mil/saat (mph)": 0.44704,
                "knot": 0.514444
            },
            "İvme": {
                "metre/saniye² (m/s²)": 1,
                "g (yerçekimi ivmesi)": 9.80665,
                "feet/saniye² (ft/s²)": 0.3048
            }
        }

        birim_secenekleri = list(birimler[birim_kategorisi].keys())

        col1, col2 = st.columns(2)

        with col1:
            kaynak_birim = st.selectbox("Kaynak birim:", birim_secenekleri, key="kaynak")
            deger = st.number_input("Değer:", value=1.0, format="%.6f")

        with col2:
            hedef_birim = st.selectbox("Hedef birim:", birim_secenekleri, key="hedef")

        # Dönüşüm hesaplama
        kaynak_carpan = birimler[birim_kategorisi][kaynak_birim]
        hedef_carpan = birimler[birim_kategorisi][hedef_birim]
        sonuc = deger * (kaynak_carpan / hedef_carpan)

        st.success(f"**Sonuç:** {deger} {kaynak_birim} = **{sonuc:.6f}** {hedef_birim}")

    # TAB 2: Vektör Hesaplayıcı
    with tab2:
        st.subheader("📊 Vektör Hesaplayıcı")

        boyut = st.radio("Vektör boyutu:", ["2D", "3D"], horizontal=True)

        islem = st.selectbox(
            "İşlem seçin:",
            [
                "Vektör Toplama (A + B)",
                "Vektör Çıkarma (A - B)",
                "Skaler (Nokta) Çarpım (A · B)",
                "Vektörel (Çapraz) Çarpım (A × B)",
                "Vektör Büyüklüğü",
                "Birim Vektör",
                "Bileşenlerden Büyüklük ve Yön",
                "Açı ve Büyüklükten Bileşenler"
            ]
        )

        if islem in ["Vektör Toplama (A + B)", "Vektör Çıkarma (A - B)", "Skaler (Nokta) Çarpım (A · B)", "Vektörel (Çapraz) Çarpım (A × B)"]:
            col1, col2 = st.columns(2)

            with col1:
                st.write("**Vektör A:**")
                Ax = st.number_input("Ax:", value=3.0, format="%.3f", key="ax")
                Ay = st.number_input("Ay:", value=4.0, format="%.3f", key="ay")
                if boyut == "3D":
                    Az = st.number_input("Az:", value=0.0, format="%.3f", key="az")
                else:
                    Az = 0

            with col2:
                st.write("**Vektör B:**")
                Bx = st.number_input("Bx:", value=1.0, format="%.3f", key="bx")
                By = st.number_input("By:", value=2.0, format="%.3f", key="by")
                if boyut == "3D":
                    Bz = st.number_input("Bz:", value=0.0, format="%.3f", key="bz")
                else:
                    Bz = 0

            A = np.array([Ax, Ay, Az])
            B = np.array([Bx, By, Bz])

            if islem == "Vektör Toplama (A + B)":
                C = A + B
                st.success(f"**A + B = ({C[0]:.3f}, {C[1]:.3f}" + (f", {C[2]:.3f})" if boyut == "3D" else ")"))

                # Görselleştirme
                if boyut == "2D":
                    fig = go.Figure()

                    # Vektör A
                    fig.add_trace(go.Scatter(
                        x=[0, Ax], y=[0, Ay],
                        mode='lines+markers',
                        name='Vektör A',
                        line=dict(color='blue', width=3),
                        marker=dict(size=8)
                    ))

                    # Vektör B (A'nın ucundan başlayarak)
                    fig.add_trace(go.Scatter(
                        x=[Ax, Ax+Bx], y=[Ay, Ay+By],
                        mode='lines+markers',
                        name='Vektör B',
                        line=dict(color='red', width=3),
                        marker=dict(size=8)
                    ))

                    # Sonuç vektörü C
                    fig.add_trace(go.Scatter(
                        x=[0, C[0]], y=[0, C[1]],
                        mode='lines+markers',
                        name='Sonuç (A+B)',
                        line=dict(color='green', width=4, dash='dash'),
                        marker=dict(size=10)
                    ))

                    fig.update_layout(
                        title="Vektör Toplama (Uç Uca Ekleme Yöntemi)",
                        xaxis_title="X",
                        yaxis_title="Y",
                        showlegend=True,
                        width=700,
                        height=500,
                        xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black'),
                        yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
                    )

                    st.plotly_chart(fig)

                else:  # 3D
                    fig = go.Figure()

                    # Vektör A
                    fig.add_trace(go.Scatter3d(
                        x=[0, Ax], y=[0, Ay], z=[0, Az],
                        mode='lines+markers',
                        name='Vektör A',
                        line=dict(color='blue', width=6),
                        marker=dict(size=5)
                    ))

                    # Vektör B
                    fig.add_trace(go.Scatter3d(
                        x=[Ax, Ax+Bx], y=[Ay, Ay+By], z=[Az, Az+Bz],
                        mode='lines+markers',
                        name='Vektör B',
                        line=dict(color='red', width=6),
                        marker=dict(size=5)
                    ))

                    # Sonuç vektörü
                    fig.add_trace(go.Scatter3d(
                        x=[0, C[0]], y=[0, C[1]], z=[0, C[2]],
                        mode='lines+markers',
                        name='Sonuç (A+B)',
                        line=dict(color='green', width=8, dash='dash'),
                        marker=dict(size=7)
                    ))

                    fig.update_layout(
                        title="3D Vektör Toplama",
                        scene=dict(
                            xaxis_title="X",
                            yaxis_title="Y",
                            zaxis_title="Z"
                        ),
                        showlegend=True,
                        width=700,
                        height=600
                    )

                    st.plotly_chart(fig)

            elif islem == "Vektör Çıkarma (A - B)":
                C = A - B
                st.success(f"**A - B = ({C[0]:.3f}, {C[1]:.3f}" + (f", {C[2]:.3f})" if boyut == "3D" else ")"))

            elif islem == "Skaler (Nokta) Çarpım (A · B)":
                if boyut == "2D":
                    dot_product = Ax*Bx + Ay*By
                else:
                    dot_product = np.dot(A, B)

                # Açı hesaplama
                mag_A = np.linalg.norm(A)
                mag_B = np.linalg.norm(B)
                if mag_A > 0 and mag_B > 0:
                    cos_theta = dot_product / (mag_A * mag_B)
                    cos_theta = np.clip(cos_theta, -1, 1)  # Numerik hata düzeltmesi
                    angle_rad = np.arccos(cos_theta)
                    angle_deg = np.degrees(angle_rad)

                    st.success(f"**A · B = {dot_product:.3f}**")
                    st.info(f"Vektörler arası açı: {angle_deg:.2f}° ({angle_rad:.3f} radyan)")
                else:
                    st.success(f"**A · B = {dot_product:.3f}**")

            elif islem == "Vektörel (Çapraz) Çarpım (A × B)":
                if boyut == "2D":
                    st.warning("Çapraz çarpım 3D vektörler için tanımlıdır. 2D için boyut seçeneğini 3D yapın.")
                else:
                    C = np.cross(A, B)
                    st.success(f"**A × B = ({C[0]:.3f}, {C[1]:.3f}, {C[2]:.3f})**")
                    st.info(f"Büyüklük: {np.linalg.norm(C):.3f}")

                    # 3D görselleştirme
                    fig = go.Figure()

                    # Vektör A
                    fig.add_trace(go.Scatter3d(
                        x=[0, Ax], y=[0, Ay], z=[0, Az],
                        mode='lines+markers',
                        name='Vektör A',
                        line=dict(color='blue', width=6),
                        marker=dict(size=5)
                    ))

                    # Vektör B
                    fig.add_trace(go.Scatter3d(
                        x=[0, Bx], y=[0, By], z=[0, Bz],
                        mode='lines+markers',
                        name='Vektör B',
                        line=dict(color='red', width=6),
                        marker=dict(size=5)
                    ))

                    # Çapraz çarpım sonucu
                    fig.add_trace(go.Scatter3d(
                        x=[0, C[0]], y=[0, C[1]], z=[0, C[2]],
                        mode='lines+markers',
                        name='A × B (Her ikisine de dik)',
                        line=dict(color='purple', width=8),
                        marker=dict(size=7)
                    ))

                    fig.update_layout(
                        title="Vektörel (Çapraz) Çarpım",
                        scene=dict(
                            xaxis_title="X",
                            yaxis_title="Y",
                            zaxis_title="Z"
                        ),
                        showlegend=True,
                        width=700,
                        height=600
                    )

                    st.plotly_chart(fig)

        elif islem == "Vektör Büyüklüğü":
            st.write("**Vektör bileşenlerini girin:**")
            Vx = st.number_input("Vx:", value=3.0, format="%.3f")
            Vy = st.number_input("Vy:", value=4.0, format="%.3f")
            if boyut == "3D":
                Vz = st.number_input("Vz:", value=0.0, format="%.3f")
            else:
                Vz = 0

            V = np.array([Vx, Vy, Vz])
            magnitude = np.linalg.norm(V)

            if boyut == "2D":
                st.success(f"**|V| = √({Vx}² + {Vy}²) = {magnitude:.3f}**")
            else:
                st.success(f"**|V| = √({Vx}² + {Vy}² + {Vz}²) = {magnitude:.3f}**")

        elif islem == "Birim Vektör":
            st.write("**Vektör bileşenlerini girin:**")
            Vx = st.number_input("Vx:", value=3.0, format="%.3f")
            Vy = st.number_input("Vy:", value=4.0, format="%.3f")
            if boyut == "3D":
                Vz = st.number_input("Vz:", value=5.0, format="%.3f")
            else:
                Vz = 0

            V = np.array([Vx, Vy, Vz])
            magnitude = np.linalg.norm(V)

            if magnitude > 0:
                unit_vector = V / magnitude
                st.success(f"**Birim vektör: ({unit_vector[0]:.3f}, {unit_vector[1]:.3f}" +
                          (f", {unit_vector[2]:.3f})" if boyut == "3D" else ")"))
                st.info(f"Orijinal büyüklük: {magnitude:.3f}")
            else:
                st.error("Sıfır vektörünün birim vektörü tanımsızdır.")

        elif islem == "Bileşenlerden Büyüklük ve Yön":
            if boyut == "2D":
                Vx = st.number_input("Vx:", value=3.0, format="%.3f")
                Vy = st.number_input("Vy:", value=4.0, format="%.3f")

                magnitude = np.sqrt(Vx**2 + Vy**2)
                angle_rad = np.arctan2(Vy, Vx)
                angle_deg = np.degrees(angle_rad)

                st.success(f"**Büyüklük:** {magnitude:.3f}")
                st.success(f"**Açı (x ekseninden):** {angle_deg:.2f}° ({angle_rad:.3f} radyan)")

                # Görselleştirme
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=[0, Vx], y=[0, Vy],
                    mode='lines+markers',
                    name='Vektör V',
                    line=dict(color='blue', width=4),
                    marker=dict(size=10)
                ))

                # Açı gösterimi
                theta = np.linspace(0, angle_rad, 50)
                arc_r = magnitude * 0.2
                fig.add_trace(go.Scatter(
                    x=arc_r * np.cos(theta),
                    y=arc_r * np.sin(theta),
                    mode='lines',
                    name=f'Açı: {angle_deg:.1f}°',
                    line=dict(color='red', width=2, dash='dash')
                ))

                fig.update_layout(
                    title=f"Vektör: Büyüklük={magnitude:.2f}, Açı={angle_deg:.1f}°",
                    xaxis_title="X",
                    yaxis_title="Y",
                    showlegend=True,
                    width=600,
                    height=500,
                    xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black'),
                    yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
                )

                st.plotly_chart(fig)
            else:
                st.info("3D için küresel koordinatlara dönüşüm:")
                Vx = st.number_input("Vx:", value=1.0, format="%.3f")
                Vy = st.number_input("Vy:", value=1.0, format="%.3f")
                Vz = st.number_input("Vz:", value=1.0, format="%.3f")

                r = np.sqrt(Vx**2 + Vy**2 + Vz**2)
                theta = np.arccos(Vz / r) if r > 0 else 0  # Polar açı
                phi = np.arctan2(Vy, Vx)  # Azimuthal açı

                st.success(f"**Büyüklük (r):** {r:.3f}")
                st.success(f"**Polar açı (θ):** {np.degrees(theta):.2f}° ({theta:.3f} rad)")
                st.success(f"**Azimuthal açı (φ):** {np.degrees(phi):.2f}° ({phi:.3f} rad)")

        elif islem == "Açı ve Büyüklükten Bileşenler":
            if boyut == "2D":
                magnitude = st.number_input("Büyüklük:", value=5.0, format="%.3f", min_value=0.0)
                angle_deg = st.number_input("Açı (derece, x ekseninden):", value=53.13, format="%.2f")

                angle_rad = np.radians(angle_deg)
                Vx = magnitude * np.cos(angle_rad)
                Vy = magnitude * np.sin(angle_rad)

                st.success(f"**Vx = {Vx:.3f}**")
                st.success(f"**Vy = {Vy:.3f}**")

                # Görselleştirme
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=[0, Vx], y=[0, Vy],
                    mode='lines+markers',
                    name='Vektör V',
                    line=dict(color='blue', width=4),
                    marker=dict(size=10)
                ))

                # X ve Y bileşenleri
                fig.add_trace(go.Scatter(
                    x=[0, Vx], y=[0, 0],
                    mode='lines+markers',
                    name=f'Vx = {Vx:.2f}',
                    line=dict(color='green', width=2, dash='dash'),
                    marker=dict(size=6)
                ))

                fig.add_trace(go.Scatter(
                    x=[Vx, Vx], y=[0, Vy],
                    mode='lines+markers',
                    name=f'Vy = {Vy:.2f}',
                    line=dict(color='red', width=2, dash='dash'),
                    marker=dict(size=6)
                ))

                fig.update_layout(
                    title=f"Vektör Bileşenleri (Büyüklük={magnitude:.2f}, Açı={angle_deg:.1f}°)",
                    xaxis_title="X",
                    yaxis_title="Y",
                    showlegend=True,
                    width=600,
                    height=500,
                    xaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black'),
                    yaxis=dict(zeroline=True, zerolinewidth=2, zerolinecolor='black')
                )

                st.plotly_chart(fig)
            else:
                st.info("3D için küresel koordinatlardan kartezyen koordinatlara:")
                r = st.number_input("Büyüklük (r):", value=5.0, format="%.3f", min_value=0.0)
                theta_deg = st.number_input("Polar açı θ (derece, z ekseninden):", value=45.0, format="%.2f")
                phi_deg = st.number_input("Azimuthal açı φ (derece, x ekseninden):", value=30.0, format="%.2f")

                theta_rad = np.radians(theta_deg)
                phi_rad = np.radians(phi_deg)

                Vx = r * np.sin(theta_rad) * np.cos(phi_rad)
                Vy = r * np.sin(theta_rad) * np.sin(phi_rad)
                Vz = r * np.cos(theta_rad)

                st.success(f"**Vx = {Vx:.3f}**")
                st.success(f"**Vy = {Vy:.3f}**")
                st.success(f"**Vz = {Vz:.3f}**")
