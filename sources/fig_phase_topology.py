import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import root_scalar

# --- Параметры потока ---
a_inf = 0.1
gammas = [5.0 / 3.0, 4.0 / 3.0]
gamma_labels = [r'$\gamma = 5/3$', r'$\gamma = 4/3$']
r_max_list = [18.0, 42.0]  # масштаб по r для каждой панели


def compute_michel(gamma, a_inf):
    """Вычисление критической точки и параметров потока Мишеля."""
    h_inf = (gamma - 1) / (gamma - 1 - a_inf**2)

    def critical_eq(r):
        f_c = 1 - 1 / r
        v_c2 = 1 / (4 * r)
        a_c2 = 1 / (4 * r - 3)
        h_c = (gamma - 1) / (gamma - 1 - a_c2)
        return h_c**2 * (f_c + v_c2) - h_inf**2

    res = root_scalar(critical_eq, bracket=[1.5, 100], method='brentq')
    r_c = res.root
    v_c = np.sqrt(1 / (4 * r_c))
    f_c = 1 - 1 / r_c
    h_c = h_inf / np.sqrt(f_c + v_c**2)
    n_c = (h_c - 1)**(1 / (gamma - 1))
    J_c = r_c**2 * n_c * v_c

    return h_inf, r_c, v_c, J_c


def compute_fields(gamma, a_inf, h_inf, r_min, r_max, v_max, n_points):
    """Вычисление полей потока на сетке."""
    r = np.linspace(r_min, r_max, n_points)
    v = np.linspace(-v_max, v_max, n_points)
    R, V = np.meshgrid(r, v)

    f = 1 - 1 / R
    # Условие физичности: a^2 >= 0  =>  f + V^2 <= h_inf^2
    valid = (f + V**2) <= h_inf**2

    h = np.full_like(R, np.nan)
    h[valid] = h_inf / np.sqrt(f[valid] + V[valid]**2)

    n = np.full_like(R, np.nan)
    n[valid] = (h[valid] - 1)**(1 / (gamma - 1))

    # Поток барионов J (интеграл Мишеля)
    J = np.full_like(R, np.nan)
    J[valid] = R[valid]**2 * n[valid] * V[valid]

    # Физическое число Маха M (для построения звукового барьера)
    a2 = (gamma - 1) * (1 - 1 / h)
    a = np.sqrt(np.maximum(a2, 0))
    V_phys = np.abs(V) / np.sqrt(f + V**2)
    M = V_phys / a

    return R, V, J, M


def draw_contours(ax, R, V, J, M, J_c, lw_bg=1.0, lw_sep=2.5, lw_m1=1.5):
    """Отрисовка контуров потока и звукового барьера."""
    levels_factor = np.array([0.2, 0.4, 0.6, 0.8, 0.95, 1.05, 1.2, 1.5, 2.0])
    # Для аккреционной ветви (отрицательные значения) инвертируем порядок,
    # чтобы массив levels_acc был строго возрастающим
    levels_acc = -J_c * levels_factor[::-1]
    levels_wind = J_c * levels_factor

    # Субкритические и суперкритические ветви (фоновые линии уровня)
    ax.contour(R, V, J, levels=levels_acc, colors='salmon', linewidths=lw_bg, alpha=0.55)
    ax.contour(R, V, J, levels=levels_wind, colors='skyblue', linewidths=lw_bg, alpha=0.55)

    # Критические сепаратрисы (трансзвуковые решения)
    ax.contour(R, V, J, levels=[-J_c], colors='darkred', linewidths=lw_sep)
    ax.contour(R, V, J, levels=[J_c], colors='darkblue', linewidths=lw_sep)

    # Звуковой барьер (M = 1)
    M_plot = np.ma.masked_invalid(M)
    ax.contour(R, V, M_plot, levels=[1.0], colors='black', linestyles='dashed', linewidths=lw_m1, alpha=0.75)


def plot_panel(ax, gamma, a_inf, r_max, gamma_label, is_first=False):
    """Отрисовка одной панели фазового портрета."""
    h_inf, r_c, v_c, J_c = compute_michel(gamma, a_inf)
    R, V, J, M = compute_fields(gamma, a_inf, h_inf, 1.01, r_max, 0.95, 1200)

    # Основная область
    draw_contours(ax, R, V, J, M, J_c)

    # Критическая точка (седло)
    ax.plot(r_c, -v_c, 'ko', markersize=6, zorder=5)
    ax.plot(r_c, v_c, 'ko', markersize=6, zorder=5)

    # Вертикальная линия акустического горизонта
    ax.axvline(r_c, color='gray', linestyle=':', linewidth=1.2, alpha=0.7)

    # Аннотации основной области
    ax.text(r_c + 0.3, -0.88, r'$r_{\mathrm{a}} = r_{\mathrm{c}}$', fontsize=11, color='gray')
    ax.text(r_max * 0.5, -0.65, r'Аккреция ($\upsilon < 0$)', fontsize=13, color='darkred', alpha=0.9, weight='bold')
    ax.text(r_max * 0.5, 0.55, r'Ветер ($\upsilon > 0$)', fontsize=13, color='darkblue', alpha=0.9, weight='bold')
    ax.text(1.8, 0.87, r'Звуковой барьер $\mathcal{M}=1$', fontsize=11, color='black', alpha=0.8)

    ax.set_xlim(1.0, r_max)
    ax.set_ylim(-0.9, 0.9)
    ax.set_xlabel(r'Радиус $r$ (в единицах $r_{\mathrm{g}}$)', fontsize=13)
    ax.set_title(gamma_label + r', $a_\infty = 0.1$', fontsize=14, pad=10)
    ax.grid(True, linestyle=':', alpha=0.4)
    ax.tick_params(labelsize=11)

    if is_first:
        ax.set_ylabel(r'Радиальная 3-скорость $\upsilon$', fontsize=13)

    return r_c, v_c


# --- Построение двухпанельного рисунка ---
plt.style.use('default')
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

for i, (gamma, gamma_label) in enumerate(zip(gammas, gamma_labels)):
    plot_panel(axes[i], gamma, a_inf, r_max_list[i], gamma_label, is_first=(i == 0))

plt.tight_layout()
plt.savefig('fig_phase_topology.pdf', dpi=300, bbox_inches='tight')
plt.savefig('fig_phase_topology.png', dpi=300, bbox_inches='tight')
plt.show()