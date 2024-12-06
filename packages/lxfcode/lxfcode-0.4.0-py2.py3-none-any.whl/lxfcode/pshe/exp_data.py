from pkg_import.pkg_import import *
from pshe.optics import WaveLength


class ExpData:
    _instance = None
    _init_flag = False

    def __init__(
        self, if_shift_dir, gh_shift_dir, thickness, permittivity_infty
    ) -> None:
        if self._init_flag:
            print("Already existing object: ", self.__class__.__name__)
            return
        else:
            self._if_shift_dir = if_shift_dir
            self._gh_shift_dir = gh_shift_dir
            self._if_samples_names = os.listdir(self._if_shift_dir)
            self._gh_samples_names = os.listdir(self._gh_shift_dir)
            self._file_num = len(self._if_samples_names)
            self.if_wls_list, self.if_shifts_list = self.load_exp_data(
                self._if_shift_dir, self._if_samples_names
            )
            self.gh_wls_list, self.gh_shifts_list = self.load_exp_data(
                self._gh_shift_dir, self._gh_samples_names
            )
            self.if_centers, self.if_inclines = self.centers_of_exp_curve(
                self.if_wls_list, self.if_shifts_list
            )
            self.gh_centers, self.gh_inclines = self.centers_of_exp_curve(
                self.gh_wls_list, self.gh_shifts_list
            )

            ##  Core parameters
            self.thickness = thickness
            self.permittivity_infty = permittivity_infty

            ##  Pre-executed functions
            self.plot_exp_data()

            self._init_flag = True

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            print("Single object created: ", cls._instance.__class__.__name__)
            return cls._instance
        else:
            return cls._instance

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

    def plot_exp_data(self):
        """Plot exp data"""
        print("Plotting experiment results of {}.".format(self.__class__.__name__))
        for ele_i in range(self._file_num):
            PlotMethod(
                self.if_wls_list[ele_i],
                self.if_shifts_list[ele_i],
                r"$\lambda$ (nm)",
                "IF shift (nm)",
                title="Sample {}".format(ele_i + 1),
                save_dir="IF/exp/{}".format(self.__class__.__name__),
                save_name="sample_{}".format(ele_i + 1),
            ).line_plot()
            PlotMethod(
                self.gh_wls_list[ele_i],
                self.gh_shifts_list[ele_i],
                r"$\lambda$ (nm)",
                "GH shift (nm)",
                title="Sample {}".format(ele_i + 1),
                save_dir="GH/exp/{}".format(self.__class__.__name__),
                save_name="sample_{}".format(ele_i + 1),
            ).line_plot()

        return


class MoS2Data:
    __Wu_cond_file_path = data_file_dir + "00_common_sense/Wu_cond_original.csv"
    __refractive_indexes_dir = "/home/aoxv/code/Data/00_common_sense/exp_indices/"
    __refractive_indexes_name = os.listdir(__refractive_indexes_dir)
    __exp_if_shift_dir = "/home/aoxv/code/Data/00_exp_data/IF_shift/MoS2/"
    __if_samples_names = os.listdir(__exp_if_shift_dir)
    __exp_gh_shift_dir = "/home/aoxv/code/Data/00_exp_data/GH_shift/MoS2/"
    __gh_samples_names = os.listdir(__exp_gh_shift_dir)
    _bg_if_gh_data = "/home/aoxv/code/Data/00_exp_data/Base_shift_BK7/bg_shift.xlsx"

    unit_sigma_eps0_x_c = eps0_x_c
    unit_sigma_e2_over_h = c_eV**2 / h_planck

    permittivity_infty = 15.6

    _instance = None
    _init_flag = False

    def __init__(self, thickness=0.65, sample_num=5) -> None:
        if self._init_flag:
            return
        else:
            # Preload data
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

            (
                self.if_wls_list,
                self.if_shifts_list,
                self.lcp_shifts,
                self.rcp_shifts,
            ) = self.load_exp_data(self.__exp_if_shift_dir, self.__if_samples_names)
            (
                self.gh_wls_list,
                self.gh_shifts_list,
                self.s_shifts,
                self.p_shifts,
            ) = self.load_exp_data(self.__exp_gh_shift_dir, self.__gh_samples_names)
            print("Time to load data: ", time.perf_counter() - t1)

            self.if_centers, self.if_inclines = self.centers_of_exp_curve(
                self.if_wls_list, self.if_shifts_list
            )
            self.gh_centers, self.gh_inclines = self.centers_of_exp_curve(
                self.gh_wls_list, self.gh_shifts_list
            )

            self.s_centers = self.centers_of_exp_curve(self.gh_wls_list, self.s_shifts)[
                0
            ]
            self.p_centers = self.centers_of_exp_curve(self.gh_wls_list, self.p_shifts)[
                0
            ]

            self.bg_wls, self.bg_gh, self.bg_if = self.load_bg_if_gh_shift()

            self.if_collections = self.plot_exp_data_in_one_plot()

            # Instance parameters
            self.thickness = thickness  # nm

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
            n_list.append(array(ele_data["n"]))  # dimensionless
            k_list.append(array(ele_data["k"]))  # dimensionless
            complex_ref_index_list.append(
                array(ele_data["n"] + 1j * ele_data["k"])
            )  # dimensionless

        return wls_list, complex_ref_index_list

    @staticmethod
    def load_exp_data(exp_dir, exp_names):
        wls_list = []
        shifts_list = []
        ele_shift1_list = []
        ele_shift2_list = []

        for ele_sample in exp_names:
            ele_data = ExcelMethod(exp_dir + ele_sample).read_xlsx_data(0, 0)
            ele_wls, ele_shift = WaveLength().get_sifted_data(ele_data[0], ele_data[3])

            ele_shift1 = WaveLength().get_sifted_data(ele_data[0], ele_data[1])[1]
            ele_shift2 = WaveLength().get_sifted_data(ele_data[0], ele_data[2])[1]

            ele_shift1_list.append(ele_shift1)
            ele_shift2_list.append(ele_shift2)

            wls_list.append(ele_wls)
            shifts_list.append(ele_shift)

        return wls_list, shifts_list, ele_shift1_list, ele_shift2_list

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
            array(self.if_shifts_list[ele_i]) + if_mean_ybar - self.if_centers[ele_i][1]
            for ele_i in range(self.sample_num)
        ]

        shifted_exp_gh_collections = [
            array(self.gh_shifts_list[ele_i]) + gh_mean_ybar - self.gh_centers[ele_i][1]
            for ele_i in range(self.sample_num)
        ]

        PlotMethod(
            self.if_wls_list,
            shifted_exp_if_collections,
            r"$\lambda$ (nm)",
            "IF shift (nm)",
            title="Experimental observations of IF shift",
            save_name="if_collection",
            legend=["Sample {}".format(ele_i + 1) for ele_i in range(self.sample_num)],
            save_dir="IF/exp",
        ).multiple_line_one_plot()

        PlotMethod(
            self.gh_wls_list,
            shifted_exp_gh_collections,
            r"$\lambda$ (nm)",
            "GH shift (nm)",
            title="Experimental observations of GH shift",
            save_name="gh_collection",
            legend=["Sample {}".format(ele_i + 1) for ele_i in range(self.sample_num)],
            save_dir="GH/exp",
        ).multiple_line_one_plot()

        return shifted_exp_if_collections, shifted_exp_gh_collections


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
        # Read the refractive index of BK-7 from database
        data_list = PubMeth.read_xlsx_data(cls.BK7_file_path, exclude_rows_num=1)

        wave_length_n0 = data_list[0]
        ref_index_n0 = array(data_list[1]) + 1j * zeros(len(data_list[1]))
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        # fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), wls_points)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        return dense_wls, dense_energy, dense_n0_index, f_n0


class WS2Data(ExpData):
    def __init__(
        self,
        if_shift_dir="/home/aoxv/code/Data/00_exp_data/IF_shift/WS2/",
        gh_shift_dir="/home/aoxv/code/Data/00_exp_data/GH_shift/WS2/",
        thickness=0.618,
        permittivity_infty=13.6,
    ) -> None:
        super().__init__(if_shift_dir, gh_shift_dir, thickness, permittivity_infty)


def main():
    data_mos2 = MoS2Data()
    cond = real(data_mos2.Wu_cond_complex_as_eps_x_c)
    wls = 1240 / data_mos2.Wu_energy_original * 1000
    PlotMethod(
        wls,
        cond,
        r"$\lambda$ (nm)",
        r"$\mathrm{Re}[\sigma/\varepsilon_0 c]$",
        x_lim=[500, 700],
        title="Reduced conductivity (Phys. Rev. B 91, 075310 (2015))",
        save_dir="Conductivity/Wu",
        save_name="wu_cond_lambda",
    ).line_plot()
    return


if __name__ == "__main__":
    main()
