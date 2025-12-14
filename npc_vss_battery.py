# ============================================================
# NPC vs Battery Capacity
# PEMFC Cogeneration System
# ============================================================

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# SYSTEM PARAMETERS
# -----------------------------
FC_NOMINAL_POWER = 5.0          # kW
FC_LIFETIME_H = 20000           # hours
MAINTENANCE_INTERVAL = 2000     # hours
OPERATING_HOURS_YEAR = 2640

# -----------------------------
# ECONOMIC PARAMETERS
# -----------------------------
FC_SYSTEM_COST = 450            # $/kW
FC_REPLACEMENT_COST = 400       # $/kW
FC_OM_COST = 0.15               # $/h
BATTERY_COST = 270              # $/kWh
H2_TANK_COST = 85               # $/kg
H2_FUEL_COST = 8                # $/kg

DISCOUNT_RATE = 0.05
PROJECT_LIFE = 20               # years

# -----------------------------
# FIXED PARAMETERS
# -----------------------------
H2_TANK_FIXED = 20.0            # kg
H2_CONS_KG_H = 0.24             # kg/h (PAC ~4 kW)

# -----------------------------
# BATTERY RANGE
# -----------------------------
battery_sizes = np.linspace(2, 50, 30)  # kWh
npc = []

# Present Worth Factor
PWF = ((1 + DISCOUNT_RATE)**PROJECT_LIFE - 1) / \
      (DISCOUNT_RATE * (1 + DISCOUNT_RATE)**PROJECT_LIFE)

for batt in battery_sizes:

    # CAPEX
    capex = (
        FC_NOMINAL_POWER * FC_SYSTEM_COST
        + batt * BATTERY_COST
        + H2_TANK_FIXED * H2_TANK_COST
    )

    # Stack replacement
    stack_life_years = FC_LIFETIME_H / OPERATING_HOURS_YEAR
    replacements = int(PROJECT_LIFE / stack_life_years)
    replacement_cost = replacements * FC_NOMINAL_POWER * FC_REPLACEMENT_COST

    # Maintenance
    maintenance_cycles = OPERATING_HOURS_YEAR / MAINTENANCE_INTERVAL
    maintenance_cost = maintenance_cycles * PROJECT_LIFE * FC_OM_COST * FC_NOMINAL_POWER

    # Fuel cost (NPV)
    fuel_cost_npv = (
        H2_CONS_KG_H * OPERATING_HOURS_YEAR * H2_FUEL_COST * PWF
    )

    npc.append(capex + replacement_cost + maintenance_cost + fuel_cost_npv)

# -----------------------------
# PLOT
# -----------------------------
plt.figure(figsize=(7, 5))
plt.plot(battery_sizes, npc, marker='o')
plt.xlabel("Capacité de la batterie (kWh)")
plt.ylabel("Coût Global Actualisé NPC ($)")
plt.title("Évolution du coût du système PEMFC \n en fonction de la capacité de batterie")
plt.grid(True)
plt.tight_layout()
plt.show()
