import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def show():
    st.markdown('<h2 class="module-header">🏃 Modül 2: Kinematik (Hareketin Tanımı)</h2>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📏 1D Hareket", "🎯 2D Atışlar", "⭕ Dairesel Hareket"])

    # TAB 1: 1D Hareket
    with tab1:
        st.subheader("📏 Bir Boyutta Hareket")

        hareket_tipi = st.radio(
            "Hareket tipi:",
            ["Sabit Hızlı Hareket", "Sabit İvmeli Hareket", "Serbest Düşme Simülasyonu"],
            horizontal=True
        )

        if hareket_tipi == "Sabit Hızlı Hareket":
            st.write("**Formül:** x = x₀ + v·t")

            col1, col2 = st.columns(2)
            with col1:
                x0 = st.number_input("İlk konum x₀ (m):", value=0.0, format="%.2f")
                v = st.number_input("Hız v (m/s):", value=10.0, format="%.2f")
            with col2:
                t = st.number_input("Zaman t (s):", value=5.0, format="%.2f", min_value=0.0)

            x = x0 + v * t
            st.success(f"**Konum:** x = {x:.2f} m")

            # Grafik
            t_array = np.linspace(0, t*1.5, 100)
            x_array = x0 + v * t_array

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=t_array, y=x_array, mode='lines', name='Konum-Zaman',
                                    line=dict(color='blue', width=3)))
            fig.add_trace(go.Scatter(x=[t], y=[x], mode='markers', name=f't={t}s',
                                    marker=dict(color='red', size=12)))

            fig.update_layout(
                title="Konum-Zaman Grafiği (Sabit Hız)",
                xaxis_title="Zaman (s)",
                yaxis_title="Konum (m)",
                showlegend=True,
                width=700,
                height=400
            )
            st.plotly_chart(fig)

        elif hareket_tipi == "Sabit İvmeli Hareket":
            st.write("**Hareket Denklemleri:**")
            st.latex(r"v = v_0 + at")
            st.latex(r"x = x_0 + v_0 t + \frac{1}{2}at^2")
            st.latex(r"v^2 = v_0^2 + 2a(x - x_0)")

            col1, col2, col3 = st.columns(3)
            with col1:
                x0 = st.number_input("İlk konum x₀ (m):", value=0.0, format="%.2f")
                v0 = st.number_input("İlk hız v₀ (m/s):", value=0.0, format="%.2f")
            with col2:
                a = st.number_input("İvme a (m/s²):", value=2.0, format="%.2f")
                t = st.number_input("Zaman t (s):", value=10.0, format="%.2f", min_value=0.0)

            # Hesaplamalar
            v = v0 + a * t
            x = x0 + v0 * t + 0.5 * a * t**2

            st.success(f"**Son hız:** v = {v:.2f} m/s")
            st.success(f"**Son konum:** x = {x:.2f} m")

            # Grafikler
            t_array = np.linspace(0, t, 100)
            x_array = x0 + v0 * t_array + 0.5 * a * t_array**2
            v_array = v0 + a * t_array

            fig = make_subplots(
                rows=2, cols=1,
                subplot_titles=("Konum-Zaman", "Hız-Zaman"),
                vertical_spacing=0.15
            )

            fig.add_trace(go.Scatter(x=t_array, y=x_array, mode='lines', name='x(t)',
                                    line=dict(color='blue', width=3)), row=1, col=1)
            fig.add_trace(go.Scatter(x=t_array, y=v_array, mode='lines', name='v(t)',
                                    line=dict(color='green', width=3)), row=2, col=1)

            fig.update_xaxes(title_text="Zaman (s)", row=2, col=1)
            fig.update_yaxes(title_text="Konum (m)", row=1, col=1)
            fig.update_yaxes(title_text="Hız (m/s)", row=2, col=1)

            fig.update_layout(height=600, showlegend=True, title_text="Sabit İvmeli Hareket Grafikleri")
            st.plotly_chart(fig)

        elif hareket_tipi == "Serbest Düşme Simülasyonu":
            st.write("**Serbest düşme:** a = g = 9.81 m/s² (aşağı yönde)")

            col1, col2 = st.columns(2)
            with col1:
                h0 = st.number_input("İlk yükseklik h₀ (m):", value=100.0, format="%.2f", min_value=0.0)
                v0 = st.number_input("İlk hız v₀ (m/s, yukarı +):", value=0.0, format="%.2f")
            with col2:
                g = st.number_input("Yerçekimi ivmesi g (m/s²):", value=9.81, format="%.2f")

            # Yere çarpma zamanı (h = h0 + v0*t - 0.5*g*t^2 = 0)
            # -0.5*g*t^2 + v0*t + h0 = 0
            # Çözüm: t = (-v0 ± sqrt(v0^2 + 2*g*h0)) / (-g)
            discriminant = v0**2 + 2 * g * h0
            if discriminant >= 0:
                t_hit = (-v0 + np.sqrt(discriminant)) / g
                v_hit = v0 - g * t_hit

                st.success(f"**Yere çarpma zamanı:** t = {t_hit:.2f} s")
                st.success(f"**Yere çarpma hızı:** v = {abs(v_hit):.2f} m/s (aşağı)")

                # Simülasyon
                t_array = np.linspace(0, t_hit, 100)
                h_array = h0 + v0 * t_array - 0.5 * g * t_array**2
                v_array = v0 - g * t_array

                fig = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=("Yükseklik-Zaman", "Hız-Zaman")
                )

                fig.add_trace(go.Scatter(x=t_array, y=h_array, mode='lines', name='h(t)',
                                        line=dict(color='blue', width=3)), row=1, col=1)
                fig.add_trace(go.Scatter(x=t_array, y=v_array, mode='lines', name='v(t)',
                                        line=dict(color='red', width=3)), row=1, col=2)

                fig.update_xaxes(title_text="Zaman (s)", row=1, col=1)
                fig.update_xaxes(title_text="Zaman (s)", row=1, col=2)
                fig.update_yaxes(title_text="Yükseklik (m)", row=1, col=1)
                fig.update_yaxes(title_text="Hız (m/s)", row=1, col=2)

                fig.update_layout(height=400, showlegend=True, title_text="Serbest Düşme")
                st.plotly_chart(fig)
            else:
                st.error("Geçersiz parametreler! Cisim yere düşmeyecek.")

    # TAB 2: 2D Atışlar
    with tab2:
        st.subheader("🎯 İki Boyutta Hareket - Atışlar")

        atis_tipi = st.radio(
            "Atış tipi:",
            ["Eğik Atış", "Yatay Atış", "Nehir Problemi"],
            horizontal=True
        )

        if atis_tipi == "Eğik Atış":
            st.write("**Eğik Atış:** Cisim bir açı ile atılır.")

            col1, col2 = st.columns(2)
            with col1:
                v0 = st.number_input("İlk hız v₀ (m/s):", value=30.0, format="%.2f", min_value=0.1, key="egik_v0")
                angle = st.number_input("Atış açısı θ (derece):", value=45.0, format="%.2f", key="egik_angle")
                h0 = st.number_input("İlk yükseklik h₀ (m):", value=0.0, format="%.2f", key="egik_h0")
            with col2:
                g = st.number_input("Yerçekimi ivmesi g (m/s²):", value=9.81, format="%.2f", key="egik_g")

            # Bileşenler
            angle_rad = np.radians(angle)
            v0x = v0 * np.cos(angle_rad)
            v0y = v0 * np.sin(angle_rad)

            # Maksimum yükseklik zamanı
            t_max_height = v0y / g
            max_height = h0 + (v0y**2) / (2 * g)

            # Toplam uçuş süresi (y = h0 + v0y*t - 0.5*g*t^2 = 0)
            discriminant = v0y**2 + 2 * g * h0
            if discriminant >= 0:
                t_flight = (v0y + np.sqrt(discriminant)) / g
                range_x = v0x * t_flight

                st.success(f"**Maksimum yükseklik:** {max_height:.2f} m (t = {t_max_height:.2f} s)")
                st.success(f"**Toplam uçuş süresi:** {t_flight:.2f} s")
                st.success(f"**Menzil:** {range_x:.2f} m")

                # Yörünge simülasyonu
                t_array = np.linspace(0, t_flight, 200)
                x_array = v0x * t_array
                y_array = h0 + v0y * t_array - 0.5 * g * t_array**2

                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=x_array, y=y_array,
                    mode='lines',
                    name='Yörünge',
                    line=dict(color='blue', width=3)
                ))

                # Başlangıç ve bitiş noktaları
                fig.add_trace(go.Scatter(
                    x=[0], y=[h0],
                    mode='markers',
                    name='Başlangıç',
                    marker=dict(color='green', size=12, symbol='circle')
                ))

                fig.add_trace(go.Scatter(
                    x=[range_x], y=[0],
                    mode='markers',
                    name='İniş',
                    marker=dict(color='red', size=12, symbol='x')
                ))

                # Maksimum yükseklik noktası
                x_max = v0x * t_max_height
                fig.add_trace(go.Scatter(
                    x=[x_max], y=[max_height],
                    mode='markers',
                    name='Maks. Yükseklik',
                    marker=dict(color='orange', size=12, symbol='star')
                ))

                fig.update_layout(
                    title=f"Eğik Atış Yörüngesi (v₀={v0} m/s, θ={angle}°)",
                    xaxis_title="Yatay Mesafe (m)",
                    yaxis_title="Yükseklik (m)",
                    showlegend=True,
                    width=800,
                    height=500,
                    xaxis=dict(range=[0, range_x*1.1]),
                    yaxis=dict(range=[0, max_height*1.2])
                )

                st.plotly_chart(fig)

                # Hız bileşenleri grafikleri
                vx_array = np.full_like(t_array, v0x)
                vy_array = v0y - g * t_array

                fig2 = make_subplots(
                    rows=1, cols=2,
                    subplot_titles=("Yatay Hız (sabit)", "Düşey Hız")
                )

                fig2.add_trace(go.Scatter(x=t_array, y=vx_array, mode='lines', name='vₓ',
                                         line=dict(color='blue', width=3)), row=1, col=1)
                fig2.add_trace(go.Scatter(x=t_array, y=vy_array, mode='lines', name='vᵧ',
                                         line=dict(color='red', width=3)), row=1, col=2)

                fig2.update_xaxes(title_text="Zaman (s)", row=1, col=1)
                fig2.update_xaxes(title_text="Zaman (s)", row=1, col=2)
                fig2.update_yaxes(title_text="Hız (m/s)", row=1, col=1)
                fig2.update_yaxes(title_text="Hız (m/s)", row=1, col=2)

                fig2.update_layout(height=400, showlegend=True)
                st.plotly_chart(fig2)

            else:
                st.error("Geçersiz parametreler!")

        elif atis_tipi == "Yatay Atış":
            st.write("**Yatay Atış:** Cisim yatay olarak atılır (θ = 0°)")

            col1, col2 = st.columns(2)
            with col1:
                v0 = st.number_input("İlk hız v₀ (m/s):", value=20.0, format="%.2f", min_value=0.1, key="yatay_v0")
                h0 = st.number_input("Yükseklik h₀ (m):", value=50.0, format="%.2f", min_value=0.0, key="yatay_h0")
            with col2:
                g = st.number_input("Yerçekimi ivmesi g (m/s²):", value=9.81, format="%.2f", key="yatay_g")

            # Düşme süresi
            t_flight = np.sqrt(2 * h0 / g)
            range_x = v0 * t_flight
            v_final = np.sqrt(v0**2 + (g * t_flight)**2)

            st.success(f"**Uçuş süresi:** {t_flight:.2f} s")
            st.success(f"**Menzil:** {range_x:.2f} m")
            st.success(f"**Yere çarpma hızı:** {v_final:.2f} m/s")

            # Simülasyon
            t_array = np.linspace(0, t_flight, 100)
            x_array = v0 * t_array
            y_array = h0 - 0.5 * g * t_array**2

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=x_array, y=y_array,
                mode='lines',
                name='Yörünge',
                line=dict(color='purple', width=3)
            ))

            fig.add_trace(go.Scatter(
                x=[0], y=[h0],
                mode='markers',
                name='Başlangıç',
                marker=dict(color='green', size=12)
            ))

            fig.add_trace(go.Scatter(
                x=[range_x], y=[0],
                mode='markers',
                name='İniş',
                marker=dict(color='red', size=12)
            ))

            fig.update_layout(
                title=f"Yatay Atış (v₀={v0} m/s, h₀={h0} m)",
                xaxis_title="Yatay Mesafe (m)",
                yaxis_title="Yükseklik (m)",
                showlegend=True,
                width=800,
                height=500
            )

            st.plotly_chart(fig)

        elif atis_tipi == "Nehir Problemi":
            st.write("**Nehir Problemi:** Bir yüzücü akıntılı nehirde karşıya geçmeye çalışıyor.")

            col1, col2 = st.columns(2)
            with col1:
                v_swimmer = st.number_input("Yüzücünün hızı (m/s):", value=2.0, format="%.2f", min_value=0.1)
                v_river = st.number_input("Nehir akıntısı hızı (m/s):", value=1.5, format="%.2f", min_value=0.0)
            with col2:
                river_width = st.number_input("Nehir genişliği (m):", value=100.0, format="%.2f", min_value=1.0)
                angle = st.number_input("Yüzme açısı (derece, akıntıya göre):", value=90.0, format="%.2f")

            angle_rad = np.radians(angle)

            # Hız bileşenleri
            v_swim_x = v_swimmer * np.cos(angle_rad)  # Akıntı yönü
            v_swim_y = v_swimmer * np.sin(angle_rad)  # Karşıya

            # Net hız
            v_net_x = v_swim_x + v_river
            v_net_y = v_swim_y

            # Karşıya geçme süresi
            if v_swim_y > 0:
                t_cross = river_width / v_swim_y
                drift = v_net_x * t_cross
                v_net = np.sqrt(v_net_x**2 + v_net_y**2)

                st.success(f"**Karşıya geçme süresi:** {t_cross:.2f} s")
                st.success(f"**Akıntıda sürüklenme:** {drift:.2f} m")
                st.success(f"**Net hız:** {v_net:.2f} m/s")

                # Görselleştirme
                fig = go.Figure()

                # Yörünge
                t_array = np.linspace(0, t_cross, 50)
                x_array = v_net_x * t_array
                y_array = v_swim_y * t_array

                fig.add_trace(go.Scatter(
                    x=x_array, y=y_array,
                    mode='lines+markers',
                    name='Yüzücünün yolu',
                    line=dict(color='blue', width=3)
                ))

                # Başlangıç ve bitiş
                fig.add_trace(go.Scatter(
                    x=[0], y=[0],
                    mode='markers',
                    name='Başlangıç',
                    marker=dict(color='green', size=15, symbol='circle')
                ))

                fig.add_trace(go.Scatter(
                    x=[drift], y=[river_width],
                    mode='markers',
                    name='Varış',
                    marker=dict(color='red', size=15, symbol='x')
                ))

                # Hız vektörleri (başlangıç noktasında)
                scale = 20
                fig.add_annotation(
                    x=v_swim_x*scale, y=v_swim_y*scale,
                    ax=0, ay=0,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="purple",
                    text="Yüzücü hızı"
                )

                fig.add_annotation(
                    x=v_river*scale, y=0,
                    ax=0, ay=0,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="orange",
                    text="Akıntı hızı"
                )

                fig.update_layout(
                    title="Nehir Problemi - Yüzücünün Yolu",
                    xaxis_title="Akıntı Yönü (m)",
                    yaxis_title="Karşıya Mesafe (m)",
                    showlegend=True,
                    width=800,
                    height=600,
                    xaxis=dict(range=[-10, drift*1.2]),
                    yaxis=dict(range=[-10, river_width*1.1])
                )

                st.plotly_chart(fig)
            else:
                st.error("Yüzücü karşıya geçemiyor! Açıyı değiştirin.")

    # TAB 3: Dairesel Hareket
    with tab3:
        st.subheader("⭕ Düzgün Dairesel Hareket")

        st.write("**Formüller:**")
        st.latex(r"\omega = \frac{2\pi}{T} = 2\pi f")
        st.latex(r"v = \omega r")
        st.latex(r"a_c = \frac{v^2}{r} = \omega^2 r")
        st.latex(r"F_c = m \cdot a_c = \frac{mv^2}{r}")

        hesaplama_tipi = st.radio(
            "Hesaplama tipi:",
            ["Parametrelerden Hesapla", "Merkezcil Kuvvet"],
            horizontal=True
        )

        if hesaplama_tipi == "Parametrelerden Hesapla":
            col1, col2 = st.columns(2)

            with col1:
                bilinen = st.selectbox(
                    "Bilinen parametre:",
                    ["Periyot (T)", "Frekans (f)", "Açısal Hız (ω)"]
                )

                if bilinen == "Periyot (T)":
                    T = st.number_input("Periyot T (s):", value=2.0, format="%.3f", min_value=0.001)
                    f = 1 / T
                    omega = 2 * np.pi / T
                elif bilinen == "Frekans (f)":
                    f = st.number_input("Frekans f (Hz):", value=0.5, format="%.3f", min_value=0.001)
                    T = 1 / f
                    omega = 2 * np.pi * f
                else:  # Açısal hız
                    omega = st.number_input("Açısal hız ω (rad/s):", value=3.14, format="%.3f", min_value=0.001)
                    T = 2 * np.pi / omega
                    f = omega / (2 * np.pi)

            with col2:
                r = st.number_input("Yarıçap r (m):", value=5.0, format="%.2f", min_value=0.01)

            v = omega * r
            ac = omega**2 * r

            st.success(f"**Periyot (T):** {T:.3f} s")
            st.success(f"**Frekans (f):** {f:.3f} Hz")
            st.success(f"**Açısal hız (ω):** {omega:.3f} rad/s")
            st.success(f"**Çizgisel hız (v):** {v:.3f} m/s")
            st.success(f"**Merkezcil ivme (aᶜ):** {ac:.3f} m/s²")

            # Animasyon
            st.write("**Dairesel Hareket Gösterimi:**")

            theta_array = np.linspace(0, 2*np.pi, 100)
            x_circle = r * np.cos(theta_array)
            y_circle = r * np.sin(theta_array)

            # Animasyon için birkaç pozisyon
            n_frames = 8
            theta_frames = np.linspace(0, 2*np.pi, n_frames, endpoint=False)

            fig = go.Figure()

            # Daire
            fig.add_trace(go.Scatter(
                x=x_circle, y=y_circle,
                mode='lines',
                name='Yörünge',
                line=dict(color='lightblue', width=2, dash='dash')
            ))

            # Cisim pozisyonları
            for i, theta in enumerate(theta_frames):
                x_pos = r * np.cos(theta)
                y_pos = r * np.sin(theta)

                fig.add_trace(go.Scatter(
                    x=[x_pos], y=[y_pos],
                    mode='markers',
                    name=f't={i*T/n_frames:.2f}s',
                    marker=dict(size=12)
                ))

                # Hız vektörü (teğetsel)
                vx = -v * np.sin(theta)
                vy = v * np.cos(theta)
                fig.add_annotation(
                    x=x_pos + vx*0.2, y=y_pos + vy*0.2,
                    ax=x_pos, ay=y_pos,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="green"
                )

                # Merkezcil ivme vektörü (merkeze doğru)
                ax_c = -ac * np.cos(theta) * 0.2
                ay_c = -ac * np.sin(theta) * 0.2
                fig.add_annotation(
                    x=x_pos + ax_c, y=y_pos + ay_c,
                    ax=x_pos, ay=y_pos,
                    xref="x", yref="y",
                    axref="x", ayref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="red"
                )

            # Merkez
            fig.add_trace(go.Scatter(
                x=[0], y=[0],
                mode='markers',
                name='Merkez',
                marker=dict(color='black', size=10, symbol='x')
            ))

            fig.update_layout(
                title=f"Düzgün Dairesel Hareket (T={T:.2f}s, f={f:.2f}Hz)",
                xaxis_title="X (m)",
                yaxis_title="Y (m)",
                showlegend=True,
                width=700,
                height=700,
                xaxis=dict(scaleanchor="y", scaleratio=1),
                yaxis=dict(scaleanchor="x", scaleratio=1)
            )

            st.plotly_chart(fig)

            st.info("🟢 Yeşil oklar: Hız vektörleri (teğetsel) | 🔴 Kırmızı oklar: Merkezcil ivme (merkeze doğru)")

        else:  # Merkezcil Kuvvet
            st.write("Merkezcil kuvvet hesaplayıcı")

            col1, col2 = st.columns(2)
            with col1:
                m = st.number_input("Kütle m (kg):", value=2.0, format="%.2f", min_value=0.01)
                v = st.number_input("Hız v (m/s):", value=10.0, format="%.2f", min_value=0.01)
            with col2:
                r = st.number_input("Yarıçap r (m):", value=5.0, format="%.2f", min_value=0.01, key="fc_r")

            ac = v**2 / r
            Fc = m * ac

            st.success(f"**Merkezcil ivme:** aᶜ = {ac:.3f} m/s²")
            st.success(f"**Merkezcil kuvvet:** Fᶜ = {Fc:.3f} N")

            st.info(f"Bu kuvvet, {m} kg kütleli cismi {r} m yarıçaplı dairesel yörüngede {v} m/s hızla tutmak için gereklidir.")
