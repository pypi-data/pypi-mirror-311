from pkg_import.pkg_import import *
from pshe.exp_data import BK7Substrate, MoS2Data
from pshe.if_calculation import IFCalculation
from pshe.gh_calculation import GHCalculation
from pshe.optics import *


class EigenShiftDifference:
    def __init__(self, incident_angles=None) -> None:
        if incident_angles is None:
            incident_angles = [pi / 4]
        self.theta_0s = incident_angles

        self.lcp, self.rcp = self._lcp_rcp_if_object()
        self.s, self.p = self._s_p_gh_object()

        pass

    def _lcp_rcp_if_object(self):
        lcp = IFCalculation(a_s=1, a_p=1, incident_angles=self.theta_0s)
        rcp = IFCalculation(a_s=1, a_p=1, eta=-pi / 2, incident_angles=self.theta_0s)
        return lcp, rcp

    def _s_p_gh_object(self):
        s = GHCalculation(a_s=1, a_p=0, incident_angles=self.theta_0s)
        p = GHCalculation(a_s=0, a_p=1, incident_angles=self.theta_0s)
        return s, p

    def lcp_rcp_if_thin_film(self, wavelengths, n1_index, thickness):
        lcp_if_wls, lcp_if_shift = self.lcp.thin_film_model(
            wavelengths, n1_index, thickness
        )
        rcp_if_wls, rcp_if_shift = self.rcp.thin_film_model(
            wavelengths, n1_index, thickness
        )

        return lcp_if_wls, rcp_if_shift - lcp_if_shift

    def lcp_rcp_if_lorentz_thin_film(
        self, wavelengths, n1_index, thickness, perm_infty=15.6
    ):
        ComplexRefractiveIndex()

        lcp_if_wls, lcp_if_shift = self.lcp.thin_film_model(
            wavelengths, n1_index, thickness
        )
        rcp_if_wls, rcp_if_shift = self.rcp.thin_film_model(
            wavelengths, n1_index, thickness
        )

        return lcp_if_wls, rcp_if_shift - lcp_if_shift

    def lcp_rcp_if_conductivity(self, wls, sigma):
        lcp_if_wls, lcp_if_shift = self.lcp.conductivity_model(wls, sigma)
        rcp_if_wls, rcp_if_shift = self.rcp.conductivity_model(wls, sigma)

        return lcp_if_wls, rcp_if_shift - lcp_if_shift

    def lcp_rcp_if_lorentz_conductivity(self, centers, amps, gammas, energy=None):
        lcp_if_wls, lcp_if_shift = self.lcp.lorentz_conductivity_model(
            centers, amps, gammas, energy=energy
        )
        rcp_if_wls, rcp_if_shift = self.rcp.lorentz_conductivity_model(
            centers, amps, gammas, energy=energy
        )

        return lcp_if_wls, rcp_if_shift - lcp_if_shift

    def s_p_gh_thin_film(self, wavelengths, n1_index, thickness, sample_index):
        """
        Calculate GH shift based on thin-film model
        """
        s_gh_wls, s_gh_shift = self.s.thin_film_model(wavelengths, n1_index, thickness)
        p_gh_wls, p_gh_shift = self.p.thin_film_model(wavelengths, n1_index, thickness)

        GHCalculation.post_treatment(
            s_gh_wls,
            s_gh_shift,
            theta_0s=self.theta_0s,
            save_name="sample_{}".format(sample_index),
            sub_save_dir="Delta-/perm_based",
            title=r"$\Delta^-$",
        )

        GHCalculation.post_treatment(
            p_gh_wls,
            p_gh_shift,
            theta_0s=self.theta_0s,
            save_name="sample_{}".format(sample_index),
            sub_save_dir="Delta+/perm_based",
            title=r"$\Delta^+$",
        )

        return s_gh_wls, p_gh_shift - s_gh_shift

    def s_p_gh_lorentz_conductivity(self, centers, amps, gammas):
        """
        Calculate GH shift based on thin-film model

        # Return
        s_gh_wls, p_gh_shift - s_gh_shift
        """
        s_gh_wls, s_gh_shift = self.s.lorentz_conductivity_model(centers, amps, gammas)
        p_gh_shift = self.p.lorentz_conductivity_model(centers, amps, gammas)[1]

        return s_gh_wls, p_gh_shift - s_gh_shift


class BackgroundShift(EigenShiftDifference):
    def __init__(self, incident_angles=None, exp_data_ob=MoS2Data()) -> None:
        super().__init__(incident_angles)
        self.exp_data_ob = exp_data_ob

    def _bg_centers(self, wls, shift_1, shift_2):
        bg_shift = shift_1 - shift_2

        bg_xbar, bg_ybar = PlotMethod(wls[0], bg_shift[0]).center_of_curve()
        return bg_xbar, bg_ybar

    def _shift_exp_data(self, bg_center_y, exp_type):
        """Shift the experiment data to the background

        # Args:
            bg_center_y (float): Y component of the theoretical background center

            exp_type (str): "if" of "gh"

        # Returns:
            list: list of shifted shifts
        """
        shifts_list = []
        for ele_i in range(len(self.exp_data_ob.gh_centers)):
            if exp_type == "if":
                center_y = self.exp_data_ob.if_centers[ele_i][1]
                shifted_exp_if = [
                    self.exp_data_ob.if_shifts_list[ele_i] + bg_center_y - center_y
                ]
            elif exp_type == "gh":
                center_y = self.exp_data_ob.gh_centers[ele_i][1]
                shifted_exp_if = [
                    self.exp_data_ob.gh_shifts_list[ele_i] + bg_center_y - center_y
                ]
            shifts_list.append(shifted_exp_if)

        return shifts_list

    def _shift_sp_data(self, sp_center_y, polartype=Literal["s", "p"]):
        shifts_list = []
        for ele_i in range(len(self.exp_data_ob.gh_centers)):
            if polartype == "s":
                center_y = self.exp_data_ob.s_centers[ele_i][1]
                shifted_exp = [
                    self.exp_data_ob.s_shifts[ele_i] + sp_center_y - center_y
                ]
            elif polartype == "p":
                center_y = self.exp_data_ob.p_centers[ele_i][1]
                shifted_exp = [
                    self.exp_data_ob.p_shifts[ele_i] + sp_center_y - center_y
                ]
            shifts_list.append(shifted_exp)
        return shifts_list

    def bg_if_shift_perm_based(self):
        bg_wls, rcp_shift = self.rcp.bg_shift_perm_based()
        lcp_shift = self.lcp.bg_shift_perm_based()[1]
        return bg_wls, rcp_shift - lcp_shift

    def bg_if_center_perm_based(self):
        bg_wls, rcp_shift = self.rcp.bg_shift_perm_based()
        lcp_shift = self.lcp.bg_shift_perm_based()[1]
        return self._bg_centers(bg_wls, rcp_shift, lcp_shift)

    def bg_if_center_cond_based(self):
        bg_wls, rcp_shift = self.rcp.bg_shift_cond_based()
        lcp_shift = self.lcp.bg_shift_cond_based()[1]
        return self._bg_centers(bg_wls, rcp_shift, lcp_shift)

    def bg_gh_center_cond_based(self):
        bg_wls, s_shift = self.s.bg_shift_cond_based()
        p_shift = self.p.bg_shift_cond_based()[1]
        return self._bg_centers(bg_wls, p_shift, s_shift)

    def bg_gh_center_perm_based(self):
        bg_wls, s_shift = self.s.bg_shift_perm_based()
        p_shift = self.p.bg_shift_perm_based()[1]
        return self._bg_centers(bg_wls, p_shift, s_shift)

    def shifted_exp_if_cond_based(self):
        bg_if_center_y = self.bg_if_center_cond_based()[1]

        return self._shift_exp_data(bg_if_center_y, exp_type="if")

    def shifted_exp_if_perm_based(self):
        bg_if_center_y = self.bg_if_center_perm_based()[1]

        return self._shift_exp_data(bg_if_center_y, exp_type="if")

    def shifted_exp_gh_cond_based(self):
        bg_gh_center_y = self.bg_gh_center_cond_based()[1]
        return self._shift_exp_data(bg_gh_center_y, exp_type="gh")

    def shifted_exp_gh_perm_based(self):
        bg_gh_center_y = self.bg_gh_center_perm_based()[1]

        return self._shift_exp_data(bg_gh_center_y, exp_type="gh")

    def shifted_exp_s_perm_base(self):
        bg_wls, s_shift = self.s.bg_shift_perm_based()
        bg_s_center_y = self._bg_centers(bg_wls, s_shift, np.zeros(s_shift.shape))[1]
        shifted_s_shifts = self._shift_sp_data(bg_s_center_y, "s")
        return shifted_s_shifts, bg_wls, s_shift

    def shifted_exp_p_perm_base(self):
        bg_wls, p_shift = self.p.bg_shift_perm_based()
        bg_p_center_y = self._bg_centers(bg_wls, p_shift, np.zeros(p_shift.shape))[1]
        shifted_p_shifts = self._shift_sp_data(bg_p_center_y, "p")
        return shifted_p_shifts, bg_wls, p_shift


def main():
    ob = BackgroundShift([pi / 4])
    ps, bgwls, bgpshift = ob.shifted_exp_p_perm_base()
    ss, bgwls, bgsshift = ob.shifted_exp_s_perm_base()

    fig, ax = plt.subplots()
    for i in range(len(ob.exp_data_ob.gh_wls_list)):
        ax.plot(ob.exp_data_ob.gh_wls_list[i], ps[i][0])
    ax.plot(bgwls[0], bgpshift[0])
    ax.set_aspect("auto")
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.set_title("", fontsize=14)
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    fig.savefig("tmpplotps_withbg.png")
    plt.close()

    fig, ax = plt.subplots()
    for i in range(len(ob.exp_data_ob.gh_wls_list)):
        ax.plot(ob.exp_data_ob.gh_wls_list[i], ss[i][0])
    ax.plot(bgwls[0], bgsshift[0])
    ax.set_aspect("auto")
    ax.set_xlabel("", fontsize=12)
    ax.set_ylabel("", fontsize=12)
    ax.set_title("", fontsize=14)
    ax.set_xlim(ax.get_xlim())
    ax.set_ylim(ax.get_ylim())
    fig.savefig("tmpplotss_withbg.png")
    plt.close()
    return


if __name__ == "__main__":
    main()
