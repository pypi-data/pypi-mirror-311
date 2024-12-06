from pkg_import.pkg_import import *
from pshe.optics import WaveLength, OpticalCoeff, Wsp, LorentzOscillator
from pshe.exp_data import *


class GHCalculation:
    def __init__(
        self,
        a_s,
        a_p,
        scan_angle_density=500,
        incident_angles=(pi / 4),
    ) -> None:
        if not (
            isinstance(incident_angles, list)
            or isinstance(incident_angles, np.ndarray)
            or isinstance(incident_angles, tuple)
        ):
            raise IncidentAngleNotAList(
                "Incident angle should be closed in a list so that you can use multiple "
                "incident angles to get multiple results for different angles"
            )

        self.scan_angle_list = linspace(
            42 / 180 * pi, 48 / 180 * pi, scan_angle_density
        )

        self.theta_0s = incident_angles
        self.a_s = a_s
        self.a_p = a_p

        self.start_wls = 496
        self.end_wls = 697

        pass

    def thin_film_model(
        self, wavelengths, n1_index, thickness, substrate_ob=BK7Substrate()
    ):
        """
        Get GH shift from thin-film model
        """
        ##  Sift data into the range we want
        boolean_arr = np.logical_and(
            wavelengths > self.start_wls, wavelengths < self.end_wls
        )
        GH_wls = wavelengths[boolean_arr]
        ##  interpolate the refractive indexes of substrate
        n0_index = substrate_ob.function_n0_wls(GH_wls)

        ##  Select n1_index on the chosen wavelength range
        n1_index = n1_index[boolean_arr]

        gh_wls_mat = np.kron(ones((len(self.theta_0s), 1)), GH_wls)

        k0 = 2 * pi * n0_index / GH_wls

        fc = OpticalCoeff(GH_wls, self.scan_angle_list, n0_index, n2_index=[1])

        r_s, r_p = fc.thin_film_model(n1_index, thickness)
        func_phis_der, func_phip_der = fc.der_phi_s_p_func(r_s, r_p)

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        w_s_func, w_p_func = Wsp(R_s, R_p, self.a_s, self.a_p).interpolate_along_row(
            self.scan_angle_list
        )

        delta_gh = array(
            [
                (
                    w_s_func(incident_angle) * func_phis_der(incident_angle)
                    + w_p_func(incident_angle) * func_phip_der(incident_angle)
                )
                / k0
                for incident_angle in self.theta_0s
            ]
        )

        return gh_wls_mat, real(delta_gh)

    @staticmethod
    def post_treatment(
        gh_wls_list,
        gh_shifts_list,
        theta_0s,
        save_name,
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
        if line_type is None:
            line_type = ["-"] * len(gh_wls_list)
        if legend is None:
            legend = [
                r"${:.2f}\degree$".format(ele_theta / pi * 180)
                for ele_theta in theta_0s
            ]
        if sub_save_dir is None:
            sub_save_dir = "GH"
        else:
            sub_save_dir = "GH/" + sub_save_dir

        return PlotMethod(
            gh_wls_list,
            gh_shifts_list,
            "$\lambda$ (nm)",
            "GH shift (nm)",
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

    def conductivity_model(self, wavelengths, sigma, substrate_ob=BK7Substrate()):
        """
        Get GH shift based on the conductivity model
        """
        ##  Sift data into the range we want
        # boolean_arr = np.logical_and(
        #     wavelengths > self.start_wls, wavelengths < self.end_wls
        # )
        # gh_wls = wavelengths[boolean_arr]
        # n0_index = substrate_ob.function_n0_wls(gh_wls)
        # sigma = sigma[boolean_arr]

        gh_wls, sigma = WaveLength().get_sifted_data(wavelengths, sigma)
        ##  interpolate the refractive indexes of substrate
        n0_index = substrate_ob.function_n0_wls(gh_wls)

        gh_wls_mat = np.kron(ones((len(self.theta_0s), 1)), gh_wls)

        k0 = 2 * pi * n0_index / gh_wls

        fc = OpticalCoeff(gh_wls, self.scan_angle_list, n0_index, n2_index=[1])

        r_s, r_p = fc.conductivity_model(sigma)
        func_phis_der, func_phip_der = fc.der_phi_s_p_func(r_s, r_p)

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        w_s_func, w_p_func = Wsp(R_s, R_p, self.a_s, self.a_p).interpolate_along_row(
            self.scan_angle_list
        )

        delta_gh = array(
            [
                (
                    w_s_func(incident_angle) * func_phis_der(incident_angle)
                    + w_p_func(incident_angle) * func_phip_der(incident_angle)
                )
                / k0
                for incident_angle in self.theta_0s
            ]
        )

        return gh_wls_mat, real(delta_gh)

    def lorentz_conductivity_model(
        self, centers, amps, gammas, energy=None, substrate_ob=BK7Substrate()
    ):
        """
        Use lorentz conductivity model to calculate GH shift

        Input energy should be in the unit of meV

        # Return
        gh_wls, gh_shift
        """
        if energy is None:
            sigma = LorentzOscillator(
                centers, amps, gammas, substrate_ob.dense_energy, times_i=True
            ).lorentz_result()

            lorentz_gh_wls, lorentz_gh_shift = self.conductivity_model(
                substrate_ob.dense_wls, sigma
            )
        else:
            sigma = LorentzOscillator(
                centers, amps, gammas, energy, times_i=True
            ).lorentz_result()

            lorentz_gh_wls, lorentz_gh_shift = self.conductivity_model(
                1240 / energy * 1000, sigma
            )

        return lorentz_gh_wls, lorentz_gh_shift

    def bg_shift_cond_based(self):
        gh_wls, gh_shift = self.lorentz_conductivity_model([2000], [0], [100])

        return gh_wls, gh_shift

    def bg_shift_perm_based(self, exp_data_ob=MoS2Data(), substrate_ob=BK7Substrate()):
        """
        Calculate Background shift based on permittivity model
        """
        wls = WaveLength().get_sifted_data(
            substrate_ob.dense_wls, substrate_ob.dense_n0_index
        )[0]
        n1_index = [sqrt(exp_data_ob.permittivity_infty)] * len(wls)

        gh_wls_mat, delta_gh = self.thin_film_model(
            wls, array(n1_index), exp_data_ob.thickness
        )

        return gh_wls_mat, delta_gh
