from public.method import *
from public.consts import *
from public.error import *


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

    def _amp_ratio_to_real_amp(self):
        def real_amp(centers, amps, gammas):
            ratio = sqrt(gammas / centers) * centers
            omega_p = ratio * amps

            max_amp = omega_p**2 / (gammas * centers)

            return max_amp

        real_amplitudes = array(
            [
                real_amp(self.centers[i], self.amps[i], self.gammas[i])
                for i in range(self.lorentz_len)
            ]
        )

        return real_amplitudes

    def lorentz_plot(self, save_name="lorentz", save_dir=None):
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
        ).multiple_line_one_plot(line_type, opacity)

        PlotMethod(
            [self.x_arr] * (1 + self.lorentz_len),
            [self.imag_part] + imag_sub_lorentz,
            x_label=self.x_arr_name,
            y_label=self.ylabel,
            title="Imaginary part",
            save_name=save_name + "_imag",
            legend=["Imaginary part"],
            save_dir=save_dir,
        ).multiple_line_one_plot(line_type, opacity)

        return


class FresnelCoefficients:
    def __init__(self, wavelengths, incident_angles, n0_index, n2_index) -> None:
        """
        Input n0 index and n2 index should NOT be in matrix form but in a list (or array) form
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
        self.theta_2s_mat = (
            arcsin(self.n0_index_mat * sin(self.theta_0s_mat)) / self.n2_index_mat
        )

        pass

    def original_coefficient(self):
        """
        Return the original coefficient when there is no material at the interface between n0 and n2
        """
        r_s = (
            self.n0_index_mat * cos(self.theta_0s_mat)
            - self.n2_index_mat * cos(self.theta_2s_mat)
        ) / (
            self.n0_index_mat * cos(self.theta_0s_mat)
            + self.n2_index_mat * cos(self.theta_2s_mat)
        )
        r_p = (
            self.n2_index_mat / cos(self.theta_2s_mat)
            - self.n0_index_mat / cos(self.theta_0s_mat)
        ) / (
            self.n2_index_mat / cos(self.theta_2s_mat)
            + self.n0_index_mat / cos(self.theta_0s_mat)
        )

        return r_s, r_p

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
        r_s = r_s_numerator / r_s_denominat

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


class BK7Substrate:
    BK7_file_path = data_file_dir + "00_common_sense/N-BK7.xlsx"

    _instance = None
    _init_flag = False

    def __init__(self, wls_points=1000) -> None:
        if self._init_flag:
            return
        else:
            (
                self.dense_wls,
                self.dense_energy,
                self.dense_n0_index,
                self.function_n0_wls,
            ) = self.get_n0_interp_func(wls_points)

            self._init_flag = True
        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
            return cls._instance
        else:
            return cls._instance

    @classmethod
    def get_n0_interp_func(cls, wls_points):
        """
        Get the interpolated function of n0 over wavelength (or energy)
        #   return
        dense_wls, dense_energy, dense_n0_index, f_n0 (f_n0 is the function of wavelength, not energy)
        """
        ##  Read the refractive index of BK-7 from database
        data_list = PubMeth.read_xlsx_data(cls.BK7_file_path, exclude_rows_num=1)

        wave_length_n0 = data_list[0]
        ref_index_n0 = array(data_list[1]) + 1j * zeros(len(data_list[1]))
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), wls_points)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        return dense_wls, dense_energy, dense_n0_index, f_n0


class MoS2Data:
    __Wu_cond_file_path = data_file_dir + "00_common_sense/Wu_cond_original.csv"
    __refractive_indexes_dir = "/home/aoxv/code/Data/00_common_sense/exp_indices/"
    __refractive_indexes_name = os.listdir(__refractive_indexes_dir)
    __exp_if_shift_dir = "/home/aoxv/code/Data/00_exp_data/IF_shift_MoS2/"
    __if_samples_names = os.listdir(__exp_if_shift_dir)
    __exp_gh_shift_dir = "/home/aoxv/code/Data/00_exp_data/GH_shift_MoS2/"
    __gh_samples_names = os.listdir(__exp_gh_shift_dir)
    _bg_if_gh_data = "/home/aoxv/code/Data/00_exp_data/Base_shift_BK7/bg_shift.xlsx"

    unit_sigma_eps0_x_c = eps0_x_c
    unit_sigma_e2_over_h = c_eV**2 / h_planck

    permittivity_infty = 15.6

    _instance = None
    _init_flag = False

    def __init__(self, thickness=0.8, sample_num=5) -> None:
        if self._init_flag:
            return
        else:
            ##  Preload data
            self.sample_num = sample_num
            t1 = time.perf_counter()
            (
                self.Wu_wls_original,
                self.Wu_energy_original,
                self.Wu_cond_complex_as_e2_over_h,
            ) = self.read_Wu_cond_original_data()
            self.Wu_cond_complex_as_eps_x_c = (
                self.Wu_cond_complex_as_e2_over_h
                / self.unit_sigma_eps0_x_c
                * self.unit_sigma_e2_over_h
            )
            (
                self.ref_indexes_wls_list,
                self.ref_index_complex_list,
            ) = self.read_exp_ref_indexes()

            self.exp_if_wls_list, self.exp_if_shifts_list = self.load_exp_data(
                self.__exp_if_shift_dir, self.__if_samples_names
            )
            self.exp_gh_wls_list, self.exp_gh_shifts_list = self.load_exp_data(
                self.__exp_gh_shift_dir, self.__gh_samples_names
            )
            print("Time to load data: ", time.perf_counter() - t1)

            self.if_centers, self.if_inclines = self.centers_of_exp_curve(
                self.exp_if_wls_list, self.exp_if_shifts_list
            )
            self.gh_centers, self.gh_inclines = self.centers_of_exp_curve(
                self.exp_gh_wls_list, self.exp_gh_shifts_list
            )

            self.bg_wls, self.bg_gh, self.bg_if = self.load_bg_if_gh_shift()

            self.if_collections = self.plot_exp_data_in_one_plot()

            ##  Instance parameters
            self.thickness = thickness  #   nm

            self._init_flag = True

        pass

    def __new__(cls, *args, **kwargs):
        if cls._instance == None:
            cls._instance = object.__new__(cls)
            return cls._instance
        else:
            return cls._instance

    @classmethod
    def read_Wu_cond_original_data(cls):
        data = pd.read_csv(cls.__Wu_cond_file_path)
        Wu_wls_original, Wu_energy_original, Wu_real_part, Wu_imag_part = [
            data.iloc[:, i] for i in range(4)
        ]
        Wu_cond_complex = Wu_real_part + 1j * Wu_imag_part

        return Wu_wls_original, Wu_energy_original, Wu_cond_complex

    @classmethod
    def read_exp_ref_indexes(cls):
        """
        From five groups
        """
        wls_list = []
        n_list = []
        k_list = []
        complex_ref_index_list = []
        for ele_name in cls.__refractive_indexes_name:
            ele_data = pd.read_csv(cls.__refractive_indexes_dir + ele_name)
            wls_list.append(array(ele_data["Wavelength, µm"] * 1000))  # nm
            n_list.append(array(ele_data["n"]))  #   dimensionless
            k_list.append(array(ele_data["k"]))  #   dimensionless
            complex_ref_index_list.append(
                array(ele_data["n"] + 1j * ele_data["k"])
            )  #   dimensionless

        return wls_list, complex_ref_index_list

    @staticmethod
    def load_exp_data(exp_dir, exp_names):
        wls_list = []
        shifts_list = []

        for ele_sample in exp_names:
            ele_data = ExcelMethod(exp_dir + ele_sample).read_xlsx_data(0, 0)
            ele_wls, ele_shift = WaveLength().get_sifted_data(ele_data[0], ele_data[3])
            wls_list.append(ele_wls)
            shifts_list.append(ele_shift)

        return wls_list, shifts_list

    @staticmethod
    def centers_of_exp_curve(exp_wls, exp_shifts):
        exp_centers = []
        k_inclines = []
        for ele_i in range(len(exp_wls)):
            ele_wls = exp_wls[ele_i]
            ele_shift = exp_shifts[ele_i]
            ele_center = PlotMethod(ele_wls, ele_shift).center_of_curve()
            exp_centers.append(ele_center)

            k_inclines.append(
                LineFit(ele_wls, ele_shift).fit_through_fixed_point(ele_center)
            )

        return exp_centers, k_inclines

    def load_bg_if_gh_shift(self):
        data_list = ExcelMethod(self._bg_if_gh_data).read_xlsx_data(exclude_rows_num=1)
        wls = data_list[0]
        bg_GH = array(data_list[1]) * 1000
        bg_IF = array(data_list[2]) * 1000

        return wls, bg_GH, bg_IF

    def plot_exp_data_in_one_plot(self):
        if_ybar_list = array(self.if_centers)[:, 1]
        if_mean_ybar = np.mean(if_ybar_list)

        gh_ybar_list = array(self.gh_centers)[:, 1]
        gh_mean_ybar = np.mean(gh_ybar_list)

        shifted_exp_if_collections = [
            array(self.exp_if_shifts_list[ele_i])
            + if_mean_ybar
            - self.if_centers[ele_i][1]
            for ele_i in range(self.sample_num)
        ]

        shifted_exp_gh_collections = [
            array(self.exp_gh_shifts_list[ele_i])
            + gh_mean_ybar
            - self.gh_centers[ele_i][1]
            for ele_i in range(self.sample_num)
        ]

        PlotMethod(
            self.exp_if_wls_list,
            shifted_exp_if_collections,
            r"$\lambda$ (nm)",
            "IF shift (nm)",
            title="Experimental observations of IF shift",
            save_name="if_collection",
            legend=["Sample {}".format(ele_i + 1) for ele_i in range(self.sample_num)],
            save_dir="IF/exp",
            x_lim=[540, 700],
        ).multiple_line_one_plot()

        PlotMethod(
            self.exp_gh_wls_list,
            shifted_exp_gh_collections,
            r"$\lambda$ (nm)",
            "GH shift (nm)",
            title="Experimental observations of GH shift",
            save_name="gh_collection",
            legend=["Sample {}".format(ele_i + 1) for ele_i in range(self.sample_num)],
            save_dir="GH/exp",
            x_lim=[540, 700],
        ).multiple_line_one_plot()

        return shifted_exp_if_collections, shifted_exp_gh_collections


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
        out_result = self.permittivity_infty + lo.complex_result

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
            complex_permittivity_result * omega * thickness / (c_speed * m2nm * 1j)
        )

        return sigma_tilde


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

        n = sqrt(modulus) * cos(half_angle)
        k = sqrt(modulus) * sin(half_angle)

        return n, k


class LorentzFitProcess:
    _base_init_flag = False
    # _instance = None

    _start_wls = 496
    _end_wls = 697

    def __init__(
        self, centers_0, amps_0, gammas_0, bottom_bound, top_bound, incident_angle_0
    ) -> None:
        if self._base_init_flag:
            print("Already exist basic initiation parameters...")
            print("Loading new parameters of centers, amplitudes and gammas")

            return
        else:
            self.BK7_substrate = BK7Substrate()
            self.mos2_data = MoS2Data()

            self._base_init_flag = True

        self.p0 = list(centers_0) + list(amps_0) + list(gammas_0)
        self.lorentz_len = len(centers_0)
        self.bounds_tuple = (bottom_bound, top_bound)
        self.lcp_if = IFCalculation(a_s=1, a_p=1, incident_angles=incident_angle_0)
        self.rcp_if = IFCalculation(
            a_s=1, a_p=1, eta=-pi / 2, incident_angles=incident_angle_0
        )
        self.s_gh = GHCalculation(a_s=1, a_p=0, incident_angles=incident_angle_0)
        self.p_gh = GHCalculation(a_s=0, a_p=1, incident_angles=incident_angle_0)

        self.shift_diff = _EigenShiftDifference(incident_angle_0)

        self.shifted_if_exp_conductivity_based = (
            self.shift_diff.shifted_if_compared_with_theory_conductivity_bg()
        )
        self.shifted_gh_exp_conductivity_based = (
            self.shift_diff.shifted_gh_compared_with_theory_conductivity_bg()
        )

        (
            self.bg_if_permittivity_xbar,
            self.bg_if_permittivity_ybar,
        ) = self.shift_diff.bg_permittivity_lcp_rcp_if_center()
        (
            self.bg_gh_permittivity_xbar,
            self.bg_gh_permittivity_ybar,
        ) = self.shift_diff.bg_permittivity_s_p_gh_center()

        self.shifted_if_exp_permittivity_based = (
            self.shift_diff.shifted_if_compared_with_theory_permittivity_bg()
        )
        self.shifted_gh_exp_permittivity_based = (
            self.shift_diff.shifted_gh_compared_with_theory_permittivity_bg()
        )

        self.theta_0s = incident_angle_0

    # def __new__(cls, *args, **kwargs):
    #     """
    #     Only one instance
    #     """
    #     if cls._instance is None:
    #         print("Creating single object: LorentzFitProcess")
    #         cls._instance = super().__new__(cls)
    #         return cls._instance
    #     else:
    #         return cls._instance

    def __if_shift_conductivity_func(self, energy, *args):
        """
        # Parameters

        energy: unit of meV
        """
        centers, amps, gammas = (
            list(args[0][: self.lorentz_len]),
            list(args[0][self.lorentz_len : self.lorentz_len * 2]),
            list(args[0][self.lorentz_len * 2 : self.lorentz_len * 3]),
        )

        if len(self.theta_0s) > 1:
            raise MultipleIncidentAngles(
                "When fitting experimental IF shift, incident angle should be a list which only contains one incident angle!"
            )

        if_shift = (
            self.rcp_if.lorentz_conductivity_model(
                centers, amps, gammas, energy=energy
            )[1]
            - self.lcp_if.lorentz_conductivity_model(
                centers, amps, gammas, energy=energy
            )[1]
        )

        if_shift = if_shift.reshape((-1,))

        return if_shift

    def __if_shift_permittivity_func(self, energy, *args):
        """
        # Parameters

        energy: unit of meV
        """
        wls = 1240 / energy * 1000  #   nm
        centers, amps, gammas = (
            list(args[0][: self.lorentz_len]),
            list(args[0][self.lorentz_len : self.lorentz_len * 2]),
            list(args[0][self.lorentz_len * 2 : self.lorentz_len * 3]),
        )

        if len(self.theta_0s) > 1:
            raise MultipleIncidentAngles(
                "When fitting experimental IF shift, incident angle should be a list which only contains one incident angle!"
            )

        complex_permittivity = Permittivity(
            self.mos2_data.permittivity_infty
        ).lorentzian_combination_to_perm(energy, centers, amps, gammas)
        complex_refractive_index = ComplexRefractiveIndex(
            complex_permittivity
        ).complex_refractive_index

        if_shift = (
            self.rcp_if.thin_film_model(
                wls, complex_refractive_index, self.mos2_data.thickness
            )[1]
            - self.lcp_if.thin_film_model(
                wls, complex_refractive_index, self.mos2_data.thickness
            )[1]
        )

        # if_shift = self.so.bg_permittivity_lcp_rcp_if()[1]

        if_shift = if_shift.reshape((-1,))

        return if_shift

    def __gh_shift_conductivity_func(self, energy, *args):
        """
        # Parameters

        energy: unit of meV
        """
        centers, amps, gammas = (
            list(args[0][: self.lorentz_len]),
            list(args[0][self.lorentz_len : self.lorentz_len * 2]),
            list(args[0][self.lorentz_len * 2 : self.lorentz_len * 3]),
        )

        if len(self.theta_0s) > 1:
            raise MultipleIncidentAngles(
                "When fitting experimental IF shift, incident angle should be a list which only contains one incident angle!"
            )

        gh_shift = (
            self.p_gh.lorentz_conductivity_model(centers, amps, gammas, energy=energy)[
                1
            ]
            - self.s_gh.lorentz_conductivity_model(
                centers, amps, gammas, energy=energy
            )[1]
        )

        gh_shift = gh_shift.reshape((-1,))

        return gh_shift

    def __gh_shift_permittivity_func(self, energy, *args):
        """
        # Parameters

        energy: unit of meV
        """
        wls = 1240 / energy * 1000  #   nm
        centers, amps, gammas = (
            list(args[0][: self.lorentz_len]),
            list(args[0][self.lorentz_len : self.lorentz_len * 2]),
            list(args[0][self.lorentz_len * 2 : self.lorentz_len * 3]),
        )

        if len(self.theta_0s) > 1:
            raise MultipleIncidentAngles(
                "When fitting experimental IF shift, incident angle should be a list which only contains one incident angle!"
            )

        complex_permittivity = Permittivity(
            self.mos2_data.permittivity_infty
        ).lorentzian_combination_to_perm(energy, centers, amps, gammas)
        complex_refractive_index = ComplexRefractiveIndex(
            complex_permittivity
        ).complex_refractive_index

        gh_shift = (
            self.p_gh.thin_film_model(
                wls, complex_refractive_index, self.mos2_data.thickness
            )[1]
            - self.s_gh.thin_film_model(
                wls, complex_refractive_index, self.mos2_data.thickness
            )[1]
        )

        gh_shift = gh_shift.reshape((-1,))

        return gh_shift

    def if_fit_conductivity_core(self, sample_index):
        """
        Based on the input n0 to fit the parameters

        Index: 0 --- 5
        """
        print("Lorentzian peaks number: ", self.lorentz_len)
        self._find_best_if_theta0(sample_index)
        exp_if_wls = self.mos2_data.exp_if_wls_list[sample_index]
        exp_if_shift = self.shifted_if_exp_conductivity_based[sample_index][0]

        exp_if_energy = 1240 / array(exp_if_wls) * 1000

        popt = curve_fit(
            lambda x, *p0: self.__if_shift_conductivity_func(x, p0),
            exp_if_energy,
            exp_if_shift,
            p0=self.p0,
            bounds=self.bounds_tuple,
            maxfev=50000,
        )[0]

        centers_fit = popt[: self.lorentz_len]
        amps_fit = popt[self.lorentz_len : self.lorentz_len * 2]
        gammas_fit = popt[self.lorentz_len * 2 : self.lorentz_len * 3]

        return centers_fit, amps_fit, gammas_fit

    def if_fit_permittivity_core(self, sample_index):
        """
        Based on the input n0 to fit the parameters

        Index: 0 --- 5
        """
        print("Lorentzian peaks number: ", self.lorentz_len)
        self._find_best_if_theta0(sample_index)
        exp_if_wls = self.mos2_data.exp_if_wls_list[sample_index]
        exp_if_shift = self.shifted_if_exp_permittivity_based[sample_index][0]

        exp_if_energy = 1240 / array(exp_if_wls) * 1000

        popt = curve_fit(
            lambda x, *p0: self.__if_shift_permittivity_func(x, p0),
            exp_if_energy,
            exp_if_shift,
            p0=self.p0,
            bounds=self.bounds_tuple,
            maxfev=50000,
        )[0]

        centers_fit = popt[: self.lorentz_len]
        amps_fit = popt[self.lorentz_len : self.lorentz_len * 2]
        gammas_fit = popt[self.lorentz_len * 2 : self.lorentz_len * 3]

        return centers_fit, amps_fit, gammas_fit

    def gh_fit_conductivity_core(self, sample_index):
        """
        Based on the input n0 to fit the parameters

        Index: 0 --- 5
        """
        print("Lorentzian peaks number: ", self.lorentz_len)
        self._find_best_gh_theta0(sample_index)
        exp_gh_wls = self.mos2_data.exp_gh_wls_list[sample_index]
        exp_gh_shift = self.shifted_gh_exp_conductivity_based[sample_index][0]

        exp_gh_energy = 1240 / array(exp_gh_wls) * 1000

        popt = curve_fit(
            lambda x, *p0: self.__gh_shift_conductivity_func(x, p0),
            exp_gh_energy,
            exp_gh_shift,
            p0=self.p0,
            bounds=self.bounds_tuple,
            maxfev=50000,
        )[0]

        centers_fit = popt[: self.lorentz_len]
        amps_fit = popt[self.lorentz_len : self.lorentz_len * 2]
        gammas_fit = popt[self.lorentz_len * 2 : self.lorentz_len * 3]

        return centers_fit, amps_fit, gammas_fit

    def gh_fit_permittivity_core(self, sample_index):
        """
        Based on the input n0 to fit the parameters

        Index: 0 --- 5
        """
        print("Lorentzian peaks number: ", self.lorentz_len)
        self._find_best_gh_theta0(sample_index)
        exp_gh_wls = self.mos2_data.exp_gh_wls_list[sample_index]
        exp_gh_shift = self.shifted_gh_exp_permittivity_based[sample_index][0]

        exp_gh_energy = 1240 / array(exp_gh_wls) * 1000

        popt = curve_fit(
            lambda x, *p0: self.__gh_shift_permittivity_func(x, p0),
            exp_gh_energy,
            exp_gh_shift,
            p0=self.p0,
            bounds=self.bounds_tuple,
            maxfev=50000,
        )[0]

        centers_fit = popt[: self.lorentz_len]
        amps_fit = popt[self.lorentz_len : self.lorentz_len * 2]
        gammas_fit = popt[self.lorentz_len * 2 : self.lorentz_len * 3]

        return centers_fit, amps_fit, gammas_fit

    def _find_best_if_theta0(self, sample_index):
        angle_list = linspace(43 / 180 * pi, 47 / 180 * pi, 400)
        shift_ob = _EigenShiftDifference(angle_list)
        ##  Incline and intercept of different background line corresponding to different incident angles
        kb_arr = shift_ob.kb_of_lcp_rcp_bg_conductivity_if_shift()

        ##  Functions of the background line
        func_list = [Functions.linear_func_fixed_pars(1, *ele_kb) for ele_kb in kb_arr]

        ##  Standard deviations between background line and the experimental observations (different incident angles)
        std_arr = FitMethod.std_between_two_curves(
            [
                line_func(self.mos2_data.exp_if_wls_list[sample_index])
                for line_func in func_list
            ],
            self.shifted_if_exp_conductivity_based[sample_index][0],
        )

        ##  Find the minimum and get the actual incident angle
        best_angle = list(angle_list)[list(std_arr).index(min(std_arr))]

        print("best if incident angle: ", best_angle / pi * 180)

        return

    def _find_best_gh_theta0(self, sample_index):
        angle_list = linspace(43 / 180 * pi, 47 / 180 * pi, 400)
        shift_diff = _EigenShiftDifference(angle_list)
        ##  Incline and intercept of different background line corresponding to different incident angles
        kb_arr = shift_diff.kb_of_s_p_bg_conductivity_gh_shift()

        ##  Functions of the background line
        func_list = [Functions.linear_func_fixed_pars(1, *ele_kb) for ele_kb in kb_arr]

        ##  Standard deviations between background line and the experimental observations (different incident angles)
        std_arr = FitMethod.std_between_two_curves(
            [
                line_func(self.mos2_data.exp_gh_wls_list[sample_index])
                for line_func in func_list
            ],
            self.shifted_gh_exp_conductivity_based[sample_index][0],
        )

        ##  Find the minimum and get the actual incident angle
        best_angle = list(angle_list)[list(std_arr).index(min(std_arr))]

        print("best gh incident angle: ", best_angle / pi * 180)

        return


class LorentzFitParameters:
    def __init__(
        self,
        bottom_e=1840,
        top_e=2400,
        incident_angles=[pi / 4],
        centers_top_bot_limit_list=None,
        amps_top_bot_limit_list=None,
        gammas_top_bot_limit_list=None,
    ) -> None:
        self.bottom_e = bottom_e
        self.top_e = top_e
        self.centers = arange(bottom_e, top_e, 50)
        self.lorentz_len = len(self.centers)
        self.amps = [0.2] * self.lorentz_len
        self.gammas = [25] * self.lorentz_len

        energy_span = 25
        if centers_top_bot_limit_list is None:
            self._centers_top_limit = [
                ele_center + energy_span for ele_center in self.centers
            ]
            self._centers_bot_limit = [
                ele_center - energy_span for ele_center in self.centers
            ]
        else:
            (
                self._centers_top_limit,
                self._centers_bot_limit,
            ) = centers_top_bot_limit_list
        if amps_top_bot_limit_list is None:
            self._amps_top_limit = [1] * self.lorentz_len
            self._amps_bot_limit = [0.0] * self.lorentz_len
        else:
            self._amps_top_limit, self._amps_bot_limit = amps_top_bot_limit_list
        if gammas_top_bot_limit_list is None:
            self._gamma_top_limit = [150] * self.lorentz_len
            self._gamma_bot_limit = [25] * self.lorentz_len
        else:
            self._gamma_top_limit, self._gamma_bot_limit = gammas_top_bot_limit_list

        self.top_bound = (
            self._centers_top_limit + self._amps_top_limit + self._gamma_top_limit
        )
        self.bot_bound = (
            self._centers_bot_limit + self._amps_bot_limit + self._gamma_bot_limit
        )

        self.theta_0s = incident_angles

    def get_pars(self):
        return (
            self.centers,
            self.amps,
            self.gammas,
            self.bot_bound,
            self.top_bound,
            self.theta_0s,
        )

    def pars_format(self, centers_fit, amps_fit, gammas_fit):
        amplitudes = LorentzOscillator(centers_fit, amps_fit, gammas_fit).amplitudes

        pars_tuples = [
            "({:.2f} meV, {:.2f}, {:.2f} meV)\n".format(
                centers_fit[i], amplitudes[i], gammas_fit[i]
            )
            for i in range(len(centers_fit))
        ]

        out_text = "Parameters: \n(Center, Amplitude, Broadening)\n" + "".join(
            pars_tuples
        )

        return out_text

    def get_optimized_pars(
        self, centers_fixed=[1830, 1922, 2032, 2137, 2200, 2380], interval_lorentz_num=2
    ):
        """
        Get the peaks pre-fixed
        """
        centers_to_add = []
        centers_fixed_span = []
        centers_added_span = []
        for ele_i in range(len(centers_fixed) - 1):
            start_p = centers_fixed[ele_i]
            end_p = centers_fixed[ele_i + 1]

            interval = (end_p - start_p) / (interval_lorentz_num + 1)
            half_interval = interval / 2
            centers_fixed_span = centers_fixed_span + [half_interval] * 2
            centers_added_span = centers_added_span + [half_interval] * 2
            for ele_j in range(interval_lorentz_num):
                centers_to_add.append(start_p + interval * (ele_j + 1))
        centers_fixed_span.pop(-1)

        centers_out = centers_fixed + centers_to_add
        amps = [0.2] * len(centers_out)
        gammas = [25] * len(centers_out)

        centers_span = centers_fixed_span + centers_added_span
        centers_top_limit = [
            centers_out[ele_i] + centers_span[ele_i]
            for ele_i in range(len(centers_out))
        ]
        centers_bot_limit = [
            centers_out[ele_i] - centers_span[ele_i]
            for ele_i in range(len(centers_out))
        ]

        amps_top_limit = [1] * len(centers_out)
        amps_bot_limit = [0.2] * len(centers_fixed) + [0] * len(centers_to_add)

        gamma_top_limit = [150] * len(centers_out)
        gamma_bot_limit = [25] * len(centers_out)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return centers_out, amps, gammas, bot_bound, top_bound, self.theta_0s

    def get_permittivity_pars(self):
        centers = arange(self.bottom_e, self.top_e, 50)
        amps = [2] * self.lorentz_len
        gammas = [25] * self.lorentz_len

        energy_span = 25
        centers_top_limit = [ele_center + energy_span for ele_center in centers]
        centers_bot_limit = [ele_center - energy_span for ele_center in centers]

        amps_top_limit = [5] * self.lorentz_len
        amps_bot_limit = [0] * self.lorentz_len

        gamma_top_limit = [150] * self.lorentz_len
        gamma_bot_limit = [25] * self.lorentz_len

        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit
        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit

        return centers, amps, gammas, bot_bound, top_bound, self.theta_0s

    def get_permittivity_optimized_pars(
        self, centers_fixed=[1830, 1922, 2032, 2137, 2200, 2380], interval_lorentz_num=2
    ):
        """
        Get the peaks pre-fixed
        """
        centers_to_add = []
        centers_fixed_span = []
        centers_added_span = []
        for ele_i in range(len(centers_fixed) - 1):
            start_p = centers_fixed[ele_i]
            end_p = centers_fixed[ele_i + 1]

            interval = (end_p - start_p) / (interval_lorentz_num + 1)
            half_interval = interval / 2
            centers_fixed_span = centers_fixed_span + [half_interval] * 2
            centers_added_span = centers_added_span + [half_interval] * 2
            for ele_j in range(interval_lorentz_num):
                centers_to_add.append(start_p + interval * (ele_j + 1))
        centers_fixed_span.pop(-1)

        centers_out = centers_fixed + centers_to_add
        amps = [2] * len(centers_out)
        gammas = [25] * len(centers_out)

        centers_span = centers_fixed_span + centers_added_span
        centers_top_limit = [
            centers_out[ele_i] + centers_span[ele_i]
            for ele_i in range(len(centers_out))
        ]
        centers_bot_limit = [
            centers_out[ele_i] - centers_span[ele_i]
            for ele_i in range(len(centers_out))
        ]

        amps_top_limit = [5] * len(centers_out)
        amps_bot_limit = [2] * len(centers_fixed) + [0] * len(centers_to_add)

        gamma_top_limit = [150] * len(centers_out)
        gamma_bot_limit = [25] * len(centers_out)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return centers_out, amps, gammas, bot_bound, top_bound, self.theta_0s


class IFCalculation:
    """
    Used to calculate IF shift based on thin-film model and conductivity model.
    """

    def __init__(self, a_s, a_p, incident_angles=[pi / 4], eta=pi / 2) -> None:
        """
        eta is the phase difference between two component of the electric field
        """
        if not (
            isinstance(incident_angles, list) or isinstance(incident_angles, np.ndarray)
        ):
            raise IncidentAngleNotAList(
                "Incident angle should be closed in a list so that you can use multiple incident angles to get multiple results for different angles"
            )

        self.BK7_substrate = BK7Substrate()
        self.mos2_data = MoS2Data()

        self.theta_0s = incident_angles
        self.a_s = a_s
        self.a_p = a_p
        self.eta = eta

        pass

    def thin_film_model(self, wavelengths, n1_index, thickness):
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
        n0_index = self.BK7_substrate.function_n0_wls(IF_wls)

        ##  Wavevector
        k0, IF_wls_mat = WaveLength.get_wave_vector_mat(
            IF_wls, n0_index, len(self.theta_0s)
        )[:2]

        r_s, r_p = FresnelCoefficients(
            IF_wls, self.theta_0s, n0_index, [1]
        ).thin_film_model(n1_index, thickness)

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

    def conductivity_model(self, wavelengths, sigma):
        """
        Note the sigma here is dimensionless conductivity
        """
        ##  Sift data into the range we want
        IF_wls, sigma = WaveLength().get_sifted_data(wavelengths, sigma)
        ##  interpolate the refractive indexes of substrate
        n0_index = self.BK7_substrate.function_n0_wls(IF_wls)

        ##  Wavevector
        k0_mat, IF_wls_mat = WaveLength.get_wave_vector_mat(
            IF_wls, n0_index, len(self.theta_0s)
        )[:2]

        r_s, r_p = FresnelCoefficients(
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
        save_dir=None,
        title="",
    ):
        if legend is None:
            legend = [
                "${:.2f}\degree$".format(ele_theta / pi * 180) for ele_theta in theta_0s
            ]
        if save_dir is None:
            save_dir = "IF"
        else:
            save_dir = "IF/" + save_dir
        if save_type == "plot":
            if text is None:
                raise TypeError(
                    "Please input the text and the text_xy when you set text_annotate as True"
                )
            PlotMethod(
                if_wls_list,
                if_shifts_list,
                "$\lambda$ (nm)",
                "IF shift (nm)",
                title,
                save_name,
                save_dir=save_dir,
                legend=legend,
                text=text,
                text_xy=text_xy,
            ).multiple_line_one_plot(text_annotate=text_annotate)
        elif save_type == "html":
            HtmlPlotMethod(
                if_wls_list,
                if_shifts_list,
                "$\lambda$ (nm)",
                "IF shift (nm)",
                title,
                save_name,
                save_dir=save_dir,
                legend=legend,
            ).multiple_line_one_plot()
        return

    def lorentz_conductivity_model(self, centers, amps, gammas, energy=None):
        """
        Use conductivity model to calculate IF shift

        Input energy should be in the unit of meV

        # Return
        if_wls, if_shift
        """
        if energy is None:
            sigma = LorentzOscillator(
                centers, amps, gammas, self.BK7_substrate.dense_energy, times_i=True
            ).lorentz_result()

            lorentz_if_wls, lorentz_if_shift = self.conductivity_model(
                self.BK7_substrate.dense_wls, sigma
            )
        else:
            sigma = LorentzOscillator(
                centers, amps, gammas, energy, times_i=True
            ).lorentz_result()

            lorentz_if_wls, lorentz_if_shift = self.conductivity_model(
                1240 / energy * 1000, sigma
            )

        return lorentz_if_wls, lorentz_if_shift

    def bg_conductivity_shift(self):
        wls, n0 = WaveLength().get_sifted_data(
            self.BK7_substrate.dense_wls, self.BK7_substrate.dense_n0_index
        )
        r_s, r_p = FresnelCoefficients(
            wls, self.theta_0s, n0, [1]
        ).original_coefficient()

        k0, IF_wls_mat = WaveLength.get_wave_vector_mat(wls, n0, len(self.theta_0s))[:2]
        theta_0s_mat = WaveLength.get_theta_0s_mat(self.theta_0s, len(wls))

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        phi_s = np.angle(r_s)  # Angle of rs and rp
        phi_p = np.angle(r_p)  # Angle of rs and rp

        w_s, w_p = Wsp(R_s, R_p, self.a_s, self.a_p).calculate()

        Delta_IF = (
            -1
            / (k0 * np.tan(theta_0s_mat))
            * (
                (w_p * self.a_s**2 + w_s * self.a_p**2)
                / (self.a_p * self.a_s)
                * sin(self.eta)
                + 2 * sqrt(w_p * w_s) * sin(self.eta - phi_p + phi_s)
            )
        )

        return IF_wls_mat, real(Delta_IF)

    def bg_permittivity_shift(self):
        """
        Calculate Background shift based on permittivity model
        """
        wls = WaveLength().get_sifted_data(
            self.BK7_substrate.dense_wls, self.BK7_substrate.dense_n0_index
        )[0]
        n1_index = [sqrt(self.mos2_data.permittivity_infty)] * len(wls)

        IF_wls_mat, Delta_IF = self.thin_film_model(
            wls, array(n1_index), self.mos2_data.thickness
        )

        return IF_wls_mat, Delta_IF


class GHCalculation:
    def __init__(
        self, a_s, a_p, scan_angle_density=500, incident_angles=[pi / 4]
    ) -> None:
        if not (
            isinstance(incident_angles, list) or isinstance(incident_angles, np.ndarray)
        ):
            raise IncidentAngleNotAList(
                "Incident angle should be closed in a list so that you can use multiple incident angles to get multiple results for different angles"
            )

        self.BK7_substrate = BK7Substrate()
        self.mos2_data = MoS2Data()

        self.scan_angle_list = linspace(
            42 / 180 * pi, 48 / 180 * pi, scan_angle_density
        )

        self.theta_0s = incident_angles
        self.a_s = a_s
        self.a_p = a_p

        self.start_wls = 496
        self.end_wls = 697

        pass

    def thin_film_model(self, wavelengths, n1_index, thickness):
        """
        Get GH shift from thin-film model
        """
        ##  Sift data into the range we want
        boolean_arr = np.logical_and(
            wavelengths > self.start_wls, wavelengths < self.end_wls
        )
        GH_wls = wavelengths[boolean_arr]
        ##  interpolate the refractive indexes of substrate
        n0_index = self.BK7_substrate.function_n0_wls(GH_wls)

        ##  Select n1_index on the chosen wavelength range
        n1_index = n1_index[boolean_arr]

        n0_index_mat = np.kron(ones((len(self.theta_0s), 1)), n0_index)
        GH_wls_mat = np.kron(ones((len(self.theta_0s), 1)), GH_wls)

        k0 = 2 * pi * n0_index / GH_wls

        fc = FresnelCoefficients(GH_wls, self.scan_angle_list, n0_index, n2_index=[1])

        r_s, r_p = fc.thin_film_model(n1_index, thickness)
        func_phis_der, func_phip_der = fc.der_phi_s_p_func(r_s, r_p)

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        w_s_func, w_p_func = Wsp(R_s, R_p, self.a_s, self.a_p).interpolate_along_row(
            self.scan_angle_list
        )

        Delta_GH = array(
            [
                (
                    w_s_func(incident_angle) * func_phis_der(incident_angle)
                    + w_p_func(incident_angle) * func_phip_der(incident_angle)
                )
                / k0
                for incident_angle in self.theta_0s
            ]
        )

        return GH_wls_mat, real(Delta_GH)

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
        save_dir=None,
        title="",
    ):
        if legend is None:
            legend = [
                "${:.2f}\degree$".format(ele_theta / pi * 180) for ele_theta in theta_0s
            ]
        if save_dir is None:
            save_dir = "GH"
        else:
            save_dir = "GH/" + save_dir

        PlotMethod(
            gh_wls_list,
            gh_shifts_list,
            "$\lambda$ (nm)",
            "GH shift (nm)",
            title,
            save_name,
            save_dir=save_dir,
            legend=legend,
            text=text,
            text_xy=text_xy,
        ).multiple_line_one_plot(text_annotate=text_annotate)

    def conductivity_model(self, wavelengths, sigma):
        """
        Get GH shift based on the conductivity model
        """
        ##  Sift data into the range we want
        boolean_arr = np.logical_and(
            wavelengths > self.start_wls, wavelengths < self.end_wls
        )
        GH_wls = wavelengths[boolean_arr]
        n0_index = self.BK7_substrate.function_n0_wls(GH_wls)
        sigma = sigma[boolean_arr]

        n0_index_mat = np.kron(ones((len(self.theta_0s), 1)), n0_index)
        GH_wls_mat = np.kron(ones((len(self.theta_0s), 1)), GH_wls)

        k0 = 2 * pi * n0_index / GH_wls

        fc = FresnelCoefficients(GH_wls, self.scan_angle_list, n0_index, n2_index=[1])

        r_s, r_p = fc.conductivity_model(sigma)
        func_phis_der, func_phip_der = fc.der_phi_s_p_func(r_s, r_p)

        R_s = abs(r_s)  # Amplitude of rs and rp
        R_p = abs(r_p)  # Amplitude of rs and rp
        w_s_func, w_p_func = Wsp(R_s, R_p, self.a_s, self.a_p).interpolate_along_row(
            self.scan_angle_list
        )

        Delta_GH = array(
            [
                (
                    w_s_func(incident_angle) * func_phis_der(incident_angle)
                    + w_p_func(incident_angle) * func_phip_der(incident_angle)
                )
                / k0
                for incident_angle in self.theta_0s
            ]
        )

        return GH_wls_mat, real(Delta_GH)

    def lorentz_conductivity_model(self, centers, amps, gammas, energy=None):
        """
        Use lorentz conductivity model to calculate GH shift

        Input energy should be in the unit of meV

        # Return
        gh_wls, gh_shift
        """
        if energy is None:
            sigma = LorentzOscillator(
                centers, amps, gammas, self.BK7_substrate.dense_energy, times_i=True
            ).lorentz_result()

            lorentz_gh_wls, lorentz_gh_shift = self.conductivity_model(
                self.BK7_substrate.dense_wls, sigma
            )
        else:
            sigma = LorentzOscillator(
                centers, amps, gammas, energy, times_i=True
            ).lorentz_result()

            lorentz_gh_wls, lorentz_gh_shift = self.conductivity_model(
                1240 / energy * 1000, sigma
            )

        return lorentz_gh_wls, lorentz_gh_shift

    def bg_conductivity_shift(self):
        gh_wls, gh_shift = self.lorentz_conductivity_model([2000], [0], [100])

        return gh_wls, gh_shift

    def bg_permittivity_shift(self):
        """
        Calculate Background shift based on permittivity model
        """
        wls = WaveLength().get_sifted_data(
            self.BK7_substrate.dense_wls, self.BK7_substrate.dense_n0_index
        )[0]
        n1_index = [sqrt(self.mos2_data.permittivity_infty)] * len(wls)

        GH_wls_mat, Delta_GH = self.thin_film_model(
            wls, array(n1_index), self.mos2_data.thickness
        )

        return GH_wls_mat, Delta_GH


class _EigenShiftDifference:
    def __init__(self, incident_angles=[pi / 4]) -> None:
        self.theta_0s = incident_angles

        self.mos2_data = MoS2Data()

        pass

    def lcp_rcp_if_object(self):
        lcp = IFCalculation(a_s=1, a_p=1, incident_angles=self.theta_0s)
        rcp = IFCalculation(a_s=1, a_p=1, eta=-pi / 2, incident_angles=self.theta_0s)
        return lcp, rcp

    def s_p_gh_object(self):
        s = GHCalculation(a_s=1, a_p=0, incident_angles=self.theta_0s)
        p = GHCalculation(a_s=0, a_p=1, incident_angles=self.theta_0s)
        return s, p

    def lcp_rcp_if_thin_film(self, wavelengths, n1_index, thickness):
        lcp, rcp = self.lcp_rcp_if_object()
        lcp_if_wls, lcp_if_shift = lcp.thin_film_model(wavelengths, n1_index, thickness)
        rcp_if_shift = rcp.thin_film_model(wavelengths, n1_index, thickness)[1]

        return lcp_if_wls, rcp_if_shift - lcp_if_shift

    def lcp_rcp_if_lorentz_conductivity(self, centers, amps, gammas):
        lcp, rcp = self.lcp_rcp_if_object()
        lcp_if_wls, lcp_if_shift = lcp.lorentz_conductivity_model(centers, amps, gammas)
        rcp_if_shift = rcp.lorentz_conductivity_model(centers, amps, gammas)[1]

        return lcp_if_wls, rcp_if_shift - lcp_if_shift

    def s_p_gh_thin_film(self, wavelengths, n1_index, thickness):
        """
        Calculate GH shift based on thin-film model
        """
        s, p = self.s_p_gh_object()
        s_gh_wls, s_gh_shift = s.thin_film_model(wavelengths, n1_index, thickness)
        p_gh_shift = p.thin_film_model(wavelengths, n1_index, thickness)[1]

        return s_gh_wls, p_gh_shift - s_gh_shift

    def s_p_gh_lorentz_conductivity(self, centers, amps, gammas):
        """
        Calculate GH shift based on thin-film model

        # Return
        s_gh_wls, p_gh_shift - s_gh_shift
        """
        s, p = self.s_p_gh_object()
        s_gh_wls, s_gh_shift = s.lorentz_conductivity_model(centers, amps, gammas)
        p_gh_shift = p.lorentz_conductivity_model(centers, amps, gammas)[1]

        return s_gh_wls, p_gh_shift - s_gh_shift

    def bg_conductivity_lcp_rcp_if(self):
        """
        Calculate the incline of the line when there is no Lorentzian peaks in conductivity, which is, the original Fresnel coefficient

        # Return
        rcp_wls, rcp_shift - lcp_shift
        """

        lcp_if, rcp_if = self.lcp_rcp_if_object()

        rcp_wls, rcp_shift = rcp_if.bg_conductivity_shift()
        lcp_shift = lcp_if.bg_conductivity_shift()[1]

        return rcp_wls, rcp_shift - lcp_shift

    def bg_permittivity_lcp_rcp_if(self):
        """
        Calculate the incline of the line when there is no Lorentzian peaks in conductivity, which is, the original Fresnel coefficient

        # Return
        rcp_wls, rcp_shift - lcp_shift
        """

        lcp_if, rcp_if = self.lcp_rcp_if_object()

        rcp_wls, rcp_shift = rcp_if.bg_permittivity_shift()
        lcp_shift = lcp_if.bg_permittivity_shift()[1]

        return rcp_wls, rcp_shift - lcp_shift

    def bg_permittivity_lcp_rcp_if_center(self):
        bg_wls, bg_shift = self.bg_permittivity_lcp_rcp_if()

        bg_xbar, bg_ybar = PlotMethod(bg_wls[0], bg_shift[0]).center_of_curve()

        return bg_xbar, bg_ybar

    def bg_conductivity_s_p_gh(self):
        """
        Calculate the incline of the line when there is no Lorentzian peaks in conductivity, which is, the original Fresnel coefficient

        # Return
        s_wls, p_shift - s_shift
        """

        s, p = self.s_p_gh_object()

        s_wls, s_shift = s.bg_conductivity_shift()
        p_shift = p.bg_conductivity_shift()[1]

        return s_wls, p_shift - s_shift

    def bg_permittivity_s_p_gh(self):
        """
        Calculate the incline of the line when there is no Lorentzian peaks in conductivity, which is, the original Fresnel coefficient

        # Return
        s_wls, p_shift - s_shift
        """

        s, p = self.s_p_gh_object()

        s_wls, s_shift = s.bg_permittivity_shift()
        p_shift = p.bg_permittivity_shift()[1]

        return s_wls, p_shift - s_shift

    def bg_permittivity_s_p_gh_center(self):
        bg_wls, bg_shift = self.bg_permittivity_s_p_gh()

        bg_xbar, bg_ybar = PlotMethod(bg_wls[0], bg_shift[0]).center_of_curve()

        return bg_xbar, bg_ybar

    def kb_of_lcp_rcp_bg_conductivity_if_shift(self):
        """
        Calculate the IF shift background of difference between lcp and rcp.
        """
        wls, shift_difference = self.bg_conductivity_lcp_rcp_if()
        linear_f = Functions.linear_func(1)
        popt_list = [
            curve_fit(linear_f, wls[ele_i], shift_difference[ele_i], p0=[1, 0])[0]
            for ele_i in range(len(wls))
        ]

        return popt_list

    def kb_of_s_p_bg_conductivity_gh_shift(self):
        """
        Calculate the IF shift background of difference between lcp and rcp.
        """
        wls, shift_difference = self.bg_conductivity_s_p_gh()
        linear_f = Functions.linear_func(1)
        popt_list = [
            curve_fit(linear_f, wls[ele_i], shift_difference[ele_i], p0=[-1, 0])[0]
            for ele_i in range(len(wls))
        ]

        return popt_list

    def shifted_if_compared_with_theory_conductivity_bg(self):
        """
        Shift the whole experimental result to bring it near the background if shift

        The bg if shift is the difference between rcp and lcp

        # Return
        Return the list which contains six sublists corresponding to six samples. Within each sublist, there are multiple list which correspond to different incident angles

        """
        # if len(self.theta_0s) > 1:
        #     raise MultipleIncidentAngles("To use this function, the incident angle list should only contain one incident angle.")

        popt_par_list = self.kb_of_lcp_rcp_bg_conductivity_if_shift()

        func_list = [
            Functions.linear_func_fixed_pars(1, *ele_pair) for ele_pair in popt_par_list
        ]

        shifts_list = []
        for ele_i in range(len(self.mos2_data.if_centers)):
            if_x = self.mos2_data.if_centers[ele_i][0]
            if_y = self.mos2_data.if_centers[ele_i][1]

            shifted_exp_if = [
                self.mos2_data.exp_if_shifts_list[ele_i] + ele_func(if_x) - if_y
                for ele_func in func_list
            ]
            shifts_list.append(shifted_exp_if)

        return shifts_list

    def shifted_if_compared_with_theory_permittivity_bg(self):
        """
        Shift the whole experimental result to bring it near the background if shift

        The bg if shift is the difference between rcp and lcp

        # Return
        Return the list which contains six sublists corresponding to six samples. Within each sublist, there are multiple list which correspond to different incident angles

        """
        # if len(self.theta_0s) > 1:
        #     raise MultipleIncidentAngles("To use this function, the incident angle list should only contain one incident angle.")
        bg_if_center_y = self.bg_permittivity_lcp_rcp_if_center()[1]

        shifts_list = []
        for ele_i in range(len(self.mos2_data.if_centers)):
            if_y = self.mos2_data.if_centers[ele_i][1]

            shifted_exp_if = [
                self.mos2_data.exp_if_shifts_list[ele_i] + bg_if_center_y - if_y
            ]
            shifts_list.append(shifted_exp_if)

        return shifts_list

    def shifted_gh_compared_with_theory_conductivity_bg(self):
        """
        Shift the whole experimental result to bring it near the background if shift

        The bg if shift is the difference between rcp and lcp

        # Return
        Return the list which contains six sublists corresponding to six samples. Within each sublist, there are multiple list which correspond to different incident angles

        """
        # if len(self.theta_0s) > 1:
        #     raise MultipleIncidentAngles("To use this function, the incident angle list should only contain one incident angle.")

        popt_par_list = self.kb_of_s_p_bg_conductivity_gh_shift()

        func_list = [
            Functions.linear_func_fixed_pars(1, *ele_pair) for ele_pair in popt_par_list
        ]

        shifts_list = []
        for ele_sample_i in range(len(self.mos2_data.gh_centers)):
            gh_x = self.mos2_data.gh_centers[ele_sample_i][0]
            gh_y = self.mos2_data.gh_centers[ele_sample_i][1]

            shifted_exp_if = [
                self.mos2_data.exp_gh_shifts_list[ele_sample_i] + ele_func(gh_x) - gh_y
                for ele_func in func_list
            ]
            shifts_list.append(shifted_exp_if)

        return shifts_list

    def shifted_gh_compared_with_theory_permittivity_bg(self):
        """
        Shift the whole experimental result to bring it near the background if shift

        The bg if shift is the difference between rcp and lcp

        # Return
        Return the list which contains six sublists corresponding to six samples. Within each sublist, there are multiple list which correspond to different incident angles

        """
        # if len(self.theta_0s) > 1:
        #     raise MultipleIncidentAngles("To use this function, the incident angle list should only contain one incident angle.")

        bg_gh_center_y = self.bg_permittivity_s_p_gh_center()[1]

        shifts_list = []
        for ele_sample_i in range(len(self.mos2_data.gh_centers)):
            gh_y = self.mos2_data.gh_centers[ele_sample_i][1]

            shifted_exp_if = [
                self.mos2_data.exp_gh_shifts_list[ele_sample_i] + bg_gh_center_y - gh_y
            ]
            shifts_list.append(shifted_exp_if)

        return shifts_list


class ParameterPerturbation:
    def __init__(
        self, a_sp_pairs, incident_angle=[pi / 4], eta=[pi / 2, -pi / 2]
    ) -> None:
        self.a_sp_pairs = a_sp_pairs
        # self.phase_list = phase
        self.theta_0 = incident_angle
        self.eta_list = eta
        pass

    def polarization_perturb(self, centers, amps, gammas):
        """
        Calculate GH shift based on different polarization
        """
        eigen_wls, eigen_shifts = _EigenShiftDifference().s_p_gh_lorentz_conductivity(
            centers, amps, gammas
        )

        gh_1 = GHCalculation(*self.a_sp_pairs[0])
        gh_2 = GHCalculation(*self.a_sp_pairs[1])

        gh_wls, gh_shift_1 = gh_1.lorentz_conductivity_model(centers, amps, gammas)
        gh_shift_2 = gh_2.lorentz_conductivity_model(centers, amps, gammas)[1]

        difference = gh_shift_2 - gh_shift_1
        difference = difference[0] - max(difference[0])

        eigen_shifts = eigen_shifts[0] - max(eigen_shifts[0])

        PlotMethod(
            [eigen_wls[0], gh_wls[0]],
            [eigen_shifts, difference],
            r"$\lambda$ (nm)",
            r"GH shift (nm)",
            "Shifted GH for $a_s/a_p={}:{}$ and $a_s/a_p={}:{}$".format(
                *self.a_sp_pairs[0], *self.a_sp_pairs[1]
            ),
            save_name="{}_{}_{}_{}".format(*self.a_sp_pairs[0], *self.a_sp_pairs[1]),
            save_dir="GH/PolarizationVaried",
            legend=["standard s-p", "deviated polarization"],
        ).multiple_line_one_plot()

        return gh_wls, gh_shift_1

    def theta0_perturbation_gh(self, centers, amps, gammas, suffix_name=""):
        """
        Adjust the incident angle and see the perturbation
        """
        eigen_wls, eigen_shifts = _EigenShiftDifference().s_p_gh_lorentz_conductivity(
            centers, amps, gammas
        )
        bg_wls, bg_shift = _EigenShiftDifference().bg_conductivity_s_p_gh()
        gh_1 = GHCalculation(*self.a_sp_pairs[0], incident_angles=self.theta_0)
        gh_2 = GHCalculation(*self.a_sp_pairs[1], incident_angles=self.theta_0)

        exp_gh_wls = MoS2Data().exp_gh_wls_list[1]
        exp_gh_shift = MoS2Data().exp_gh_shifts_list[1]

        gh_wls, gh_shift_1 = gh_1.lorentz_conductivity_model(centers, amps, gammas)
        gh_shift_2 = gh_2.lorentz_conductivity_model(centers, amps, gammas)[1]

        difference = gh_shift_2 - gh_shift_1
        difference = difference[0] - max(difference[0]) - 10

        eigen_shifts = eigen_shifts[0] - max(eigen_shifts[0])

        bg_shift = bg_shift[0] - max(bg_shift[0])

        exp_gh_shift = exp_gh_shift - max(exp_gh_shift) - 10

        PlotMethod(
            [bg_wls[0], eigen_wls[0], gh_wls[0], exp_gh_wls],
            [bg_shift, eigen_shifts, difference, exp_gh_shift],
            r"$\lambda$ (nm)",
            r"GH shift (nm)",
            r"Shifted GH for $\theta_0={:.2f}\degree$".format(
                self.theta_0[0] / pi * 180
            ),
            save_name="theta0_{:.2f}".format(self.theta_0[0] / pi * 180) + suffix_name,
            save_dir="GH/Theta0Varied",
            legend=["Background", "$45\degree$", r"deviated $\theta_0$", "Experiment"],
        ).multiple_line_one_plot()

        HtmlPlotMethod(
            [bg_wls[0], eigen_wls[0], gh_wls[0], exp_gh_wls],
            [bg_shift, eigen_shifts, difference, exp_gh_shift],
            r"$\lambda$ (nm)",
            r"GH shift (nm)",
            r"Shifted GH for $\theta_0={:.2f}\degree$".format(
                self.theta_0[0] / pi * 180
            ),
            save_name="theta0_{:.2f}".format(self.theta_0[0] / pi * 180) + suffix_name,
            save_dir="GH/Theta0Varied",
            legend=["Background", "$45\degree$", r"deviated $\theta_0$", "Experiment"],
        ).multiple_line_one_plot()

    def theta0_perturbation_if(self, centers, amps, gammas, suffix_name=""):
        """
        Adjust the incident angle and see the perturbation
        """
        (
            eigen_wls,
            eigen_shifts,
        ) = _EigenShiftDifference().lcp_rcp_if_lorentz_conductivity(
            centers, amps, gammas
        )
        bg_wls, bg_shift = _EigenShiftDifference().bg_conductivity_lcp_rcp_if()
        if_1 = IFCalculation(
            *self.a_sp_pairs[0], incident_angles=self.theta_0, eta=self.eta_list[0]
        )
        if_2 = IFCalculation(
            *self.a_sp_pairs[1], incident_angles=self.theta_0, eta=self.eta_list[1]
        )

        exp_if_wls = MoS2Data().exp_if_wls_list[1]
        exp_if_shift = MoS2Data().exp_if_shifts_list[1]

        if_wls, if_shift_1 = if_1.lorentz_conductivity_model(centers, amps, gammas)
        if_shift_2 = if_2.lorentz_conductivity_model(centers, amps, gammas)[1]

        difference = if_shift_2 - if_shift_1
        difference = difference[0] - min(difference[0])

        eigen_shifts = eigen_shifts[0] - min(eigen_shifts[0])

        bg_shift = bg_shift[0] - min(bg_shift[0])

        exp_if_shift = exp_if_shift - min(exp_if_shift)

        PlotMethod(
            [bg_wls[0], eigen_wls[0], if_wls[0], exp_if_wls],
            [bg_shift, eigen_shifts, difference, exp_if_shift],
            r"$\lambda$ (nm)",
            r"GH shift (nm)",
            r"Shifted IF for $\theta_0={:.2f}\degree$".format(
                self.theta_0[0] / pi * 180
            ),
            save_name="theta0_{:.2f}".format(self.theta_0[0] / pi * 180) + suffix_name,
            save_dir="IF/Theta0Varied",
            legend=["Background", "$45\degree$", r"deviated $\theta_0$", "Experiment"],
        ).multiple_line_one_plot()

        HtmlPlotMethod(
            [bg_wls[0], eigen_wls[0], if_wls[0], exp_if_wls],
            [bg_shift, eigen_shifts, difference, exp_if_shift],
            r"$\lambda$ (nm)",
            r"GH shift (nm)",
            r"Shifted IF for $\theta_0={:.2f}\degree$".format(
                self.theta_0[0] / pi * 180
            ),
            save_name="theta0_{:.2f}".format(self.theta_0[0] / pi * 180) + suffix_name,
            save_dir="IF/Theta0Varied",
            legend=["Background", "$45\degree$", r"deviated $\theta_0$", "Experiment"],
        ).multiple_line_one_plot()


class FitCore:
    _fit_file_path = data_file_dir + "FitFiles/"

    def __init__(self, incident_angles=None, pars_type="default") -> None:
        if incident_angles is None:
            incident_angles = [pi / 4]
        self.theta_0s = incident_angles

        self.shift_object = _EigenShiftDifference(self.theta_0s)

        if pars_type == "optimized":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters().get_optimized_pars()
            )
        elif pars_type == "default":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters().get_pars()
            )
        elif pars_type == "permittivity":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters().get_permittivity_pars()
            )
        elif pars_type == "permittivity_optimized":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters().get_permittivity_optimized_pars()
            )

        self.data_mos2 = MoS2Data()
        pass

    def _save_fit_pars(self, centers, amps, gammas, save_name):
        """
        Save the fitted parameters
        """
        pars = array([centers, amps, gammas])

        np.save(self._fit_file_path + save_name, pars)

        return

    def _load_fit_pars(self, save_name):
        """
        Load the fit parameters
        """
        out_load = np.load(self._fit_file_path + save_name)
        centers, amps, gammas = [out_load[ele_i, :] for ele_i in range(3)]

        return centers, amps, gammas

    def fit_if_exp_conductivity_based(self, sample_index, save_name, update=False):
        """
        Fit Experimental IF shift
        """
        ##  Fitted parameters
        file_name = save_name + "_{}".format(sample_index)
        if update or (not os.path.exists(self._fit_file_path + file_name + ".npy")):
            print("New calculation: ", save_name)
            (
                centers_fit,
                amps_fit,
                gammas_fit,
            ) = self.lorentz_fit_process.if_fit_conductivity_core(sample_index)
            self._save_fit_pars(centers_fit, amps_fit, gammas_fit, save_name=file_name)

        else:
            print("Fit done before.")
            centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        annotation_text = LorentzFitParameters().pars_format(
            centers_fit, amps_fit, gammas_fit
        )

        LorentzOscillator(
            centers_fit,
            amps_fit,
            gammas_fit,
            linspace(1500, 2500, 400),
            times_i=True,
            x_label="E (meV)",
            y_label=r"$\sigma/\varepsilon_0 c$",
        ).lorentz_plot(
            save_name="{}_sample_{}".format(save_name, sample_index), save_dir="fit"
        )

        if_wls, if_shift = self.shift_object.lcp_rcp_if_lorentz_conductivity(
            centers_fit, amps_fit, gammas_fit
        )

        IFCalculation.post_treatment(
            [if_wls[0], self.data_mos2.exp_if_wls_list[sample_index]],
            [
                if_shift[0],
                self.lorentz_fit_process.shifted_if_exp_conductivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitIF_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        ##  Plot GH shift based on the fitted parameters
        gh_wls, gh_shift = self.shift_object.s_p_gh_lorentz_conductivity(
            centers_fit, amps_fit, gammas_fit
        )

        GHCalculation.post_treatment(
            [gh_wls[0], self.data_mos2.exp_gh_wls_list[sample_index]],
            [
                gh_shift[0],
                self.lorentz_fit_process.shifted_gh_exp_conductivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitGH_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        return

    def fit_gh_exp_conductivity_based(self, sample_index, save_name, update=False):
        """
        Fit Experimental IF shift
        """
        ##  Fitted parameters
        file_name = save_name + "_{}".format(sample_index)
        if update or (not os.path.exists(self._fit_file_path + file_name + ".npy")):
            print("New calculation.")
            (
                centers_fit,
                amps_fit,
                gammas_fit,
            ) = self.lorentz_fit_process.gh_fit_conductivity_core(sample_index)
            self._save_fit_pars(centers_fit, amps_fit, gammas_fit, save_name=file_name)

        else:
            print("Fit done before.")
            centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        annotation_text = LorentzFitParameters().pars_format(
            centers_fit, amps_fit, gammas_fit
        )

        LorentzOscillator(
            centers_fit,
            amps_fit,
            gammas_fit,
            linspace(1500, 2500, 400),
            times_i=True,
            x_label="E (meV)",
            y_label=r"$\sigma/\varepsilon_0 c$",
        ).lorentz_plot(
            save_name="{}_sample_{}".format(save_name, sample_index), save_dir="fit"
        )

        ##  Calculate IF shift based on fitted parameters
        if_wls, if_shift = self.shift_object.lcp_rcp_if_lorentz_conductivity(
            centers_fit, amps_fit, gammas_fit
        )

        IFCalculation.post_treatment(
            [if_wls[0], self.data_mos2.exp_if_wls_list[sample_index]],
            [
                if_shift[0],
                self.lorentz_fit_process.shifted_if_exp_conductivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitIF_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        ##  Plot GH shift based on the fitted parameters
        gh_wls, gh_shift = self.shift_object.s_p_gh_lorentz_conductivity(
            centers_fit, amps_fit, gammas_fit
        )

        GHCalculation.post_treatment(
            [gh_wls[0], self.data_mos2.exp_gh_wls_list[sample_index]],
            [
                gh_shift[0],
                self.lorentz_fit_process.shifted_gh_exp_conductivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitGH_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        return

    def fit_if_exp_permittivity_based(self, sample_index, save_name, update=False):
        """
        Fit Experimental IF shift
        """
        ##  Fitted parameters
        file_name = save_name + "_{}".format(sample_index)
        if update or (not os.path.exists(self._fit_file_path + file_name + ".npy")):
            print("New calculation.")
            (
                centers_fit,
                amps_fit,
                gammas_fit,
            ) = self.lorentz_fit_process.if_fit_permittivity_core(sample_index)
            self._save_fit_pars(centers_fit, amps_fit, gammas_fit, save_name=file_name)

        else:
            print("Fit done before.")
            centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        annotation_text = LorentzFitParameters().pars_format(
            centers_fit, amps_fit, gammas_fit
        )

        E_fit_range = linspace(1500, 2500, 400)
        wls_fit_range = 1240 / E_fit_range * 1000

        LorentzOscillator(
            centers_fit,
            amps_fit,
            gammas_fit,
            E_fit_range,
            times_i=True,
            x_label="E (meV)",
            y_label=r"$\sigma/\varepsilon_0 c$",
        ).lorentz_plot(
            save_name="{}_sample_{}".format(save_name, sample_index), save_dir="fit"
        )

        complex_refractive_index_fit = ComplexRefractiveIndex(
            Permittivity(
                self.data_mos2.permittivity_infty
            ).lorentzian_combination_to_perm(
                linspace(1500, 2500, 400), centers_fit, amps_fit, gammas_fit
            )
        ).complex_refractive_index

        if_wls, if_shift = self.shift_object.lcp_rcp_if_thin_film(
            wls_fit_range, complex_refractive_index_fit, self.data_mos2.thickness
        )

        IFCalculation.post_treatment(
            [if_wls[0], self.data_mos2.exp_if_wls_list[sample_index]],
            [
                if_shift[0],
                self.lorentz_fit_process.shifted_if_exp_permittivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitIF_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        ##  Plot GH shift based on the fitted parameters
        gh_wls, gh_shift = self.shift_object.s_p_gh_thin_film(
            wls_fit_range, complex_refractive_index_fit, self.data_mos2.thickness
        )

        GHCalculation.post_treatment(
            [gh_wls[0], self.data_mos2.exp_gh_wls_list[sample_index]],
            [
                gh_shift[0],
                self.lorentz_fit_process.shifted_gh_exp_permittivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitGH_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        return

    def fit_gh_exp_permittivity_based(self, sample_index, save_name, update=False):
        """
        Fit Experimental IF shift
        """
        ##  Fitted parameters
        file_name = save_name + "_{}".format(sample_index)
        if update or (not os.path.exists(self._fit_file_path + file_name + ".npy")):
            print("New calculation.")
            (
                centers_fit,
                amps_fit,
                gammas_fit,
            ) = self.lorentz_fit_process.gh_fit_permittivity_core(sample_index)
            self._save_fit_pars(centers_fit, amps_fit, gammas_fit, save_name=file_name)

        else:
            print("Fit done before.")
            centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        annotation_text = LorentzFitParameters().pars_format(
            centers_fit, amps_fit, gammas_fit
        )

        E_fit_range = linspace(1500, 2500, 400)
        wls_fit_range = 1240 / E_fit_range * 1000

        LorentzOscillator(
            centers_fit,
            amps_fit,
            gammas_fit,
            E_fit_range,
            times_i=True,
            x_label="E (meV)",
            y_label=r"$\sigma/\varepsilon_0 c$",
        ).lorentz_plot(
            save_name="{}_sample_{}".format(save_name, sample_index), save_dir="fit"
        )

        complex_refractive_index_fit = ComplexRefractiveIndex(
            Permittivity(
                self.data_mos2.permittivity_infty
            ).lorentzian_combination_to_perm(
                linspace(1500, 2500, 400), centers_fit, amps_fit, gammas_fit
            )
        ).complex_refractive_index

        ##  Calculate IF shift based on fitted parameters
        if_wls, if_shift = self.shift_object.lcp_rcp_if_thin_film(
            wls_fit_range, complex_refractive_index_fit, self.data_mos2.thickness
        )

        IFCalculation.post_treatment(
            [if_wls[0], self.data_mos2.exp_if_wls_list[sample_index]],
            [
                if_shift[0],
                self.lorentz_fit_process.shifted_if_exp_permittivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitIF_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        ##  Plot GH shift based on the fitted parameters
        gh_wls, gh_shift = self.shift_object.s_p_gh_thin_film(
            wls_fit_range, complex_refractive_index_fit, self.data_mos2.thickness
        )

        GHCalculation.post_treatment(
            [gh_wls[0], self.data_mos2.exp_gh_wls_list[sample_index]],
            [
                gh_shift[0],
                self.lorentz_fit_process.shifted_gh_exp_permittivity_based[
                    sample_index
                ][0],
            ],
            theta_0s=self.theta_0s,
            save_name="{}_fitGH_sample_{}".format(save_name, sample_index),
            legend=["Theoretical Fit", "Experimental result"],
            text=annotation_text,
            text_xy=(1.01, 0),
            text_annotate=True,
            save_dir="fit",
            title="Sample {}".format(sample_index + 1),
        )

        return

    def collect_fit_conductivities_cond_based(
        self,
        prefix_name,
        num_files,
        save_name,
        y_label_list=[
            r"$\rm{Re}[\sigma/\varepsilon_0 c]$",
            r"$\rm{Im}[\sigma/\varepsilon_0 c]$",
        ],
        save_dir="Conductivity",
    ):
        """
        Plot all the fitted conductivities together
        """
        real_part = []
        imag_part = []
        for ele_i in range(num_files):
            ele_file = prefix_name + "_{}.npy".format(ele_i)
            centers, amps, gammas = self._load_fit_pars(ele_file)
            real_part.append(
                LorentzOscillator(
                    centers,
                    amps,
                    gammas,
                    linspace(1500, 2500, 400),
                    times_i=True,
                    x_label="E (meV)",
                    y_label=y_label_list[0],
                ).real_part
            )
            imag_part.append(
                LorentzOscillator(
                    centers,
                    amps,
                    gammas,
                    linspace(1500, 2500, 400),
                    times_i=True,
                    x_label="E (meV)",
                    y_label=y_label_list[1],
                ).imag_part
            )
        PlotMethod(
            [linspace(1500, 2500, 400)] * num_files,
            real_part,
            x_label="E (meV)",
            y_label=y_label_list[0],
            title=r"Real part of fitted conductivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_real",
            save_dir=save_dir,
        ).multiple_line_one_plot()
        PlotMethod(
            [linspace(1500, 2500, 400)] * num_files,
            imag_part,
            x_label="E (meV)",
            y_label=y_label_list[1],
            title=r"Imaginary part of fitted conductivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_imag",
            save_dir=save_dir,
        ).multiple_line_one_plot()

        return

    def collect_fit_conductivities_permi_based(self, prefix_name, num_files, save_name):
        """
        Plot all the fitted conductivities together
        """
        real_part_sigma = []
        imag_part_sigma = []
        n_list = []
        k_list = []
        perm_real_list = []
        perm_imag_list = []
        energy_range = linspace(1500, 2500, 400)
        for ele_i in range(num_files):
            ele_file = prefix_name + "_{}.npy".format(ele_i)
            centers, amps, gammas = self._load_fit_pars(ele_file)

            perm_ob = Permittivity(self.data_mos2.permittivity_infty)
            sigma_tilde = perm_ob.lorentz_combi_to_sigma_2d(
                energy_range, centers, amps, gammas, self.data_mos2.thickness
            )
            ref_index_ob = ComplexRefractiveIndex(
                perm_ob.lorentzian_combination_to_perm(
                    energy_range, centers, amps, gammas
                )
            )

            real_part_sigma.append(real(sigma_tilde))
            imag_part_sigma.append(imag(sigma_tilde))

            n_list.append(real(ref_index_ob.complex_refractive_index))
            k_list.append(imag(ref_index_ob.complex_refractive_index))

            perm_real_list.append(real(ref_index_ob.complex_permittivity))
            perm_imag_list.append(imag(ref_index_ob.complex_permittivity))

        PlotMethod(
            [energy_range] * num_files,
            real_part_sigma,
            x_label="E (meV)",
            y_label=r"$\rm{Re}[\sigma/\varepsilon_0 c]$",
            title=r"Real part of fitted conductivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_real",
            save_dir="Conductivity",
        ).multiple_line_one_plot()
        PlotMethod(
            [energy_range] * num_files,
            imag_part_sigma,
            x_label="E (meV)",
            y_label=r"$\rm{Im}[\sigma/\varepsilon_0 c]$",
            title=r"Imaginary part of fitted conductivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_imag",
            save_dir="Conductivity",
        ).multiple_line_one_plot()

        PlotMethod(
            [energy_range] * num_files,
            perm_real_list,
            x_label="E (meV)",
            y_label=r"$\rm{Re}[\varepsilon]$",
            title=r"Real part of fitted Permittivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_real",
            save_dir="Permittivity",
        ).multiple_line_one_plot()
        PlotMethod(
            [energy_range] * num_files,
            perm_imag_list,
            x_label="E (meV)",
            y_label=r"$\rm{Im}[\varepsilon]$",
            title=r"Imaginary part of fitted Permittivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_imag",
            save_dir="Permittivity",
        ).multiple_line_one_plot()

        PlotMethod(
            [energy_range] * num_files,
            n_list,
            x_label="E (meV)",
            y_label=r"$n$",
            title=r"Real part of complex refractive index",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name,
            save_dir="Complex_n_k/n",
        ).multiple_line_one_plot()
        PlotMethod(
            [energy_range] * num_files,
            k_list,
            x_label="E (meV)",
            y_label=r"$k$",
            title=r"Imaginary part of complex refractive index",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name,
            save_dir="Complex_n_k/k",
        ).multiple_line_one_plot()

        return

    def get_fitted_pars(self, save_name, sample_index):
        file_name = save_name + "_{}".format(sample_index)
        centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        return centers_fit, amps_fit, gammas_fit


class FitExperimentExecution:
    def __init__(self, name="") -> None:
        self.name = name
        pass

    @staticmethod
    def if_based_optimized_fit_conductivity_based(update=False, name="OptimizedFit"):
        """
        Launch fit based on IF shift
        """
        fit_funcs = FitCore(pars_type="optimized")
        for i in range(5):
            fit_funcs.fit_if_exp_conductivity_based(i, save_name=name, update=update)
        fit_funcs.collect_fit_conductivities_cond_based(name, 5, name)
        return

    @staticmethod
    def gh_based_fit_conductivity_based(update=False, name="OptimizedFitGHBased"):
        """
        Launch fit based on IF shift
        """
        fit_funcs = FitCore(pars_type="default")
        for i in range(5):
            fit_funcs.fit_gh_exp_conductivity_based(i, save_name=name, update=update)
        fit_funcs.collect_fit_conductivities_cond_based(name, 5, name)
        return

    @staticmethod
    def if_based_fit_permittivity_based(
        update=False, name="PermittivityFit", pars_type="permittivity"
    ):
        """
        Launch fit based on IF shift
        """
        fit_funcs = FitCore(pars_type=pars_type)
        for i in range(5):
            fit_funcs.fit_if_exp_permittivity_based(i, save_name=name, update=update)
        fit_funcs.collect_fit_conductivities_permi_based(name, 5, name)
        return

    @staticmethod
    def if_based_optimized_fit_permittivity_based(
        update=False,
        name="PermittivityOptimizedFit",
        pars_type="permittivity_optimized",
    ):
        """
        Launch fit based on IF shift
        """
        fit_funcs = FitCore(pars_type=pars_type)
        for i in range(5):
            fit_funcs.fit_if_exp_permittivity_based(i, save_name=name, update=update)
        fit_funcs.collect_fit_conductivities_permi_based(name, 5, name)
        return

    @staticmethod
    def gh_based_fit_permittivity_based(update=False, name="PermittivityFitGHBased"):
        """
        Launch fit based on IF shift
        """
        fit_funcs = FitCore(pars_type="permittivity")
        for i in range(5):
            fit_funcs.fit_gh_exp_permittivity_based(i, save_name=name, update=update)
        fit_funcs.collect_fit_conductivities_permi_based(name, 5, name)
        return

    @staticmethod
    def comp_perm_if_gh(name="PermittivityFitGHBased"):
        """
        Launch fit based on IF shift
        """

        fit_funcs = FitCore(pars_type="permittivity")
        for i in range(1):
            fit_funcs.fit_gh_exp_permittivity_based(i, save_name=name)
        fit_funcs.collect_fit_conductivities_permi_based(name, 5, name)
        return


class CompareLorentzianPeaks(FitCore):
    def __init__(self, incident_angles=[pi / 4], pars_type="default") -> None:
        super().__init__(incident_angles, pars_type)

    def compare_lorentz_pars(self, save_name):
        """
        Compare centers and gammas as x and y
        """
        centers_list = []
        gammas_list = []
        for ele_i in range(self.sample_num):
            centers, amps, gammas = self.get_fitted_pars(save_name, ele_i)
            centers_list.append(centers)
            gammas_list.append(gammas)

        PlotMethod(
            centers_list,
            gammas_list,
            "E (meV)",
            r"$\gamma$ (meV)",
            "Lorentzian Subpeaks Distribution",
            save_name="{}_sub_lorentz_2".format(save_name),
            legend=["Sample {}".format(ele_i + 1) for ele_i in range(self.sample_num)],
            save_dir="Lorentz/SubCompare",
        ).multiple_scatter_one_plot()

        return

    def compare_conductivity_across_model(
        self,
        sample_indexes,
        model_1_name="PermittivityOptimizedFit",
        model_2_name="PermittivityFitGHBased",
        save_name="model_comparison",
    ):
        """
        compare the conductivity from different model
        """

        traces_list = []
        for ele_sample_i in sample_indexes:
            ele_centers_1, ele_amps_1, ele_gammas_1 = self.get_fitted_pars(
                model_1_name, ele_sample_i
            )
            ele_centers_2, ele_amps_2, ele_gammas_2 = self.get_fitted_pars(
                model_2_name, ele_sample_i
            )

            perm_ob_1 = Permittivity(self.data_mos2.permittivity_infty)
            cond1 = perm_ob_1.lorentz_combi_to_sigma_2d(
                linspace(1500, 2500, 400),
                ele_centers_1,
                ele_amps_1,
                ele_gammas_1,
                thickness=self.data_mos2.thickness,
            )

            perm_ob_2 = Permittivity(self.data_mos2.permittivity_infty)
            cond2 = perm_ob_2.lorentz_combi_to_sigma_2d(
                linspace(1500, 2500, 400),
                ele_centers_2,
                ele_amps_2,
                ele_gammas_2,
                thickness=self.data_mos2.thickness,
            )
            traces_list.append(real(cond1))
            traces_list.append(real(cond2))
        legs_list = [
            "{} Sample {}".format(model_1_name, ele_i) for ele_i in sample_indexes
        ] + ["{} Sample {}".format(model_2_name, ele_i) for ele_i in sample_indexes]

        PlotMethod(
            [linspace(1500, 2500, 400)] * len(traces_list),
            traces_list,
            "E (meV)",
            r"$\mathrm{Re}[\sigma/\varepsilon_0 c]$",
            "Comparison {} v.s. {}".format(model_1_name, model_2_name),
            save_name=save_name,
            legend=legs_list,
            save_dir="Conductivity/ModelCompare",
        ).multiple_line_one_plot()

        return


class PSHE:
    def __init__(self) -> None:
        pass


    @staticmethod
    def get_gh_shift_ref_index(wave_lengths, n0_index, n1_index, n2_index=1, theta_0=pi/4, thickness_of_n1=0.8, start_wls=496):
        """
        # n0 index is the substrate index
        # n1 index is the indices of MoS2 or other materials
        """
        ##  Theta and angle list
        theta_list = linspace(1 / 180 * pi, pi / 2, 500)
        angle_list = theta_list / pi * 180

        ##  Incident angle
        angle_theta_0 = theta_0 / pi * 180

        phi_s_list = []
        phi_p_list = []

        ##  Wavelength in n0 medium
        k_0 = 2 * pi * array(n0_index) / array(wave_lengths)

        for ele_theta in theta_list:

            theta_1 = arcsin(array(n0_index) * sin(ele_theta) / array(n1_index))  # the refractive angle in MoS2
            theta_2 = conj(arcsin(array(n0_index) * sin(ele_theta) / n2_index))  # the refractive angle in air

            k = 2 * pi / array(wave_lengths)  # the wave vector in MoS2

            delta_phase = 2j * k * array(n1_index) * thickness_of_n1 * cos(theta_1) # The light path in MoS2
            phase_factor = exp(delta_phase) # The phase factor of light path in MoS2

            r1s = -sin(ele_theta - theta_1) / sin(ele_theta + theta_1)
            r2s = -sin(theta_1 - theta_2) / (sin(theta_1 + theta_2))
            r1p = np.tan(ele_theta - theta_1) / np.tan(ele_theta + theta_1)
            r2p = np.tan(theta_1 - theta_2) / np.tan(theta_1 + theta_2)

            r_s = (r1s + r2s * phase_factor) / (1 + r1s * r2s * phase_factor)
            r_p = (r1p + r2p * phase_factor) / (1 + r1p * r2p * phase_factor)

            Ang_rs = np.angle(r_s)  # Angle of rs and rp
            Ang_rp = np.angle(r_p)  # Angle of rs and rp

            phi_s_list.append(Ang_rs)  #   extract the phase of rs and rp
            phi_p_list.append(Ang_rp)  #   extract the phase of rs and rp

        ##  get the differential of rs and rp with respect to the incident angles
        diff_inci_angle = np.diff(theta_list)
        rs_phi_deriv_theta0_list = []
        rp_phi_deriv_theta0_list = []

        for ele_phi_rs_rp_vs_angle_index in range(array(phi_s_list).shape[1]):
            ele_rs_angle = array(phi_s_list)[:, ele_phi_rs_rp_vs_angle_index]    # extract every column data from rs angle
            ele_rp_angle = array(phi_p_list)[:, ele_phi_rs_rp_vs_angle_index]    # extract every column data from rp angle
            ele_diff_rs = np.diff(ele_rs_angle) # diff rs phi vs angle
            ele_diff_rp = np.diff(ele_rp_angle) # diff rp phi vs angle
            ele_deriv_rs = ele_diff_rs / diff_inci_angle    # get the derivative of rs phi
            ele_deriv_rp = ele_diff_rp / diff_inci_angle    # get the derivative of rp phi
            f_rs_phi_deriv = interpolate.interp1d(angle_list[:-1], ele_deriv_rs) # interpolate function of rs der
            f_rp_phi_deriv = interpolate.interp1d(angle_list[:-1], ele_deriv_rp) # interpolate function of rp der
            rs_phi_deriv_theta0_list.append(f_rs_phi_deriv(angle_theta_0))
            rp_phi_deriv_theta0_list.append(f_rp_phi_deriv(angle_theta_0))
        GH_shift = - (array(rs_phi_deriv_theta0_list) - array(rp_phi_deriv_theta0_list)) / k_0

        GH_shift = real(GH_shift)[wave_lengths > start_wls]
        wave_lengths = wave_lengths[wave_lengths > start_wls]

        return GH_shift, wave_lengths

    @staticmethod
    def get_if_shift_ref_index(wave_lengths, n0_index, n1_index, n2_index=1, theta_0=pi/4, thickness_of_n1=0.8, start_wls=496):
        """
        ## n0_index is the substrate index
        ## n1_index is the complex refractive indices of MoS2 or other materials
        """
        # # n0_index is the substrate index
        # # n1_index is the indices of MoS2 or other materials
        k_0 = 2 * pi * array(n0_index) / array(wave_lengths)
        theta_1 = arcsin(array(n0_index) * sin(theta_0) / array(n1_index))  # the refractive angle in MoS2
        theta_2 = conj(arcsin(array(n0_index) * sin(theta_0) / n2_index))  # the refractive angle in air
        k = 2 * pi / array(wave_lengths)  # the wave vector in MoS2
        delta_phase = 2j * k * array(n1_index) * thickness_of_n1 * cos(theta_1)
        phase_factor = exp(delta_phase)
        r1s = -sin(theta_0 - theta_1) / sin(theta_0 + theta_1)
        r2s = -sin(theta_1 - theta_2) / (sin(theta_1 + theta_2))
        r1p = np.tan(theta_0 - theta_1) / np.tan(theta_0 + theta_1)
        r2p = np.tan(theta_1 - theta_2) / np.tan(theta_1 + theta_2)
        r_s = (r1s + r2s * phase_factor) / (1 + r1s * r2s * phase_factor)
        r_p = (r1p + r2p * phase_factor) / (1 + r1p * r2p * phase_factor)
        Amp_rs = abs(r_s)  # Amplitude of rs and rp
        Amp_rp = abs(r_p)  # Amplitude of rs and rp
        Ang_rs = np.angle(r_s)  # Angle of rs and rp
        Ang_rp = np.angle(r_p)  # Angle of rs and rp
        Delta_IF = 1 / (k_0 * np.tan(theta_0)) * (1 + 2 * Amp_rs * Amp_rp / (Amp_rs ** 2 + Amp_rp ** 2) * cos(Ang_rp - Ang_rs))

        Delta_IF = 2 * abs(Delta_IF)

        Delta_IF = Delta_IF[wave_lengths > start_wls]
        wave_lengths = wave_lengths[wave_lengths > start_wls]

        return Delta_IF, wave_lengths

    @staticmethod
    def graphene_cond_analytic(energy_range, mu=100):
        """
        # energy_range: (meV)
        The energy range of photon energy, should be single value or array  of energy.

        # mu:
        chemical potential (meV)
        The unit of conductivity is sigma / (epsilon_0 * c) after times the renormalized constant (which is e^2/(4 pi alpha hbar))

        # return:
        Omega_range, gra_cond
        """
        renormalized_constant = pi * alpha_fsc
        Omega_range = energy_range / mu
        gra_cond = np.heaviside(Omega_range - 2, 0.5) + 1j * (4 / (pi * Omega_range) - 1 / pi * np.log(abs((Omega_range + 2) / (Omega_range - 2))))
        return Omega_range, gra_cond * renormalized_constant

    @staticmethod
    def rs_rp_from_cond(n0_index, cond, n2_index=1, theta_0=pi/4):
        """

        # n0 index
        is the refractive index of the medium where light incident from.
        n0 index should be a list of data over wavelength or a single value. Here, n0 is the BK-7
        # n2 index
        is the refractive index of the medium where light goes into.
        n2 index should be a list of data over wavelength or a single value when you investigate the variation of r_s and r_p over different photon energy. Here n2 is the air.
        # cond:
        Conductivity of the material, must be complex, could be an array over wavelength or a single value

        # return:
        rs, rp

        """
        ##  This corresponds to single incident angle over fixed wavelength range for n0, n2 and cond
        situation1 = isinstance(theta_0, float) or isinstance(theta_0, int)
        ##  This corresponds to a list of incident angle but for fixed n0, n2 and cond
        situation2 = (not isinstance(theta_0, float) and len(theta_0) != 1) and (isinstance(n2_index, float) or isinstance(n2_index, int)) and (isinstance(n0_index, float) or isinstance(n0_index, int)) and (isinstance(cond, complex) or isinstance(cond, float) or isinstance(cond, int))


        if situation1:
            ##  calculation of rs for single n0_index
            numerator_rs = n0_index * cos(theta_0) - np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) - cond
            denominat_rs = n0_index * cos(theta_0) + np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond
            r_s = numerator_rs / denominat_rs

            ##  calculation of rp for single n0_index
            numerator_rp = n2_index ** 2 * cos(theta_0) - n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
            denominat_rp = n2_index ** 2 * cos(theta_0) + n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
            r_p = numerator_rp / denominat_rp


        elif (not isinstance(theta_0, float) and len(theta_0) != 1) and (not isinstance(cond, complex) and len(cond) != 1):
            ##  Scan the incident angle over fixed wavelength for n0, n2 and conductivity
            ##  Judge which is air index
            if isinstance(n0_index, float) or isinstance(n0_index, int):
                n0_index = [n0_index] * len(n2_index)
            elif isinstance(n2_index, float) or isinstance(n2_index, int):
                n2_index = [n2_index] * len(n0_index)

            ##  Get n0, n2, cond in matrix form
            n0_mat = [list(n0_index)] * len(theta_0)
            n0_mat = array(n0_mat)
            n2_mat = [list(n2_index)] * len(theta_0)
            n2_mat = array(n2_mat)
            cond_mat = [list(cond)] * len(theta_0)
            cond_mat = array(cond_mat)
            cos_array = cos(array(theta_0).reshape((len(theta_0), -1)))
            sin_array = sin(array(theta_0).reshape((len(theta_0), -1)))

            numerator_rs = n0_mat * cos_array - np.emath.sqrt(n2_mat ** 2 - n0_mat ** 2 * sin_array ** 2) - cond_mat
            denominat_rs = n0_mat * cos_array + np.emath.sqrt(n2_mat ** 2 - n0_mat ** 2 * sin_array ** 2) + cond_mat
            r_s = numerator_rs / denominat_rs

            numerator_rp = n2_mat ** 2 * cos_array - n0_mat * np.emath.sqrt(n2_mat ** 2 - n0_mat ** 2 * sin_array ** 2) + cond_mat * cos_array * np.emath.sqrt(n2_mat ** 2 - n0_mat ** 2 * sin_array ** 2)
            denominat_rp = n2_mat ** 2 * cos_array + n0_mat * np.emath.sqrt(n2_mat ** 2 - n0_mat ** 2 * sin_array ** 2) + cond_mat * cos_array * np.emath.sqrt(n2_mat ** 2 - n0_mat ** 2 * sin_array ** 2)
            r_p = numerator_rp / denominat_rp


        elif situation2:
            ##  Scan the incident angle for fixed n0, n2 and conductivity
            # print("Scan the incident angle for fixed n0, n2 and conductivity")

            ##  calculation of rs for single n0_index over theta list. This returns a list
            numerator_rs = n0_index * cos(theta_0) - np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) - cond
            denominat_rs = n0_index * cos(theta_0) + np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond
            r_s = numerator_rs / denominat_rs

            ##  calculation of rp for single n0_index over that list. This returns a list
            numerator_rp = n2_index ** 2 * cos(theta_0) - n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
            denominat_rp = n2_index ** 2 * cos(theta_0) + n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
            r_p = numerator_rp / denominat_rp

        #region
        # if (type(n0_index) == int or type(n0_index) == float) and (type(n2_index) == int or type(n2_index) == float):
        #     ##  calculation of rs for single n0_index
        #     numerator_rs = n0_index * cos(theta_0) - np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) - cond
        #     denominat_rs = n0_index * cos(theta_0) + np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond
        #     r_s = numerator_rs / denominat_rs

        #     ##  calculation of rp for single n0_index
        #     numerator_rp = n2_index ** 2 * cos(theta_0) - n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        #     denominat_rp = n2_index ** 2 * cos(theta_0) + n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        #     r_p = numerator_rp / denominat_rp
        # elif (type(n0_index) != int and type(n0_index) != float) and len(n0_index) != 1 and (type(n2_index) == int or type(n2_index) == float):
        #     ##  Then it means the variation of rs and rp are over wavelength. Meanwhile, the conductivity is over wavelength
        #     r_s = []
        #     r_p = []
        #     for ele_n0_i in range(len(n0_index)):
        #         ##  calculation of rs for single n0_index[n0_index[ele_n0_i]_i]
        #         numerator_rs = n0_index[ele_n0_i] * cos(theta_0) - np.emath.sqrt(n2_index ** 2 - n0_index[ele_n0_i] ** 2 * sin(theta_0) ** 2) - cond[ele_n0_i]
        #         denominat_rs = n0_index[ele_n0_i] * cos(theta_0) + np.emath.sqrt(n2_index ** 2 - n0_index[ele_n0_i] ** 2 * sin(theta_0) ** 2) + cond[ele_n0_i]
        #         ele_rs = numerator_rs / denominat_rs

        #         ##  calculation of rp for single n0_index[ele_n0_i]
        #         numerator_rp = n2_index ** 2 * cos(theta_0) - n0_index[ele_n0_i] * np.emath.sqrt(n2_index ** 2 - n0_index[ele_n0_i] ** 2 * sin(theta_0) ** 2) + cond[ele_n0_i] * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index[ele_n0_i] ** 2 * sin(theta_0) ** 2)
        #         denominat_rp = n2_index ** 2 * cos(theta_0) + n0_index[ele_n0_i] * np.emath.sqrt(n2_index ** 2 - n0_index[ele_n0_i] ** 2 * sin(theta_0) ** 2) + cond[ele_n0_i] * cos(theta_0) * np.emath.sqrt(n2_index ** 2 - n0_index[ele_n0_i] ** 2 * sin(theta_0) ** 2)
        #         ele_rp = numerator_rp / denominat_rp

        #         ##  Output of rs and rp
        #         r_s.append(ele_rs)
        #         r_p.append(ele_rp)
        # elif (type(n2_index) != int and type(n2_index) != float) and len(n2_index) != 1 and (type(n0_index) == int or type(n0_index) == float):
        #     ##  Then it means the variation of rs and rp are over wavelength. Meanwhile, the conductivity is over wavelength
        #     r_s = []
        #     r_p = []
        #     for ele_n2_i in range(len(n2_index)):
        #         ##  calculation of rs for single n0_index[n0_index_i]
        #         numerator_rs = n0_index * cos(theta_0) - np.emath.sqrt(n2_index[ele_n2_i] ** 2 - n0_index ** 2 * sin(theta_0) ** 2) - cond[ele_n2_i]
        #         denominat_rs = n0_index * cos(theta_0) + np.emath.sqrt(n2_index[ele_n2_i] ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond[ele_n2_i]
        #         ele_rs = numerator_rs / denominat_rs

        #         ##  calculation of rp for single n0_index
        #         numerator_rp = n2_index[ele_n2_i] ** 2 * cos(theta_0) - n0_index * np.emath.sqrt(n2_index[ele_n2_i] ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond[ele_n2_i] * cos(theta_0) * np.emath.sqrt(n2_index[ele_n2_i] ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        #         denominat_rp = n2_index[ele_n2_i] ** 2 * cos(theta_0) + n0_index * np.emath.sqrt(n2_index[ele_n2_i] ** 2 - n0_index ** 2 * sin(theta_0) ** 2) + cond[ele_n2_i] * cos(theta_0) * np.emath.sqrt(n2_index[ele_n2_i] ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        #         ele_rp = numerator_rp / denominat_rp

        #         ##  Output of rs and rp
        #         r_s.append(ele_rs)
        #         r_p.append(ele_rp)
        #endregion

        return r_s, r_p


    @staticmethod
    def rs_rp_between_two_medium(n0_index, n2_index, theta_0=pi/4):
        ##  calculation of rs
        numerator_rs = n0_index * cos(theta_0) - np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        denominat_rs = n0_index * cos(theta_0) + np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        r_s = numerator_rs / denominat_rs

        ##  calculation of rp
        numerator_rp = n2_index ** 2 * cos(theta_0) - n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        denominat_rp = n2_index ** 2 * cos(theta_0) + n0_index * np.emath.sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        r_p = numerator_rp / denominat_rp

        return r_s, r_p


    @staticmethod
    def get_if_shift_cond_over_wl(wave_lengths, n0_index, cond, n2_index=1, theta_0=pi/4):
        """
        # wave_lengths:
        the wavelength we investigate
        # n0_index:
        the index of the incoming medium
        # n2_index:
        the index of the outgoing medium
        # theta_0:
        the incident angle
        # return:
        IF shift over wavelength
        """
        ##  rs, rp and k0
        r_s, r_p = PSHE.rs_rp_from_cond(n0_index, cond, n2_index=n2_index, theta_0=theta_0)
        k_0 = 2 * pi * array(n0_index) / array(wave_lengths)

        ##  amplitude and angle of rs and rp
        Amp_rs = [abs(ele_rs) for ele_rs in r_s]
        Amp_rp = [abs(ele_rp) for ele_rp in r_p]
        Ang_rs = [np.angle(ele_rs) for ele_rs in r_s]
        Ang_rp = [np.angle(ele_rp) for ele_rp in r_p]

        ##  Turn all amplitudes and angles into array
        Amp_rs = array(Amp_rs)
        Amp_rp = array(Amp_rp)
        Ang_rs = array(Ang_rs)
        Ang_rp = array(Ang_rp)

        ##  express the IF shift
        Delta_IF = 1 / (k_0 * np.tan(theta_0)) * (1 + 2 * Amp_rs * Amp_rp / (Amp_rs ** 2 + Amp_rp ** 2) * cos(Ang_rp - Ang_rs))

        return 2 * abs(Delta_IF)

    @staticmethod
    def w_sp(Amp_rs, Amp_rp, a_s, a_p):
        """
        # Amp_rs, Amp_rp
        The amplitude of r_s and r_p
        # a_s, a_p
        The component of two polarization
        # return:
        w_s, w_p
        """

        w_s = a_s ** 2 * Amp_rs ** 2 / (a_p ** 2 * Amp_rp ** 2 + a_s ** 2 * Amp_rs ** 2)
        w_p = a_p ** 2 * Amp_rp ** 2 / (a_p ** 2 * Amp_rp ** 2 + a_s ** 2 * Amp_rs ** 2)

        return w_s, w_p

    @staticmethod
    def get_if_shift_cond_no_wl(n0_index, cond, n2_index=1, theta_0=pi/4, a_s=1, a_p=1, eta_phase=pi/2):
        """
        # wave_lengths:
        the wavelength we investigate
        # n0_index:
        the index of the incoming medium
        # n2_index:
        the index of the outgoing medium
        # theta_0:
        the incident angle
        # return:
        IF shift over wavelength
        # note!
        this function only considers one part of the IF shift (for lcp or rcp only)
        """
        ##  rs, rp and k0
        r_s, r_p = PSHE.rs_rp_from_cond(n0_index, cond, n2_index=n2_index, theta_0=theta_0)

        ##  amplitude and angle of rs and rp
        Amp_rs = np.abs(r_s)
        Amp_rp = np.abs(r_p)
        Ang_rs = np.angle(r_s)
        Ang_rp = np.angle(r_p)

        ##  get w_s and w_p
        w_s, w_p = PSHE.w_sp(Amp_rs, Amp_rp, a_s, a_p)

        ##  express the IF shift
        Delta_IF = 1 / np.tan(theta_0) * (1 + 2 * Amp_rs * Amp_rp / (Amp_rs ** 2 + Amp_rp ** 2) * cos(Ang_rp - Ang_rs))

        ##  express the IF shift
        coeff1 = (w_p * a_s ** 2 + w_s * a_p ** 2) / (a_p * a_s) * sin(eta_phase)
        coeff2 = 2 * np.sqrt(w_p * w_s) * sin(eta_phase - Ang_rp + Ang_rs)
        Delta_IF = 1 / np.tan(theta_0) * (coeff1 + coeff2)

        return -abs(Delta_IF)

    @staticmethod
    def get_gh_func_from_cond_over_wl(n0_index, cond, n2_index=1):
        """
        This function is used to get the interpolated function for a range of wavelength

        No incident angles are needed because we already did the incident angles scan

        # return
        deriv_rs_angle_f, deriv_rp_angle_f
        """
        ##  situation: corresponds to the n0 and n2 over wavelength


        ##  Theta list and angle list
        theta_list = linspace(0, pi / 2, 500)
        angle_list = theta_list / pi * 180

        ##  input theta list into to get rs and rp from conductivity
        rs_mat, rp_mat = PSHE.rs_rp_from_cond(n0_index, cond, n2_index=n2_index, theta_0=theta_list)
        ##  Angle of rs and rp
        Ang_rs = np.angle(rs_mat)
        Ang_rp = np.angle(rp_mat)
        ##  difference of rs and rp angle
        diff_inci_angle = np.diff(theta_list)
        diff_rs_angle = np.diff(Ang_rs, axis=0)
        diff_rp_angle = np.diff(Ang_rp, axis=0)
        ##  get the derivative of rs and rp angle
        deriv_rs_angle = diff_rs_angle / diff_inci_angle.reshape((-1, 1))
        deriv_rp_angle = diff_rp_angle / diff_inci_angle.reshape((-1, 1))
        ##  get the interpolated function based on the derivative. These functions take in the incident angle and spit out the derivative of rs or rp angle under the wavelength.
        deriv_rs_func_list = [interpolate.interp1d(theta_list[:-1], deriv_rs_angle[:, col_i]) for col_i in range(deriv_rs_angle.shape[1])]
        deriv_rp_func_list = [interpolate.interp1d(theta_list[:-1], deriv_rp_angle[:, col_i]) for col_i in range(deriv_rp_angle.shape[1])]

        def deriv_rs_angle_f(theta_in):
            der_over_wl = [ele_func(theta_in) for ele_func in deriv_rs_func_list]
            return array(der_over_wl)

        def deriv_rp_angle_f(theta_in):
            der_over_wl = [ele_func(theta_in) for ele_func in deriv_rp_func_list]
            return array(der_over_wl)

        return deriv_rs_angle_f, deriv_rp_angle_f

    @staticmethod
    def get_gh_func_from_cond_no_wl(n0_index, cond, n2_index=1, sample_points=1000):
        """
        Get the interpolated function for single n0, n2 and cond but for a range of incident angles
        # return

        """
        ##  situation: corresponds to single n0, n2 and conductivity

        ##  Theta list and angle list
        theta_list = linspace(0, pi / 2, sample_points)
        angle_list = theta_list / pi * 180

        ##  input theta list into to get rs and rp from conductivity
        rs_list, rp_list = PSHE.rs_rp_from_cond(n0_index, cond, n2_index=n2_index, theta_0=theta_list)
        ##  Angle of rs and rp
        Ang_rs = np.angle(rs_list)
        Ang_rp = np.angle(rp_list)
        ##  difference of rs and rp angle
        diff_inci_angle = np.diff(theta_list)
        diff_rs_angle = np.diff(Ang_rs)
        diff_rp_angle = np.diff(Ang_rp)
        ##  get the derivative of rs and rp angle
        deriv_rs_angle = diff_rs_angle / diff_inci_angle
        deriv_rp_angle = diff_rp_angle / diff_inci_angle
        ##  get the interpolated function based on the derivative. These functions take in the incident angle and spit out the derivative of rs or rp angle under the wavelength.
        deriv_rs_func = interpolate.interp1d(angle_list[:-1], deriv_rs_angle)
        deriv_rp_func = interpolate.interp1d(angle_list[:-1], deriv_rp_angle)

        return deriv_rs_func, deriv_rp_func


    @staticmethod
    def get_gh_shift_cond_over_wl(wave_lengths, n0_index, cond, n2_index=1, theta_0=pi/4):
        """
        Only one incident angle is considered in this function.

        Only calculate the difference between rs and rp light
        """

        ##  Express the wavevector
        k0 = 2 * pi * array(n0_index) / array(wave_lengths)

        der_rs_angle_f, der_rp_angle_f = PSHE.get_gh_func_from_cond_over_wl(n0_index, cond, n2_index)

        ##  calculate the GH shift for both rs and rp light
        def gh_shift_for_theta0(theta_0_in):
            rs_shift = der_rs_angle_f(theta_0_in)
            rp_shift = der_rp_angle_f(theta_0_in)

            GH_shift = -(rs_shift - rp_shift) / k0
            return GH_shift

        return gh_shift_for_theta0(theta_0)


    @staticmethod
    def get_gh_shift_cond_no_wl(n0_index, cond, n2_index=1, theta_0=pi/4, w_s=1, w_p=0, sample_points=20000):
        """
        # The calculation of Goos-Hanchen shift based on conductivity.
        ##  n0 index
        It is the refractive index of the medium where light comes from.
        ##  n1 index
        It is the refractive index of the medium where light goes into.
        ##  theta_0
        It is the incident angle. In our experiment, it is pi/4
        """

        ##  Get the function of derivative of phi_s and phi_p over a range of incident angles
        der_rs_angle_f, der_rp_angle_f = PSHE.get_gh_func_from_cond_no_wl(n0_index=n0_index, cond=cond, n2_index=n2_index, sample_points=sample_points)

        ##  Get GH shift for w_s and w_p
        angle_in = theta_0 / pi * 180
        delta_rs = der_rs_angle_f(angle_in)
        delta_rp = der_rp_angle_f(angle_in)

        GH_shift = delta_rs * w_s + delta_rp * w_p

        return GH_shift


    @staticmethod
    def get_BK7_ref_index(path=data_file_dir + "00_common_sense/N-BK7.xlsx"):
        """
        Get the refractive index of BK-7 from the database
        # return
        wave_length_BK7, ref_index_BK7
        """
        data_list = PubMeth.read_xlsx_data(path, exclude_rows_num=1)
        wave_length_BK7 = data_list[0]
        ref_index_BK7 = array(data_list[1]) + 1j * zeros(len(data_list[1]))
        return wave_length_BK7, ref_index_BK7

    @staticmethod
    def sample_wl_fit_substrate_wl(sub_wl, sam_wl, lists_to_cut):
        """
        # return:
        cutted_wl, cutted_lists
        """
        cutted_wl, min_wl_index, max_wl_index = PubMeth.cut_list_within_range(sam_wl, min(sub_wl), max(sub_wl))

        cutted_lists = []
        for ele_list in lists_to_cut:
            ele_cutted_ls = PubMeth.cut_list(ele_list, min_wl_index, max_wl_index)
            cutted_lists.append(array(ele_cutted_ls))

        return cutted_wl, cutted_lists

    @staticmethod
    def read_mos2_if_shift_data():
        """
        # Return:
        all_wls, all_tot_shifts
        """
        ##  load the data of 5 samples
        samples_list = [1, 2, 3, 4, 5]
        all_wls = []
        all_tot_shifts = []
        for ele_sample in samples_list:
            ele_data_list = PubMeth.read_xlsx_data("/home/aoxv/code/Data/00_exp_data/IF_shift_MoS2/sample{}.xlsx".format(ele_sample), exclude_rows_num=0)
            ele_wavelength = ele_data_list[0]
            ele_tot_shift = ele_data_list[3]

            all_wls.append(ele_wavelength)
            all_tot_shifts.append(ele_tot_shift)

        return all_wls, all_tot_shifts

    @staticmethod
    def read_mos2_gh_shift_data():
        """
        # Return:
        all_wls, all_tot_shifts
        """
        ##  load the data of 4 samples
        samples_list = [1, 2, 3, 4, 5]
        all_wls = []
        all_tot_shifts = []
        for ele_sample in samples_list:
            ele_data_list = PubMeth.read_xlsx_data("/home/aoxv/code/Data/00_exp_data/GH_shift_MoS2/sample{}.xlsx".format(ele_sample), exclude_rows_num=0)
            ele_wavelength = ele_data_list[0]
            ele_tot_shift = ele_data_list[3]

            all_wls.append(ele_wavelength)
            all_tot_shifts.append(ele_tot_shift)

        return all_wls, all_tot_shifts

    @staticmethod
    def get_exp_if_center(update=False):
        xbar_list = []
        ybar_list = []

        wls_list, shifts_list = PSHE.read_mos2_if_shift_data()

        if os.path.exists("/home/aoxv/code/Data/PSHE/inclines/xy_bar/if_xbar_list.npy") and (not update):
            print("Using existing data")
            xbar_list = np.load("/home/aoxv/code/Data/PSHE/inclines/xy_bar/if_xbar_list.npy")
            ybar_list = np.load("/home/aoxv/code/Data/PSHE/inclines/xy_bar/if_ybar_list.npy")
        else:
            for ele_i in range(len(wls_list)):
                ele_wls = wls_list[ele_i]
                ele_shift = shifts_list[ele_i]

                ele_xbar, ele_ybar = PubMeth.get_center_of_curve(ele_wls, ele_shift)
                xbar_list.append(ele_xbar)
                ybar_list.append(ele_ybar)
            np.save("/home/aoxv/code/Data/PSHE/inclines/xy_bar/if_xbar_list.npy", xbar_list)
            np.save("/home/aoxv/code/Data/PSHE/inclines/xy_bar/if_ybar_list.npy", ybar_list)

        return xbar_list, ybar_list

    @staticmethod
    def get_exp_gh_center(update=False):
        xbar_list = []
        ybar_list = []

        wls_list, shifts_list = PSHE.read_mos2_gh_shift_data()

        if os.path.exists("/home/aoxv/code/Data/PSHE/inclines/xy_bar/gh_xbar_list.npy") and (not update):
            print("Using existing data")
            xbar_list = np.load("/home/aoxv/code/Data/PSHE/inclines/xy_bar/gh_xbar_list.npy")
            ybar_list = np.load("/home/aoxv/code/Data/PSHE/inclines/xy_bar/gh_ybar_list.npy")
        else:
            for ele_i in range(len(wls_list)):
                ele_wls = wls_list[ele_i]
                ele_shift = shifts_list[ele_i]

                ele_xbar, ele_ybar = PubMeth.get_center_of_curve(ele_wls, ele_shift)
                xbar_list.append(ele_xbar)
                ybar_list.append(ele_ybar)
            np.save("/home/aoxv/code/Data/PSHE/inclines/xy_bar/gh_xbar_list.npy", xbar_list)
            np.save("/home/aoxv/code/Data/PSHE/inclines/xy_bar/gh_ybar_list.npy", ybar_list)

        return xbar_list, ybar_list

    @staticmethod
    def std_of_if_from_line_through_center():
        """
        Set the line of different incline and calculate the standard deviations
        """
        k_range = linspace(0, 1, 200)

        ##  Load IF shifts
        wls_list, shifts_list = PSHE.read_mos2_if_shift_data()

        ##  standard deviations list
        std_func_list = []

        ##  deviations list
        for ele_i in range(len(wls_list)):
            ele_std_list = []
            ele_wls = wls_list[ele_i]
            ele_shift = shifts_list[ele_i]

            ele_xbar, ele_ybar = PubMeth.get_center_of_curve(ele_wls, ele_shift)

            for ele_k in k_range:
                func_for_k = PubMeth.line_through_dot((ele_xbar, ele_ybar), ele_k)

                func_vals_list = func_for_k(array(ele_wls))

                variance_list = (ele_shift - func_vals_list) ** 2

                var_sum = sum(variance_list)

                ele_std_list.append(sqrt(var_sum))

            ele_std_func = interpolate.interp1d(k_range, ele_std_list)

            std_func_list.append(ele_std_func)

        return std_func_list

    @staticmethod
    def std_of_gh_from_line_through_center():
        """
        Set the line of different incline and calculate the standard deviations
        """
        k_range = linspace(-2, 0, 200)

        ##  Load IF shifts
        wls_list, shifts_list = PSHE.read_mos2_gh_shift_data()

        ##  standard deviations list
        std_func_list = []

        ##  deviations list
        for ele_i in range(len(wls_list)):
            ele_std_list = []
            ele_wls = wls_list[ele_i]
            ele_shift = shifts_list[ele_i]

            ele_xbar, ele_ybar = PubMeth.get_center_of_curve(ele_wls, ele_shift)

            for ele_k in k_range:
                func_for_k = PubMeth.line_through_dot((ele_xbar, ele_ybar), ele_k)

                func_vals_list = func_for_k(array(ele_wls))

                variance_list = (ele_shift - func_vals_list) ** 2

                var_sum = sum(variance_list)

                ele_std_list.append(sqrt(var_sum))

            ele_std_func = interpolate.interp1d(k_range, ele_std_list)

            std_func_list.append(ele_std_func)

        return std_func_list


    @staticmethod
    def read_mos2_the_cond_Wu_as_e2_h_shifted(path="/home/aoxv/code/Data/00_common_sense/Wu_cond_real_imag.xlsx"):
        ##  read the data
        data_list = PubMeth.read_xlsx_data(path, exclude_rows_num=2)
        wls = data_list[0]
        real_part = data_list[1]
        imag_part = data_list[2]

        ## Convert data to e^2 / h to verify whether it is correct
        unit_sigma_Wu = c_eV ** 2 / (h_planck)
        real_part = array(real_part) / unit_sigma_Wu
        imag_part = array(imag_part) / unit_sigma_Wu

        return wls, real_part, imag_part

    @staticmethod
    def read_mos2_the_cond_Wu_as_eps_x_c_shifted(path="/home/aoxv/code/Data/00_common_sense/Wu_cond_real_imag.xlsx"):
        """
        # return:
        wavelength, real part (cond), imaginary part (cond)
        """
        ##  read the data
        data_list = PubMeth.read_xlsx_data(path, exclude_rows_num=2)
        wls = data_list[0]
        real_part = data_list[1]
        imag_part = data_list[2]

        ## Convert data to eps0_x_c to verify whether it is correct
        unit_sigma = eps0_x_c
        real_part = array(real_part) / unit_sigma
        imag_part = array(imag_part) / unit_sigma

        return wls, real_part, imag_part

    @staticmethod
    def read_mos2_the_cond_Wu_as_e2_h_unshifted(path="/home/aoxv/code/Data/00_common_sense/Wu_cond_real_imag.xlsx"):
        energy_shift = 100 #   meV

        ##  read the data
        data_list = PubMeth.read_xlsx_data(path, exclude_rows_num=2)

        wls = data_list[0]
        shifted_energy = 1240 / array(wls) * 1000 + energy_shift
        shifted_wls = 1240 / shifted_energy * 1000

        real_part = data_list[1]
        imag_part = data_list[2]

        ## Convert data to e^2 / h to verify whether it is correct
        unit_sigma_Wu = c_eV ** 2 / (h_planck)
        real_part = array(real_part) / unit_sigma_Wu
        imag_part = array(imag_part) / unit_sigma_Wu

        df_dict = {
            "Wavelength": shifted_wls, "Energy": shifted_energy, "RealPart": real_part, "ImaginaryPart": imag_part
        }

        data = pd.DataFrame(df_dict)
        data.to_csv(data_file_dir + "00_common_sense/Wu_cond_original.csv", index=False)


        return shifted_wls, real_part, imag_part

    @staticmethod
    def read_mos2_the_cond_Wu_as_eps_x_c_unshifted(path="/home/aoxv/code/Data/00_common_sense/Wu_cond_real_imag.xlsx"):
        """
        # return:
        wavelength, real part (cond), imaginary part (cond)
        """
        ##  read the data
        energy_shift = 100 #   meV

        data_list = PubMeth.read_xlsx_data(path, exclude_rows_num=2)

        wls = data_list[0]
        shifted_energy = 1240 / array(wls) * 1000 + energy_shift
        shifted_wls = 1240 / shifted_energy * 1000

        real_part = data_list[1]
        imag_part = data_list[2]

        ## Convert data to eps0_x_c to verify whether it is correct
        unit_sigma = eps0_x_c
        real_part = array(real_part) / unit_sigma
        imag_part = array(imag_part) / unit_sigma

        return shifted_wls, real_part, imag_part


    @staticmethod
    def coeff_of_s1_s2(energy_list):
        """
        Calculate the coefficient of sigma1 and sigma2
        """
        d = 0.6 * 1e-9  #   m
        omega_arr = PubMeth.convert_e_to_omega(energy_list)
        coeff = omega_arr * d / c_speed    #   dimensionless

        return coeff


    @staticmethod
    def sigma1(energy_list, omega_p, omega_o, gamma):
        """
        Express the sigma1 term
        """
        omega_arr = PubMeth.convert_e_to_omega(energy_list)

        numerator = omega_p ** 2 * gamma * omega_arr
        denominator_term1 = (omega_o ** 2 - omega_arr ** 2) ** 2
        denominator_term2 = gamma ** 2 * omega_arr ** 2

        output_term = numerator / (denominator_term1 + denominator_term2) * PSHE.coeff_of_s1_s2(energy_list)

        return output_term

    @staticmethod
    def sigma2(energy_list, omega_p, omega_o, gamma):
        """
        Express the sigama2 term
        """
        omega_arr = PubMeth.convert_e_to_omega(energy_list)

        ##  epsilon infty for MoS2
        eps_infty = 15.6

        term1_numerator = omega_p ** 2 * (omega_o ** 2 - omega_arr ** 2)
        term1_denominator_term1 = (omega_o ** 2 - omega_arr ** 2) ** 2
        term1_denominator_term2 = gamma ** 2 * omega_arr ** 2

        term1 = term1_numerator / (term1_denominator_term1 + term1_denominator_term2)
        term2 = eps_infty - 1

        output_term = (term1 + term2) * PSHE.coeff_of_s1_s2(energy_list)

        return output_term

    @staticmethod
    def trial_single_lorentz_s1_s2(energy_list, center_energy=1930, omegap_coeff=sqrt(2), gamma_energy=20, type_s="fromdim"):
        """
        The trial sigma1 and sigma2.
        #   type
        fromdim or direct
        """
        if type_s == "fromdim":
            ##  omega_o
            omega_o = PubMeth.convert_e_to_omega(center_energy)

            ##  omega_p
            omega_p = omega_o * omegap_coeff

            ##  gamma
            gamma = PubMeth.convert_e_to_omega(gamma_energy)

            s1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
            s2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

            return s1, s2
        elif type_s == "direct":
            omega_p = 0

            s1 = PubMeth.lorentz_real(energy_list, omega_p)


    @staticmethod
    def trial_multi_lorentz_s1_s2(energy_list, center_list, omegap_coeff_list, gamma_list, type_s="fromdim"):
        """
        Create the conductivity with multiple Lorentzian oscillator
        """
        if type_s == "fromdim":
            sigma1_list = []
            sigma2_list = []
            ##  epsilon infty for MoS2
            eps_infty = 15.6

            for ele_i in range(len(center_list)):
                omega_o = PubMeth.convert_e_to_omega(center_list[ele_i])

                omega_p = omega_o * omegap_coeff_list[ele_i]

                gamma = PubMeth.convert_e_to_omega(gamma_list[ele_i])

                s1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
                s2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

                sigma1_list.append(s1)
                sigma2_list.append(s2)

            s1_sum = sum(sigma1_list)
            s2_sum = sum(sigma2_list)
            s2_sum_correct = s2_sum - (eps_infty - 1) * (len(center_list) - 1) * PSHE.coeff_of_s1_s2(energy_list)

            return s1_sum, s2_sum_correct

        elif type_s == "direct":
            sigma1_list = []
            sigma2_list = []

            for ele_i in range(len(center_list)):
                ##  parameters
                omega_p = omegap_coeff_list[ele_i]
                omega_o = center_list[ele_i]
                gamma = gamma_list[ele_i]
                ##  Get the Lorentzian peaks
                ##  Here omega_p is the amplitude ratio, ranging from 0 to 1.
                ele_sigma = PubMeth.lorentz_full(energy_list, omega_o, omega_p, gamma, timesi=True)
                s1 = real(ele_sigma)
                s2 = imag(ele_sigma)

                sigma1_list.append(s1)
                sigma2_list.append(s2)

            s1_sum = sum(sigma1_list)
            s2_sum = sum(sigma2_list)

            return s1_sum, s2_sum


    @staticmethod
    def cond_lorentz_s1_s2(energy_list, omega_p, omega_o, gamma):
        """
        fit the conductivity as Lorentzian peaks (single)
        """
        sigma_1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
        sigma_2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

        output_term = sigma_1 + 1j * sigma_2

        return output_term

    @staticmethod
    def matrix_n0_n2_for_gh(n0_index, n2_index, theta_array):
        """
        We need to express the n0 and n2 as matrices
        #   n0_index
        This one should be wavelength-variant
        #   n2_index
        This one should be float or integer. (usually 1 for our case)
        #   theta_array
        The theta list we passed into the function
        #   return
        n0_mat, n2_mat, theta_mat
        """
        ##  theta array into the function
        len_of_theta_list = len(theta_array)

        ##  return what we need
        if PubMeth.array_or_list(n2_index) and PubMeth.float_or_int(n0_index):
            ##  length of wavelength number
            len_wls = len(n2_index)

            ##  n0 matrix
            n0_mat = n0_index * np.ones((len_of_theta_list, len_wls))

            ##  n2 matrix
            n2_mat = np.kron(array(n2_index), np.ones((len_of_theta_list, 1)))

        elif PubMeth.array_or_list(n0_index) and PubMeth.float_or_int(n2_index):
            ##  length of wavelength number
            len_wls = len(n0_index)

            ##  n0 matrix, each row is the same (stands for a specific angle), each column stands for the refractive index under this wavelength.
            n0_mat = np.kron(array(n0_index), np.ones((len_of_theta_list, 1)))

            ##  n2 matrix, each row is the same (stands for a specific angle), each column stands for the refractive index under this wavelength. And because n2 is integer or float, we multiply the value by a matrix of 1 with shape (len_of_theta_list, len_wls)
            n2_mat = n2_index * np.ones((len_of_theta_list, len_wls))

        ##  theta matrix. First we transform the theta list into a column vector so that each row stands for one specific angle. Then we broadcast it to the length of wavelength
        theta_mat = np.kron(theta_array.reshape((-1, 1)), np.ones(len_wls))

        return n0_mat, n2_mat, theta_mat

    @staticmethod
    def f_func_in_rs(n0_index, n2_index, theta_0=pi/4, cal_type='IF'):
        """
        Express the f function in rs
        """
        if cal_type == "IF":
            term1 = n0_index
            term2 = sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)

        elif cal_type == "GH":
            theta_array = array(theta_0)
            n0_mat, n2_mat, theta_mat = PSHE.matrix_n0_n2_for_gh(n0_index, n2_index, theta_array)

            term1 = n0_mat
            term2 = sqrt(n2_mat ** 2 - n0_mat ** 2 * sin(theta_mat) ** 2)

        output_term = term1 - term2

        return output_term

    @staticmethod
    def g_func_in_rs(n0_index, n2_index, theta_0=pi/4, cal_type="IF"):
        """
        Express the g function in rs
        """
        if cal_type == "IF":
            term1 = n0_index
            term2 = sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)

        elif cal_type == "GH":
            theta_array = array(theta_0)
            n0_mat, n2_mat, theta_mat = PSHE.matrix_n0_n2_for_gh(n0_index, n2_index, theta_array)

            term1 = n0_mat
            term2 = sqrt(n2_mat ** 2 - n0_mat ** 2 * sin(theta_mat) ** 2)

        output_term = term1 + term2

        return output_term

    @staticmethod
    def m_func_in_rp(n0_index, n2_index, theta_0=pi/4, cal_type="IF"):
        """
        Express the m function in rp
        """
        if cal_type == "IF":
            numerator_term1 = n2_index ** 2 * cos(theta_0)
            numerator_term2 = n0_index * sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
            numerator = numerator_term1 - numerator_term2

            denominator = cos(theta_0) * sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)

        elif cal_type == "GH":
            theta_array = array(theta_0)
            n0_mat, n2_mat, theta_mat = PSHE.matrix_n0_n2_for_gh(n0_index, n2_index, theta_array)

            numerator_term1 = n2_mat ** 2 * cos(theta_mat)
            numerator_term2 = n0_mat * sqrt(n2_mat ** 2 - n0_mat ** 2 * sin(theta_mat) ** 2)
            numerator = numerator_term1 - numerator_term2

            denominator = cos(theta_mat) * sqrt(n2_mat ** 2 - n0_mat ** 2 * sin(theta_mat) ** 2)

        output_term = numerator / denominator

        return output_term

    @staticmethod
    def n_func_in_rp(n0_index, n2_index, theta_0=pi/4, cal_type="IF"):
        """
        Express the n function in rp
        """
        if cal_type == "IF":
            numerator_term1 = n2_index ** 2 * cos(theta_0)
            numerator_term2 = n0_index * sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
            numerator = numerator_term1 + numerator_term2

            denominator = cos(theta_0) * sqrt(n2_index ** 2 - n0_index ** 2 * sin(theta_0) ** 2)
        elif cal_type == "GH":
            theta_array = array(theta_0)
            n0_mat, n2_mat, theta_mat = PSHE.matrix_n0_n2_for_gh(n0_index, n2_index, theta_array)

            numerator_term1 = n2_mat ** 2 * cos(theta_mat)
            numerator_term2 = n0_mat * sqrt(n2_mat ** 2 - n0_mat ** 2 * sin(theta_mat) ** 2)
            numerator = numerator_term1 + numerator_term2

            denominator = cos(theta_mat) * sqrt(n2_mat ** 2 - n0_mat ** 2 * sin(theta_mat) ** 2)

        output_term = numerator / denominator

        return output_term

    @staticmethod
    def rs_from_s1_s2(sigma1, sigma2, dense_n0_index, theta_0=pi/4, cal_type="IF"):
        """
        Express the amplitude and angle of r_s based on refractive index of BK-7 and air
        """
        if cal_type == "IF":
            ##  Express f and g in the calculations
            f = PSHE.f_func_in_rs(dense_n0_index, n2_index=1, theta_0=theta_0, cal_type=cal_type)
            g = PSHE.g_func_in_rs(dense_n0_index, n2_index=1, theta_0=theta_0, cal_type=cal_type)

            ##  Express rs
            term1 = f - sigma1
            term2 = -1j * sigma2

            numerator = term1 + term2
            denominator = g + sigma1 + 1j * sigma2

        elif cal_type == "GH":
            ##  Express f and g in matrix form, now theta_0 is a list
            f_mat = PSHE.f_func_in_rs(dense_n0_index, n2_index=1, theta_0=theta_0, cal_type=cal_type)
            g_mat = PSHE.g_func_in_rs(dense_n0_index, n2_index=1, theta_0=theta_0, cal_type=cal_type)
            ##  Len of theta list
            len_theta_list = len(theta_0)
            ##  Express the sigma1 and sigma2 as matrix form. Each row corresponds to a specific angle and each column corresponds to a specific wavelength.
            sigma1_mat = np.kron(array(sigma1), np.ones((len_theta_list, 1)))
            sigma2_mat = np.kron(array(sigma2), np.ones((len_theta_list, 1)))

            term1 = f_mat - sigma1_mat
            term2 = -1j * sigma2_mat

            numerator = term1 + term2
            denominator = g_mat + sigma1_mat + 1j * sigma2_mat

        rs = numerator / denominator

        ##  Express Rs and Angle
        Rs = np.abs(rs)
        phi_s = np.angle(rs)

        return Rs, phi_s

    @staticmethod
    def rp_from_s1_s2(sigma1, sigma2, dense_n0_index, theta_0=pi/4, cal_type="IF"):
        """
        Express the amplitude and angle of r_p based on refractive index of BK-7 and air
        """
        if cal_type == "IF":
            ##  Express f and g in the calculations
            m = PSHE.m_func_in_rp(dense_n0_index, n2_index=1, theta_0=theta_0)
            n = PSHE.n_func_in_rp(dense_n0_index, n2_index=1, theta_0=theta_0)

            ##  Express rs
            term1 = m + sigma1
            term2 = 1j * sigma2

            numerator = term1 + term2
            denominator = n + sigma1 + 1j * sigma2
        elif cal_type == "GH":
            ##  Express f and g in the matrix form
            m_mat = PSHE.m_func_in_rp(dense_n0_index, n2_index=1, theta_0=theta_0, cal_type=cal_type)
            n_mat = PSHE.n_func_in_rp(dense_n0_index, n2_index=1, theta_0=theta_0, cal_type=cal_type)
            ##  Len of theta list
            len_theta_list = len(theta_0)

            ##  Express the sigma1 and sigma2 as matrix form
            sigma1_mat = np.kron(array(sigma1), np.ones((len_theta_list, 1)))
            sigma2_mat = np.kron(array(sigma2), np.ones((len_theta_list, 1)))

            ##  Express rs
            term1 = m_mat + sigma1_mat
            term2 = 1j * sigma2_mat

            numerator = term1 + term2
            denominator = n_mat + sigma1_mat + 1j * sigma2_mat

        rp = numerator / denominator

        ##  Express Rs and Angle
        Rp = np.abs(rp)
        phi_p = np.angle(rp)

        return Rp, phi_p

    @staticmethod
    def rs_from_s1_s2_static(s1, s2, n0, n2, theta_0):
        """
        Get rs for static values
        """
        if PubMeth.float_or_int(s1) and PubMeth.float_or_int(s2):
            sigma = s1 + 1j * s2

        elif PubMeth.array_or_list(s1) and PubMeth.array_or_list(s2):
            print("Input s1 and s2 are both array. Matrix-izing... for rs")
            ##  create sigma matrix, horizontal axis is s1 and vertical axis is s2
            sigma = array([ele_s2 + array(s1) for ele_s2 in s2])

        numerator_term1 = n0 * cos(theta_0)
        numerator_term2 = np.emath.sqrt(n2 ** 2 - n0 ** 2 * sin(theta_0) ** 2)
        numerator = numerator_term1 - numerator_term2 - sigma

        denominat_term1 = n0 * cos(theta_0)
        denominat_term2 = np.emath.sqrt(n2 ** 2 - n0 ** 2 * sin(theta_0) ** 2)
        denominat = denominat_term1 + denominat_term2 + sigma

        rs = numerator / denominat

        Rs = np.abs(rs)
        phi_s = np.angle(rs)

        return Rs, phi_s


    @staticmethod
    def rp_from_s1_s2_static(s1, s2, n0, n2, theta_0):
        """
        Get rp for static values
        s1 and s2 can be two ndarray, which we will matrix-ize them and get the rs matrix
        """
        if PubMeth.float_or_int(s1) and PubMeth.float_or_int(s2):
            sigma = s1 + 1j * s2

        elif PubMeth.array_or_list(s1) and PubMeth.array_or_list(s2):
            print("Input s1 and s2 are both array. Matrix-izing... for rp")
            ##  create sigma matrix, horizontal axis is s1 and vertical axis is s2
            sigma = array([ele_s2 + array(s1) for ele_s2 in s2])

        numerator_term1 = n2 ** 2 * cos(theta_0)
        numerator_term2 = n0 * np.emath.sqrt(n2 ** 2 - n0 ** 2 * sin(theta_0) ** 2)
        numerator_term3 = sigma * cos(theta_0) * np.emath.sqrt(n2 ** 2 - n0 ** 2 * sin(theta_0) ** 2)
        numerator = numerator_term1 - numerator_term2 + numerator_term3

        denominat_term1 = n2 ** 2 * cos(theta_0)
        denominat_term2 = n0 * np.emath.sqrt(n2 ** 2 - n0 ** 2 * sin(theta_0) ** 2)
        denominat_term3 = sigma * cos(theta_0) * np.emath.sqrt(n2 ** 2 - n0 ** 2 * sin(theta_0) ** 2)
        denominat = denominat_term1 + denominat_term2 + denominat_term3

        rp = numerator / denominat

        Rp = np.abs(rp)
        phi_p = np.angle(rp)

        return Rp, phi_p

    @staticmethod
    def get_if_shift_from_s1_s2(sigma1, sigma2, dense_wls, dense_n0_index, theta_0=pi/4, lorentz_const=0, start_wls=496, dimensionless=False):
        """
        Get IF shift from sigma1 and sigma2 (Lorentzian peak)
        """

        ##  k0 wave vector
        k0 = 2 * pi * array(dense_n0_index) / array(dense_wls)

        ##  Rs and phi_s
        Rs, phi_s = PSHE.rs_from_s1_s2(sigma1 + lorentz_const, sigma2, dense_n0_index, theta_0=theta_0)

        ##  Rp and phi_p
        Rp, phi_p = PSHE.rp_from_s1_s2(sigma1 + lorentz_const, sigma2, dense_n0_index, theta_0=theta_0)


        if dimensionless:
            ##  Dimensionless IF shift expression
            Delta_IF = -1 / np.tan(theta_0) * (1 + 2 * Rs * Rp / (Rs ** 2 + Rp ** 2) * cos(phi_p - phi_s))

            Delta_IF = Delta_IF[dense_wls > start_wls]
        else:
            ##  Regular IF shift expression
            Delta_IF = -1 / (k0 * np.tan(theta_0)) * (1 + 2 * Rs * Rp / (Rs ** 2 + Rp ** 2) * cos(phi_p - phi_s))

            Delta_IF = Delta_IF[dense_wls > start_wls]

        return 2 * abs(Delta_IF)


    @staticmethod
    def get_der_phi_sp_func_from_s1_s2(sigma1, sigma2, dense_n0_index, lorentz_const=0, sample_points=1000):
        """
        Calculate the derivative of phi_s and phi_p based on conductivity.
        Remind that phi_s and phi_p are both matrices here. Each row corresponds to an incident angle while each column corresponds to a specific wavelength
        """

        ##  Set the angles we need to get the phi_s and phi_p derivative
        theta_list = linspace(0, pi / 2, sample_points)
        diff_theta = np.diff(theta_list)
        diff_theta = diff_theta.reshape((-1, 1))    #   reshape it as column vector so that the difference of phi_s and phi_p will be divided by difference of theta

        ##  length of wavelength number
        len_wls = len(sigma1)

        ##  Rs and phi_s matrices
        Rs_mat, phis_mat = PSHE.rs_from_s1_s2(sigma1 + lorentz_const, sigma2, dense_n0_index, theta_0=theta_list, cal_type="GH")

        ##  Rp and phi_p matrices
        Rp_mat, phip_mat = PSHE.rp_from_s1_s2(sigma1 + lorentz_const, sigma2, dense_n0_index, theta_0=theta_list, cal_type="GH")

        ##  Calculate the derivative of phi_s and phi_p with respect to the incident angles.
        ##  The diff function calculates the difference between each row
        diff_phis_mat = np.diff(phis_mat, axis=0)
        diff_phip_mat = np.diff(phip_mat, axis=0)

        ##  Now the dimension of the matrix is (len(theta)-1, len(wavelength))
        der_phis_mat = diff_phis_mat / diff_theta
        der_phip_mat = diff_phip_mat / diff_theta

        ##  Interpolate each column data so that we can have any incident angle we want.
        der_phis_func_list = [interpolate.interp1d(theta_list[:-1], der_phis_mat[:, ele_i]) for ele_i  in range(len_wls)]
        der_phip_func_list = [interpolate.interp1d(theta_list[:-1], der_phip_mat[:, ele_i]) for ele_i  in range(len_wls)]

        def der_phis_at_theta(theta_in):
            """
            Output the derivative of phi_s at specific theta over a range of wavelength
            """
            value_arr = [ele_f(theta_in) for ele_f in der_phis_func_list]

            return array(value_arr)

        def der_phip_at_theta(theta_in):
            """
            Output the derivative of phi_p at specific theta over a range of wavelength
            """
            value_arr = [ele_f(theta_in) for ele_f in der_phip_func_list]

            return array(value_arr)

        print("Complete creat function handle of two derivatives of phi_s and phi_p")

        return der_phis_at_theta, der_phip_at_theta

    @staticmethod
    def get_gh_shift_from_s1_s2(sigma1, sigma2, dense_wls, dense_n0_index, theta_0=pi/4, lorentz_const=0, sample_points=1000, start_wls=496):
        """
        Get GH shift from sigma1 and sigma2 (Lorentzian peaks)
        """
        ##  Get the derivative of phi_s and phi_p based on conductivity
        der_phis_func, der_phip_func = PSHE.get_der_phi_sp_func_from_s1_s2(sigma1, sigma2, dense_n0_index, lorentz_const, sample_points=sample_points)

        ##  Wave vector expression
        k0 = 2 * pi * array(dense_n0_index) / array(dense_wls)

        ##  Express the GH shift from s-light
        delta_s = -1 / k0 * (der_phis_func(theta_0))
        delta_p = -1 / k0 * (der_phip_func(theta_0))

        ##  Express the total difference
        Delta_GH = delta_s - delta_p

        ##  Output can be shifted by a certain constant
        output_term = Delta_GH

        output_term = output_term[dense_wls > start_wls]

        return real(output_term)

    @staticmethod
    def get_n0_interp_func(wls_points):
        """
        Get the interpolated function of n0 over wavelength (or energy)
        #   return
        dense_wls, dense_n0_index, f_n0 (f_n0 is the function of wavelength, not energy)
        """
        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), wls_points)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        return dense_wls, dense_n0_index, f_n0

    @staticmethod
    def get_gh_shift_over_wl_s1_s2_direct_lorentz(center_list, amp_ratio_list, gamma_list, theta_0=pi/4, lorentz_const=0, sample_points=500, wls_points=1000, start_wls=496):
        """
        Express GH shift based the direct expression of Lorentzian peaks
        """

        ##  Get the interpolated n0 over specific wavelength range
        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_energy = 1240 / dense_wls * 1000

        ##  s1 and s2 directly from Lorentzian peaks
        sigma= PubMeth.lorentz_full(dense_energy, center_list, amp_ratio_list, gamma_list, True, pars_type="list")
        s1 = real(sigma)
        s2 = imag(sigma)

        ##  calculate the GH shift
        GH_shift = PSHE.get_gh_shift_from_s1_s2(s1, s2, dense_wls, dense_n0_index, theta_0=theta_0, lorentz_const=lorentz_const, sample_points=sample_points)

        dense_wls = dense_wls[dense_wls > start_wls]

        return GH_shift, dense_wls

    @staticmethod
    def get_if_shift_over_wl_s1_s2_direct_lorentz(dense_energy, center_list, amp_ratio_list, gamma_list, theta_0=pi/4, lorentz_const=0, wls_points=1000, start_wls=496, dimensionless=False):
        """
        Express IF shift based the direct expression of Lorentzian peaks
        """

        ##  Get the interpolated n0 over specific wavelength range
        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_wls = 1240 / dense_energy * 1000
        dense_n0_index = f_n0(dense_wls)

        ##  s1 and s2 directly from Lorentzian peaks
        sigma= PubMeth.lorentz_full(dense_energy, center_list, amp_ratio_list, gamma_list, True, pars_type="list")
        s1 = real(sigma)
        s2 = imag(sigma)

        ##  calculate the GH shift
        IF_shift = PSHE.get_if_shift_from_s1_s2(s1, s2, dense_wls, dense_n0_index, theta_0=theta_0, lorentz_const=lorentz_const, dimensionless=dimensionless)

        dense_wls = dense_wls[dense_wls > start_wls]

        return IF_shift, dense_wls

    @staticmethod
    def wrapper_if_shift_direct_lorentz_func(dense_energy, N, theta_0, *args):
        """
        #   N
        the number of Lorentzian peaks you put in
        #   Parameters to put in
        [N energy centers, N amplitudes, N gammas, total shift, lorentzian peaks]
        """
        center_list, amp_ratio_list, gamma_list = list(args[0][ : N]), list(args[0][N : 2 * N]), list(args[0][2 * N : 3 * N])

        output_if_shift = PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(dense_energy, center_list, amp_ratio_list, gamma_list, theta_0=theta_0)[0]

        return output_if_shift

    @staticmethod
    def fit_exp_IF_direct_lorentz_dash(initial_p0, target_energy, target_if_shift, theta_0=pi / 4):
        """
        Fit the experiment results (with dimension)
        #   initial p0

        for both fromdim and direct:

        [center_list, coeff_list, gamma_list, lorentz_const]
        #   bounds_tuple

        for both fromdim and direct:

        (low_bound_list, up_bound_list):
            (
                [center_list_low_bound, amp_ratio_low_bound, gamma_low_bound, const_low_bound],
                [center_list_up_bound, amp_ratio_up_bound, gamma_up_bound, const_up_bound]
            )

        #   return
        center_list_fit, amp_ratio_list_fit, gamma_list_fit, lorentz_const_fit
        """
        ##  Define the number of lorentzian peaks
        extra_pars = 0  #   extra parameters besides original lorentzian peak parameters: lorentz constant
        unit_par_num_lorentz = 3    #   number of parameters each lorentzian peak holds
        lorentz_num = (len(initial_p0) - extra_pars) // unit_par_num_lorentz
        print("# of Lorentzian peaks: ", lorentz_num)

        ##  Define the boundaries of these parameters
        center_list_origin = initial_p0[ : lorentz_num]
        amp_ratio_list_origin = initial_p0[lorentz_num : lorentz_num * 2]
        gamma_list_origin = initial_p0[lorentz_num * 2 : lorentz_num * 3]

        center_list_up_bound = [ele_center + 10 for ele_center in center_list_origin]
        center_list_be_bound = [ele_center - 10 for ele_center in center_list_origin]

        amp_ratio_up_bound = [ele_amp + 0.2 for ele_amp in amp_ratio_list_origin]
        amp_ratio_be_bound = [ele_amp - 0.2 for ele_amp in amp_ratio_list_origin]

        amp_ratio_up_bound = [1] * 6
        amp_ratio_be_bound = [0.25] * 6

        gamma_up_bound = [ele_gamma + 0.001 for ele_gamma in gamma_list_origin]
        gamma_be_bound = [ele_gamma - 0.001 for ele_gamma in gamma_list_origin]

        gamma_up_bound = [80] * 6
        gamma_be_bound = [23] * 6

        up_bound_list = center_list_up_bound + amp_ratio_up_bound + gamma_up_bound
        be_bound_list = center_list_be_bound + amp_ratio_be_bound + gamma_be_bound

        bounds_tuple = (be_bound_list, up_bound_list)

        ##  Fit the curve
        print("Fitting Begins!")
        popt, pcov = curve_fit(lambda x, *p_0: PSHE.wrapper_if_shift_direct_lorentz_func(x, lorentz_num, theta_0, p_0), target_energy, target_if_shift, p0=initial_p0, bounds=bounds_tuple, maxfev=500000)
        print("The energy of every Lorentzian peaks: \n", popt[:lorentz_num])
        print("The coefficient of omega_p over omega_o: \n", popt[lorentz_num:lorentz_num*2])
        print("The gamma energy of every Lorenzian peak: \n", popt[lorentz_num*2:lorentz_num*3])
        print("Lorentzian constant: \n", popt[-1])

        center_list_fit = popt[ : lorentz_num]
        amp_ratio_list_fit = popt[lorentz_num : lorentz_num * 2]
        gamma_list_fit = popt[lorentz_num * 2 : lorentz_num * 3]

        return center_list_fit, amp_ratio_list_fit, gamma_list_fit

    @staticmethod
    def fit_exp_IF_continuous_lorentzian_peaks(target_energy, target_if_shift, theta_0=pi / 4):
        """
        Fit the experiment results (with dimension)
        #   initial p0

        for both fromdim and direct:

        [center_list, coeff_list, gamma_list, lorentz_const]
        #   bounds_tuple

        for both fromdim and direct:

        (low_bound_list, up_bound_list):
            (
                [center_list_low_bound, amp_ratio_low_bound, gamma_low_bound, const_low_bound],
                [center_list_up_bound, amp_ratio_up_bound, gamma_up_bound, const_up_bound]
            )

        #   return
        center_list_fit, amp_ratio_list_fit, gamma_list_fit, lorentz_const_fit
        """
        energy_centers = arange(1820, 2400, 60)
        lorentz_num = len(energy_centers)
        amp_ratio_list = [0.25] * lorentz_num
        gamma_list = [50] & lorentz_num

        initial_p0 = energy_centers + amp_ratio_list + gamma_list

        ##  Define the number of lorentzian peaks
        print("# of Lorentzian peaks: ", lorentz_num)

        ##  Define the boundaries of these parameters
        center_list_origin = initial_p0[ : lorentz_num]
        amp_ratio_list_origin = initial_p0[lorentz_num : lorentz_num * 2]
        gamma_list_origin = initial_p0[lorentz_num * 2 : lorentz_num * 3]

        center_list_up_bound = [ele_center + 10 for ele_center in center_list_origin]
        center_list_be_bound = [ele_center - 10 for ele_center in center_list_origin]

        # amp_ratio_up_bound = [ele_amp + 0.2 for ele_amp in amp_ratio_list_origin]
        # amp_ratio_be_bound = [ele_amp - 0.2 for ele_amp in amp_ratio_list_origin]

        amp_ratio_up_bound = [1] * 6
        amp_ratio_be_bound = [0.25] * 6

        # gamma_up_bound = [ele_gamma + 0.001 for ele_gamma in gamma_list_origin]
        # gamma_be_bound = [ele_gamma - 0.001 for ele_gamma in gamma_list_origin]

        gamma_up_bound = [80] * 6
        gamma_be_bound = [25] * 6

        up_bound_list = center_list_up_bound + amp_ratio_up_bound + gamma_up_bound
        be_bound_list = center_list_be_bound + amp_ratio_be_bound + gamma_be_bound

        bounds_tuple = (be_bound_list, up_bound_list)

        ##  Fit the curve
        print("Fitting Begins!")
        popt, pcov = curve_fit(lambda x, *p_0: PSHE.wrapper_if_shift_direct_lorentz_func(x, lorentz_num, theta_0, p_0), target_energy, target_if_shift, p0=initial_p0, bounds=bounds_tuple, maxfev=500000)
        print("The energy of every Lorentzian peaks: \n", popt[:lorentz_num])
        print("The coefficient of omega_p over omega_o: \n", popt[lorentz_num:lorentz_num*2])
        print("The gamma energy of every Lorenzian peak: \n", popt[lorentz_num*2:lorentz_num*3])
        print("Lorentzian constant: \n", popt[-1])

        center_list_fit = popt[ : lorentz_num]
        amp_ratio_list_fit = popt[lorentz_num : lorentz_num * 2]
        gamma_list_fit = popt[lorentz_num * 2 : lorentz_num * 3]

        return center_list_fit, amp_ratio_list_fit, gamma_list_fit


    @staticmethod
    def if_shift_func_multi_lorentz(dense_energy, center_list, amp_ratio_list, gamma_list, total_shift, lorentz_const=0, type_s="fromdim"):
        """
        # Start from 0!
        Use this function to do fitting to the experimental data. Experiment data and theoretical data are set to start from 0
        # total shift
        The total shift is to shift all the results upward or downward
        """

        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = 1240 / dense_energy * 1000
        dense_n0_index = f_n0(dense_wls)

        ##  Get the conductivity based on the Lorentzian peaks parameters
        s1, s2 = PSHE.trial_multi_lorentz_s1_s2(dense_energy, center_list, amp_ratio_list, gamma_list, type_s=type_s)

        ##  Calculate IF-shift based on s1 and s2
        IF_shift = PSHE.get_if_shift_from_s1_s2(s1, s2, dense_wls, dense_n0_index, theta_0=pi/4, lorentz_const=lorentz_const) + total_shift

        return IF_shift


    @staticmethod
    def wrapper_if_shift_multi_lorentz_func(dense_energy, N, *args, type_s='fromdim'):
        """
        #   N
        the number of Lorentzian peaks you put in
        #   Parameters to put in
        [N energy centers, N amplitudes, N gammas, total shift, lorentzian peaks]
        """
        center_list, coeff_list, gamma_list = list(args[0][:N]), list(args[0][N:2*N]), list(args[0][2*N:3*N])
        total_shift = args[0][-2]
        lorentz_const = args[0][-1]

        return PSHE.if_shift_func_multi_lorentz(dense_energy, center_list, coeff_list, gamma_list, total_shift, lorentz_const=lorentz_const, type_s=type_s)


    @staticmethod
    def fit_exp_IF_multi_lorentz(initial_p0, bounds_tuple, fit_file_name="if_fit_lorentz", sample_index=1, type_s='fromdim'):
        """
        Fit the experiment results (with dimension)
        #   initial p0

        for both fromdim and direct:

        [center_list, coeff_list, gamma_list, total_shift, lorentz_const]
        #   bounds_tuple

        for both fromdim and direct:

        (low_bound_list, up_bound_list):
            (
                [center_list_low_bound, coeff_low_bound, gamma_low_bound, shift_low_bound, const_low_bound],
                [center_list_up_bound, coeff_up_bound, gamma_up_bound, shift_up_bound, const_up_bound]
            )

        #   return
        center_list_fit, coeff_list_fit, gamma_list_fit, total_shift_fit
        """
        ##  Define the number of lorentzian peaks
        extra_pars = 2  #   extra parameters besides original lorentzian peak parameters
        unit_par_num_lorentz = 3    #   number of parameters each lorentzian peak holds
        lorentz_num = (len(initial_p0) - extra_pars) // unit_par_num_lorentz

        ##  load the experiment result, remind that we don't use the data shifted to 0.
        wls_list, IF_shift_list = PSHE.read_mos2_if_shift_data()
        target_IF_shift = IF_shift_list[sample_index]
        target_wls = wls_list[sample_index]
        target_energy = 1240 / array(target_wls) * 1000 #   meV

        ## Read n0 and get the density energies
        dense_wls = PSHE.get_n0_interp_func(1000)[0]
        dense_energy = 1240 / dense_wls * 1000  #   meV

        ##  Fit the curve
        popt, pcov = curve_fit(lambda x, *p_0: PSHE.wrapper_if_shift_multi_lorentz_func(x, lorentz_num, p_0, type_s=type_s), target_energy, target_IF_shift, p0=initial_p0, bounds=bounds_tuple, maxfev=500000)
        print("The energy of every Lorentzian peaks: \n", popt[:lorentz_num])
        print("The coefficient of omega_p over omega_o: \n", popt[lorentz_num:lorentz_num*2])
        print("The gamma energy of every Lorenzian peak: \n", popt[lorentz_num*2:lorentz_num*3])
        print("Total shift: \n", popt[-2])
        print("Lorentzian constant: \n", popt[-1])

        center_list_fit = popt[ : lorentz_num]
        amp_ratio_list_fit = popt[lorentz_num : lorentz_num * 2]
        gamma_list_fit = popt[lorentz_num * 2 : lorentz_num * 3]

        total_shift_fit = popt[-2]
        lorentz_const_fit = popt[-1]

        ##  Plot IF shift based on the fitted parameters
        IF_shift_fit = PSHE.if_shift_func_multi_lorentz(target_energy, center_list_fit, amp_ratio_list_fit, gamma_list_fit, total_shift=total_shift_fit, lorentz_const=lorentz_const_fit, type_s=type_s)

        ##  Plot the fitted result with respect to the energy
        fig, ax_fit = plt.subplots()
        ax_fit.plot(target_energy, IF_shift_fit)
        ax_fit.plot(target_energy, target_IF_shift)
        ax_fit.set_aspect('auto')
        ax_fit.set_xlabel('E (meV)', fontsize=12)
        ax_fit.set_ylabel(r'$\Delta_{IF}$ (nm)', fontsize=12)
        ax_fit.set_title('', fontsize=14)
        # ax_fit.set_xlim([500, 700])
        ax_fit.set_ylim(ax_fit.get_ylim())
        ax_fit.legend(["Theory", "Experiment"])
        fig.savefig(data_file_dir + "PSHE/fit_exp_direct/{}_E.png".format(fit_file_name), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
        plt.close()

        ##  Plot the fitted result with respect to wavelength
        fig, ax_fit = plt.subplots()
        ax_fit.plot(target_wls, IF_shift_fit)
        ax_fit.plot(target_wls, target_IF_shift)
        ax_fit.set_aspect('auto')
        ax_fit.set_xlabel('$\lambda$ (nm)', fontsize=12)
        ax_fit.set_ylabel(r'$\Delta_{IF}$ (nm)', fontsize=12)
        ax_fit.set_title('', fontsize=14)
        ax_fit.set_xlim([500, 700])
        ax_fit.set_ylim(ax_fit.get_ylim())
        ax_fit.legend(["Theory", "Experiment"])
        fig.savefig(data_file_dir + "PSHE/fit_exp_direct/{}_lambda.png".format(fit_file_name), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
        plt.close()

        ##  Plot the fitted sigma
        fig, ax_s1 = plt.subplots()
        ax_s1.plot()
        ax_s1.set_aspect('auto')
        ax_s1.set_xlabel('', fontsize=12)
        ax_s1.set_ylabel('', fontsize=12)
        ax_s1.set_title('', fontsize=14)
        ax_s1.set_xlim(ax_s1.get_xlim())
        ax_s1.set_ylim(ax_s1.get_ylim())
        ax_s1.legend([])
        fig.savefig(data_file_dir + ".png", dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
        fig.savefig(data_file_dir + ".pdf", dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
        plt.close()

        return center_list_fit, amp_ratio_list_fit, gamma_list_fit, total_shift_fit, lorentz_const_fit


    @staticmethod
    def eta_amp_to_center_gamma(center, gamma, scale_ratio=1):
        """
        ratio of eta which makes lorentzian amplitude to be 1.
        """
        ratio = sqrt(gamma / center)

        output_term = ratio * center * scale_ratio

        return output_term

    #region
    # @staticmethod
    # def scan_s1_s2_for_one_lambda(s1, s2, wl, theta_0=pi/4):
    #     """
    #     Scan sigma1 and sigma2 for one single lambda
    #     """


    #     ##  get n0 for the specific lambda
    #     dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(1000)
    #     n0_lambda = f_n0(wl)

    #     ##  k0 vector
    #     k0 = 2 * pi * n0_lambda / wl

    #     ##  Express static rs and rp (both amplitude and angles)
    #     Rs, phi_s = PSHE.rs_from_s1_s2_static(s1, s2, n0_lambda, n2=1, theta_0=theta_0)
    #     Rp, phi_p = PSHE.rp_from_s1_s2_static(s1, s2, n0_lambda, n2=1, theta_0=theta_0)

    #     ##  Express the IF shift based on rs and rp properties
    #     Delta_IF = -1 / (k0 * np.tan(theta_0)) * (1 + 2 * Rs * Rp / (Rs ** 2 + Rp ** 2) * cos(phi_p - phi_s))

    #     return 2 * abs(Delta_IF)
    #endregion


    @staticmethod
    def initial_lorentz_pars(type_s="fromdim", lorentz_num=6):
        """
        #   type_s
        "fromdim" or "direct"

        Input initial parameters of Lorentzian peaks to start fitting.

        Now we only consider 6 Lorentzian peaks in the calculations

        remind that amplitude list is the maximum value of each Lorentzian peak. It can only be reduced rather than increased

        Parameters

        #   return
        initial_p0, bound_up_list, bound_be_list
        """
        ##  Initial parameters
        # lorentz_num = 6
        energy_centers = [1823.56, 1924.11, 2030.66, 2127.53, 2193.29, 2370.82]
        amp_ratio_list = [0.32, 0.3, 0.39, 0.25, 0.25, 0.31]
        # gamma_list = [80] * lorentz_num
        gamma_list = [55.63, 80.0, 78.65, 26.19, 23.0, 59.52]

        initial_p0 = energy_centers + amp_ratio_list + gamma_list

        return initial_p0


    @staticmethod
    def get_incline_of_no_lorentzian_line(update=False):
        ##  parameters
        wls_points = 1200

        center_list = [1]
        amp_ratio_list = [0.]
        gamma_list = [40]

        theta_list = linspace(0, pi / 2, 50)

        ##  Get the interpolated n0 over specific wavelength range
        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_energy = 1240 / dense_wls * 1000

        ##  Experiment data
        # wls_list, if_shift_list = PSHE.read_mos2_if_shift_data()
        # wavelengths1 = wls_list[0]
        # if_shift1 = array(if_shift_list[0]) + 40

        # wls_list, gh_shift_list = PSHE.read_mos2_gh_shift_data()
        # gh_wls1 = wls_list[0]
        # gh_shift1 = array(gh_shift_list[0]) - 190

        ##  GH shift dependence on incident angle
        plot_theta_list = arange(42.5 / 180 * pi, 60 / 180 * pi, 0.1 / 180 * pi)
        plot_angle_list = plot_theta_list / pi * 180
        # plot_theta_list = [55 / 180 * pi]
        # traces_GH_list = []
        # traces_IF_list = []

        k_incline_GH_list = []
        k_incline_IF_list = []
        b_incepts_GH_list = []
        b_incepts_IF_list = []

        if os.path.exists("/home/aoxv/code/Data/PSHE/inclines/incline_if.npy") and (not update):
            k_incline_IF_list = np.load("/home/aoxv/code/Data/PSHE/inclines/incline_if.npy")
            k_incline_GH_list = np.load("/home/aoxv/code/Data/PSHE/inclines/incline_gh.npy")
            b_incepts_IF_list = np.load("/home/aoxv/code/Data/PSHE/inclines/incepts_if.npy")
            b_incepts_GH_list = np.load("/home/aoxv/code/Data/PSHE/inclines/incepts_gh.npy")
            plot_angle_list = np.load("/home/aoxv/code/Data/PSHE/inclines/angles.npy")
        else:
            for ele_theta in plot_theta_list:
                ele_GH_shift, ele_GH_wls = PSHE.get_gh_shift_over_wl_s1_s2_direct_lorentz(center_list, amp_ratio_list, gamma_list, theta_0=ele_theta, sample_points=1000, wls_points=wls_points)
                ele_IF_shift, ele_wavelengths = PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(dense_energy, center_list, amp_ratio_list, gamma_list, theta_0=ele_theta, wls_points=wls_points)

                print("Complete angle (degree): ", round(ele_theta / pi * 180, 2))
                k_incline_GH = np.mean(np.diff(ele_GH_shift) / np.diff(ele_GH_wls))
                k_incline_GH_list.append(k_incline_GH)
                b_incept_GH = ele_GH_shift[0] - k_incline_GH * ele_GH_wls[0]
                b_incepts_GH_list.append(b_incept_GH)

                k_incline_IF = np.mean(np.diff(ele_IF_shift) / np.diff(ele_wavelengths))
                k_incline_IF_list.append(k_incline_IF)
                b_incept_IF = ele_IF_shift[0] - k_incline_IF * ele_wavelengths[0]
                b_incepts_IF_list.append(b_incept_IF)

            np.save("/home/aoxv/code/Data/PSHE/inclines/incline_if.npy", k_incline_IF_list)
            np.save("/home/aoxv/code/Data/PSHE/inclines/incline_gh.npy", k_incline_GH_list)
            np.save("/home/aoxv/code/Data/PSHE/inclines/incepts_if.npy", b_incepts_IF_list)
            np.save("/home/aoxv/code/Data/PSHE/inclines/incepts_gh.npy", b_incepts_GH_list)
            np.save("/home/aoxv/code/Data/PSHE/inclines/angles.npy", plot_angle_list)

        interp_for_incline_IF = interpolate.interp1d(plot_angle_list, k_incline_IF_list)
        interp_for_incline_GH = interpolate.interp1d(plot_angle_list, k_incline_GH_list)

        interp_for_incepts_IF = interpolate.interp1d(plot_angle_list, b_incepts_IF_list)
        interp_for_incepts_GH = interpolate.interp1d(plot_angle_list, b_incepts_GH_list)

        return interp_for_incline_IF, interp_for_incline_GH, interp_for_incepts_IF, interp_for_incepts_GH

    @staticmethod
    def std_if_gh_to_get_actual_angles():
        """
        Standard deviations of IF and GH shift
        """
        ##  Angle list
        theta_list = arange(42.5 / 180 * pi, 60 / 180 * pi, 0.1 / 180 * pi)
        angle_list = theta_list / pi * 180

        if_std_func_list = PSHE.std_of_if_from_line_through_center()
        gh_std_func_list = PSHE.std_of_gh_from_line_through_center()

        if_incline_func, gh_incline_func = PSHE.get_incline_of_no_lorentzian_line()[:2]

        if_gh_std_list = []

        actual_angles_list = []

        for ele_i in range(len(if_std_func_list)):
            ele_if_gh_std_list = []
            ele_if_std_func = if_std_func_list[ele_i]
            ele_gh_std_func = gh_std_func_list[ele_i]
            for ele_angle in angle_list:
                ele_if_k = if_incline_func(ele_angle)
                ele_gh_k = gh_incline_func(ele_angle)

                ele_if_std = ele_if_std_func(ele_if_k)
                ele_gh_std = ele_gh_std_func(ele_gh_k)

                ele_if_var = ele_if_std ** 2
                ele_gh_var = ele_gh_std ** 2

                ele_if_plus_gh_var = ele_if_var + ele_gh_var
                ele_if_plus_gh_std = sqrt(ele_if_plus_gh_var)

                ele_if_gh_std_list.append(ele_if_plus_gh_std)

            if_gh_std_list.append(ele_if_gh_std_list)

            fig, ax_if_gh_std = plt.subplots()
            ax_if_gh_std.plot(angle_list, ele_if_gh_std_list)
            ax_if_gh_std.set_aspect('auto')
            ax_if_gh_std.set_xlabel(r'($\degree$)', fontsize=12)
            ax_if_gh_std.set_ylabel('(nm)', fontsize=12)
            ax_if_gh_std.set_title('Standard Deviations (IF + GH)', fontsize=14)
            ax_if_gh_std.set_xlim(ax_if_gh_std.get_xlim())
            ax_if_gh_std.set_ylim(ax_if_gh_std.get_ylim())
            fig.savefig(data_file_dir + "PSHE/inclines/if_plus_gh_std_for_angle/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            plt.close()

            ele_actual_angle = angle_list[ele_if_gh_std_list.index(min(ele_if_gh_std_list))]

            actual_angles_list.append(ele_actual_angle)

        actual_angles_list = [45] * 6

        return actual_angles_list

    @staticmethod
    def shift_of_exp_if_to_the(update=False):
        """
        The amount of shift we should do to the IF shift to make it correspond to the theory.
        """
        wavelengths, if_shifts = PSHE.read_mos2_if_shift_data()
        if_xbar_list, if_ybar_list = PSHE.get_exp_if_center()

        actual_angles_list = PSHE.std_if_gh_to_get_actual_angles()

        if_incline_func, gh_incline_func, if_incepts_func, gh_incepts_func = PSHE.get_incline_of_no_lorentzian_line()

        difference_list = []

        if os.path.exists("/home/aoxv/code/Data/PSHE/inclines/diff_exp_to_the/if_shift_exp_to_the.npy") and (not update):
            print("Using existing IF data")
            difference_list = np.load("/home/aoxv/code/Data/PSHE/inclines/diff_exp_to_the/if_shift_exp_to_the.npy")
        else:
            for ele_i in range(len(wavelengths)):

                ele_if_the_line_k = if_incline_func(actual_angles_list[ele_i])
                ele_if_the_line_b = if_incepts_func(actual_angles_list[ele_i])

                ele_if_the_line_func = PubMeth.line_incline_incept(ele_if_the_line_k, ele_if_the_line_b)

                target_x = if_xbar_list[ele_i]

                target_if_shift = ele_if_the_line_func(target_x)

                diff_between_exp_the = target_if_shift - if_ybar_list[ele_i]

                difference_list.append(diff_between_exp_the)
            np.save("/home/aoxv/code/Data/PSHE/inclines/diff_exp_to_the/if_shift_exp_to_the.npy", difference_list)

        return difference_list

    @staticmethod
    def shift_of_exp_gh_to_the(update=False):
        """
        The amount of shift we should do to the IF shift to make it correspond to the theory.
        """
        gh_wls, gh_shifts = PSHE.read_mos2_gh_shift_data()
        gh_xbar_list, gh_ybar_list = PSHE.get_exp_gh_center()

        actual_angles_list = PSHE.std_if_gh_to_get_actual_angles()

        if_incline_func, gh_incline_func, if_incepts_func, gh_incepts_func = PSHE.get_incline_of_no_lorentzian_line(update=update)

        difference_list = []

        if os.path.exists("/home/aoxv/code/Data/PSHE/inclines/diff_exp_to_the/gh_shift_exp_to_the.npy") and (not update):
            print("Using existing GH data")
            difference_list = np.load("/home/aoxv/code/Data/PSHE/inclines/diff_exp_to_the/gh_shift_exp_to_the.npy")
        else:
            for ele_i in range(len(gh_wls)):

                ele_gh_the_line_k = gh_incline_func(actual_angles_list[ele_i])
                ele_gh_the_line_b = gh_incepts_func(actual_angles_list[ele_i])

                ele_gh_the_line_func = PubMeth.line_incline_incept(ele_gh_the_line_k, ele_gh_the_line_b)

                target_x = gh_xbar_list[ele_i]

                target_gh_shift = ele_gh_the_line_func(target_x)

                diff_between_exp_the = target_gh_shift - gh_ybar_list[ele_i]

                difference_list.append(diff_between_exp_the)
            np.save("/home/aoxv/code/Data/PSHE/inclines/diff_exp_to_the/gh_shift_exp_to_the.npy", difference_list)

        return difference_list

    @staticmethod
    def convert_2d_sigma_to_permittivity(energy_range, sigma_tilde, thickness_d=0.7):
        """
        Convert 2d conductivity to permittivity

        The unit of thickness should be nm
        """
        ##  Convert energy to omega
        omega_range = PubMeth.convert_e_to_omega(energy_range)

        ##  Convert thickness to m
        thickness_d = thickness_d * 1e-9

        ##  epsilon infty for MoS2
        eps_infty = 15.6

        ##  Calculate 3d permittivity
        epsilon_out = eps_infty + 1j * sigma_tilde * c_speed / (omega_range * thickness_d)

        return epsilon_out

    @staticmethod
    def convert_permittivity_to_ref_index(complex_epsilon_in):
        """
        Convert the complex permittivity to refractive index
        """
        modulus_e = abs(complex_epsilon_in)

        angle_permittivity = np.angle(complex_epsilon_in)

        half_angle = angle_permittivity / 2 ##  arc unit

        n = sqrt(modulus_e) * cos(half_angle)
        k = sqrt(modulus_e) * sin(half_angle)

        return n, k

    @staticmethod
    def diff_if_gh_exp_data():
        """
        Calculate the differential experimental results of IF and GH shift
        """
        wavelengths, if_shifts = PSHE.read_mos2_if_shift_data()
        gh_wls, gh_shifts = PSHE.read_mos2_gh_shift_data()

        for ele_i in range(len(if_shifts)):
            diff_if_shift = np.diff(if_shifts[ele_i]) / np.diff(wavelengths[ele_i])
            diff_gh_shift = np.diff(gh_shifts[ele_i]) / np.diff(gh_wls[ele_i])

            fig, ax_diff_if = plt.subplots()
            ax_diff_if.plot(wavelengths[ele_i][:-1], diff_if_shift, "--")
            ax_diff_if.plot(wavelengths[ele_i][:-1], 0 * arange(len(diff_if_shift)))
            ax_diff_if.set_aspect('auto')
            ax_diff_if.set_xlabel('$\lambda$ (nm)', fontsize=12)
            ax_diff_if.set_ylabel('Differential IF', fontsize=12)
            ax_diff_if.set_title('', fontsize=14)
            ax_diff_if.set_xlim(ax_diff_if.get_xlim())
            ax_diff_if.set_ylim(ax_diff_if.get_ylim())
            ax_diff_if.legend([])
            fig.savefig(data_file_dir + "PSHE/exp_ob_IF/diff_sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            plt.close()

            fig, ax_diff_gh = plt.subplots()
            ax_diff_gh.plot(gh_wls[ele_i][:-1], diff_gh_shift, "--")
            ax_diff_if.plot(gh_wls[ele_i][:-1], 0 * arange(len(diff_gh_shift)))
            ax_diff_gh.set_aspect('auto')
            ax_diff_gh.set_xlabel('$\lambda$ (nm)', fontsize=12)
            ax_diff_gh.set_ylabel('Differential GH', fontsize=12)
            ax_diff_gh.set_title('', fontsize=14)
            ax_diff_gh.set_xlim(ax_diff_gh.get_xlim())
            ax_diff_gh.set_ylim(ax_diff_gh.get_ylim())
            ax_diff_gh.legend([])
            fig.savefig(data_file_dir + "PSHE/exp_ob_GH/diff_sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            plt.close()

        return

    @staticmethod
    def smooth_line():
        """
        Use the algorithm to smooth the experimental result of IF and GH shift
        """
        window_length = 15
        poly_order = 3

        wavelengths, if_shifts = PSHE.read_mos2_if_shift_data()
        gh_wls, gh_shifts = PSHE.read_mos2_gh_shift_data()

        for ele_i in range(len(if_shifts)):

            if_smooth = savgol_filter(if_shifts[ele_i], window_length, poly_order)
            print(len(if_smooth))
            diff_if_smooth = np.diff(if_smooth)

            fig, ax_smooth = plt.subplots()
            ax_smooth.plot(wavelengths[ele_i], if_shifts[ele_i])
            ax_smooth.plot(wavelengths[ele_i], if_smooth)
            ax_smooth.set_aspect('auto')
            ax_smooth.set_xlabel('$\lambda$ (nm)', fontsize=12)
            ax_smooth.set_ylabel('IF shift (nm)', fontsize=12)
            ax_smooth.set_title('Sample {}'.format(ele_i + 1), fontsize=14)
            ax_smooth.set_xlim(ax_smooth.get_xlim())
            ax_smooth.set_ylim(ax_smooth.get_ylim())
            ax_smooth.legend(["Original", "Smoothed"])
            fig.savefig(data_file_dir + "PSHE/exp_ob_IF/smooth_sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            plt.close()

            fig, ax_smooth = plt.subplots()
            ax_smooth.plot(wavelengths[ele_i][:-1], diff_if_smooth, "--")
            ax_smooth.plot(wavelengths[ele_i][:-1], 0 * arange(len(diff_if_smooth)))
            ax_smooth.set_aspect('auto')
            ax_smooth.set_xlabel('$\lambda$ (nm)', fontsize=12)
            ax_smooth.set_ylabel('Differential IF', fontsize=12)
            ax_smooth.set_title('Sample {}'.format(ele_i + 1), fontsize=14)
            ax_smooth.set_xlim(ax_smooth.get_xlim())
            ax_smooth.set_ylim(ax_smooth.get_ylim())
            fig.savefig(data_file_dir + "PSHE/exp_ob_IF/diff_smooth_sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            plt.close()

        return

    @staticmethod
    def read_the_exciton_energy(file_path="/home/aoxv/code/Data/PSHE/exciton_energy/exciton_energy.csv"):
        data = pd.read_csv(file_path)

        exciton_elist = data["E"] * 1000

        A_exciton_e = 1240 / 680 * 1000 #   meV
        shift = A_exciton_e - exciton_elist[0]

        shift_excitons = array(exciton_elist) + shift

        # shift_wls =

        print(shift_excitons)
        print()

        return list(exciton_elist)


    # @staticmethod
    # def comp_gh_if_incline_with_exp():
    #     """
    #     Get the incline of the GH and IF shift based on the IF shift and then find the angle
    #     """
    #     interp_IF_angle_func, interp_GH_incline_func = PSHE.get_incline_of_no_lorentzian_line()

    #     wls_points = 1000

    #     ##  Get the interpolated n0 over specific wavelength range
    #     dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
    #     dense_energy = 1240 / dense_wls * 1000

    #     ##  Get the incline based on the least standard deviations
    #     k_incline_exp_list = PSHE.std_of_if_from_line_through_center()

    #     ##  Get the center of IF and GH shifts
    #     if_xbar_list, if_ybar_list = PSHE.get_exp_if_center()
    #     gh_xbar_list, gh_ybar_list = PSHE.get_exp_gh_center()

    #     ##  Experiment data
    #     gh_wls_list, gh_shift_list = PSHE.read_mos2_if_shift_data()
    #     gh_wls_list, gh_shift_list = PSHE.read_mos2_gh_shift_data()

    #     for ele_i in range(len(gh_wls_list)):
    #         ##  IF center
    #         if_center = (if_xbar_list[ele_i], if_ybar_list[ele_i])
    #         gh_center = (gh_xbar_list[ele_i], gh_ybar_list[ele_i])

    #         ele_k_incline_exp = k_incline_exp_list[ele_i]   ##  IF incline

    #         angle_of_if = interp_IF_angle_func(ele_k_incline_exp)   ##  Get the angle of the experiment

    #         print("The actual IF angle should be: ", angle_of_if)

    #         ##  Get the GH incline
    #         gh_incline = interp_GH_incline_func(angle_of_if)

    #         ##  GH line function
    #         gh_line_func = PubMeth.line_through_dot(gh_center, gh_incline)

    #         ##  IF Plot
    #         fig, ax_gh = plt.subplots()
    #         ax_gh.plot(gh_wls_list[ele_i], gh_shift_list[ele_i])
    #         ax_gh.plot(gh_wls_list[ele_i], gh_line_func(gh_wls_list[ele_i]))
    #         ax_gh.set_aspect('auto')
    #         ax_gh.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
    #         ax_gh.set_ylabel('GH (nm)', fontsize=12)
    #         ax_gh.set_title('Sample {}'.format(ele_i + 1), fontsize=14)
    #         ax_gh.set_xlim(ax_gh.get_xlim())
    #         ax_gh.set_ylim(ax_gh.get_ylim())
    #         fig.savefig(data_file_dir + "PSHE/exp_ob_GH/incline_comp/comp_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
    #         fig.savefig(data_file_dir + ".pdf", dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
    #         plt.close()

    #     return


def main():
    MoS2Data(0.65, 5).plot_exp_data_in_one_plot()
    return


if __name__ == "__main__":
    main()
