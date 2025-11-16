import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show():
    st.markdown('<h2 class="module-header">〰️ Modül 7: Salınımlar ve Dalgalar</h2>', unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔄 Yay-Kütle Sistemi", "⚖️ Basit Sarkaç"])

    # TAB 1: Yay-Kütle Sistemi
    with tab1:
        st.subheader("🔄 Yay-Kütle Sistemi (Basit Harmonik Hareket)")

        st.write("**Basit Harmonik Hareket Denklemleri:**")
        st.latex(r"x(t) = A \cos(\omega t + \phi)")
        st.latex(r"v(t) = -A\omega \sin(\omega t + \phi)")
        st.latex(r"a(t) = -A\omega^2 \cos(\omega t + \phi)")

        st.write("**Açısal Frekans:**")
        st.latex(r"\omega = \sqrt{\frac{k}{m}}")

        st.write("**Periyot ve Frekans:**")
        st.latex(r"T = \frac{2\pi}{\omega} = 2\pi\sqrt{\frac{m}{k}}")
        st.latex(r"f = \frac{1}{T}")

        col1, col2 = st.columns(2)

        with col1:
            m = st.number_input("Kütle m (kg):", value=2.0, format="%.2f", min_value=0.01, key="shm_m")
            k = st.number_input("Yay sabiti k (N/m):", value=50.0, format="%.2f", min_value=0.01, key="shm_k")

        with col2:
            A = st.number_input("Genlik A (m):", value=0.5, format="%.3f", min_value=0.001)
            phi_deg = st.number_input("Faz açısı φ (derece):", value=0.0, format="%.2f")

        phi = np.radians(phi_deg)
        omega = np.sqrt(k / m)
        T = 2 * np.pi / omega
        f = 1 / T

        # Maksimum hız ve ivme
        v_max = A * omega
        a_max = A * omega**2

        # Enerji
        E_total = 0.5 * k * A**2

        st.success(f"**Açısal frekans:** ω = {omega:.3f} rad/s")
        st.success(f"**Periyot:** T = {T:.3f} s")
        st.success(f"**Frekans:** f = {f:.3f} Hz")
        st.success(f"**Maksimum hız:** v_max = {v_max:.3f} m/s")
        st.success(f"**Maksimum ivme:** a_max = {a_max:.3f} m/s²")
        st.success(f"**Toplam mekanik enerji:** E = {E_total:.3f} J")

        # Simülasyon
        st.write("**Simülasyon:**")

        t_sim = st.slider("Simülasyon süresi (saniye):", min_value=1.0, max_value=20.0, value=10.0, step=0.5)

        t_array = np.linspace(0, t_sim, 500)
        x_array = A * np.cos(omega * t_array + phi)
        v_array = -A * omega * np.sin(omega * t_array + phi)
        a_array = -A * omega**2 * np.cos(omega * t_array + phi)

        # Enerji hesaplamaları
        KE_array = 0.5 * m * v_array**2
        PE_array = 0.5 * k * x_array**2

        # Grafikler
        fig = make_subplots(
            rows=4, cols=1,
            subplot_titles=("Konum x(t)", "Hız v(t)", "İvme a(t)", "Enerji"),
            vertical_spacing=0.08,
            row_heights=[0.25, 0.25, 0.25, 0.25]
        )

        # Konum
        fig.add_trace(go.Scatter(
            x=t_array, y=x_array,
            mode='lines',
            name='x(t)',
            line=dict(color='blue', width=2)
        ), row=1, col=1)

        # Hız
        fig.add_trace(go.Scatter(
            x=t_array, y=v_array,
            mode='lines',
            name='v(t)',
            line=dict(color='green', width=2)
        ), row=2, col=1)

        # İvme
        fig.add_trace(go.Scatter(
            x=t_array, y=a_array,
            mode='lines',
            name='a(t)',
            line=dict(color='red', width=2)
        ), row=3, col=1)

        # Enerji
        fig.add_trace(go.Scatter(
            x=t_array, y=KE_array,
            mode='lines',
            name='KE (Kinetik)',
            line=dict(color='orange', width=2)
        ), row=4, col=1)

        fig.add_trace(go.Scatter(
            x=t_array, y=PE_array,
            mode='lines',
            name='PE (Potansiyel)',
            line=dict(color='purple', width=2)
        ), row=4, col=1)

        fig.add_trace(go.Scatter(
            x=t_array, y=KE_array + PE_array,
            mode='lines',
            name='Toplam Enerji',
            line=dict(color='black', width=2, dash='dash')
        ), row=4, col=1)

        fig.update_xaxes(title_text="Zaman (s)", row=4, col=1)
        fig.update_yaxes(title_text="x (m)", row=1, col=1)
        fig.update_yaxes(title_text="v (m/s)", row=2, col=1)
        fig.update_yaxes(title_text="a (m/s²)", row=3, col=1)
        fig.update_yaxes(title_text="Enerji (J)", row=4, col=1)

        fig.update_layout(height=1000, showlegend=True, title_text=f"Yay-Kütle Sistemi (T={T:.2f}s, f={f:.2f}Hz)")
        st.plotly_chart(fig)

        # Animasyon
        st.write("**Görsel Animasyon:**")

        # Belirli bir anı seç
        t_selected = st.slider("Zaman seçin (s):", min_value=0.0, max_value=t_sim, value=0.0, step=0.1)

        x_t = A * np.cos(omega * t_selected + phi)
        v_t = -A * omega * np.sin(omega * t_selected + phi)
        KE_t = 0.5 * m * v_t**2
        PE_t = 0.5 * k * x_t**2

        # Yay gösterimi
        fig2 = make_subplots(
            rows=1, cols=2,
            subplot_titles=(f"Yay-Kütle (t={t_selected:.2f}s)", "Enerji Dağılımı"),
            specs=[[{"type": "xy"}, {"type": "bar"}]],
            column_widths=[0.6, 0.4]
        )

        # Sol: Yay-Kütle görselleştirmesi
        # Sabit duvar
        fig2.add_trace(go.Scatter(
            x=[-0.5, -0.5], y=[-0.2, 0.2],
            mode='lines',
            name='Duvar',
            line=dict(color='brown', width=8)
        ), row=1, col=1)

        # Yay (zigzag çizimi)
        n_coils = 10
        spring_x = np.linspace(-0.4, x_t - 0.1, n_coils * 2)
        spring_y = np.zeros(n_coils * 2)
        for i in range(n_coils * 2):
            spring_y[i] = 0.05 * ((-1) ** i)

        fig2.add_trace(go.Scatter(
            x=spring_x, y=spring_y,
            mode='lines',
            name='Yay',
            line=dict(color='blue', width=2)
        ), row=1, col=1)

        # Kütle
        fig2.add_trace(go.Scatter(
            x=[x_t], y=[0],
            mode='markers+text',
            name='Kütle',
            marker=dict(color='red', size=30, symbol='square'),
            text=[f'm={m}kg'],
            textposition='top center'
        ), row=1, col=1)

        # Denge konumu
        fig2.add_trace(go.Scatter(
            x=[0, 0], y=[-0.3, 0.3],
            mode='lines',
            name='Denge',
            line=dict(color='green', width=1, dash='dash')
        ), row=1, col=1)

        fig2.update_xaxes(title_text="Konum (m)", row=1, col=1, range=[-0.6, max(A, 0.5) + 0.2])
        fig2.update_yaxes(title_text="", row=1, col=1, range=[-0.4, 0.4], showticklabels=False)

        # Sağ: Enerji barları
        fig2.add_trace(go.Bar(
            x=['Kinetik', 'Potansiyel', 'Toplam'],
            y=[KE_t, PE_t, E_total],
            marker_color=['orange', 'purple', 'black'],
            name='Enerji',
            text=[f'{KE_t:.2f}J', f'{PE_t:.2f}J', f'{E_total:.2f}J'],
            textposition='auto'
        ), row=1, col=2)

        fig2.update_xaxes(title_text="", row=1, col=2)
        fig2.update_yaxes(title_text="Enerji (J)", row=1, col=2)

        fig2.update_layout(height=400, showlegend=False, title_text=f"Anlık Durum (x={x_t:.3f}m, v={v_t:.3f}m/s)")
        st.plotly_chart(fig2)

    # TAB 2: Basit Sarkaç
    with tab2:
        st.subheader("⚖️ Basit Sarkaç")

        st.write("**Basit Sarkaç (küçük açılar için):**")
        st.latex(r"\theta(t) = \theta_0 \cos(\omega t + \phi)")
        st.latex(r"\omega = \sqrt{\frac{g}{L}}")
        st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")

        col1, col2 = st.columns(2)

        with col1:
            L = st.number_input("İp uzunluğu L (m):", value=2.0, format="%.2f", min_value=0.1, key="pendulum_L")
            g = st.number_input("Yerçekimi g (m/s²):", value=9.81, format="%.2f", key="pendulum_g")

        with col2:
            theta_0_deg = st.number_input("Başlangıç açısı θ₀ (derece):", value=15.0, format="%.2f", min_value=0.1, max_value=30.0)
            m = st.number_input("Kütle m (kg):", value=1.0, format="%.2f", min_value=0.01, key="pendulum_m")

        theta_0 = np.radians(theta_0_deg)
        omega = np.sqrt(g / L)
        T = 2 * np.pi / L * np.sqrt(L / g)
        f = 1 / T

        st.success(f"**Açısal frekans:** ω = {omega:.3f} rad/s")
        st.success(f"**Periyot:** T = {T:.3f} s")
        st.success(f"**Frekans:** f = {f:.3f} Hz")

        # Not
        if theta_0_deg > 15:
            st.warning("⚠️ Açı 15° üzerinde, küçük açı yaklaşımı hata verebilir.")

        # Simülasyon
        st.write("**Simülasyon:**")

        t_sim = st.slider("Simülasyon süresi (saniye):", min_value=5.0, max_value=30.0, value=15.0, step=1.0, key="pendulum_sim")

        t_array = np.linspace(0, t_sim, 500)
        theta_array = theta_0 * np.cos(omega * t_array)
        theta_dot_array = -theta_0 * omega * np.sin(omega * t_array)

        # Pozisyon (kartezyen)
        x_array = L * np.sin(theta_array)
        y_array = -L * np.cos(theta_array)

        # Hız (çizgisel)
        v_array = L * theta_dot_array

        # Enerji
        h_array = L * (1 - np.cos(theta_array))
        PE_array = m * g * h_array
        KE_array = 0.5 * m * v_array**2
        E_total = m * g * L * (1 - np.cos(theta_0))

        # Grafikler
        fig = make_subplots(
            rows=3, cols=1,
            subplot_titles=("Açı θ(t)", "Açısal Hız θ'(t)", "Enerji"),
            vertical_spacing=0.12,
            row_heights=[0.33, 0.33, 0.34]
        )

        # Açı
        fig.add_trace(go.Scatter(
            x=t_array, y=np.degrees(theta_array),
            mode='lines',
            name='θ(t)',
            line=dict(color='blue', width=2)
        ), row=1, col=1)

        # Açısal hız
        fig.add_trace(go.Scatter(
            x=t_array, y=theta_dot_array,
            mode='lines',
            name="θ'(t)",
            line=dict(color='green', width=2)
        ), row=2, col=1)

        # Enerji
        fig.add_trace(go.Scatter(
            x=t_array, y=KE_array,
            mode='lines',
            name='KE (Kinetik)',
            line=dict(color='orange', width=2)
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x=t_array, y=PE_array,
            mode='lines',
            name='PE (Potansiyel)',
            line=dict(color='purple', width=2)
        ), row=3, col=1)

        fig.add_trace(go.Scatter(
            x=t_array, y=KE_array + PE_array,
            mode='lines',
            name='Toplam Enerji',
            line=dict(color='black', width=2, dash='dash')
        ), row=3, col=1)

        fig.update_xaxes(title_text="Zaman (s)", row=3, col=1)
        fig.update_yaxes(title_text="Açı (derece)", row=1, col=1)
        fig.update_yaxes(title_text="Açısal Hız (rad/s)", row=2, col=1)
        fig.update_yaxes(title_text="Enerji (J)", row=3, col=1)

        fig.update_layout(height=800, showlegend=True, title_text=f"Basit Sarkaç (L={L}m, T={T:.2f}s)")
        st.plotly_chart(fig)

        # Animasyon
        st.write("**Görsel Animasyon:**")

        t_selected = st.slider("Zaman seçin (s):", min_value=0.0, max_value=t_sim, value=0.0, step=0.1, key="pendulum_t")

        theta_t = theta_0 * np.cos(omega * t_selected)
        theta_dot_t = -theta_0 * omega * np.sin(omega * t_selected)
        x_t = L * np.sin(theta_t)
        y_t = -L * np.cos(theta_t)
        v_t = L * theta_dot_t

        h_t = L * (1 - np.cos(theta_t))
        PE_t = m * g * h_t
        KE_t = 0.5 * m * v_t**2

        # Sarkaç gösterimi
        fig2 = make_subplots(
            rows=1, cols=2,
            subplot_titles=(f"Sarkaç (t={t_selected:.2f}s)", "Enerji Dağılımı"),
            specs=[[{"type": "xy"}, {"type": "bar"}]],
            column_widths=[0.6, 0.4]
        )

        # Sol: Sarkaç
        # Sabitleme noktası
        fig2.add_trace(go.Scatter(
            x=[0], y=[0],
            mode='markers',
            name='Sabitleme',
            marker=dict(color='black', size=15, symbol='x')
        ), row=1, col=1)

        # İp
        fig2.add_trace(go.Scatter(
            x=[0, x_t], y=[0, y_t],
            mode='lines',
            name='İp',
            line=dict(color='gray', width=3)
        ), row=1, col=1)

        # Kütle
        fig2.add_trace(go.Scatter(
            x=[x_t], y=[y_t],
            mode='markers+text',
            name='Kütle',
            marker=dict(color='red', size=25, symbol='circle'),
            text=[f'm={m}kg'],
            textposition='bottom center'
        ), row=1, col=1)

        # Yörünge (yay)
        theta_arc = np.linspace(-theta_0, theta_0, 50)
        x_arc = L * np.sin(theta_arc)
        y_arc = -L * np.cos(theta_arc)

        fig2.add_trace(go.Scatter(
            x=x_arc, y=y_arc,
            mode='lines',
            name='Yörünge',
            line=dict(color='lightblue', width=1, dash='dash')
        ), row=1, col=1)

        # Denge konumu (düşey)
        fig2.add_trace(go.Scatter(
            x=[0, 0], y=[0, -L],
            mode='lines',
            name='Denge',
            line=dict(color='green', width=1, dash='dash')
        ), row=1, col=1)

        fig2.update_xaxes(title_text="X (m)", row=1, col=1, range=[-L*1.2, L*1.2])
        fig2.update_yaxes(title_text="Y (m)", row=1, col=1, range=[-L*1.2, 0.2], scaleanchor="x", scaleratio=1)

        # Sağ: Enerji barları
        fig2.add_trace(go.Bar(
            x=['Kinetik', 'Potansiyel', 'Toplam'],
            y=[KE_t, PE_t, E_total],
            marker_color=['orange', 'purple', 'black'],
            name='Enerji',
            text=[f'{KE_t:.3f}J', f'{PE_t:.3f}J', f'{E_total:.3f}J'],
            textposition='auto'
        ), row=1, col=2)

        fig2.update_xaxes(title_text="", row=1, col=2)
        fig2.update_yaxes(title_text="Enerji (J)", row=1, col=2)

        fig2.update_layout(height=500, showlegend=False, title_text=f"Anlık Durum (θ={np.degrees(theta_t):.2f}°, v={v_t:.3f}m/s)")
        st.plotly_chart(fig2)

        st.info("""
        **Not:** Bu simülasyon küçük açı yaklaşımı kullanır (sin θ ≈ θ).
        Büyük açılar için gerçek sarkaç hareketi daha karmaşıktır ve periyot açıya bağlıdır.
        """)
