try:
    import ipywidgets as widgets
except ImportError:
    import piplite
    await piplite.install('ipywidgets')
    import ipywidgets as widgets

import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display

# 2. THE SIMULATION ENGINE
def aircraft_simulation(mass, S, CL_max, CD0, k, power_hp, eta, mu, altitude):
    g = 9.81
    rho0 = 1.225
    W = mass * g
    
    # Environment (Density decreases with altitude)
    rho = rho0 * np.exp(-altitude / 8500)
    
    # Speed range (m/s)
    V = np.arange(20, 101, 1)
    
    # Aerodynamics
    CL = (2 * W) / (rho * V**2 * S)
    CD = CD0 + k * (CL**2)
    Drag = 0.5 * rho * (V**2) * S * CD
    
    # Propulsion
    power_watt = power_hp * 745.7
    Thrust = (eta * power_watt) / V
    
    # Performance Calculations
    V_stall = np.sqrt((2 * W) / (rho * S * CL_max))
    V_TO = 1.2 * V_stall
    
    # Takeoff Distance Estimate
    V_avg = V_TO * 0.707
    Drag_avg = 0.5 * rho * (V_avg**2) * S * CD0
    Thrust_avg = (eta * power_watt) / V_avg
    F_net = Thrust_avg - Drag_avg - (mu * W)
    a_TO = F_net / mass
    S_TO = (V_TO**2) / (2 * a_TO)

    # OUTPUT PLOTS
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Force Graph
    ax1.plot(V, Drag, label="Total Drag", color='blue', lw=2)
    ax1.plot(V, Thrust, label="Thrust Available", color='red', lw=2)
    ax1.axvline(V_stall, color='black', ls='--', label=f"Stall ({V_stall:.1f} m/s)")
    ax1.set_xlabel("Velocity (m/s)")
    ax1.set_ylabel("Force (N)")
    ax1.set_title("Flight Envelope")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Text Results
    ax2.axis('off')
    ax2.text(0.1, 0.4, 
             f"Density: {rho:.3f} kg/m³\n"
             f"Stall Speed: {V_stall:.2f} m/s\n"
             f"Takeoff Speed: {V_TO:.2f} m/s\n\n"
             f"TAKEOFF DISTANCE: {S_TO:.2f} m", 
             fontsize=14, family='monospace', bbox={'facecolor':'#f0f0f0', 'pad':10})
    
    plt.show()

# 3. GUI INTERFACE
style = {'description_width': 'initial'}
ui = widgets.interactive(
    aircraft_simulation,
    mass=(500, 2500, 50),
    S=(10, 30, 1),
    CL_max=(1.0, 2.0, 0.1),
    CD0=(0.01, 0.05, 0.005),
    k=(0.02, 0.08, 0.005),
    power_hp=(80, 400, 10),
    eta=(0.5, 0.9, 0.05),
    mu=(0.02, 0.1, 0.01),
    altitude=(0, 5000, 500)
)
display(ui)
