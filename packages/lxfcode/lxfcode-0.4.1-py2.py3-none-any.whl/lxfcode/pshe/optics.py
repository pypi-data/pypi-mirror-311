from pkg_import.pkg_import import *


class WaveLength:
    def __init__(self, start_wls=496, end_wls=697) -> None:
        self.start_wls = start_wls
        self.end_wls = end_wls
        pass

    def get_sifted_data(self, wls_in, var_in):
        boolean_arr = np.logical_and(
            array(wls_in) > self.start_wls, array(wls_in) < self.end_wls
        )
        wls = array(wls_in)[boolean_arr]
        var = array(var_in)[boolean_arr]

        return wls, var

    @staticmethod
    def get_wave_vector_mat(wavelength, n_index, len_theta):
        # print(len(wavelength), len(n_index), len_theta)

        n_index_mat = np.kron(ones((len_theta, 1)), n_index)
        wls_mat = np.kron(ones((len_theta, 1)), wavelength)

        ##  Wavevector
        k0 = 2 * pi * n_index_mat / wls_mat

        return k0, wls_mat, n_index_mat

    @staticmethod
    def get_theta_0s_mat(theta_0s, len_wls):
        """
        Get the matrix for theta_0
        """
        theta_0s_mat = np.kron(
            array(theta_0s).reshape((-1, 1)), array(ones((1, len_wls)))
        )

        return theta_0s_mat


class FresnelCoeff:
    """
    # Notes
    n0 and n2 should be arrays.
    """

    def __init__(
        self, incident_angle: float, n0_index: np.ndarray, n2_index: np.ndarray
    ) -> None:
        self.theta0 = incident_angle
        self.n0_index = n0_index
        self.n2_index = n2_index
        self.theta2 = arcsin(self.n0_index * sin(self.theta0)) / self.n2_index
        pass

    def original_coefficient(self):
        """
        Return the original coefficient when there is no material at the interface between n0 and n2

        # Return
        r_s, r_p, t_s, t_p
        """
        r_s: np.ndarray = (
            self.n0_index * cos(self.theta0) - self.n2_index * cos(self.theta2)
        ) / (self.n0_index * cos(self.theta0) + self.n2_index * cos(self.theta2))
        r_p: np.ndarray = (
            self.n2_index / cos(self.theta0) - self.n0_index / cos(self.theta2)
        ) / (self.n2_index / cos(self.theta0) + self.n0_index / cos(self.theta2))
        t_s: np.ndarray = (
            2
            * self.n0_index
            * cos(self.theta0)
            / (self.n0_index * cos(self.theta0) + self.n2_index * cos(self.theta2))
        )
        t_p: np.ndarray = (
            2
            * self.n0_index
            * cos(self.theta0)
            / (self.n2_index / cos(self.theta0) + self.n0_index / cos(self.theta2))
        )

        return r_s, r_p, t_s, t_p


class OpticalCoeff:
    def __init__(self, wavelengths, incident_angles, n0_index, n2_index) -> None:
        """
        Input n0 index and n2 index should NOT be in matrix form but should be in a list (or array) form
        """
        self.wls = array(wavelengths)
        self.theta_0s = array(incident_angles)

        if len(n0_index) != len(wavelengths):
            # print("Array-ize n0")
            self.n0_index = array(list(n0_index) * len(wavelengths))
        else:
            self.n0_index = n0_index

        if len(n2_index) != len(wavelengths):
            # print("Array-ize n2")
            self.n2_index = array(list(n2_index) * len(wavelengths))
        else:
            self.n2_index = array(n2_index)

        self.len_theta0 = len(incident_angles)
        self.len_wls = len(wavelengths)

        self.n0_index_mat = np.kron(ones((self.len_theta0, 1)), self.n0_index)
        self.n2_index_mat = np.kron(ones((self.len_theta0, 1)), self.n2_index)

        self.theta_0s_mat = np.kron(
            ones((1, self.len_wls)), self.theta_0s.reshape((self.len_theta0, 1))
        )
        self.theta_2s_mat = arcsin(
            self.n0_index_mat * sin(self.theta_0s_mat) / self.n2_index_mat
        )

        pass

    def original_coefficient(self):
        """
        Return the original coefficient when there is no material at the interface between n0 and n2

        # Return
        r_s, r_p
        """
        r_s = (
            self.n0_index_mat * cos(self.theta_0s_mat)
            - self.n2_index_mat * cos(self.theta_2s_mat)
        ) / (
            self.n0_index_mat * cos(self.theta_0s_mat)
            + self.n2_index_mat * cos(self.theta_2s_mat)
        )
        r_p = (
            self.n2_index_mat / cos(self.theta_0s_mat)
            - self.n0_index_mat / cos(self.theta_2s_mat)
        ) / (
            self.n2_index_mat / cos(self.theta_0s_mat)
            + self.n0_index_mat / cos(self.theta_2s_mat)
        )
        t_s = (
            2
            * self.n0_index_mat
            * cos(self.theta_0s_mat)
            / (
                self.n0_index_mat * cos(self.theta_0s_mat)
                + self.n2_index_mat * cos(self.theta_2s_mat)
            )
        )
        t_p = (
            2
            * self.n0_index_mat
            * cos(self.theta_0s_mat)
            / (
                self.n2_index_mat / cos(self.theta_0s_mat)
                + self.n0_index_mat / cos(self.theta_2s_mat)
            )
        )

        return r_s, r_p, t_s, t_p

    def thin_film_model(self, n1_index, thickness):
        """
            Get rs and rp from thin-film model

            --- Wavelength ---
            -
            -
            -
        incident angle
            -
            -
            -
        """
        n1_index = np.kron(ones((self.len_theta0, 1)), n1_index)

        ##  angle in MoS2
        theta_1 = arcsin(self.n0_index_mat * sin(self.theta_0s_mat) / n1_index)

        ##  angle in air
        theta_2 = conj(
            arcsin(self.n0_index_mat * sin(self.theta_0s_mat) / self.n2_index_mat)
        )

        ##  the wave vector in MoS2
        k = 2 * pi * n1_index / self.wls

        ##  Phase
        phase_factor = exp(2j * k * thickness * cos(theta_1))

        r1s = -sin(self.theta_0s_mat - theta_1) / sin(self.theta_0s_mat + theta_1)
        r2s = -sin(theta_1 - theta_2) / (sin(theta_1 + theta_2))
        r1p = np.tan(self.theta_0s_mat - theta_1) / np.tan(self.theta_0s_mat + theta_1)
        r2p = np.tan(theta_1 - theta_2) / np.tan(theta_1 + theta_2)

        r_s = (r1s + r2s * phase_factor) / (1 + r1s * r2s * phase_factor)
        r_p = (r1p + r2p * phase_factor) / (1 + r1p * r2p * phase_factor)

        return r_s, r_p

    def conductivity_model(self, sigma):
        """
        Get rs and rp from conductivity
        """
        ##  theta 2
        theta_2_mat = conj(
            arcsin(self.n0_index_mat * sin(self.theta_0s_mat) / self.n2_index_mat)
        )

        sigma_mat = np.kron(ones((self.len_theta0, 1)), sigma)

        r_s_numerator = (
            self.n0_index_mat * cos(self.theta_0s_mat)
            - self.n2_index_mat * cos(theta_2_mat)
            - sigma_mat
        )
        r_s_denominat = (
            self.n0_index_mat * cos(self.theta_0s_mat)
            + self.n2_index_mat * cos(theta_2_mat)
            + sigma_mat
        )

        r_p_numerator = (
            self.n2_index_mat / cos(theta_2_mat)
            - self.n0_index_mat / cos(self.theta_0s_mat)
            + sigma_mat
        )
        r_p_denominat = (
            self.n2_index_mat / cos(theta_2_mat)
            + self.n0_index_mat / cos(self.theta_0s_mat)
            + sigma_mat
        )
        r_s = r_s_numerator / r_s_denominat
        r_p = r_p_numerator / r_p_denominat

        return r_s, r_p

    def der_phi_s_p_func(self, r_s, r_p):
        """
        Get the derivative of phi_s and phi_p
        """
        if len(self.theta_0s) > 1:
            phi_s = np.angle(r_s)
            phi_p = np.angle(r_p)

            diff_phi_s = np.diff(phi_s, axis=0)
            diff_phi_p = np.diff(phi_p, axis=0)

            der_phi_s = diff_phi_s / np.diff(self.theta_0s).reshape((-1, 1))
            der_phi_p = diff_phi_p / np.diff(self.theta_0s).reshape((-1, 1))

            der_phi_s_func_list = [
                interpolate.interp1d(self.theta_0s[:-1], der_phi_s[:, col_i])
                for col_i in range(der_phi_s.shape[1])
            ]
            der_phi_p_func_list = [
                interpolate.interp1d(self.theta_0s[:-1], der_phi_p[:, col_i])
                for col_i in range(der_phi_p.shape[1])
            ]

            def func_phis_derivative(theta_in):
                derivative = [ele_func(theta_in) for ele_func in der_phi_s_func_list]
                return array(derivative)

            def func_phip_derivative(theta_in):
                derivative = [ele_func(theta_in) for ele_func in der_phi_p_func_list]
                return array(derivative)

            return func_phis_derivative, func_phip_derivative

        else:
            print("The length of incident angle list should be greater than 1.")

    def diff_R_thin_film(self, n1_index, thickness):
        """
        # Return
        Diff_R_s, Diff_R_p
        """
        n1_index = np.kron(ones((self.len_theta0, 1)), n1_index)

        ##  angle in MoS2
        theta_1 = arcsin(self.n0_index_mat * sin(self.theta_0s_mat) / n1_index)

        ##  angle in air
        theta_2 = conj(
            arcsin(self.n0_index_mat * sin(self.theta_0s_mat) / self.n2_index_mat)
        )

        ##  the wave vector in MoS2
        k = 2 * pi * n1_index / self.wls

        ##  Phase
        phase_factor = exp(2j * k * thickness * cos(theta_1))

        r1s = -sin(self.theta_0s_mat - theta_1) / sin(self.theta_0s_mat + theta_1)
        r2s = -sin(theta_1 - theta_2) / (sin(theta_1 + theta_2))
        r1p = np.tan(self.theta_0s_mat - theta_1) / np.tan(self.theta_0s_mat + theta_1)
        r2p = np.tan(theta_1 - theta_2) / np.tan(theta_1 + theta_2)

        r_s = (r1s + r2s * phase_factor) / (1 + r1s * r2s * phase_factor)
        r_p = (r1p + r2p * phase_factor) / (1 + r1p * r2p * phase_factor)

        rs_0, rp_0 = self.original_coefficient()[:2]

        R_s = abs(r_s) ** 2
        R_p = abs(r_p) ** 2
        Rs_0 = abs(rs_0) ** 2
        Rp_0 = abs(rp_0) ** 2

        Diff_R_s = (R_s - Rs_0) / Rs_0
        Diff_R_p = (R_p - Rp_0) / Rp_0

        return Diff_R_s, Diff_R_p


class Wsp:
    def __init__(self, R_s, R_p, a_s, a_p) -> None:
        self.R_s = R_s
        self.R_p = R_p
        self.a_s = a_s
        self.a_p = a_p
        pass

    def calculate(self):
        """
        # Return
        w_s
        """
        numerator_s = self.R_s**2 * self.a_s**2
        numerator_p = self.R_p**2 * self.a_p**2
        denominat = self.R_s**2 * self.a_s**2 + self.R_p**2 * self.a_p**2

        output_s = numerator_s / denominat
        output_p = numerator_p / denominat

        return output_s, output_p

    def interpolate_along_row(self, angle_list):
        """
        Interpolate the value along the row direction to get the w_s and w_p array at specific incident angle.

        This function only applies when the dimension of R_s and R_p is greater than 1 (2)
        """
        numerator_s = self.R_s**2 * self.a_s**2
        numerator_p = self.R_p**2 * self.a_p**2
        denominat = self.R_s**2 * self.a_s**2 + self.R_p**2 * self.a_p**2

        w_s_mat = numerator_s / denominat
        w_p_mat = numerator_p / denominat

        w_s_lambda_func_list = [
            interpolate.interp1d(angle_list, w_s_mat[:, col_i])
            for col_i in range(w_s_mat.shape[1])
        ]
        w_p_lambda_func_list = [
            interpolate.interp1d(angle_list, w_p_mat[:, col_i])
            for col_i in range(w_p_mat.shape[1])
        ]

        def w_s_at_certain_angle(theta_in):
            result = [ele_func(theta_in) for ele_func in w_s_lambda_func_list]
            return array(result)

        def w_p_at_certain_angle(theta_in):
            result = [ele_func(theta_in) for ele_func in w_p_lambda_func_list]
            return array(result)

        return w_s_at_certain_angle, w_p_at_certain_angle


class LorentzOscillator:
    def __init__(
        self,
        centers,
        amps,
        gammas,
        x_arr=linspace(0, 3000, 200),
        times_i=False,
        x_label="x",
        y_label="y",
    ) -> None:
        """
        Input centers, amplitudes and gammas should be all in list and have one-to-one correspondence.
        """
        self.lorentz_len = len(centers)

        self.centers = array(centers)
        self.amps = array(amps)
        self.gammas = array(gammas)
        self.times_i = times_i

        self.x_arr = x_arr
        self.x_arr_name = x_label
        self.ylabel = y_label

        self.complex_result = self.lorentz_result()
        self.real_part = real(self.complex_result)
        self.imag_part = imag(self.complex_result)

        self.amplitudes = self._amp_ratio_to_real_amp()

        self.save_dir = "Lorentz"

        pass

    def lorentz_result(self):
        """
        The original form of Lorentzian oscillator.
        """

        def lorentz_single(centers, amps, gammas, times_i):
            ratio = sqrt(gammas / centers) * centers
            amp = ratio * amps

            denominator_1 = (centers**2 - self.x_arr**2) ** 2
            denominator_2 = gammas**2 * self.x_arr**2
            denominator = denominator_1 + denominator_2

            real_part = amp**2 * (centers**2 - self.x_arr**2) / denominator
            imag_part = amp**2 * gammas * self.x_arr / denominator

            complex_form = real_part + 1j * imag_part
            if times_i:
                complex_form = complex_form * (-1j)

            return complex_form

        results_arr = array(
            [
                lorentz_single(
                    self.centers[i], self.amps[i], self.gammas[i], times_i=self.times_i
                )
                for i in range(self.lorentz_len)
            ]
        )
        # print("Result array: ", results_arr.shape)
        sum_arr = np.sum(results_arr, axis=0)
        return sum_arr

    def components_list(self):

        def lorentz_single(centers, amps, gammas, times_i):
            ratio = sqrt(gammas / centers) * centers
            amp = ratio * amps

            denominator_1 = (centers**2 - self.x_arr**2) ** 2
            denominator_2 = gammas**2 * self.x_arr**2
            denominator = denominator_1 + denominator_2

            real_part = amp**2 * (centers**2 - self.x_arr**2) / denominator
            imag_part = amp**2 * gammas * self.x_arr / denominator

            complex_form = real_part + 1j * imag_part
            if times_i:
                complex_form = complex_form * (-1j)

            return complex_form

        results_arr = array(
            [
                lorentz_single(
                    self.centers[i], self.amps[i], self.gammas[i], times_i=self.times_i
                )
                for i in range(self.lorentz_len)
            ]
        )

        return results_arr

    def _amp_ratio_to_real_amp(self):
        def real_amp(centers, amps, gammas):
            ratio = sqrt(gammas / centers) * centers
            omega_p = ratio * amps

            max_amp = omega_p**2 / (gammas * centers)

            return omega_p  # max_amp

        real_amplitudes = array(
            [
                real_amp(self.centers[i], self.amps[i], self.gammas[i])
                for i in range(self.lorentz_len)
            ]
        )

        return real_amplitudes

    def lorentz_plot(self, save_name="lorentz", save_dir=None, text=""):
        """
        Deal with list of parameters
        """
        if save_dir is None:
            pass
        else:
            save_dir = self.save_dir + "/" + save_dir
        PlotMethod(
            [self.x_arr] * 2,
            [self.real_part, self.imag_part],
            x_label=self.x_arr_name,
            y_label="y",
            title="Lorentz oscillator",
            save_name=save_name + "_total",
            legend=["Real part", "Imaginary part"],
            save_dir=save_dir,
        ).multiple_line_one_plot()

        real_sub_lorentz = [
            LorentzOscillator(
                [self.centers[i]],
                [self.amps[i]],
                [self.gammas[i]],
                x_arr=self.x_arr,
                times_i=self.times_i,
            ).real_part
            for i in range(self.lorentz_len)
        ]
        imag_sub_lorentz = [
            LorentzOscillator(
                [self.centers[i]],
                [self.amps[i]],
                [self.gammas[i]],
                x_arr=self.x_arr,
                times_i=self.times_i,
            ).imag_part
            for i in range(self.lorentz_len)
        ]

        line_type = ["-"] + ["--"] * self.lorentz_len
        opacity = [1] + [0.2] * self.lorentz_len

        PlotMethod(
            [self.x_arr] * (1 + self.lorentz_len),
            [self.real_part] + real_sub_lorentz,
            x_label=self.x_arr_name,
            y_label=self.ylabel,
            title="Real part",
            save_name=save_name + "_real",
            legend=["Real part"],
            save_dir=save_dir,
            text=text,
            text_xy=(1.01, 0),
            line_type=line_type,
        ).multiple_line_one_plot(opacity, text_annotate=True)

        PlotMethod(
            [self.x_arr] * (1 + self.lorentz_len),
            [self.imag_part] + imag_sub_lorentz,
            x_label=self.x_arr_name,
            y_label=self.ylabel,
            title="Imaginary part",
            save_name=save_name + "_imag",
            legend=["Imaginary part"],
            save_dir=save_dir,
            text=text,
            text_xy=(1.01, 0),
            line_type=line_type,
        ).multiple_line_one_plot(opacity, text_annotate=True)


class Permittivity:
    def __init__(self, permittivity_infty) -> None:
        self.permittivity_infty = permittivity_infty

        pass

    def lorentzian_combination_to_perm(self, energy, centers, amps, gammas):
        """
        # Return
        complex_permittivity
        """
        lo = LorentzOscillator(
            centers,
            amps,
            gammas,
            energy,
            times_i=False,
            x_label="E (meV)",
            y_label=r"$\varepsilon_0$",
        )
        out_result: np.ndarray = self.permittivity_infty + lo.complex_result

        return out_result

    def lorentz_combi_to_sigma_2d(self, energy, centers, amps, gammas, thickness):
        """
        Convert Lorentzian combinations to 2d conductivity

        # Return
        Complex 2D sigma tilde (reduced conductivity)
        """
        omega = UnitsConversion.energy2omega(energy)

        complex_permittivity_result = self.lorentzian_combination_to_perm(
            energy, centers, amps, gammas
        )

        sigma_tilde = (
            (complex_permittivity_result - self.permittivity_infty)
            * omega
            * thickness
            / (c_speed * m2nm * 1j)
        )

        return sigma_tilde

    def lorentz_component_to_sigma_2d_list(
        self, energy, centers, amps, gammas, thickness
    ):

        y = []
        for elei in range(len(centers)):
            ele_center = [centers[elei]]
            ele_amp = [amps[elei]]
            ele_gamma = [gammas[elei]]
            result = self.lorentz_combi_to_sigma_2d(
                energy, ele_center, ele_amp, ele_gamma, thickness
            )
            y.append(result)

        return y

    def lorentz_sigma2d_to_perm(self, energy, centers, amps, gammas, thickness):
        """
        Convert 2d conductivity to permittivity

        # Return
        Permittivity
        """
        omega = UnitsConversion.energy2omega(energy)

        lo = LorentzOscillator(
            centers,
            amps,
            gammas,
            energy,
            times_i=True,
            x_label="E (meV)",
            y_label=r"$\varepsilon_0$",
        )

        sigma_tilde = lo.complex_result

        response_term = 1j * (sigma_tilde * c_speed * m2nm) / (omega * thickness)

        perm = self.permittivity_infty + response_term

        return perm


class ComplexRefractiveIndex:
    def __init__(self, complex_permittivity) -> None:
        self.complex_permittivity = complex_permittivity

        self.n, self.k = self.get_n_k_from_permittivity()

        self.complex_refractive_index = self.n + 1j * self.k

        pass

    def get_n_k_from_permittivity(self):
        """
        Get n and k from permittivity

        # Return
        n, k
        """
        modulus = abs(self.complex_permittivity)

        angle = np.angle(self.complex_permittivity)

        half_angle = angle / 2

        n: np.ndarray = sqrt(modulus) * cos(half_angle)
        k: np.ndarray = sqrt(modulus) * sin(half_angle)

        return n, k
