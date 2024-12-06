from fit_process.eigen_shifts import EigenShiftDifference
from fit_process.lorentz_fit import LorentzFitProcess
from fit_process.parameters import LorentzFitParameters
from pshe.exp_data import *
from pshe.optics import *
from pshe.if_calculation import IFCalculation
from pshe.gh_calculation import GHCalculation


class FitCore:
    def __init__(
        self,
        incident_angles=None,
        pars_type: Literal[
            "default",
            "if_fixed",
            "gh_fixed",
            "perm_if_fixed",
            "perm_gh_fixed",
            "perm_if_mod",
        ] = "default",
        exp_dat_ob=MoS2Data(),
        sub_dat_ob=BK7Substrate(),
    ) -> None:
        if incident_angles is None:
            incident_angles = [pi / 4]
        self.theta_0s = incident_angles

        self.eigen_shifts = EigenShiftDifference(self.theta_0s)

        if pars_type == "if_fixed":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters(
                    exp_dat_ob=exp_dat_ob
                ).get_if_fixed_pars_cond_based()
            )
        # elif pars_type == "optimized":
        #     self.lorentz_fit_process = LorentzFitProcess(
        # *LorentzFitParameters().get_if_optimized_pars()
        #     )
        elif pars_type == "gh_fixed":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters(
                    exp_dat_ob=exp_dat_ob
                ).get_gh_fixed_pars_cond_based()
            )
        elif pars_type == "perm_if_fixed":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters(
                    exp_dat_ob=exp_dat_ob
                ).get_if_fixed_pars_perm_based()
            )
        elif pars_type == "perm_gh_fixed":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters(
                    exp_dat_ob=exp_dat_ob
                ).get_gh_fixed_pars_perm_based()
            )
        elif pars_type == "perm_if_mod":
            self.lorentz_fit_process = LorentzFitProcess(
                *LorentzFitParameters(
                    exp_dat_ob=exp_dat_ob
                ).get_if_fixed_pars_perm_based_mod()
            )
        # elif pars_type == "default":
        #     self.lorentz_fit_process = LorentzFitProcess(
        #         *LorentzFitParameters().get_pars()
        #     )
        # elif pars_type == "permittivity":
        #     self.lorentz_fit_process = LorentzFitProcess(
        #         *LorentzFitParameters().get_permittivity_pars()
        #     )
        # elif pars_type == "permittivity_optimized":
        #     self.lorentz_fit_process = LorentzFitProcess(
        #         *LorentzFitParameters().get_permittivity_optimized_pars()
        #     )

        self.exp_dat_ob = exp_dat_ob
        self.sub_dat_ob = sub_dat_ob
        self._fit_file_path = (
            data_file_dir + "/FitFiles/" + exp_dat_ob.__class__.__name__ + "/"
        )
        if not os.path.exists(self._fit_file_path):
            os.makedirs(self._fit_file_path)
        pass

    def _find_fit_pars(self, file_name):
        """
        Find the numpy files in the target directory.
        """
        exist1 = not os.path.exists(self._fit_file_path + file_name + ".npy")
        exist2 = not os.path.exists(
            os.path.dirname(self._fit_file_path) + os.sep + file_name + ".npy"
        )

        return exist1 or exist2

    def _save_fit_pars(self, centers, amps, gammas, save_name):
        """
        Save the fitted parameters
        """
        pars = array([centers, amps, gammas])

        np.save(self._fit_file_path + save_name, pars)

        return

    def _load_fit_pars(self, save_name):
        """
        load fit parameters
        """
        out_load = np.load(self._fit_file_path + save_name)
        centers, amps, gammas = [out_load[ele_i, :] for ele_i in range(3)]

        return centers, amps, gammas

    def post_plot(
        self,
        fit_base,
        centers_fit,
        amps_fit,
        gammas_fit,
        sample_index,
        save_name,
    ):
        def post_treatment(
            shift_class: IFCalculation | GHCalculation, base_type, fit_type, wls, shift
        ):
            if base_type == "cond":
                if fit_type == "if":
                    exp_wls = self.exp_dat_ob.if_wls_list[sample_index]
                    shifted_exp_data = (
                        self.lorentz_fit_process.shifted_if_exp_conductivity_based[
                            sample_index
                        ][0]
                    )
                elif fit_type == "gh":
                    exp_wls = self.exp_dat_ob.gh_wls_list[sample_index]
                    shifted_exp_data = (
                        self.lorentz_fit_process.shifted_gh_exp_conductivity_based[
                            sample_index
                        ][0]
                    )
            elif base_type == "perm":
                if fit_type == "if":
                    exp_wls = self.exp_dat_ob.if_wls_list[sample_index]
                    shifted_exp_data = (
                        self.lorentz_fit_process.shifted_if_exp_permittivity_based[
                            sample_index
                        ][0]
                    )
                elif fit_type == "gh":
                    exp_wls = self.exp_dat_ob.gh_wls_list[sample_index]
                    shifted_exp_data = (
                        self.lorentz_fit_process.shifted_gh_exp_permittivity_based[
                            sample_index
                        ][0]
                    )
            fig, ax = shift_class.post_treatment(
                [wls[0], exp_wls],
                [
                    shift[0],
                    shifted_exp_data,
                ],
                theta_0s=self.theta_0s,
                save_name="{}_sample_{}".format(save_name, sample_index),
                legend=["Theoretical Fit", "Experimental result"],
                text=annotation_text,
                text_xy=(1.1, -0.03),
                text_annotate=True,
                sub_save_dir="fit",
                title="Sample {}".format(sample_index + 1),
                line_type=["-", "."],
                ax_return=True,
                colors=["#000000", "#D25F27"],
            )

            return fig, ax

        E_fit_range = linspace(1500, 2500, 400)
        wls_fit_range = 1240 / E_fit_range * 1000

        annotation_text = LorentzFitParameters.pars_format(
            centers_fit, amps_fit, gammas_fit
        )

        ##  No Lorentzian peak information
        annotation_text = ""

        lorentz_osci = LorentzOscillator(
            centers_fit,
            amps_fit,
            gammas_fit,
            E_fit_range,
            times_i=True,
            x_label="E (meV)",
            y_label=r"$\sigma/\varepsilon_0 c$",
        )

        lorentz_osci.lorentz_plot(
            save_name="{}_sample_{}".format(save_name, sample_index),
            save_dir="fit",
            text=annotation_text,
        )

        if fit_base == "cond":
            if_wls, if_shift = self.eigen_shifts.lcp_rcp_if_lorentz_conductivity(
                centers_fit[:-1], amps_fit[:-1], gammas_fit[:-1]
            )
            gh_wls, gh_shift = self.eigen_shifts.s_p_gh_lorentz_conductivity(
                centers_fit, amps_fit, gammas_fit
            )
            # reduced_sigma = real(lorentz_osci.real_part)
            reduced_sigma = real(np.sum(lorentz_osci.components_list()[:-1], axis=0))
        elif fit_base == "perm":
            perm_ob = Permittivity(self.exp_dat_ob.permittivity_infty)

            reduced_sigma = real(
                perm_ob.lorentz_combi_to_sigma_2d(
                    E_fit_range,
                    centers_fit[:-1],
                    amps_fit[:-1],
                    gammas_fit[:-1],
                    self.exp_dat_ob.thickness,
                )
            )

            complex_refractive_index_fit = ComplexRefractiveIndex(
                perm_ob.lorentzian_combination_to_perm(
                    E_fit_range, centers_fit[:-1], amps_fit[:-1], gammas_fit[:-1]
                )
            ).complex_refractive_index

            if_wls, if_shift = self.eigen_shifts.lcp_rcp_if_thin_film(
                wls_fit_range, complex_refractive_index_fit, self.exp_dat_ob.thickness
            )
            gh_wls, gh_shift = self.eigen_shifts.s_p_gh_thin_film(
                wls_fit_range,
                complex_refractive_index_fit,
                self.exp_dat_ob.thickness,
                sample_index,
            )

        ##  Plot IF shift based on the fitted parameters
        fig_if, ax_if = post_treatment(IFCalculation, fit_base, "if", if_wls, if_shift)
        ##  Plot GH shift based on the fitted parameters
        fig_gh, ax_gh = post_treatment(GHCalculation, fit_base, "gh", gh_wls, gh_shift)

        ##  Double-y plot for IF shift
        pMethod_IF = PlotExistingAxMethod(
            wls_fit_range,
            reduced_sigma,
            y_label=r"$\mathrm{Re}[\sigma/\varepsilon_0 c]$",
            line_type="--",
            color="#E49F23",
            save_dir="IF/CompareCollection/" + self.exp_dat_ob.__class__.__name__,
            save_name="{}_sample_{}".format(save_name, sample_index),
            existing_fig_ax=(fig_if, ax_if),
            y_lim=[0, 0.5],
            x_lim=[540, 700],
            legend=["Reduced conductivity"],
            title=r"$\Delta_{IF}^{+} - \Delta_{IF}^{-}$",
            ax_return=True,
        )
        fig_IF, ax_IF = pMethod_IF.twinx_existing_ax(twin_ax_return=True)

        if fit_base == "cond":
            sigma_y = lorentz_osci.components_list()
        elif fit_base == "perm":
            perm_ob = Permittivity(self.exp_dat_ob.permittivity_infty)
            sigma_y = perm_ob.lorentz_component_to_sigma_2d_list(
                E_fit_range,
                centers_fit,
                amps_fit,
                gammas_fit,
                self.exp_dat_ob.thickness,
            )
        # print(np.real(sigma_y[0]), wls_fit_range)

        A_series_lo = [np.real(sigma_y[0]), np.real(sigma_y[2]), np.real(sigma_y[3])]
        B_series_lo = [np.real(sigma_y[1]), np.real(sigma_y[4]), np.real(sigma_y[5])]
        for ele_A in A_series_lo:
            ax_IF.plot(wls_fit_range, ele_A, ":", color="#E11F25")
        for ele_B in B_series_lo:
            ax_IF.plot(wls_fit_range, ele_B, ":", color="#009E73")
        # ax_IF.plot([540, 620, 700], [180, 190, 200])

        print(pMethod_IF.save_png_path)
        fig_IF.savefig(
            pMethod_IF.save_png_path,
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )

        ##  Double-y plot for GH shift
        PlotExistingAxMethod(
            wls_fit_range,
            reduced_sigma,
            y_label=r"$\mathrm{Re}[\sigma/\varepsilon_0 c]$",
            line_type="--",
            color="red",
            save_dir="GH/CompareCollection/" + self.exp_dat_ob.__class__.__name__,
            save_name="{}_sample_{}".format(save_name, sample_index),
            existing_fig_ax=(fig_gh, ax_gh),
            y_lim=[0, 0.5],
            x_lim=[500, 700],
            legend=["Reduced conductivity"],
            title=r"$\Delta_{GH}^{s} - \Delta_{GH}^{p}$",
        ).twinx_existing_ax()

    def cond_fit_post(
        self,
        centers_fit,
        amps_fit,
        gammas_fit,
        sample_index,
        save_name,
    ):
        self.post_plot(
            "cond",
            centers_fit,
            amps_fit,
            gammas_fit,
            sample_index,
            save_name,
        )

    def perm_fit_post(
        self,
        centers_fit,
        amps_fit,
        gammas_fit,
        sample_index,
        save_name,
    ):
        self.post_plot(
            "perm",
            centers_fit,
            amps_fit,
            gammas_fit,
            sample_index,
            save_name,
        )

    def conductivity_based_fit(self, sample_index, save_name, fit_type, update=False):
        """
        Fit Experimental IF shift
        """
        ##  Fitted parameters
        file_name = save_name + "_{}".format(sample_index)
        if update or self._find_fit_pars(file_name):
            print("New calculation: ", save_name)
            if fit_type == "if":
                (
                    centers_fit,
                    amps_fit,
                    gammas_fit,
                ) = self.lorentz_fit_process.if_fit_conductivity_core(sample_index)
                self._save_fit_pars(
                    centers_fit, amps_fit, gammas_fit, save_name=file_name
                )
            elif fit_type == "gh":
                (
                    centers_fit,
                    amps_fit,
                    gammas_fit,
                ) = self.lorentz_fit_process.gh_fit_conductivity_core(sample_index)
                self._save_fit_pars(
                    centers_fit, amps_fit, gammas_fit, save_name=file_name
                )

        else:
            print("Fit done before, generating figures")
            centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        self.cond_fit_post(centers_fit, amps_fit, gammas_fit, sample_index, save_name)
        return centers_fit, amps_fit, gammas_fit

    def permittivity_based_fit(
        self, sample_index, save_name, shift_type, update=False, fig_generate=True
    ):
        """
        Fit Experimental IF shift
        """
        ##  Fitted parameters
        file_name = save_name + "_{}".format(sample_index)
        if update or self._find_fit_pars(file_name):
            print("New calculation.", save_name)
            if shift_type == "if":
                (
                    centers_fit,
                    amps_fit,
                    gammas_fit,
                ) = self.lorentz_fit_process.if_fit_permittivity_core(sample_index)
                self._save_fit_pars(
                    centers_fit, amps_fit, gammas_fit, save_name=file_name
                )
            elif shift_type == "gh":
                (
                    centers_fit,
                    amps_fit,
                    gammas_fit,
                ) = self.lorentz_fit_process.gh_fit_permittivity_core(sample_index)
                self._save_fit_pars(
                    centers_fit, amps_fit, gammas_fit, save_name=file_name
                )

        else:
            print("Fit done before, generating figures")
            centers_fit, amps_fit, gammas_fit = self._load_fit_pars(file_name + ".npy")

        if fig_generate:
            print("Generating figures.")
            self.perm_fit_post(
                centers_fit, amps_fit, gammas_fit, sample_index, save_name
            )

        return centers_fit, amps_fit, gammas_fit

    def collect_fit_conductivities_cond_based(
        self,
        prefix_name,
        num_files,
        save_name,
        y_label_list=None,
        save_dir="Conductivity",
    ):
        """
        Plot all the fitted conductivities together
        """
        save_dir = self.exp_dat_ob.__class__.__name__ + "/" + save_dir
        if y_label_list is None:
            y_label_list = [
                r"$\rm{Re}[\sigma/\varepsilon_0 c]$",
                r"$\rm{Im}[\sigma/\varepsilon_0 c]$",
            ]
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

    def collect_fit_conductivities_perm_based(
        self,
        prefix_name,
        num_files,
        save_name,
    ):
        """
        Plot all the fitted conductivities together
        """
        real_part_sigma = []
        imag_part_sigma = []
        n_list = []
        k_list = []
        diff_R_wls_list = []
        diff_Rs_list = []
        diff_Rp_list = []
        perm_real_list = []
        perm_imag_list = []
        energy_range = linspace(1500, 2500, 400)
        wls_range = 1240 / energy_range * 1000
        for ele_i in range(num_files):
            ele_file = prefix_name + "_{}.npy".format(ele_i)
            centers, amps, gammas = self._load_fit_pars(ele_file)

            perm_ob = Permittivity(self.exp_dat_ob.permittivity_infty)
            sigma_tilde = perm_ob.lorentz_combi_to_sigma_2d(
                energy_range, centers, amps, gammas, self.exp_dat_ob.thickness
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

            selected_wls, comp_ref_index = WaveLength().get_sifted_data(
                wls_range, ref_index_ob.complex_refractive_index
            )
            diff_R_wls_list.append(selected_wls)
            n0_index = self.sub_dat_ob.function_n0_wls(selected_wls)
            tmp_fc = OpticalCoeff(selected_wls, self.theta_0s, n0_index, n2_index=[1])
            ele_diff_Rs, ele_diff_Rp = tmp_fc.diff_R_thin_film(
                comp_ref_index, self.exp_dat_ob.thickness
            )
            diff_Rs_list.append(ele_diff_Rs[0])
            diff_Rp_list.append(ele_diff_Rp[0])

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
            save_dir="Conductivity/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()

        PlotMethod(
            [energy_range] * num_files,
            imag_part_sigma,
            x_label="E (meV)",
            y_label=r"$\rm{Im}[\sigma/\varepsilon_0 c]$",
            title=r"Imaginary part of fitted conductivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_imag",
            save_dir="Conductivity/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()

        PlotMethod(
            [energy_range] * num_files,
            perm_real_list,
            x_label="E (meV)",
            y_label=r"$\rm{Re}[\varepsilon]$",
            title=r"Real part of fitted Permittivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_real",
            save_dir="Permittivity/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()

        PlotMethod(
            [energy_range] * num_files,
            perm_imag_list,
            x_label="E (meV)",
            y_label=r"$\rm{Im}[\varepsilon]$",
            title=r"Imaginary part of fitted Permittivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name + "_imag",
            save_dir="Permittivity/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()
        PlotMethod(
            [energy_range] * num_files,
            n_list,
            x_label="E (meV)",
            y_label=r"$n$",
            title=r"Real part of complex refractive index",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name,
            save_dir="Complex_n_k/n/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()
        PlotMethod(
            [energy_range] * num_files,
            k_list,
            x_label="E (meV)",
            y_label=r"$k$",
            title=r"Imaginary part of complex refractive index",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name,
            save_dir="Complex_n_k/k/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()
        PlotMethod(
            diff_R_wls_list,
            diff_Rs_list,
            x_label="E (meV)",
            y_label=r"$\frac{r_s - r_s^0}{r_s^0}$",
            title=r"Differential reflectivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name,
            save_dir="DiffR/Rs/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()
        PlotMethod(
            diff_R_wls_list,
            diff_Rp_list,
            x_label="E (meV)",
            y_label=r"$\frac{r_p - r_p^0}{r_p^0}$",
            title=r"Differential reflectivity",
            legend=["Sample {}".format(i + 1) for i in range(num_files)],
            save_name=save_name,
            save_dir="DiffR/Rp/" + self.exp_dat_ob.__class__.__name__,
        ).multiple_line_one_plot()
