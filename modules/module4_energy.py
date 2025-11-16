import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show():
    st.markdown('<h2 class="module-header">⚡ Modül 4: İş, Güç ve Enerji</h2>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔨 İş Hesaplayıcı", "⚡ Enerji Hesaplayıcı", "⚖️ Enerji Korunumu", "💪 Güç Hesaplayıcı"])

    # TAB 1: İş Hesaplayıcı
    with tab1:
        st.subheader("🔨 İş Hesaplayıcı")

        st.write("**İş formülü:**")
        st.latex(r"W = F \cdot d \cdot \cos(\theta)")

        col1, col2, col3 = st.columns(3)

        with col1:
            F = st.number_input("Kuvvet F (N):", value=50.0, format="%.2f")
        with col2:
            d = st.number_input("Yer değiştirme d (m):", value=10.0, format="%.2f", min_value=0.0)
        with col3:
            theta = st.number_input("Açı θ (derece):", value=0.0, format="%.2f")

        theta_rad = np.radians(theta)
        W = F * d * np.cos(theta_rad)

        st.success(f"**Yapılan İş:** W = {W:.2f} J (Joule)")

        if W > 0:
            st.info("✅ Pozitif iş: Kuvvet hareket yönünde")
        elif W < 0:
            st.info("⛔ Negatif iş: Kuvvet harekete zıt yönde")
        else:
            st.info("➖ Sıfır iş: Kuvvet harekete dik")

        # Görselleştirme
        fig = go.Figure()

        # Yer değiştirme vektörü
        fig.add_trace(go.Scatter(
            x=[0, d], y=[0, 0],
            mode='lines+markers',
            name='Yer değiştirme (d)',
            line=dict(color='blue', width=4),
            marker=dict(size=10)
        ))

        # Kuvvet vektörü
        Fx = F * np.cos(theta_rad) / 10  # Ölçeklendirme
        Fy = F * np.sin(theta_rad) / 10

        fig.add_annotation(
            x=d/2 + Fx, y=Fy,
            ax=d/2, ay=0,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="red",
            text=f"F={F}N (θ={theta}°)"
        )

        # Açı gösterimi
        if abs(theta) > 0.1:
            arc_theta = np.linspace(0, theta_rad, 30)
            arc_r = d * 0.15
            fig.add_trace(go.Scatter(
                x=d/2 + arc_r * np.cos(arc_theta),
                y=arc_r * np.sin(arc_theta),
                mode='lines',
                name=f'θ = {theta}°',
                line=dict(color='green', width=2, dash='dash')
            ))

        fig.update_layout(
            title=f"İş: W = {W:.2f} J",
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            showlegend=True,
            width=700,
            height=400,
            xaxis=dict(range=[-1, d*1.2]),
            yaxis=dict(range=[-d*0.3, d*0.3], scaleanchor="x", scaleratio=1)
        )

        st.plotly_chart(fig)

    # TAB 2: Enerji Hesaplayıcı
    with tab2:
        st.subheader("⚡ Enerji Hesaplayıcıları")

        enerji_tipi = st.radio(
            "Enerji tipi:",
            ["Kinetik Enerji", "Yerçekimsel Potansiyel Enerji", "Yay Potansiyel Enerjisi"],
            horizontal=True
        )

        if enerji_tipi == "Kinetik Enerji":
            st.write("**Kinetik Enerji:**")
            st.latex(r"KE = \frac{1}{2}mv^2")

            col1, col2 = st.columns(2)
            with col1:
                m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01, key="ke_m")
            with col2:
                v = st.number_input("Hız v (m/s):", value=5.0, format="%.2f", min_value=0.0)

            KE = 0.5 * m * v**2
            st.success(f"**Kinetik Enerji:** KE = {KE:.2f} J")

            # Grafik: KE vs hız
            v_range = np.linspace(0, v*2, 100)
            KE_range = 0.5 * m * v_range**2

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=v_range, y=KE_range,
                mode='lines',
                name='KE(v)',
                line=dict(color='blue', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[v], y=[KE],
                mode='markers',
                name='Mevcut durum',
                marker=dict(color='red', size=12)
            ))

            fig.update_layout(
                title=f"Kinetik Enerji vs Hız (m={m} kg)",
                xaxis_title="Hız (m/s)",
                yaxis_title="Kinetik Enerji (J)",
                showlegend=True,
                width=700,
                height=400
            )
            st.plotly_chart(fig)

        elif enerji_tipi == "Yerçekimsel Potansiyel Enerji":
            st.write("**Yerçekimsel Potansiyel Enerji:**")
            st.latex(r"PE = mgh")

            col1, col2, col3 = st.columns(3)
            with col1:
                m = st.number_input("Kütle m (kg):", value=5.0, format="%.2f", min_value=0.01, key="pe_m")
            with col2:
                g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="pe_g")
            with col3:
                h = st.number_input("Yükseklik h (m):", value=10.0, format="%.2f")

            PE = m * g * h
            st.success(f"**Potansiyel Enerji:** PE = {PE:.2f} J")

            # Görselleştirme
            fig = go.Figure()

            # Zemin
            fig.add_trace(go.Scatter(
                x=[-2, 2], y=[0, 0],
                mode='lines',
                name='Zemin (h=0)',
                line=dict(color='brown', width=4)
            ))

            # Cisim
            fig.add_trace(go.Scatter(
                x=[0], y=[h],
                mode='markers+text',
                name='Cisim',
                marker=dict(color='blue', size=20, symbol='square'),
                text=[f'm={m}kg'],
                textposition='top center'
            ))

            # Yükseklik çizgisi
            fig.add_trace(go.Scatter(
                x=[0, 0], y=[0, h],
                mode='lines',
                name=f'h={h}m',
                line=dict(color='red', width=2, dash='dash')
            ))

            fig.update_layout(
                title=f"Potansiyel Enerji: PE = {PE:.2f} J",
                xaxis_title="X",
                yaxis_title="Yükseklik (m)",
                showlegend=True,
                width=600,
                height=500,
                xaxis=dict(range=[-3, 3]),
                yaxis=dict(range=[-1, h*1.3])
            )
            st.plotly_chart(fig)

        else:  # Yay Potansiyel Enerjisi
            st.write("**Yay Potansiyel Enerjisi:**")
            st.latex(r"PE_{yay} = \frac{1}{2}kx^2")

            col1, col2 = st.columns(2)
            with col1:
                k = st.number_input("Yay sabiti k (N/m):", value=100.0, format="%.2f", min_value=0.01)
            with col2:
                x = st.number_input("Sıkıştırma/Uzama x (m):", value=0.5, format="%.3f")

            PE_spring = 0.5 * k * x**2
            st.success(f"**Yay Potansiyel Enerjisi:** PE = {PE_spring:.2f} J")

            # Grafik: PE vs uzama
            x_range = np.linspace(-abs(x)*2, abs(x)*2, 100)
            PE_range = 0.5 * k * x_range**2

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_range, y=PE_range,
                mode='lines',
                name='PE(x)',
                line=dict(color='green', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[x], y=[PE_spring],
                mode='markers',
                name='Mevcut durum',
                marker=dict(color='red', size=12)
            ))

            fig.update_layout(
                title=f"Yay Potansiyel Enerjisi vs Uzama (k={k} N/m)",
                xaxis_title="Uzama/Sıkıştırma (m)",
                yaxis_title="Potansiyel Enerji (J)",
                showlegend=True,
                width=700,
                height=400
            )
            st.plotly_chart(fig)

    # TAB 3: Enerji Korunumu
    with tab3:
        st.subheader("⚖️ Enerjinin Korunumu Simülasyonları")

        simulasyon = st.radio(
            "Simülasyon seçin:",
            ["Sarkaç", "Roller Coaster (Hız Treni)"],
            horizontal=True
        )

        if simulasyon == "Sarkaç":
            st.write("**Sarkaç:** Kinetik ve Potansiyel Enerji dönüşümü")

            col1, col2 = st.columns(2)
            with col1:
                m = st.number_input("Kütle m (kg):", value=1.0, format="%.2f", min_value=0.01, key="pendulum_m")
                L = st.number_input("İp uzunluğu L (m):", value=2.0, format="%.2f", min_value=0.1)
            with col2:
                theta_0 = st.number_input("Başlangıç açısı θ₀ (derece):", value=60.0, format="%.2f", min_value=0.1, max_value=90.0)
                g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="pendulum_g")

            theta_0_rad = np.radians(theta_0)

            # Enerji hesaplamaları
            h_max = L * (1 - np.cos(theta_0_rad))  # Maksimum yükseklik
            E_total = m * g * h_max  # Toplam mekanik enerji

            st.success(f"**Toplam Mekanik Enerji:** E = {E_total:.3f} J (sabit)")

            # Simülasyon
            # Basit harmonik yaklaşım kullanmıyoruz, gerçek formülleri kullanacağız
            # Enerji korunumu: mgh + (1/2)mv^2 = E_total
            # h = L(1 - cos(theta))
            # v = sqrt(2g(h_max - h))

            theta_range = np.linspace(-theta_0_rad, theta_0_rad, 100)
            h_range = L * (1 - np.cos(theta_range))
            PE_range = m * g * h_range
            KE_range = E_total - PE_range
            v_range = np.sqrt(2 * KE_range / m)

            # Pozisyon
            x_range = L * np.sin(theta_range)
            y_range = -L * np.cos(theta_range)

            # Animasyon için birkaç nokta
            n_points = 10
            theta_points = theta_0_rad * np.cos(np.linspace(0, np.pi, n_points))

            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Sarkaç Hareketi", "Enerji Dönüşümü"),
                specs=[[{"type": "xy"}, {"type": "xy"}]],
                column_widths=[0.5, 0.5]
            )

            # Sol: Sarkaç yörüngesi
            fig.add_trace(go.Scatter(
                x=x_range, y=y_range,
                mode='lines',
                name='Yörünge',
                line=dict(color='lightblue', width=2, dash='dash')
            ), row=1, col=1)

            # Sarkaç pozisyonları
            for i, theta in enumerate(theta_points):
                x_pos = L * np.sin(theta)
                y_pos = -L * np.cos(theta)

                # İp
                fig.add_trace(go.Scatter(
                    x=[0, x_pos], y=[0, y_pos],
                    mode='lines',
                    line=dict(color='gray', width=1),
                    showlegend=False,
                    opacity=0.5
                ), row=1, col=1)

                # Kütle
                fig.add_trace(go.Scatter(
                    x=[x_pos], y=[y_pos],
                    mode='markers',
                    marker=dict(size=8, opacity=0.6),
                    showlegend=False
                ), row=1, col=1)

            # Sabitleme noktası
            fig.add_trace(go.Scatter(
                x=[0], y=[0],
                mode='markers',
                name='Sabitleme',
                marker=dict(color='black', size=10, symbol='x')
            ), row=1, col=1)

            # Sağ: Enerji grafikleri
            theta_plot = np.linspace(-theta_0_rad, theta_0_rad, 100)
            h_plot = L * (1 - np.cos(theta_plot))
            PE_plot = m * g * h_plot
            KE_plot = E_total - PE_plot

            theta_deg_plot = np.degrees(theta_plot)

            fig.add_trace(go.Scatter(
                x=theta_deg_plot, y=PE_plot,
                mode='lines',
                name='PE (Potansiyel)',
                line=dict(color='red', width=3)
            ), row=1, col=2)

            fig.add_trace(go.Scatter(
                x=theta_deg_plot, y=KE_plot,
                mode='lines',
                name='KE (Kinetik)',
                line=dict(color='blue', width=3)
            ), row=1, col=2)

            fig.add_trace(go.Scatter(
                x=theta_deg_plot, y=[E_total]*len(theta_deg_plot),
                mode='lines',
                name='Toplam Enerji',
                line=dict(color='green', width=2, dash='dash')
            ), row=1, col=2)

            fig.update_xaxes(title_text="X (m)", row=1, col=1)
            fig.update_yaxes(title_text="Y (m)", row=1, col=1, scaleanchor="x", scaleratio=1)
            fig.update_xaxes(title_text="Açı (derece)", row=1, col=2)
            fig.update_yaxes(title_text="Enerji (J)", row=1, col=2)

            fig.update_layout(height=500, showlegend=True, title_text=f"Sarkaç Simülasyonu (E_total = {E_total:.2f} J)")
            st.plotly_chart(fig)

            # En alt noktada hız
            v_max = np.sqrt(2 * g * h_max)
            st.info(f"**En alt noktadaki maksimum hız:** v_max = {v_max:.3f} m/s")

        else:  # Roller Coaster
            st.write("**Roller Coaster (Hız Treni):** Bir tren tepeden aşağı iniyor")

            col1, col2 = st.columns(2)
            with col1:
                m = st.number_input("Kütle m (kg):", value=500.0, format="%.2f", min_value=0.01, key="coaster_m")
                h1 = st.number_input("İlk yükseklik h₁ (m):", value=50.0, format="%.2f", min_value=0.0)
            with col2:
                v1 = st.number_input("İlk hız v₁ (m/s):", value=0.0, format="%.2f", min_value=0.0)
                h2 = st.number_input("Son yükseklik h₂ (m):", value=10.0, format="%.2f", min_value=0.0)
                g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="coaster_g")

            # Enerji korunumu: E1 = E2
            # (1/2)m*v1^2 + m*g*h1 = (1/2)m*v2^2 + m*g*h2
            # v2 = sqrt(v1^2 + 2*g*(h1 - h2))

            E1 = 0.5 * m * v1**2 + m * g * h1
            E2_potential = m * g * h2
            E2_kinetic = E1 - E2_potential

            if E2_kinetic >= 0:
                v2 = np.sqrt(2 * E2_kinetic / m)

                st.success(f"**Başlangıç toplam enerjisi:** E₁ = {E1:.2f} J")
                st.success(f"**Son hız:** v₂ = {v2:.3f} m/s")
                st.success(f"**Son kinetik enerji:** KE₂ = {E2_kinetic:.2f} J")
                st.success(f"**Son potansiyel enerji:** PE₂ = {E2_potential:.2f} J")

                # Simülasyon - yol boyunca enerji dönüşümü
                # Basit bir yörünge oluşturalım
                n_points = 100
                x_path = np.linspace(0, 100, n_points)

                # Yükseklik profili (basit bir eğri)
                h_path = h1 - (h1 - h2) * (x_path / 100)**2

                # Her noktada hız (enerji korunumu)
                PE_path = m * g * h_path
                KE_path = E1 - PE_path
                KE_path = np.maximum(KE_path, 0)  # Negatif enerji olmasın
                v_path = np.sqrt(2 * KE_path / m)

                fig = make_subplots(
                    rows=2, cols=1,
                    subplot_titles=("Roller Coaster Yörüngesi", "Enerji Dönüşümü"),
                    row_heights=[0.5, 0.5],
                    vertical_spacing=0.15
                )

                # Üst: Yörünge
                fig.add_trace(go.Scatter(
                    x=x_path, y=h_path,
                    mode='lines',
                    name='Yörünge',
                    line=dict(color='brown', width=4),
                    fill='tozeroy',
                    fillcolor='rgba(139, 69, 19, 0.3)'
                ), row=1, col=1)

                # Başlangıç ve bitiş noktaları
                fig.add_trace(go.Scatter(
                    x=[0], y=[h1],
                    mode='markers+text',
                    name='Başlangıç',
                    marker=dict(color='green', size=15),
                    text=['Start'],
                    textposition='top center'
                ), row=1, col=1)

                fig.add_trace(go.Scatter(
                    x=[100], y=[h2],
                    mode='markers+text',
                    name='Bitiş',
                    marker=dict(color='red', size=15),
                    text=['End'],
                    textposition='top center'
                ), row=1, col=1)

                # Alt: Enerji grafikleri
                fig.add_trace(go.Scatter(
                    x=x_path, y=PE_path,
                    mode='lines',
                    name='PE (Potansiyel)',
                    line=dict(color='red', width=3),
                    fill='tonexty'
                ), row=2, col=1)

                fig.add_trace(go.Scatter(
                    x=x_path, y=KE_path,
                    mode='lines',
                    name='KE (Kinetik)',
                    line=dict(color='blue', width=3),
                    fill='tonexty'
                ), row=2, col=1)

                fig.add_trace(go.Scatter(
                    x=x_path, y=[E1]*len(x_path),
                    mode='lines',
                    name='Toplam Enerji',
                    line=dict(color='green', width=2, dash='dash')
                ), row=2, col=1)

                fig.update_xaxes(title_text="Yatay Mesafe (m)", row=1, col=1)
                fig.update_yaxes(title_text="Yükseklik (m)", row=1, col=1)
                fig.update_xaxes(title_text="Yatay Mesafe (m)", row=2, col=1)
                fig.update_yaxes(title_text="Enerji (J)", row=2, col=1)

                fig.update_layout(height=700, showlegend=True, title_text=f"Roller Coaster (E_total = {E1:.2f} J)")
                st.plotly_chart(fig)

            else:
                st.error("⚠️ Tren son yüksekliğe ulaşamaz! İlk enerji yetersiz.")

    # TAB 4: Güç Hesaplayıcı
    with tab4:
        st.subheader("💪 Güç Hesaplayıcı")

        st.write("**Güç formülü:**")
        st.latex(r"P = \frac{W}{t} = \frac{E}{t}")

        hesaplama_tipi = st.radio(
            "Hesaplama tipi:",
            ["İş ve Zamandan Güç", "Kuvvet ve Hızdan Güç"],
            horizontal=True
        )

        if hesaplama_tipi == "İş ve Zamandan Güç":
            col1, col2 = st.columns(2)

            with col1:
                W = st.number_input("Yapılan İş W (J):", value=1000.0, format="%.2f")
            with col2:
                t = st.number_input("Zaman t (s):", value=10.0, format="%.2f", min_value=0.01)

            P = W / t

            st.success(f"**Güç:** P = {P:.2f} W (Watt)")
            st.info(f"**Güç (kW):** P = {P/1000:.3f} kW")
            st.info(f"**Güç (hp - beygir gücü):** P = {P/745.7:.3f} hp")

        else:  # Kuvvet ve Hızdan
            st.write("Sabit kuvvet ve hız için:")
            st.latex(r"P = F \cdot v")

            col1, col2 = st.columns(2)

            with col1:
                F = st.number_input("Kuvvet F (N):", value=100.0, format="%.2f", key="power_f")
            with col2:
                v = st.number_input("Hız v (m/s):", value=5.0, format="%.2f", min_value=0.0, key="power_v")

            P = F * v

            st.success(f"**Güç:** P = {P:.2f} W (Watt)")
            st.info(f"**Güç (kW):** P = {P/1000:.3f} kW")
            st.info(f"**Güç (hp):** P = {P/745.7:.3f} hp")

        st.markdown("---")
        st.write("**Güç birimleri:**")
        st.info("""
        - 1 Watt (W) = 1 J/s
        - 1 Kilowatt (kW) = 1000 W
        - 1 Beygir Gücü (hp) ≈ 745.7 W
        - 1 kWh (kilowatt-saat) = 3.6 × 10⁶ J (enerji birimi)
        """)
