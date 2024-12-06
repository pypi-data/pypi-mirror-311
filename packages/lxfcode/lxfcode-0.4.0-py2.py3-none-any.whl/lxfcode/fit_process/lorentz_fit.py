from pkg_import.pkg_import import *
from pshe.exp_data import BK7Substrate, MoS2Data
from pshe.if_calculation import IFCalculation
from pshe.gh_calculation import GHCalculation
from pshe.optics import *
from fit_process.eigen_shifts import EigenShiftDifference, BackgroundShift


class LorentzFitProcess:
    _base_init_flag = False
    # _instance = None

    _start_wls = 496
    _end_wls = 697

    def __init__(
        self,
        centers_0,
        amps_0,
        gammas_0,
        bottom_bound,
        top_bound,
        incident_angle_0,
        exp_data_ob=MoS2Data(),
    ) -> None:
        if self._base_init_flag:
            print("Already exist basic initiation parameters...")
            print("Loading new parameters of centers, amplitudes and gammas")

            return
        else:
            self.BK7_substrate = BK7Substrate()
            self.exp_data = exp_data_ob

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

        self.eigen_shifts = EigenShiftDifference(incident_angle_0)
        self.backgrounds = BackgroundShift(incident_angle_0, exp_data_ob=exp_data_ob)

        ##  shifted if and gh based on conductivity or permittivity
        self.shifted_if_exp_conductivity_based = (
            self.backgrounds.shifted_exp_if_cond_based()
        )
        self.shifted_gh_exp_conductivity_based = (
            self.backgrounds.shifted_exp_gh_cond_based()
        )
        self.shifted_if_exp_permittivity_based = (
            self.backgrounds.shifted_exp_if_perm_based()
        )
        self.shifted_gh_exp_permittivity_based = (
            self.backgrounds.shifted_exp_gh_perm_based()
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
            self.exp_data.permittivity_infty
        ).lorentzian_combination_to_perm(energy, centers, amps, gammas)
        complex_refractive_index = ComplexRefractiveIndex(
            complex_permittivity
        ).complex_refractive_index

        if_shift = (
            self.rcp_if.thin_film_model(
                wls, complex_refractive_index, self.exp_data.thickness
            )[1]
            - self.lcp_if.thin_film_model(
                wls, complex_refractive_index, self.exp_data.thickness
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
            self.exp_data.permittivity_infty
        ).lorentzian_combination_to_perm(energy, centers, amps, gammas)
        complex_refractive_index = ComplexRefractiveIndex(
            complex_permittivity
        ).complex_refractive_index

        gh_shift = (
            self.p_gh.thin_film_model(
                wls, complex_refractive_index, self.exp_data.thickness
            )[1]
            - self.s_gh.thin_film_model(
                wls, complex_refractive_index, self.exp_data.thickness
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
        # self._find_best_if_theta0(sample_index)
        exp_if_wls = self.exp_data.if_wls_list[sample_index]
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
        # self._find_best_if_theta0(sample_index)
        exp_if_wls = self.exp_data.if_wls_list[sample_index]
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
        # self._find_best_gh_theta0(sample_index)
        exp_gh_wls = self.exp_data.gh_wls_list[sample_index]
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
        # self._find_best_gh_theta0(sample_index)
        exp_gh_wls = self.exp_data.gh_wls_list[sample_index]
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
        shift_ob = EigenShiftDifference(angle_list)
        ##  Incline and intercept of different background line corresponding to different incident angles
        kb_arr = shift_ob.kb_of_lcp_rcp_bg_conductivity_if_shift()

        ##  Functions of the background line
        func_list = [Functions.linear_func_fixed_pars(1, *ele_kb) for ele_kb in kb_arr]

        ##  Standard deviations between background line and the experimental observations (different incident angles)
        std_arr = FitMethod.std_between_two_curves(
            [
                line_func(self.exp_data.if_wls_list[sample_index])
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
        shift_diff = EigenShiftDifference(angle_list)
        ##  Incline and intercept of different background line corresponding to different incident angles
        kb_arr = shift_diff.kb_of_s_p_bg_conductivity_gh_shift()

        ##  Functions of the background line
        func_list = [Functions.linear_func_fixed_pars(1, *ele_kb) for ele_kb in kb_arr]

        ##  Standard deviations between background line and the experimental observations (different incident angles)
        std_arr = FitMethod.std_between_two_curves(
            [
                line_func(self.exp_data.gh_wls_list[sample_index])
                for line_func in func_list
            ],
            self.shifted_gh_exp_conductivity_based[sample_index][0],
        )

        ##  Find the minimum and get the actual incident angle
        best_angle = list(angle_list)[list(std_arr).index(min(std_arr))]

        print("best gh incident angle: ", best_angle / pi * 180)

        return
