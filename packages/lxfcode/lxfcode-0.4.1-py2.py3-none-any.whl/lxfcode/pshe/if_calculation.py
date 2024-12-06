from pkg_import.pkg_import import *
from pshe.optics import (
    WaveLength,
    OpticalCoeff,
    Wsp,
    LorentzOscillator,
    Permittivity,
    ComplexRefractiveIndex,
)
from pshe.exp_data import *


class IFCalculation:
    """
    Used to calculate IF shift based on thin-film model and conductivity model.
    """

    def __init__(self, a_s, a_p, incident_angles=(pi / 4,), eta=pi / 2) -> None:
        """
        eta is the phase difference between two component of the electric field
        """
        if not (
            isinstance(incident_angles, list)
            or isinstance(incident_angles, np.ndarray)
            or isinstance(incident_angles, tuple)
        ):
            raise IncidentAngleNotAList(
                "Incident angle should be closed in a list so that you can use multiple "
                "incident angles to get multiple results for different angles"
            )

        self.theta_0s = incident_angles
        self.a_s = a_s
        self.a_p = a_p
        self.eta = eta

        pass

    def thin_film_model(
        self, wavelengths, n1_index, thickness, substrate_ob=BK7Substrate()
    ):
        """
        Use thin film model to calculate tht IF shift based on the refractive indexes of substrate and material
        # Parameters

        start_wls: The wavelength starting point in the calculations

        # Notes
        The wavelengths input should be in the unit of nm

        # Return
        IF_wls_mat, real(Delta_IF)
        """
        ##  Sift data into the range we want
        IF_wls, n1_index = WaveLength().get_sifted_data(wavelengths, n1_index)
        ##  interpolate the refractive indexes of substrate
        n0_index = substrate_ob.function_n0_wls(IF_wls)

        ##  Wavevector
        k0, IF_wls_mat = WaveLength.get_wave_vector_mat(
            IF_wls, n0_index, len(self.theta_0s)
        )[:2]

        r_s, r_p = OpticalCoeff(IF_wls, self.theta_0s, n0_index, [1]).thin_film_model(
            n1_index, thickness
        )

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        phi_s = np.angle(r_s)  # Angle of rs and rp
        phi_p = np.angle(r_p)  # Angle of rs and rp

        w_s, w_p = Wsp(R_s, R_p, self.a_s, self.a_p).calculate()

        Delta_IF = (
            -1
            / (k0 * np.tan(self.theta_0s))
            * (
                (w_p * self.a_s**2 + w_s * self.a_p**2)
                / (self.a_p * self.a_s)
                * sin(self.eta)
                + 2 * sqrt(w_p * w_s) * sin(self.eta - phi_p + phi_s)
            )
        )

        return IF_wls_mat, real(Delta_IF)

    def conductivity_model(self, wavelengths, sigma, substrate_ob=BK7Substrate()):
        """
        Note the sigma here is dimensionless conductivity
        """
        ##  Sift data into the range we want
        IF_wls, sigma = WaveLength().get_sifted_data(wavelengths, sigma)
        ##  interpolate the refractive indexes of substrate
        n0_index = substrate_ob.function_n0_wls(IF_wls)

        ##  Wavevector
        k0_mat, IF_wls_mat = WaveLength.get_wave_vector_mat(
            IF_wls, n0_index, len(self.theta_0s)
        )[:2]

        r_s, r_p = OpticalCoeff(
            IF_wls, self.theta_0s, n0_index, [1]
        ).conductivity_model(sigma)

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        phi_s = np.angle(r_s)  # Angle of rs and rp
        phi_p = np.angle(r_p)  # Angle of rs and rp

        w_s, w_p = Wsp(R_s, R_p, self.a_s, self.a_p).calculate()

        theta_0s_mat = WaveLength.get_theta_0s_mat(self.theta_0s, len(IF_wls))

        # print(theta_0s_mat.shape, k0_mat.shape, IF_wls_mat.shape)

        Delta_IF = (
            -1
            / (k0_mat * np.tan(theta_0s_mat))
            * (
                (w_p * self.a_s**2 + w_s * self.a_p**2)
                / (self.a_p * self.a_s)
                * sin(self.eta)
                + 2 * sqrt(w_p * w_s) * sin(self.eta - phi_p + phi_s)
            )
        )

        return IF_wls_mat, real(Delta_IF)

    @staticmethod
    def post_treatment(
        if_wls_list,
        if_shifts_list,
        theta_0s,
        save_name="testIF",
        save_type="plot",
        legend=None,
        text=None,
        text_xy=None,
        text_annotate=False,
        sub_save_dir=None,
        title="",
        line_type=None,
        ax_return=False,
        colors=None,
    ):
        if legend is None:
            legend = [
                r"${:.2f}\degree$".format(ele_theta / pi * 180)
                for ele_theta in theta_0s
            ]
        if line_type is None:
            line_type = ["-"] * len(if_wls_list)
        if sub_save_dir is None:
            sub_save_dir = "IF"
        else:
            sub_save_dir = "IF/" + sub_save_dir
        if save_type == "plot":
            if (text is None) and text_annotate:
                raise TypeError(
                    "Please input the text and the text_xy when you set text_annotate as True"
                )
            return PlotMethod(
                if_wls_list,
                if_shifts_list,
                r"$\lambda$ (nm)",
                "IF shift (nm)",
                title=title,
                save_name=save_name,
                save_dir=sub_save_dir,
                legend=legend,
                text=text,
                text_xy=text_xy,
                line_type=line_type,
                ax_return=ax_return,
                colors=colors,
            ).multiple_line_one_plot(text_annotate=text_annotate)
        elif save_type == "html":
            HtmlPlotMethod(
                if_wls_list,
                if_shifts_list,
                r"$\lambda$ (nm)",
                "IF shift (nm)",
                title=title,
                save_name=save_name,
                save_dir=sub_save_dir,
                legend=legend,
            ).multiple_line_one_plot()

    def lorentz_conductivity_model(
        self, centers, amps, gammas, energy=None, substrate_ob=BK7Substrate()
    ):
        """
        Use conductivity model to calculate IF shift

        Input energy should be in the unit of meV

        # Return
        if_wls, if_shift
        """
        if energy is None:
            sigma = LorentzOscillator(
                centers, amps, gammas, substrate_ob.dense_energy, times_i=True
            ).lorentz_result()

            lorentz_if_wls, lorentz_if_shift = self.conductivity_model(
                substrate_ob.dense_wls, sigma
            )
        else:
            sigma = LorentzOscillator(
                centers, amps, gammas, energy, times_i=True
            ).lorentz_result()

            lorentz_if_wls, lorentz_if_shift = self.conductivity_model(
                1240 / energy * 1000, sigma
            )

        return lorentz_if_wls, lorentz_if_shift

    def bg_shift_cond_based(self, substrate_ob=BK7Substrate()):
        wls, n0 = WaveLength().get_sifted_data(
            substrate_ob.dense_wls, substrate_ob.dense_n0_index
        )

        k0, IF_wls_mat = WaveLength.get_wave_vector_mat(wls, n0, len(self.theta_0s))[:2]
        theta_0s_mat = WaveLength.get_theta_0s_mat(self.theta_0s, len(wls))

        return self.conductivity_model(wls, np.zeros((len(wls),)))

        # r_s, r_p = OpticalCoeff(wls, self.theta_0s, n0, [1]).original_coefficient()[:2]

        # k0, IF_wls_mat = WaveLength.get_wave_vector_mat(wls, n0, len(self.theta_0s))[:2]
        # theta_0s_mat = WaveLength.get_theta_0s_mat(self.theta_0s, len(wls))

        # R_s = abs(r_s)  # Amplitude of rs and rp
        # R_p = abs(r_p)  # Amplitude of rs and rp
        # phi_s = np.angle(r_s)  # Angle of rs and rp
        # phi_p = np.angle(r_p)  # Angle of rs and rp

        # w_s, w_p = Wsp(R_s, R_p, self.a_s, self.a_p).calculate()

        # Delta_IF = (
        #     -1
        #     / (k0 * np.tan(theta_0s_mat))
        #     * (
        #         (w_p * self.a_s**2 + w_s * self.a_p**2)
        #         / (self.a_p * self.a_s)
        #         * sin(self.eta)
        #         + 2 * sqrt(w_p * w_s) * sin(self.eta - phi_p + phi_s)
        #     )
        # )

        # return IF_wls_mat, real(Delta_IF)

    def bg_shift_perm_based(self, exp_data_ob=MoS2Data(), substrate_ob=BK7Substrate()):
        """
        Calculate Background shift based on permittivity model
        """
        wls = WaveLength().get_sifted_data(
            substrate_ob.dense_wls, substrate_ob.dense_n0_index
        )[0]
        n1_index = [sqrt(exp_data_ob.permittivity_infty)] * len(wls)

        IF_wls_mat, Delta_IF = self.thin_film_model(
            wls, array(n1_index), exp_data_ob.thickness
        )

        return IF_wls_mat, Delta_IF


def main() -> NoReturn:
    """
    Test the sensitivity of Photonic spin Hall effect.
    """
    wls, shift = IFCalculation(1, 1).lorentz_conductivity_model([2100], [0.3], [50])
    fig, ax = plt.subplots()
    ax.plot(wls[0], shift[0])
    ax.set_aspect("auto")
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.set_title("", fontsize=14)
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    fig.savefig(
        "ifShift_lorentz.png",
        dpi=330,
        facecolor="w",
        bbox_inches="tight",
        pad_inches=0.1,
    )
    plt.close()

    centers = [2100]
    amps = [0.8]
    gammas = [50]
    perm = Permittivity(15.6).lorentzian_combination_to_perm(
        np.linspace(1700, 2300), centers, amps, gammas
    )
    fig, ax = plt.subplots()
    ax.plot(np.linspace(1700, 2300), np.real(perm))
    ax.plot(np.linspace(1700, 2300), np.imag(perm))
    ax.set_aspect("auto")
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.set_title("", fontsize=14)
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    fig.savefig(
        "perm_lorentz.png",
        dpi=330,
        facecolor="w",
        bbox_inches="tight",
        pad_inches=0.1,
    )
    plt.close()

    # density = 300
    # energy_range = linspace(1800, 2500, density)
    # wls_range = 1240 / energy_range * 1000

    # perm_ob = Permittivity(MoS2Data().permittivity_infty)
    # perm_result = perm_ob.lorentzian_combination_to_perm(
    #     linspace(1800, 2500, density), [2000], [4], [30]
    # )
    # n, k = ComplexRefractiveIndex(perm_result).get_n_k_from_permittivity()
    # n1 = n + 1j * k
    # if_shift = EigenShiftDifference(incident_angles=[pi / 4]).lcp_rcp_if_thin_film(
    #     wls_range, n1, MoS2Data().thickness
    # )

    # x_bar, y_bar = BackgroundShift(
    #     incident_angles=[pi / 4], exp_data_ob=MoS2Data()
    # ).bg_if_center_perm_based()

    # p_method = PlotMethod(
    #     wls_range, if_shift[0], save_dir="IF/theory/MoS2/bg", save_name="test"
    # )
    # p_method.line_plot()

    # for ele_perm in perm_infty_list:
    #     perm = Permittivity(ele_perm)
    #     energy_range = linspace(1800, 2500, density)
    #     wls_range = 1240 / energy_range * 1000
    #     perm_result = perm.lorentzian_combination_to_perm(
    #         linspace(1800, 2500, density),
    #         [2000],
    #         [4],
    #         [30],
    #     )
    #     n, k = ComplexRefractiveIndex(perm_result).get_n_k_from_permittivity()
    #     n1 = n + 1j * k

    #     lcp_if_wls, lcp_if_shift = IFCalculation(
    #         a_s=1, a_p=1, eta=-pi / 2
    #     ).thin_film_model(wls_range, n1, 0.8)

    #     ##  Find peaks
    #     peaks = scipy.signal.argrelextrema(lcp_if_shift[0], np.greater, order=10)
    #     ditches = scipy.signal.argrelextrema(lcp_if_shift[0], np.less, order=10)
    #     l_peaks.append(lcp_if_shift[0][peaks])

    #     l_ditches.append(lcp_if_shift[0][ditches])

    #     lwls_list.append(lcp_if_wls[0])
    #     lshift_list.append(lcp_if_shift[0])

    # for ele_i in range(len(MoS2Data().if_shifts_list)):
    #     data1 = MoS2Data().if_shifts_list[ele_i]
    #     wls1 = MoS2Data().if_wls_list[ele_i]
    #     peaks = scipy.signal.argrelextrema(data1, np.greater, order=1)
    #     peaks, _ = scipy.signal.find_peaks(data1, distance=6)
    #     # ditches = scipy.signal.argrelextrema(data1, np.less, order=4)
    #     pmethod = PlotMethod(
    #         wls1,
    #         data1,
    #         save_dir="IF/exp/MoS2Data",
    #         save_name="peaks_ditches_sample{}".format(ele_i),
    #         x_label=r"$\lambda$ (nm)",
    #         y_label="IF shift (nm)",
    #         title="Sample 1",
    #         hold_on=True,
    #     )
    #     pmethod.line_plot()
    #     pmethod.x = [wls1[peaks]]
    #     pmethod.y = [data1[peaks]]
    #     pmethod.legend = ["Peaks"]
    #     pmethod.multiple_scatter_one_plot()
    return


if __name__ == "__main__":
    main()
