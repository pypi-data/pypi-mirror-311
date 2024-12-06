from ..filesop.fileman import FileManager
from .optcond_cal import OptCondCal
import numpy as np
from ..filesop.filesave import FilesSave
import matplotlib.pyplot as plt
from ..pubmeth import PubMethod
from ..vel_op.velop_cal import VelLoad
from tqdm import tqdm


plt.rc("font", family="Times New Roman")  # change the font of plot
plt.rcParams["mathtext.fontset"] = "stix"

__all__ = ["OptCondPlot"]


class OptCondPlot:
    fontsize = 12
    titlesize = 14

    def __init__(
        self,
        OptCondInst: OptCondCal,
        ffolder="",
        disable_elet=False,
    ) -> None:
        self.OptCondInst = OptCondInst
        self.ffolder = ffolder
        self.results_list = ["cond_dist", "kvecs", "bz_bounds"]

        self.OptFileInst = FileManager(
            self.OptCondInst,
            root_dir_name="OptCond",
            ffolder=ffolder,
            results_list=self.results_list,
        )

        self.disable_elet = disable_elet

    def _plot_ele_mat(
        self,
        ab_dist: np.ndarray,  #   (kpoints, e_range) array
        k_arrs: np.ndarray,
        bound_vecs: np.ndarray,
        save_dir: FilesSave,
    ) -> None:
        fig, ax = plt.subplots(figsize=(7, 7))
        print("Shape: ", ab_dist.shape)

        for ele_col in tqdm(range(ab_dist.shape[-1])):
            fname = self.OptFileInst.ele_name.format(self.OptCondInst.e_range[ele_col])
            title = r"$\theta = {:.2f}\degree$ $E = {:.2f}$ meV".format(
                self.OptCondInst.haInst.moInst.twist_angle,
                self.OptCondInst.e_range[ele_col],
            )  #   title for each photon energy

            PubMethod.cmap_scatters(  # No need for square matrix to plot the distributions
                k_arrs[:, 0],
                k_arrs[:, 1],
                np.real(ab_dist[:, ele_col]),
                bound_vecs,
                save_dir,
                fname,
                title=title,
                clabel_name="Absorption (a.u.)",
                figax_in=(fig, ax),
                cmap="jet",
            )
        plt.close(fig)

    def _plot_overall(self, cond_intensity):
        fig, ax_ab = plt.subplots(figsize=(7, 5))
        (line,) = ax_ab.plot(self.OptCondInst.e_range, np.real(cond_intensity))
        ax_ab.set_aspect("auto")
        ax_ab.set_xlabel("E (meV)", fontsize=12)
        ax_ab.set_ylabel(r"$\sigma_{\text{mono}}$", fontsize=12)
        ax_ab.set_title(self.OptCondInst.haInst.sigs_title, fontsize=14)
        self.OptFileInst.root_dir.save_fig(
            fig,
            f"Cond_real_{self.OptCondInst.gamma}",
        )
        line.remove()
        ax_ab.plot(self.OptCondInst.e_range, np.imag(cond_intensity))
        self.OptFileInst.root_dir.save_fig(
            fig,
            f"Cond_imag_{self.OptCondInst.gamma}",
        )
        plt.close(fig)

    def plot(
        self, update_elet: bool = False, check_bds_upd=False, load_from_exist_dat=False
    ) -> np.ndarray:
        """Calculations and plot of complex conductivity

        Args:
            update_elet: [Update the ele transitions figure or not]
            update_gamma: [update gamma or e_range or not]

        Returns:
            Complex conductivity of (kp, e_range) shape
        """
        if load_from_exist_dat:
            print(
                "Loading existing data. Excluding calculations based on broadening and incident photon energy."
            )
            cond_dist, k_arrs, bound_vecs = (
                self.OptFileInst.load()
            )  #   (kp, e_range) shape
            cond_intensity = np.sum(cond_dist, axis=0)
            self._plot_overall(cond_intensity)
            return cond_dist

        Mop2, ediff, k_arrs, bound_vecs = VelLoad(self.OptCondInst.velopCalInst).load(
            check_bds_upd, upd_vel_files=self.OptCondInst.upd_vel_files
        )

        #
        cond_dist_mat = []
        for ele_e in self.OptCondInst.e_range:
            tmp_cond = (
                Mop2 / (ediff * (ediff - ele_e + 1j * self.OptCondInst.gamma)) * 1j
            )
            cond_dist_mat.append(
                np.sum(
                    tmp_cond * self.OptCondInst.renorm_const,
                    axis=(len(Mop2.shape) - 1, len(Mop2.shape) - 2),
                )
            )

        cond_dist_mat = np.array(cond_dist_mat)  #   (e_range, kp) shape
        cond_dist_mat = cond_dist_mat.T  #   (kp, e_range) shape

        cond_dist: np.ndarray = cond_dist_mat  #   (kp, e_range) shape

        if (not self.disable_elet) or (update_elet):
            print("Plotting element transitions...")
            self._plot_ele_mat(cond_dist, k_arrs, bound_vecs, self.OptFileInst.root_dir)
        cond_intensity = np.sum(cond_dist, axis=0)

        self._plot_overall(cond_intensity)

        self.OptFileInst.save([cond_dist, k_arrs, bound_vecs])

        return cond_intensity
