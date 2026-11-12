import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Parámetros del sistema
m = 0.05      # kg
g = 9.81      # m/s^2
k = 1e-4      # N*m^2/A^2
R = 10.0      # Ohms
L = 0.1       # Henrys
u_e = 7.0036  # Voltios constantes (lazo abierto)

# Sistema de Ecuaciones Diferenciales
def maglev_dynamics(t, x):
    x1, x2, x3 = x
    # Evitar división por cero o posiciones negativas
    x1 = max(x1, 1e-5) 
    
    dx1_dt = x2
    dx2_dt = g - (k / m) * (x3 / x1)**2
    dx3_dt = -(R / L) * x3 + (1 / L) * u_e
    return [dx1_dt, dx2_dt, dx3_dt]

# Tiempo de simulación
t_span = (0, 0.5)
t_eval = np.linspace(0, 0.5, 1000)

# Simulación con diferentes condiciones iniciales cerca del equilibrio
condiciones_iniciales = [
    [0.010, 0.0, 0.7004],  # En equilibrio
    [0.009, 0.0, 0.7004],  # Ligero desplazamiento hacia arriba
    [0.011, 0.0, 0.7004]   # Ligero desplazamiento hacia abajo
]

plt.figure(figsize=(10, 4))
for x0 in condiciones_iniciales:
    sol = solve_ivp(maglev_dynamics, t_span, x0, t_eval=t_eval)
    plt.plot(sol.y[0] * 100, sol.y[1], label=f'x1(0) = {x0[0]*100:.1f} cm')

plt.title('Plano de Fase: Velocidad vs Posición (Lazo Abierto)')
plt.xlabel('Posición x1 (cm)')
plt.ylabel('Velocidad x2 (m/s)')
plt.axvline(x=1.0, color='r', linestyle='--', label='Punto de Equilibrio (1 cm)')
plt.grid(True)
plt.legend()
plt.show()