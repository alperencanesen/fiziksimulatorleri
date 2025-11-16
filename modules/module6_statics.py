import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show():
    st.markdown('<h2 class="module-header">🏗️ Modül 6: Statik ve Dönme Hareketi</h2>', unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["🔄 Tork", "⚖️ Denge", "📍 Kütle Merkezi", "⚙️ Dönme Dinamiği"])

    # TAB 1: Tork
    with tab1:
        st.subheader("🔄 Tork (Moment) Hesaplayıcı")

        st.write("**Tork formülü:**")
        st.latex(r"\tau = r \times F = rF\sin(\theta)")

        col1, col2, col3 = st.columns(3)

        with col1:
            r = st.number_input("Kuvvet kolu r (m):", value=2.0, format="%.2f", min_value=0.0)
        with col2:
            F = st.number_input("Kuvvet F (N):", value=50.0, format="%.2f")
        with col3:
            theta = st.number_input("Açı θ (derece):", value=90.0, format="%.2f")

        theta_rad = np.radians(theta)
        tau = r * F * np.sin(theta_rad)

        st.success(f"**Tork:** τ = {tau:.2f} N·m")

        if tau > 0:
            st.info("🔄 Pozitif tork: Saat yönünün tersine dönme")
        elif tau < 0:
            st.info("🔃 Negatif tork: Saat yönünde dönme")
        else:
            st.info("➖ Sıfır tork: Dönme yok (kuvvet merkezden geçiyor veya θ=0°/180°)")

        # Görselleştirme
        fig = go.Figure()

        # Dönme ekseni (merkez)
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            name='Dönme Ekseni',
            marker=dict(color='black', size=15, symbol='x')
        ))

        # Kuvvet kolu
        fig.add_trace(go.Scatter(
            x=[0, r], y=[0, 0],
            mode='lines+markers',
            name='Kuvvet Kolu (r)',
            line=dict(color='blue', width=4),
            marker=dict(size=10)
        ))

        # Kuvvet vektörü
        scale = 0.02
        Fx = F * np.cos(theta_rad) * scale
        Fy = F * np.sin(theta_rad) * scale

        fig.add_annotation(
            x=r + Fx, y=Fy,
            ax=r, ay=0,
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=3,
            arrowcolor="red",
            text=f"F={F}N"
        )

        # Açı yayı
        if abs(theta) > 1:
            arc_theta = np.linspace(0, theta_rad, 30)
            arc_r = r * 0.3
            fig.add_trace(go.Scatter(
                x=arc_r * np.cos(arc_theta),
                y=arc_r * np.sin(arc_theta),
                mode='lines',
                name=f'θ = {theta}°',
                line=dict(color='green', width=2, dash='dash')
            ))

        # Dönme yönü göstergesi
        if abs(tau) > 0.1:
            rotation_sign = "↺" if tau > 0 else "↻"
            fig.add_annotation(
                x=0, y=r*0.5,
                text=f"{rotation_sign} τ={tau:.1f} N·m",
                showarrow=False,
                font=dict(size=16, color='purple')
            )

        fig.update_layout(
            title=f"Tork: τ = {tau:.2f} N·m",
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            showlegend=True,
            width=700,
            height=500,
            xaxis=dict(range=[-0.5, r*1.5], zeroline=True),
            yaxis=dict(range=[-r*0.5, r*1.2], scaleanchor="x", scaleratio=1, zeroline=True)
        )

        st.plotly_chart(fig)

    # TAB 2: Denge
    with tab2:
        st.subheader("⚖️ Statik Denge - Basit Kiriş")

        st.write("**Denge koşulları:**")
        st.latex(r"\sum F = 0 \quad \text{(Kuvvet dengesi)}")
        st.latex(r"\sum \tau = 0 \quad \text{(Moment dengesi)}")

        st.write("Bir kiriş üzerinde yükler var, destek noktalarındaki tepki kuvvetlerini bulalım.")

        col1, col2 = st.columns(2)

        with col1:
            L = st.number_input("Kiriş uzunluğu L (m):", value=10.0, format="%.2f", min_value=1.0)
            m_beam = st.number_input("Kiriş kütlesi (kg):", value=100.0, format="%.2f", min_value=0.0)
            g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="beam_g")

        with col2:
            support_A = st.number_input("Destek A konumu (m, soldan):", value=0.0, format="%.2f", min_value=0.0, max_value=100.0)
            support_B = st.number_input("Destek B konumu (m, soldan):", value=10.0, format="%.2f", min_value=0.0, max_value=100.0)

        # Yükler
        st.write("**Nokta Yükleri:**")
        n_loads = st.number_input("Yük sayısı:", min_value=0, max_value=5, value=2, step=1)

        loads = []
        for i in range(n_loads):
            col_a, col_b = st.columns(2)
            with col_a:
                pos = st.number_input(f"Yük {i+1} konumu (m):", value=(i+1)*L/(n_loads+1), format="%.2f", min_value=0.0, max_value=L, key=f"load_pos_{i}")
            with col_b:
                force = st.number_input(f"Yük {i+1} kuvveti (N, aşağı):", value=500.0, format="%.2f", min_value=0.0, key=f"load_force_{i}")
            loads.append((pos, force))

        # Kiriş ağırlığı (merkezde)
        W_beam = m_beam * g
        beam_center = L / 2

        # Toplam aşağı kuvvet
        total_down = W_beam + sum(f for _, f in loads)

        # Moment dengesi (A noktasına göre)
        # Σ τ_A = 0
        # R_B * (support_B - support_A) - W_beam * (beam_center - support_A) - Σ(load_i * (pos_i - support_A)) = 0

        if abs(support_B - support_A) > 0.1:
            moment_A = 0
            moment_A -= W_beam * (beam_center - support_A)
            for pos, force in loads:
                moment_A -= force * (pos - support_A)

            R_B = moment_A / (support_B - support_A)
            R_B = -R_B  # İşaret düzeltmesi

            # Kuvvet dengesi
            R_A = total_down - R_B

            st.success(f"**Destek A tepki kuvveti:** R_A = {R_A:.2f} N")
            st.success(f"**Destek B tepki kuvveti:** R_B = {R_B:.2f} N")
            st.success(f"**Toplam aşağı kuvvet:** {total_down:.2f} N")
            st.success(f"**Kontrol (R_A + R_B):** {R_A + R_B:.2f} N {'✓' if abs(R_A + R_B - total_down) < 0.1 else '✗'}")

            # Görselleştirme
            fig = go.Figure()

            # Kiriş
            fig.add_trace(go.Scatter(
                x=[0, L], y=[0, 0],
                mode='lines',
                name='Kiriş',
                line=dict(color='brown', width=8)
            ))

            # Destekler
            fig.add_trace(go.Scatter(
                x=[support_A], y=[0],
                mode='markers+text',
                name='Destek A',
                marker=dict(color='green', size=20, symbol='triangle-up'),
                text=[f'A: {R_A:.0f}N'],
                textposition='bottom center'
            ))

            fig.add_trace(go.Scatter(
                x=[support_B], y=[0],
                mode='markers+text',
                name='Destek B',
                marker=dict(color='blue', size=20, symbol='triangle-up'),
                text=[f'B: {R_B:.0f}N'],
                textposition='bottom center'
            ))

            # Kiriş ağırlığı
            fig.add_annotation(
                x=beam_center, y=-W_beam*0.001,
                ax=beam_center, ay=0,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=2,
                arrowcolor="purple",
                text=f"W_beam={W_beam:.0f}N"
            )

            # Nokta yükleri
            for i, (pos, force) in enumerate(loads):
                fig.add_annotation(
                    x=pos, y=-force*0.001,
                    ax=pos, ay=0,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=3,
                    arrowcolor="red",
                    text=f"F{i+1}={force:.0f}N"
                )

            # Tepki kuvvetleri
            scale = 0.001
            fig.add_annotation(
                x=support_A, y=R_A*scale,
                ax=support_A, ay=0,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=3,
                arrowcolor="green"
            )

            fig.add_annotation(
                x=support_B, y=R_B*scale,
                ax=support_B, ay=0,
                xref="x", yref="y",
                axref="x", ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=3,
                arrowcolor="blue"
            )

            fig.update_layout(
                title="Kiriş Statik Denge",
                xaxis_title="Konum (m)",
                yaxis_title="",
                showlegend=True,
                width=900,
                height=400,
                xaxis=dict(range=[-1, L+1]),
                yaxis=dict(range=[-max(total_down*0.002, 1), max(total_down*0.002, 1)], showticklabels=False)
            )

            st.plotly_chart(fig)

        else:
            st.error("Destekler aynı noktada olamaz!")

    # TAB 3: Kütle Merkezi
    with tab3:
        st.subheader("📍 Kütle Merkezi Hesaplayıcı")

        st.write("**Kütle merkezi formülü:**")
        st.latex(r"x_{cm} = \frac{\sum m_i x_i}{\sum m_i}, \quad y_{cm} = \frac{\sum m_i y_i}{\sum m_i}")

        hesaplama_tipi = st.radio(
            "Hesaplama tipi:",
            ["Nokta Kütleler", "Geometrik Şekiller"],
            horizontal=True
        )

        if hesaplama_tipi == "Nokta Kütleler":
            st.write("Birden fazla nokta kütlenin kütle merkezini hesaplayın:")

            n_masses = st.number_input("Kütle sayısı:", min_value=2, max_value=10, value=3, step=1)

            masses = []
            for i in range(n_masses):
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    m = st.number_input(f"m{i+1} (kg):", value=1.0, format="%.2f", min_value=0.01, key=f"cm_m_{i}")
                with col_b:
                    x = st.number_input(f"x{i+1} (m):", value=float(i), format="%.2f", key=f"cm_x_{i}")
                with col_c:
                    y = st.number_input(f"y{i+1} (m):", value=float(i), format="%.2f", key=f"cm_y_{i}")
                masses.append((m, x, y))

            # Kütle merkezi
            total_mass = sum(m for m, _, _ in masses)
            x_cm = sum(m * x for m, x, _ in masses) / total_mass
            y_cm = sum(m * y for m, _, y in masses) / total_mass

            st.success(f"**Toplam kütle:** M = {total_mass:.2f} kg")
            st.success(f"**Kütle merkezi:** (x_cm, y_cm) = ({x_cm:.3f}, {y_cm:.3f}) m")

            # Görselleştirme
            fig = go.Figure()

            # Kütleler
            for i, (m, x, y) in enumerate(masses):
                fig.add_trace(go.Scatter(
                    x=[x], y=[y],
                    mode='markers+text',
                    name=f'm{i+1}={m}kg',
                    marker=dict(size=m*20, color=f'rgb({50+i*40},{100+i*30},{200-i*20})'),
                    text=[f'm{i+1}'],
                    textposition='top center'
                ))

            # Kütle merkezi
            fig.add_trace(go.Scatter(
                x=[x_cm], y=[y_cm],
                mode='markers+text',
                name='Kütle Merkezi',
                marker=dict(color='red', size=25, symbol='star'),
                text=['CM'],
                textposition='bottom center'
            ))

            fig.update_layout(
                title=f"Kütle Merkezi: ({x_cm:.2f}, {y_cm:.2f})",
                xaxis_title="X (m)",
                yaxis_title="Y (m)",
                showlegend=True,
                width=700,
                height=600,
                xaxis=dict(zeroline=True, scaleanchor="y", scaleratio=1),
                yaxis=dict(zeroline=True, scaleanchor="x", scaleratio=1)
            )

            st.plotly_chart(fig)

        else:  # Geometrik Şekiller
            st.write("L veya T şeklinde plakaların kütle merkezini hesaplayın:")

            shape = st.selectbox("Şekil:", ["L Şekli", "T Şekli", "Dikdörtgen"])

            if shape == "Dikdörtgen":
                col1, col2 = st.columns(2)
                with col1:
                    width = st.number_input("Genişlik (m):", value=4.0, format="%.2f", min_value=0.1)
                with col2:
                    height = st.number_input("Yükseklik (m):", value=2.0, format="%.2f", min_value=0.1)

                x_cm = width / 2
                y_cm = height / 2

                st.success(f"**Kütle merkezi (merkez):** ({x_cm:.2f}, {y_cm:.2f}) m")

                # Görselleştirme
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[0, width, width, 0, 0],
                    y=[0, 0, height, height, 0],
                    mode='lines',
                    name='Dikdörtgen',
                    line=dict(color='blue', width=3),
                    fill='toself',
                    fillcolor='rgba(0, 0, 255, 0.2)'
                ))

                fig.add_trace(go.Scatter(
                    x=[x_cm], y=[y_cm],
                    mode='markers+text',
                    name='Kütle Merkezi',
                    marker=dict(color='red', size=15, symbol='x'),
                    text=['CM'],
                    textposition='top center'
                ))

                fig.update_layout(
                    title="Dikdörtgen Kütle Merkezi",
                    xaxis_title="X (m)",
                    yaxis_title="Y (m)",
                    showlegend=True,
                    width=600,
                    height=500,
                    xaxis=dict(scaleanchor="y", scaleratio=1),
                    yaxis=dict(scaleanchor="x", scaleratio=1)
                )

                st.plotly_chart(fig)

            elif shape == "L Şekli":
                st.write("L şeklini iki dikdörtgene ayırarak hesaplayalım:")

                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Alt dikdörtgen (yatay):**")
                    w1 = st.number_input("Genişlik (m):", value=6.0, format="%.2f", min_value=0.1, key="l_w1")
                    h1 = st.number_input("Yükseklik (m):", value=2.0, format="%.2f", min_value=0.1, key="l_h1")

                with col2:
                    st.write("**Dikey dikdörtgen:**")
                    w2 = st.number_input("Genişlik (m):", value=2.0, format="%.2f", min_value=0.1, key="l_w2")
                    h2 = st.number_input("Yükseklik (m):", value=4.0, format="%.2f", min_value=0.1, key="l_h2")

                # Alanlar (kütle orantılı)
                A1 = w1 * h1
                A2 = w2 * h2

                # Her parçanın merkezi
                x1, y1 = w1/2, h1/2
                x2, y2 = w2/2, h1 + h2/2

                # Toplam kütle merkezi
                x_cm = (A1 * x1 + A2 * x2) / (A1 + A2)
                y_cm = (A1 * y1 + A2 * y2) / (A1 + A2)

                st.success(f"**L şekli kütle merkezi:** ({x_cm:.3f}, {y_cm:.3f}) m")

                # Görselleştirme
                fig = go.Figure()

                # Alt dikdörtgen
                fig.add_trace(go.Scatter(
                    x=[0, w1, w1, 0, 0],
                    y=[0, 0, h1, h1, 0],
                    mode='lines',
                    name='Alt parça',
                    line=dict(color='blue', width=3),
                    fill='toself',
                    fillcolor='rgba(0, 0, 255, 0.3)'
                ))

                # Dikey dikdörtgen
                fig.add_trace(go.Scatter(
                    x=[0, w2, w2, 0, 0],
                    y=[h1, h1, h1+h2, h1+h2, h1],
                    mode='lines',
                    name='Üst parça',
                    line=dict(color='green', width=3),
                    fill='toself',
                    fillcolor='rgba(0, 255, 0, 0.3)'
                ))

                # Kütle merkezi
                fig.add_trace(go.Scatter(
                    x=[x_cm], y=[y_cm],
                    mode='markers+text',
                    name='Kütle Merkezi',
                    marker=dict(color='red', size=15, symbol='x'),
                    text=['CM'],
                    textposition='top center'
                ))

                fig.update_layout(
                    title=f"L Şekli Kütle Merkezi: ({x_cm:.2f}, {y_cm:.2f})",
                    xaxis_title="X (m)",
                    yaxis_title="Y (m)",
                    showlegend=True,
                    width=600,
                    height=600,
                    xaxis=dict(scaleanchor="y", scaleratio=1),
                    yaxis=dict(scaleanchor="x", scaleratio=1)
                )

                st.plotly_chart(fig)

            else:  # T Şekli
                st.info("T şekli için benzer şekilde hesaplanır (iki dikdörtgen).")

    # TAB 4: Dönme Dinamiği
    with tab4:
        st.subheader("⚙️ Dönme Hareketi Dinamiği")

        alt_tab = st.radio(
            "Hesaplama seç:",
            ["Eylemsizlik Momenti", "Dönme Dinamiği (τ = Iα)", "Dönme Kinetik Enerjisi"],
            horizontal=True
        )

        if alt_tab == "Eylemsizlik Momenti":
            st.write("**Eylemsizlik Momenti (I):** Cismin dönmeye karşı direncidir")

            shape = st.selectbox(
                "Geometrik şekil:",
                ["Nokta Kütle", "Çubuk (merkez eksen)", "Çubuk (uç eksen)", "Disk/Silindir", "Küre (katı)", "Halka"]
            )

            if shape == "Nokta Kütle":
                st.latex(r"I = mr^2")
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Kütle m (kg):", value=5.0, format="%.2f", min_value=0.01, key="I_point_m")
                with col2:
                    r = st.number_input("Dönme yarıçapı r (m):", value=2.0, format="%.2f", min_value=0.0, key="I_point_r")

                I = m * r**2
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

            elif shape == "Çubuk (merkez eksen)":
                st.latex(r"I = \frac{1}{12}mL^2")
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01, key="I_rod_m")
                with col2:
                    L = st.number_input("Uzunluk L (m):", value=2.0, format="%.2f", min_value=0.01, key="I_rod_L")

                I = (1/12) * m * L**2
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

            elif shape == "Çubuk (uç eksen)":
                st.latex(r"I = \frac{1}{3}mL^2")
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01, key="I_rod_end_m")
                with col2:
                    L = st.number_input("Uzunluk L (m):", value=2.0, format="%.2f", min_value=0.01, key="I_rod_end_L")

                I = (1/3) * m * L**2
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

            elif shape == "Disk/Silindir":
                st.latex(r"I = \frac{1}{2}mR^2")
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Kütle m (kg):", value=20.0, format="%.2f", min_value=0.01, key="I_disk_m")
                with col2:
                    R = st.number_input("Yarıçap R (m):", value=0.5, format="%.2f", min_value=0.01, key="I_disk_R")

                I = 0.5 * m * R**2
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

            elif shape == "Küre (katı)":
                st.latex(r"I = \frac{2}{5}mR^2")
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Kütle m (kg):", value=15.0, format="%.2f", min_value=0.01, key="I_sphere_m")
                with col2:
                    R = st.number_input("Yarıçap R (m):", value=0.3, format="%.2f", min_value=0.01, key="I_sphere_R")

                I = 0.4 * m * R**2
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

            else:  # Halka
                st.latex(r"I = mR^2")
                col1, col2 = st.columns(2)
                with col1:
                    m = st.number_input("Kütle m (kg):", value=5.0, format="%.2f", min_value=0.01, key="I_ring_m")
                with col2:
                    R = st.number_input("Yarıçap R (m):", value=1.0, format="%.2f", min_value=0.01, key="I_ring_R")

                I = m * R**2
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

        elif alt_tab == "Dönme Dinamiği (τ = Iα)":
            st.write("**Dönme hareketi için Newton'un 2. Yasası:**")
            st.latex(r"\tau_{net} = I \cdot \alpha")

            hesaplama = st.radio("Ne hesaplamak istiyorsunuz?", ["Açısal İvme (α)", "Tork (τ)", "Eylemsizlik Momenti (I)"], horizontal=True)

            if hesaplama == "Açısal İvme (α)":
                col1, col2 = st.columns(2)
                with col1:
                    tau = st.number_input("Net Tork τ (N·m):", value=50.0, format="%.2f", key="rot_tau")
                with col2:
                    I = st.number_input("Eylemsizlik Momenti I (kg·m²):", value=10.0, format="%.3f", min_value=0.01, key="rot_I")

                alpha = tau / I
                st.success(f"**Açısal İvme:** α = {alpha:.3f} rad/s²")

            elif hesaplama == "Tork (τ)":
                col1, col2 = st.columns(2)
                with col1:
                    I = st.number_input("Eylemsizlik Momenti I (kg·m²):", value=10.0, format="%.3f", min_value=0.01, key="rot_I2")
                with col2:
                    alpha = st.number_input("Açısal İvme α (rad/s²):", value=5.0, format="%.3f", key="rot_alpha")

                tau = I * alpha
                st.success(f"**Net Tork:** τ = {tau:.3f} N·m")

            else:  # I
                col1, col2 = st.columns(2)
                with col1:
                    tau = st.number_input("Net Tork τ (N·m):", value=50.0, format="%.2f", key="rot_tau2")
                with col2:
                    alpha = st.number_input("Açısal İvme α (rad/s²):", value=5.0, format="%.3f", min_value=0.01, key="rot_alpha2")

                I = tau / alpha
                st.success(f"**Eylemsizlik Momenti:** I = {I:.3f} kg·m²")

        else:  # Dönme Kinetik Enerjisi
            st.write("**Dönme Kinetik Enerjisi:**")
            st.latex(r"KE_{rot} = \frac{1}{2}I\omega^2")

            col1, col2 = st.columns(2)
            with col1:
                I = st.number_input("Eylemsizlik Momenti I (kg·m²):", value=5.0, format="%.3f", min_value=0.01, key="ke_rot_I")
            with col2:
                omega = st.number_input("Açısal Hız ω (rad/s):", value=10.0, format="%.3f", key="ke_rot_omega")

            KE_rot = 0.5 * I * omega**2
            st.success(f"**Dönme Kinetik Enerjisi:** KE_rot = {KE_rot:.3f} J")

            # Grafik
            omega_range = np.linspace(0, omega*2, 100)
            KE_range = 0.5 * I * omega_range**2

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=omega_range, y=KE_range,
                mode='lines',
                name='KE_rot(ω)',
                line=dict(color='purple', width=3)
            ))
            fig.add_trace(go.Scatter(
                x=[omega], y=[KE_rot],
                mode='markers',
                name='Mevcut durum',
                marker=dict(color='red', size=12)
            ))

            fig.update_layout(
                title=f"Dönme Kinetik Enerjisi (I={I} kg·m²)",
                xaxis_title="Açısal Hız ω (rad/s)",
                yaxis_title="Kinetik Enerji (J)",
                showlegend=True,
                width=700,
                height=400
            )
            st.plotly_chart(fig)
