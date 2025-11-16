import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show():
    st.markdown('<h2 class="module-header">💥 Modül 5: Momentum ve Çarpışmalar</h2>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Momentum ve İtme", "💥 1D Çarpışmalar", "🎱 2D Çarpışmalar"])

    # TAB 1: Momentum ve İtme
    with tab1:
        st.subheader("📊 Momentum ve İtme (Impulse)")

        st.write("**Formüller:**")
        st.latex(r"p = mv \quad \text{(Momentum)}")
        st.latex(r"I = F \cdot \Delta t = \Delta p \quad \text{(İtme)}")

        hesaplama_tipi = st.radio(
            "Hesaplama tipi:",
            ["Momentum Hesapla", "İtme ve Momentum Değişimi"],
            horizontal=True
        )

        if hesaplama_tipi == "Momentum Hesapla":
            col1, col2 = st.columns(2)

            with col1:
                m = st.number_input("Kütle m (kg):", value=10.0, format="%.2f", min_value=0.01)
            with col2:
                v = st.number_input("Hız v (m/s):", value=5.0, format="%.2f")

            p = m * v

            st.success(f"**Momentum:** p = {p:.2f} kg·m/s")

            if v > 0:
                st.info("➡️ Momentum pozitif yönde")
            elif v < 0:
                st.info("⬅️ Momentum negatif yönde")
            else:
                st.info("⏸️ Cisim durgun, momentum sıfır")

        else:  # İtme
            st.write("Bir cisme uygulanan kuvvet momentumu değiştirir.")

            col1, col2 = st.columns(2)

            with col1:
                m = st.number_input("Kütle m (kg):", value=5.0, format="%.2f", min_value=0.01, key="impulse_m")
                v1 = st.number_input("İlk hız v₁ (m/s):", value=10.0, format="%.2f")
                v2 = st.number_input("Son hız v₂ (m/s):", value=20.0, format="%.2f")

            with col2:
                dt = st.number_input("Zaman aralığı Δt (s):", value=2.0, format="%.2f", min_value=0.01)

            p1 = m * v1
            p2 = m * v2
            dp = p2 - p1
            I = dp
            F_avg = I / dt

            st.success(f"**İlk momentum:** p₁ = {p1:.2f} kg·m/s")
            st.success(f"**Son momentum:** p₂ = {p2:.2f} kg·m/s")
            st.success(f"**Momentum değişimi:** Δp = {dp:.2f} kg·m/s")
            st.success(f"**İtme:** I = {I:.2f} N·s")
            st.success(f"**Ortalama kuvvet:** F_avg = {F_avg:.2f} N")

            # Görselleştirme
            fig = make_subplots(
                rows=1, cols=2,
                subplot_titles=("Momentum Değişimi", "Kuvvet-Zaman Grafiği")
            )

            # Sol: Momentum çubuğu
            fig.add_trace(go.Bar(
                x=['İlk', 'Son'],
                y=[p1, p2],
                marker_color=['blue', 'red'],
                name='Momentum',
                text=[f'{p1:.1f}', f'{p2:.1f}'],
                textposition='auto'
            ), row=1, col=1)

            # Sağ: Kuvvet-zaman (basit dikdörtgen)
            fig.add_trace(go.Scatter(
                x=[0, 0, dt, dt, 0],
                y=[0, F_avg, F_avg, 0, 0],
                mode='lines',
                name='Kuvvet',
                line=dict(color='green', width=3),
                fill='tozeroy',
                fillcolor='rgba(0, 255, 0, 0.3)'
            ), row=1, col=2)

            fig.update_xaxes(title_text="", row=1, col=1)
            fig.update_yaxes(title_text="Momentum (kg·m/s)", row=1, col=1)
            fig.update_xaxes(title_text="Zaman (s)", row=1, col=2)
            fig.update_yaxes(title_text="Kuvvet (N)", row=1, col=2)

            fig.update_layout(height=400, showlegend=True, title_text=f"İtme: I = {I:.2f} N·s")
            st.plotly_chart(fig)

            st.info(f"📐 Kuvvet-zaman grafiği altındaki alan = İtme = {I:.2f} N·s")

    # TAB 2: 1D Çarpışmalar
    with tab2:
        st.subheader("💥 Bir Boyutta Çarpışmalar")

        carpisma_tipi = st.radio(
            "Çarpışma tipi:",
            ["Elastik Çarpışma", "Tam İnelastik Çarpışma", "Kısmen İnelastik Çarpışma"],
            horizontal=True
        )

        st.write("**Momentum korunumu:**")
        st.latex(r"m_1 v_1 + m_2 v_2 = m_1 v_1' + m_2 v_2'")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Cisim 1:**")
            m1 = st.number_input("Kütle m₁ (kg):", value=2.0, format="%.2f", min_value=0.01, key="coll_m1")
            v1 = st.number_input("İlk hız v₁ (m/s):", value=5.0, format="%.2f", key="coll_v1")

        with col2:
            st.write("**Cisim 2:**")
            m2 = st.number_input("Kütle m₂ (kg):", value=3.0, format="%.2f", min_value=0.01, key="coll_m2")
            v2 = st.number_input("İlk hız v₂ (m/s):", value=0.0, format="%.2f", key="coll_v2")

        # Başlangıç momentumu ve enerjisi
        p_initial = m1 * v1 + m2 * v2
        KE_initial = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2

        if carpisma_tipi == "Elastik Çarpışma":
            st.write("**Elastik çarpışma:** Hem momentum hem de kinetik enerji korunur")

            # Elastik çarpışma formülleri
            v1_final = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
            v2_final = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)

            p_final = m1 * v1_final + m2 * v2_final
            KE_final = 0.5 * m1 * v1_final**2 + 0.5 * m2 * v2_final**2

            st.success(f"**Cisim 1 son hız:** v₁' = {v1_final:.3f} m/s")
            st.success(f"**Cisim 2 son hız:** v₂' = {v2_final:.3f} m/s")
            st.success(f"**Toplam momentum:** {p_initial:.3f} → {p_final:.3f} kg·m/s ✓")
            st.success(f"**Toplam kinetik enerji:** {KE_initial:.3f} → {KE_final:.3f} J ✓")

        elif carpisma_tipi == "Tam İnelastik Çarpışma":
            st.write("**Tam inelastik çarpışma:** Cisimler birleşir, sadece momentum korunur")

            # Birleşik hız
            v_final = (m1 * v1 + m2 * v2) / (m1 + m2)

            p_final = (m1 + m2) * v_final
            KE_final = 0.5 * (m1 + m2) * v_final**2
            energy_loss = KE_initial - KE_final

            st.success(f"**Birleşik cisim son hız:** v' = {v_final:.3f} m/s")
            st.success(f"**Toplam momentum:** {p_initial:.3f} → {p_final:.3f} kg·m/s ✓")
            st.warning(f"**Kinetik enerji:** {KE_initial:.3f} → {KE_final:.3f} J")
            st.warning(f"**Enerji kaybı:** {energy_loss:.3f} J (ısı, ses, deformasyon)")

        else:  # Kısmen İnelastik
            st.write("**Kısmen inelastik çarpışma:** Restitüsyon katsayısı e kullanılır")
            st.latex(r"e = \frac{v_2' - v_1'}{v_1 - v_2}")

            e = st.slider("Restitüsyon katsayısı e:", min_value=0.0, max_value=1.0, value=0.5, step=0.1)

            st.info(f"e = 0: Tam inelastik | e = 1: Elastik | e = {e}: Kısmen inelastik")

            # Momentum korunumu: m1*v1 + m2*v2 = m1*v1' + m2*v2'
            # Restitüsyon: e = (v2' - v1')/(v1 - v2)
            # İki bilinmeyen, iki denklem

            v_rel = v1 - v2
            if abs(v_rel) > 0.001:
                # Çözüm:
                v1_final = (m1 * v1 + m2 * v2 - m2 * e * v_rel) / (m1 + m2)
                v2_final = (m1 * v1 + m2 * v2 + m1 * e * v_rel) / (m1 + m2)

                p_final = m1 * v1_final + m2 * v2_final
                KE_final = 0.5 * m1 * v1_final**2 + 0.5 * m2 * v2_final**2
                energy_loss = KE_initial - KE_final

                st.success(f"**Cisim 1 son hız:** v₁' = {v1_final:.3f} m/s")
                st.success(f"**Cisim 2 son hız:** v₂' = {v2_final:.3f} m/s")
                st.success(f"**Toplam momentum:** {p_initial:.3f} → {p_final:.3f} kg·m/s ✓")
                st.warning(f"**Kinetik enerji:** {KE_initial:.3f} → {KE_final:.3f} J")
                st.warning(f"**Enerji kaybı:** {energy_loss:.3f} J ({energy_loss/KE_initial*100:.1f}%)")
            else:
                st.error("Cisimler zaten aynı hızda, çarpışma yok!")
                v1_final = v1
                v2_final = v2

        # Animasyon
        st.write("**Çarpışma Animasyonu:**")

        fig = go.Figure()

        # Zaman çizelgesi
        t_before = 2  # Çarpışma öncesi süre
        t_collision = 0.1  # Çarpışma anı
        t_after = 2  # Çarpışma sonrası

        # Çarpışma konumunu belirle
        # v1*t = collision_x - start_x1
        # v2*t = collision_x - start_x2
        # Basitlik için collision_x = 0 alalım

        collision_x = 0
        start_x1 = collision_x - v1 * t_before
        start_x2 = collision_x - v2 * t_before

        frames = []
        n_frames = 60

        for i in range(n_frames):
            if i < n_frames * 0.4:  # Öncesi
                t = i / (n_frames * 0.4) * t_before
                x1 = start_x1 + v1 * t
                x2 = start_x2 + v2 * t
            elif i < n_frames * 0.5:  # Çarpışma
                x1 = collision_x
                x2 = collision_x
            else:  # Sonrası
                t = (i - n_frames * 0.5) / (n_frames * 0.5) * t_after
                if carpisma_tipi == "Tam İnelastik Çarpışma":
                    x1 = collision_x + v_final * t
                    x2 = collision_x + v_final * t
                else:
                    x1 = collision_x + v1_final * t
                    x2 = collision_x + v2_final * t

            frame_data = [
                go.Scatter(
                    x=[x1], y=[0],
                    mode='markers+text',
                    marker=dict(size=30, color='red'),
                    text=[f'm₁'],
                    textposition='top center',
                    name='Cisim 1'
                ),
                go.Scatter(
                    x=[x2], y=[0.5],
                    mode='markers+text',
                    marker=dict(size=30, color='blue'),
                    text=[f'm₂'],
                    textposition='top center',
                    name='Cisim 2'
                )
            ]

            frames.append(go.Frame(data=frame_data, name=str(i)))

        # İlk frame
        fig.add_trace(go.Scatter(
            x=[start_x1], y=[0],
            mode='markers+text',
            marker=dict(size=30, color='red'),
            text=[f'm₁'],
            textposition='top center',
            name='Cisim 1'
        ))

        fig.add_trace(go.Scatter(
            x=[start_x2], y=[0.5],
            mode='markers+text',
            marker=dict(size=30, color='blue'),
            text=[f'm₂'],
            textposition='top center',
            name='Cisim 2'
        ))

        fig.update_layout(
            xaxis=dict(range=[min(start_x1, start_x2) - 5, max(start_x1, start_x2) + 10], zeroline=True),
            yaxis=dict(range=[-1, 2], showticklabels=False),
            title="Çarpışma Simülasyonu (Basitleştirilmiş)",
            showlegend=True,
            height=300,
            updatemenus=[dict(
                type="buttons",
                buttons=[dict(label="▶ Oynat", method="animate", args=[None, {"frame": {"duration": 50}}])]
            )],
            frames=frames
        )

        st.plotly_chart(fig)

    # TAB 3: 2D Çarpışmalar
    with tab3:
        st.subheader("🎱 İki Boyutta Çarpışmalar")

        st.write("2D çarpışmalarda hem x hem y yönünde momentum korunur:")
        st.latex(r"m_1 v_{1x} + m_2 v_{2x} = m_1 v_{1x}' + m_2 v_{2x}'")
        st.latex(r"m_1 v_{1y} + m_2 v_{2y} = m_1 v_{1y}' + m_2 v_{2y}'")

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Cisim 1:**")
            m1 = st.number_input("Kütle m₁ (kg):", value=2.0, format="%.2f", min_value=0.01, key="2d_m1")
            v1x = st.number_input("İlk hız v₁ₓ (m/s):", value=3.0, format="%.2f", key="2d_v1x")
            v1y = st.number_input("İlk hız v₁ᵧ (m/s):", value=0.0, format="%.2f", key="2d_v1y")

        with col2:
            st.write("**Cisim 2:**")
            m2 = st.number_input("Kütle m₂ (kg):", value=1.0, format="%.2f", min_value=0.01, key="2d_m2")
            v2x = st.number_input("İlk hız v₂ₓ (m/s):", value=0.0, format="%.2f", key="2d_v2x")
            v2y = st.number_input("İlk hız v₂ᵧ (m/s):", value=2.0, format="%.2f", key="2d_v2y")

        carpisma_2d = st.radio(
            "Çarpışma tipi:",
            ["Tam İnelastik (Birleşme)", "Elastik (Basitleştirilmiş)"],
            horizontal=True
        )

        # Başlangıç momentumu
        px_initial = m1 * v1x + m2 * v2x
        py_initial = m1 * v1y + m2 * v2y
        p_total_initial = np.sqrt(px_initial**2 + py_initial**2)

        KE_initial = 0.5 * m1 * (v1x**2 + v1y**2) + 0.5 * m2 * (v2x**2 + v2y**2)

        if carpisma_2d == "Tam İnelastik (Birleşme)":
            # Birleşik hız
            vx_final = px_initial / (m1 + m2)
            vy_final = py_initial / (m1 + m2)
            v_final_mag = np.sqrt(vx_final**2 + vy_final**2)

            px_final = (m1 + m2) * vx_final
            py_final = (m1 + m2) * vy_final

            KE_final = 0.5 * (m1 + m2) * (vx_final**2 + vy_final**2)
            energy_loss = KE_initial - KE_final

            st.success(f"**Birleşik cisim son hızı:**")
            st.success(f"   vₓ' = {vx_final:.3f} m/s")
            st.success(f"   vᵧ' = {vy_final:.3f} m/s")
            st.success(f"   |v'| = {v_final_mag:.3f} m/s")
            st.success(f"**Momentum korunumu:** ({px_initial:.2f}, {py_initial:.2f}) → ({px_final:.2f}, {py_final:.2f}) ✓")
            st.warning(f"**Enerji kaybı:** {energy_loss:.3f} J")

        else:  # Elastik (basitleştirilmiş - merkezi çarpışma değil, genel durum)
            st.info("Elastik 2D çarpışma çok değişkenli. Basitleştirilmiş örnek:")

            # Basit bir yaklaşım: momentum korunumu + enerji korunumu
            # Gerçek çözüm için çarpışma açısı gerekli, burada basitleştirilmiş gösteriyoruz

            # Tam çözüm için çok karmaşık, burada sadece momentum korunumunu gösterelim
            st.warning("Tam elastik 2D çarpışma için çarpışma geometrisi (açılar) gereklidir.")
            st.info("Momentum korunumu:")
            st.success(f"   Toplam pₓ = {px_initial:.3f} kg·m/s")
            st.success(f"   Toplam pᵧ = {py_initial:.3f} kg·m/s")

        # Görselleştirme
        fig = go.Figure()

        # Cisim 1 yörüngesi (öncesi)
        t_before = 2
        x1_path = np.array([v1x * (-t) for t in np.linspace(t_before, 0, 20)])
        y1_path = np.array([v1y * (-t) for t in np.linspace(t_before, 0, 20)])

        fig.add_trace(go.Scatter(
            x=x1_path, y=y1_path,
            mode='lines',
            name='Cisim 1 yolu',
            line=dict(color='red', width=2, dash='dash')
        ))

        # Cisim 2 yörüngesi (öncesi)
        x2_path = np.array([v2x * (-t) for t in np.linspace(t_before, 0, 20)])
        y2_path = np.array([v2y * (-t) for t in np.linspace(t_before, 0, 20)])

        fig.add_trace(go.Scatter(
            x=x2_path, y=y2_path,
            mode='lines',
            name='Cisim 2 yolu',
            line=dict(color='blue', width=2, dash='dash')
        ))

        # Başlangıç pozisyonları
        fig.add_trace(go.Scatter(
            x=[x1_path[0]], y=[y1_path[0]],
            mode='markers+text',
            name='m₁ başlangıç',
            marker=dict(color='red', size=15),
            text=['m₁'],
            textposition='top center'
        ))

        fig.add_trace(go.Scatter(
            x=[x2_path[0]], y=[y2_path[0]],
            mode='markers+text',
            name='m₂ başlangıç',
            marker=dict(color='blue', size=15),
            text=['m₂'],
            textposition='top center'
        ))

        # Çarpışma noktası
        fig.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            name='Çarpışma noktası',
            marker=dict(color='orange', size=20, symbol='x')
        ))

        # Sonrası yörünge
        if carpisma_2d == "Tam İnelastik (Birleşme)":
            t_after = 2
            x_final_path = np.array([vx_final * t for t in np.linspace(0, t_after, 20)])
            y_final_path = np.array([vy_final * t for t in np.linspace(0, t_after, 20)])

            fig.add_trace(go.Scatter(
                x=x_final_path, y=y_final_path,
                mode='lines+markers',
                name='Birleşik cisim yolu',
                line=dict(color='purple', width=3),
                marker=dict(size=5)
            ))

        # Hız vektörleri (başlangıçta)
        scale = 2
        fig.add_annotation(
            x=x1_path[0] + v1x*scale, y=y1_path[0] + v1y*scale,
            ax=x1_path[0], ay=y1_path[0],
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="red"
        )

        fig.add_annotation(
            x=x2_path[0] + v2x*scale, y=y2_path[0] + v2y*scale,
            ax=x2_path[0], ay=y2_path[0],
            xref="x", yref="y",
            axref="x", ayref="y",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=2,
            arrowcolor="blue"
        )

        fig.update_layout(
            title="2D Çarpışma Görselleştirmesi",
            xaxis_title="X (m)",
            yaxis_title="Y (m)",
            showlegend=True,
            width=700,
            height=700,
            xaxis=dict(scaleanchor="y", scaleratio=1, zeroline=True),
            yaxis=dict(scaleanchor="x", scaleratio=1, zeroline=True)
        )

        st.plotly_chart(fig)
