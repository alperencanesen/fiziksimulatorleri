import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show():
    st.markdown('<h2 class="module-header">💪 Modül 3: Dinamik (Hareketin Nedenleri)</h2>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["⚖️ Newton Yasaları", "🔥 Sürtünme", "📐 Eğik Düzlem", "🔗 Makara Sistemleri"])

    # TAB 1: Newton Yasaları
    with tab1:
        st.subheader("⚖️ Newton'un Yasaları")

        st.write("**Newton'un İkinci Yasası:**")
        st.latex(r"F_{net} = m \cdot a")

        hesaplama = st.radio(
            "Ne hesaplamak istiyorsunuz?",
            ["Net Kuvvet", "Kütle", "İvme"],
            horizontal=True
        )

        if hesaplama == "Net Kuvvet":
            col1, col2 = st.columns(2)
            with col1:
                m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01)
            with col2:
                a = st.number_input("İvme a (m/s²):", value=2.0, format="%.2f")

            F = m * a
            st.success(f"**Net Kuvvet:** F = {F:.2f} N")

        elif hesaplama == "Kütle":
            col1, col2 = st.columns(2)
            with col1:
                F = st.number_input("Net Kuvvet F (N):", value=20.0, format="%.2f")
            with col2:
                a = st.number_input("İvme a (m/s²):", value=2.0, format="%.2f", min_value=0.01)

            m = F / a
            st.success(f"**Kütle:** m = {m:.2f} kg")

        else:  # İvme
            col1, col2 = st.columns(2)
            with col1:
                F = st.number_input("Net Kuvvet F (N):", value=20.0, format="%.2f")
            with col2:
                m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01)

            a = F / m
            st.success(f"**İvme:** a = {a:.2f} m/s²")

        st.markdown("---")
        st.write("**Newton'un Yasaları:**")
        st.info("""
        **1. Yasa (Eylemsizlik):** Bir cisim, üzerine dış kuvvet uygulanmadıkça durgun halde veya düzgün doğrusal harekete devam eder.

        **2. Yasa:** Bir cisme uygulanan net kuvvet, cismin kütlesi ile ivmesinin çarpımına eşittir (F = ma).

        **3. Yasa (Etki-Tepki):** Her etkiye eşit büyüklükte ve zıt yönde bir tepki vardır.
        """)

    # TAB 2: Sürtünme
    with tab2:
        st.subheader("🔥 Sürtünme Kuvveti")

        st.write("**Sürtünme Formülleri:**")
        st.latex(r"f_s \leq \mu_s \cdot N \quad \text{(Statik sürtünme)}")
        st.latex(r"f_k = \mu_k \cdot N \quad \text{(Kinetik sürtünme)}")

        sutunme_tipi = st.radio(
            "Sürtünme tipi:",
            ["Yatay Yüzeyde Sürtünme", "Eğik Düzlemde Sürtünme"],
            horizontal=True
        )

        if sutunme_tipi == "Yatay Yüzeyde Sürtünme":
            col1, col2 = st.columns(2)

            with col1:
                m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01, key="fric_m")
                g = st.number_input("Yerçekimi ivmesi g (m/s²):", value=9.81, format="%.2f", key="fric_g")
                mu_s = st.number_input("Statik sürtünme katsayısı μₛ:", value=0.5, format="%.3f", min_value=0.0)

            with col2:
                mu_k = st.number_input("Kinetik sürtünme katsayısı μₖ:", value=0.3, format="%.3f", min_value=0.0)
                F_applied = st.number_input("Uygulanan kuvvet F (N):", value=30.0, format="%.2f", min_value=0.0)

            N = m * g  # Normal kuvvet
            f_s_max = mu_s * N  # Maksimum statik sürtünme
            f_k = mu_k * N  # Kinetik sürtünme

            st.success(f"**Normal kuvvet:** N = {N:.2f} N")
            st.success(f"**Maksimum statik sürtünme:** fₛ(max) = {f_s_max:.2f} N")
            st.success(f"**Kinetik sürtünme:** fₖ = {f_k:.2f} N")

            # Hareket analizi
            if F_applied <= f_s_max:
                st.info(f"✋ **Cisim hareketsiz!** Uygulanan kuvvet ({F_applied:.2f} N) maksimum statik sürtünmeden ({f_s_max:.2f} N) küçük.")
                st.info(f"Statik sürtünme kuvveti: fₛ = {F_applied:.2f} N (Uygulanan kuvvete eşit)")
            else:
                F_net = F_applied - f_k
                a = F_net / m
                st.success(f"🏃 **Cisim hareket ediyor!**")
                st.success(f"Net kuvvet: Fₙₑₜ = {F_net:.2f} N")
                st.success(f"İvme: a = {a:.2f} m/s²")

            # Görselleştirme
            fig = go.Figure()

            # Kuvvet-hareket grafiği
            F_range = np.linspace(0, f_s_max * 2, 100)
            friction_force = []
            acceleration = []

            for F in F_range:
                if F <= f_s_max:
                    friction_force.append(F)
                    acceleration.append(0)
                else:
                    friction_force.append(f_k)
                    acceleration.append((F - f_k) / m)

            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Sürtünme Kuvveti vs Uygulanan Kuvvet", "İvme vs Uygulanan Kuvvet")
            )

            fig.add_trace(go.Scatter(
                x=F_range, y=friction_force,
                mode='lines',
                name='Sürtünme kuvveti',
                line=dict(color='red', width=3)
            ), row=1, col=1)

            fig.add_trace(go.Scatter(
                x=[F_applied], y=[f_k if F_applied > f_s_max else F_applied],
                mode='markers',
                name='Mevcut durum',
                marker=dict(color='blue', size=12)
            ), row=1, col=1)

            fig.add_trace(go.Scatter(
                x=F_range, y=acceleration,
                mode='lines',
                name='İvme',
                line=dict(color='green', width=3)
            ), row=1, col=2)

            fig.add_trace(go.Scatter(
                x=[F_applied], y=[(F_applied - f_k) / m if F_applied > f_s_max else 0],
                mode='markers',
                name='Mevcut durum',
                marker=dict(color='blue', size=12)
            ), row=1, col=2)

            fig.update_xaxes(title_text="Uygulanan Kuvvet (N)", row=1, col=1)
            fig.update_xaxes(title_text="Uygulanan Kuvvet (N)", row=1, col=2)
            fig.update_yaxes(title_text="Sürtünme (N)", row=1, col=1)
            fig.update_yaxes(title_text="İvme (m/s²)", row=1, col=2)

            fig.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig)

        else:  # Eğik düzlemde sürtünme
            st.write("Eğik düzlem üzerinde sürtünme hesaplamaları için 'Eğik Düzlem' sekmesine bakın.")

    # TAB 3: Eğik Düzlem
    with tab3:
        st.subheader("📐 Eğik Düzlem Simülasyonu")

        st.write("Bir cisim eğik düzlem üzerinde hareket ediyor.")

        col1, col2 = st.columns(2)

        with col1:
            m = st.number_input("Kütle m (kg):", value=5.0, format="%.2f", min_value=0.01, key="incline_m")
            theta = st.number_input("Eğim açısı θ (derece):", value=30.0, format="%.2f", min_value=0.0, max_value=90.0)
            g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="incline_g")

        with col2:
            mu = st.number_input("Sürtünme katsayısı μ:", value=0.2, format="%.3f", min_value=0.0)
            v0 = st.number_input("İlk hız v₀ (m/s, yukarı +):", value=0.0, format="%.2f")

        theta_rad = np.radians(theta)

        # Kuvvet analizi
        W = m * g  # Ağırlık
        N = W * np.cos(theta_rad)  # Normal kuvvet
        W_parallel = W * np.sin(theta_rad)  # Paralel bileşen (aşağı)
        f = mu * N  # Sürtünme kuvveti

        # Net kuvvet (yukarı + pozitif)
        if v0 >= 0:  # Yukarı hareket veya durgun
            F_net = -W_parallel - f  # Sürtünme aşağı
        else:  # Aşağı hareket
            F_net = -W_parallel + f  # Sürtünme yukarı

        a = F_net / m

        st.success(f"**Ağırlık:** W = {W:.2f} N")
        st.success(f"**Normal kuvvet:** N = {N:.2f} N")
        st.success(f"**Paralel bileşen:** W∥ = {W_parallel:.2f} N (aşağı)")
        st.success(f"**Sürtünme kuvveti:** f = {f:.2f} N")
        st.success(f"**Net kuvvet:** Fₙₑₜ = {F_net:.2f} N {'(yukarı)' if F_net > 0 else '(aşağı)'}")
        st.success(f"**İvme:** a = {a:.2f} m/s²")

        # Görselleştirme - Kuvvet diyagramı
        fig = go.Figure()

        # Eğik düzlem
        L = 10  # Düzlem uzunluğu (görsel için)
        x_incline = [0, L * np.cos(theta_rad), L * np.cos(theta_rad), 0, 0]
        y_incline = [0, L * np.sin(theta_rad), 0, 0, 0]

        fig.add_trace(go.Scatter(
            x=x_incline, y=y_incline,
            mode='lines',
            name='Eğik düzlem',
            line=dict(color='brown', width=4),
            fill='tonexty',
            fillcolor='rgba(139, 69, 19, 0.3)'
        ))

        # Cisim (ortada)
        x_obj = L/2 * np.cos(theta_rad)
        y_obj = L/2 * np.sin(theta_rad)

        fig.add_trace(go.Scatter(
            x=[x_obj], y=[y_obj],
            mode='markers',
            name='Cisim',
            marker=dict(color='blue', size=20, symbol='square')
        ))

        # Kuvvet vektörleri (ölçeklendirme)
        scale = 0.5

        # Ağırlık (düşey aşağı)
        fig.add_annotation(
            x=x_obj, y=y_obj - W * scale * 0.1,
            ax=x_obj, ay=y_obj,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="purple",
            text=f"W={W:.1f}N"
        )

        # Normal kuvvet (düzleme dik)
        Nx = -N * scale * 0.1 * np.sin(theta_rad)
        Ny = N * scale * 0.1 * np.cos(theta_rad)
        fig.add_annotation(
            x=x_obj + Nx, y=y_obj + Ny,
            ax=x_obj, ay=y_obj,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="green",
            text=f"N={N:.1f}N"
        )

        # Paralel bileşen (düzlem boyunca aşağı)
        Wpx = W_parallel * scale * 0.1 * np.cos(theta_rad)
        Wpy = -W_parallel * scale * 0.1 * np.sin(theta_rad)
        fig.add_annotation(
            x=x_obj - Wpx, y=y_obj + Wpy,
            ax=x_obj, ay=y_obj,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="red",
            text=f"W∥={W_parallel:.1f}N"
        )

        # Sürtünme kuvveti (düzlem boyunca yukarı)
        fx = f * scale * 0.1 * np.cos(theta_rad)
        fy = f * scale * 0.1 * np.sin(theta_rad)
        fig.add_annotation(
            x=x_obj + fx, y=y_obj + fy,
            ax=x_obj, ay=y_obj,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=3,
            arrowcolor="orange",
            text=f"f={f:.1f}N"
        )

        fig.update_layout(
            title=f"Eğik Düzlem Kuvvet Diyagramı (θ={theta}°)",
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            showlegend=True,
            width=700,
            height=500,
            xaxis=dict(range=[-1, L*1.1]),
            yaxis=dict(range=[-1, L*np.sin(theta_rad)*1.5], scaleanchor="x", scaleratio=1)
        )

        st.plotly_chart(fig)

        # Hareket simülasyonu
        if abs(a) > 0.01:
            st.write("**Hareket Simülasyonu:**")

            # Hareket denklemi: s = v0*t + 0.5*a*t^2
            # Duracak mı?
            if v0 != 0 and a * v0 < 0:  # Zıt yönde ivme
                t_stop = -v0 / a
                s_stop = v0 * t_stop + 0.5 * a * t_stop**2
                t_max = t_stop * 1.5
            else:
                t_max = 5  # Sabit simülasyon süresi

            t_array = np.linspace(0, t_max, 100)
            v_array = v0 + a * t_array
            s_array = v0 * t_array + 0.5 * a * t_array**2

            fig2 = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Hız-Zaman", "Konum-Zaman")
            )

            fig2.add_trace(go.Scatter(x=t_array, y=v_array, mode='lines', name='v(t)',
                                     line=dict(color='blue', width=3)), row=1, col=1)
            fig2.add_trace(go.Scatter(x=t_array, y=s_array, mode='lines', name='s(t)',
                                     line=dict(color='green', width=3)), row=1, col=2)

            fig2.update_xaxes(title_text="Zaman (s)", row=1, col=1)
            fig2.update_xaxes(title_text="Zaman (s)", row=1, col=2)
            fig2.update_yaxes(title_text="Hız (m/s)", row=1, col=1)
            fig2.update_yaxes(title_text="Konum (m)", row=1, col=2)

            fig2.update_layout(height=400, showlegend=True)
            st.plotly_chart(fig2)

    # TAB 4: Makara Sistemleri
    with tab4:
        st.subheader("🔗 Makara Sistemleri (Atwood Düzeneği)")

        st.write("İki kütle bir ip ile makaraya bağlı.")

        col1, col2 = st.columns(2)

        with col1:
            m1 = st.number_input("Kütle 1 (m₁) (kg):", value=5.0, format="%.2f", min_value=0.01)
            m2 = st.number_input("Kütle 2 (m₂) (kg):", value=3.0, format="%.2f", min_value=0.01)

        with col2:
            g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="atwood_g")

        # Sistem analizi (sürtünmesiz, kütlesiz makara)
        # m1 > m2 olduğunu varsayalım (m1 aşağı, m2 yukarı)

        # Net kuvvet: (m1 - m2)*g = (m1 + m2)*a
        a = ((m1 - m2) / (m1 + m2)) * g

        # İp gerilmesi: T = m2*(g + a) veya T = m1*(g - a)
        T = m2 * (g + a)

        st.success(f"**Sistem ivmesi:** a = {abs(a):.3f} m/s²")

        if a > 0:
            st.success(f"**Hareket:** m₁ aşağı, m₂ yukarı hareket ediyor")
        elif a < 0:
            st.success(f"**Hareket:** m₁ yukarı, m₂ aşağı hareket ediyor")
        else:
            st.success(f"**Hareket:** Sistem dengede (m₁ = m₂)")

        st.success(f"**İp gerilmesi:** T = {T:.3f} N")

        # Kontrol
        T_check = m1 * (g - a)
        st.info(f"Kontrol: T = m₁(g - a) = {T_check:.3f} N ✓")

        # Görselleştirme
        fig = go.Figure()

        # Makara (daire)
        theta = np.linspace(0, 2*np.pi, 100)
        r_pulley = 0.5
        x_pulley = 5
        y_pulley = 8

        fig.add_trace(go.Scatter(
            x=x_pulley + r_pulley * np.cos(theta),
            y=y_pulley + r_pulley * np.sin(theta),
            mode='lines',
            name='Makara',
            line=dict(color='gray', width=3),
            fill='toself',
            fillcolor='rgba(128, 128, 128, 0.3)'
        ))

        # İpler
        # Sol taraf (m1)
        x1 = x_pulley - r_pulley
        y1_top = y_pulley
        y1_bottom = y_pulley - 4

        fig.add_trace(go.Scatter(
            x=[x1, x1], y=[y1_top, y1_bottom],
            mode='lines',
            name='İp',
            line=dict(color='black', width=2)
        ))

        # Sağ taraf (m2)
        x2 = x_pulley + r_pulley
        y2_top = y_pulley
        y2_bottom = y_pulley - 2

        fig.add_trace(go.Scatter(
            x=[x2, x2], y=[y2_top, y2_bottom],
            mode='lines',
            name='İp',
            line=dict(color='black', width=2),
            showlegend=False
        ))

        # Kütleler
        fig.add_trace(go.Scatter(
            x=[x1], y=[y1_bottom],
            mode='markers+text',
            name=f'm₁ = {m1} kg',
            marker=dict(color='red', size=30, symbol='square'),
            text=[f'm₁'],
            textposition='bottom center',
            textfont=dict(size=14, color='white')
        ))

        fig.add_trace(go.Scatter(
            x=[x2], y=[y2_bottom],
            mode='markers+text',
            name=f'm₂ = {m2} kg',
            marker=dict(color='blue', size=30, symbol='square'),
            text=[f'm₂'],
            textposition='bottom center',
            textfont=dict(size=14, color='white')
        ))

        # Kuvvet okları
        arrow_scale = 0.5

        # m1 üzerindeki kuvvetler
        # Ağırlık
        fig.add_annotation(
            x=x1, y=y1_bottom - m1*g*arrow_scale*0.05,
            ax=x1, ay=y1_bottom,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="purple",
            text=f"W₁={m1*g:.1f}N"
        )

        # Gerilme
        fig.add_annotation(
            x=x1, y=y1_bottom + T*arrow_scale*0.05,
            ax=x1, ay=y1_bottom,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="green",
            text=f"T={T:.1f}N"
        )

        # m2 üzerindeki kuvvetler
        # Ağırlık
        fig.add_annotation(
            x=x2, y=y2_bottom - m2*g*arrow_scale*0.05,
            ax=x2, ay=y2_bottom,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="purple",
            text=f"W₂={m2*g:.1f}N"
        )

        # Gerilme
        fig.add_annotation(
            x=x2, y=y2_bottom + T*arrow_scale*0.05,
            ax=x2, ay=y2_bottom,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="green",
            text=f"T={T:.1f}N"
        )

        fig.update_layout(
            title=f"Atwood Düzeneği (a={abs(a):.2f} m/s², T={T:.2f} N)",
            xaxis_title="",
            yaxis_title="",
            showlegend=True,
            width=600,
            height=600,
            xaxis=dict(range=[2, 8], showticklabels=False),
            yaxis=dict(range=[0, 10], scaleanchor="x", scaleratio=1, showticklabels=False)
        )

        st.plotly_chart(fig)

        st.info("""
        **Formüller:**
        - İvme: a = [(m₁ - m₂)/(m₁ + m₂)] × g
        - İp gerilmesi: T = m₂(g + a) = m₁(g - a)

        (Sürtünmesiz, kütlesiz makara ve ip varsayımı ile)
        """)
