import numpy as np
import matplotlib.pyplot as plt

# --- Безразмерные переменные ---
q = np.linspace(-1.6, 1.6, 1600)
V = (1.0 - q**2)**2                      # потенциал в единицах ΔE

tau = np.linspace(-6.0, 6.0, 800)        # евклидово время в единицах τ0
q_inst = np.tanh(tau)                    # инстантонная траектория

plt.style.use('default')
fig, ax = plt.subplots(figsize=(7.2, 6.0))

# --- Основная панель: потенциал двойной ямы ---
ax.plot(q, V, color='black', linewidth=2.0, zorder=5)
ax.axhline(1.0, color='gray', linestyle='--', linewidth=1.3, alpha=0.9)

# Вертикальные направляющие в характерных точках
for qc in (-1.0, 0.0, 1.0):
    ax.axvline(qc, color='gray', linestyle=':', linewidth=0.9, alpha=0.5)

# Маркеры минимумов (ветви) и максимума (остановленный поток)
ax.plot([-1.0, 1.0], [0.0, 0.0], 'o', color='#d73027', markersize=8, zorder=6)
ax.plot([0.0], [1.0], 's', color='#4575b4', markersize=8, zorder=6)

# Аннотации характерных точек
ax.annotate('аккреция (ЧД)', xy=(-1.0, 0.0), xytext=(-1.55, 0.55),
            fontsize=12, color='#d73027',
            arrowprops=dict(arrowstyle='->', color='#d73027', lw=1.2))
ax.annotate('ветер (БД)', xy=(1.0, 0.0), xytext=(0.72, 0.55),
            fontsize=12, color='#d73027',
            arrowprops=dict(arrowstyle='->', color='#d73027', lw=1.2))
ax.annotate('остановленный поток', xy=(0.0, 1.0), xytext=(0.15, 1.30),
            fontsize=12, color='#4575b4',
            arrowprops=dict(arrowstyle='->', color='#4575b4', lw=1.2))
ax.text(1.60, 1.03, r'$\Delta E$', fontsize=13, color='gray', va='bottom')

ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-0.12, 2.6)
ax.set_xlabel(r'коллективная координата $q$', fontsize=13)
ax.set_ylabel(r'$V(q)\,/\,\Delta E$', fontsize=13)
ax.grid(True, linestyle=':', alpha=0.4)
ax.tick_params(labelsize=11)

# --- Вставка: инстантонная траектория (размещена в свободной верхней зоне) ---
axins = ax.inset_axes([0.30, 0.62, 0.40, 0.33])   # [x0, y0, width, height] в координатах осей
axins.plot(tau, q_inst, color='#d73027', linewidth=1.8)
axins.axhline(1.0, color='gray', linestyle='--', linewidth=0.9, alpha=0.8)
axins.axhline(-1.0, color='gray', linestyle='--', linewidth=0.9, alpha=0.8)
axins.axhline(0.0, color='gray', linestyle=':', linewidth=0.7, alpha=0.5)
axins.plot([0.0], [0.0], 's', color='#4575b4', markersize=5, zorder=6)
axins.set_xlim(-6.0, 6.0)
axins.set_ylim(-1.15, 1.15)
axins.set_xlabel(r'$\tau/\tau_0$', fontsize=10)
axins.set_ylabel(r'$q(\tau)$', fontsize=10)
axins.set_title(r'$q(\tau) = \tanh(\tau/\tau_0)$', fontsize=10)
axins.set_xticks([-4, 0, 4])
axins.set_yticks([-1, 0, 1])
axins.tick_params(labelsize=8)
axins.grid(True, linestyle=':', alpha=0.4)

plt.tight_layout()
plt.savefig('fig_double_well_potential.pdf', dpi=300, bbox_inches='tight')
plt.savefig('fig_double_well_potential.png', dpi=300, bbox_inches='tight')
plt.show()