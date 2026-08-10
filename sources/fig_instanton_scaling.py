import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from matplotlib.lines import Line2D

# --- 1. Данные и параметры ---
a_inf = np.linspace(0.05, 0.20, 100)
gammas = [5.0 / 3.0, 4.0 / 3.0]
gamma_labels = [r'$\gamma = 5/3$', r'$\gamma = 4/3$']
colors = ['#d73027', '#4575b4']  # красный и синий

# Таблица 1 статьи (инстантонная работа): калибровочные точки
a_tab = np.array([0.05, 0.10])
tab = {
    5.0 / 3.0: dict(I=np.array([380.0, 120.0]),  dE=np.array([3.1, 2.1]),
                    S=np.array([65.0, 30.0]),     tau0=np.array([7.8, 5.3])),
    4.0 / 3.0: dict(I=np.array([4700.0, 850.0]), dE=np.array([21.0, 7.8]),
                    S=np.array([590.0, 154.0]),   tau0=np.array([10.6, 7.4])),
}

# Таблица 4 (Acoustic Geometry paper): kappa(a_inf) для tau_QNM
a_k = np.array([0.05, 0.10, 0.15, 0.20])
kappa_data = {
    5.0 / 3.0: np.array([4.10e-3, 1.38e-2, 2.69e-2, 4.19e-2]),
    4.0 / 3.0: np.array([4.82e-4, 3.51e-3, 1.03e-2, 2.06e-2]),
}
kappa_funcs = {g: interp1d(a_k, k, kind='cubic') for g, k in kappa_data.items()}


# --- 2. Модельные функции ---
def _exponent(a_ref, y_ref):
    """Показатель степенной зависимости через две калибровочные точки."""
    return np.log(y_ref[0] / y_ref[1]) / np.log(a_ref[1] / a_ref[0])


def get_I_dE(gamma, a):
    """I(a) и DeltaE(a) --- степенные интерполяции, калиброванные по Таблице 1."""
    d = tab[gamma]
    p_I = _exponent(a_tab, d['I'])
    p_E = _exponent(a_tab, d['dE'])
    I = d['I'][1] * (a / 0.1) ** (-p_I)
    dE = d['dE'][1] * (a / 0.1) ** (-p_E)
    return I, dE


def get_S_tau0(gamma, a):
    """Точные соотношения однопараметрической модели:
    S = (4/3) sqrt(2 I DeltaE), tau_0 = sqrt(I / (2 DeltaE))."""
    I, dE = get_I_dE(gamma, a)
    S = (4.0 / 3.0) * np.sqrt(2.0 * I * dE)
    tau0 = np.sqrt(I / (2.0 * dE))
    return S, tau0


# --- 3. Построение графика ---
plt.style.use('default')
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

solid_lines, dash_lines = [], []

for i, gamma in enumerate(gammas):
    color = colors[i]
    label = gamma_labels[i]

    kappa = kappa_funcs[gamma](a_inf)
    tau_qnm = 1.0 / kappa
    S, tau0 = get_S_tau0(gamma, a_inf)
    S_scale = S[np.argmin(abs(a_inf - 0.1))] * (0.1 / a_inf) ** 2

    # --- Левая панель: действие ---
    l1, = ax1.plot(a_inf, S, color=color, linewidth=2.5, label=label)
    l2, = ax1.plot(a_inf, S_scale, color=color, linewidth=1.5,
                   linestyle='--', alpha=0.6)
    ax1.plot(a_tab, tab[gamma]['S'], 'o', color=color,
             markeredgecolor='k', markerfacecolor=color, markersize=7)
    solid_lines.append(l1)
    dash_lines.append(l2)

    # --- Правая панель: времена ---
    ax2.plot(a_inf, tau0, color=color, linewidth=2.5, label=label)
    ax2.plot(a_inf, tau_qnm, color='gray', linewidth=1.5,
             linestyle=':', alpha=0.8)
    ax2.plot(a_tab, tab[gamma]['tau0'], 'o', color=color,
             markeredgecolor='k', markerfacecolor=color, markersize=7)

# --- Оформление левой панели (S) ---
ax1.set_yscale('log')
ax1.set_xlabel(r'Асимптотическая скорость звука $a_\infty$', fontsize=13)
ax1.set_ylabel(r'Инстантонное действие $\mathcal{S}_{\mathrm{inst}}$', fontsize=13)
ax1.set_title(r'Зависимость действия от $a_\infty$', fontsize=14)
ax1.grid(True, which='both', ls=':', alpha=0.5)

# Первая легенда --- цвета (gamma); закрепляем и добавляем вторую (стили линий)
leg1 = ax1.legend(fontsize=12, loc='upper right')
ax1.add_artist(leg1)
style_elements = [
    Line2D([0], [0], color='k', linewidth=2, label='Расчёт по Таблице 1'),
    Line2D([0], [0], color='k', linewidth=1.5, linestyle='--',
           label=r'Скейлинг $\propto a_\infty^{-2}$'),
    Line2D([0], [0], color='k', marker='o', linestyle='none',
           label='Табличные значения'),
]
ax1.legend(handles=style_elements, loc='lower left', fontsize=10, framealpha=0.9)

# --- Оформление правой панели (tau) ---
ax2.set_yscale('log')
ax2.set_xlabel(r'Асимптотическая скорость звука $a_\infty$', fontsize=13)
ax2.set_ylabel(r'Характерное время (ед. $r_{\mathrm{g}}/c$)', fontsize=13)
ax2.set_title(r'Временные масштабы: $\tau_0$ и $\tau_{\mathrm{QNM}}$', fontsize=14)
ax2.grid(True, which='both', ls=':', alpha=0.5)

legend_elements_2 = [
    Line2D([0], [0], color='#d73027', linewidth=2.5, label=r'$\gamma=5/3$ ($\tau_0$)'),
    Line2D([0], [0], color='#4575b4', linewidth=2.5, label=r'$\gamma=4/3$ ($\tau_0$)'),
    Line2D([0], [0], color='gray', linewidth=1.5, linestyle=':',
           label=r'$\tau_{\mathrm{QNM}} = \kappa^{-1}$'),
    Line2D([0], [0], color='k', marker='o', linestyle='none',
           label='Табличные значения'),
]
ax2.legend(handles=legend_elements_2, loc='upper right', fontsize=10, framealpha=0.9)

plt.tight_layout()

# Сохранение
plt.savefig('fig_instanton_scaling.pdf', dpi=300, bbox_inches='tight')
plt.savefig('fig_instanton_scaling.png', dpi=300, bbox_inches='tight')
plt.show()