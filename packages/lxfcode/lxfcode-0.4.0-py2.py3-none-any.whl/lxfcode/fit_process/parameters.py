from pkg_import.pkg_import import *
from pshe.optics import LorentzOscillator
from pshe.exp_data import WS2Data, MoS2Data


class LorentzFitParameters:
    def __init__(
        self,
        bottom_e=1840,
        top_e=2400,
        incident_angles=(pi / 4,),
        centers_top_bot_limit_list=None,
        amps_top_bot_limit_list=None,
        gammas_top_bot_limit_list=None,
        exp_dat_ob=MoS2Data(),
    ) -> None:
        self.bottom_e = bottom_e
        self.top_e = top_e
        self.centers = arange(bottom_e, top_e, 50)
        self.lorentz_len = len(self.centers)
        self.amps = [0.2] * self.lorentz_len
        self.gammas = [25] * self.lorentz_len
        self.exp_dat_ob = exp_dat_ob
        print("Type of Data: ", exp_dat_ob.__class__.__name__)

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

        self.fitted_files_save_dir = (
            data_file_dir + "/FitFiles/" + exp_dat_ob.__class__.__name__ + "/"
        )

    def get_pars(self):
        return (
            self.centers,
            self.amps,
            self.gammas,
            self.bot_bound,
            self.top_bound,
            self.theta_0s,
        )

    def _return_pars(self, centers, amps, gammas, bot_bound, top_bound):
        return (
            centers,
            amps,
            gammas,
            bot_bound,
            top_bound,
            self.theta_0s,
            self.exp_dat_ob,
        )

    def load_fitted_pars(self, save_name, sample_i):
        pars = np.load(
            self.fitted_files_save_dir + save_name + "_{}.npy".format(sample_i)
        )
        centers, amps, gammas = [pars[ele_i, :] for ele_i in range(3)]
        return centers, amps, gammas

    @staticmethod
    def pars_format(centers_fit, amps_fit, gammas_fit):
        amplitudes = LorentzOscillator(centers_fit, amps_fit, gammas_fit).amplitudes

        pars_tuples = [
            "({:.2f}, {:.2f}, {:.2f}, {:.2f})\n".format(
                1240 / centers_fit[i] * 1000,
                centers_fit[i],
                amplitudes[i],
                gammas_fit[i],
            )
            for i in range(len(centers_fit))
        ]

        out_text = (
            "Parameters: \n($\lambda$ (nm), $E$ (meV), Amplitude, Broadening (meV))\n"
            + "".join(pars_tuples)
        )

        return out_text

    def get_if_fixed_pars_cond_based(self):
        """
        Get the peaks pre-fixed for conductivity model
        """
        centers = [
            1820,
            1925,
            1990,
            2030,
            2140,
            2190,
            2365,
        ]

        amps = [0.2] * len(centers)
        gammas = [25] * len(centers)

        centers_top_limit = [centers[ele_i] + 10 for ele_i in range(len(centers))]
        centers_bot_limit = [centers[ele_i] - 10 for ele_i in range(len(centers))]

        amps_top_limit = [1] * len(centers)
        amps_bot_limit = [0.2] * len(centers)

        gamma_top_limit = [150] * len(centers)
        gamma_bot_limit = [25] * len(centers)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return self._return_pars(centers, amps, gammas, bot_bound, top_bound)

    def get_gh_fixed_pars_cond_based(self):
        """
        Fix the GH parameters to launch fit.
        """
        centers = [1815, 1875, 1915, 1965, 2065, 2153, 2230, 2354]

        amps = [0.2] * len(centers)
        gammas = [25] * len(centers)

        centers_top_limit = [centers[ele_i] + 10 for ele_i in range(len(centers))]
        centers_bot_limit = [centers[ele_i] - 10 for ele_i in range(len(centers))]

        amps_top_limit = [1] * len(centers)
        amps_bot_limit = [0.2] * len(centers)

        gamma_top_limit = [150] * len(centers)
        gamma_bot_limit = [25] * len(centers)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return self._return_pars(centers, amps, gammas, bot_bound, top_bound)

    def get_if_fixed_pars_perm_based(self):
        """
        Get the peaks pre-fixed for permittivity model
        """
        if type(self.exp_dat_ob) == MoS2Data:
            centers = [
                1820,
                1925,
                1990,
                2030,
                2100,
                2140,
                2190,
                2300,
                2365,
            ]
        elif type(self.exp_dat_ob) == WS2Data:
            centers = [1835, 2000, 2085, 2255, 2385]

        amps = [2] * len(centers)
        gammas = [25] * len(centers)

        centers_top_limit = [centers[ele_i] + 10 for ele_i in range(len(centers))]
        centers_bot_limit = [centers[ele_i] - 10 for ele_i in range(len(centers))]

        amps_top_limit = [5] * len(centers)
        amps_bot_limit = [2] * len(centers)

        gamma_top_limit = [150] * len(centers)
        gamma_bot_limit = [25] * len(centers)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return self._return_pars(centers, amps, gammas, bot_bound, top_bound)

    def get_gh_fixed_pars_perm_based(self):
        """
        Fix the GH parameters to launch fit.
        """
        if type(self.exp_dat_ob) == MoS2Data:
            centers = [1815, 1875, 1915, 1965, 2065, 2153, 2230, 2354]
        elif type(self.exp_dat_ob) == WS2Data:
            centers = [1835, 2005, 2100, 2255, 2410]

        amps = [2] * len(centers)
        gammas = [25] * len(centers)

        centers_top_limit = [centers[ele_i] + 10 for ele_i in range(len(centers))]
        centers_bot_limit = [centers[ele_i] - 10 for ele_i in range(len(centers))]

        amps_top_limit = [5] * len(centers)
        amps_bot_limit = [2] * len(centers)

        gamma_top_limit = [150] * len(centers)
        gamma_bot_limit = [25] * len(centers)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return self._return_pars(centers, amps, gammas, bot_bound, top_bound)

    def get_if_fixed_pars_perm_based_mod(self):
        """
        Get the peaks pre-fixed for permittivity model
        """
        e_span = 30
        if type(self.exp_dat_ob) == MoS2Data:
            centers = [
                1918,
                2070,
                2125,
                2146,
                2156,
                2163,
                2066,
                2243,
                2300,
                2323,
                2333,
                # 2342,
            ]
            centers = np.array(centers) - 100
        elif type(self.exp_dat_ob) == WS2Data:
            centers = [1835, 2000, 2085, 2255, 2385]

        amps = [2] * len(centers)
        gammas = [25] * len(centers)

        centers_top_limit = [centers[ele_i] + e_span for ele_i in range(len(centers))]
        centers_bot_limit = [centers[ele_i] - e_span for ele_i in range(len(centers))]

        amps_top_limit = [5] * len(centers)
        amps_bot_limit = [2] * len(centers)

        gamma_top_limit = [150] * len(centers)
        gamma_bot_limit = [25] * len(centers)

        bot_bound = centers_bot_limit + amps_bot_limit + gamma_bot_limit
        top_bound = centers_top_limit + amps_top_limit + gamma_top_limit

        return self._return_pars(centers, amps, gammas, bot_bound, top_bound)
