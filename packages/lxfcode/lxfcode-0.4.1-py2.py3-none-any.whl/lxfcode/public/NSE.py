"""Numerical solutions of Schrodinger equation"""

from public.consts import *
from scipy.special import yn, struve
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt


class KeldyshPotential:
    """
    Used to numerically solve the Schrodinger equation with Keldysh potential
    """

    def __init__(self, mu_m0, E_g, kappa, r_0) -> None:
        self.mu_m0 = mu_m0
        self.E_g = E_g
        self.kappa = kappa
        self.r_0 = r_0

        self.zB = self.kappa * BOHR_R / self.r_0
        self.u0 = pi * self.mu_m0 / (self.kappa * self.zB)

    def Fz(self, z):
        """
        Here, z is the dimensionless coordinate.
        """

        return struve(0, z) - yn(0, z)

    def h_matrix(self, zmax=180, N=1000):
        # Method 1
        h = zmax / N
        z_list = np.linspace(0, zmax, N + 1)
        f_list = [self.Fz(ele_z) for ele_z in z_list[1:N]]
        # f_list[0] = self.Fz(0.316 / self.r_0)

        diag_terms = 2 - np.array(f_list) * self.u0 * h**2

        mat = np.zeros((N - 1, N - 1))
        mat[np.diag_indices_from(mat)] = diag_terms
        for i in range(0, N - 2):
            mat[i][i + 1] = mat[i + 1][i] = -1

        # # Method 2
        # h = zmax / N
        # z_list = np.linspace(0, zmax, N + 1)
        # f_list = [self.Fz(ele_z) for ele_z in z_list[: N + 1]]
        # f_list[0] = self.Fz(0.319 / self.r_0)
        # # print("F_list: ", f_list)

        # diag_terms = 2 - np.array(f_list) * self.u0 * h**2

        # mat = np.zeros((N + 1, N + 1))
        # mat[np.diag_indices_from(mat)] = diag_terms
        # for i in range(0, N):
        #     mat[i][i + 1] = mat[i + 1][i] = -1

        return mat / h**2

    def get_eigen(self, z_max=180, N=1000):
        """
        Solve the Hamiltonian and get eigen energies and eigen vectors
        """
        eig_e, eig_v = np.linalg.eig(self.h_matrix(z_max, N))
        E_n = self.E_g + self.zB**2 / self.mu_m0 * eig_e * RYDBERG

        return E_n, eig_v


class ExcitonFit:
    def __init__(self, x, y, mu_m0) -> None:
        self.x = x
        self.energies = y
        self.mu_m0 = mu_m0

    def KeldyshFit(self, p0):
        """
        x: indexes of excitons
        y: Energy of excitons (eV)
        """

        def KeldyshExcitons(x, *args):
            E_g = args[0][0]
            r_0 = args[0][1]
            E_n = KeldyshPotential(self.mu_m0, E_g, 2.35, r_0).get_eigen()[0]
            E_n.sort()
            return E_n[np.arange(len(x))]

        popt = scipy.optimize.curve_fit(
            lambda x, *p0: KeldyshExcitons(x, p0),
            self.x,
            self.energies,
            p0=p0,
            maxfev=50000,
            bounds=((p0[0] - 0.2, 1), (p0[0] + 0.2, 4)),
        )[0]
        print(popt)
        return popt


def main():
    mu_m0A = 0.27  #   m_0
    mu_m0B = 0.28  #   m_0
    e_list = []
    x_AB = [1, 2, 3]
    kappa = 2.3
    for ele_i in range(5):
        energies = np.load(
            "/home/aoxv/code/Data/FitFiles/MoS2Data/"
            + "PermIFFixedFit_{}.npy".format(ele_i)
        )[0]
        e_list.append(energies / 1000)
    E_A = np.array(e_list)[:, [0, 2, 3]]
    E_B = np.array(e_list)[:, [1, 4, 5]]

    E_A_mean = np.mean(E_A, axis=0)
    E_B_mean = np.mean(E_B, axis=0)

    A_err = np.zeros((2, len(E_A_mean)))
    A_err[0, :] = E_A_mean - np.min(E_A, axis=0)
    A_err[1, :] = np.max(E_A, axis=0) - E_A_mean
    B_err = np.zeros((2, len(E_B_mean)))
    B_err[0, :] = E_B_mean - np.min(E_B, axis=0)
    B_err[1, :] = np.max(E_B, axis=0) - E_B_mean
    print(A_err, B_err)

    A_fit = ExcitonFit(x_AB, E_A_mean, mu_m0A)
    popt_A = A_fit.KeldyshFit([2.1, 3.12])
    EnA = KeldyshPotential(mu_m0A, popt_A[0], kappa, popt_A[1]).get_eigen()[0]
    EnA.sort()

    B_fit = ExcitonFit(x_AB, E_B_mean, mu_m0B)
    popt_B = B_fit.KeldyshFit([2.1, 3.12])
    EnB = KeldyshPotential(mu_m0B, popt_B[0], kappa, popt_B[1]).get_eigen()[0]
    EnB.sort()

    fig, ax = plt.subplots()
    ax.errorbar(
        np.arange(1, 4),
        E_A_mean,
        yerr=A_err,
        fmt="o",
        label=r"X$_{\mathrm{A}}$",
        capsize=4,
        ecolor="r",
        # ecolor="k",
        # mfc="orange"
        # elinewidth=0.5,
        # marker="s",
        # mfc="orange",
        # mec="k",
        # mew=1,
        # ms=10,
        # alpha=1,
        # capsize=5,
        # capthick=3,
        # linestyle="none",
        # label="A series",
    )
    ax.errorbar(
        np.arange(1, 4),
        E_B_mean,
        yerr=B_err,
        fmt="o",
        label=r"X$_{\mathrm{B}}$",
        capsize=4,
        ecolor="r",
        # ecolor="k",
        # mfc="blue"
        # elinewidth=0.5,
        # marker="s",
        # mfc="orange",
        # mec="k",
        # mew=1,
        # ms=10,
        # alpha=1,
        # capsize=5,
        # capthick=3,
        # linestyle="none",
        # label="B series",
    )

    ax.plot(np.arange(1, 7), EnA[:6], label=r"Keldysh X$_{\mathrm{A}}$")
    ax.plot(np.arange(1, 7), EnB[:6], label=r"Keldysh X$_{\mathrm{B}}$")
    ax.hlines(popt_A[0], 1, 6, linestyles="dashed", colors="blue")
    ax.hlines(popt_B[0], 1, 6, linestyles="dashed", colors="orange")
    ax.text(
        4.5, popt_A[0] + 0.01, r"$E_g^A=%.3f \mathrm{eV}$" % (popt_A[0]), fontsize=12
    )
    ax.text(
        4.5, popt_B[0] + 0.01, r"$E_g^B=%.3f \mathrm{eV}$" % (popt_B[0]), fontsize=12
    )
    print("Bound energy for A series: ", popt_A[0] - E_A_mean[0])
    print("Bound energy for B series: ", popt_B[0] - E_B_mean[0])
    ax.set_aspect("auto")
    ax.set_xlabel("n", fontsize=12)
    ax.set_ylabel("E (eV)", fontsize=12)
    ax.set_title("", fontsize=14)
    # ax.set_xlim([0.8, 6.5])
    ax.set_ylim([ax.get_ylim()[0], ax.get_ylim()[1] + 0.015])
    ax.legend()
    fig.savefig(
        "/home/aoxv/code/Data/Plots/ExcitonStates/" + "fit_excitons_AB.png",
        dpi=330,
        facecolor="w",
        bbox_inches="tight",
        pad_inches=0.1,
    )
    plt.close()

    # ### Fit Lorentzian peaks to excitonic states
    # mu_m0_A = 0.27  #   m_0
    # kappa = 2.3
    # E_A = [1.823, 1.980, 2.035]
    # x_A = [1, 2, 3]
    # A_fit = ExcitonFit(x_A, E_A, mu_m0_A)
    # popt = A_fit.KeldyshFit([2.1, 3.12])
    # # E_n = KeldyshPotential(mu_m0_A, *popt).get_eigen()[0]
    # E_n = KeldyshPotential(mu_m0_A, popt[0], kappa, popt[1]).get_eigen()[0]
    # E_n.sort()

    # fig, ax = plt.subplots()
    # ax.scatter(x_A, E_A, marker="o", color="r")
    # ax.plot(np.arange(1, 7), E_n[:6])
    # ax.set_aspect("auto")
    # ax.set_xlabel("", fontsize=12)
    # ax.set_ylabel("", fontsize=12)
    # ax.set_title("", fontsize=14)
    # ax.set_xlim(ax.get_xlim())
    # ax.set_ylim(ax.get_ylim())
    # fig.savefig(
    #     "/home/aoxv/code/Data/Plots/ExcitonStates/" + "fit_excitons_A.png",
    #     dpi=330,
    #     facecolor="w",
    #     bbox_inches="tight",
    #     pad_inches=0.1,
    # )
    # plt.close()

    # ### Fit Lorentzian peaks to excitonic states
    # mu_m0_B = 0.28  #   m_0
    # E_B = [1.921, 2.13, 2.193]
    # x_B = [1, 2, 3]
    # A_fit = ExcitonFit(x_B, E_B, mu_m0_B)
    # popt = A_fit.KeldyshFit([2.15, 3.05])
    # # E_n = KeldyshPotential(mu_m0_A, *popt).get_eigen()[0]
    # E_n = KeldyshPotential(mu_m0_B, popt[0], kappa, popt[1]).get_eigen()[0]
    # E_n.sort()

    # fig, ax = plt.subplots()
    # ax.scatter(x_B, E_B, marker="o", color="r")
    # ax.plot(np.arange(1, 7), E_n[:6])
    # ax.set_aspect("auto")
    # ax.set_xlabel("", fontsize=12)
    # ax.set_ylabel("", fontsize=12)
    # ax.set_title("", fontsize=14)
    # ax.set_xlim(ax.get_xlim())
    # ax.set_ylim(ax.get_ylim())
    # fig.savefig(
    #     "/home/aoxv/code/Data/Plots/ExcitonStates/" + "fit_excitons_B.png",
    #     dpi=330,
    #     facecolor="w",
    #     bbox_inches="tight",
    #     pad_inches=0.1,
    # )
    # plt.close()

    ### Initial verification
    # mu_m0_A = 0.27  #   m_0
    # mu_m0_B = 0.28  #   m_0

    # E_Ag = 2.18  #  eV
    # E_Bg = 2.36  #  eV

    # r_A0 = 3.05  #   nm
    # r_B0 = 2.70  #   nm

    # kappa = 4.4  #   dimensionless

    # A_series = KeldyshPotential(mu_m0_A, E_Ag, kappa, r_A0)
    # E_nA_list = []
    # zmax_list = [250]
    # eig_v_list = []
    # x_list = []

    # En_len = 8

    # psi_len = 1000
    # psi_num = 8

    # for zmax_i in zmax_list:
    #     E_nA, tmp_v = A_series.get_eigen(z_max=zmax_i, N=psi_len)
    #     print(sorted(E_nA))
    #     for n_i in range(psi_num):
    #         tmp_modulus = abs(tmp_v[:, np.argsort(E_nA)[n_i]]) ** 2
    #         tmp_modulus = np.insert(tmp_modulus, 0, 0)
    #         tmp_modulus = np.insert(tmp_modulus, len(tmp_modulus), 0)
    #         eig_v_list.append(tmp_modulus)
    #         x_list.append(np.linspace(0, zmax_i, psi_len + 1))
    #     E_nA.sort()
    #     E_nA_list.append(E_nA)

    # PlotMethod(
    #     [np.arange(1, En_len)] * len(E_nA_list),
    #     np.array(E_nA_list)[:, : En_len - 1],
    #     "n",
    #     "$E_n$ (meV)",
    #     title="A series",
    #     save_dir="tmp",
    #     save_name="A_series",
    #     legend=[r"$z_{\mathrm{max}}=%s$" % zmax for zmax in zmax_list],
    # ).multiple_line_one_plot()

    # PlotMethod(
    #     x_list,
    #     eig_v_list,
    #     "z",
    #     "$|\psi|^2$",
    #     title="",
    #     save_dir="tmp",
    #     save_name="A_series_wvf",
    #     legend=[r"$n=%s$" % n_i for n_i in np.arange(1, 7)],
    # ).multiple_line_one_plot()

    # #  Verification
    # mu = 0.16
    # kappa = 1
    # r_0 = 7.5  #   nm
    # E_g = 2.41  #   eV
    # rydberg_series = KeldyshPotential(mu, E_g, kappa, r_0)

    # E_nA_list = []
    # zmax_list = [600]
    # eig_v_list = []
    # x_list = []

    # En_len = 8
    # psi_num = 8
    # psi_len = 3500

    # for zmax_i in zmax_list:
    #     E_nA, tmp_v = rydberg_series.get_eigen(z_max=zmax_i, N=psi_len)
    #     for n_i in range(psi_num):
    #         tmp_modulus = abs(tmp_v[:, np.argsort(E_nA)[n_i]]) ** 2
    #         # print(tmp_modulus[0], tmp_modulus[-1])
    #         tmp_modulus = np.insert(tmp_modulus, 0, 0)
    #         tmp_modulus = np.insert(tmp_modulus, len(tmp_modulus), 0)
    #         eig_v_list.append(tmp_modulus)
    #         x_list.append(np.linspace(0, zmax_i, psi_len + 1))
    #     E_nA.sort()
    #     print(E_nA)
    #     E_nA_list.append(E_nA)
    # PlotMethod(
    #     [np.arange(1, En_len)] * len(E_nA_list),
    #     np.array(E_nA_list)[:, : En_len - 1],
    #     "n",
    #     "$E_n$ (meV)",
    #     title="Rydberg series",
    #     save_dir="tmp",
    #     save_name="Rydberg_series",
    #     legend=[r"$z_{\mathrm{max}}=%s$" % zmax for zmax in zmax_list],
    # ).multiple_scatter_one_plot()

    # PlotMethod(
    #     x_list,
    #     eig_v_list,
    #     "z",
    #     "$|\psi|^2$",
    #     title="",
    #     save_dir="tmp",
    #     save_name="Rydberg_series_wvf",
    #     legend=[r"$n=%s$" % n_i for n_i in np.arange(1, 7)],
    #     x_lim=[0, 10],
    # ).multiple_line_one_plot()

    pass


if __name__ == "__main__":
    main()
