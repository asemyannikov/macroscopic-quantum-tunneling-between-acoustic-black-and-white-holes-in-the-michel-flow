import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

# Совместимость с NumPy >= 2.0 (trapz -> trapezoid)
_trapezoid = getattr(np, "trapezoid", np.trapz)

# --- Параметры потока ---
a_inf = 0.1
gammas = [5.0 / 3.0, 4.0 / 3.0]
gamma_labels = [r'$\gamma = 5/3$', r'$\gamma = 4/3$']

# Радиус Бонди (внешний обрезатель)
r_B = 200.0


def find_rc(gamma, a_inf):
    """Поиск критической точки (акустического горизонта) r_c."""
    h_inf = (gamma - 1) / (gamma - 1 - a_inf**2)

    def critical_eq(r):
        f_c = 1 - 1 / r
        v_c2 = 1 / (4 * r)
        a_c2 = 1 / (4 * r - 3)
        h_c = (gamma - 1) / (gamma - 1 - a_c2)
        return h_c**2 * (f_c + v_c2) - h_inf**2

    res = root_scalar(critical_eq, bracket=[1.5, 1000], method='brentq')
    return res.root


def compute_integrand(gamma, a_inf, r_c, n_points=5000):
    """Вычисление подынтегральной функции 4*pi*r^2*rho*v^2.
    
    С учётом сохранения барионов и интеграла Бернулли,
    подынтегральное выражение пропорционально h(r) * |v(r)|.
    """
    h_inf = (gamma - 1) / (gamma - 1 - a_inf**2)

    f_c = 1 - 1 / r_c
    v_c2 = 1 / (4 * r_c)
    a_c2 = v_c2 / (1 - 3 * v_c2)
    h_c = (gamma - 1) / (gamma - 1 - a_c2)
    v_c = np.sqrt(v_c2)

    n_c_scaled = (h_c - 1)**(1 / (gamma - 1))
    J_scaled = r_c**2 * n_c_scaled * v_c

    r = np.linspace(r_c, r_B, n_points)
    f = 1 - 1 / r
    
    h_arr = np.zeros_like(r)
    v_arr = np.zeros_like(r)

    for i, ri in enumerate(r):
        fi = f[i]
        
        # Физически допустимый диапазон для энтальпии: h \in [h_inf, h_inf / sqrt(f)]
        # Добавляем малые отступы, чтобы избежать граничных сингулярностей v=0
        h_low = h_inf + 1e-12
        h_high = h_inf / np.sqrt(fi) - 1e-12
        
        if h_low >= h_high:
            h_sol = h_inf
        else:
            def eq_h(h):
                v2 = h_inf**2 / h**2 - fi
                if v2 < 0:
                    return -J_scaled
                v_val = np.sqrt(v2)
                n_val = (h - 1)**(1 / (gamma - 1))
                return ri**2 * n_val * v_val - J_scaled

            try:
                res = root_scalar(eq_h, bracket=[h_low, h_high], method='brentq', xtol=1e-14)
                h_sol = res.root
            except ValueError:
                h_sol = h_c if np.isclose(ri, r_c) else h_inf
                
        v2 = max(0, h_inf**2 / h_sol**2 - fi)
        v_val = np.sqrt(v2)

        h_arr[i] = h_sol
        v_arr[i] = v_val

    # Подынтегральная функция (пропорциональна h * |v|)
    integrand = h_arr * v_arr

    return r, integrand


def plot_panel(ax, gamma, a_inf, r_c):
    """Отрисовка одной панели."""
    r, integrand = compute_integrand(gamma, a_inf, r_c)

    # Нормировка на максимум
    integrand_norm = integrand / np.max(integrand)

    # Границы зон
    r_zone1_end = 2 * r_c
    r_zone2_end = r_B / 2

    # Основная кривая
    ax.plot(r, integrand_norm, color='black', linewidth=2, zorder=5)

    # Закрашенные области
    mask1 = (r >= r_c) & (r <= r_zone1_end)
    ax.fill_between(r[mask1], integrand_norm[mask1],
                    color='#d73027', alpha=0.4, interpolate=True)

    mask2 = (r > r_zone1_end) & (r <= r_zone2_end)
    ax.fill_between(r[mask2], integrand_norm[mask2],
                    color='#fc8d59', alpha=0.4, interpolate=True)

    mask3 = r > r_zone2_end
    ax.fill_between(r[mask3], integrand_norm[mask3],
                    color='#91bfdb', alpha=0.4, interpolate=True)

    # Вычисление долей вклада (используем метод трапеций для точности)
    I_total = _trapezoid(integrand_norm, r)
    I1 = _trapezoid(integrand_norm[mask1], r[mask1])
    I2 = _trapezoid(integrand_norm[mask2], r[mask2])
    I3 = _trapezoid(integrand_norm[mask3], r[mask3])

    frac1 = I1 / I_total * 100
    frac2 = I2 / I_total * 100
    frac3 = I3 / I_total * 100

    # Вертикальная линия r_c
    ax.axvline(r_c, color='gray', linestyle=':', linewidth=1.5, alpha=0.8,
               label=r'$r_{\mathrm{c}} = ' + f'{r_c:.2f}$')

    # Аннотации долей (размещаем вверху, так как кривая быстро спадает)
    ax.text(r_c + (r_zone1_end - r_c) / 2, 0.95,
            f'{frac1:.0f}%', fontsize=11, ha='center', color='#d73027',
            weight='bold')
    ax.text(r_zone1_end + (r_zone2_end - r_zone1_end) / 2, 0.95,
            f'{frac2:.0f}%', fontsize=11, ha='center', color='#fc8d59',
            weight='bold')
    ax.text(r_zone2_end + (r_B - r_zone2_end) / 2, 0.95,
            f'{frac3:.0f}%', fontsize=11, ha='center', color='#91bfdb',
            weight='bold')

    # Оформление
    ax.set_xlim(r_c, r_B)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(r'Радиус $r$ (в единицах $r_{\mathrm{g}}$)', fontsize=13)
    ax.set_ylabel(r'Нормированная подынтегральная функция', fontsize=13)
    ax.legend(loc='upper right', fontsize=11)
    ax.grid(True, linestyle=':', alpha=0.3)


# --- Построение двухпанельного рисунка ---
plt.style.use('default')
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

for i, (gamma, gamma_label) in enumerate(zip(gammas, gamma_labels)):
    r_c = find_rc(gamma, a_inf)
    plot_panel(axes[i], gamma, a_inf, r_c)
    axes[i].set_title(gamma_label + r', $a_\infty = 0.1$', fontsize=14, pad=10)

plt.tight_layout()
plt.savefig('fig_inertia_localization.pdf', dpi=300, bbox_inches='tight')
plt.savefig('fig_inertia_localization.png', dpi=300, bbox_inches='tight')
plt.show()