from public.method import *
from public.pshe import *
from public.raman import *
from public.consts import *

# from public.dash import *
from mono.TB_mono_MoS2_exciton import *


class DemoFunc:

    @staticmethod
    def demo_rs_rp_with_gra_cond():
        """
        This function investigates the rs and rp over a range of incident angle for a fixed Omega.
        There are two situations: one is that light comes from the n0=1 and goes into n2=n, the other is that light comes from n0=n and goes into n2=1. Between two medium, there is graphene layer
        """
        n = 1.5  #   the refractive index which differs from that of air

        gra_cond = PSHE.graphene_cond_analytic(2.5, mu=1)[
            1
        ]  # the conductivity of the graphene
        theta_list = linspace(0 / 180 * pi, 90 / 180 * pi, 200)  #   theta list
        angle_list = theta_list / pi * 180  #   angle list

        ##  First situation n0=1 to n2=n
        Amp_rs_list_1 = []
        Amp_rp_list_1 = []
        Ang_rs_list_1 = []
        Ang_rp_list_1 = []
        for ele_theta in theta_list:
            ele_rs, ele_rp = PSHE.rs_rp_from_cond(
                n0_index=1, cond=gra_cond, n2_index=n, theta_0=ele_theta
            )
            ele_Amp_rs = abs(ele_rs)
            ele_Amp_rp = abs(ele_rp)
            ele_Ang_rs = np.angle(ele_rs)
            ele_Ang_rp = np.angle(ele_rp)

            Amp_rs_list_1.append(ele_Amp_rs)
            Amp_rp_list_1.append(ele_Amp_rp)
            Ang_rs_list_1.append(ele_Ang_rs)
            Ang_rp_list_1.append(ele_Ang_rp)

        ##  Plot the amplitude and the angle for situation 1
        data_list_1 = [Amp_rs_list_1, Amp_rp_list_1, Ang_rs_list_1, Ang_rp_list_1]
        y_labels_list_1 = [r"$R_s$", r"$R_p$", r"$\phi_s$", r"$\phi_p$"]
        file_name_list_1 = ["amp_rs", "amp_rp", "ang_rs", "ang_rp"]
        x_lim_list_1 = [[0, 90], [40, 70], [0, 90], [40, 70]]
        y_lim_list_1 = [[0, 1], [0, 0.2], [3.1, 3.18], [-pi, 0]]
        xlabel = r"$\theta[\degree]$"

        for ele_data_i in range(len(data_list_1)):
            fig, ax_ele_data = plt.subplots(figsize=(8, 4))
            ax_ele_data.plot(angle_list, data_list_1[ele_data_i])
            ax_ele_data.set_aspect("auto")
            ax_ele_data.set_xlabel(xlabel, fontsize=12)
            ax_ele_data.set_ylabel(y_labels_list_1[ele_data_i], fontsize=12)
            ax_ele_data.set_title("", fontsize=14)
            ax_ele_data.set_xlim(x_lim_list_1[ele_data_i])
            ax_ele_data.set_ylim(y_lim_list_1[ele_data_i])
            fig.savefig(
                data_file_dir
                + "PSHE/gra_cond/{}_1.png".format(file_name_list_1[ele_data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        ##  Second situation n0=n to n2=1
        Amp_rs_list_2 = []
        Amp_rp_list_2 = []
        Ang_rs_list_2 = []
        Ang_rp_list_2 = []
        for ele_theta in theta_list:
            ele_rs, ele_rp = PSHE.rs_rp_from_cond(
                n0_index=n, cond=gra_cond, n2_index=1, theta_0=ele_theta
            )
            ele_Amp_rs = abs(ele_rs)
            ele_Amp_rp = abs(ele_rp)
            ele_Ang_rs = np.angle(ele_rs)
            ele_Ang_rp = np.angle(ele_rp)

            Amp_rs_list_2.append(ele_Amp_rs)
            Amp_rp_list_2.append(ele_Amp_rp)
            Ang_rs_list_2.append(ele_Ang_rs)
            Ang_rp_list_2.append(ele_Ang_rp)

        ##  Plot the amplitude and the angle for situation 2
        data_list_2 = [Amp_rs_list_2, Amp_rp_list_2, Ang_rs_list_2, Ang_rp_list_2]
        y_labels_list_2 = [r"$R_s$", r"$R_p$", r"$\phi_s$", r"$\phi_p$"]
        file_name_list_2 = ["amp_rs", "amp_rp", "ang_rs", "ang_rp"]
        y_lim_list_2 = [[0, 1], [0, 1], [-pi, 0.1], [-pi, 0.1]]
        xlabel = r"$\theta[\degree]$"

        for ele_data_i in range(len(data_list_2)):
            fig, ax_ele_data = plt.subplots(figsize=(8, 4))
            ax_ele_data.plot(angle_list, data_list_2[ele_data_i])
            ax_ele_data.set_aspect("auto")
            ax_ele_data.set_xlabel(xlabel, fontsize=12)
            ax_ele_data.set_ylabel(y_labels_list_2[ele_data_i], fontsize=12)
            ax_ele_data.set_title("", fontsize=14)
            ax_ele_data.set_xlim([0, 90])
            ax_ele_data.set_ylim(y_lim_list_2[ele_data_i])
            fig.savefig(
                data_file_dir
                + "PSHE/gra_cond/{}_2.png".format(file_name_list_2[ele_data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        return data_list_1, data_list_2

    @staticmethod
    def demo_rs_rp_without_gra_cond():
        """
        This is to demonstrate the situation without the graphene
        """
        n = 1.5  #   the refractive index which differs from that of air

        theta_list = linspace(0 / 180 * pi, 90 / 180 * pi, 200)  #   theta list

        ##  First situation n0=1 to n2=n
        Amp_rs_list_1 = []
        Amp_rp_list_1 = []
        Ang_rs_list_1 = []
        Ang_rp_list_1 = []
        for ele_theta in theta_list:
            ele_rs, ele_rp = PSHE.rs_rp_between_two_medium(
                n0_index=1, n2_index=n, theta_0=ele_theta
            )
            ele_Amp_rs = abs(ele_rs)
            ele_Amp_rp = abs(ele_rp)
            ele_Ang_rs = np.angle(ele_rs)
            ele_Ang_rp = np.angle(ele_rp)

            Amp_rs_list_1.append(ele_Amp_rs)
            Amp_rp_list_1.append(ele_Amp_rp)
            Ang_rs_list_1.append(ele_Ang_rs)
            Ang_rp_list_1.append(ele_Ang_rp)

        data_list_1 = [Amp_rs_list_1, Amp_rp_list_1, Ang_rs_list_1, Ang_rp_list_1]

        ##  Second situation n0=n to n2=1
        Amp_rs_list_2 = []
        Amp_rp_list_2 = []
        Ang_rs_list_2 = []
        Ang_rp_list_2 = []
        for ele_theta in theta_list:
            ele_rs, ele_rp = PSHE.rs_rp_between_two_medium(
                n0_index=n, n2_index=1, theta_0=ele_theta
            )
            ele_Amp_rs = abs(ele_rs)
            ele_Amp_rp = abs(ele_rp)
            ele_Ang_rs = np.angle(ele_rs)
            ele_Ang_rp = np.angle(ele_rp)

            Amp_rs_list_2.append(ele_Amp_rs)
            Amp_rp_list_2.append(ele_Amp_rp)
            Ang_rs_list_2.append(ele_Ang_rs)
            Ang_rp_list_2.append(ele_Ang_rp)

        data_list_2 = [Amp_rs_list_2, Amp_rp_list_2, Ang_rs_list_2, Ang_rp_list_2]

        return data_list_1, data_list_2

    @staticmethod
    def demo_plot_compare_rs_rp():
        """
        Plot figures to compare rs and rp for situations with and without graphene conductivity
        """
        theta_list = linspace(0 / 180 * pi, 90 / 180 * pi, 200)  #   theta list
        angle_list = theta_list / pi * 180  #   angle list

        with_gra_cond_1, with_gra_cond_2 = DemoFunc.demo_rs_rp_with_gra_cond()
        wino_gra_cond_1, wino_gra_cond_2 = DemoFunc.demo_rs_rp_without_gra_cond()

        ##  Plot for situation 1
        y_labels_list_1 = [r"$R_s$", r"$R_p$", r"$\phi_s$", r"$\phi_p$"]
        file_name_list_1 = ["amp_rs", "amp_rp", "ang_rs", "ang_rp"]
        x_lim_list_1 = [[0, 90], [40, 70], [0, 90], [40, 70]]
        y_lim_list_1 = [[0, 1], [0, 0.2], [3.1, 3.18], [-pi - 0.1, pi + 0.1]]
        xlabel = r"$\theta[\degree]$"
        additional_line_list_1 = [[[]], [[]], [[]], [[pi, pi], [-pi, -pi]]]
        additional_x_list_1 = [[], [], [], [0, 90]]

        for ele_data_i in range(len(with_gra_cond_1)):
            fig, ax_ele_data = plt.subplots(figsize=(8, 4))
            ax_ele_data.plot(angle_list, with_gra_cond_1[ele_data_i])
            ax_ele_data.plot(angle_list, wino_gra_cond_1[ele_data_i])
            for ele_line in additional_line_list_1[ele_data_i]:
                ax_ele_data.plot(additional_x_list_1[ele_data_i], ele_line, "k--")
            ax_ele_data.set_aspect("auto")
            ax_ele_data.set_xlabel(xlabel, fontsize=12)
            ax_ele_data.set_ylabel(y_labels_list_1[ele_data_i], fontsize=12)
            ax_ele_data.set_title("", fontsize=14)
            ax_ele_data.set_xlim(x_lim_list_1[ele_data_i])
            ax_ele_data.set_ylim(y_lim_list_1[ele_data_i])
            ax_ele_data.legend(["With Graphene", "Without Graphene"])
            fig.savefig(
                data_file_dir
                + "PSHE/gra_cond/with_wino_{}_1.png".format(
                    file_name_list_1[ele_data_i]
                ),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        ##  Plot the amplitude and the angle for situation 2
        y_labels_list_2 = [r"$R_s$", r"$R_p$", r"$\phi_s$", r"$\phi_p$"]
        file_name_list_2 = ["amp_rs", "amp_rp", "ang_rs", "ang_rp"]
        y_lim_list_2 = [[0, 1], [0, 1], [-pi, 0.1], [-pi - 0.1, pi + 0.1]]
        xlabel = r"$\theta[\degree]$"
        additional_line_list_2 = [[[]], [[]], [[]], [[pi, pi], [-pi, -pi]]]
        additional_x_list_2 = [[], [], [], [0, 90]]

        for ele_data_i in range(len(with_gra_cond_2)):
            fig, ax_ele_data = plt.subplots(figsize=(8, 4))
            ax_ele_data.plot(angle_list, with_gra_cond_2[ele_data_i])
            ax_ele_data.plot(angle_list, wino_gra_cond_2[ele_data_i])
            for ele_line in additional_line_list_2[ele_data_i]:
                ax_ele_data.plot(additional_x_list_2[ele_data_i], ele_line, "k--")
            ax_ele_data.set_aspect("auto")
            ax_ele_data.set_xlabel(xlabel, fontsize=12)
            ax_ele_data.set_ylabel(y_labels_list_2[ele_data_i], fontsize=12)
            ax_ele_data.set_title("", fontsize=14)
            ax_ele_data.set_xlim([0, 90])
            ax_ele_data.set_ylim(y_lim_list_2[ele_data_i])
            ax_ele_data.legend(["With Graphene", "Without Graphene"])
            fig.savefig(
                data_file_dir
                + "PSHE/gra_cond/with_wino_{}_2.png".format(
                    file_name_list_2[ele_data_i]
                ),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        pass

    @staticmethod
    def demo_gra_if_gh_shift_from_single_cond_example_old():
        """
        n0_index, cond, n2_index=1, theta_0=pi/4
        """

        ##  Example from reference
        gra_cond_example = PSHE.graphene_cond_analytic(2.5, mu=1)[1]
        incident_theta_list = linspace(
            1 / 180 * pi, 89.9 / 180 * pi, 300
        )  #   incident angles
        incident_angle_list = incident_theta_list / pi * 180
        ##  Situation 1: n0 = 1, n2 = 1.5 for cp light
        IF_shift_example_cp1 = []
        IF_shift_example_45lp1 = []
        GH_shift_example_s1 = []
        GH_shift_example_p1 = []
        for ele_theta in incident_theta_list:
            ele_IF_cp = PSHE.get_if_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                eta_phase=pi / 2,
            )
            ele_IF_45lp = PSHE.get_if_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                eta_phase=0,
            )

            ele_GH_s1 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                w_s=1,
                w_p=0,
            )
            ele_GH_p1 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                w_s=0,
                w_p=1,
            )

            IF_shift_example_cp1.append(ele_IF_cp)
            IF_shift_example_45lp1.append(ele_IF_45lp)
            GH_shift_example_s1.append(ele_GH_s1)
            GH_shift_example_p1.append(ele_GH_p1)

        ##  Plot of data
        data_list1 = [
            IF_shift_example_cp1,
            IF_shift_example_45lp1,
            GH_shift_example_s1,
            GH_shift_example_p1,
        ]
        name_list = [
            "example_situ1_IF_cp",
            "example_situ1_IF_45lp",
            "example_situ1_GH_s",
            "example_situ1_GH_p",
        ]
        y_label_list = [
            r"$k_0 \Delta_{IF}$",
            r"$k_0 \Delta_{IF}$",
            r"$k_0 \Delta_{GH}$",
            r"$k_0 \Delta_{GH}$",
        ]
        for data_i in range(len(data_list1)):
            fig, ax_example = plt.subplots(figsize=(6, 3))
            ax_example.plot(incident_angle_list, data_list1[data_i])
            ax_example.set_aspect("auto")
            ax_example.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax_example.set_ylabel(y_label_list[data_i], fontsize=12)
            ax_example.set_title("", fontsize=14)
            ax_example.set_xlim(ax_example.get_xlim())
            ax_example.set_ylim(ax_example.get_ylim())
            fig.savefig(
                data_file_dir + "PSHE/gra_if_gh_shift/{}.png".format(name_list[data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        ##  Situation 2: n0 = 1.5, n2 = 1 for cp light
        incident_theta_list2 = linspace(40 / 180 * pi, 50 / 180 * pi, 10000)
        incident_angle_list2 = incident_theta_list2 / pi * 180
        IF_shift_example_cp2 = []
        IF_shift_example_45lp2 = []
        GH_shift_example_s2 = []
        GH_shift_example_p2 = []
        for ele_theta in incident_theta_list:
            ele_IF_cp2 = PSHE.get_if_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                eta_phase=pi / 2,
            )
            ele_IF_45lp2 = PSHE.get_if_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                eta_phase=0,
            )

            IF_shift_example_cp2.append(ele_IF_cp2)
            IF_shift_example_45lp2.append(ele_IF_45lp2)

        for ele_theta in incident_theta_list2:
            ele_GH_s2 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                w_s=1,
                w_p=0,
            )
            ele_GH_p2 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                w_s=0,
                w_p=1,
            )

            GH_shift_example_s2.append(ele_GH_s2)
            GH_shift_example_p2.append(ele_GH_p2)

        ##  Plot of data
        data_list2 = [IF_shift_example_cp2, IF_shift_example_45lp2]
        data_list3 = [GH_shift_example_s2, GH_shift_example_p2]
        name_list2 = ["example_situ2_IF_cp", "example_situ2_IF_45lp"]
        name_list3 = ["example_situ2_GH_s", "example_situ2_GH_p"]
        y_label_list2 = [r"$k_0 \Delta_{IF}$", r"$k_0 \Delta_{IF}$"]
        y_label_list3 = [r"$k_0 \Delta_{GH}$", r"$k_0 \Delta_{GH}$"]
        x_range_list2 = [[0, 90], [0, 90]]
        x_range_list3 = [[40, 50], [40, 50]]

        for data_i in range(len(data_list2)):
            fig, ax_example = plt.subplots(figsize=(6, 3))
            ax_example.plot(incident_angle_list, data_list2[data_i])
            ax_example.set_aspect("auto")
            ax_example.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax_example.set_ylabel(y_label_list2[data_i], fontsize=12)
            ax_example.set_title("", fontsize=14)
            ax_example.set_xlim(x_range_list2[data_i])
            ax_example.set_ylim(ax_example.get_ylim())
            fig.savefig(
                data_file_dir
                + "PSHE/gra_if_gh_shift/{}.png".format(name_list2[data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()
        for data_i in range(len(data_list3)):
            fig, ax_example = plt.subplots(figsize=(6, 3))
            ax_example.plot(incident_angle_list2, data_list3[data_i])
            ax_example.set_aspect("auto")
            ax_example.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax_example.set_ylabel(y_label_list3[data_i], fontsize=12)
            ax_example.set_title("", fontsize=14)
            ax_example.set_xlim(x_range_list3[data_i])
            ax_example.set_ylim(ax_example.get_ylim())
            fig.savefig(
                data_file_dir
                + "PSHE/gra_if_gh_shift/{}.png".format(name_list3[data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

    @staticmethod
    def demo_gra_if_gh_shift_from_single_cond_example():
        """
        n0_index, cond, n2_index=1, theta_0=pi/4
        """

        ##  Example from reference
        gra_cond_example = PSHE.graphene_cond_analytic(2.5, mu=1)[1]
        incident_theta_list = linspace(0, 89 / 180 * pi, 300)  #   incident angles
        incident_angle_list = incident_theta_list / pi * 180
        ##  Situation 1: n0 = 1, n2 = 1.5 for cp light
        IF_shift_example_cp1 = []
        IF_shift_example_45lp1 = []
        GH_shift_example_s1 = []
        GH_shift_example_p1 = []

        for ele_theta in incident_theta_list:
            ele_IF_cp = PSHE.get_if_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                eta_phase=pi / 2,
            )
            ele_IF_45lp = PSHE.get_if_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                eta_phase=0,
            )

            ele_GH_s1 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                w_s=1,
                w_p=0,
            )
            ele_GH_p1 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1,
                cond=gra_cond_example,
                n2_index=1.5,
                theta_0=ele_theta,
                w_s=0,
                w_p=1,
            )

            IF_shift_example_cp1.append(ele_IF_cp)
            IF_shift_example_45lp1.append(ele_IF_45lp)
            GH_shift_example_s1.append(ele_GH_s1)
            GH_shift_example_p1.append(ele_GH_p1)

        ##  Plot of data
        data_list1 = [
            IF_shift_example_cp1,
            IF_shift_example_45lp1,
            GH_shift_example_s1,
            GH_shift_example_p1,
        ]
        name_list = [
            "example_situ1_IF_cp",
            "example_situ1_IF_45lp",
            "example_situ1_GH_s_new",
            "example_situ1_GH_p_new",
        ]
        y_label_list = [
            r"$k_0 \Delta_{IF}$",
            r"$k_0 \Delta_{IF}$",
            r"$k_0 \Delta_{GH}$",
            r"$k_0 \Delta_{GH}$",
        ]
        for data_i in range(len(data_list1)):
            fig, ax_example = plt.subplots(figsize=(6, 3))
            ax_example.plot(incident_angle_list, data_list1[data_i])
            ax_example.set_aspect("auto")
            ax_example.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax_example.set_ylabel(y_label_list[data_i], fontsize=12)
            ax_example.set_title("", fontsize=14)
            ax_example.set_xlim(ax_example.get_xlim())
            ax_example.set_ylim(ax_example.get_ylim())
            fig.savefig(
                data_file_dir + "PSHE/gra_if_gh_shift/{}.png".format(name_list[data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        ##  Situation 2: n0 = 1.5, n2 = 1 for cp light
        incident_theta_list2 = linspace(40 / 180 * pi, 50 / 180 * pi, 2000)
        incident_angle_list2 = incident_theta_list2 / pi * 180
        IF_shift_example_cp2 = []
        IF_shift_example_45lp2 = []
        GH_shift_example_s2 = []
        GH_shift_example_p2 = []
        for ele_theta in incident_theta_list:
            ele_IF_cp2 = PSHE.get_if_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                eta_phase=pi / 2,
            )
            ele_IF_45lp2 = PSHE.get_if_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                eta_phase=0,
            )

            IF_shift_example_cp2.append(ele_IF_cp2)
            IF_shift_example_45lp2.append(ele_IF_45lp2)

        for ele_theta in incident_theta_list2:
            ele_GH_s2 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                w_s=1,
                w_p=0,
            )
            ele_GH_p2 = PSHE.get_gh_shift_cond_no_wl(
                n0_index=1.5,
                cond=gra_cond_example,
                n2_index=1,
                theta_0=ele_theta,
                w_s=0,
                w_p=1,
            )

            GH_shift_example_s2.append(ele_GH_s2)
            GH_shift_example_p2.append(ele_GH_p2)

        ##  Plot of data
        data_list2 = [IF_shift_example_cp2, IF_shift_example_45lp2]
        data_list3 = [GH_shift_example_s2, GH_shift_example_p2]
        name_list2 = ["example_situ2_IF_cp", "example_situ2_IF_45lp"]
        name_list3 = ["example_situ2_GH_s", "example_situ2_GH_p"]
        y_label_list2 = [r"$k_0 \Delta_{IF}$", r"$k_0 \Delta_{IF}$"]
        y_label_list3 = [r"$k_0 \Delta_{GH}$", r"$k_0 \Delta_{GH}$"]
        x_range_list2 = [[0, 90], [0, 90]]
        x_range_list3 = [[40, 50], [40, 50]]

        for data_i in range(len(data_list2)):
            fig, ax_example = plt.subplots(figsize=(6, 3))
            ax_example.plot(incident_angle_list, data_list2[data_i])
            ax_example.set_aspect("auto")
            ax_example.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax_example.set_ylabel(y_label_list2[data_i], fontsize=12)
            ax_example.set_title("", fontsize=14)
            ax_example.set_xlim(x_range_list2[data_i])
            ax_example.set_ylim(ax_example.get_ylim())
            fig.savefig(
                data_file_dir
                + "PSHE/gra_if_gh_shift/{}.png".format(name_list2[data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()
        for data_i in range(len(data_list3)):
            fig, ax_example = plt.subplots(figsize=(6, 3))
            ax_example.plot(incident_angle_list2, data_list3[data_i])
            ax_example.set_aspect("auto")
            ax_example.set_xlabel(r"$\theta$ ($\degree$)", fontsize=12)
            ax_example.set_ylabel(y_label_list3[data_i], fontsize=12)
            ax_example.set_title("", fontsize=14)
            ax_example.set_xlim(x_range_list3[data_i])
            ax_example.set_ylim(ax_example.get_ylim())
            fig.savefig(
                data_file_dir
                + "PSHE/gra_if_gh_shift/{}.png".format(name_list3[data_i]),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

    @staticmethod
    def demo_gra_cond_for_mu():
        ##  read the refractive index of BK-7 and then create a fit function
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        wave_lengths = linspace(410, 690, 300)  # wavelength of light, unit: nm
        photon_energy_list = 1240 / wave_lengths * 1000
        print(
            "Energy range for graphene conductivity: ",
            min(photon_energy_list),
            max(photon_energy_list),
        )
        wave_length_arr = array(wave_lengths)  # array of wavelengths

        ref_index_n0 = f_n0(wave_length_arr)  #   overwrite by interpolated data

        mu_list = linspace(5, 100, 200)  # chemical potential, unit: meV

        ##  get the conductivity of graphene in the target range for a specific mu
        gra_cond_for_mu = []
        for ele_mu in mu_list:
            ele_gra_cond = PSHE.graphene_cond_analytic(photon_energy_list, ele_mu)[1]
            gra_cond_for_mu.append(ele_gra_cond)

        ##  Plot of the graphene conductivity for different mu
        # region
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            real(gra_cond_for_mu),
            extent=(wave_length_arr[0], wave_length_arr[-1], mu_list[-1], mu_list[0]),
        )
        ax.set_aspect("auto")
        ax.set_xlabel(r"$\lambda$ (nm)")
        ax.set_ylabel(r"$\mu$ (meV)")
        ax.set_title("Real Part")
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label(r"Graphene Conductivity ($\varepsilon_0 c$)")
        fig.savefig(
            data_file_dir + "PSHE/gra_cond/gra_for_mu_real.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            imag(gra_cond_for_mu),
            extent=(wave_length_arr[0], wave_length_arr[-1], mu_list[-1], mu_list[0]),
        )
        ax.set_aspect("auto")
        ax.set_xlabel(r"$\lambda$ (nm)")
        ax.set_ylabel(r"$\mu$ (meV)")
        ax.set_title("Imaginary Part")
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label(r"Graphene Conductivity ($\varepsilon_0 c$)")
        fig.savefig(
            data_file_dir + "PSHE/gra_cond/gra_for_mu_imag.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()
        # endregion

    @staticmethod
    def demo_gra_if_shift_from_cond_over_wl():
        ##  read the refractive index of BK-7 and then create a fit function
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        wave_lengths = linspace(410, 690, 300)  # wavelength of light, unit: nm
        photon_energy_list = 1240 / wave_lengths * 1000
        print(
            "Energy range for graphene conductivity: ",
            min(photon_energy_list),
            max(photon_energy_list),
        )
        wave_length_arr = array(wave_lengths)  # array of wavelengths
        ref_index_n0 = f_n0(wave_length_arr)  #   overwrite by interpolated data

        ##  Plot of graphene IF shift for different incident angles
        ##  n0_index = 1, n2_index = n. Situation 1
        mu_select = 1000
        energy_example = mu_select * 2.5  #   The example Omega is 2.5
        wavelength_example = (
            1240 / energy_example * 1000
        )  #   The wavelength of the example photon energy
        gra_cond_low_doped1 = PSHE.graphene_cond_analytic(
            photon_energy_list, mu=mu_select
        )[1]
        gra_cond_low_doped1 = array(gra_cond_low_doped1)
        IF_shift_for_theta1 = []
        incident_theta_list = linspace(
            1 / 180 * pi, 90 / 180 * pi, 200
        )  #   incident angles
        incident_angle_list = incident_theta_list / pi * 180
        for ele_theta in incident_theta_list:
            ele_IF_shift1 = PSHE.get_if_shift_cond_over_wl(
                wave_length_arr,
                n0_index=1,
                cond=gra_cond_low_doped1,
                n2_index=ref_index_n0,
                theta_0=ele_theta,
            )
            IF_shift_for_theta1.append(ele_IF_shift1)
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            IF_shift_for_theta1,
            extent=(
                wave_length_arr[0],
                wave_length_arr[-1],
                incident_angle_list[-1],
                incident_angle_list[0],
            ),
        )
        ax.plot(
            [wavelength_example, wavelength_example],
            [incident_angle_list[0], incident_angle_list[-1]],
            "r--",
        )
        ax.text(wavelength_example + 5, 80, r"$\Omega=2.5$", color="r")
        ax.set_aspect("auto")
        ax.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax.set_ylabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax.set_title(r"$\mu={:.1f}$ meV".format(mu_select))
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label("IF shift (nm)")
        fig.savefig(
            data_file_dir + "PSHE/gra_if_gh_shift/if_shift_for_theta1.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()

        ##  Plot of graphene IF shift for different incident angles
        ##  n0_index = n, n2_index = 1. Situation 2
        mu_select = 1000
        energy_example = mu_select * 2.5  #   The example Omega is 2.5
        wavelength_example = (
            1240 / energy_example * 1000
        )  #   The wavelength of the example photon energy
        gra_cond_low_doped = PSHE.graphene_cond_analytic(
            photon_energy_list, mu=mu_select
        )[1]
        gra_cond_low_doped = array(gra_cond_low_doped)
        IF_shift_for_theta = []
        incident_theta_list = linspace(
            1 / 180 * pi, 90 / 180 * pi, 200
        )  #   incident angles
        incident_angle_list = incident_theta_list / pi * 180
        for ele_theta in incident_theta_list:
            ele_IF_shift = PSHE.get_if_shift_cond_over_wl(
                wave_length_arr,
                n0_index=ref_index_n0,
                cond=gra_cond_low_doped,
                n2_index=1,
                theta_0=ele_theta,
            )
            IF_shift_for_theta.append(ele_IF_shift)
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            IF_shift_for_theta,
            extent=(
                wave_length_arr[0],
                wave_length_arr[-1],
                incident_angle_list[-1],
                incident_angle_list[0],
            ),
        )
        ax.plot(
            [wavelength_example, wavelength_example],
            [incident_angle_list[0], incident_angle_list[-1]],
            "r--",
        )
        ax.text(wavelength_example + 5, 80, r"$\Omega=2.5$", color="r")
        ax.set_aspect("auto")
        ax.set_xlabel(r"$\lambda$ (nm)")
        ax.set_ylabel(r"$\theta$ ($\degree$)")
        ax.set_title(r"$\mu={:.1f}$ meV".format(mu_select))
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label("IF shift (nm)")
        fig.savefig(
            data_file_dir + "PSHE/gra_if_gh_shift/if_shift_for_theta2.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()

    @staticmethod
    def demo_gra_gh_shift_from_cond_over_wl():
        ##  read the refractive index of BK-7 and then create a fit function
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        wave_lengths = linspace(410, 690, 300)  # wavelength of light, unit: nm
        photon_energy_list = 1240 / wave_lengths * 1000
        print(
            "Energy range for graphene conductivity: ",
            min(photon_energy_list),
            max(photon_energy_list),
        )
        wave_length_arr = array(wave_lengths)  # array of wavelengths
        ref_index_n0 = f_n0(wave_length_arr)  #   overwrite by interpolated data

        ##  Conductivity of graphene
        mu_select = 1000
        gra_cond_low_doped1 = PSHE.graphene_cond_analytic(
            photon_energy_list, mu=mu_select
        )[1]

        ##  Example energy
        energy_example = mu_select * 2.5  #   The example Omega is 2.5
        wavelength_example = (
            1240 / energy_example * 1000
        )  #   The wavelength of the example photon energy

        ##  Situation 1: n0 = n, n2 = 1
        ##  Total GH shift
        GH_shift_mat1 = []
        ##  Get the interpolated function of derivative of rs and rp angles
        der_rs_angle_f, der_rp_angle_f = PSHE.get_gh_func_from_cond_over_wl(
            ref_index_n0, gra_cond_low_doped1, n2_index=1
        )
        ##  Express the wave vector
        k0_1 = 2 * pi * array(ref_index_n0) / array(wave_lengths)
        gra_cond_low_doped1 = array(gra_cond_low_doped1)
        incident_theta_list = linspace(0, 89 / 180 * pi, 200)  #   incident angles
        incident_angle_list = incident_theta_list / pi * 180
        ##  Scan all angles
        for ele_angle in incident_angle_list:
            ele_der_rs_angle = der_rs_angle_f(ele_angle)
            ele_der_rp_angle = der_rp_angle_f(ele_angle)
            ele_GH_shift = -(ele_der_rs_angle - ele_der_rp_angle) / k0_1
            GH_shift_mat1.append(real(ele_GH_shift))

        ##  Plot of graphene GH shift for different angles
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            GH_shift_mat1,
            extent=(
                wave_length_arr[0],
                wave_length_arr[-1],
                incident_angle_list[-1],
                incident_angle_list[0],
            ),
        )
        ax.set_aspect("auto")
        ax.plot(
            [wavelength_example, wavelength_example],
            [incident_angle_list[0], incident_angle_list[-1]],
            "r--",
        )
        ax.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax.set_ylabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax.set_title(r"$\mu={:.1f}$ meV".format(mu_select))
        ax.text(wavelength_example + 5, 80, r"$\Omega=2.5$", color="r")
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label("GH shift (nm)")
        fig.savefig(
            data_file_dir + "PSHE/gra_if_gh_shift/gh_shift_for_theta2.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()

        ##  Situation 2: n0 = 1, n2 = n
        ##  Total GH shift
        GH_shift_mat2 = []
        ##  Get the interpolated function of derivative of rs and rp angles
        der_rs_angle_f2, der_rp_angle_f2 = PSHE.get_gh_func_from_cond_over_wl(
            n0_index=1, cond=gra_cond_low_doped1, n2_index=ref_index_n0
        )
        ##  Express the wave vector
        k0_1 = 2 * pi / array(wave_lengths)
        gra_cond_low_doped1 = array(gra_cond_low_doped1)
        incident_theta_list = linspace(
            1 / 180 * pi, 90 / 180 * pi, 200
        )  #   incident angles
        incident_angle_list = incident_theta_list / pi * 180
        ##  Scan all angles
        for ele_angle in incident_theta_list:
            ele_der_rs_angle = der_rs_angle_f2(ele_angle)
            ele_der_rp_angle = der_rp_angle_f2(ele_angle)
            ele_GH_shift = -(ele_der_rs_angle - ele_der_rp_angle) / k0_1
            GH_shift_mat2.append(real(ele_GH_shift))
        ##  Plot of graphene GH shift for different angles
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            GH_shift_mat2,
            extent=(
                wave_length_arr[0],
                wave_length_arr[-1],
                incident_angle_list[-1],
                incident_angle_list[0],
            ),
        )
        ax.plot(
            [wavelength_example, wavelength_example],
            [incident_angle_list[0], incident_angle_list[-1]],
            "r--",
        )
        ax.set_aspect("auto")
        ax.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax.set_ylabel(r"$\theta$ ($\degree$)", fontsize=12)
        ax.set_title(r"$\mu={:.1f}$ meV".format(mu_select))
        ax.text(wavelength_example + 5, 80, r"$\Omega=2.5$", color="r")
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label("GH shift (nm)")
        fig.savefig(
            data_file_dir + "PSHE/gra_if_gh_shift/gh_shift_for_theta1.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()

    @staticmethod
    def demo_verify_mos2_cond_Wu():
        ##  read data
        wls, cond_realpart, cond_imagpart = PSHE.read_mos2_the_cond_Wu_as_e2_h_shifted()

        ##  Plot data
        energy = 1240 / array(wls)
        fig, ax_cond = plt.subplots()
        ax_cond.plot(wls, cond_realpart)
        ax_cond.plot(wls, cond_imagpart)
        ax_cond.set_aspect("auto")
        ax_cond.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_cond.set_ylabel(r"$e^2 / h$", fontsize=12)
        ax_cond.set_title("Conductivity of MoS$_2$", fontsize=14)
        ax_cond.set_xlim(ax_cond.get_xlim())
        ax_cond.set_ylim(ax_cond.get_ylim())
        ax_cond.legend(["Real part", "Imaginary part"])
        fig.savefig(
            data_file_dir + "PSHE/MoS2_cond_Wu/cond_real_imag.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        fig, ax_cond = plt.subplots()
        ax_cond.plot(energy, cond_realpart)
        ax_cond.plot(energy, cond_imagpart)
        ax_cond.set_aspect("auto")
        ax_cond.set_xlabel(r"$E$ (eV)", fontsize=12)
        ax_cond.set_ylabel(r"$e^2 / h$", fontsize=12)
        ax_cond.set_title("Conductivity of MoS$_2$", fontsize=14)
        ax_cond.set_xlim(ax_cond.get_xlim())
        ax_cond.set_ylim(ax_cond.get_ylim())
        ax_cond.legend(["Real part", "Imaginary part"])
        fig.savefig(
            data_file_dir + "PSHE/MoS2_cond_Wu/cond_real_e.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        ##  read unshifted data
        wls, cond_realpart, cond_imagpart = (
            PSHE.read_mos2_the_cond_Wu_as_e2_h_unshifted()
        )

        ##  Plot unshifted data
        energy = 1240 / array(wls)
        fig, ax_cond = plt.subplots()
        ax_cond.plot(wls, cond_realpart)
        ax_cond.plot(wls, cond_imagpart)
        ax_cond.set_aspect("auto")
        ax_cond.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_cond.set_ylabel(r"$e^2 / h$", fontsize=12)
        ax_cond.set_title("$\sigma$ of MoS$_2$", fontsize=14)
        ax_cond.set_xlim(ax_cond.get_xlim())
        ax_cond.set_ylim(ax_cond.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/MoS2_cond_Wu/cond_real_imag_unshifted.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        fig, ax_cond = plt.subplots()
        ax_cond.plot(energy, cond_realpart)
        ax_cond.plot(energy, cond_imagpart)
        ax_cond.set_aspect("auto")
        ax_cond.set_xlabel(r"$E$ (eV)", fontsize=12)
        ax_cond.set_ylabel(r"$e^2 / h$", fontsize=12)
        ax_cond.set_title("$\sigma$ of MoS$_2$", fontsize=14)
        ax_cond.set_xlim(ax_cond.get_xlim())
        ax_cond.set_ylim(ax_cond.get_ylim())
        ax_cond.legend(["Real part", "Imaginary part"])
        fig.savefig(
            data_file_dir + "PSHE/MoS2_cond_Wu/cond_real_e_unshifted.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

    @staticmethod
    def demo_mos2_if_gh_shift_from_cond_unshifted():
        ##  read data
        wls_mos2, cond_realpart, cond_imagpart = (
            PSHE.read_mos2_the_cond_Wu_as_eps_x_c_unshifted()
        )

        ##  substrate index and fit function
        wls_sub, ref_index_sub = PSHE.get_BK7_ref_index()
        f_substrate = interpolate.interp1d(wls_sub, ref_index_sub)

        ##  fit the mos2 wavelength to the substrate wavelength
        wls_mos2, cond_realimag = PSHE.sample_wl_fit_substrate_wl(
            wls_sub, wls_mos2, [cond_realpart, cond_imagpart]
        )
        cond_realpart = cond_realimag[0]
        cond_imagpart = cond_realimag[1]
        cond_mos2 = cond_realpart + 1j * cond_imagpart
        ##  get the fitted substrate ref index from fit function
        ref_index_sub = f_substrate(wls_mos2)

        ##  get the IF shift from cond
        IF_mos2_from_cond = PSHE.get_if_shift_cond_over_wl(
            wls_mos2, ref_index_sub, cond_mos2, n2_index=1, theta_0=pi / 4
        )
        GH_mos2_from_cond = PSHE.get_gh_shift_cond_over_wl(
            wls_mos2, ref_index_sub, cond_mos2, n2_index=1, theta_0=pi / 4
        )

        ##  Load the experiment results of IF and GH shifts
        if_wls, if_shifts = PSHE.read_mos2_if_shift_data()
        gh_wls, gh_shifts = PSHE.read_mos2_gh_shift_data()

        ##  Plot of IF and GH shift
        fig, ax_IF_GH = plt.subplots(1, 2, figsize=(12, 5))
        ax_IF_GH[0].plot(wls_mos2, IF_mos2_from_cond)
        ax_IF_GH[0].plot(if_wls[0], if_shifts[0])
        ax_IF_GH[0].set_aspect("auto")
        ax_IF_GH[0].set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_IF_GH[0].set_ylabel(r"IF shift (nm)", fontsize=12)
        ax_IF_GH[0].set_title("(a)", fontsize=20, loc="left", fontweight="bold")
        ax_IF_GH[0].set_xlim([500, 700])
        ax_IF_GH[0].legend(["Theoretical calculation", "Experimental data"])

        ax_IF_GH[1].plot(wls_mos2, GH_mos2_from_cond)
        ax_IF_GH[1].plot(gh_wls[0], gh_shifts[0])
        ax_IF_GH[1].set_aspect("auto")
        ax_IF_GH[1].set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_IF_GH[1].set_ylabel(r"GH shift (nm)", fontsize=12)
        ax_IF_GH[1].set_title("(b)", fontsize=20, loc="left", fontweight="bold")
        ax_IF_GH[1].set_xlim([500, 700])
        ax_IF_GH[1].legend(["Theoretical calculation", "Experimental data"])
        fig.savefig(
            data_file_dir
            + "PSHE/IF_shift_theory/if_gh_shift_from_cond_unshifted_comp_exp.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        pass

    @staticmethod
    def demo_e_2_omega():
        energy_list = linspace(10, 5000, 300)
        omega_list = PubMeth.convert_e_to_omega(energy_list)

        print("Convert ", energy_list[0], energy_list[-1], " meV")
        print("To: ", omega_list[0], omega_list[-1], " s^-1")

    @staticmethod
    def demo_sigma1_sigma2():
        """
        Example to show sigma1 and sigma2 picture
        """
        ##  energy range
        energy_list = linspace(100, 5000, 1000)

        ##  chosen a center energy example
        center_energy = 1500  #   meV
        omega_o = PubMeth.convert_e_to_omega(center_energy)

        ##  Amplitude is chosen to be related to the center frequency
        omega_p = sqrt(3) * omega_o

        ##  choose a broadening parameter gamma as an example
        gamma_energy = 20  #   meV
        gamma = PubMeth.convert_e_to_omega(gamma_energy)

        s1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
        s2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

        ##  separate plot of s1 and s2
        fig, ax_s1_s2 = plt.subplots()
        ax_s1_s2.plot(energy_list, s1)
        ax_s1_s2.plot(energy_list, s2)
        ax_s1_s2.set_aspect("auto")
        ax_s1_s2.set_xlabel("E (meV)", fontsize=12)
        ax_s1_s2.set_ylabel(r"$\sigma_1$", fontsize=12)
        ax_s1_s2.set_title("", fontsize=14)
        ax_s1_s2.set_xlim(ax_s1_s2.get_xlim())
        ax_s1_s2.set_ylim(ax_s1_s2.get_ylim())
        ax_s1_s2.legend([r"$\sigma_1$", r"$\sigma_2$"])
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/s1_s2.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        ##  express the s1 as the function of s2
        fig, ax_s1_func_s2 = plt.subplots()
        ax_s1_func_s2.plot(s1, s2)
        ax_s1_func_s2.set_aspect("auto")
        ax_s1_func_s2.set_xlabel("$\sigma_1$", fontsize=12)
        ax_s1_func_s2.set_ylabel("$\sigma_2$", fontsize=12)
        ax_s1_func_s2.set_title("", fontsize=14)
        ax_s1_func_s2.set_xlim(ax_s1_func_s2.get_xlim())
        ax_s1_func_s2.set_ylim(ax_s1_func_s2.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/s1_func_s2.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        ##  animation of s1 function of s2
        PubMeth.line_dot_track_animation(
            s1, s2, frames_num=len(s1), file_name="s1_func_s2"
        )

        return

    @staticmethod
    def demo_s1_s2_omegap_evolve():
        """
        Example to show the effect of omegap in sigma1
        """
        ##  energy range
        energy_list = linspace(100, 5000, 1000)

        ##  chosen a center energy example
        center_energy = 1500  #   meV
        omega_o = PubMeth.convert_e_to_omega(center_energy)

        ##  choose a broadening parameter gamma as an example
        gamma_energy = 20  #   meV
        gamma = PubMeth.convert_e_to_omega(gamma_energy)

        s1_lists = []
        s2_lists = []

        ##  Amplitude is chosen to be related to the center frequency
        omegap_coeff_list = linspace(0.1, 3, 600)
        title_list = []
        for ele_coeff in omegap_coeff_list:
            omega_p = ele_coeff * omega_o

            s1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
            s2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

            s1_lists.append(s1)
            s2_lists.append(s2)
            title_list.append(r"$\omega_p = {:.2f}\omega_o$".format(ele_coeff))

        ##  Multi-Column Animation
        PubMeth.line_evolve_animation_in_a_row(
            [s1_lists, [energy_list] * len(s1_lists), [energy_list] * len(s1_lists)],
            [s2_lists, s1_lists, s2_lists],
            frames_num=len(s1_lists),
            xlabels_list=[r"$\sigma_1$", r"E (meV)", r"E (meV)"],
            ylabels_list=[r"$\sigma_2$", r"$\sigma_1$", r"$\sigma_2$"],
            titles_list=[title_list, title_list, title_list],
            file_name="All_comp_omegap",
        )

        # ##  Plot the single function of s1 and s2
        # PubMeth.line_evolve_animation(s1_lists, s2_lists, len(s1_lists), title=title_list, xlabel=r"$\sigma_1$", ylabel=r"$\sigma_2$", file_name="s1_s2_omegap")

        return

    @staticmethod
    def demo_s1_s2_omegao_evolve():
        """
        Example to show the effect of omegap in sigma1
        """
        ##  energy range
        energy_list = linspace(100, 5000, 1000)

        ##  chosen a center energy example
        title_list = []
        s1_lists = []
        s2_lists = []
        for ele_energy in linspace(1000, 4000, 600):
            center_energy = ele_energy  #   meV
            omega_o = PubMeth.convert_e_to_omega(center_energy)

            ##  choose a broadening parameter gamma as an example
            gamma_energy = 20  #   meV
            gamma = PubMeth.convert_e_to_omega(gamma_energy)

            ##  Amplitude is chosen to be related to the center frequency
            omega_p = sqrt(2) * omega_o

            s1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
            s2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

            s1_lists.append(s1)
            s2_lists.append(s2)
            title_list.append(r"$\omega_o = {:e}$".format(omega_o) + r" $s^{-1}$")

        ##  Multi-Column Animation
        PubMeth.line_evolve_animation_in_a_row(
            [s1_lists, [energy_list] * len(s1_lists), [energy_list] * len(s1_lists)],
            [s2_lists, s1_lists, s2_lists],
            frames_num=len(s1_lists),
            xlabels_list=[r"$\sigma_1$", r"E (meV)", r"E (meV)"],
            ylabels_list=[r"$\sigma_2$", r"$\sigma_1$", r"$\sigma_2$"],
            titles_list=[title_list, title_list, title_list],
            file_name="All_comp_omegao",
        )

        # ##  Animation
        # PubMeth.line_evolve_animation(s1_lists, s2_lists, len(s1_lists), title=title_list, xlabel=r"$\sigma_1$", ylabel=r"$\sigma_2$", file_name="s1_s2_omegao")

        return

    @staticmethod
    def demo_s1_s2_gamma_evolve():
        """
        Example to show the effect of omegap in sigma1
        """
        ##  energy range
        energy_list = linspace(100, 5000, 1000)

        ##  chosen a center energy example
        title_list = []
        s1_lists = []
        s2_lists = []
        center_energy = 1930  #   meV
        omega_o = PubMeth.convert_e_to_omega(center_energy)

        ##  Amplitude is chosen to be related to the center frequency
        omega_p = sqrt(2) * omega_o

        ##  choose a broadening parameter gamma as an example
        for ele_gamma_energy in linspace(5, 300, 600):
            gamma_energy = ele_gamma_energy  #   meV
            gamma = PubMeth.convert_e_to_omega(gamma_energy)

            s1 = PSHE.sigma1(energy_list, omega_p, omega_o, gamma)
            s2 = PSHE.sigma2(energy_list, omega_p, omega_o, gamma)

            s1_lists.append(s1)
            s2_lists.append(s2)
            title_list.append(r"$\gamma = {:.2f}$ eV".format(gamma_energy))

        ##  Multi-Column Animation
        PubMeth.line_evolve_animation_in_a_row(
            [s1_lists, [energy_list] * len(s1_lists), [energy_list] * len(s1_lists)],
            [s2_lists, s1_lists, s2_lists],
            frames_num=len(s1_lists),
            xlabels_list=[r"$\sigma_1$", r"E (meV)", r"E (meV)"],
            ylabels_list=[r"$\sigma_2$", r"$\sigma_1$", r"$\sigma_2$"],
            titles_list=[title_list, title_list, title_list],
            file_name="All_comp_gamma",
        )

        # ##  Single Column Animation
        # PubMeth.line_evolve_animation(s1_lists, s2_lists, len(s1_lists), title=title_list, xlabel=r"$\sigma_1$", ylabel=r"$\sigma_2$", file_name="s1_s2_gamma")

        return

    @staticmethod
    def demo_get_rs_rp_from_s1_s2():
        """
        Get rs and rp from sigma1 and sigma2
        """
        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), 1000)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        ##  s1 and s2
        sigma1, sigma2 = PSHE.trial_single_lorentz_s1_s2(dense_energy)

        ##  Rs and phi_s
        Rs, phi_s = PSHE.rs_from_s1_s2(sigma1, sigma2, dense_n0_index)
        ##  Rp and phi_p
        Rp, phi_p = PSHE.rp_from_s1_s2(sigma1, sigma2, dense_n0_index)

        ##  Plot Rs and phi_s
        # region
        fig, axe_list = plt.subplots(1, 2, figsize=(10, 4))
        ax_1 = axe_list[0]
        ax_1.plot(dense_wls, Rs)
        ax_1.set_aspect("auto")
        ax_1.set_xlabel("$\lambda$ (nm)", fontsize=12)
        ax_1.set_ylabel("$R_s$", fontsize=12)
        ax_1.set_title("", fontsize=14)
        ax_1.set_xlim(ax_1.get_xlim())
        ax_1.set_ylim(ax_1.get_ylim())
        ax_2 = axe_list[1]
        ax_2.plot(dense_wls, phi_s)
        ax_2.set_aspect("auto")
        ax_2.set_xlabel("$\lambda$ (nm)", fontsize=12)
        ax_2.set_ylabel("$\phi_s$", fontsize=12)
        ax_2.set_title("", fontsize=14)
        ax_2.set_xlim(ax_2.get_xlim())
        ax_2.set_ylim(ax_2.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/Rs_phis.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()
        ##  Plot Rs and phi_s
        fig, axe_list = plt.subplots(1, 2, figsize=(10, 4))
        ax_1 = axe_list[0]
        ax_1.plot(dense_wls, Rp)
        ax_1.set_aspect("auto")
        ax_1.set_xlabel("$\lambda$ (nm)", fontsize=12)
        ax_1.set_ylabel("$R_p$", fontsize=12)
        ax_1.set_title("", fontsize=14)
        ax_1.set_xlim(ax_1.get_xlim())
        ax_1.set_ylim(ax_1.get_ylim())
        ax_2 = axe_list[1]
        ax_2.plot(dense_wls, phi_p)
        ax_2.set_aspect("auto")
        ax_2.set_xlabel("$\lambda$ (nm)", fontsize=12)
        ax_2.set_ylabel("$\phi_p$", fontsize=12)
        ax_2.set_title("", fontsize=14)
        ax_2.set_xlim(ax_2.get_xlim())
        ax_2.set_ylim(ax_2.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/Rp_phip.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()
        # endregion

        ##  Plot Rs as function of sigma1 and sigma2
        PubMeth.line_3d_dot_track_animation(
            sigma1,
            sigma1,
            Rs,
            len(sigma1),
            xlabel="$\sigma_1$",
            ylabel="$\sigma_2$",
            zlabel="$R_s$",
            title="",
            file_name="R_s_s1_s2",
        )
        PubMeth.line_3d_dot_track_animation(
            sigma1,
            sigma1,
            phi_s,
            len(sigma1),
            xlabel="$\sigma_1$",
            ylabel="$\sigma_2$",
            zlabel="$\phi_s$",
            title="",
            file_name="phis_s1_s2",
        )
        PubMeth.line_3d_dot_track_animation(
            sigma1,
            sigma1,
            Rp,
            len(sigma1),
            xlabel="$\sigma_1$",
            ylabel="$\sigma_2$",
            zlabel="$R_p$",
            title="",
            file_name="R_p_s1_s2",
        )
        PubMeth.line_3d_dot_track_animation(
            sigma1,
            sigma1,
            phi_p,
            len(sigma1),
            xlabel="$\sigma_1$",
            ylabel="$\sigma_2$",
            zlabel="$\phi_p$",
            title="",
            file_name="phip_s1_s2",
        )

    @staticmethod
    def demo_if_shift_from_s1_s2_single_lorentz():
        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), 1000)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        ##  s1 and s2
        sigma1, sigma2 = PSHE.trial_single_lorentz_s1_s2(dense_energy)

        ##  Get IF shift from s1 and s2
        IF_shift = PSHE.get_if_shift_from_s1_s2(
            sigma1, sigma2, dense_wls, dense_n0_index, theta_0=pi / 4
        )

        ##  Plot IF shift over wavelength
        # region
        fig, ax_IF = plt.subplots()
        ax_IF.plot(dense_wls, IF_shift)
        ax_IF.set_aspect("auto")
        ax_IF.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_IF.set_ylabel(r"$\Delta_{IF}$", fontsize=12)
        ax_IF.set_title("", fontsize=14)
        ax_IF.set_xlim(ax_IF.get_xlim())
        ax_IF.set_ylim(ax_IF.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/IF_single_lorentz.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()
        # endregion

        ##  Evolution of IF shift over omega_p, omega_o and gamma parameters
        center_e_list = linspace(1930, 3000, 300)
        evolution_over_center_e = []
        title_list1 = []
        for ele_center_e in center_e_list:

            sigma1, sigma2 = PSHE.trial_single_lorentz_s1_s2(
                dense_energy, center_energy=ele_center_e
            )

            ele_IF_shift = PSHE.get_if_shift_from_s1_s2(
                sigma1, sigma2, dense_wls, dense_n0_index, theta_0=pi / 4
            )

            evolution_over_center_e.append(ele_IF_shift)

            title_list1.append(r"$\hbar \omega_o = {:.2f}$ meV".format(ele_center_e))

        omega_p_coeff_list = linspace(0, 3, 300)
        evolution_over_omegap_coeff = []
        title_list2 = []
        for ele_coeff in omega_p_coeff_list:

            sigma1, sigma2 = PSHE.trial_single_lorentz_s1_s2(
                dense_energy, omegap_coeff=ele_coeff
            )

            ele_IF_shift = PSHE.get_if_shift_from_s1_s2(
                sigma1, sigma2, dense_wls, dense_n0_index, theta_0=pi / 4
            )

            evolution_over_omegap_coeff.append(ele_IF_shift)

            title_list2.append(r"$\omega_p = {:.2f} \omega_o$".format(ele_coeff))

        gamma_e_list = linspace(5, 300, 300)
        evolution_over_gamma_e = []
        title_list3 = []
        for ele_gamma in gamma_e_list:

            sigma1, sigma2 = PSHE.trial_single_lorentz_s1_s2(
                dense_energy, gamma_energy=ele_gamma
            )

            ele_IF_shift = PSHE.get_if_shift_from_s1_s2(
                sigma1, sigma2, dense_wls, dense_n0_index, theta_0=pi / 4
            )

            evolution_over_gamma_e.append(ele_IF_shift)

            title_list3.append(r"$\hbar\gamma = {:.2f} $ meV".format(ele_gamma))

        PubMeth.line_evolve_animation(
            [dense_wls] * len(evolution_over_center_e),
            evolution_over_center_e,
            frames_num=len(evolution_over_center_e),
            xlabel=r"$\lambda$ (nm)",
            ylabel=r"$\Delta_{IF}$",
            title=title_list1,
            file_name="IF_evo_center_e",
        )
        PubMeth.line_evolve_animation(
            [dense_wls] * len(evolution_over_omegap_coeff),
            evolution_over_omegap_coeff,
            frames_num=len(evolution_over_omegap_coeff),
            xlabel=r"$\lambda$ (nm)",
            ylabel=r"$\Delta_{IF}$",
            title=title_list2,
            file_name="IF_evo_omegap_coeff",
        )
        PubMeth.line_evolve_animation(
            [dense_wls] * len(evolution_over_gamma_e),
            evolution_over_gamma_e,
            frames_num=len(evolution_over_gamma_e),
            xlabel=r"$\lambda$ (nm)",
            ylabel=r"$\Delta_{IF}$",
            title=title_list3,
            file_name="IF_evo_gamma",
        )

        wls_lists = [
            [dense_wls] * len(evolution_over_center_e),
            [dense_wls] * len(evolution_over_omegap_coeff),
            [dense_wls] * len(evolution_over_gamma_e),
        ]
        shifts_list = [
            evolution_over_center_e,
            evolution_over_omegap_coeff,
            evolution_over_gamma_e,
        ]
        PubMeth.line_evolve_animation_in_a_row(
            wls_lists,
            shifts_list,
            frames_num=len(evolution_over_center_e),
            xlabels_list=[r"$\lambda$ (nm)", r"$\lambda$ (nm)", r"$\lambda$ (nm)"],
            ylabels_list=[r"$\Delta_{IF}$", r"$\Delta_{IF}$", r"$\Delta_{IF}$"],
            titles_list=[title_list1, title_list2, title_list3],
            file_name="multi_factor_IF_shift",
        )

    @staticmethod
    def demo_multiple_lorentz_s1_s2():
        """
        Demo of multiple lorentz s1 and s2
        """
        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), 1000)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        center_list = [1930, 2000]
        coeff_list = [1.4, 1.4]
        gamma_list = [30, 30]

        s1, s2 = PSHE.trial_multi_lorentz_s1_s2(
            dense_energy, center_list, coeff_list, gamma_list
        )

        ##  compare sigma1 and sigma2
        fig, ax_sigma = plt.subplots()
        ax_sigma.plot(dense_energy, s1)
        ax_sigma.plot(dense_energy, s2)
        ax_sigma.set_aspect("auto")
        ax_sigma.set_xlabel("E (meV)", fontsize=12)
        ax_sigma.set_ylabel("", fontsize=12)
        ax_sigma.set_title(
            r"$\hbar \omega_{o_1} = %s \mathrm{meV}, \hbar \omega_{o_2} = %s \mathrm{meV}$"
            % (center_list[0], center_list[1]),
            fontsize=14,
        )
        ax_sigma.set_xlim(ax_sigma.get_xlim())
        ax_sigma.set_ylim(ax_sigma.get_ylim())
        ax_sigma.legend([r"$\sigma_1$", r"$\sigma_2$"])
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/multi_lorentz.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

    @staticmethod
    def demo_if_shift_from_s1_s2_multi_lorentz():
        """
        Get IF shift from multiple Lorentzian peaks
        """
        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), 1000)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        center_list = [1900, 2100]
        coeff_list = [1, 1]
        gamma_list = [30, 60]

        s1, s2 = PSHE.trial_multi_lorentz_s1_s2(
            dense_energy, center_list, coeff_list, gamma_list
        )

        IF_shift = PSHE.get_if_shift_from_s1_s2(
            s1, s2, dense_wls, dense_n0_index, theta_0=pi / 4
        )

        ##  Plot the IF shift from multiple Lorentzian peaks
        # region
        fig, ax_IF = plt.subplots()
        ax_IF.plot(dense_wls, IF_shift)
        ax_IF.set_aspect("auto")
        ax_IF.set_xlabel("$\lambda$ (nm)", fontsize=12)
        ax_IF.set_ylabel("$\Delta_{IF}$ (nm)", fontsize=12)
        ax_IF.set_title("", fontsize=14)
        ax_IF.set_xlim(ax_IF.get_xlim())
        ax_IF.set_ylim(ax_IF.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/IF_multi_lorentz.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()
        # endregion

        ##  Scan one of the omega_o energy, coeff and gamma
        frames = 300

        center2_e_list = linspace(1930, 3000, frames)
        evo_if_center_e = []
        title_list1 = []
        for ele_center_e in center2_e_list:
            center_list = [1930, ele_center_e]
            coeff_list = [1.4, 1.4]
            gamma_list = [30, 30]

            s1, s2 = PSHE.trial_multi_lorentz_s1_s2(
                dense_energy, center_list, coeff_list, gamma_list
            )

            IF_shift = PSHE.get_if_shift_from_s1_s2(
                s1, s2, dense_wls, dense_n0_index, theta_0=pi / 4
            )

            evo_if_center_e.append(IF_shift)

            title_list1.append(r"$\hbar \omega_o = {:.2f}$ meV".format(ele_center_e))

        omega_p_coeff_list = linspace(0, 3, frames)
        evo_if_coeff = []
        title_list2 = []
        for ele_coeff in omega_p_coeff_list:

            center_list = [1930, 2000]
            coeff_list = [1.4, ele_coeff]
            gamma_list = [30, 30]

            s1, s2 = PSHE.trial_multi_lorentz_s1_s2(
                dense_energy, center_list, coeff_list, gamma_list
            )

            ele_IF_shift = PSHE.get_if_shift_from_s1_s2(
                s1, s2, dense_wls, dense_n0_index, theta_0=pi / 4
            )

            evo_if_coeff.append(ele_IF_shift)

            title_list2.append(r"$\omega_p = {:.2f} \omega_o$".format(ele_coeff))

        gamma_e_list = linspace(5, 300, frames)
        evo_if_gamma_e = []
        title_list3 = []
        for ele_gamma in gamma_e_list:

            center_list = [1930, 2000]
            coeff_list = [1.4, 1.4]
            gamma_list = [30, ele_gamma]

            s1, s2 = PSHE.trial_multi_lorentz_s1_s2(
                dense_energy, center_list, coeff_list, gamma_list
            )

            ele_IF_shift = PSHE.get_if_shift_from_s1_s2(
                s1, s2, dense_wls, dense_n0_index, theta_0=pi / 4
            )

            evo_if_gamma_e.append(ele_IF_shift)

            title_list3.append(r"$\hbar\gamma = {:.2f} $ meV".format(ele_gamma))

        wls_lists = [
            [dense_wls] * len(evo_if_center_e),
            [dense_wls] * len(evo_if_coeff),
            [dense_wls] * len(evo_if_gamma_e),
        ]
        shifts_list = [evo_if_center_e, evo_if_coeff, evo_if_gamma_e]

        ##  animation
        # PubMeth.line_evolve_animation([dense_wls] * len(evo_if_center_e), evo_if_center_e, frames_num=len(evo_if_center_e), xlabel=r"$\lambda$ (nm)", ylabel=r"$\Delta_{IF}$", title=title_list1, file_name="IF_evo_center_e_multi_lorentz")
        # PubMeth.line_evolve_animation([dense_wls] * len(evo_if_coeff), evo_if_coeff, frames_num=len(evo_if_coeff), xlabel=r"$\lambda$ (nm)", ylabel=r"$\Delta_{IF}$", title=title_list2, file_name="IF_evo_omegap_coeff_multi_lorentz")
        # PubMeth.line_evolve_animation([dense_wls] * len(evo_if_gamma_e), evo_if_gamma_e, frames_num=len(evo_if_gamma_e), xlabel=r"$\lambda$ (nm)", ylabel=r"$\Delta_{IF}$", title=title_list3, file_name="IF_evo_gamma_multi_lorentz")
        # PubMeth.line_evolve_animation_in_a_row(wls_lists, shifts_list, frames_num=len(evo_if_center_e), xlabels_list=[r"$\lambda$ (nm)", r"$\lambda$ (nm)", r"$\lambda$ (nm)"], ylabels_list=[r"$\Delta_{IF}$", r"$\Delta_{IF}$", r"$\Delta_{IF}$"], titles_list=[title_list1, title_list2, title_list3], file_name="multi_lorentz_IF_shift")

        return

    @staticmethod
    def demo_draw_exp_if_gh_data():
        """
        Draw the experimental data of GH and IF shift
        """
        gh_wls, gh_tot_shifts = PSHE.read_mos2_gh_shift_data()
        if_wls, if_tot_shifts = PSHE.read_mos2_if_shift_data()

        for ele_i, ele_gh in enumerate(gh_tot_shifts):
            fig, ax_gh = plt.subplots()
            ax_gh.plot(gh_wls[ele_i], ele_gh)
            ax_gh.set_aspect("auto")
            ax_gh.set_xlabel("$\lambda$ (nm)", fontsize=12)
            ax_gh.set_ylabel("$\Delta_{GH}$ (nm)", fontsize=12)
            ax_gh.set_title("Sample {}".format(ele_i + 1), fontsize=14)
            ax_gh.set_xlim(ax_gh.get_xlim())
            ax_gh.set_ylim(ax_gh.get_ylim())
            fig.savefig(
                data_file_dir + "PSHE/exp_ob_GH/sample_{}.png".format(ele_i + 1),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        for ele_i, ele_if in enumerate(if_tot_shifts):
            fig, ax_gh = plt.subplots()
            ax_gh.plot(if_wls[ele_i], ele_if)
            ax_gh.set_aspect("auto")
            ax_gh.set_xlabel("$\lambda$ (nm)", fontsize=12)
            ax_gh.set_ylabel("$\Delta_{IF}$ (nm)", fontsize=12)
            ax_gh.set_title("Sample {}".format(ele_i + 1), fontsize=14)
            ax_gh.set_xlim(ax_gh.get_xlim())
            ax_gh.set_ylim(ax_gh.get_ylim())
            fig.savefig(
                data_file_dir + "PSHE/exp_ob_IF/sample_{}.png".format(ele_i + 1),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

        return

    @staticmethod
    def scan_omega_p_gamma():
        """
        Scan different parameters of omega_p and gamma to get different maxima of different sigma
        """
        energy_list = linspace(1500, 3500, 1000)
        center_e = 2500  #   meV
        coeff_list = linspace(0, 5, 500)
        gamma_list = linspace(0, 500, 500)

        all_mat = []
        for ele_coeff in coeff_list:
            row_data = []
            for ele_gamma in gamma_list:
                s1, s2 = PSHE.trial_single_lorentz_s1_s2(
                    energy_list, center_e, ele_coeff, ele_gamma
                )
                if max(s1) <= 1 and max(s1) > 1 / 2:
                    row_data.append(2)
                elif max(s1) > 0 and max(s1) < 1 / 2:
                    row_data.append(1)
                else:
                    row_data.append(0)

            all_mat.append(row_data)
        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(
            all_mat,
            extent=(gamma_list[0], gamma_list[-1], coeff_list[-1], coeff_list[0]),
        )
        ax.set_aspect("auto")
        ax.set_xlabel("$\gamma$")
        ax.set_ylabel("$\omega_p$")
        ax.set_title("Title")
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label("value")
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/scan_omega_p_gamma.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()

        return

    @staticmethod
    def demo_dash_app():

        external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

        app = Dash(__name__, external_stylesheets=external_stylesheets)

        app.layout = html.Div(
            [
                html.P("Enter a composite number to see its prime factors"),
                dcc.Input(id="num", type="number", debounce=True, min=2, step=1),
                html.P(id="err", style={"color": "red"}),
                html.P(id="out"),
            ]
        )

        @app.callback(
            Output("out", "children"), Output("err", "children"), Input("num", "value")
        )
        def show_factors(num):
            if num is None:
                # PreventUpdate prevents ALL outputs updating
                raise dash.exceptions.PreventUpdate

            factors = prime_factors(num)
            if len(factors) == 1:
                # dash.no_update prevents any single output updating
                # (note: it's OK to use for a single-output callback too)
                return dash.no_update, "{} is prime!".format(num)

            return "{} is {}".format(num, " * ".join(str(n) for n in factors)), ""

        def prime_factors(num):
            n, i, out = num, 2, []
            while i * i <= n:
                if n % i == 0:
                    n = int(n / i)
                    out.append(i)
                else:
                    i += 1 if i == 2 else 2
            out.append(n)
            return out

        app.run_server(debug=True, port=8080)

    @staticmethod
    def demo_lorentz_peak():

        frames = 500

        var_list = linspace(0, 100, 500)
        amp_ratio_list = 1
        center_list = 50
        gamma_list = 10

        lorentz_real = PubMeth.lorentz_real(
            var_list, amp_ratio_list, center_list, gamma_list
        )

        lorentz_imag = PubMeth.lorentz_imag(
            var_list, amp_ratio_list, center_list, gamma_list
        )

        fig, ax_lorentz = plt.subplots()
        ax_lorentz.plot(var_list, lorentz_real)
        ax_lorentz.plot(var_list, lorentz_imag)
        ax_lorentz.set_aspect("auto")
        ax_lorentz.set_xlabel("x", fontsize=12)
        ax_lorentz.set_ylabel("y", fontsize=12)
        ax_lorentz.set_title("Lorentzian peaks", fontsize=14)
        ax_lorentz.set_xlim(ax_lorentz.get_xlim())
        ax_lorentz.set_ylim(ax_lorentz.get_ylim())
        ax_lorentz.legend(["Real part", "Imaginary part"])
        fig.savefig(
            data_file_dir + "PSHE/lorentz/real_imag_part.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_if_shift_from_s1_s2_multi_lorentz_direct():
        """
        get sigma1 and sigma2 directly from Lorentzian peaks
        """
        ##  Read the refractive index of BK-7 from database
        wave_length_n0, ref_index_n0 = PSHE.get_BK7_ref_index()
        f_n0 = interpolate.interp1d(wave_length_n0, ref_index_n0)

        ##  fit it at more points from long-wavelength (low energy) to short-wavelength (high energy). And express the photon energy
        dense_wls = linspace(max(wave_length_n0), min(wave_length_n0), 1000)
        dense_n0_index = f_n0(dense_wls)
        dense_energy = 1240 / dense_wls * 1000

        ##  load the experiment result
        wls_list, IF_shift_list = PSHE.read_mos2_if_shift_data()
        target_IF_shift = IF_shift_list[-1]
        target_wls = wls_list[-1]
        target_energy = 1240 / array(target_wls) * 1000

        ##  parameters list
        center_list = [1.9624354e03]
        num_of_lorentz = len(center_list)
        gamma_list = [95] * num_of_lorentz
        amp_ratio_list = [1] * num_of_lorentz

        ##  Express the IF shift
        IF_shift = PSHE.if_shift_func_multi_lorentz(
            target_energy, center_list, amp_ratio_list, gamma_list, 0, 0, "direct"
        )

        ##  Scan center, amplitude and gamma, respectively
        frames_num = 600
        center_list = linspace(1800, 3000, frames_num)
        gamma_list = linspace(1, 300, frames_num)
        lorentz_const_list = linspace(0, 0.5, frames_num)

        evo_center_list = []
        evo_amp_list = []
        evo_gamma_list = []
        evo_const_list = []

        center_titles = []
        amp_titles = []
        gamma_titles = []
        const_titles = []

        center_default = 2000
        gamma_default = 80
        amp_default = 1

        for ele_center in center_list:
            amp = 1
            ele_if = PSHE.if_shift_func_multi_lorentz(
                target_energy,
                [ele_center],
                [amp],
                [gamma_default],
                total_shift=0,
                lorentz_const=0,
                type_s="direct",
            )
            evo_center_list.append(ele_if)
            center_titles.append(r"$\omega_o$={:.2f}".format(ele_center))

        for ele_gamma in gamma_list:
            amp = 1
            ele_if = PSHE.if_shift_func_multi_lorentz(
                target_energy,
                [center_default],
                [amp],
                [ele_gamma],
                total_shift=0,
                lorentz_const=0,
                type_s="direct",
            )
            evo_gamma_list.append(ele_if)
            gamma_titles.append(r"$\gamma$={:.2f}".format(ele_gamma))

        for ele_ratio in linspace(0, 1, frames_num):
            ele_amp = ele_ratio
            ele_if = PSHE.if_shift_func_multi_lorentz(
                target_energy,
                [center_default],
                [ele_amp],
                [gamma_default],
                total_shift=0,
                lorentz_const=0,
                type_s="direct",
            )
            evo_amp_list.append(ele_if)
            amp_titles.append("ratio = {}".format(ele_ratio))

        for ele_const in lorentz_const_list:
            amp_ratio = 1
            ele_if = PSHE.if_shift_func_multi_lorentz(
                target_energy,
                [center_default],
                [amp_ratio],
                [gamma_default],
                total_shift=0,
                lorentz_const=ele_const,
                type_s="direct",
            )
            evo_const_list.append(ele_if)
            const_titles.append(r"Const={:.2f}".format(ele_const))

        images_list = [evo_amp_list, evo_center_list, evo_gamma_list, evo_const_list]
        x_lists = [[target_wls] * frames_num] * len(images_list)

        title_list = [amp_titles, center_titles, gamma_titles, const_titles]

        PubMeth.line_evolve_animation_in_a_row(
            x_lists,
            images_list,
            frames_num=frames_num,
            xlabels_list=[r"$\lambda$"] * len(images_list),
            ylabels_list=[r"$\Delta_{IF}$"] * len(images_list),
            titles_list=title_list,
            file_name="IF_s1_s2_direct_lorentz",
            fig_height=5,
        )

        return

    @staticmethod
    def demo_gh_shift_from_s1_s2():
        """
        get gh shift from s1 and s2
        """

        ##  parameters list
        center_list = [1.9624354e03]
        num_of_lorentz = len(center_list)
        gamma_list = [5] * num_of_lorentz
        amp_list = [
            PSHE.eta_amp_to_center_gamma(
                center_list[ele_i], gamma_list[ele_i], scale_ratio=1
            )
            for ele_i in range(len(center_list))
        ]

        ##  Express the IF shift
        GH_shift, dense_wls = PSHE.get_gh_shift_over_wl_s1_s2_direct_lorentz(
            center_list, amp_list, gamma_list, theta_0=pi / 4
        )

        fig, ax_gh = plt.subplots()
        ax_gh.plot(dense_wls, GH_shift)
        ax_gh.set_aspect("auto")
        ax_gh.set_xlabel("", fontsize=12)
        ax_gh.set_ylabel("", fontsize=12)
        ax_gh.set_title("", fontsize=14)
        ax_gh.set_xlim(ax_gh.get_xlim())
        ax_gh.set_ylim(ax_gh.get_ylim())
        ax_gh.legend([])
        fig.savefig(
            data_file_dir + "PSHE/lorentz/gh.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_scan_s1_s2_for_one_lambda():
        """
        Scan s1 and s2 for one single lambda
        """
        ##  Fix the range of sigma1 and sigma2
        s1 = linspace(0, 1, 200)
        s2 = linspace(-2, 2, 200)

        target_wl = 500  #   nm
        IF_map = PSHE.scan_s1_s2_for_one_lambda(s1, s2, target_wl)

        fig, ax = plt.subplots()
        fig.set_size_inches(5, 5)
        img = ax.imshow(IF_map, extent=(s1[0], s1[-1], s2[-1], s2[0]))
        ax.set_aspect("auto")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_title("Title")
        c_ax = PubMeth.add_right_cax(ax, 0.03, 0.02)
        c_bar = fig.colorbar(img, cax=c_ax)
        c_bar.set_label("IF shift")
        fig.savefig(
            data_file_dir + "PSHE/s1_s2/scan/tmp_map.png",
            dpi=330,
            pad_inches=0.2,
            bbox_inches="tight",
        )
        plt.close()

        trace1 = go.Surface(x=s1, y=s2, z=IF_map)
        layout = PubMeth.plotly_layout(
            xlabel=r"$\sigma_1$",
            ylabel="$\sigma_2$",
            zlabel=r"IF shift (nm)",
            figuretitle=r"$\lambda=$ {}nm".format(target_wl),
        )
        fig = go.Figure(data=[trace1], layout=layout)
        fig.write_html(data_file_dir + "html_files/3d_scatter_plot.html")

        return

    @staticmethod
    def demo_mono_mos2():
        """
        Plot the band structure of monolayer MoS2
        """
        mos2 = MoS2()

        ##  Band structure depiction
        k_path = [mos2.path_K1, mos2.path_gamma, mos2.path_M, mos2.path_K2]
        n = 5
        k_path = [
            mos2.path_K1 + (mos2.path_M2 - mos2.path_K1) / n,
            mos2.path_K1 + (mos2.path_M - mos2.path_K1) / n,
        ]
        # k_path = [
        #     mos2.path_K1 + (mos2.path_K1 - mos2.path_M) / n,
        #     mos2.path_K1 + (mos2.path_M - mos2.path_K1) / n,
        # ]
        kp_list = []
        plt.figure(figsize=(2.5, 4))
        # fig, ax = plt.subplots(figsize=(5,10))
        for i in range(len(k_path) - 1):
            kp_list.extend(PubMeth.p2p(k_path[i], k_path[i + 1], 100))
        eig_list = []
        for ele_kp in kp_list:
            tmp_e, tmp_a = eig(mos2.hamiltonian(ele_kp))
            tmp_e.sort()
            eig_list.append(real(tmp_e))

        A_series = [1.9297, 2.1291, 2.1834]

        B_series = [2.0554, 2.2655]

        plt.plot(eig_list, lw=1, color="k")
        plt.ylabel("E(eV)")
        # plt.axis("off")
        plt.ylim([-0.5, 2])
        plt.hlines(
            [
                eig_list[len(eig_list) // 2][0],
                eig_list[len(eig_list) // 2][1],
                eig_list[len(eig_list) // 2][2],
                # eig_list[len(eig_list) // 2][3],
            ],
            0,
            len(eig_list) - 1,
            linestyles=["--", "--", "--"],
            linewidths=[0.5, 0.5, 0.5],
            colors=["b", "g", "g"],
        )

        plt.hlines(
            A_series,
            0,
            len(eig_list) - 1,
            linestyles="--",
            linewidths=0.5,
            colors="r",
        )
        plt.text(11, 1.3, "here")
        plt.savefig(
            data_file_dir + "bands/MoS2/mono_bands.png", dpi=330, bbox_inches="tight"
        )

        # ##  State vector depiction
        # k_path = [mos2.path_K1, mos2.path_gamma, mos2.path_M, mos2.path_K2]
        # kp_list = []
        # for i in range(len(k_path) - 1):
        #     kp_list.extend(PubMeth.p2p(k_path[i], k_path[i + 1], 100))
        # even_x_lis = []
        # odd_x_list = []
        # even_dot = []
        # odd_dots = []
        # for kp_index, ele_kp in enumerate(kp_list):
        #     ##  Eigen values and eigen states of the Hamiltonian
        #     eig_vals, eig_vecs, even_judge, odd_judge = mos2.get_sort_vals_vecs(ele_kp)
        #     # print("LEN OF EVEN: ", len(even_judge[even_judge]))

        # plt.scatter(even_x_lis, even_dot, marker=".")
        # plt.scatter(odd_x_list, odd_dots, marker=".")
        # plt.ylabel("E(eV)")
        # plt.savefig(data_file_dir + "bands/MoS2/even_odd_2.png", dpi=330)

        # ##  Test of V_q
        # mos2.V_q_sum(array([0, 0]), shell_num=5)

        return

    @staticmethod
    def demo_VR_test():
        mos2 = MoS2Data()

        ##  Scan spatial distribution of V_R
        r_list = linspace(0.1, 800, 500)

        V_R = mos2.V_R(r_list)

        fig, ax_V_R = plt.subplots()
        ax_V_R.plot(r_list, V_R)
        ax_V_R.set_aspect("auto")
        ax_V_R.set_xlabel("", fontsize=12)
        ax_V_R.set_ylabel("", fontsize=12)
        ax_V_R.set_title("", fontsize=14)
        ax_V_R.set_xlim(ax_V_R.get_xlim())
        ax_V_R.set_ylim(ax_V_R.get_ylim())
        fig.savefig(
            data_file_dir + "00_small_test/V_R.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_Vq_test():
        """
        Test the Vq function
        """
        tmp_mos2 = MoS2Data()

        k_arr = tmp_mos2.path_K1
        g_arr = tmp_mos2.b1
        gamma = tmp_mos2.path_gamma

        ##  Shells number we want to calculate
        shells_list = arange(1, 50)

        # ##  Summation of V_R
        # Vq_list = []
        # for ele_shell_num in shells_list:
        #     ele_Vq = tmp_mos2.V_q_sum(k_arr, shell_num=ele_shell_num)
        #     print("Complete: ", ele_shell_num)
        #     Vq_list.append(ele_Vq)
        tmp_mos2.V_q(g_arr + 2 * g_arr, shell_num=20)
        tmp_mos2.V_q(g_arr, shell_num=20)
        tmp_mos2.V_q(gamma, shell_num=20)

        tmp_mos2.V_q(k_arr + 2 * g_arr, shell_num=20)
        tmp_mos2.V_q(k_arr, shell_num=20)

        return

    @staticmethod
    def demo_mos2_bands():
        tmp_mos2 = MoS2Data(k_mesh_density=45)

        eig_val, eig_vec = tmp_mos2.get_unitary_U(tmp_mos2.path_K1)

        # eig_vals_df, eig_vecs_df = tmp_mos2.vals_vecs_mirror_df(tmp_mos2.path_K1)

        # tmp_mos2.exciton_mat(array([0, 1]))

        # tmp_mos2.loop_to_load_save_vals_vecs_judge(array([0, 1]))
        tmp_mos2.exciton_mat(tmp_mos2.path_gamma)

        return

    @staticmethod
    def demo_mos2_converge():
        tmp_mos2 = MoS2Data(k_mesh_density=30, k_boundary=False)
        x_list = [ele[0] for ele in tmp_mos2.k_mesh()]
        y_list = [ele[1] for ele in tmp_mos2.k_mesh()]
        # x_list.pop(0)
        # y_list.pop(0)

        boundary_list = [
            tmp_mos2.path_gamma,
            tmp_mos2.b1,
            tmp_mos2.b1 + tmp_mos2.b2,
            tmp_mos2.b2,
            tmp_mos2.path_gamma,
        ]

        for ele_i in range(70):
            ele_shells = 2 * ele_i + 1

            V_q_real_list = []
            V_q_imag_list = []
            # for ele_kp in tmp_mos2.k_mesh():
            V_q, N_cell = tmp_mos2.V_q_sum(tmp_mos2.k_mesh(), shell_num=ele_shells)
            V_q_real_list.append(real(V_q))
            V_q_imag_list.append(imag(V_q))
            # V_q_real_list.pop(0)
            # V_q_imag_list.pop(0)
            fig, ax_N = plt.subplots()
            # ax_N.quiver(x_list, y_list, V_q_real_list, V_q_imag_list)
            sc = ax_N.scatter(x_list, y_list, c=V_q_real_list)
            PubMeth.draw_box(boundary_list)
            # c_ax = PubMeth.add_right_cax(ax_N, 0.01, 0.1)
            plt.colorbar(sc)
            ax_N.axis("off")
            ax_N.set_aspect("equal")
            ax_N.set_xlabel("", fontsize=12)
            ax_N.set_ylabel("", fontsize=12)
            ax_N.set_title("$N={}$".format(N_cell), fontsize=14)
            ax_N.set_xlim([-1, 2.5])
            ax_N.set_ylim([-1.5, 2.5])
            fig.savefig(
                "/home/aoxv/code/Data/bands/MoS2/V_q_sum/N_Vq_nb_{}.png".format(ele_i),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.4,
            )
            plt.close()

        # img_path = '/home/aoxv/code/Data/bands/MoS2/V_q_sum/N_Vq_nb_0.png'
        # read_img = cv2.imread(img_path)

        # writer = cv2.VideoWriter("/home/aoxv/code/Data/bands/MoS2/V_q_sum/N_Vq_nb.mp4", cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), 10, (1586, 1556))
        # total_frame = 70
        # for ele_frame in range(total_frame):
        #     img_path = '/home/aoxv/code/Data/bands/MoS2/V_q_sum/N_Vq_nb_{}.png'.format(ele_frame)

        #     read_img = cv2.imread(img_path)
        #     read_img = cv2.resize(read_img, (1586, 1556), interpolation=cv2.INTER_CUBIC)
        #     print(read_img.shape)
        #     writer.write(read_img)
        # writer.release()

        return

    @staticmethod
    def demo_struve_bessel_function():
        x = linspace(0.1, 100, 500)

        y_bessel = yn(0, x)
        y_struve = struve(0, x)

        fig, ax = plt.subplots()
        ax.plot(x, y_bessel)
        ax.plot(x, y_struve)
        ax.plot(x, y_struve - y_bessel)
        ax.set_aspect("auto")
        ax.set_xlabel("", fontsize=12)
        ax.set_ylabel("", fontsize=12)
        ax.set_title("", fontsize=14)
        ax.set_xlim(ax.get_xlim())
        ax.set_ylim(ax.get_ylim())
        fig.savefig(
            data_file_dir + "00_small_test/struve_bessel.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_PL_mos2():
        file_path = "/home/aoxv/code/Data/00_exp_data/PL/PL.xlsx"
        file_data = PubMeth.read_xlsx_data(file_path, exclude_rows_num=0)

        x_wls = file_data[0]
        y_PL = file_data[1]

        fig, ax_PL = plt.subplots()
        ax_PL.plot(x_wls, y_PL)
        ax_PL.set_aspect("auto")
        ax_PL.set_xlabel(r"$\lambda$ (nm)", fontsize=18)
        ax_PL.set_ylabel(r"Intensity (a.u.)", fontsize=18)
        ax_PL.set_title("Photoluminescence of MoS$_2$", fontsize=20)
        ax_PL.set_xlim(ax_PL.get_xlim())
        ax_PL.set_ylim(ax_PL.get_ylim())
        ax_PL.set_yticks([])
        plt.tick_params(labelsize=16)
        fig.savefig(
            data_file_dir + "PL/MoS2.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        fig, ax_PL = plt.subplots()
        ax_PL.plot(1240 / array(x_wls), y_PL)
        ax_PL.set_aspect("auto")
        ax_PL.set_xlabel(r"$E$ (eV)", fontsize=12)
        ax_PL.set_ylabel(r"Intensity (a.u.)", fontsize=12)
        ax_PL.set_title("Photoluminescence of MoS$_2$", fontsize=14)
        ax_PL.set_xlim(ax_PL.get_xlim())
        ax_PL.set_ylim(ax_PL.get_ylim())
        fig.savefig(
            data_file_dir + "PL/MoS2_e.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_comp_BK7():
        """
        Compare refractive indices of BK-7 from different database
        """
        path_1 = path = data_file_dir + "00_common_sense/N-BK7.xlsx"
        path_2 = path = data_file_dir + "00_common_sense/N-BK7_2.xlsx"

        data_1 = PubMeth.read_xlsx_data(
            path_1,
        )
        data_2 = PubMeth.read_xlsx_data(
            path_2,
        )

        x1 = data_1[0]
        x2 = data_2[0]

        y1 = data_1[1]
        y2 = data_2[1]

        fig, ax_BK7 = plt.subplots()
        ax_BK7.plot(x2, y2)
        ax_BK7.plot(x1, y1)
        ax_BK7.set_aspect("auto")
        ax_BK7.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_BK7.set_ylabel("Refractive index", fontsize=12)
        ax_BK7.set_title("", fontsize=14)
        ax_BK7.set_xlim(ax_BK7.get_xlim())
        ax_BK7.set_ylim(ax_BK7.get_ylim())
        ax_BK7.legend(["currently using", "another database"])
        fig.savefig(
            data_file_dir + "00_small_test/BK7_comp.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_if_gh_angle_test():
        ##  parameters
        wls_points = 1200

        center_list = [1]
        amp_ratio_list = [0.0]
        gamma_list = [40]

        theta_list = linspace(0, pi / 2, 50)

        ##  Get the interpolated n0 over specific wavelength range
        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_energy = 1240 / dense_wls * 1000

        ##  s1 and s2 directly from Lorentzian peaks
        sigma = PubMeth.lorentz_full(
            dense_energy,
            center_list,
            amp_ratio_list,
            gamma_list,
            True,
            pars_type="list",
        )
        s1 = real(sigma)
        s2 = imag(sigma)

        ##  r_s and r_p
        ##  Rs and phi_s matrices
        Rs_mat, phis_mat = PSHE.rs_from_s1_s2(
            s1, s2, dense_n0_index, theta_0=theta_list, cal_type="GH"
        )

        wls_list, if_shift_list = PSHE.read_mos2_if_shift_data()
        if_wls1 = wls_list[0]
        if_shift1 = array(if_shift_list[0]) + 40

        wls_list, gh_shift_list = PSHE.read_mos2_gh_shift_data()
        gh_wls1 = wls_list[0]
        gh_shift1 = array(gh_shift_list[0]) - 190

        ##  GH shift dependence on incident angle
        plot_theta_list = arange(43 / 180 * pi, 47 / 180 * pi, 0.1 / 180 * pi)
        traces_list = []
        for ele_theta in plot_theta_list:
            ele_GH_shift, ele_wls = PSHE.get_gh_shift_over_wl_s1_s2_direct_lorentz(
                center_list,
                amp_ratio_list,
                gamma_list,
                theta_0=ele_theta,
                sample_points=1000,
                wls_points=wls_points,
            )
            # ele_GH_shift = ele_GH_shift - max(ele_GH_shift)
            ele_trace = go.Scatter(
                name=round(ele_theta / pi * 180, 1), x=ele_wls, y=ele_GH_shift
            )
            traces_list.append(ele_trace)
            print("Complete angle (degree): ", round(ele_theta / pi * 180, 2))
        traces_list.append(go.Scatter(name="exp", x=gh_wls1, y=gh_shift1))

        layout = PubMeth.plotly_layout()
        fig = go.Figure(data=traces_list, layout=layout)

        fig.update_layout(
            title="GH shift without Lorentzian peaks",
            xaxis_title="Wavelength (nm)",
            yaxis_title="GH shift (nm)",
        )
        fig.write_html(data_file_dir + "00_small_test/gh_test_angles.html")

        ##  GH shift dependence on incident angle
        plot_theta_list = arange(43 / 180 * pi, 47 / 180 * pi, 0.1 / 180 * pi)
        traces_list = []
        for ele_theta in plot_theta_list:
            ele_if_shift, ele_wls = PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(
                dense_energy,
                center_list,
                amp_ratio_list,
                gamma_list,
                theta_0=ele_theta,
                wls_points=wls_points,
            )
            # ele_if_shift = ele_if_shift - min(ele_if_shift)
            ele_trace = go.Scatter(
                name=round(ele_theta / pi * 180, 1), x=ele_wls, y=ele_if_shift
            )
            traces_list.append(ele_trace)
            print("Complete angle (degree): ", round(ele_theta / pi * 180, 2))
        traces_list.append(go.Scatter(name="exp", x=if_wls1, y=if_shift1))

        layout = PubMeth.plotly_layout()
        fig = go.Figure(data=traces_list, layout=layout)

        layout = PubMeth.plotly_layout()
        fig = go.Figure(data=traces_list, layout=layout)
        fig.write_html(data_file_dir + "00_small_test/gh_test_angles.html")
        fig.update_layout(
            title="IF shift without Lorentzian peaks",
            xaxis_title="Wavelength (nm)",
            yaxis_title="IF shift (nm)",
        )
        fig.write_html(data_file_dir + "00_small_test/if_test_angles.html")

        return

    @staticmethod
    def demo_center_of_curve():
        """
        Test the center of the curve
        """
        # wls_list, shifts_list = PSHE.read_mos2_if_shift_data()

        # for ele_i in range(len(wls_list)):
        #     xbar_list, ybar_list = PSHE.get_exp_if_center()

        #     fig, ax_if = plt.subplots()
        #     ax_if.plot(wls_list[ele_i], shifts_list[ele_i])
        #     ax_if.scatter([xbar_list[ele_i]], [ybar_list[ele_i]])
        #     ax_if.set_aspect('auto')
        #     ax_if.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
        #     ax_if.set_ylabel('IF shift (nm)', fontsize=12)
        #     ax_if.set_title('Sample {}'.format(ele_i + 1), fontsize=14)
        #     ax_if.set_xlim(ax_if.get_xlim())
        #     ax_if.set_ylim(ax_if.get_ylim())
        #     fig.savefig(data_file_dir + "PSHE/exp_ob_IF/center_of_curve/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
        #     plt.close()

        # wls_list, shifts_list = PSHE.read_mos2_gh_shift_data()

        # for ele_i in range(len(wls_list)):
        #     xbar_list, ybar_list = PSHE.get_exp_gh_center()

        #     fig, ax_if = plt.subplots()
        #     ax_if.plot(wls_list[ele_i], shifts_list[ele_i])
        #     ax_if.scatter([xbar_list[ele_i]], [ybar_list[ele_i]])
        #     ax_if.set_aspect('auto')
        #     ax_if.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
        #     ax_if.set_ylabel('GH shift (nm)', fontsize=12)
        #     ax_if.set_title('Sample {}'.format(ele_i + 1), fontsize=14)
        #     ax_if.set_xlim(ax_if.get_xlim())
        #     ax_if.set_ylim(ax_if.get_ylim())
        #     fig.savefig(data_file_dir + "PSHE/exp_ob_GH/center_of_curve/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
        #     plt.close()

        PSHE.std_of_if_from_line_through_center()

        PSHE.std_of_gh_from_line_through_center()

        return

    @staticmethod
    def demo_model_comp():

        if_wls, if_shifts = PSHE.read_mos2_if_shift_data()
        gh_wls, gh_shifts = PSHE.read_mos2_gh_shift_data()
        if_xbar_list, if_ybar_list = PSHE.get_exp_if_center()
        gh_xbar_list, gh_ybar_list = PSHE.get_exp_gh_center()

        ##  Energy range we plot the sigma_1
        wls_points = 1000
        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_energy = 1240 / dense_wls * 1000  #   meV

        exp_name_list = ["Zhang", "Islam", "Ermolaev", "Hsu", "Jung"]

        for ele_i in range(len(if_wls)):

            all_pars_list = np.load(
                "/home/aoxv/code/Data/00_dash_app/data/fit_pars/fit_pars_{}.npy".format(
                    ele_i + 1
                )
            )

            energy_centers = all_pars_list[0]
            amp_ratio_list = all_pars_list[1]
            gamma_list = all_pars_list[2]

            sigma = PubMeth.lorentz_full(
                dense_energy,
                energy_centers,
                amp_ratio_list,
                gamma_list,
                timesi=True,
                pars_type="list",
            )

            permittivity_epsilon = PSHE.convert_2d_sigma_to_permittivity(
                dense_energy, sigma
            )

            n, k = PSHE.convert_permittivity_to_ref_index(permittivity_epsilon)

            n1_index = n + 1j * k

            if_shift_ref_index, if_wls_ref_index = PSHE.get_if_shift_ref_index(
                dense_wls, dense_n0_index, n1_index
            )
            gh_shift_ref_index, gh_wls_ref_index = PSHE.get_gh_shift_ref_index(
                dense_wls, dense_n0_index, n1_index
            )

            if_shift_sigma, if_wls_sigma = (
                PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(
                    dense_energy, energy_centers, amp_ratio_list, gamma_list
                )
            )
            gh_shift_sigma, gh_wls_sigma = (
                PSHE.get_gh_shift_over_wl_s1_s2_direct_lorentz(
                    energy_centers, amp_ratio_list, gamma_list
                )
            )

            xybar_if_ref_index = PubMeth.get_center_of_curve(
                if_wls_ref_index, if_shift_ref_index
            )

            xybar_gh_ref_index = PubMeth.get_center_of_curve(
                gh_wls_ref_index, gh_shift_ref_index
            )
            xybar_gh_sigma = PubMeth.get_center_of_curve(gh_wls_sigma, gh_shift_sigma)
            mutual_ybar = (
                xybar_gh_ref_index[1] + xybar_gh_sigma[1] + gh_ybar_list[ele_i]
            ) / 3

            gh_diff_ref_index = xybar_gh_ref_index[1] - mutual_ybar
            gh_diff_sigma = xybar_gh_sigma[1] - mutual_ybar
            gh_diff_exp = gh_ybar_list[ele_i] - mutual_ybar

            mod_gh_shift_ref_index = gh_shift_ref_index - gh_diff_ref_index
            mod_gh_shift_sigma = gh_shift_sigma - gh_diff_sigma
            mod_gh_shift_exp = gh_shifts[ele_i] - gh_diff_exp

            fig, ax_gh_comp = plt.subplots()
            ax_gh_comp.plot(gh_wls[ele_i], mod_gh_shift_exp, ".")
            ax_gh_comp.plot(gh_wls_ref_index, mod_gh_shift_ref_index)
            ax_gh_comp.plot(gh_wls_sigma, mod_gh_shift_sigma)
            ax_gh_comp.set_aspect("auto")
            ax_gh_comp.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
            ax_gh_comp.set_ylabel("GH shift (nm)", fontsize=12)
            ax_gh_comp.set_title("", fontsize=14)
            ax_gh_comp.set_xlim(ax_gh_comp.get_xlim())
            ax_gh_comp.set_ylim(ax_gh_comp.get_ylim())
            ax_gh_comp.legend(
                [
                    "Experiment result",
                    "Thin-film model",
                    "Conductivity model",
                ]
            )
            fig.savefig(
                data_file_dir
                + "PSHE/model_comp/GH shift_same_center/sample_{}.png".format(
                    ele_i + 1
                ),
                dpi=330,
                facecolor="w",
                bbox_inches="tight",
                pad_inches=0.1,
            )
            plt.close()

            if_diff_between_xybar = if_ybar_list[ele_i] - xybar_if_ref_index[1]

            mod_exp_if = array(if_shifts[ele_i]) - if_diff_between_xybar

            # fig, ax_list = plt.subplots(1, 2, figsize=(10, 5))
            # ax_n, ax_k = ax_list

            # ax_n.plot(dense_wls, n)
            # ax_k.plot(dense_wls, k)

            # for ele_name in exp_name_list:
            #     ele_file = data_file_dir + "PSHE/exp_indices/" + ele_name + '.csv'
            #     data = pd.read_csv(ele_file)

            #     ele_wls = list(data['Wavelength, µm'] * 1000)
            #     ele_n = list(data['n'])
            #     ele_k = list(data['k'])

            #     ax_n.plot(ele_wls, ele_n)
            #     ax_k.plot(ele_wls, ele_k)
            # ax_n.set_aspect('auto')
            # ax_n.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
            # ax_n.set_ylabel(r'$n$', fontsize=12)
            # ax_n.set_title('Real part', fontsize=14)
            # ax_n.set_xlim([500, 700])
            # ax_n.set_ylim(ax_n.get_ylim())
            # ax_n.legend(["Theoretical"] + exp_name_list)

            # ax_k.set_aspect('auto')
            # ax_k.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
            # ax_k.set_ylabel(r'$\kappa$', fontsize=12)
            # ax_k.set_title('Imaginary part', fontsize=14)
            # ax_k.set_xlim([500, 700])
            # ax_k.set_ylim(ax_k.get_ylim())
            # ax_k.legend(["Theoretical"] + exp_name_list)
            # fig.savefig(data_file_dir + "PSHE/model_comp/the_exp_ref_indices/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            # plt.close()

            # fig, ax_if = plt.subplots()
            # ax_if.plot(if_wls[ele_i], mod_exp_if)
            # ax_if.plot(if_wls_ref_index, if_shift_ref_index)
            # ax_if.plot(if_wls_sigma, if_shift_sigma)
            # ax_if.set_aspect('auto')
            # ax_if.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
            # ax_if.set_ylabel('IF shift (nm)', fontsize=12)
            # ax_if.set_title('', fontsize=14)
            # ax_if.set_xlim(ax_if.get_xlim())
            # ax_if.set_ylim(ax_if.get_ylim())
            # ax_if.legend(["Experiment result", "Thin-film model", "Conductivity model"])
            # fig.savefig(data_file_dir + "PSHE/model_comp/IF shift/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            # plt.close()

            # gh_diff_between_xybar = gh_ybar_list[ele_i] - xybar_gh_sigma[1]

            # mod_exp_gh = array(gh_shifts[ele_i]) - gh_diff_between_xybar

            # fig, ax_gh1 = plt.subplots()
            # ax_gh1.plot(gh_wls[ele_i], mod_exp_gh)
            # ax_gh1.plot(gh_wls_sigma, gh_shift_sigma)
            # ax_gh1.set_aspect('auto')
            # ax_gh1.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
            # ax_gh1.set_ylabel('GH shift (nm)', fontsize=12)
            # ax_gh1.set_title('Conductivity model', fontsize=14)
            # ax_gh1.set_xlim(ax_gh1.get_xlim())
            # ax_gh1.set_ylim(ax_gh1.get_ylim())
            # ax_gh1.legend(["Experiment result", "Theoretical"])
            # fig.savefig(data_file_dir + "PSHE/model_comp/GH shift_cond/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            # plt.close()

            # gh_diff_between_xybar = gh_ybar_list[ele_i] - xybar_gh_ref_index[1]

            # mod_exp_gh = array(gh_shifts[ele_i]) - gh_diff_between_xybar

            # fig, ax_gh2 = plt.subplots()
            # ax_gh2.plot(gh_wls[ele_i], mod_exp_gh)
            # ax_gh2.plot(gh_wls_ref_index, gh_shift_ref_index)
            # ax_gh2.set_aspect('auto')
            # ax_gh2.set_xlabel(r'$\lambda$ (nm)', fontsize=12)
            # ax_gh2.set_ylabel('GH shift (nm)', fontsize=12)
            # ax_gh2.set_title('Thin-film model', fontsize=14)
            # ax_gh2.set_xlim(ax_gh2.get_xlim())
            # ax_gh2.set_ylim(ax_gh2.get_ylim())
            # ax_gh2.legend(["Experiment result", "Theoretical"])
            # fig.savefig(data_file_dir + "PSHE/model_comp/GH shift_thin_film/sample_{}.png".format(ele_i + 1), dpi=330, facecolor='w', bbox_inches='tight', pad_inches=0.1)
            # plt.close()

        return

    @staticmethod
    def demo_lorentz_puzzle():
        """
        Compare different imaginary part
        """

        energy_centers = [1823.56, 1924.11, 2030.66, 2127.53, 2193.29, 2370.82]
        amp_ratio_list = [0.32, 0.3, 0.39, 0.25, 0.25, 0.31]
        gamma_list = [55.63, 80.0, 78.65, 26.19, 23.0, 59.52]

        ##  Energy range we plot the sigma_1
        wls_points = 1000
        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_energy = 1240 / dense_wls * 1000  #   meV

        sigma = PubMeth.lorentz_full(
            dense_energy,
            energy_centers,
            amp_ratio_list,
            gamma_list,
            timesi=True,
            pars_type="list",
        )

        if_shift_sigma, if_wls_sigma = PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(
            dense_energy, energy_centers, amp_ratio_list, gamma_list
        )

        fig, ax_fig1 = plt.subplots()
        ax_fig1.plot(if_wls_sigma, if_shift_sigma)
        ax_fig1.set_aspect("auto")
        ax_fig1.set_xlabel(r"$\lambda$ (nm)", fontsize=12)
        ax_fig1.set_ylabel("IF shift (nm)", fontsize=12)
        ax_fig1.set_title("", fontsize=14)
        ax_fig1.set_xlim(ax_fig1.get_xlim())
        ax_fig1.set_ylim(ax_fig1.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/lorentz/model2.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_comp_ref_indices():
        """
        Compare theoretical refractive indices and experimental results
        """
        exp_name_list = ["Zhang", "Islam", "Ermolaev", "Hsu", "Jung"]

        for ele_name in exp_name_list:
            ele_file = data_file_dir + "PSHE/exp_indices/" + ele_name + ".csv"
            data = pd.read_csv(ele_file)

        return

    @staticmethod
    def demo_continuous_lorentz_fit():
        """
        Set up many Lorentzian peaks to fit the experimental curve
        """

        return

    @staticmethod
    def demo_comp_Wu_mos2_lorentzian_mos2():
        wls, cond_realpart, cond_imagpart = (
            PSHE.read_mos2_the_cond_Wu_as_e2_h_unshifted()
        )

        data_set = pd.read_csv(
            "/home/aoxv/code/Data/00_common_sense/Wu_cond_real_original.csv"
        )

        E = data_set["E"]
        S1 = data_set["S1"]

        E2 = 1240 / wls

        fig, ax_comp = plt.subplots()
        ax_comp.plot(E, S1)
        ax_comp.plot(E2, cond_realpart)
        ax_comp.plot(E2, cond_imagpart)
        ax_comp.set_aspect("auto")
        ax_comp.set_xlabel("E (eV)", fontsize=12)
        ax_comp.set_ylabel(r"$e^2/h$", fontsize=12)
        ax_comp.set_title("", fontsize=14)
        ax_comp.set_xlim(ax_comp.get_xlim())
        ax_comp.set_ylim(ax_comp.get_ylim())
        ax_comp.legend(
            [
                "Original data",
                "Lorentzian-fitted real part",
                "Lorentzian-fitted imaginary part",
            ]
        )
        fig.savefig(
            data_file_dir + "PSHE/MoS2_cond_Wu/comp_origin_lorentzian_fit.pdf",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    @staticmethod
    def demo_all_exp_if_data():
        """
        Plot all the experimental data in one figure
        """
        if_wls, if_shifts = PSHE.read_mos2_if_shift_data()
        gh_wls, gh_shifts = PSHE.read_mos2_gh_shift_data()

        fig_IF = plt.figure(figsize=(18, 10))
        spec_IF = fig_IF.add_gridspec(
            nrows=2,
            ncols=14,
        )
        fig_GH = plt.figure(figsize=(18, 10))
        spec_GH = fig_GH.add_gridspec(
            nrows=2,
            ncols=14,
        )

        for ele_i in range(3):
            ax1 = fig_IF.add_subplot(
                spec_IF[0, ele_i * 4 + ele_i : (ele_i + 1) * 4 + ele_i]
            )
            ax1.plot(if_wls[ele_i], if_shifts[ele_i])
            ax1.set_aspect("auto")
            ax1.set_xlabel("$\lambda$ (nm)", fontsize=12)
            ax1.set_ylabel("IF shift (nm)", fontsize=12)
            ax1.set_title("Sample {}".format(ele_i + 1), fontsize=14)

            ax2 = fig_GH.add_subplot(
                spec_GH[0, ele_i * 4 + ele_i : (ele_i + 1) * 4 + ele_i]
            )
            ax2.plot(gh_wls[ele_i], gh_shifts[ele_i])
            ax2.set_aspect("auto")
            ax2.set_xlabel("$\lambda$ (nm)", fontsize=12)
            ax2.set_ylabel("GH shift (nm)", fontsize=12)
            ax2.set_title("Sample {}".format(ele_i + 1), fontsize=14)

        for ele_i in range(2):
            ax1 = fig_IF.add_subplot(spec_IF[1, ele_i * 6 + 2 : ele_i * 6 + 6])
            ax1.plot(if_wls[ele_i + 3], if_shifts[ele_i + 3])
            ax1.set_aspect("auto")
            ax1.set_xlabel("$\lambda$ (nm)", fontsize=12)
            ax1.set_ylabel("IF shift (nm)", fontsize=12)
            ax1.set_title("Sample {}".format(ele_i + 1 + 3), fontsize=14)

            ax2 = fig_GH.add_subplot(spec_GH[1, ele_i * 6 + 2 : ele_i * 6 + 6])
            ax2.plot(gh_wls[ele_i + 3], gh_shifts[ele_i + 3])
            ax2.set_aspect("auto")
            ax2.set_xlabel("$\lambda$ (nm)", fontsize=12)
            ax2.set_ylabel("GH shift (nm)", fontsize=12)
            ax2.set_title("Sample {}".format(ele_i + 1 + 3), fontsize=14)

        fig_IF.savefig(
            data_file_dir + "PSHE/exp_ob/shifts_collection/if_collections.pdf",
            bbox_inches="tight",
            pad_inches=0.1,
            dpi=330,
        )
        plt.close(fig_IF)

        fig_GH.savefig(
            data_file_dir + "PSHE/exp_ob/shifts_collection/gh_collections.pdf",
            bbox_inches="tight",
            pad_inches=0.1,
            dpi=330,
        )
        plt.close(fig_GH)

        return

    @staticmethod
    def demo_dimensionless_IF_GH():
        """
        To test the dimensionless IF and GH
        """
        center_list = [2000]
        gamma_list = [50]
        amp_ratio_list = [0.0]

        wls_points = 1000

        dense_wls, dense_n0_index, f_n0 = PSHE.get_n0_interp_func(wls_points)
        dense_energy = 1240 / dense_wls * 1000

        IF_shift_0, out_wls_0 = PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(
            dense_energy, center_list, amp_ratio_list, gamma_list, dimensionless=False
        )

        center_list = [2000, 2100]
        gamma_list = [50, 70]
        amp_ratio_list = [0.3, 0.3]

        IF_shift, out_wls = PSHE.get_if_shift_over_wl_s1_s2_direct_lorentz(
            dense_energy, center_list, amp_ratio_list, gamma_list, dimensionless=False
        )

        fig, ax_dimensionless = plt.subplots()
        ax_dimensionless.plot(1240 / out_wls * 1000, IF_shift / IF_shift_0)
        ax_dimensionless.set_aspect("auto")
        ax_dimensionless.set_xlabel("$\lambda$ (nm)", fontsize=12)
        ax_dimensionless.set_ylabel("$k_0 \Delta_{IF}$", fontsize=12)
        ax_dimensionless.set_title("Dimensionless IF shift", fontsize=14)
        ax_dimensionless.set_xlim(ax_dimensionless.get_xlim())
        ax_dimensionless.set_ylim(ax_dimensionless.get_ylim())
        fig.savefig(
            data_file_dir + "PSHE/shifts_theory/dimensionless_IF.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return

    # @staticmethod
    # def


def main():
    DemoFunc.demo_mono_mos2()
    pass


if __name__ == "__main__":
    main()
