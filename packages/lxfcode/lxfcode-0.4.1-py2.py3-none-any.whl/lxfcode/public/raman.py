from public.method import *
from public.consts import *
from twisted_mat.twisted_tri_gra import ContiAbdTtgInst


class RamanCalPost:
    marker_size = 5.5
    marker_type = "h"
    colorbar_pad = 0.01
    colorbar_width = 0.01

    def __init__(
        self,
        save_dir,
        args_list,
        kp_num=70,
        colorbar=True,
        model_type="conti",
        mat_type="ABt-TTG",
        a0_constant=1.42 * sqrt(3),
    ) -> None:
        self.save_dir = save_dir
        self.kps_list, self.bound_vecs_arr = ContiAbdTtgInst(
            1, kp_num=kp_num
        ).kp_in_moire_b_zone(boundary_vec_return=True)
        self.x_list = [ele[0] for ele in self.kps_list]
        self.y_list = [ele[1] for ele in self.kps_list]
        self.args_list = args_list

        self.trans_npy_dir = (
            data_file_dir + "Raman/ele_raman_trans_npy/" + save_dir + "/"
        )
        self.trans_pic_dir = (
            data_file_dir + "Raman/ele_raman_transitions/" + save_dir + "/"
        )
        self.mat_npy_dir = data_file_dir + "Raman/raman_mat_files/" + save_dir + "/"

        self.colorbar = colorbar

        self.model_type = model_type

        self.mat_type = mat_type

        self.a0_const = a0_constant

        pass

    def raman_scatters(
        self,
        c_data,
        ele_col,
        vmin,
        vmax,
        model_type,
        twist_angle_conti,
        mat_type,
        number_type,
        cmap_type="jet",
    ):
        PubMeth.scatter_2d_plot(
            x_list=self.x_list,
            y_list=self.y_list,
            c_mat=c_data,
            marker_size=self.marker_size,
            marker_type=self.marker_type,
            colorbar=self.colorbar,
            cbar_label="Real part intensity (a.u.)",
            colorbar_pad=self.colorbar_pad,
            colorbar_width=self.colorbar_width,
            figuretitle=r"$v_{} \to c_{}$".format(
                ele_col % self.args_list[0] + 1,
                ele_col // self.args_list[0] + 1,
            ),
            figure_name="v{}_c{}_{}_{}_{}".format(
                ele_col % self.args_list[0] + 1,
                ele_col // self.args_list[0] + 1,
                model_type,
                twist_angle_conti,
                mat_type,
            ),
            uni_vmin=vmin,
            uni_vmax=vmax,
            figs_save_dir=self.trans_pic_dir
            + "{}".format(twist_angle_conti)
            + "/{}/".format(number_type),
            title_font_size=25,
            cmap=cmap_type,
            boundary_vecs=self.bound_vecs_arr,
        )

    def replot_ele_transition(self, plot_2d=True):
        angle_dir_list = os.listdir(self.trans_npy_dir)
        angle_dir_list.sort()
        angle_list = [float(ele) for ele in angle_dir_list]
        ele_trans_sum_real = []
        ele_trans_sum_imag = []

        angle_transition_list = []
        for ele_angle_dir in angle_dir_list:
            transition_mat = []
            aM_lattice_conti = self.a0_const / (
                2 * sin(float(ele_angle_dir) / 180 * pi / 2)
            )
            unit_moire_cell_area_conti = sqrt(3) / 2 * aM_lattice_conti**2
            print(unit_moire_cell_area_conti)

            ele_angle_trans_sum_real = []
            ele_angle_trans_sum_imag = []
            print("Loading: ", ele_angle_dir)
            uni_min_max_list = np.load(
                self.mat_npy_dir + ele_angle_dir + "/" + "uni_min_max.npy"
            )

            (
                uni_real_vmin,
                uni_real_vmax,
                uni_imag_vmin,
                uni_imag_vmax,
            ) = uni_min_max_list

            real_limit = (
                abs(uni_real_vmin)
                if abs(uni_real_vmin) > abs(uni_real_vmax)
                else abs(uni_real_vmax)
            )
            imag_limit = (
                abs(uni_imag_vmin)
                if abs(uni_imag_vmin) > abs(uni_imag_vmax)
                else abs(uni_imag_vmax)
            )

            ele_npy_list = os.listdir(self.trans_npy_dir + ele_angle_dir)
            for ele_npy in ele_npy_list:
                ele_col = int(str(ele_npy).split("_")[1])
                model_type = str(ele_npy).split("_")[2]
                twist_angle = str(ele_npy).split("_")[4]
                mat_type = str(ele_npy).split("_")[5]
                ele_transition = np.load(
                    self.trans_npy_dir + ele_angle_dir + "/" + ele_npy
                )

                # local_imag_vmin = min(imag(ele_transition))
                # local_imag_vmax = max(imag(ele_transition))
                # local_real_vmin = min(real(ele_transition))
                # local_real_vmax = max(real(ele_transition))

                if plot_2d:
                    self.raman_scatters(
                        real(ele_transition),
                        ele_col,
                        -real_limit,
                        real_limit,
                        model_type,
                        twist_angle,
                        mat_type,
                        number_type="real",
                        cmap_type="bwr",
                    )
                    self.raman_scatters(
                        imag(ele_transition),
                        ele_col,
                        -imag_limit,
                        imag_limit,
                        model_type,
                        twist_angle,
                        mat_type,
                        number_type="imag",
                        cmap_type="bwr",
                    )
                ele_angle_trans_sum_real.append(
                    real(ele_transition).sum() / unit_moire_cell_area_conti
                )
                ele_angle_trans_sum_imag.append(
                    imag(ele_transition).sum() / unit_moire_cell_area_conti
                )
                transition_mat.append(ele_transition / unit_moire_cell_area_conti)
            ele_trans_sum_real.append(ele_angle_trans_sum_real)
            ele_trans_sum_imag.append(ele_angle_trans_sum_imag)
            angle_transition_list.append(transition_mat)

            print("Complete: ", ele_angle_dir)
        ##  Real part
        # region

        print(len(angle_dir_list), len(ele_trans_sum_real))
        fig, ax_trans = plt.subplots()
        [
            ax_trans.plot(angle_list, array(ele_trans_sum_real)[:, ele_i], "k-")
            for ele_i in range(len(ele_npy_list))
        ]
        ax_trans.set_aspect("auto")
        ax_trans.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax_trans.set_ylabel("Real part", fontsize=12)
        ax_trans.set_title("", fontsize=14)
        fig.savefig(
            data_file_dir + "Raman/ele_trans_sum_plot/real_part.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        for ele_j in range(len(ele_npy_list)):
            v_i = ele_j % int(sqrt(len(ele_npy_list))) + 1
            c_i = ele_j // int(sqrt(len(ele_npy_list))) + 1
            l = ax_trans.plot(angle_list, array(ele_trans_sum_real)[:, ele_j], "r--")
            fig.savefig(
                data_file_dir
                + "Raman/ele_trans_sum_plot/real_part/v{}_c{}.png".format(v_i, c_i),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            ax_trans.get_lines()[-1].remove()
        plt.close()

        ##  Imaginary part
        fig, ax_trans = plt.subplots()
        [
            ax_trans.plot(angle_list, array(ele_trans_sum_imag)[:, ele_i], "k-")
            for ele_i in range(len(ele_npy_list))
        ]
        ax_trans.set_aspect("auto")
        ax_trans.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax_trans.set_ylabel("Imaginary part", fontsize=12)
        ax_trans.set_title("", fontsize=14)
        fig.savefig(
            data_file_dir + "Raman/ele_trans_sum_plot/imag_part.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        for ele_j in range(len(ele_npy_list)):
            v_i = ele_j % int(sqrt(len(ele_npy_list))) + 1
            c_i = ele_j // int(sqrt(len(ele_npy_list))) + 1
            ax_trans.plot(angle_list, array(ele_trans_sum_imag)[:, ele_j], "r--")
            fig.savefig(
                data_file_dir
                + "Raman/ele_trans_sum_plot/imag_part/v{}_c{}.png".format(v_i, c_i),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            ax_trans.get_lines()[-1].remove()
        plt.close()
        # endregion

        return

    def variation_across_angles(self):
        angle_dir_list = os.listdir(self.mat_npy_dir)
        real_list = []
        imag_list = []
        angle_dir_list.sort()
        angle_list = [float(ele) for ele in angle_dir_list]
        for ele_angle_dir in angle_dir_list:
            print("Loading: ", ele_angle_dir)
            mat_data = np.load(
                self.mat_npy_dir
                + ele_angle_dir
                + "/"
                + "{}_raman_{:.2f}_mat_renormed_by_area.npy".format(
                    self.model_type, float(ele_angle_dir)
                )
            )
            mat_sum = mat_data.sum()
            real_list.append(real(mat_sum))
            imag_list.append(imag(mat_sum))
            print("Complete: ", mat_sum)

        intensities = array(real_list) ** 2 + array(imag_list) ** 2
        fig, ax_line = plt.subplots()
        ax_line.plot(angle_list, intensities)
        ax_line.set_aspect("auto")
        ax_line.set_xlabel("", fontsize=12)
        ax_line.set_ylabel("", fontsize=12)
        ax_line.set_title("", fontsize=14)
        ax_line.set_xlim(ax_line.get_xlim())
        ax_line.set_ylim(ax_line.get_ylim())
        fig.savefig(
            data_file_dir + "Plots/tmp/tmp_intensities.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()
        return real_list, imag_list


class RamanCal:
    ##  Raman parameters set
    E_photon = 1240 / 532 * 1000
    cv_bands_taken = 7

    ##  Twist angles list
    twist_angles_list = arange(10, 20, 10 / 100)

    @staticmethod
    def ABt_TTG_single_raman_cal(
        twist_angle,
        mat_dir_name,
        pics_dir_name,
        npy_dir_name,
        ele_trans_pic_dir_name,
        mod_pars=[1, 1],
    ):
        """
        Single Raman calculation over Brillouin zone
        Default parameters: [self.bands_taken, self.photon_energy]
        # return
        Raman intensity
        """
        from twisted_mat.twisted_tri_gra import ContiAbdTtgInst

        tmp_abd = ContiAbdTtgInst(twist_angle, coupling_mod_pars=mod_pars)
        intensity = tmp_abd.multi_proc_raman_i_cal(
            [RamanCal.cv_bands_taken, RamanCal.E_photon],
            mat_2d_subfolder_name=mat_dir_name,
            pics_2d_save_dir=pics_dir_name,
            ele_trans_npy_save_dir=npy_dir_name,
            ele_trans_pic_dir=ele_trans_pic_dir_name,
        )
        RamanCal.print_return_ABt_TTG_fermi_orient_info(tmp_abd)

        return intensity

    @staticmethod
    def continue_from_break():
        """
        Continue from the unexpected break
        """

        fit_twist_angles, fermi_pars, orient_pars = RamanCal.read_fit_pars_from_ab()
        for ele_i in range(len(fermi_pars)):
            pars_i = ele_i + 1

            ele_fermi_v_mod = fermi_pars[ele_i]
            ele_orient_mod = orient_pars[ele_i]
            par_pairs = [ele_fermi_v_mod, ele_orient_mod]

            ##  Hint
            print(
                "Begin the calculation for parameters: ",
                ele_fermi_v_mod,
                ele_orient_mod,
            )

            ##  name for different coupling parameters
            ele_name = "{}_{:2f}_{:.2f}".format(pars_i, ele_fermi_v_mod, ele_orient_mod)

            ##  test the directory exists or not
            ele_mat_dir = data_file_dir + "Raman/raman_mat_files/{}/".format(ele_name)
            ##  scan the angle to find out which angle is not calculated
            for angle_i, ele_angle in enumerate(RamanCal.twist_angles_list):
                ele_angle_dir = ele_mat_dir + "{:.1f}/".format(ele_angle)
                if (
                    os.path.exists(ele_angle_dir)
                    and len(os.listdir(ele_angle_dir)) != 0
                ):
                    print("Already exist the data: ", ele_angle)
                else:
                    break
            if angle_i != len(RamanCal.twist_angles_list) - 1:
                print(
                    "The angle we are stopped at is: ",
                    RamanCal.twist_angles_list[angle_i],
                )

                ##  Load the previous Raman intensities we have calculated
                Intensity_list_previous = RamanCal.load_intensities_from_angles(
                    pars_i, par_pairs, angle_i
                )

                for ele_angle_left in RamanCal.twist_angles_list[angle_i:]:
                    dir_name = "{}/{:.1f}/".format(ele_name, ele_angle_left)
                    print(
                        "Now continue the calculation of angle: ",
                        ele_angle_left,
                        " for the parameters pair: ",
                        par_pairs,
                    )
                    ele_i = RamanCal.ABt_TTG_single_raman_cal(
                        ele_angle_left,
                        mat_dir_name=dir_name,
                        pics_dir_name=dir_name,
                        npy_dir_name=dir_name,
                        mod_pars=par_pairs,
                        ele_trans_pic_dir_name=dir_name,
                    )
                    Intensity_list_previous.append(ele_i)

                    ##  Save every new list to overwrite the file
                    intensity_file_name = (
                        data_file_dir + "Raman/raman_i_list/" + ele_name + ".npy"
                    )
                    np.save(intensity_file_name, Intensity_list_previous)

                ##  Renormalized Raman intensity
                Intensity_list_previous = array(Intensity_list_previous) / max(
                    Intensity_list_previous
                )
                ##  comparison of experimental and theoretical data
                RamanCal.comp_exp_the_raman_i(
                    RamanCal.twist_angles_list, Intensity_list_previous, ele_name
                )
            else:
                print(
                    "The calculations for parameters: ",
                    par_pairs,
                    " have been completed",
                )

    @staticmethod
    def load_overall_raman_i(angle_in, path_in):
        ##  Calculate the area of moire cell based on the twist angle
        moire_area = PubMeth.twisted_graphene_super_cell_area(angle_in)
        ##  Load the matrix of intensity
        raman_mat = np.load(path_in)

        return abs(raman_mat.sum()) ** 2 / moire_area**2

    @staticmethod
    def load_intensities_from_angles(pars_i, par_pair, angle_i):
        """
        Load the intensities from a few front twist angles into a list
        """
        ele_fermi_v_mod = par_pair[0]
        ele_orient_mod = par_pair[1]

        ele_name = "{}_{:2f}_{:.2f}".format(pars_i, ele_fermi_v_mod, ele_orient_mod)
        mat_dir_name = data_file_dir + "Raman/raman_mat_files/{}/".format(ele_name)

        ##  Raman intensity list to output
        raman_i_list = []
        for ele_angle in RamanCal.twist_angles_list[:angle_i]:
            ele_data_name = (
                mat_dir_name
                + "{:.1f}/".format(ele_angle)
                + "conti_raman_{:.2f}_mat_.npy".format(ele_angle)
            )
            ele_intensity = RamanCal.load_overall_raman_i(ele_angle, ele_data_name)
            raman_i_list.append(ele_intensity)
        print(
            "Load the intensity from angle range: ",
            RamanCal.twist_angles_list[0],
            "---",
            RamanCal.twist_angles_list[angle_i - 1],
        )

        return raman_i_list

    @staticmethod
    def ABt_TTG_angles_scan(
        intensity_list_name="intensity_array", pre_fix="angle", mod_pars=[1, 1]
    ):
        """
        Scan the twist angles of ABt-TTG for a range
        """
        i_list_out = []
        for ele_angle in RamanCal.twist_angles_list:
            ##  subdirectory name to save matrix, pictures and npy file
            dir_name = "{}/{:.1f}/".format(pre_fix, ele_angle)

            ##  calculate the Raman intensity for a single twist angle
            ele_intensity = RamanCal.ABt_TTG_single_raman_cal(
                ele_angle,
                mat_dir_name=dir_name,
                pics_dir_name=dir_name,
                npy_dir_name=dir_name,
                mod_pars=mod_pars,
                ele_trans_pic_dir_name=dir_name,
            )
            i_list_out.append(ele_intensity)

            ##  Save the intensity array for complete calculations
            intensity_arr_name = data_file_dir + "Raman/raman_i_list/{}.npy".format(
                intensity_list_name
            )

            ##  Save the npy file every time complete the single Raman calculation
            np.save(intensity_arr_name, i_list_out)

            ##  Hint
            print("Complete angle: ", ele_angle)

        return i_list_out

    @staticmethod
    def print_return_ABt_TTG_fermi_orient_info(abd_object):
        """
        Print out the information of the ABt-TTG: Fermi velocity and the oriented coupling
        """
        d = 1.42  #   A
        t = (
            abd_object.res_intra_coup[0][1]
            + abd_object.base_intra_coup[0][1]
            + abd_object.twist_intra_coup[0][1]
        ) / 3  #   meV
        t_orient = abd_object.orient_coup[0][1]
        fermi_v = 3 * d * A2m * t / (2 * h_bar_eV * eV2meV) / 1e6
        print("The Fermi velocity is: ", fermi_v, " *10^6 m/s")
        print("The AB bilayer interlayer coupling is: ", t_orient, " meV")

        return fermi_v, t_orient

    @staticmethod
    def read_raman_exp_data():
        """
        Read the experimental observations
        #   return
        exp_angle_list, exp_raman_i_list
        """
        ##  integrated intensity
        # exp_raman_i_from_data = [7.206331037140206, 20.65961320964642, 9.176482024311996, 15.538857411466433, 25.963473068025312, 19.708824781450502, 13.209452224957275, 8.151279174163275, 3.074189935550862, 2.018892163728973, 3.066941860699329]  # integrated intensity from data (delete the substrate signal)
        exp_angle_list = [11, 12.3, 13.2, 15, 16, 16.7, 17, 17.3, 18, 19, 20]
        exp_raman_i_from_fit = [
            7.145643832002423,
            20.42737629899334,
            8.910332164126979,
            13.497531420293852,
            25.30639573638074,
            20.024850079390106,
            13.516707038047128,
            8.313010465178571,
            2.913302965831959,
            2.076318814888275,
            2.962280678354917,
        ]  # integrated intensity from the fit curve
        exp_raman_i_from_fit = array(exp_raman_i_from_fit) / max(exp_raman_i_from_fit)

        return exp_angle_list, exp_raman_i_from_fit

    @staticmethod
    def read_fit_pars_from_ab():
        """
        Extract the fitting parameters from the absorption data
        # return
        Fermi velocity fitting, Oriented coupling fitting
        """
        ##  The Fermi modification of the list
        fit_twist_angle_list = [11.0, 12.3, 13.2, 16, 17]
        orient_mod = array([0.9, 0.9, 0.9, 0.9, 0.9])  # meV
        fermi_coeff = [1.185, 1.05, 0.92, 0.9, 0.93]

        return fit_twist_angle_list, fermi_coeff, orient_mod

    @staticmethod
    def read_fit_pars_from_ab_mod():
        """
        Extract the fitting parameters from the absorption data
        # return
        Fermi velocity fitting, Oriented coupling fitting
        """
        ##  The Fermi modification of the list
        fit_twist_angle_list = [12.3, 13.2, 16, 17]
        orient_mod = array([0.9, 0.9])  # meV
        fermi_coeff = [1.05, 0.92]

        return fit_twist_angle_list, fermi_coeff, orient_mod

    @staticmethod
    def comp_exp_the_raman_i(
        the_angles, the_raman_i_list, comp_file_name="exp_the_comp"
    ):
        """
        Compare the experimental and theoretical Raman intensity
        #   return
        """
        exp_angles, exp_raman_i_list = RamanCal.read_raman_exp_data()

        fig, ax_comp = plt.subplots()
        ax_comp.plot(exp_angles, exp_raman_i_list)
        ax_comp.plot(the_angles, the_raman_i_list)
        ax_comp.set_aspect("auto")
        ax_comp.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax_comp.set_ylabel("Renormalized Intensity", fontsize=12)
        ax_comp.set_title("", fontsize=14)
        ax_comp.set_xlim(ax_comp.get_xlim())
        ax_comp.set_ylim(ax_comp.get_ylim())
        ax_comp.legend(["Experiment", "Theory"])
        fig.savefig(
            data_file_dir + "Raman/exp_the_comp/{}.png".format(comp_file_name),
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

    @staticmethod
    def comp_exp_the_errorbar():
        """
        Compare the experimental and theoretical Raman intensity. Spot out the data we want to fit
        """
        ##  Read the modified data
        fit_twist_angles, fermi_pars, orient_pars = RamanCal.read_fit_pars_from_ab()

        for ele_i in range(len(fermi_pars)):
            par_i = ele_i + 1
            ele_fermi_v_mod = fermi_pars[ele_i]
            ele_orient_mod = orient_pars[ele_i]
            par_pair = [ele_fermi_v_mod, ele_orient_mod]

            ele_name = "{}_{:2f}_{:.2f}".format(par_i, ele_fermi_v_mod, ele_orient_mod)

            npy_data = data_file_dir + "Raman/raman_i_list/" + ele_name + ".npy"

            custom_lines = [Line2D([0], [0], color="b"), Line2D([0], [0], color="r")]

            ##  load the npy file to plot
            if os.path.exists(npy_data):
                ele_i_list = np.load(npy_data)
                ele_i_list = array(ele_i_list) / max(ele_i_list)
                ##  load the theoretical data
                exp_angles, exp_raman_i_list = RamanCal.read_raman_exp_data()
                exp_raman_i_list = array(exp_raman_i_list) / max(exp_raman_i_list)
                fig, ax_comp = plt.subplots()
                ax_comp.errorbar(
                    exp_angles, exp_raman_i_list, xerr=0.2, c="b"
                )  #   error bar plot
                ax_comp.plot(
                    RamanCal.twist_angles_list[: len(ele_i_list)], ele_i_list, color="r"
                )
                ax_comp.scatter(
                    fit_twist_angles[ele_i],
                    exp_raman_i_list[exp_angles.index(fit_twist_angles[ele_i])],
                    color="purple",
                    s=60,
                )
                ax_comp.set_aspect("auto")
                ax_comp.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
                ax_comp.set_ylabel("Renormalized Intensity", fontsize=12)
                ax_comp.set_title("", fontsize=14)
                ax_comp.set_xlim(ax_comp.get_xlim())
                ax_comp.set_ylim(ax_comp.get_ylim())
                ax_comp.legend(custom_lines, ["Experiment", "Theory"])
                fig.savefig(
                    data_file_dir + "Raman/exp_the_comp/Dot_{}.png".format(par_i),
                    dpi=330,
                    facecolor="w",
                    bbox_inches="tight",
                    pad_inches=0.1,
                )
                plt.close()
                print("Complete the comparison of: ", par_pair)
            else:
                print("The file doesn't exist! Please do some calculations!")

        for ele_i in [2]:
            par_i = ele_i + 1
            ele_fermi_v_mod = fermi_pars[ele_i]
            ele_orient_mod = orient_pars[ele_i]
            par_pair = [ele_fermi_v_mod, ele_orient_mod]

            ele_name = "{}_{:2f}_{:.2f}".format(par_i, ele_fermi_v_mod, ele_orient_mod)

            npy_data = data_file_dir + "Raman/raman_i_list/" + ele_name + ".npy"

            custom_lines = [Line2D([0], [0], color="b"), Line2D([0], [0], color="r")]

            ##  load the npy file to plot
            if os.path.exists(npy_data):
                ele_i_list = np.load(npy_data)
                ele_i_list = array(ele_i_list) / max(ele_i_list)
                ##  load the theoretical data
                exp_angles, exp_raman_i_list = RamanCal.read_raman_exp_data()
                exp_raman_i_list = array(exp_raman_i_list) / max(exp_raman_i_list)
                fig, ax_comp = plt.subplots()
                ax_comp.errorbar(
                    exp_angles, exp_raman_i_list, xerr=0.2, c="b"
                )  #   error bar plot
                ax_comp.plot(
                    RamanCal.twist_angles_list[: len(ele_i_list)], ele_i_list, color="r"
                )
                print("Fit angles: ", fit_twist_angles[ele_i:])
                target_i_list = [
                    exp_angles.index(ele_twist)
                    for ele_twist in fit_twist_angles[ele_i:]
                ]
                ax_comp.scatter(
                    fit_twist_angles[ele_i:],
                    exp_raman_i_list[target_i_list],
                    color="purple",
                    s=60,
                )
                ax_comp.set_aspect("auto")
                ax_comp.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
                ax_comp.set_ylabel("Renormalized Intensity", fontsize=12)
                ax_comp.set_title("", fontsize=14)
                ax_comp.set_xlim(ax_comp.get_xlim())
                ax_comp.set_ylim(ax_comp.get_ylim())
                ax_comp.legend(custom_lines, ["Experiment", "Theory"])
                fig.savefig(
                    data_file_dir + "Raman/exp_the_comp/Dot_{}.png".format(5),
                    dpi=330,
                    facecolor="w",
                    bbox_inches="tight",
                    pad_inches=0.1,
                )
                plt.close()
                print("Complete the comparison of: ", par_pair)
            else:
                print("The file doesn't exist! Please do some calculations!")

        pass

    @staticmethod
    def comp_exp_the_errorbar_ver2():
        """
        Compare the experimental and theoretical data --- version 2
        """
        ##  First plot the part for 0.92_0.9 for last few points
        exp_angles, exp_intensities = RamanCal.read_raman_exp_data()
        the_angles = RamanCal.twist_angles_list
        ##  Part-2 data
        the_int_part2 = np.load(
            "/home/aoxv/code/Data/Raman/raman_i_list/bak/3_0.920000_0.90.npy"
        )
        exp_ang_part2 = exp_angles[2:]
        exp_int_part2 = exp_intensities[2:]
        ##  Part-1 data
        the_int_part1 = np.load(
            "/home/aoxv/code/Data/Raman/raman_i_list/bak/2_1.050000_0.90.npy"
        )
        exp_ang_part1 = [exp_angles[1]] + [exp_angles[3]]
        exp_int_part1 = exp_intensities[1]

        ##  Plot the Fermi velocity
        from twisted_mat.twisted_tri_gra import ContiAbdTtgInst

        tmp_abd1 = ContiAbdTtgInst(12, coupling_mod_pars=[1.050000, 0.90])
        tmp_abd2 = ContiAbdTtgInst(12, coupling_mod_pars=[0.920000, 0.90])

        fermi1, orient1 = RamanCal.print_return_ABt_TTG_fermi_orient_info(tmp_abd1)
        fermi2, orient2 = RamanCal.print_return_ABt_TTG_fermi_orient_info(tmp_abd2)

        ##  Find the maximum location
        the_int_part2_list = list(the_int_part2)
        max_i = the_int_part2_list.index(max(the_int_part2_list))
        print("The maximum index is: ", max_i)
        print("The corresponding twist angle is: ", the_angles[max_i])

        ##  customized legends
        custom_lines = [
            Line2D([0], [0], color="w", marker="o", markerfacecolor="r"),
            Line2D([0], [0], color="w", marker="o", markerfacecolor="b"),
            Line2D([0], [0], color="r", linestyle="--", alpha=0.3),
            Line2D([0], [0], color="b", linestyle="--", alpha=0.3),
        ]

        #  renormalization of two intensity files
        the_int_part2 = array(the_int_part2) / 4900**2
        the_int_part1 = array(the_int_part1) / 4900**2

        exp_max_angle = exp_angles[np.argmax(exp_intensities)]
        the_intmax_i = np.argmin(np.abs(the_angles - exp_max_angle))
        the_intmax = the_int_part2[the_intmax_i]

        exp_intensities = exp_intensities / np.max(exp_intensities) * the_intmax
        exp_int_part1 = np.hstack([exp_intensities[1], [exp_intensities[3]]])
        exp_int_part2 = exp_intensities[2:]

        fig, ax_v2 = plt.subplots()
        ##  Part-2 plot
        ax_v2.plot(the_angles, the_int_part2, "r--", alpha=0.3)
        ax_v2.errorbar(
            exp_ang_part2,
            exp_int_part2,
            xerr=0.2,
            ls="none",
            color="r",
            marker="o",
            capsize=5,
        )
        ##  Part-1 plot
        ax_v2.plot(the_angles, the_int_part1, "b--", alpha=0.3)
        ax_v2.errorbar(
            exp_ang_part1,
            exp_int_part1,
            xerr=0.2,
            ls="none",
            color="b",
            marker="o",
            capsize=5,
        )
        ##  ax set
        ax_v2.set_aspect("auto")
        ax_v2.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax_v2.set_ylabel(r"Raman Intensity", fontsize=12)
        ax_v2.set_title("", fontsize=14)
        ax_v2.set_xlim(ax_v2.get_xlim())
        ax_v2.set_ylim(ax_v2.get_ylim())
        ax_v2.legend(
            custom_lines,
            [
                "Experiment",
                "Experiment",
                r"$v_F=${:.3f}$\times 10^6$ m/s".format(fermi2),
                r"$v_F=${:.3f}$\times 10^6$ m/s".format(fermi1),
            ],
        )
        fig.savefig(
            data_file_dir + "Raman/exp_the_comp/comp_v3.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        fig.savefig(
            data_file_dir + "Raman/exp_the_comp/comp_v3.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def ABt_TTG_angles_scan_with_diff_pars():
        """
        Adjust the parameters of Fermi velocity and orient coupling in ABt TTG
        """
        fit_twist_angles, fermi_pars, orient_pars = RamanCal.read_fit_pars_from_ab_mod()
        for ele_i in range(len(fermi_pars)):
            par_i = ele_i + 1
            ele_fermi_v_mod = fermi_pars[ele_i]
            ele_orient_mod = orient_pars[ele_i]

            ##  Hint
            print(
                "Begin the calculation for parameters: ",
                ele_fermi_v_mod,
                ele_orient_mod,
            )

            ##  name for different coupling parameters
            ele_name = "{}_{:2f}_{:.2f}".format(par_i, ele_fermi_v_mod, ele_orient_mod)
            par_pairs = [ele_fermi_v_mod, ele_orient_mod]
            ##  Raman calculation of different parameters
            ele_i_list = RamanCal.ABt_TTG_angles_scan(
                intensity_list_name=ele_name, pre_fix=ele_name, mod_pars=par_pairs
            )
            ##  Renormalized Raman intensity
            ele_i_list = array(ele_i_list) / max(ele_i_list)
            ##  comparison of experimental and theoretical data
            RamanCal.comp_exp_the_raman_i(
                RamanCal.twist_angles_list, ele_i_list, ele_name
            )

    @staticmethod
    def plot_ele_trans_pic(
        subfolder_name, angle, mat_type="ABt-TTG", model_type="conti"
    ):
        """
        Read element transition matrix and plot 2d picture
        """
        target_folder = (
            data_file_dir
            + "Raman/ele_raman_trans_npy/"
            + subfolder_name
            + "{:.1f}/".format(angle)
        )

        if os.path.exists(target_folder):
            file_name_list = os.listdir(
                target_folder
            )  ##  file name list in the target directory
            bands_to_take = int(
                sqrt(len(file_name_list))
            )  ##  number of bands (v and c) we take in the calculations
            index_list = [
                int(ele_filename.split("_")[1]) for ele_filename in file_name_list
            ]  # get the index of each figure
            index_list.sort()  # sort the index

            ##  Generate the k points in the moire brillouin zone
            test_mat = np.load(target_folder + file_name_list[0])
            kp_num = int(sqrt(test_mat.shape[0]))
            kps_list = PubMeth.kps_in_moire(kp_num)
            x_list = array(kps_list)[:, 0]
            y_list = array(kps_list)[:, 1]

            ##  Name the directory we want to save figures in
            pics_folder = (
                data_file_dir + "Raman/ele_raman_transitions/" + subfolder_name
            )

            ##  Load universal minimum and maximum
            uni_min_max_filename = (
                data_file_dir
                + "Raman/raman_mat_files/"
                + subfolder_name
                + "{:.1f}/uni_min_max.npy".format(angle)
            )
            uni_min_max = np.load(uni_min_max_filename)
            uni_real_vmin, uni_real_vmax, uni_imag_vmin, uni_imag_vmax = uni_min_max

            for ele_index in index_list:
                ele_filename = (
                    target_folder
                    + "transition_{}_conti_raman_{:.2f}_{}.npy".format(
                        ele_index, angle, mat_type
                    )
                )
                ele_transition = np.load(ele_filename)

                ##  plot the real part of the k-space distribution
                PubMeth.scatter_2d_plot(
                    x_list=x_list,
                    y_list=y_list,
                    c_mat=real(ele_transition),
                    marker_size=5.5,
                    marker_type="h",
                    colorbar=False,
                    colorbar_pad=0.01,
                    colorbar_width=0.01,
                    figuretitle=r"$v_{} \to c_{}$".format(
                        ele_index % bands_to_take + 1, ele_index // bands_to_take + 1
                    ),
                    figure_name="v{}_c{}_{}_{:.2f}_{}".format(
                        ele_index % bands_to_take + 1,
                        ele_index // bands_to_take + 1,
                        model_type,
                        angle,
                        mat_type,
                    ),
                    uni_vmin=uni_real_vmin,
                    uni_vmax=uni_real_vmax,
                    figs_save_dir=pics_folder
                    + "{:.1f}".format(angle)
                    + os.sep
                    + "real/",
                    title_font_size=25,
                )
                ##  plot the imag part of the k-space distribution
                PubMeth.scatter_2d_plot(
                    x_list=x_list,
                    y_list=y_list,
                    c_mat=imag(ele_transition),
                    marker_size=5.5,
                    marker_type="h",
                    colorbar=False,
                    colorbar_pad=0.01,
                    colorbar_width=0.01,
                    figuretitle=r"$v_{} \to c_{}$".format(
                        ele_index % bands_to_take + 1, ele_index // bands_to_take + 1
                    ),
                    figure_name="v{}_c{}_{}_{:.2f}_{}".format(
                        ele_index % bands_to_take + 1,
                        ele_index // bands_to_take + 1,
                        model_type,
                        angle,
                        mat_type,
                    ),
                    uni_vmin=uni_imag_vmin,
                    uni_vmax=uni_imag_vmax,
                    figs_save_dir=pics_folder
                    + "{:.1f}".format(angle)
                    + os.sep
                    + "imag/",
                    title_font_size=25,
                )

        else:
            print("Folder doesn't exist!!!")

        return


class SuperlatticeRaman:
    def __init__(self, angle1, angle2, lat) -> None:
        self.angle1 = angle1
        self.angle2 = angle2
        self.theta1 = angle1 / 180 * pi
        self.theta2 = angle2 / 180 * pi

        self.K = array([4 * pi / (3 * lat), 0])

        self.r_K1 = PubMeth.rotation(self.angle1) @ self.K
        self.r_K2 = PubMeth.rotation(-self.angle2) @ self.K

        pass

    @staticmethod
    def build_hexagon(start_p, arr_in, ccw=True):
        """
        ccw: counter-clockwise
        """
        p_list = [start_p]
        for r_i in range(6):  #   Full hexagon
            if ccw:
                r_arr = PubMeth.rotation(60 * r_i) @ arr_in
            else:
                r_arr = PubMeth.rotation(-60 * r_i) @ arr_in
            tmp_p = p_list[-1] + r_arr

            p_list.append(tmp_p)

        return array(p_list)

    @staticmethod
    def translation_vecs(arr_in, ccw=True):
        if ccw:
            prim_vec1 = -sqrt(3) * PubMeth.rotation(30) @ arr_in
            prim_vec2 = -sqrt(3) * PubMeth.rotation(-30) @ arr_in
            prim_vec3 = -sqrt(3) * PubMeth.rotation(-90) @ arr_in
        else:
            prim_vec1 = sqrt(3) * PubMeth.rotation(30) @ arr_in
            prim_vec2 = sqrt(3) * PubMeth.rotation(-30) @ arr_in
            prim_vec3 = sqrt(3) * PubMeth.rotation(-90) @ arr_in
        prim_vecs = [prim_vec1, prim_vec2, prim_vec3]

        return prim_vecs

    def rotated_BZ(self):
        hex1_ps = self.build_hexagon(self.K, self.r_K1 - self.K, ccw=False)
        hex2_ps = self.build_hexagon(self.K, self.r_K2 - self.K)

        fig, ax_line = plt.subplots()
        ax_line.plot(hex1_ps[:, 0], hex1_ps[:, 1], label="BZ1", marker=".")
        ax_line.plot(hex2_ps[:, 0], hex2_ps[:, 1], label="BZ2", marker=".")
        ax_line.set_aspect("equal")
        ax_line.set_xlabel("$k_x$", fontsize=12)
        ax_line.set_ylabel("$k_y$", fontsize=12)
        ax_line.set_title("Two twisted Brillouin zones", fontsize=14)
        ax_line.legend()
        fig.savefig(
            data_file_dir + "Plots/tmp/superlats.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )

        return fig, ax_line

    def BZ_period(self):
        shift_length = 10

        hex2_ps = self.build_hexagon(self.K, self.r_K2 - self.K)
        prim_vecs = self.translation_vecs(self.r_K2 - self.K)

        fig, ax_line = self.rotated_BZ()
        x_lim = ax_line.get_xlim()
        y_lim = ax_line.get_ylim()

        expand_lists = []
        vec_l = [prim_vecs[0] * ele_length for ele_length in range(shift_length)]
        vec_m = [prim_vecs[1] * ele_length for ele_length in range(shift_length)]
        vec_r = [prim_vecs[2] * ele_length for ele_length in range(shift_length)]
        expand_lists += vec_l
        expand_lists += vec_m
        expand_lists += vec_r
        for ele_i in range(len(vec_m)):
            ele_vec_m = vec_m[ele_i]
            tmp_vec_lm = ele_vec_m + array(vec_l)
            tmp_vec_rm = ele_vec_m + array(vec_r)
            expand_lists += list(tmp_vec_lm)
            expand_lists += list(tmp_vec_rm)

        for ele_shift in expand_lists:
            tmp_vecs = hex2_ps + ele_shift
            ax_line.plot(tmp_vecs[:, 0], tmp_vecs[:, 1], color="orange")
        ax_line.set_xlim(x_lim)
        ax_line.set_ylim(y_lim)
        fig.savefig(
            data_file_dir + "Plots/tmp/superlats_periods.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )


def main():
    RamanCal.comp_exp_the_errorbar_ver2()
    return


if __name__ == "__main__":
    main()
