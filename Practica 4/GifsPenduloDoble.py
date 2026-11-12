import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint
import warnings


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.integrate import odeint

# ==========================================
# 1. PARÁMETROS DEL SISTEMA (Según el Póster)
# ==========================================
# Masas y longitudes (Sección 3)
m1, m2 = 1.0, 0.8      
l1, l2 = 1.0, 0.8      
g = 9.81               
k = 3.0                # Constante del resorte (N/m)

# Fuerza de excitación u(t) = 0.30*cos(1.2*t) (Sección 1)
F0 = 0.30
w_d = 1.2

def u(t):
    return F0 * np.cos(w_d * t)

# Constantes inerciales (Sección 2)
A = (m1 + m2) * l1**2
B_const = m2 * l1 * l2
C = m2 * l2**2

# ==========================================
# 2. ECUACIONES DE MOVIMIENTO (Lagrange)
# ==========================================
def derivadas(state, t, c_damp):
    th1, th2, w1, w2 = state
    delta = th1 - th2
    
    # Matrices de inercia
    M11 = A
    M12 = B_const * np.cos(delta)
    M21 = M12
    M22 = C
    
    # Fuerzas generalizadas (despejando términos no inerciales)
    F1 = l1 * u(t) * np.cos(th1) \
         - B_const * np.sin(delta) * w2**2 \
         - (m1 + m2) * g * l1 * np.sin(th1) \
         - k * (l1**2) * np.sin(th1) * np.cos(th1) \
         - c_damp * (l1**2) * (np.cos(th1)**2) * w1
         
    F2 = B_const * np.sin(delta) * w1**2 - m2 * g * l2 * np.sin(th2)
    
    # Resolver sistema por regla de Cramer
    det = M11 * M22 - M12 * M21
    dw1 = (F1 * M22 - F2 * M12) / det
    dw2 = (M11 * F2 - M21 * F1) / det
    
    return [w1, w2, dw1, dw2]

# ==========================================
# 3. CONDICIONES INICIALES Y SIMULACIÓN
# ==========================================
# theta1 = 0.35 rad, theta2 = -0.20 rad 
state0 = [0.35, -0.20, 0.0, 0.0]
t = np.linspace(0, 30, 900)  # Simulación de 30 segundos

# Simulación 1: Nominal Amortiguado (c = 0.15)
state_nom = odeint(derivadas, state0, t, args=(0.15,))

# Simulación 2: Caótico (c = 0.0 )
# Condiciones iniciales para caos: soltar desde 90 grados (pi/2)
state0_cao = [np.pi/2, 0.0, 0.0, 0.0] 
state_cao = odeint(derivadas, state0_cao, t, args=(0.0,))

# Transformación Cinemática a coordenadas XY (Sección 1)
def get_xy(state):
    th1, th2 = state[:, 0], state[:, 1]
    x1 = l1 * np.sin(th1)
    y1 = -l1 * np.cos(th1)
    x2 = x1 + l2 * np.sin(th2)
    y2 = y1 - l2 * np.cos(th2)
    return x1, y1, x2, y2

x1_nom, y1_nom, x2_nom, y2_nom = get_xy(state_nom)
x1_cao, y1_cao, x2_cao, y2_cao = get_xy(state_cao)

# ==========================================
# 4. ANIMACIÓN DUAL
# ==========================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
fig.suptitle('Práctica 4: Péndulo Doble Planar', fontsize=14)

# Configuración de límites y formato
for ax, title in zip([ax1, ax2], ['Amortiguado (c=0.15) - Figura 4', 'Caótico (c=0) - Sección 8']):
    ax.set_xlim(-2.2, 2.2)
    ax.set_ylim(-2.2, 2.2)
    ax.set_aspect('equal')
    ax.set_title(title)
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.plot(0, 0, 'k^', markersize=10, label='Pivote')

# Elementos gráficos de la Simulación 1 (Nominal)
line1_nom, = ax1.plot([], [], 'o-', lw=3, color='navy', markersize=8)
line2_nom, = ax1.plot([], [], 'o-', lw=3, color='navy', markersize=8)
trace_nom, = ax1.plot([], [], 'g-', lw=1.5, alpha=0.6, label='Trayectoria m2')

# Elementos gráficos de la Simulación 2 (Caótico)
line1_cao, = ax2.plot([], [], 'o-', lw=3, color='darkred', markersize=8)
line2_cao, = ax2.plot([], [], 'o-', lw=3, color='darkred', markersize=8)
trace_cao, = ax2.plot([], [], 'orange', lw=1.5, alpha=0.6, label='Trayectoria m2')

ax1.legend(loc="upper right")
ax2.legend(loc="upper right")

# Historial para las estelas de movimiento
hist_x2_nom, hist_y2_nom = [], []
hist_x2_cao, hist_y2_cao = [], []

def animate(i):
    # Actualizar Nominal
    line1_nom.set_data([0, x1_nom[i]], [0, y1_nom[i]])
    line2_nom.set_data([x1_nom[i], x2_nom[i]], [y1_nom[i], y2_nom[i]])
    hist_x2_nom.append(x2_nom[i])
    hist_y2_nom.append(y2_nom[i])
    trace_nom.set_data(hist_x2_nom[-120:], hist_y2_nom[-120:]) # Estela corta
    
    # Actualizar Caótico
    line1_cao.set_data([0, x1_cao[i]], [0, y1_cao[i]])
    line2_cao.set_data([x1_cao[i], x2_cao[i]], [y1_cao[i], y2_cao[i]])
    hist_x2_cao.append(x2_cao[i])
    hist_y2_cao.append(y2_cao[i])
    trace_cao.set_data(hist_x2_cao[-120:], hist_y2_cao[-120:]) 
    
    return line1_nom, line2_nom, trace_nom, line1_cao, line2_cao, trace_cao

ani = animation.FuncAnimation(fig, animate, frames=len(t), blit=True, interval=30)
plt.tight_layout()
plt.show()

# Ocultar advertencias de Matplotlib durante la generación de GIFs
warnings.filterwarnings("ignore")

# ==========================================
# 1. PARÁMETROS GLOBALES (Práctica 4)
# ==========================================
m1, m2 = 1.0, 0.8
l1, l2 = 1.0, 0.8
g = 9.81
k_resorte = 3.0

A_inercia = (m1 + m2) * l1**2
B_inercia = m2 * l1 * l2
C_inercia = m2 * l2**2

def u_fuerza(t):
    return 0.30 * np.cos(1.2 * t)

# ==========================================
# 2. MODELOS MATEMÁTICOS
# ==========================================
def derivadas_nolineal(state, t, c_damp, excitacion):
    th1, th2, w1, w2 = state
    delta = th1 - th2
    
    M11, M12 = A_inercia, B_inercia * np.cos(delta)
    M21, M22 = M12, C_inercia
    
    u_t = u_fuerza(t) if excitacion else 0.0
    
    F1 = l1 * u_t * np.cos(th1) \
         - B_inercia * np.sin(delta) * w2**2 \
         - (m1 + m2) * g * l1 * np.sin(th1) \
         - k_resorte * (l1**2) * np.sin(th1) * np.cos(th1) \
         - c_damp * (l1**2) * (np.cos(th1)**2) * w1
         
    F2 = B_inercia * np.sin(delta) * w1**2 - m2 * g * l2 * np.sin(th2)
    
    det = M11 * M22 - M12 * M21
    dw1 = (F1 * M22 - F2 * M12) / det
    dw2 = (M11 * F2 - M21 * F1) / det
    
    return [w1, w2, dw1, dw2]

def derivadas_lineal(state, t, c_damp, excitacion):
    # Aproximación de pequeños ángulos: sin(th) = th, cos(th) = 1, w^2 = 0
    th1, th2, w1, w2 = state
    M11, M12 = A_inercia, B_inercia
    M21, M22 = B_inercia, C_inercia
    
    u_t = u_fuerza(t) if excitacion else 0.0
    
    F1 = l1 * u_t - (m1 + m2) * g * l1 * th1 - k_resorte * (l1**2) * th1 - c_damp * (l1**2) * w1
    F2 = - m2 * g * l2 * th2
    
    det = M11 * M22 - M12 * M21
    dw1 = (F1 * M22 - F2 * M12) / det
    dw2 = (M11 * F2 - M21 * F1) / det
    
    return [w1, w2, dw1, dw2]

# Transformación cinemática
def get_xy(state):
    x1 = l1 * np.sin(state[:, 0])
    y1 = -l1 * np.cos(state[:, 0])
    x2 = x1 + l2 * np.sin(state[:, 1])
    y2 = y1 - l2 * np.cos(state[:, 1])
    return x1, y1, x2, y2

# ==========================================
# 3. GENERADORES DE ANIMACIONES (GIFs)
# ==========================================

def generar_gif_lineal_vs_nolineal():
    print("Generando lineal_vs_nolineal.gif...")
    t = np.linspace(0, 15, 450)
    # Condición inicial grande (0.8 rad) para forzar la divergencia entre modelos
    state0 = [0.8, 0.0, 0.0, 0.0] 
    
    st_nl = odeint(derivadas_nolineal, state0, t, args=(0.15, True))
    st_l = odeint(derivadas_lineal, state0, t, args=(0.15, True))
    
    x1_nl, y1_nl, x2_nl, y2_nl = get_xy(st_nl)
    x1_l, y1_l, x2_l, y2_l = get_xy(st_l)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xlim(-2, 2); ax.set_ylim(-2.2, 0.5)
    ax.set_title("Divergencia: Modelo No Lineal vs Linealizado")
    ax.grid(True, linestyle='--')
    
    line_nl, = ax.plot([], [], 'o-', lw=3, color='#102C57', label='Real (No Lineal)')
    line_l, = ax.plot([], [], 'o--', lw=2, color='red', alpha=0.6, label='Aproximación Lineal')
    ax.legend()
    
    def animate(i):
        line_nl.set_data([0, x1_nl[i], x2_nl[i]], [0, y1_nl[i], y2_nl[i]])
        line_l.set_data([0, x1_l[i], x2_l[i]], [0, y1_l[i], y2_l[i]])
        return line_nl, line_l
    
    ani = animation.FuncAnimation(fig, animate, frames=len(t), blit=True)
    ani.save('lineal_vs_nolineal.gif', writer='pillow', fps=30)
    plt.close(fig)

def generar_gif_energia():
    print("Generando dinamica_energia.gif...")
    t = np.linspace(0, 20, 600)
    state0 = [1.0, 0.0, 0.0, 0.0]
    st = odeint(derivadas_nolineal, state0, t, args=(0.15, False)) # Sin excitación para ver disipación
    
    x1, y1, x2, y2 = get_xy(st)
    th1, th2, w1, w2 = st[:,0], st[:,1], st[:,2], st[:,3]
    
    # Cálculo de energías
    T = 0.5 * A_inercia * w1**2 + 0.5 * C_inercia * w2**2 + B_inercia * np.cos(th1 - th2) * w1 * w2
    # Energía potencial desplazada (V=0 en reposo)
    V0 = -(m1 + m2)*g*l1 - m2*g*l2
    V = -(m1 + m2)*g*l1*np.cos(th1) - m2*g*(l1*np.cos(th1) + l2*np.cos(th2)) + 0.5*k_resorte*l1**2 * np.sin(th1)**2 - V0
    E_total = T + V
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.set_xlim(-2, 2); ax1.set_ylim(-2.2, 0.5); ax1.grid(True, linestyle='--')
    ax1.set_title("Movimiento Amortiguado")
    
    ax2.set_ylim(0, max(E_total)*1.1)
    ax2.set_title("Balance de Energía (Joules)")
    
    line, = ax1.plot([], [], 'o-', lw=3, color='navy')
    barras = ax2.bar(['Cinética (T)', 'Potencial (V)', 'Total (E)'], [0, 0, 0], color=['blue', 'green', 'purple'])
    
    def animate(i):
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
        barras[0].set_height(T[i])
        barras[1].set_height(max(0, V[i])) # Evitar bugs gráficos con V ligeramente negativo
        barras[2].set_height(E_total[i])
        return line, barras[0], barras[1], barras[2]
    
    ani = animation.FuncAnimation(fig, animate, frames=len(t), blit=False)
    ani.save('dinamica_energia.gif', writer='pillow', fps=30)
    plt.close(fig)

def generar_gif_caos_fase():
    print("Generando caos_plano_fase.gif...")
    t = np.linspace(0, 30, 900)
    state0 = [0.0, 0.0, 0.0, 0.0]
    st = odeint(derivadas_nolineal, state0, t, args=(0.0, True)) # c=0, con excitación
    
    x1, y1, x2, y2 = get_xy(st)
    th1, w1 = st[:,0], st[:,2]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    ax1.set_xlim(-2.2, 2.2); ax1.set_ylim(-2.2, 2.2); ax1.grid(True, linestyle='--')
    ax1.set_title("Péndulo Caótico (c=0)")
    
    ax2.set_xlim(min(th1)-0.5, max(th1)+0.5)
    ax2.set_ylim(min(w1)-1, max(w1)+1)
    ax2.set_title("Plano de Fase: $\\theta_1$ vs $\\dot{\\theta}_1$")
    ax2.set_xlabel("Posición Angular (rad)")
    ax2.set_ylabel("Velocidad Angular (rad/s)")
    ax2.grid(True, linestyle='--')
    
    line, = ax1.plot([], [], 'o-', lw=3, color='darkred')
    fase_line, = ax2.plot([], [], '-', lw=1, color='darkblue', alpha=0.7)
    fase_punto, = ax2.plot([], [], 'ro', markersize=6)
    
    def animate(i):
        line.set_data([0, x1[i], x2[i]], [0, y1[i], y2[i]])
        fase_line.set_data(th1[:i], w1[:i])
        fase_punto.set_data([th1[i]], [w1[i]])
        return line, fase_line, fase_punto
    
    ani = animation.FuncAnimation(fig, animate, frames=len(t), blit=True)
    ani.save('caos_plano_fase.gif', writer='pillow', fps=30)
    plt.close(fig)

if __name__ == "__main__":
    print("Iniciando renderizado. Esto tomará unos 1 a 2 minutos...")
    generar_gif_lineal_vs_nolineal()
    generar_gif_energia()
    generar_gif_caos_fase()
    print("¡Todos los GIFs se han generado exitosamente en tu carpeta actual!")