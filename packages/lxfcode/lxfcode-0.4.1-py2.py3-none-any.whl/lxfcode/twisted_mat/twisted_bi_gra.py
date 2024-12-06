# # 这是转角双层石墨烯的连续模型和紧束缚模型的代码整理，里面包含了一些功能实现，如吸收谱，拉曼光谱等。
# # 这部分为在计算当中需要用到的常数
from public.consts import *
from public.method import *

data_file_dir = expanduser("~/code") + os.sep + "Data" + os.sep


class ContiTbgInst:  # # 连续性模型的核心代码
    # # 若干常量的定义

    if "SLURM_CPUS_PER_TASK" in os.environ:
        cores_num = int(os.environ["SLURM_CPUS_PER_TASK"])
    else:
        cores_num = multiprocessing.cpu_count()
    print("Cores Num: ", cores_num)

    interval_k = 0.005

    b_p_arr = array([sqrt(3) / 2, 3 / 2])
    b_n_arr = array([-sqrt(3) / 2, 3 / 2])

    gamma0_arr = array([0, 0])
    gamma1_arr = array([-sqrt(3) / 2, 3 / 2])
    gamma2_arr = array([-sqrt(3), 0])
    k_b_arr = array([-sqrt(3) / 2, -1 / 2])
    k_t_arr = array([-sqrt(3) / 2, 1 / 2])
    m_1_arr = array([-sqrt(3) / 2, 0])
    m_2_arr = array([-sqrt(3) / 4, 3 / 4])

    # # k空间的路径定义
    default_paths = [
        [k_b_arr, k_t_arr, gamma1_arr, gamma0_arr, k_b_arr],
        [k_b_arr, k_t_arr, gamma1_arr, gamma2_arr, k_b_arr],
        [k_b_arr, gamma0_arr, m_1_arr, k_t_arr],
        [k_b_arr, k_t_arr],
    ]
    default_path_labels = [
        [r"K$_{\rm b}$", r"K$_{\rm t}$", r"$\Gamma$", r"$\Gamma$", r"K$_{\rm b}$"],
        [r"K$_{\rm b}$", r"K$_{\rm t}$", r"$\Gamma$", r"$\Gamma$", r"K$_{\rm b}$"],
        [r"K$_{\rm b}$", r"$\Gamma$", r"M", r"K$_{\rm t}$"],
        [r"K$_{\rm b}$", r"K$_{\rm t}$"],
    ]

    # # 初始化及可选参数定义
    def __init__(
        self,
        twist_angle_conti,
        v_F=1e6,
        w=118,
        kp_num=70,
        raman_gamma=100,
        ab_delta=100,
        e_phonon=196,
        a0_constant=1.42 * sqrt(3),
        basis_loop_times=7,
        density_per_path=100,
        density_per_jdos_path=200,
    ):  # m/s for v_F, meV for w
        self.density_per_path = density_per_path

        self.twist_angle_conti = twist_angle_conti
        self.twist_theta_conti = twist_angle_conti / 180 * pi

        self.a0_constant_conti = a0_constant
        self.unit_origin_cell_area_conti = sqrt(3) / 2 * self.a0_constant_conti**2
        self.norm_KG_conti = 4 * pi / (3 * self.a0_constant_conti)

        self.aM_lattice_conti = self.a0_constant_conti / (
            2 * sin(self.twist_theta_conti / 2)
        )  # the moire lattice length
        self.unit_moire_cell_area_conti = (
            sqrt(3) / 2 * self.aM_lattice_conti**2
        )  # the area of moire unit
        self.norm_Kg_conti = abs(
            4 * pi / (3 * self.aM_lattice_conti)
        )  # the norm of Kg in k-space

        self.v_F = v_F  # Fermi velocity
        self.epsilon = (
            h_bar_eV * self.v_F * self.norm_Kg_conti * m2A * eV2meV
        )  # dimensionless constant (describes the energy)
        self.w = w  # interlayer coupling in tbg

        self.kp_num = kp_num  # number of k points along one side of diamond Brillouin zone in k-space
        self.N_k = int(kp_num**2)  # number of total k points

        self.raman_gamma = raman_gamma  # the broadening parameter in raman calculations
        self.e_phonon = e_phonon  # the energy of G-band model in raman calculations
        self.ab_delta = ab_delta  # the broadening parameter in absorption calculations
        self.ab_renorm_const = (
            2
            * c_eV**2
            / (h_bar_eV * c_speed * epsilon_0_eV)
            / self.N_k
            / self.unit_moire_cell_area_conti
        )  # the renormalization constant in absorption calculations, remember that here the factor 2 accounts for the valley degeneracy
        self.jdos_renorm_with_area = (
            2 / self.N_k / self.unit_moire_cell_area_conti
        )  # the renormalization constant in jdos calculations

        self.pre_basis_list = self.basis_set(
            basis_loop_times
        )  # pre-calculated set of basis in the calculations
        self.pre_basis_layer_base = [
            ele_basis for ele_basis in self.pre_basis_list if ele_basis[2] == 1
        ]
        self.pre_basis_layer_twist = [
            ele_basis for ele_basis in self.pre_basis_list if ele_basis[2] == 2
        ]
        self.inter_h_12, self.inter_h_21 = self.inter_h_pre_mat()
        self.intra_h1_k, self.intra_h2_k = self.intra_h_pre_k_mat()
        # print(len(self.pre_basis_list))

        self.kps_in_BZ, self.BZ_boundaries_vecs = self.kp_in_moire_b_zone(
            boundary_vec_return=True
        )
        self.mat_type = "TBG"
        self.model_type = "conti"

    # # 底层石墨烯哈密顿量定义，k矢量已经旋转
    def h_b(self, k):
        x_wave = k[0] - self.k_b_arr[0]
        y_wave = k[1] - self.k_b_arr[1]
        return self.epsilon * array(
            [
                [0, (x_wave - 1j * y_wave) * exp(-1j * self.twist_theta_conti / 2)],
                [(x_wave + 1j * y_wave) * exp(1j * self.twist_theta_conti / 2), 0],
            ]
        )

    # # 顶层石墨烯哈密顿量定义，k矢量已经旋转
    def h_t(self, k):
        x_wave = k[0] - self.k_t_arr[0]
        y_wave = k[1] - self.k_t_arr[1]
        return self.epsilon * array(
            [
                [0, (x_wave - 1j * y_wave) * exp(1j * self.twist_theta_conti / 2)],
                [(x_wave + 1j * y_wave) * exp(-1j * self.twist_theta_conti / 2), 0],
            ]
        )

    # # 层间耦合矩阵1
    def t_0(self):
        return self.w * array([[1, 1], [1, 1]])

    # # 层间耦合矩阵2
    def t_p1(self):
        return self.w * array([[1, exp(-2j * pi / 3)], [exp(2j * pi / 3), 1]])

    # # 层间耦合矩阵3
    def t_n1(self):
        return self.w * array([[1, exp(2j * pi / 3)], [exp(-2j * pi / 3), 1]])

    # # 1层至2层k点的耦合
    @staticmethod
    def layer1to2(vec):  # (the number of b_p, the number of b_n)
        v1 = (vec[0], vec[1], 2)  # the same wave vector
        v2 = (vec[0] + 1, vec[1], 2)  # plus a b_p
        v3 = (vec[0], vec[1] + 1, 2)  # plus a b_n
        return v1, v2, v3

    # # 2层至1层k点的耦合
    @staticmethod
    def layer2to1(vec):
        v1 = (vec[0], vec[1], 1)  # the same wave vector
        v2 = (vec[0] - 1, vec[1], 1)  # minus a b_p
        v3 = (vec[0], vec[1] - 1, 1)  # minus a b_n
        return v1, v2, v3

    # # 基矢构建
    @staticmethod
    def basis_set(loop_times):  # create the basis of calculation
        t1 = time.perf_counter()
        layer1_basis = [(0, 0, 1)]
        layer1_to_2 = True
        layer2_basis = []
        layer2_to_1 = False
        times = 0
        layer1_new_basis = [(0, 0, 1)]
        layer2_new_basis = []
        while times < loop_times:
            times = times + 1
            if layer1_to_2 and (not layer2_to_1):
                new_layer2_basis_list = [
                    ele_tuple + array([[0, 0, 1], [1, 0, 1], [0, 1, 1]])
                    for ele_tuple in layer1_new_basis
                ]
                tmp_array_mat = array(new_layer2_basis_list).reshape(-1, 3)
                new_basis_tuples = set([tuple(ele) for ele in tmp_array_mat])
                layer2_new_basis = list(
                    new_basis_tuples - (new_basis_tuples & set(layer2_basis))
                )
                layer2_basis.extend(list(new_basis_tuples))
                layer1_to_2 = False
                layer2_to_1 = True
            elif layer2_to_1 and (not layer1_to_2):
                new_layer1_basis_list = [
                    ele_tuple + array([[0, 0, -1], [-1, 0, -1], [0, -1, -1]])
                    for ele_tuple in layer2_new_basis
                ]
                tmp_array_mat = array(new_layer1_basis_list).reshape(-1, 3)
                new_basis_tuples = set([tuple(ele) for ele in tmp_array_mat])
                layer1_new_basis = list(
                    new_basis_tuples - (new_basis_tuples & set(layer1_basis))
                )
                layer1_basis.extend(list(new_basis_tuples))
                layer1_to_2 = True
                layer2_to_1 = False
        output_basis = list(set(layer1_basis) | set(layer2_basis))
        return output_basis

    def intra_h_pre_k_mat(self):
        h1_diagonal_term = [
            ele_basis[0] * self.b_p_arr + ele_basis[1] * self.b_n_arr - self.k_b_arr
            for ele_basis in self.pre_basis_layer_base
        ]
        h1_mat = h1_diagonal_term
        h2_diagonal_term = [
            ele_basis[0] * self.b_p_arr + ele_basis[1] * self.b_n_arr - self.k_t_arr
            for ele_basis in self.pre_basis_layer_twist
        ]
        h2_mat = h2_diagonal_term
        return array(h1_mat), array(h2_mat)

    def inter_h_pre_mat(self):
        mat_in_list = []
        for layer1_basis in self.pre_basis_layer_base:
            row = []
            for layer2_basis in self.pre_basis_layer_twist:
                if layer2_basis == (layer1_basis[0], layer1_basis[1], 2):
                    row.append(self.t_0())
                elif layer2_basis == (layer1_basis[0] + 1, layer1_basis[1], 2):
                    row.append(self.t_p1())
                elif layer2_basis == (layer1_basis[0], layer1_basis[1] + 1, 2):
                    row.append(self.t_n1())
                else:
                    row.append(zeros((2, 2)))
            mat_in_list.append(row)
        return block(mat_in_list), conj(block(mat_in_list)).T

    def diag_h_construct(self, k_arr):
        h1_plus_k = k_arr + self.intra_h1_k
        h2_plus_k = k_arr + self.intra_h2_k

        intra_h1_mat = [
            PubMeth.sigma_angle_dot_p(ele_arr, self.twist_angle_conti / 2)
            for ele_arr in h1_plus_k
        ]
        intra_h2_mat = [
            PubMeth.sigma_angle_dot_p(ele_arr, -self.twist_angle_conti / 2)
            for ele_arr in h2_plus_k
        ]

        return self.epsilon * block_diag(*intra_h1_mat), self.epsilon * block_diag(
            *intra_h2_mat
        )

    def hamiltonian_construction(self, k_arr):
        intra_h_1, intra_h_2 = self.diag_h_construct(k_arr)
        out_mat = [[intra_h_1, self.inter_h_12], [self.inter_h_21, intra_h_2]]
        return block(out_mat)

    # # k空间路径描述
    def path_depiction(
        self,
        i,
        point1,
        point2,
        out_list,
        multi_process="off",
        include_last_k=False,
        hint=False,
    ):
        k_along = PubMeth.path_between_two_vec(
            point1,
            point2,
            density=int(norm(point1 - point2) * self.density_per_path),
            include_last=include_last_k,
        )
        if multi_process == "on":
            value_list = []
            for kp in k_along:
                eig_v_f = np.linalg.eig(self.hamiltonian_construction(kp))[0]
                eig_v_f.sort()
                value_list.append(eig_v_f)
                if hint:
                    print("Complete: ", kp)
            value_list.append(i)
            out_list.append(value_list)
            print("Complete: ", point1, " to ", point2)

    # # k空间路径坐标构建
    def label_pos(self, path_list):
        pos_list = [0]
        for ii in range(len(path_list) - 1):
            number_of_points = int(
                self.density_per_path
                * sqrt(
                    (path_list[ii + 1][1] - path_list[ii][1]) ** 2
                    + (path_list[ii + 1][0] - path_list[ii][0]) ** 2
                )
            )
            next_pos = pos_list[-1] + number_of_points
            pos_list.append(next_pos)
        return pos_list

    # # 多进程计算k空间路径能带，每条路径一个核计算
    def multi_proc_path(
        self,
        kp_path_list,
        save_fig_or_not=True,
        save_npy_or_not=True,
        y_range=[-1000, 1000],
        line_type="k-",
        x_labs=[],
        show_or_not=False,
        lw=1,
        hold_on=False,
        figsize=(7, 5),
        comm_angle_in_title=None,
        delta_angle_in_title=None,
        shift_energy=True,
        test_mode=False,
        selected_bds_index_list=[],
        hint=False,
        ax_input=False,
        title_font_size=14,
        label_font_size=12,
        tick_font_size=10,
        include_last_k=True,
        save_fig_dir_name="bands",
        save_npy_dir_name="bands_data",
        update=False,
    ):
        conti_title = "conti_band_{:.3f}_{}".format(
            self.twist_angle_conti, self.mat_type
        )
        npy_file = (
            PubMeth.get_right_save_path_and_create(
                save_npy_dir_name, data_files_or_not=True
            )
            + conti_title
            + ".npy"
        )
        x_label_pos = PubMeth.situate_x_labels(kp_path_list, self.density_per_path)

        print("The npy file name is: ", npy_file)

        if os.path.exists(npy_file) and (not update):
            print("Using the existing data...")
            total_energy_list = np.load(npy_file)
        else:
            out_eig_list_f = multiprocessing.Manager().list()
            path_num = len(kp_path_list) - 1
            p_f = Pool(path_num)
            path_depiction = functools.partial(self.path_depiction, hint=hint)
            for i in range(path_num - 1):
                p_f.apply_async(
                    path_depiction,
                    args=(
                        i,
                        kp_path_list[i],
                        kp_path_list[i + 1],
                        out_eig_list_f,
                        "on",
                        False,
                    ),
                )
            ### Include the last k point in the last path
            p_f.apply_async(
                path_depiction,
                args=(
                    path_num - 1,
                    kp_path_list[path_num - 1],
                    kp_path_list[path_num],
                    out_eig_list_f,
                    "on",
                    include_last_k,
                ),
            )
            print("Waiting for all subprocesses done...")
            p_f.close()
            p_f.join()
            print("All subprocesses done.")
            total_energy_list = []
            for path_i in range(path_num):
                for ele_path in out_eig_list_f:
                    if ele_path[-1] == path_i:
                        total_energy_list.extend(ele_path[0:-1])

        if isinstance(shift_energy, bool):
            half_energy = PubMeth.find_half_filling_energy(total_energy_list)
            if shift_energy:
                shifted_energy_list = array(total_energy_list) - half_energy
            else:
                shifted_energy_list = array(total_energy_list)

            if (not comm_angle_in_title) and (comm_angle_in_title != 0):
                figure_title = r"Band structure of ${:.2f}\degree$ {}".format(
                    self.twist_angle_conti, self.mat_type
                )
                save_fig_npy_title = conti_title
                PubMeth.plot_energies(
                    real(shifted_energy_list),
                    y_range=y_range,
                    line_type=line_type,
                    figuretitle=figure_title,
                    x_label_pos=x_label_pos,
                    x_labs=x_labs,
                    save_fig_or_not=save_fig_or_not,
                    show_or_not=show_or_not,
                    save_fig_npy_title=save_fig_npy_title,
                    lw=lw,
                    hold_on=hold_on,
                    fig_size=figsize,
                    test_mode=test_mode,
                    selected_bds_indices=selected_bds_index_list,
                    html_name="conti_energies_{:.4f}_{}".format(
                        self.twist_angle_conti, self.mat_type
                    ),
                    ax_input=ax_input,
                    save_npy_or_not=save_npy_or_not,
                    save_npy_dir_name=save_npy_dir_name,
                    save_fig_dir_name=save_fig_dir_name,
                    title_font_size=title_font_size,
                    tick_font_size=tick_font_size,
                    label_font_size=label_font_size,
                )
            else:
                if not delta_angle_in_title:
                    figure_title = r"Band structure of ${:.2f}\degree$ {}".format(
                        self.twist_angle_conti, self.mat_type
                    )
                    save_fig_npy_title = "conti_band_{:.3f}_{}".format(
                        comm_angle_in_title, self.mat_type
                    )
                    PubMeth.plot_energies(
                        real(shifted_energy_list),
                        y_range=y_range,
                        line_type=line_type,
                        figuretitle=figure_title,
                        x_label_pos=x_label_pos,
                        x_labs=x_labs,
                        save_fig_or_not=save_fig_or_not,
                        show_or_not=show_or_not,
                        save_fig_npy_title=save_fig_npy_title,
                        lw=lw,
                        hold_on=hold_on,
                        fig_size=figsize,
                        test_mode=test_mode,
                        selected_bds_indices=selected_bds_index_list,
                        html_name="conti_energies_{:.4f}_{}".format(
                            self.twist_angle_conti, self.mat_type
                        ),
                        ax_input=ax_input,
                        save_npy_or_not=save_npy_or_not,
                        save_npy_dir_name=save_npy_dir_name,
                        save_fig_dir_name=save_fig_dir_name,
                        title_font_size=title_font_size,
                        tick_font_size=tick_font_size,
                        label_font_size=label_font_size,
                    )
                else:
                    figure_title = r"$\theta_0={:.5f} \degree, \delta \theta = {:e} \degree$".format(
                        comm_angle_in_title, delta_angle_in_title
                    )
                    save_fig_npy_title = "conti_band_{:.3f}_{:e}".format(
                        comm_angle_in_title, delta_angle_in_title
                    )
                    PubMeth.plot_energies(
                        real(shifted_energy_list),
                        y_range=y_range,
                        line_type=line_type,
                        figuretitle=figure_title,
                        x_label_pos=x_label_pos,
                        x_labs=x_labs,
                        save_fig_or_not=save_fig_or_not,
                        show_or_not=show_or_not,
                        save_fig_npy_title=save_fig_npy_title,
                        lw=lw,
                        hold_on=hold_on,
                        fig_size=figsize,
                        test_mode=test_mode,
                        selected_bds_indices=selected_bds_index_list,
                        html_name="conti_energies_{:.4f}_{:.e}".format(
                            comm_angle_in_title, self.twist_angle_conti
                        ),
                        ax_input=ax_input,
                        save_npy_or_not=save_npy_or_not,
                        save_npy_dir_name=save_npy_dir_name,
                        save_fig_dir_name=save_fig_dir_name,
                        title_font_size=title_font_size,
                        tick_font_size=tick_font_size,
                        label_font_size=label_font_size,
                    )

            return shifted_energy_list  # total_energy_list is un-shifted energy list
        else:
            shift_energy = array(total_energy_list) - shift_energy
            if (not comm_angle_in_title) and (comm_angle_in_title != 0):
                figure_title = r"Band structure of ${:.2f}\degree$ {}".format(
                    self.twist_angle_conti, self.mat_type
                )
                save_fig_npy_title = conti_title
                PubMeth.plot_energies(
                    real(shift_energy),
                    y_range=y_range,
                    line_type=line_type,
                    figuretitle=figure_title,
                    x_label_pos=x_label_pos,
                    x_labs=x_labs,
                    save_fig_or_not=save_fig_or_not,
                    show_or_not=show_or_not,
                    save_fig_npy_title=save_fig_npy_title,
                    lw=lw,
                    hold_on=hold_on,
                    fig_size=figsize,
                    test_mode=test_mode,
                    selected_bds_indices=selected_bds_index_list,
                    html_name="conti_energies_{:.4f}_{}".format(
                        self.twist_angle_conti, self.mat_type
                    ),
                    ax_input=ax_input,
                    save_npy_or_not=save_npy_or_not,
                    save_npy_dir_name=save_npy_dir_name,
                    save_fig_dir_name=save_fig_dir_name,
                    title_font_size=title_font_size,
                    tick_font_size=tick_font_size,
                    label_font_size=label_font_size,
                )
            else:
                if not delta_angle_in_title:
                    figure_title = r"Band structure of ${:.2f}\degree$ {}".format(
                        self.twist_angle_conti, self.mat_type
                    )
                    save_fig_npy_title = "conti_band_{:.3f}_{}".format(
                        comm_angle_in_title, self.mat_type
                    )
                    PubMeth.plot_energies(
                        real(shift_energy),
                        y_range=y_range,
                        line_type=line_type,
                        figuretitle=figure_title,
                        x_label_pos=x_label_pos,
                        x_labs=x_labs,
                        save_fig_or_not=save_fig_or_not,
                        show_or_not=show_or_not,
                        save_fig_npy_title=save_fig_npy_title,
                        lw=lw,
                        hold_on=hold_on,
                        fig_size=figsize,
                        test_mode=test_mode,
                        selected_bds_indices=selected_bds_index_list,
                        html_name="conti_energies_{:.4f}".format(
                            self.twist_angle_conti, self.mat_type
                        ),
                        ax_input=ax_input,
                        save_npy_or_not=save_npy_or_not,
                        save_npy_dir_name=save_npy_dir_name,
                        save_fig_dir_name=save_fig_dir_name,
                        title_font_size=title_font_size,
                        tick_font_size=tick_font_size,
                        label_font_size=label_font_size,
                    )
                else:
                    figure_title = r"$\theta_0={:.3f} \degree, \delta \theta = {:e} \degree$".format(
                        comm_angle_in_title, delta_angle_in_title
                    )
                    save_fig_npy_title = "conti_band_{:.3f}_{:e}".format(
                        comm_angle_in_title, delta_angle_in_title
                    )
                    PubMeth.plot_energies(
                        real(shift_energy),
                        y_range=y_range,
                        line_type=line_type,
                        figuretitle=figure_title,
                        x_label_pos=x_label_pos,
                        x_labs=x_labs,
                        save_fig_or_not=save_fig_or_not,
                        show_or_not=show_or_not,
                        save_fig_npy_title=save_fig_npy_title,
                        lw=lw,
                        hold_on=hold_on,
                        fig_size=figsize,
                        test_mode=test_mode,
                        selected_bds_indices=selected_bds_index_list,
                        html_name="energies_{:.4f}_{:e}".format(
                            comm_angle_in_title, self.twist_angle_conti
                        ),
                        ax_input=ax_input,
                        save_npy_or_not=save_npy_or_not,
                        save_npy_dir_name=save_npy_dir_name,
                        save_fig_dir_name=save_fig_dir_name,
                        title_font_size=title_font_size,
                        tick_font_size=tick_font_size,
                        label_font_size=label_font_size,
                    )

            return total_energy_list

    # # 布里渊区k点的定义
    def kp_in_moire_b_zone(
        self, boundary_vec_return=False
    ):  # # kp_num 为菱形边长上k点的数目
        """
        return: k point list
        """
        kp_list_f = []
        for ele_m in arange(0, 1, 1 / self.kp_num):
            for ele_n in arange(0, 1, 1 / self.kp_num):
                k_p = ele_m * self.b_p_arr + ele_n * self.b_n_arr
                kp_list_f.append(k_p)
        if boundary_vec_return:
            len_limit = arange(0, 1, 1 / self.kp_num)[-1]
            return kp_list_f, array(
                [
                    [0, 0],
                    len_limit * self.b_p_arr,
                    len_limit * (self.b_p_arr + self.b_n_arr),
                    len_limit * self.b_n_arr,
                    [0, 0],
                ]
            )
        return kp_list_f

    def rect_moire_b_zone(self):
        kp_list = []
        for ele_x in arange(-sqrt(3) / 2, sqrt(3) / 2, sqrt(3) / self.kp_num):
            for ele_y in arange(-1 / 2, 1, 3 / (2 * self.kp_num)):
                kp_list.append(array([ele_x, ele_y]))
        return kp_list

    # # 将布里渊区的k点分成若干个列表
    def divide_kp_list(self):
        all_kp_list_f = self.kp_in_moire_b_zone()
        kp_part_list_f = []
        for i in range(self.cores_num - 1):
            kp_part_list_f.append(
                all_kp_list_f[
                    int(len(all_kp_list_f) / self.cores_num)
                    * i : int(len(all_kp_list_f) / self.cores_num)
                    * (i + 1)
                ]
            )
        kp_part_list_f.append(
            all_kp_list_f[
                int(len(all_kp_list_f) / self.cores_num) * (self.cores_num - 1) :
            ]
        )
        return kp_part_list_f

    def part_e_dic(self, i, point_list, out_list, multi_process="off"):
        if multi_process == "off":
            all_energy_list = []
            dic = {}
            for k_index, k_point in enumerate(point_list):
                eig_v = np.linalg.eig(self.hamiltonian_construction(k_point))[0]
                eig_v.sort()
                dic[(k_point[0], k_point[1])] = eig_v
                all_energy_list.extend(eig_v)
            return dic, all_energy_list
        elif multi_process == "on":
            print("The # ", i, "process is running")
            all_energy_list = []
            dic = {}
            for k_index, k_point in enumerate(point_list):
                eig_v = np.linalg.eig(self.hamiltonian_construction(k_point))[0]
                eig_v.sort()
                dic[(k_point[0], k_point[1])] = eig_v
                all_energy_list.extend(eig_v)
            out_list.append(all_energy_list)

    def get_fermi_vel(self):
        e_at_k = eig(self.hamiltonian_construction(self.k_b_arr))[0]
        e_at_k.sort()
        e_c1_k = e_at_k[int(len(e_at_k) / 2)]
        e_at_m = eig(self.hamiltonian_construction(self.m_1_arr))[0]
        e_at_m.sort()
        e_c1_m = e_at_m[int(len(e_at_m) / 2)]
        Delta_E = e_c1_m - e_c1_k
        Delta_k = norm(self.m_1_arr - self.k_b_arr) * self.norm_Kg_conti
        return real(Delta_E / (Delta_k * h_bar_eV * m2A * eV2meV))  # m/s

    def multi_proc_all_e(self, kp_part_list_f, save_or_not=False):
        out_eig_list_f = multiprocessing.Manager().list()
        p_f = Pool(self.cores_num)
        for i in range(self.cores_num):
            p_f.apply_async(
                self.part_e_dic, args=(i, kp_part_list_f[i], out_eig_list_f, "on")
            )
        print("Waiting for all subprocesses done...")
        p_f.close()
        p_f.join()
        print("All subprocesses done.")
        total_energy_list = []
        for ele_e_list in out_eig_list_f:
            total_energy_list.extend(ele_e_list)
        if save_or_not:
            target_dir = PubMeth.get_right_save_path_and_create(
                "Dat", data_files_or_not=True
            )
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            np.save(
                target_dir + "conti_tbg_%.2f_all_e.npy" % self.twist_angle_conti,
                total_energy_list,
            )
        return total_energy_list

    def plot_along_path(
        self,
        path=0,
        labels=0,
        yrange=[-2000, 2000],
        line_s="k-",
        lw=1,
        save_fig_or_not=True,
        show=False,
        hold_or_not=False,
        figsize=(7, 5),
        shift_or_not=True,
        test_mode=True,
        selected_bds=[],
        ax_input=False,
        title_font_size=14,
        label_font_size=12,
        tick_font_size=10,
        update=False,
    ):
        if isinstance(path, int):
            self.multi_proc_path(
                self.default_paths[path],
                x_labs=self.default_path_labels[path],
                y_range=yrange,
                line_type=line_s,
                lw=lw,
                save_fig_or_not=save_fig_or_not,
                show_or_not=show,
                hold_on=hold_or_not,
                shift_energy=shift_or_not,
                test_mode=test_mode,
                selected_bds_index_list=selected_bds,
                ax_input=ax_input,
                title_font_size=title_font_size,
                label_font_size=label_font_size,
                tick_font_size=tick_font_size,
                update=update,
            )
        else:
            self.multi_proc_path(
                path,
                save_fig_or_not=save_fig_or_not,
                x_labs=labels,
                y_range=yrange,
                line_type=line_s,
                lw=lw,
                show_or_not=show,
                hold_on=hold_or_not,
                figsize=figsize,
                shift_energy=shift_or_not,
                test_mode=test_mode,
                selected_bds_index_list=selected_bds,
                ax_input=ax_input,
                title_font_size=title_font_size,
                label_font_size=label_font_size,
                tick_font_size=tick_font_size,
            )

    def raman_i_cal(self, k_point_arr, num_half_f, e_photon, hint=False):
        cent_h = self.hamiltonian_construction(k_point_arr)
        partial_hx = (
            self.hamiltonian_construction(
                (k_point_arr[0] + self.interval_k, k_point_arr[1])
            )
            - cent_h
        ) / (
            self.interval_k * self.norm_Kg_conti
        )  # The kx derivative of the Hamiltonian matrix
        partial_hy = (
            self.hamiltonian_construction(
                (k_point_arr[0], k_point_arr[1] + self.interval_k)
            )
            - cent_h
        ) / (
            self.interval_k * self.norm_Kg_conti
        )  # The ky derivative of the Hamiltonian matrix

        eig_v, eig_a = eig(
            cent_h
        )  # get the eigen values and the eigen states of the original Hamiltonian matrix.

        mid_i = (
            len(eig_v) // 2
        )  # get the middle index of total length to find the half-filling condition

        v_energy_list = eig_v[
            argsort(real(eig_v))[mid_i - 1 : mid_i - 1 - num_half_f : -1]
        ]  # valence energy and valence state (top --- bottom)
        v_states_list = eig_a.T[
            argsort(real(eig_v))[mid_i - 1 : mid_i - 1 - num_half_f : -1]
        ]  # valence energy and valence state (top --- bottom)

        c_energy_list = eig_v[
            argsort(real(eig_v))[mid_i : mid_i + num_half_f]
        ]  # conduction energy and conduction state  (bottom --- top)
        c_states_list = eig_a.T[
            argsort(real(eig_v))[mid_i : mid_i + num_half_f]
        ]  # conduction energy and conduction state  (bottom --- top)

        term_h_x = (
            conj(c_states_list) @ partial_hx @ v_states_list.T
        )  # get the expectation values under hx
        term_h_y = (
            conj(c_states_list) @ partial_hy @ v_states_list.T
        )  # get the expectation values under hy
        trans_list = (
            abs(term_h_x) ** 2 + abs(term_h_y) ** 2
        )  # get the total expectations of Hamiltonian derivative
        e_diff_list = array(
            [ele_c_e - v_energy_list for ele_c_e in c_energy_list]
        )  # get the energy difference between all conduction and valence bands

        # # the shape of raman_term_list is (num_half, num_half)
        raman_term_list = array(trans_list) / (
            (e_photon - array(e_diff_list) - 1j * self.raman_gamma)
            * (e_photon - array(e_diff_list) - self.e_phonon - 1j * self.raman_gamma)
        )

        # # save the Raman resonance for transitions
        if hint:
            print("Complete: ", k_point_arr)
        return raman_term_list.reshape(
            (num_half_f**2,)
        )  # return the square of the modulus of the raman intensity term

    def multi_proc_raman_i_cal(
        self,
        args_list: tuple[int, float],
        hint=False,
        pics_2d_save_dir="2d_default/",
        mat_2d_subfolder_name="mat_default/",
        ele_trans_npy_save_dir="npy_default/",
        ele_trans_pic_dir="pics_default/",
        marker_size=5.5,
        uni_real_vmin=False,
        uni_real_vmax=False,
        marker_type="h",
        colorbar=True,
        colorbar_pad=0.01,
        colorbar_width=0.01,
    ):
        """
        Offer of parameter "mod_pics_save_dir" and "mat_save_subfolder_name" are highly suggested
        :param args_list: [num_half, e_photon(meV)]
        :return:
        """
        print("Begin Raman Calculations")  # hint for what calculations

        ##  dir locations
        mat_save_dir_loc = (
            data_file_dir + "Raman/raman_mat_files/" + mat_2d_subfolder_name
        )
        pics_2d_save_dir = data_file_dir + "Raman/raman_2d_pic/" + pics_2d_save_dir
        ele_trans_npy_save_dir = (
            data_file_dir + "Raman/ele_raman_trans_npy/" + ele_trans_npy_save_dir
        )
        ele_trans_pic_dir = (
            data_file_dir + "Raman/ele_raman_transitions/" + ele_trans_pic_dir
        )
        if not os.path.exists(mat_save_dir_loc):
            os.makedirs(mat_save_dir_loc)
        if not os.path.exists(pics_2d_save_dir):
            os.makedirs(pics_2d_save_dir)
        if not os.path.exists(ele_trans_npy_save_dir):
            os.makedirs(ele_trans_npy_save_dir)
        if not os.path.exists(ele_trans_pic_dir):
            os.makedirs(ele_trans_pic_dir)

        parts_list = self.divide_kp_list()
        kps_list = self.kp_in_moire_b_zone()
        x_list = [ele[0] for ele in kps_list]
        y_list = [ele[1] for ele in kps_list]
        raman_i_cal = functools.partial(self.raman_i_cal, hint=hint)
        all_list = PubMeth.multi_proc_func(raman_i_cal, parts_list, args_list)
        uni_real_vmin = array(
            real(all_list)
        ).min()  # get the min and max of all data. This is the real part
        uni_real_vmax = array(
            real(all_list)
        ).max()  # get the min and max of all data. This is the real part
        uni_imag_vmin = array(
            imag(all_list)
        ).min()  # get the min and max of all data. This is the imaginary part
        uni_imag_vmax = array(
            imag(all_list)
        ).max()  # get the min and max of all data. This is the imaginary part
        ##  save the universal min and max of real and imaginary part
        real_imag_min_max_list = [
            uni_real_vmin,
            uni_real_vmax,
            uni_imag_vmin,
            uni_imag_vmax,
        ]
        np.save(mat_save_dir_loc + "uni_min_max.npy", real_imag_min_max_list)

        for ele_col in range(array(all_list).shape[-1]):
            ele_transition = array(all_list)[:, ele_col]
            ##  plot the real part of the k-space distribution
            PubMeth.scatter_2d_plot(
                x_list=x_list,
                y_list=y_list,
                c_mat=real(ele_transition),
                marker_size=marker_size,
                marker_type=marker_type,
                colorbar=colorbar,
                cbar_label="Real part intensity (a.u.)",
                colorbar_pad=colorbar_pad,
                colorbar_width=colorbar_width,
                figuretitle=r"$v_{} \to c_{}$".format(
                    ele_col % args_list[0] + 1, ele_col // args_list[0] + 1
                ),
                figure_name="v{}_c{}_{}_{:.2f}_{}".format(
                    ele_col % args_list[0] + 1,
                    ele_col // args_list[0] + 1,
                    self.model_type,
                    self.twist_angle_conti,
                    self.mat_type,
                ),
                uni_vmin=uni_real_vmin,
                uni_vmax=uni_real_vmax,
                figs_save_dir=ele_trans_pic_dir
                + "{:.2f}".format(self.twist_angle_conti)
                + os.sep
                + "real/",
                title_font_size=25,
                boundary_vecs=self.BZ_boundaries_vecs,
            )
            ##  plot the imag part of the k-space distribution
            PubMeth.scatter_2d_plot(
                x_list=x_list,
                y_list=y_list,
                c_mat=imag(ele_transition),
                marker_size=marker_size,
                marker_type=marker_type,
                colorbar=colorbar,
                cbar_label="Imaginary part intensity (a.u.)",
                colorbar_pad=colorbar_pad,
                colorbar_width=colorbar_width,
                figuretitle=r"$v_{} \to c_{}$".format(
                    ele_col % args_list[0] + 1, ele_col // args_list[0] + 1
                ),
                figure_name="v{}_c{}_{}_{:.2f}_{}".format(
                    ele_col % args_list[0] + 1,
                    ele_col // args_list[0] + 1,
                    self.model_type,
                    self.twist_angle_conti,
                    self.mat_type,
                ),
                uni_vmin=uni_imag_vmin,
                uni_vmax=uni_imag_vmax,
                figs_save_dir=ele_trans_pic_dir
                + "{:.2f}".format(self.twist_angle_conti)
                + os.sep
                + "imag/",
                title_font_size=25,
                boundary_vecs=self.BZ_boundaries_vecs,
            )
            # # The save file will be named in order of the element transitions. Ordered by conduction band indextitle_ and the mid_trans_num parameter
            np.save(
                ele_trans_npy_save_dir
                + "transition_{}_{}_raman_{:.2f}_{}".format(
                    ele_col, self.model_type, self.twist_angle_conti, self.mat_type
                ),
                ele_transition,
            )
        im_mat = np.sum(
            all_list, axis=1
        )  #   after this summation, the contributions from different conduction and valence bands are summed up

        ##  save the mat (un-renormalized by the area of twisted trilayer graphene) in the target folder
        np.save(
            mat_save_dir_loc
            + "{}_raman_{:.2f}_mat_.npy".format(
                self.model_type, self.twist_angle_conti
            ),
            im_mat,
        )
        ##  save the mat (renormalized by the area of twisted trilayer graphene) in the target folder
        np.save(
            mat_save_dir_loc
            + "{}_raman_{:.2f}_mat_renormed_by_area.npy".format(
                self.model_type, self.twist_angle_conti
            ),
            im_mat / self.unit_moire_cell_area_conti,
        )

        # # plot the real part of the k-space distribution
        PubMeth.scatter_2d_plot(
            x_list=x_list,
            y_list=y_list,
            c_mat=real(im_mat),
            marker_size=marker_size,
            marker_type=marker_type,
            colorbar=colorbar,
            cbar_label="Real part intensity (a.u.)",
            colorbar_pad=colorbar_pad,
            colorbar_width=colorbar_width,
            figuretitle=r"$\theta = {:.2f} \degree$".format(self.twist_angle_conti),
            figure_name="{}_raman_real_{:.2f}_{}".format(
                self.model_type, self.twist_angle_conti, self.mat_type
            ),
            uni_vmin=uni_real_vmin,
            uni_vmax=uni_real_vmax,
            figs_save_dir=pics_2d_save_dir,
            title_font_size=24,
            boundary_vecs=self.BZ_boundaries_vecs,
        )

        # # plot the imaginary part of the k-space distribution
        PubMeth.scatter_2d_plot(
            x_list=x_list,
            y_list=y_list,
            c_mat=imag(im_mat),
            marker_size=marker_size,
            marker_type=marker_type,
            colorbar=colorbar,
            cbar_label="Imaginary part intensity (a.u.)",
            colorbar_pad=colorbar_pad,
            colorbar_width=colorbar_width,
            figuretitle=r"$\theta = {:.2f} \degree$".format(self.twist_angle_conti),
            figure_name="{}_raman_imag_{:.2f}_{}".format(
                self.model_type, self.twist_angle_conti, self.mat_type
            ),
            uni_vmin=uni_real_vmin,
            uni_vmax=uni_real_vmax,
            figs_save_dir=pics_2d_save_dir,
            title_font_size=24,
            boundary_vecs=self.BZ_boundaries_vecs,
        )

        return abs(im_mat.sum()) ** 2 / self.unit_moire_cell_area_conti**2

    def ab_cal(self, k_point_arr, num_half_f, e_photon_list):
        cent_h = self.hamiltonian_construction(k_point_arr)
        partial_hx = (
            self.hamiltonian_construction(
                (k_point_arr[0] + self.interval_k, k_point_arr[1])
            )
            - cent_h
        ) / (self.interval_k * self.norm_Kg_conti)
        partial_hy = (
            self.hamiltonian_construction(
                (k_point_arr[0], k_point_arr[1] + self.interval_k)
            )
            - cent_h
        ) / (self.interval_k * self.norm_Kg_conti)

        eig_v, eig_a = eig(cent_h)
        vv_dic = {}
        for i_f in range(len(eig_v)):
            vv_dic[eig_v[i_f]] = eig_a.T[i_f]

        eig_v.sort()
        mid_i = len(eig_v) // 2
        chosen_energy = []
        states_list = []
        for i_b in range(-num_half_f, num_half_f):
            chosen_energy.append(eig_v[mid_i + i_b])
            states_list.append(vv_dic[eig_v[mid_i + i_b]])

        v_energy_list = chosen_energy[:num_half_f]
        c_energy_list = chosen_energy[num_half_f:]

        v_states_list = states_list[:num_half_f]
        c_states_list = states_list[num_half_f:]

        e_diff_list = []

        trans_list = []
        for i1 in range(len(v_states_list)):
            for i2 in range(len(c_states_list)):
                term1 = dot(dot(conj(c_states_list[i2]), partial_hx), v_states_list[i1])
                term2 = dot(dot(conj(c_states_list[i2]), partial_hy), v_states_list[i1])
                e_diff_list.append(c_energy_list[i2] - v_energy_list[i1])
                trans_list.append(abs(term1) ** 2 + abs(term2) ** 2)

        ab_along_e = []
        for ele_photon in e_photon_list:
            tmp_term = (
                array(trans_list)
                * self.ab_delta
                / ((array(e_diff_list) - ele_photon) ** 2 + self.ab_delta**2)
            )
            tmp_sum = tmp_term.sum() / ele_photon
            ab_along_e.append(tmp_sum)
        print("Complete: ", k_point_arr)
        return ab_along_e

    def multi_proc_ab_cal(
        self,
        args_list,
        save_ab_results=True,
        save_ab_for_energy=False,
        suffix="",
        ylim=[],
    ):
        """
        :param args_list: [num_half, e_photon_list]
        :return:
        """
        print("Begin the absorption calculation...")  # hint for calculation type
        dir_name = PubMeth.get_right_save_path_and_create(
            "absorption", data_files_or_not=True
        )
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        parts_list = self.divide_kp_list()
        ab_all_k_along_e = PubMeth.multi_proc_func(self.ab_cal, parts_list, args_list)

        out_ab = zeros(len(args_list[-1]))
        for ele_along in ab_all_k_along_e:
            out_ab = out_ab + array(ele_along) * self.ab_renorm_const

        if save_ab_for_energy:
            # # plot the absorption with respect to the energy of photon
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.plot(args_list[-1], real(out_ab))
            ax.set_xlabel("E(meV)", fontsize=12)
            ax.set_ylabel("Absorption", fontsize=12)
            ax.set_title(
                "The absorption of {:.2f}$\degree$-{}".format(
                    self.twist_angle_conti, self.mat_type
                ),
                fontsize=14,
            )
            ax.set_xlim(ax.get_xlim())
            if len(ylim) != 0:
                ax.set_ylim(ylim)
            else:
                ax.set_ylim([0, 0.1])
            if len(suffix) != 0:
                fig_name = "ab_E_{:.2f}_{}_{}".format(
                    self.twist_angle_conti, self.mat_type, suffix
                )
            else:
                fig_name = "ab_E_{:.2f}_{}".format(
                    self.twist_angle_conti, self.mat_type
                )
            fig.savefig(dir_name + fig_name + ".pdf", dpi=330, facecolor="w")
            fig.savefig(dir_name + fig_name + ".png", dpi=330, facecolor="w")
            plt.close()

            # # html file for absorption with respect to the energy of photon
            trace1 = go.Scatter(x=args_list[-1], y=real(out_ab))
            layout = PubMeth.plotly_layout()
            fig = go.Figure(data=[trace1], layout=layout)
            fig.write_html(dir_name + fig_name + ".html")

        if len(suffix) != 0:
            fig_name = "ab_lambda_{:.2f}_{}_{}".format(
                self.twist_angle_conti, self.mat_type, suffix
            )
        else:
            fig_name = "ab_lambda_{:.2f}_{}_{}".format(
                self.twist_angle_conti, self.mat_type, suffix
            )
        # # plot the absorption with respect to the wavelength of photon
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(1240 * 1000 / array(args_list[-1]), real(out_ab))
        ax.set_xlabel(r"$\lambda$(nm)", fontsize=12)
        ax.set_ylabel("Absorption", fontsize=12)
        ax.set_title(
            "The absorption of {:.2f}$\degree$-{}".format(
                self.twist_angle_conti, self.mat_type
            ),
            fontsize=14,
        )
        ax.set_xlim([400, 1000])
        if len(ylim) != 0:
            ax.set_ylim(ylim)
        else:
            ax.set_ylim([0, 0.1])
        fig.savefig(dir_name + fig_name + ".pdf", dpi=330, facecolor="w")
        fig.savefig(dir_name + fig_name + ".png", dpi=330, facecolor="w")
        plt.close()

        # # html file for absorption with respect to the wavelength of photon
        trace1 = go.Scatter(x=1240 * 1000 / array(args_list[-1]), y=real(out_ab))
        layout = PubMeth.plotly_layout()
        fig = go.Figure(data=[trace1], layout=layout)
        fig.write_html(dir_name + fig_name + ".html")

        # # save the absorption result as npy file
        if save_ab_results:
            ab_npy_dir = PubMeth.get_right_save_path_and_create(
                "absorption_npy", data_files_or_not=True
            )
            if not os.path.exists(ab_npy_dir):
                os.makedirs(ab_npy_dir)
            if len(suffix) != 0:
                np.save(
                    ab_npy_dir
                    + "ab_{:.2f}_{}_{}.npy".format(
                        self.twist_angle_conti, self.mat_type, suffix
                    ),
                    out_ab,
                )  # save the absorption
                np.save(
                    ab_npy_dir + "E_photon.npy", args_list[-1]
                )  # save the photon energy
                np.save(
                    ab_npy_dir + "lambda_photon.npy", 1240 * 1000 / array(args_list[-1])
                )  # save the photon wavelength
            else:
                np.save(
                    ab_npy_dir
                    + "ab_{:.2f}_{}_.npy".format(self.twist_angle_conti, self.mat_type),
                    out_ab,
                )  # save the absorption
                np.save(
                    ab_npy_dir + "E_photon.npy", args_list[-1]
                )  # save the photon energy
                np.save(
                    ab_npy_dir + "lambda_photon.npy", 1240 * 1000 / array(args_list[-1])
                )  # save the photon wavelength

        return out_ab

    def multi_proc_ab_2d(self, args_list, suffix=""):
        """
        :param args_list: [num_half, e_photon_list]
        :return: output absorption list
        """
        kp_list = self.kp_in_moire_b_zone()  # all the k points we do calculations over
        x_list = [ele[0] for ele in kp_list]  # positions of k points in momentum space
        y_list = [ele[1] for ele in kp_list]  # positions of k points in momentum space
        parts_list = self.divide_kp_list()
        ab_all_k_along_e = PubMeth.multi_proc_func(
            self.ab_cal, parts_list, args_list
        )  # calculate the absorption
        ab_all_k_along_e = array(ab_all_k_along_e)
        out_ab = []
        ##  traverse every data under every photon energy to get 2D plot
        for i in range(len(args_list[-1])):
            chosen_e = args_list[-1][i]  # The incident photon energy
            chosen_mat = real(ab_all_k_along_e)[
                :, i
            ]  # get the intensity distribution for every photon energy
            PubMeth.scatter_2d_plot(
                x_list,
                y_list,
                chosen_mat,
                figure_name="{}_{}_{}_{}".format(
                    self.model_type, self.mat_type, self.twist_angle_conti, chosen_e
                ),
                figs_save_dir=data_file_dir + "absorption/2d/",
                figuretitle=r"E=%.2f meV".format(chosen_e),
            )  # plot the distribution in k-space
            out_ab.append(
                ab_all_k_along_e[:, i].sum() * self.ab_renorm_const
            )  # sum all the k contributions for every photon energy

            # ##  Old method of 2D plot
            # chosen_mat = real(ab_all_k_along_e)[:, i].reshape((self.kp_num, self.kp_num))   # the distribution in k-space for incident photon energy
            # PubMeth.rect2diam(chosen_mat, "Conti_e_%.2f" % chosen_e, r"$E=%.2f meV$" % chosen_e, save_2d_plots=figs_save)
            # print("Complete: ", args_list[-1][i], "meV")
            # out_ab.append(ab_all_k_along_e[:, i].sum() * self.ab_renorm_const)

        # # plot the absorption with respect to the energy of photon
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(args_list[-1], real(out_ab))
        ax.set_xlabel("E(meV)", fontsize=12)
        ax.set_ylabel("Absorption", fontsize=12)
        ax.set_title(
            "The absorption of {:.2f}$\degree$-{}".format(
                self.twist_angle_conti, self.mat_type
            ),
            fontsize=14,
        )
        ax.set_xlim(ax.get_xlim())
        ax.set_ylim([0, 0.1])
        if len(suffix) != 0:
            fig_name = "ab_E_{:.2f}_{}_{}".format(
                self.twist_angle_conti, self.mat_type, suffix
            )
        else:
            fig_name = "ab_E_{:.2f}_{}".format(self.twist_angle_conti, self.mat_type)
        fig.savefig(
            data_file_dir + "absorption/E/" + fig_name + ".pdf", dpi=330, facecolor="w"
        )
        fig.savefig(
            data_file_dir + "absorption/E/" + fig_name + ".png", dpi=330, facecolor="w"
        )
        plt.close()

        # # plot the absorption with respect to the wavelength of photon
        if len(suffix) != 0:
            fig_name = "ab_lambda_{:.2f}_{}_{}".format(
                self.twist_angle_conti, self.mat_type, suffix
            )
        else:
            fig_name = "ab_lambda_{:.2f}_{}_{}".format(
                self.twist_angle_conti, self.mat_type, suffix
            )
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(1240 * 1000 / array(args_list[-1]), real(out_ab))
        ax.set_xlabel(r"$\lambda$(nm)", fontsize=12)
        ax.set_ylabel("Absorption", fontsize=12)
        ax.set_title(
            "The absorption of {:.2f}$\degree$-{}".format(
                self.twist_angle_conti, self.mat_type
            ),
            fontsize=14,
        )
        ax.set_xlim([400, 1000])
        ax.set_ylim([0, 0.1])
        fig.savefig(
            data_file_dir + "absorption/lambda/" + fig_name + ".pdf",
            dpi=330,
            facecolor="w",
        )
        fig.savefig(
            data_file_dir + "absorption/lambda/" + fig_name + ".png",
            dpi=330,
            facecolor="w",
        )
        plt.close()

        # # save the absorption result as npy file
        if len(suffix) != 0:
            np.save(
                data_file_dir
                + "absorption/npy/"
                + "ab_{:.2f}_{}_{}.npy".format(
                    self.twist_angle_conti, self.mat_type, suffix
                ),
                out_ab,
            )  # save the absorption
            np.save(
                data_file_dir
                + "absorption/npy/"
                + "all_mat_{:.2f}_{}_{}.npy".format(
                    self.twist_angle_conti, self.mat_type, suffix
                ),
                ab_all_k_along_e,
            )  # save all mats
            np.save(
                data_file_dir + "absorption/npy/" + "E_photon.npy", args_list[-1]
            )  # save the photon energy
            np.save(
                data_file_dir + "absorption/npy/" + "lambda_photon.npy",
                1240 * 1000 / array(args_list[-1]),
            )  # save the photon wavelength
        else:
            np.save(
                data_file_dir
                + "absorption/npy/"
                + "ab_{:.2f}_{}_.npy".format(self.twist_angle_conti, self.mat_type),
                out_ab,
            )  # save the absorption
            np.save(
                data_file_dir
                + "absorption/npy/"
                + "all_mat_{:.2f}_{}_.npy".format(
                    self.twist_angle_conti, self.mat_type
                ),
                ab_all_k_along_e,
            )  # save all mats
            np.save(
                data_file_dir + "absorption/npy/" + "E_photon.npy", args_list[-1]
            )  # save the photon energy
            np.save(
                data_file_dir + "absorption/npy/" + "lambda_photon.npy",
                1240 * 1000 / array(args_list[-1]),
            )  # save the photon wavelength

        return out_ab

    def berry_cur_niumeth(self, kp_arr, band_i):
        if band_i > 0:
            chosen_band_i = len(self.pre_basis_list) + band_i - 1
        else:
            chosen_band_i = len(self.pre_basis_list) + band_i

        cent_h = self.hamiltonian_construction(kp_arr)
        e_v, e_a = eig(cent_h)
        vector_n = e_a.T[np.argsort(real(e_v))[chosen_band_i]]
        e_n = e_v[np.argsort(real(e_v))[chosen_band_i]]

        other_n_pri = list(e_a.T)
        other_e = list(e_v)
        other_n_pri.pop(np.argsort(real(e_v))[chosen_band_i])
        other_e.pop(np.argsort(real(e_v))[chosen_band_i])

        par_h_kx = (
            self.hamiltonian_construction(
                array([kp_arr[0] + self.interval_k, kp_arr[1]])
            )
            - cent_h
        ) / (self.interval_k * self.norm_Kg_conti)
        par_h_ky = (
            self.hamiltonian_construction(
                array([kp_arr[0], kp_arr[1] + self.interval_k])
            )
            - cent_h
        ) / (self.interval_k * self.norm_Kg_conti)

        t1 = time.time()
        out_result = 0
        for ele_i in range(len(other_e)):
            tmp_e = other_e[ele_i]
            tmp_n_pri = other_n_pri[ele_i]

            mat_n_n_pri = tmp_n_pri.reshape(-1, 1) @ conj(tmp_n_pri.reshape(1, -1))
            cent_mat_xy = par_h_kx @ mat_n_n_pri @ par_h_ky
            cent_mat_yx = par_h_ky @ mat_n_n_pri @ par_h_kx
            term_xy = conj(vector_n.reshape(1, -1)) @ cent_mat_xy @ vector_n
            term_yx = conj(vector_n.reshape(1, -1)) @ cent_mat_yx @ vector_n
            out_result = out_result + (term_xy - term_yx) / (real(e_n - tmp_e)) ** 2

        print(time.time() - t1)
        print("Complete: ", kp_arr)
        return out_result * 1j

    def multi_proc_chern_num_niumeth(self, kp_density, args_list):
        """
        :param kp_density: num of points along a side of MBZ
        :param args_list: [band_i]
        :return:
        """
        # all_kps = self.moire_b_zone(kp_density)
        all_kps = self.rect_moire_b_zone(kp_density)
        print("N_k: ", len(all_kps))
        all_parts = PubMeth.divide_list(all_kps)
        berry_cur_list = PubMeth.multi_proc_func(
            self.berry_cur_niumeth, all_parts, args_list
        )
        return (
            sum(berry_cur_list)
            / (len(all_kps) * self.unit_moire_cell_area_conti)
            * 2
            * pi
        )

    def multi_proc_berry_2d_niumeth(self, kp_density, args_list):
        """
        :param kp_density: num points along a side of MBZ
        :param args_list: [band_i]
        :return:
        """
        xy_list = []
        for ele_y in linspace(1, -1, kp_density):
            for ele_x in linspace(-sqrt(3) / 2, sqrt(3) / 2, kp_density):
                xy_list.append(array([ele_x, ele_y]))

        print("N_k: ", len(xy_list))
        all_parts = PubMeth.divide_list(xy_list)
        berry_list = PubMeth.multi_proc_func(
            self.berry_cur_niumeth, all_parts, args_list
        )
        im_mat = array(berry_list).reshape((kp_density, kp_density))
        return real(im_mat)

    def berry_cur_jmeth(self, k_arr, band_i, kp_num):
        delta_space = 1 / kp_num

        delta_kx = self.b_p_arr[0] * delta_space * 2
        delta_ky = self.b_p_arr[1] * delta_space

        if band_i > 0:
            chosen_band_i = len(self.pre_basis_list) + band_i - 1
        else:
            chosen_band_i = len(self.pre_basis_list) + band_i

        cent_h = self.hamiltonian_construction(k_arr)
        e_v, e_a = eig(cent_h)
        cent_vec = e_a[:, np.argsort(real(e_v))[chosen_band_i]]

        delta_kx_h = self.hamiltonian_construction(k_arr + array([delta_kx, 0]))
        e_v, e_a = eig(delta_kx_h)
        delta_kx_vec = e_a[:, np.argsort(real(e_v))[chosen_band_i]]

        delta_ky_h = self.hamiltonian_construction(array(k_arr + array([0, delta_ky])))
        e_v, e_a = eig(delta_ky_h)
        delta_ky_vec = e_a[:, np.argsort(real(e_v))[chosen_band_i]]

        delta_kx_ky_h = self.hamiltonian_construction(
            k_arr + array([delta_kx, delta_ky])
        )
        e_v, e_a = eig(delta_kx_ky_h)
        delta_kx_ky_vec = e_a[:, np.argsort(real(e_v))[chosen_band_i]]

        Ux = dot(conj(cent_vec), delta_kx_vec) / abs(dot(conj(cent_vec), delta_kx_vec))
        Uy = dot(conj(cent_vec), delta_ky_vec) / abs(dot(conj(cent_vec), delta_ky_vec))
        Ux_y = dot(conj(delta_ky_vec), delta_kx_ky_vec) / abs(
            dot(conj(delta_ky_vec), delta_kx_ky_vec)
        )
        Uy_x = dot(conj(delta_kx_vec), delta_kx_ky_vec) / abs(
            dot(conj(delta_kx_vec), delta_kx_ky_vec)
        )

        F_12 = cmath.log(Ux * Uy_x * (1 / Ux_y) * (1 / Uy))
        # print("Complete: ", k_arr)
        return F_12

    def multi_proc_chern_num_jmeth(
        self, args_list, save_2d_plot=True, mat_2d_save=True
    ):
        """
        :param args_list: [band_i, kp_num]
        :return:
        """
        all_kps = self.kp_in_moire_b_zone(args_list[-1])
        all_parts = PubMeth.divide_list(all_kps)
        berry_cur_list = PubMeth.multi_proc_func(
            self.berry_cur_jmeth, all_parts, args_list
        )
        chern_num = 1j * sum(berry_cur_list) / (2 * pi)
        if save_2d_plot:
            PubMeth.rect2diam(
                -array(imag(berry_cur_list)).reshape((args_list[-1], args_list[-1])),
                file_name="berry_2D_{}_chern_num_{:.2f}".format(
                    self.mat_type, real(chern_num)
                ),
                title_name="Chern Number={:.2f}, N={:.0f}".format(
                    real(chern_num), len(all_kps)
                ),
                save_2d_plots=save_2d_plot,
                save_in_case_same_name=True,
                rm_raw=True,
                save_mat=mat_2d_save,
            )
        print("Chern number: ", chern_num)
        return chern_num

    def energy_at_k(self, k_arr_in, band_index_list=[], hint=False):
        """
        :param args_list: [k_arr_in, [band_index_start, band_index_stop]]
        :return: real list
        """
        eigen_values = np.linalg.eig(self.hamiltonian_construction(k_arr_in))[0]
        eigen_values.sort()
        if len(band_index_list) != 0:
            energy_out = eigen_values[
                len(eigen_values) // 2
                + band_index_list[0] : len(eigen_values) // 2
                + band_index_list[1]
            ]
        else:
            energy_out = eigen_values[:]
        energy_out = array(energy_out)
        if hint:
            print("Complete: ", k_arr_in)
        return real(energy_out)

    def multi_proc_energy_over_BZ(self, args_list, hint=False):
        """
        :param args_list: [k_arr_list, [band_index_start, band_index_stop]]
        :return: list
        """
        parts_list = PubMeth.divide_list(args_list[0])
        print("# of total k: ", len(args_list[0]))
        energy_at_k = functools.partial(self.energy_at_k, hint=hint)
        eigen_enegies = PubMeth.multi_proc_func(
            energy_at_k, parts_list, [args_list[-1]]
        )
        energy_dat_name = (
            data_file_dir
            + "energy_data/"
            + "{}_energy_set_{:.4f}_{}_density_{}.npy".format(
                self.model_type, self.twist_angle_conti, self.mat_type, self.kp_num
            )
        )
        np.save(energy_dat_name, array(eigen_enegies))
        return array(eigen_enegies)

    def multi_proc_dos_cal(
        self,
        energy_range: list,
        save_fig_or_not=True,
        save_fig_dir_name="dos",
        save_dat_dir_name="energy_data",
        bins_num="auto",
        hint=False,
        bands_count=(-10, 10),
    ):
        save_fig_dir = PubMeth.get_right_save_path_and_create(
            save_fig_dir_name, data_files_or_not=True
        )
        save_fig_name = save_fig_dir + "{}_dos_{:.4f}_{}.png".format(
            self.model_type, self.twist_angle_conti, self.mat_type
        )
        save_dat_dir = PubMeth.get_right_save_path_and_create(
            save_dat_dir_name, data_files_or_not=True
        )
        save_dat_name = save_dat_dir + "{}_energy_set_{:.4f}_{}_density_{}.npy".format(
            self.model_type, self.twist_angle_conti, self.mat_type, self.kp_num
        )
        if save_fig_or_not:
            if not os.path.exists(save_fig_dir):
                os.makedirs(save_fig_dir)
            if not os.path.exists(save_dat_dir):
                os.makedirs(save_dat_dir)

        if not os.path.exists(save_dat_name):
            energies_set = self.multi_proc_energy_over_BZ(
                [self.kps_in_BZ, bands_count], hint=hint
            )
        elif os.path.exists(save_dat_name):
            print("Using the existing data...")
            energies_set = np.load(save_dat_name)
        energies_set = array(energies_set).reshape(
            -1,
        )
        if len(energy_range) != 0:
            energy_filter = (energies_set > energy_range[0]) & (
                energies_set < energy_range[1]
            )
            energies_set = energies_set[energy_filter]
        n, bins, patches = plt.hist(
            x=energies_set, bins=bins_num, color="grey", alpha=0.7, rwidth=0.85
        )
        print("# of bins: ", len(n))
        ax = plt.gca()
        ax.set_xlabel("E(meV)", fontsize=12)
        ax.set_ylabel("DOS", fontsize=12)
        ax.set_title("DOS of {}".format(self.mat_type), fontsize=14)
        x_pos = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
        plt.plot(x_pos, n)
        plt.savefig(save_fig_name, dpi=330, facecolor="w")
        plt.close()

    def multi_proc_jdos_cal_all_BZ(
        self,
        energy_range: list,
        save_fig_or_not=True,
        save_fig_dir_name="jdos",
        save_energy_dat_dir_name="energy_data",
        bins_num="auto",
        hint=False,
        save_jdos_npy_dir_name="jdos_npy",
        save_npy_or_not=True,
        bands_count=(-10, 10),
        energy_cut=0,
        energy_broaden=1,
    ):
        print("Begin JDOS calculation...")  # hint for calculation
        save_fig_dir = PubMeth.get_right_save_path_and_create(
            save_fig_dir_name, data_files_or_not=True
        )
        save_fig_name = save_fig_dir + "total/{}_jdos_{:.4f}_{}.png".format(
            self.model_type, self.twist_angle_conti, self.mat_type
        )
        save_dat_dir = PubMeth.get_right_save_path_and_create(
            save_energy_dat_dir_name, data_files_or_not=True
        )
        energy_dat_name = (
            save_dat_dir
            + "{}_energy_set_{:.4f}_{}_density_{}.npy".format(
                self.model_type, self.twist_angle_conti, self.mat_type, self.kp_num
            )
        )
        save_npy_dir = PubMeth.get_right_save_path_and_create(
            save_jdos_npy_dir_name, data_files_or_not=True
        )
        save_jdos_npy_name = (
            save_npy_dir
            + "total/{}_jdos_{:.4f}_{}_density_{}.npy".format(
                self.model_type, self.twist_angle_conti, self.mat_type, self.kp_num
            )
        )
        if save_fig_or_not:
            if not os.path.exists(save_fig_dir):
                os.makedirs(save_fig_dir)
            if not os.path.exists(save_dat_dir):
                os.makedirs(save_dat_dir)

        if not os.path.exists(energy_dat_name):
            energies_set = self.multi_proc_energy_over_BZ(
                [self.kps_in_BZ, bands_count], hint=hint
            )
        elif os.path.exists(energy_dat_name):
            print("Using the existing data...")
            energies_set = np.load(energy_dat_name)

        mid_band_i = (energies_set.shape[1]) // 2
        c_energy_set = energies_set[:, mid_band_i : mid_band_i + bands_count[1]].T
        v_energy_set = energies_set[
            :, mid_band_i - 1 : mid_band_i - 1 + bands_count[0] : -1
        ].T
        e_diff_set = array([c_energy_set - ele_e for ele_e in v_energy_set])
        e_diff_set = e_diff_set.reshape((-1, len(self.kps_in_BZ)))

        for ele_pair_i in range(len(e_diff_set)):
            c_i = ele_pair_i // len(c_energy_set) + 1
            v_i = ele_pair_i % len(v_energy_set) + 1
            e_diff = e_diff_set[ele_pair_i]

            sub_folder = save_fig_dir + "energy_diff/{:.2f}/".format(
                self.twist_angle_conti
            )
            save_fig2d_name = "{}_jdos_v{}_c{}_{}".format(
                self.model_type, v_i, c_i, self.mat_type
            )
            if not os.path.exists(sub_folder):
                os.makedirs(sub_folder)
            x_arr = array(self.kps_in_BZ)[:, 0]
            y_arr = array(self.kps_in_BZ)[:, 1]

            ##  Sift the energy = energy_cut

            uni_vmin = min(e_diff)
            uni_vmax = max(e_diff)
            fig_2d, ax_2d, png_name, pdf_name = PubMeth.scatter_2d_plot(
                x_list=x_arr,
                y_list=y_arr,
                c_mat=e_diff,
                marker_size=7.5,
                marker_type="h",
                colorbar=True,
                cbar_label=r"$\Delta E$ (meV)",
                colorbar_pad=0.05,
                colorbar_width=0.01,
                figuretitle=r"$v_{} \to c_{}$".format(v_i, c_i),
                figure_name=save_fig2d_name,
                uni_vmin=uni_vmin,
                uni_vmax=uni_vmax,
                figs_save_dir=sub_folder,
                title_font_size=25,
                boundary_vecs=self.BZ_boundaries_vecs,
                ax_return=True,
            )
            ax_2d.tricontour(
                x_arr,
                y_arr,
                e_diff,
                levels=[
                    energy_cut - energy_broaden,
                    energy_cut,
                    # energy_cut + energy_broaden,
                ],
                colors=["r", "k", "r"],
            )
            fig_2d.savefig(png_name, bbox_inches="tight", pad_inches=0.1, dpi=330)
            fig_2d.savefig(pdf_name, bbox_inches="tight", pad_inches=0.1, dpi=330)
            plt.close(fig_2d)

        e_diff_set = array(e_diff_set).reshape(
            -1,
        )

        if len(energy_range) != 0:
            energy_filter = (e_diff_set > energy_range[0]) & (
                e_diff_set < energy_range[1]
            )
            e_diff_set = e_diff_set[energy_filter]

        jdos_y, bins, patches = plt.hist(
            x=e_diff_set,
            bins=bins_num,
            color="grey",
            alpha=0.7,
            rwidth=0.85,
            range=energy_range,
        )
        delta_energy = bins[1] - bins[0]
        jdos_renorm_const = self.jdos_renorm_with_area / delta_energy
        jdos_y = jdos_y * jdos_renorm_const
        print(
            "# of bins: ", len(jdos_y), " The delta energy is: ", delta_energy
        )  # hint for basic information of the calculation

        # # plot the jdos figure
        energy_x = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
        print(
            "Energy range is: ", energy_x[0], "---", energy_x[-1]
        )  # hint for the energy range we plot
        fig, ax = plt.subplots()
        ax.plot(energy_x, jdos_y)
        ax.set_xlabel("E(meV)", fontsize=12)
        ax.set_ylabel("JDOS", fontsize=12)
        ax.set_yticks([])
        ax.set_title(
            "JDOS of {:.3f}$\degree$-{}".format(self.twist_angle_conti, self.mat_type),
            fontsize=14,
        )
        energy_x = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
        fig.savefig(save_fig_name, dpi=330, facecolor="w")
        plt.close()

        # # save the jdos as npy file
        if save_npy_or_not:
            if not os.path.exists(save_npy_dir):
                os.makedirs(save_npy_dir)
            np.save(save_jdos_npy_name, jdos_y)
        return energy_x, jdos_y

    def multi_proc_energy_diff_2d_cal(
        self,
        selected_band_index_list,
        save_fig_or_not=True,
        save_fig_dir_name="e_diff",
        save_dat_dir_name="energy_data",
        bins_num="auto",
        energy_range=[],
    ):
        save_fig_name = "{}_e_diff_{}_{}_{}_to_{}.png".format(
            self.model_type,
            self.twist_angle_conti,
            self.mat_type,
            selected_band_index_list[0],
            selected_band_index_list[1],
        )
        save_dat_dir = PubMeth.get_right_save_path_and_create(
            save_dat_dir_name, data_files_or_not=True
        )
        save_dat_name = save_dat_dir + "{}_energy_set_{:.4f}_{}_density_{}.npy".format(
            self.model_type, self.twist_angle_conti, self.mat_type, self.kp_num
        )
        if not os.path.exists(save_dat_dir):
            os.makedirs(save_dat_dir)

        if not os.path.exists(save_dat_name):
            k_arrs_list = self.kp_in_moire_b_zone()
            energies_set = self.multi_proc_energy_over_BZ([k_arrs_list, [-10, 10]])
            np.save(save_dat_name, energies_set)

            x_list = [ele[0] for ele in k_arrs_list]
            y_list = [ele[1] for ele in k_arrs_list]

            chosen_valence_i = selected_band_index_list[
                0
            ]  # # must be negative, top most valence band is -1
            chosen_cond_i = selected_band_index_list[
                1
            ]  # # must be positive, bottom most conduction band is 1

            chosen_band_low = energies_set[
                :, (energies_set.shape[1]) // 2 + chosen_valence_i
            ]
            chosen_band_high = energies_set[
                :, (energies_set.shape[1]) // 2 + chosen_cond_i - 1
            ]

            energy_diff_mat = chosen_band_high - chosen_band_low

            PubMeth.scatter_2d_plot(
                x_list,
                y_list,
                energy_diff_mat.reshape((len(x_list),)),
                figuretitle=r"$\theta={:.2f}\degree$".format(self.twist_angle_conti),
                figs_save_dir=save_fig_dir_name,
                figure_name=save_fig_name,
            )

        elif os.path.exists(save_dat_name):
            print("Using the existing data...")
            x_list = [ele[0] for ele in self.kp_in_moire_b_zone()]
            y_list = [ele[1] for ele in self.kp_in_moire_b_zone()]
            energies_set = np.load(save_dat_name)

            chosen_valence_i = selected_band_index_list[
                0
            ]  # # must be negative, top most valence band is -1
            chosen_cond_i = selected_band_index_list[
                1
            ]  # # must be positive, bottom most conduction band is 1

            chosen_band_low = energies_set[
                :, (energies_set.shape[1]) // 2 + chosen_valence_i
            ]
            chosen_band_high = energies_set[
                :, (energies_set.shape[1]) // 2 + chosen_cond_i - 1
            ]

            energy_diff_mat = chosen_band_high - chosen_band_low

            PubMeth.scatter_2d_plot(
                x_list,
                y_list,
                energy_diff_mat.reshape((len(x_list),)),
                figuretitle=r"$\theta={:.2f}\degree$".format(self.twist_angle_conti),
                figs_save_dir=save_fig_dir_name,
                figure_name=save_fig_name,
                marker_size=6,
                colorbar=True,
                colorbar_pad=0.1,
            )


class TightTbgInst:  # # 紧束缚模型核心代码
    if "SLURM_CPUS_PER_TASK" in os.environ:
        cores_num = int(os.environ["SLURM_CPUS_PER_TASK"])
    else:
        cores_num = multiprocessing.cpu_count()
    print("Cores Num: ", cores_num)
    interval_k = 0.00001

    expand_vecs = [
        array([1, 0]),
        array([0, 1]),
        array([-1, 0]),
        array([0, -1]),
        array([1, -1]),
        array([-1, 1]),
    ]

    def __init__(
        self,
        m0,
        r,
        t_intra=-2700,
        t_inter=480,
        ab_delta=20,
        kp_num=70,
        dyn_cond_eta=20,
        raman_gamma=100,
        e_phonon=196,
        a0=1.42 * sqrt(3),
        d0=3.35,
        density_per_path=100,
        atoms_within_unit_cell=4,
    ):  # eV for two couplings
        self.mat_type = "TBG"
        self.model_type = "tb"

        self.twist_angle_cos = (3 * m0**2 + 3 * m0 * r + r**2 / 2) / (
            3 * m0**2 + 3 * m0 * r + r**2
        )
        self.twist_angle_sin = sqrt(1 - self.twist_angle_cos**2)
        self.twist_angle = np.arccos(self.twist_angle_cos) / pi * 180
        self.twist_theta = np.arccos(self.twist_angle_cos)
        self.e_phonon = e_phonon

        self.a0_const = a0
        self.atoms_within_unit_cell = atoms_within_unit_cell
        # # rotate the basis to form a symmetric unit cell
        # self.a1 = PubMeth.rotation(-self.theta / 2) @ (self.a0 * array([sqrt(3) / 2, -1 / 2]))
        # self.a2 = PubMeth.rotation(-self.theta / 2) @ (self.a0 * array([sqrt(3) / 2, 1 / 2]))
        # self.b1 = PubMeth.rotation(-self.theta / 2) @ (2 * pi / a0 * array([1 / sqrt(3), -1]))
        # self.b2 = PubMeth.rotation(-self.theta / 2) @ (2 * pi / a0 * array([1 / sqrt(3), 1]))
        self.a1 = self.a0_const * array([sqrt(3) / 2, -1 / 2])
        self.a2 = self.a0_const * array([sqrt(3) / 2, 1 / 2])
        self.b1 = 2 * pi / a0 * array([1 / sqrt(3), -1])
        self.b2 = 2 * pi / a0 * array([1 / sqrt(3), 1])
        self.delta = (self.a1 + self.a2) / 3
        self.r_a1 = self.a1 * (
            self.twist_angle_cos - self.twist_angle_sin / sqrt(3)
        ) + self.a2 * 2 * self.twist_angle_sin / sqrt(3)
        self.r_a2 = self.a2 * (
            self.twist_angle_cos + self.twist_angle_sin / sqrt(3)
        ) - self.a1 * 2 * self.twist_angle_sin / sqrt(3)
        self.r_delta = (self.r_a1 + self.r_a2) / 3

        self.d0 = d0
        self.delta_0_par = 0.184 * self.a0_const
        self.m0 = m0
        self.r = r
        self.kp_num = kp_num
        self.Nk = int(kp_num**2)

        self.t_intra = t_intra
        self.t_inter = t_inter

        if self.r % 3 != 0:
            self.R_1 = self.m0 * self.a1 + (self.m0 + self.r) * self.a2
            self.R_2 = -(self.m0 + self.r) * self.a1 + (2 * self.m0 + self.r) * self.a2
            self.G_1 = (
                (2 * self.m0 + self.r) * self.b1 + (self.m0 + self.r) * self.b2
            ) / (3 * self.m0**2 + 3 * self.m0 * self.r + self.r**2)
            self.G_2 = (-(self.m0 + self.r) * self.b1 + self.m0 * self.b2) / (
                3 * self.m0**2 + 3 * self.m0 * self.r + self.r**2
            )
            self.n_atoms = int(
                self.atoms_within_unit_cell * (3 * m0**2 + 3 * m0 * r + r**2)
            )
        else:
            n = self.r // 3
            self.R_1 = (self.m0 + n) * self.a1 + n * self.a2
            self.R_2 = -n * self.a1 + (self.m0 + 2 * n) * self.a2
            self.G_1 = ((self.m0 + 2 * n) * self.b1 + n * self.b2) / (
                self.m0**2 + self.m0 * self.r + self.r**2 / 3
            )
            self.G_2 = (-n * self.b1 + (self.m0 + n) * self.b2) / (
                self.m0**2 + self.m0 * self.r + self.r**2 / 3
            )
            self.n_atoms = int(
                self.atoms_within_unit_cell * (m0**2 + m0 * r + r**2 / 3)
            )

        self.n_unit_cells = int((m0**2 + m0 * r + r**2 / 3))

        self.K_1 = (self.G_1 + 2 * self.G_2) / 3
        self.K_2 = (2 * self.G_1 + self.G_2) / 3
        self.M = (self.K_1 + self.K_2) / 2

        self.a_M_comm = norm(self.R_1)
        self.unit_moire_comm = sqrt(3) / 2 * self.a_M_comm**2

        self.a_M_conti = self.a0_const / (2 * sin(self.twist_theta / 2))
        self.unit_moire_conti = sqrt(3) / 2 * self.a_M_conti**2

        self.ab_renorm_const = (
            c_eV**2 / h_bar_eV / c_speed / epsilon_0_eV / self.unit_moire_comm / self.Nk
        )
        self.dyn_conda_renorm_const = (
            1 / self.Nk / self.unit_moire_comm * c_eV**2 / h_bar_eV / sigma_xx_mono * 2
        )
        self.density_per_path = density_per_path / np.linalg.norm(self.K_1)
        self.ab_delta = ab_delta
        self.dyn_cond_eta = dyn_cond_eta
        self.raman_gamma = raman_gamma
        self.sup_vec_list = [
            array([0, 0]),
            self.R_1,
            self.R_2,
            -self.R_1,
            -self.R_2,
            self.R_2 - self.R_1,
            self.R_1 - self.R_2,
            self.R_1 + self.R_2,
            -self.R_1 - self.R_2,
            2 * self.R_2 - self.R_1,
            self.R_1 - 2 * self.R_2,
            2 * self.R_1 - self.R_2,
            self.R_2 - 2 * self.R_1,
        ]

        self.sup_vec_3d_list = [array([*ele_arr, 0]) for ele_arr in self.sup_vec_list]

        self.Kg = norm(self.K_1)
        self.path_gamma = array([0, 0])

        # self.indices_of_lattice = self.lattice_indices()
        # self.positions_of_atoms_test = self.atom_positions()
        # self.value_cos_mat, self.dists_arr_mat = self.atom_relations()

        # # self.positions_of_atoms = self.atom_positions_origin()
        # # self.relations_of_atoms = self.atom_relations_origin()

        # self.V_pppi = self.couple_V_pppi()
        # self.V_ppsigma = self.couple_V_ppsigma()

        # self.K_energy_wavefunc_pair = np.linalg.eig(
        #     self.hamiltonian_construction(self.K_1)
        # )
        # self.K_energy = self.K_energy_wavefunc_pair[0]
        # self.K_energy.sort()
        # self.ref_energy = (
        #     self.K_energy[len(self.K_energy) // 2]
        #     + self.K_energy[len(self.K_energy) // 2 - 1]
        # ) / 2

        # self.default_paths = [
        #     [self.K_1, self.path_gamma, self.M, self.K_2],
        #     [self.path_gamma, self.G_2, 2 * self.K_1, self.K_1, self.path_gamma],
        #     [self.K_2, self.K_1, self.G_2, self.path_gamma, self.K_2],
        # ]
        # self.default_path_labels = [
        #     [r"K$_1$", r"$\Gamma$", r"$M$", r"K$_2$"],
        #     [r"$\Gamma$", r"$G_2$", r"K$_2$", r"K$_1$", r"$\Gamma$"],
        #     [r"K$_2$", r"K$_1$", r"$\Gamma$", r"$\Gamma$", r"K$_2$"],
        # ]

    def lattice_indices(self):
        def create_index(loop_times):
            initial = [(0, 0)]
            new_vecs = []
            i_flag = 0
            while i_flag < loop_times:
                i_flag = i_flag + 1
                if len(new_vecs) == 0:
                    for e_vec in self.expand_vecs:
                        new_vecs.append((e_vec[0], e_vec[1]))
                    initial.extend(new_vecs)
                else:
                    tmp_new_vecs = []
                    for old_vec in new_vecs:
                        for e_vec in self.expand_vecs:
                            tmp_vec = old_vec + e_vec
                            tmp_new_vecs.append((tmp_vec[0], tmp_vec[1]))
                    tmp_new_vecs = list(set(tmp_new_vecs))
                    out_vecs = []
                    for vec_f in tmp_new_vecs:
                        if vec_f not in initial:
                            out_vecs.append(vec_f)
                    new_vecs = out_vecs[:]
                    initial.extend(out_vecs)
            return initial

        i = 1
        loop_index_list = create_index(i)
        while (self.m0, self.m0 + self.r) not in loop_index_list:
            i = i + 1
            loop_index_list = create_index(i)
        return loop_index_list

    def arrange_bound_p(self):
        R_3 = self.R_2 - self.R_1
        return [
            (0, 0),
            (R_3[0], R_3[1]),
            (self.R_2[0], self.R_2[1]),
            (self.R_1[0], self.R_1[1]),
            (0, 0),
        ]

    def atom_positions(self):
        atoms_tuple = []
        bound_list_f = self.arrange_bound_p()
        for ele_index in self.indices_of_lattice:
            A1 = ele_index[0] * self.a1 + ele_index[1] * self.a2
            B1 = ele_index[0] * self.a1 + ele_index[1] * self.a2 + self.delta
            A2 = ele_index[0] * self.r_a1 + ele_index[1] * self.r_a2
            B2 = ele_index[0] * self.r_a1 + ele_index[1] * self.r_a2 + self.r_delta
            if PubMeth.isInterArea(A1, bound_list_f) and not PubMeth.at_corners(
                A1, bound_list_f
            ):
                atoms_tuple.append((*A1, 0))
            if PubMeth.isInterArea(B1, bound_list_f) and not PubMeth.at_corners(
                B1, bound_list_f
            ):
                atoms_tuple.append((*B1, 0))
            if PubMeth.isInterArea(A2, bound_list_f) and not PubMeth.at_corners(
                A2, bound_list_f
            ):
                atoms_tuple.append((*A2, self.d0))
            if PubMeth.isInterArea(B2, bound_list_f) and not PubMeth.at_corners(
                B2, bound_list_f
            ):
                atoms_tuple.append((*B2, self.d0))
        atoms_tuple.append((0, 0, 0))
        atoms_tuple.append((0, 0, self.d0))
        return atoms_tuple

    def atom_relations(self):
        relations_arr_list = []
        value_cos_list = []
        for bra_p in self.positions_of_atoms_test:
            for ket_p in self.positions_of_atoms_test:
                dist_arr = array(ket_p) - array(bra_p)
                minimum_vec = PubMeth.get_smallest_distance(
                    dist_arr, self.sup_vec_3d_list
                )
                tmp_value_cos = minimum_vec[-1] / norm(minimum_vec)
                value_cos_list.append(tmp_value_cos)
                relations_arr_list.append(minimum_vec)
        out_value_cos_mat = array(value_cos_list).reshape((self.n_atoms, self.n_atoms))
        rows, cols = np.diag_indices_from(out_value_cos_mat)
        out_value_cos_mat[rows, cols] = 0
        return out_value_cos_mat, array(relations_arr_list)

    def couple_V_pppi(self):
        V_pppi_mat = (
            self.t_intra
            * exp(
                -(norm(self.dists_arr_mat, axis=1) - self.a0_const / sqrt(3))
                / self.delta_0_par
            )
        ).reshape((self.n_atoms, self.n_atoms))
        V_pppi_mat = V_pppi_mat - diag(diag(V_pppi_mat))
        return V_pppi_mat

    def couple_V_ppsigma(self):
        V_ppsigma_mat = (
            self.t_inter
            * exp(-(norm(self.dists_arr_mat, axis=1) - self.d0) / self.delta_0_par)
        ).reshape((self.n_atoms, self.n_atoms))
        V_ppsigma_mat = V_ppsigma_mat - diag(diag(V_ppsigma_mat))
        return V_ppsigma_mat

    def hamiltonian_construction(self, k_arr_f):
        t1 = time.perf_counter()
        k_dot_dist_arr_list = (k_arr_f * self.dists_arr_mat[:, :2]).sum(axis=1)
        phase_term = exp(-1j * k_dot_dist_arr_list).reshape(
            (self.n_atoms, self.n_atoms)
        )
        h_mat = (
            self.V_pppi * (1 - self.value_cos_mat**2)
            + self.V_ppsigma * self.value_cos_mat**2
        ) * phase_term
        return h_mat

    def plot_atoms(
        self, save_or_not=True, fig_format=global_fig_format, super_cell_view=True
    ):
        layer1_atoms = []
        layer2_atoms = []
        for ele_index in self.indices_of_lattice:
            layer1_atoms.append(ele_index[0] * self.a1 + ele_index[1] * self.a2)
            layer1_atoms.append(
                ele_index[0] * self.a1 + ele_index[1] * self.a2 + self.delta
            )
            layer2_atoms.append(ele_index[0] * self.r_a1 + ele_index[1] * self.r_a2)
            layer2_atoms.append(
                ele_index[0] * self.r_a1 + ele_index[1] * self.r_a2 + self.r_delta
            )

        cor_x1 = array(layer1_atoms)[:, 0]
        cor_y1 = array(layer1_atoms)[:, 1]
        cor_x2 = array(layer2_atoms)[:, 0]
        cor_y2 = array(layer2_atoms)[:, 1]
        bound = self.arrange_bound_p()

        plt.scatter(cor_x1, cor_y1, marker=".")
        plt.scatter(cor_x2, cor_y2, marker=".")
        plt.plot(array(bound)[:, 0], array(bound)[:, 1], color="red")

        ax = plt.gca()
        ax.set_aspect("equal")
        plt.title(
            r"Atomic Structure of Twisted Bilayer Graphene. $\theta=%.3f \degree$"
            % self.twist_angle,
            fontsize=14,
        )
        plt.xlabel("X($\AA$)", fontsize=12)
        plt.ylabel("Y($\AA$)", fontsize=12)
        if save_or_not:
            save_dir = PubMeth.get_right_save_path_and_create(
                "structures", data_files_or_not=True
            )
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            plt.savefig(
                save_dir
                + "Atomic_structure_%.2f_%s.pdf" % (self.twist_angle, self.mat_type),
                dpi=330,
            )
            plt.savefig(
                save_dir
                + "Atomic_structure_%.2f_%s.png" % (self.twist_angle, self.mat_type),
                dpi=330,
            )
        if super_cell_view:
            ax = plt.gca()
            ax.set_xlabel("", fontsize=12)
            ax.set_ylabel("", fontsize=12)
            ax.set_title("", fontsize=14)
            plt.xlim([min([ele[0] for ele in bound]), max([ele[0] for ele in bound])])
            plt.ylim([min([ele[1] for ele in bound]), max([ele[1] for ele in bound])])
            plt.savefig(
                save_dir
                + "supercell_view_{:.3f}_{}".format(self.twist_angle, self.mat_type)
                + fig_format,
                dpi=330,
                facecolor="w",
            )
        plt.close()

        trace1 = go.Scatter(x=cor_x1, y=cor_y1, mode="markers")
        trace2 = go.Scatter(x=cor_x2, y=cor_y2, mode="markers")
        layout = PubMeth.plotly_layout()
        fig = go.Figure(data=[trace1, trace2], layout=layout)
        fig.update_yaxes(
            scaleanchor="x",
            scaleratio=1,
        )
        fig.write_html(
            save_dir
            + "atomic_structure_{:.3f}_{}.html".format(self.twist_angle, self.mat_type)
        )

    def plot_MBZ(self, save_or_not=True, fig_format=global_fig_format):
        vex_list = [
            self.K_1,
            self.K_2,
            self.K_2 - self.K_1,
            -self.K_1,
            -self.K_2,
            self.K_1 - self.K_2,
            self.K_1,
        ]
        PubMeth.draw_box(vex_list)
        ax = plt.gca()
        ax.set_aspect("equal")
        ax.text(self.K_1[0], self.K_1[1], "K1")
        ax.text(self.K_2[0], self.K_2[1], "K2")
        ax.arrow(0, 0, self.G_1[0], self.G_1[1], width=0.015)
        ax.text(self.G_1[0], self.G_1[1], "G1")
        ax.arrow(0, 0, self.G_2[0], self.G_2[1], width=0.015)
        ax.text(self.G_2[0], self.G_2[1], "G2")
        ax.set_xlabel(r"$k_{x}$ ($\acute{A}$)")
        ax.set_ylabel(r"$k_{y}$ ($\acute{A}$)")
        ax.set_title(r"BZ of %.2f$\degree$ %s" % (self.twist_angle, self.mat_type))
        if save_or_not:
            save_dir = PubMeth.get_right_save_path_and_create(
                "structures", data_files_or_not=True
            )
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            plt.savefig(
                save_dir
                + "BZ_%.2f_%s" % (self.twist_angle, self.mat_type)
                + fig_format,
                dpi=330,
            )
        plt.close()

    def kp_in_moire_b_zone(self):
        v_2 = self.G_2
        v_1 = self.G_1 + self.G_2
        kp_list_f = []
        for ele_m in arange(0, 1, 1 / self.kp_num):
            for ele_n in arange(0, 1, 1 / self.kp_num):
                k_p = ele_m * v_1 + ele_n * v_2
                kp_list_f.append(k_p)
        return kp_list_f

    def divide_kp_list(self):
        all_kp_list_f = self.kp_in_moire_b_zone()
        kp_part_list_f = PubMeth.divide_list(all_kp_list_f)
        return kp_part_list_f

    def velocity_me(self, half_b_num, kp_arr_f, delta_k):
        cent_h = self.hamiltonian_construction(kp_arr_f)
        partial_hx = (
            self.hamiltonian_construction(kp_arr_f + array([delta_k, 0])) - cent_h
        ) / delta_k
        partial_hy = (
            self.hamiltonian_construction(kp_arr_f + array([0, delta_k])) - cent_h
        ) / delta_k
        eig_v, eig_a = eig(cent_h)
        vv_dic = {}
        for i_e in range(len(eig_v)):
            vv_dic[eig_v[i_e]] = eig_a.T[i_e]
        eig_v.sort()
        mid_i = int(len(eig_v) / 2)
        states_list = []
        for i_e in arange(-half_b_num, half_b_num):
            states_list.append(vv_dic[eig_v[mid_i + i_e]])
        all_trans_list = []
        half_of_states = int(len(states_list) / 2)
        for bra_i in range(0, half_of_states):
            bra_state = states_list[bra_i]
            for ket_i in range(half_of_states, len(states_list)):
                ket_state = states_list[ket_i]
                term1 = dot(dot(conj(ket_state), partial_hx), bra_state)
                term2 = dot(dot(conj(ket_state), partial_hy), bra_state)
                # all_trans_list.append(abs(dot(dot(conj(ket_state), partial_hx + partial_hy), bra_state)))
                # print(dot(dot(conj(ket_state), partial_hx + partial_hy), bra_state))
                all_trans_list.append(abs(term1**2 + term2**2))
        return all_trans_list

    def path_depiction(self, i, point1, point2, out_list, multi_process="off"):
        k_along = []
        if point2[0] != point1[0]:
            k_slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
            number_of_points = int(
                self.density_per_path
                * sqrt((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2)
            )
            for xx in linspace(point1[0], point2[0], number_of_points):
                k_along.append(array([xx, k_slope * (xx - point2[0]) + point2[1]]))
        elif point2[0] == point1[0]:
            number_of_points = int(
                self.density_per_path * sqrt((point2[1] - point1[1]) ** 2)
            )
            for yy in linspace(point1[1], point2[1], number_of_points):
                k_along.append(array([point2[0], yy]))
        if multi_process == "on":
            value_list = []
            for index, kp in enumerate(k_along):
                eig_v_f, eig_a_f = np.linalg.eig(self.hamiltonian_construction(kp))
                eig_v_f.sort()
                value_list.append(eig_v_f)
                print("Complete: ", index)
            value_list.append(i)
            out_list.append(value_list)
            print("Complete: ", point1, " to ", point2)

    def multi_proc_path(
        self,
        kp_path_list,
        x_labs=[],
        save_fig_or_not=True,
        y_range=[-1000, 1000],
        line_type="k-",
        show_or_not=False,
        lw=1,
        hold_on=False,
        figsize=(7, 5),
        shift_energy=True,
        test_mode=True,
        selected_bds_index_list=[],
        fig_format=global_fig_format,
        energy_lines=[],
        save_bands_dir_name="bands",
        save_npy_or_not=False,
        save_npy_title="",
        save_npy_dir_name="bands_data",
    ):
        out_eig_list_f = multiprocessing.Manager().list()
        path_num = len(kp_path_list) - 1
        p_f = Pool(path_num)
        for i in range(path_num):
            p_f.apply_async(
                self.path_depiction,
                args=(i, kp_path_list[i], kp_path_list[i + 1], out_eig_list_f, "on"),
            )
        x_label_pos = PubMeth.situate_x_labels(kp_path_list, self.density_per_path)
        print("Waiting for all subprocesses done...")
        p_f.close()
        p_f.join()
        print("All subprocesses done.")
        total_energy_list = []
        for path_i in range(path_num):
            for ele_path in out_eig_list_f:
                if ele_path[-1] == path_i:
                    total_energy_list.extend(ele_path[0:-1])

        if isinstance(shift_energy, bool):
            half_energy = PubMeth.find_half_filling_energy(total_energy_list)

            if shift_energy:
                shifted_energy_list = array(total_energy_list) - half_energy

                figure_title = r"Band structure for $\theta={:.3f} \degree$-{}".format(
                    self.twist_angle, self.mat_type
                )
                if save_npy_title == "":
                    save_npy_title = "tb_band_{:.3f}_{}".format(
                        self.twist_angle, self.mat_type
                    )
                else:
                    pass
                PubMeth.plot_energies(
                    real(shifted_energy_list),
                    y_range=y_range,
                    line_type=line_type,
                    figuretitle=figure_title,
                    x_label_pos=x_label_pos,
                    x_labs=x_labs,
                    save_fig_or_not=save_fig_or_not,
                    show_or_not=show_or_not,
                    save_fig_npy_title=save_npy_title,
                    lw=lw,
                    hold_on=hold_on,
                    fig_size=figsize,
                    test_mode=test_mode,
                    selected_bds_indices=selected_bds_index_list,
                    html_name="tb_energies_{:.4f}_{}".format(
                        self.twist_angle, self.mat_type
                    ),
                    fig_format=fig_format,
                    energy_line=energy_lines,
                    save_fig_dir_name=save_bands_dir_name,
                    save_npy_or_not=save_npy_or_not,
                    save_npy_dir_name=save_npy_dir_name,
                )
            else:
                shifted_energy_list = array(total_energy_list)

                figure_title = r"Band structure for $\theta={:.3f} \degree$-{}".format(
                    self.twist_angle, self.mat_type
                )
                if save_npy_title == "":
                    save_npy_title = "tb_band_{:.3f}_{}".format(
                        self.twist_angle, self.mat_type
                    )
                else:
                    pass
                PubMeth.plot_energies(
                    real(shifted_energy_list),
                    y_range=y_range,
                    line_type=line_type,
                    figuretitle=figure_title,
                    x_label_pos=x_label_pos,
                    x_labs=x_labs,
                    save_fig_or_not=save_fig_or_not,
                    show_or_not=show_or_not,
                    save_fig_npy_title=save_npy_title,
                    lw=lw,
                    hold_on=hold_on,
                    fig_size=figsize,
                    test_mode=test_mode,
                    selected_bds_indices=selected_bds_index_list,
                    html_name="tb_energies_{:.4f}_{}".format(
                        self.twist_angle, self.mat_type
                    ),
                    fig_format=fig_format,
                    energy_line=energy_lines,
                    save_fig_dir_name=save_bands_dir_name,
                    save_npy_or_not=save_npy_or_not,
                    save_npy_dir_name=save_npy_dir_name,
                )
            return shifted_energy_list  # total_energy_list is un-shifted energy list
        else:
            shift_energy = array(total_energy_list) - shift_energy
            figure_title = r"Band structure for $\theta={:.3f} \degree$-{}".format(
                self.twist_angle, self.mat_type
            )
            if save_npy_title == "":
                save_npy_title = "tb_band_{:.3f}_{}".format(
                    self.twist_angle, self.mat_type
                )
            else:
                pass
            PubMeth.plot_energies(
                real(shift_energy),
                y_range=y_range,
                line_type=line_type,
                figuretitle=figure_title,
                x_label_pos=x_label_pos,
                x_labs=x_labs,
                save_fig_or_not=save_fig_or_not,
                show_or_not=show_or_not,
                save_fig_npy_title=save_npy_title,
                lw=lw,
                hold_on=hold_on,
                fig_size=figsize,
                test_mode=test_mode,
                selected_bds_indices=selected_bds_index_list,
                html_name="tb_energies_{:.4f}_{}".format(
                    self.twist_angle, self.mat_type
                ),
                fig_format=fig_format,
                energy_line=energy_lines,
                save_fig_dir_name=save_bands_dir_name,
                save_npy_or_not=save_npy_or_not,
                save_npy_dir_name=save_npy_dir_name,
            )
            return total_energy_list

    def plot_along_path(
        self,
        path=0,
        labels=0,
        yrange=[-2000, 2000],
        line_s="k-",
        lw=1,
        save_fig_or_not=True,
        show=False,
        hold_or_not=False,
        figsize=(7, 5),
        shift_energy=True,
        test_or_not=True,
        selected_bds_list=[],
        fig_format=global_fig_format,
        energy_lines=[],
        save_bands_dir_name="bands",
        save_npy_or_not=True,
        save_npy_title="",
        save_npy_dir_name="bands_data",
    ):
        if isinstance(path, int):
            # label_positions = ContiTbgInst.label_pos(
            #     self, ContiTbgInst.default_paths[path])
            # print("The density: ", label_positions)
            return self.multi_proc_path(
                self.default_paths[path],
                x_labs=self.default_path_labels[path],
                y_range=yrange,
                line_type=line_s,
                lw=lw,
                save_fig_or_not=save_fig_or_not,
                show_or_not=show,
                hold_on=hold_or_not,
                shift_energy=shift_energy,
                test_mode=test_or_not,
                selected_bds_index_list=selected_bds_list,
                fig_format=fig_format,
                figsize=figsize,
                energy_lines=energy_lines,
                save_bands_dir_name=save_bands_dir_name,
                save_npy_or_not=save_npy_or_not,
                save_npy_title=save_npy_title,
                save_npy_dir_name=save_npy_dir_name,
            )
        else:
            # label_positions = ContiTbgInst.label_pos(self, path)
            # print("The density: ", label_positions)
            return self.multi_proc_path(
                path,
                save_fig_or_not=save_fig_or_not,
                x_labs=labels,
                y_range=yrange,
                line_type=line_s,
                lw=lw,
                show_or_not=show,
                hold_on=hold_or_not,
                figsize=figsize,
                shift_energy=shift_energy,
                test_mode=test_or_not,
                selected_bds_index_list=selected_bds_list,
                fig_format=fig_format,
                energy_lines=energy_lines,
                save_bands_dir_name=save_bands_dir_name,
                save_npy_or_not=save_npy_or_not,
                save_npy_title=save_npy_title,
                save_npy_dir_name=save_npy_dir_name,
            )

    def label_pos(self, path_list):
        pos_list = [0]
        for ii in range(len(path_list) - 1):
            number_of_points = int(
                self.density_per_path
                * sqrt(
                    (path_list[ii + 1][1] - path_list[ii][1]) ** 2
                    + (path_list[ii + 1][0] - path_list[ii][0]) ** 2
                )
            )
            next_pos = pos_list[-1] + number_of_points
            pos_list.append(next_pos)

        return pos_list

    def ab_cal(self, kp_arr_f, num_half_f, e_photon_list):
        cent_h = self.hamiltonian_construction(kp_arr_f)
        partial_hx = (
            self.hamiltonian_construction(kp_arr_f + array([self.interval_k, 0]))
            - cent_h
        ) / self.interval_k
        partial_hy = (
            self.hamiltonian_construction(kp_arr_f + array([0, self.interval_k]))
            - cent_h
        ) / self.interval_k

        eig_v, eig_a = eig(cent_h)
        vv_dic = {}
        for i_f in range(len(eig_v)):
            vv_dic[eig_v[i_f]] = eig_a.T[i_f]

        # six energies
        eig_v.sort()
        mid_i = len(eig_v) // 2
        chosen_energy = []  # v3, v2, v1, c1, c2, c3
        states_list = []  # v3, v2, v1, c1, c2, c3
        for i_b in range(-num_half_f, num_half_f):
            chosen_energy.append(eig_v[mid_i + i_b])
            states_list.append(vv_dic[eig_v[mid_i + i_b]])

        v_energy_list = chosen_energy[:num_half_f]
        c_energy_list = chosen_energy[num_half_f:]

        v_states_list = states_list[:num_half_f]
        c_states_list = states_list[num_half_f:]

        e_diff_list = []

        trans_list = []
        for i1 in range(len(v_states_list)):
            for i2 in range(len(c_states_list)):
                term1 = dot(dot(conj(c_states_list[i2]), partial_hx), v_states_list[i1])
                term2 = dot(dot(conj(c_states_list[i2]), partial_hy), v_states_list[i1])
                e_diff_list.append(c_energy_list[i2] - v_energy_list[i1])
                trans_list.append(abs(term1) ** 2 + abs(term2) ** 2)

        ab_along_e = []
        for ele_photon in e_photon_list:
            tmp_term = (
                array(trans_list)
                * self.ab_delta
                / ((array(e_diff_list) - ele_photon) ** 2 + self.ab_delta**2)
            )
            tmp_sum = tmp_term.sum() / ele_photon
            ab_along_e.append(tmp_sum)
        return ab_along_e

    def multi_proc_ab_cal(self, args_list):
        """
        :param args_list: [num_half_f, e_photon_list]
        :return: list of absorption
        """
        parts_list = self.divide_kp_list()
        ab_all_k_along_e = PubMeth.multi_proc_func(self.ab_cal, parts_list, args_list)

        out_ab = zeros(len(args_list[-1]))
        for ele_along in ab_all_k_along_e:
            out_ab = out_ab + array(ele_along) * self.ab_renorm_const
        return out_ab

    def multi_proc_ab_2d(self, args_list, figs_save=True):
        """
        :param args_list: [num_half_f, e_photon_list]
        :return: list of absorption
        """
        parts_list = self.divide_kp_list()
        ab_all_k_along_e = PubMeth.multi_proc_func(self.ab_cal, parts_list, args_list)
        ab_all_k_along_e = array(ab_all_k_along_e)
        out_ab = []
        for i in range(len(args_list[-1])):
            chosen_e = args_list[-1][i]
            chosen_mat = real(ab_all_k_along_e)[:, i].reshape(
                (self.kp_num, self.kp_num)
            )
            PubMeth.rect2diam(
                chosen_mat,
                "TB_e_%.2f" % chosen_e,
                r"$E=%.2f meV$" % chosen_e,
                save_2d_plots=figs_save,
            )
            print("Complete: ", args_list[-1][i], "meV")
            out_ab.append(ab_all_k_along_e[:, i].sum() * self.ab_renorm_const)

        return out_ab

    def dyn_cond_cal(
        self,
        i_core,
        num_half_f,
        point_list,
        out_list,
        E_photon_list,
        multi_process="off",
    ):
        i_count = 0
        if multi_process == "on":
            print("The # ", i_core, "process is running")
            mat_trans = []
            mat_e_diff = []
            for k_index, kp_arr_f in enumerate(point_list):
                # t1 = time()
                cent_h = self.hamiltonian_construction(kp_arr_f)
                partial_hx = (
                    self.hamiltonian_construction(
                        kp_arr_f + array([self.interval_k, 0])
                    )
                    - cent_h
                ) / self.interval_k
                eig_v, eig_a = eig(cent_h)
                vv_dic = {}
                for i in range(len(eig_v)):
                    vv_dic[eig_v[i]] = eig_a.T[i]

                # six energies
                eig_v.sort()
                mid_i = int(len(eig_v) / 2)
                chosen_energy = []  # v3, v2, v1, c1, c2, c3
                states_list = []  # v3, v2, v1, c1, c2, c3
                for i_b in range(-num_half_f, num_half_f):
                    chosen_energy.append(eig_v[mid_i + i_b])
                    states_list.append(vv_dic[eig_v[mid_i + i_b]])

                v_energy_list = chosen_energy[:num_half_f]
                c_energy_list = chosen_energy[num_half_f:]

                v_states_list = states_list[:num_half_f]
                c_states_list = states_list[num_half_f:]

                e_diff_list = []

                trans_list = []  # v3 -- c123, v2 -- c123, v1 -- c123
                for i1 in range(len(v_states_list)):
                    for i2 in range(len(c_states_list)):
                        term1 = dot(
                            dot(conj(c_states_list[i2]), partial_hx), v_states_list[i1]
                        )
                        e_diff_list.append(c_energy_list[i2] - v_energy_list[i1])
                        trans_list.append(abs(term1) ** 2)

                mat_trans.append(trans_list)
                mat_e_diff.append(e_diff_list)
                i_count = i_count + 1
                if i_count % 100 == 0:
                    print("Core %s: " % i_core, "Complete: ", i_count)
                elif len(point_list) - i_count < 100 and i_count % 10 == 0:
                    print("Core %s: " % i_core, "Complete: ", i_count)

            out_dyn_cond = []
            for ele_photon_e in E_photon_list:
                tmp_term = array(mat_trans) / (
                    array(mat_e_diff)
                    * (array(mat_e_diff) - ele_photon_e + 1j * self.dyn_cond_eta)
                )
                tmp_sum = tmp_term.sum()
                out_dyn_cond.append(tmp_sum)

            out_list.append(array(out_dyn_cond))

    def multi_proc_dyn_cond_cal(
        self, kp_part_list_f, num_half_f, E_photon_list, dict_save="off"
    ):
        t1 = time.time()
        print("Dimension of matrix: ", len(self.relations_of_atoms))
        out_dyn_list_f = multiprocessing.Manager().list()
        p_f = Pool(self.cores_num)
        for i in range(self.cores_num):
            p_f.apply_async(
                self.dyn_cond_cal,
                args=(
                    i,
                    num_half_f,
                    kp_part_list_f[i],
                    out_dyn_list_f,
                    E_photon_list,
                    "on",
                ),
            )
        print("Waiting for all subprocesses done...")
        p_f.close()
        p_f.join()
        print("All subprocesses done.")
        print("Time consumed: ", time.time() - t1)
        out_result = zeros(len(E_photon_list))
        for ele_arr in out_dyn_list_f:
            out_result = out_result + ele_arr
        if dict_save == "on":
            target_dir = PubMeth.get_right_save_path_and_create(
                "tb_tbg_dyn_cond", data_files_or_not=True
            )
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            save(
                target_dir
                + "m0_%s_r_%s_half_%s_nk_%s.npy"
                % (self.m0, self.r, num_half_f, self.Nk),
                out_result,
            )
        return -imag(array(out_result))

    def raman_i_cal(
        self, k_point_arr, num_half_f, e_photon, hint=False, mid_trans_num=0
    ):
        t1 = time.perf_counter()
        cent_h = self.hamiltonian_construction(k_point_arr)
        partial_hx = (
            self.hamiltonian_construction(
                (k_point_arr[0] + self.interval_k, k_point_arr[1])
            )
            - cent_h
        ) / self.interval_k
        partial_hy = (
            self.hamiltonian_construction(
                (k_point_arr[0], k_point_arr[1] + self.interval_k)
            )
            - cent_h
        ) / self.interval_k

        eig_v, eig_a = eig(cent_h)

        mid_i = len(eig_v) // 2

        v_energy_list = eig_v[argsort(real(eig_v))[mid_i - num_half_f : mid_i]]
        v_states_list = eig_a.T[argsort(real(eig_v))[mid_i - num_half_f : mid_i]]

        c_energy_list = eig_v[argsort(real(eig_v))[mid_i : mid_i + num_half_f]]
        c_states_list = eig_a.T[argsort(real(eig_v))[mid_i : mid_i + num_half_f]]

        term_h_x = conj(c_states_list) @ partial_hx @ v_states_list.T
        term_h_y = conj(c_states_list) @ partial_hy @ v_states_list.T
        trans_list = abs(term_h_x) ** 2 + abs(term_h_y) ** 2
        e_diff_list = array([ele_c_e - v_energy_list for ele_c_e in c_energy_list])

        raman_term_list = array(trans_list) / (
            (e_photon - array(e_diff_list) - 1j * self.raman_gamma)
            * (e_photon - self.e_phonon - array(e_diff_list) - 1j * self.raman_gamma)
        )
        # # save the Raman resonance for transitions
        if mid_trans_num != 0 and mid_trans_num <= num_half_f:
            mid_trans_indices = []
            for ele_loop in range(mid_trans_num):
                mid_trans_indices = mid_trans_indices + [
                    ele_index + num_half_f * ele_loop
                    for ele_index in arange(mid_trans_num)
                ]
            return raman_term_list[mid_trans_indices]
        elif mid_trans_num > num_half_f:
            print("Please enter the right middle transition number!")
            print("Doing the overal Raman sum over...")

        raman_i = raman_term_list.sum()
        if hint:
            print("Complete: ", k_point_arr)
        t2 = time.perf_counter()
        print("Modified function time: ", t2 - t1)
        return raman_i

    def multi_proc_raman_i_cal(
        self,
        args_list,
        figs_save=True,
        hint=False,
        mid_trans_num=0,
        marker_size=1,
        uni_vmin=False,
        uni_vmax=False,
        marker_type="h",
        colorbar=False,
        colorbar_pad=0.01,
        colorbar_width=0.01,
    ):
        """
        :param args_list: [num_half, e_photon]
        # return
        """
        kps_list = self.kp_in_moire_b_zone()
        x_list = [ele[0] for ele in kps_list]
        y_list = [ele[1] for ele in kps_list]
        parts_list = self.divide_kp_list()
        raman_cal = functools.partial(self.raman_i_cal, hint=hint)
        all_list = PubMeth.multi_proc_func(raman_cal, parts_list, args_list)
        im_mat = array(all_list).reshape((self.kp_num, self.kp_num))
        if (not isinstance(uni_vmin, bool)) and (not isinstance(uni_vmax, bool)):
            vmin = uni_vmin
            vmax = uni_vmax
        else:
            vmin = im_mat.min()
            vmax = im_mat.max()
        if figs_save:
            fig, ax_2d = plt.subplots(figsize=(7, 7))
            im_var = ax_2d.scatter(
                x_list,
                y_list,
                c=real(im_mat).reshape((len(x_list),)),
                s=marker_size,
                vmin=vmin,
                vmax=vmax,
                marker=marker_type,
            )
            ax_2d.set_aspect("equal")
            ax_2d.axis("off")
            ax_2d.set_title(r"$\theta = {:.2f} \degree$".format(self.twist_angle))
            if colorbar:
                c_ax = PubMeth.add_right_cax(ax_2d, colorbar_pad, colorbar_width)
                cbar = fig.colorbar(im_var, cax=c_ax)
            fig.savefig(
                data_file_dir
                + "TB_raman_real_{:.3f}_{}".format(self.twist_angle, self.mat_type)
                + ".png"
            )
            fig.savefig(
                data_file_dir
                + "TB_raman_real_{:.3f}_{}".format(self.twist_angle, self.mat_type)
                + ".pdf"
            )
            # PubMeth.rect2diam(real(im_mat), "TB_raman_{:.3f}_{}".format(self.twist_angle, self.mat_type), r"$\theta = %.2f \degree$" % self.twist_angle, save_2d_plots=figs_save)

        return abs(im_mat.sum()) ** 2 / self.unit_moire_comm**2

    def get_fermi_vel(self, proportion_K_to_M=1):
        e_at_k = eig(self.hamiltonian_construction(self.K_1))[0]
        e_at_k.sort()
        e_cv_k = e_at_k[int(len(e_at_k) / 2) - 2 : int(len(e_at_k) / 2) + 2]

        delta_vec_K_to_M = (self.M - self.K_1) * proportion_K_to_M
        target_k_point = self.K_1 + delta_vec_K_to_M

        e_at_m = eig(self.hamiltonian_construction(target_k_point))[0]
        e_at_m.sort()
        e_cv_m = e_at_m[int(len(e_at_m) / 2) - 2 : int(len(e_at_m) / 2) + 2]
        Delta_E = array(e_cv_m - e_cv_k)
        print("∆E: ", Delta_E)
        Delta_k = norm(self.K_1 - target_k_point) * ones(len(Delta_E))
        return abs(Delta_E / (Delta_k * h_bar_eV * m2A * eV2meV))  # m/s

    def energy_at_k(self, k_arr_in, band_index_list):
        """
        :param args_list: [k_arr_in, [band_index_start, band_index_stop]]
        :return: real list
        """
        eigen_values = np.linalg.eig(self.hamiltonian_construction(k_arr_in))[0]
        eigen_values.sort()
        energy_out = eigen_values[
            len(eigen_values) // 2
            + band_index_list[0] : len(eigen_values) // 2
            + band_index_list[1]
        ]
        energy_out = array(energy_out) - self.ref_energy
        print("Complete: ", k_arr_in)
        return real(energy_out)

    def multi_proc_energy_at_k(self, args_list):
        """
        :param args_list: [k_arr_list, [band_index_start, band_index_stop]]
        :return: list
        """
        parts_list = PubMeth.divide_list(args_list[0])
        print("# of total k: ", len(args_list[0]))
        eigen_enegies = PubMeth.multi_proc_func(
            self.energy_at_k, parts_list, [args_list[-1]]
        )
        return eigen_enegies

    def contour_of_band_around_point(
        self, center_vec, delta_vec, band_range_width, density=70
    ):
        dots_arr_list = PubMeth.dots_around_one_point(
            center_vec, delta_vec, density=density
        )
        energies_list = self.multi_proc_energy_at_k(
            [dots_arr_list, [-band_range_width, band_range_width]]
        )
        save_path_figs = PubMeth.get_right_save_path_and_create(
            "contour_band_plots", data_files_or_not=True
        )
        save_path_data = PubMeth.get_right_save_path_and_create(
            "contour_band_data", data_files_or_not=True
        )

        for draw_i in range(0, 2 * band_range_width):
            trace1 = go.Contour(
                z=array(real(energies_list))[:, draw_i].reshape(
                    (density + 1, density + 1)
                ),
                contours_coloring="lines",
                line_width=1,
                contours={
                    "showlabels": True,
                    "labelfont": {"size": 12, "color": "green"},
                },
            )
            layout = PubMeth.plotly_layout(
                figuretitle="Contour of Bands for Band {}. Angle = {:.2f}".format(
                    draw_i, self.twist_angle
                )
            )
            fig = go.Figure(data=[trace1], layout=layout)
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=1,
            )
            filename = "contour_{:.2f}_band_{}".format(self.twist_angle, draw_i)
            fig.update_traces(ncontours=45, selector=dict(type="contour"))
            if not os.path.exists(save_path_figs):
                os.makedirs(save_path_figs)
            if not os.path.exists(save_path_data):
                os.makedirs(save_path_data)
            np.save(
                save_path_data + filename + ".npy",
                array(real(energies_list))[:, draw_i].reshape(
                    (density + 1, density + 1)
                ),
            )
            fig.write_html(save_path_figs + filename + ".html")

    def get_fermi_vel_from_K(self, k_arr_in, band_index, valley_index="K1"):
        eigen_values = np.linalg.eig(self.hamiltonian_construction(k_arr_in))[0]
        eigen_values.sort()
        fermi_vel_out = eigen_values[
            len(eigen_values) // 2 - band_index : len(eigen_values) // 2 + band_index
        ]

        if valley_index == "K1":
            # # Exclusion of K point, which is a singularity
            fermi_vel_out = abs(
                (array(fermi_vel_out) - self.ref_energy) / (norm(k_arr_in - self.K_1))
            ) / (h_bar_eV * eV2meV * m2A * 1e3)

            # # Inclusion of K point, which is a singularity
            # if norm(k_arr_in - self.K_1) != 0:
            #     fermi_vel_out = abs((array(fermi_vel_out) - self.ref_energy) / (norm(k_arr_in - self.K_1))) / (h_bar_eV * eV2meV * m2A * 1e6)
            # elif norm(k_arr_in - self.K_1) == 0:
            #     fermi_vel_out = np.zeros(len(fermi_vel_out))
        elif valley_index == "K2":
            # # Exclusion of K point, which is a singularity
            fermi_vel_out = abs(
                (array(fermi_vel_out) - self.ref_energy) / (norm(k_arr_in - self.K_2))
            ) / (h_bar_eV * eV2meV * m2A * 1e3)

            # # Inclusion of K point, which is a singularity
            # if norm(k_arr_in - self.K_2) != 0:
            #     fermi_vel_out = abs((array(fermi_vel_out) - self.ref_energy) / (norm(k_arr_in - self.K_2))) / (h_bar_eV * eV2meV * m2A * 1e6)
            # elif norm(k_arr_in - self.K_2) == 0:
            #     fermi_vel_out = np.zeros(len(fermi_vel_out))
        return fermi_vel_out

    def multi_proc_get_fermi_vel_from_K(self, args_list):
        """
        :param args_list: [k_arr_list, band_index]
        :return: list
        """
        parts_list = PubMeth.divide_list(args_list[0])
        print("# of total k: ", len(args_list[0]))
        eigen_enegies = PubMeth.multi_proc_func(
            self.get_fermi_vel_from_K, parts_list, [args_list[-1]]
        )
        return eigen_enegies

    def contour_of_fermi_vel_around_K(
        self,
        center_vec,
        delta_vec,
        band_range_width,
        density=70,
        filename="contour",
        contour_color="Hot",
        size_of_contour=0.001,
    ):
        dots_arr_list = PubMeth.dots_around_one_point(
            center_vec, delta_vec, density=density
        )
        energies_list = self.multi_proc_get_fermi_vel_from_K(
            [dots_arr_list, band_range_width]
        )
        save_path = PubMeth.get_right_save_path_and_create(
            "contour_fermi_vel_plots", data_files_or_not=True
        )
        save_path_data = PubMeth.get_right_save_path_and_create(
            "contour_fermi_vel_data", data_files_or_not=True
        )

        for draw_i in range(0, 2 * band_range_width):
            trace1 = go.Contour(
                z=array(real(energies_list))[:, draw_i].reshape(
                    (density + 1, density + 1)
                ),
                contours_coloring="lines",
                colorscale=[[0, "gold"], [0.5, "mediumturquoise"], [1, "lightsalmon"]],
                line_width=1,
                contours={
                    "showlabels": True,
                    "labelfont": {"size": 12, "color": "green"},
                    "start": 0,
                    "end": 3000,
                    "size": 5,
                },
            )
            layout = PubMeth.plotly_layout(
                figuretitle="Contour of Fermi Velocity for Bnad {}. Angle = {:.2f}".format(
                    draw_i, self.twist_angle
                )
            )
            fig = go.Figure(data=[trace1], layout=layout)
            fig.update_yaxes(
                scaleanchor="x",
                scaleratio=1,
            )
            filename = "contour_{:.2f}_fermi_vel_{}".format(self.twist_angle, draw_i)
            # fig.update_traces(ncontours=45, selector=dict(type='contour'))
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            if not os.path.exists(save_path_data):
                os.makedirs(save_path_data)
            np.save(
                save_path_data + filename + ".npy",
                array(real(energies_list))[:, draw_i].reshape(
                    (density + 1, density + 1)
                ),
            )
            fig.write_html(save_path + filename + ".html")

    def surface_at_certain_energy(
        self,
        target_energy,
        center_vec,
        delta_vec,
        band_index_b_t,
        density=70,
        filename="tb_surface_at_energy",
        tolerance=2,
        path=1,
        x_label=1,
        band_y_range=[-2000, 2000],
        line_type="k-",
        lw=2,
    ):
        """
        :param args_list: [target energy, center vector, delta vector, band_index_b_t list]
        :return:
        """
        save_data_name = (
            filename
            + "_density_"
            + "{}".format(density)
            + "_center_"
            + "{}_{}_delta_{}_{}".format(
                center_vec[0], center_vec[1], delta_vec[0], delta_vec[1]
            )
        )
        save_fig_name = (
            filename
            + "_"
            + "{:.4f}".format(target_energy)
            + "_density_"
            + "{}_{}_{}".format(density, path, x_label)
        )
        save_bands_name = "bands_for_surface_plot_{}_{}_".format(path, x_label)
        save_path_figs = PubMeth.get_right_save_path_and_create(
            "surface_at_energy_plots", data_files_or_not=True
        )
        save_path_data = PubMeth.get_right_save_path_and_create(
            "surface_at_energy_data", data_files_or_not=True
        )
        save_path_bands = PubMeth.get_right_save_path_and_create(
            "surface_at_energy_data", data_files_or_not=True
        )
        ratio_deltav_to_K = norm(delta_vec) / norm(self.K_1)
        # energies_list = self.plot_along_path(0, 0, save_fig_or_not=False, save_npy_or_not=True, save_npy_title=save_bands_name, save_npy_dir_name='surface_at_energy_data')
        if os.path.exists(save_path_data + save_data_name + ".npy"):
            fig_bands_and_surface = plt.figure(figsize=(17, 5))
            if os.path.exists(save_path_bands + save_bands_name + ".npy"):
                bands_data = np.load(save_path_bands + save_bands_name + ".npy")
                fig_band_title = (
                    r"Band structure for $\theta={:.3f} \degree$-{}".format(
                        self.twist_angle, self.mat_type
                    )
                )
                x_label_pos = PubMeth.situate_x_labels(
                    self.default_paths[path], self.density_per_path
                )
                x_labs = self.default_path_labels[x_label]

                gs = fig_bands_and_surface.add_gridspec(1, 3)
                ax_bands = fig_bands_and_surface.add_subplot(gs[0, 0:2])
                ax_bands.plot(real(bands_data), line_type, linewidth=lw)
                ax_bands.set_ylabel("E(meV)", fontsize=12)
                ax_bands.set_title(fig_band_title, fontsize=14)
                ax_bands.set_xticks(x_label_pos, x_labs)
                ax_bands.plot(
                    np.kron(
                        ones(len(bands_data)).reshape(len(bands_data), 1), target_energy
                    ),
                    "r--",
                    linewidth=lw,
                )
                ax_bands.set_ylim(band_y_range)

            elif not os.path.exists(save_path_bands + save_bands_name + ".npy"):
                bands_data = self.plot_along_path(
                    path,
                    x_label,
                    yrange=band_y_range,
                    save_fig_or_not=False,
                    save_npy_or_not=True,
                    save_npy_title=save_bands_name,
                    save_npy_dir_name="surface_at_energy_data",
                )

                fig_band_title = (
                    r"Band structure for $\theta={:.3f} \degree$-{}".format(
                        self.twist_angle, self.mat_type
                    )
                )
                x_label_pos = PubMeth.situate_x_labels(
                    self.default_paths[path], self.density_per_path
                )
                x_labs = self.default_path_labels[x_label]

                gs = fig_bands_and_surface.add_gridspec(1, 3)
                ax_bands = fig_bands_and_surface.add_subplot(gs[0, 0:2])
                ax_bands.plot(real(bands_data), line_type, linewidth=lw)
                ax_bands.set_ylabel("E(meV)", fontsize=12)
                ax_bands.set_title(fig_band_title, fontsize=14)
                ax_bands.set_xticks(x_label_pos, x_labs)
                ax_bands.plot(
                    np.kron(
                        ones(len(bands_data)).reshape(len(bands_data), 1), target_energy
                    ),
                    "r--",
                    linewidth=lw,
                )
                ax_bands.set_ylim(band_y_range)

            print("Using the existing data...")
            energies_list = np.load(save_path_data + save_data_name + ".npy")
            if (
                min(array(energies_list)[:, 0]) < target_energy
                and max(array(energies_list)[:, -1]) > target_energy
            ):
                band_inclusion_list = []
                for ele_band in array(energies_list).T:
                    if max(ele_band) > target_energy and min(ele_band) < target_energy:
                        band_inclusion_list.append(ele_band)
                    elif (
                        abs(max(ele_band) - target_energy) < tolerance
                        or abs(min(ele_band) - target_energy) < tolerance
                    ):
                        band_inclusion_list.append(ele_band)
                    else:
                        continue
                energy_dist = np.sum(
                    abs(array(band_inclusion_list) - target_energy) < tolerance, axis=0
                )
                reshaped_energy_dist = energy_dist.reshape(
                    (int(sqrt(len(energies_list))), int(sqrt(len(energies_list))))
                )
                # plt.figure(dpi=330, figsize=(7, 7))
                ax_surface = fig_bands_and_surface.add_subplot(gs[0, 2])
                img_surface = ax_surface.imshow(reshaped_energy_dist, vmin=0, vmax=2)
                fig_surface = ax_surface.figure
                ax_surface.set_aspect("auto")
                ax_surface.set_xticks(
                    [-0.5, len(reshaped_energy_dist) - 0.5],
                    [
                        "-{:.3f}|K|".format(ratio_deltav_to_K),
                        "{:.3f}|K|".format(ratio_deltav_to_K),
                    ],
                )
                ax_surface.set_yticks(
                    [-0.5, len(reshaped_energy_dist) - 0.5],
                    [
                        "-{:.3f}|K|".format(ratio_deltav_to_K),
                        "{:.3f}|K|".format(ratio_deltav_to_K),
                    ],
                )
                ax_surface.set_title(
                    "The Fermi surface at E={:.3f}meV".format(target_energy),
                    fontsize=14,
                )
                c_ax = PubMeth.add_right_cax(ax_surface, 0.02, 0.02)
                fig_surface.colorbar(img_surface, cax=c_ax)
                if not os.path.exists(save_path_figs):
                    os.makedirs(save_path_figs)
                fig_bands_and_surface.savefig(
                    save_path_figs + save_fig_name + global_fig_format,
                    dpi=330,
                    facecolor="w",
                )
                plt.close()

            elif min(array(energies_list)[:, 0]) > target_energy:
                print("Selected Energy below the bands chosen!")
                return
            elif max(array(energies_list)[:, -1]) < target_energy:
                print("Selected Energy over the bands chosen!")
                return
        elif not os.path.exists(save_path_data + save_data_name + ".npy"):
            fig_bands_and_surface = plt.figure(figsize=(15, 5))
            dots_arr_list = PubMeth.dots_around_one_point(
                center_vec, delta_vec, density=density
            )
            energies_list = self.multi_proc_energy_at_k([dots_arr_list, band_index_b_t])
            if not os.path.exists(save_path_data):
                os.makedirs(save_path_data)
            np.save(save_path_data + save_data_name + ".npy", energies_list)

            if os.path.exists(save_path_bands + save_bands_name + ".npy"):
                bands_data = np.load(save_path_bands + save_bands_name + ".npy")
                fig_band_title = (
                    r"Band structure for $\theta={:.3f} \degree$-{}".format(
                        self.twist_angle, self.mat_type
                    )
                )
                x_label_pos = PubMeth.situate_x_labels(
                    self.default_paths[path], self.density_per_path
                )
                x_labs = self.default_path_labels[x_label]

                gs = fig_bands_and_surface.add_gridspec(1, 3)
                ax_bands = fig_bands_and_surface.add_subplot(gs[0, 0:2])
                ax_bands.plot(real(bands_data), line_type, linewidth=lw)
                ax_bands.set_ylabel("E(meV)", fontsize=12)
                ax_bands.set_title(fig_band_title, fontsize=14)
                ax_bands.set_xticks(x_label_pos, x_labs)
                ax_bands.plot(
                    np.kron(
                        ones(len(bands_data)).reshape(len(bands_data), 1), target_energy
                    ),
                    "r--",
                    linewidth=lw,
                )
                ax_bands.set_ylim(band_y_range)

            elif not os.path.exists(save_path_bands + save_bands_name + ".npy"):
                bands_data = self.plot_along_path(
                    path,
                    x_label,
                    yrange=band_y_range,
                    save_fig_or_not=False,
                    save_npy_or_not=True,
                    save_npy_title=save_bands_name,
                    save_npy_dir_name="surface_at_energy_data",
                )

                fig_band_title = (
                    r"Band structure for $\theta={:.3f} \degree$-{}".format(
                        self.twist_angle, self.mat_type
                    )
                )
                x_label_pos = PubMeth.situate_x_labels(
                    self.default_paths[path], self.density_per_path
                )
                x_labs = self.default_path_labels[x_label]

                gs = fig_bands_and_surface.add_gridspec(1, 3)
                ax_bands = fig_bands_and_surface.add_subplot(gs[0, 0:2])
                ax_bands.plot(real(bands_data), line_type, linewidth=lw)
                ax_bands.set_ylabel("E(meV)", fontsize=12)
                ax_bands.set_title(fig_band_title, fontsize=14)
                ax_bands.set_xticks(x_label_pos, x_labs)
                ax_bands.plot(
                    np.kron(
                        ones(len(bands_data)).reshape(len(bands_data), 1), target_energy
                    ),
                    "r--",
                    linewidth=lw,
                )
                ax_bands.set_ylim(band_y_range)

            if (
                min(array(energies_list)[:, 0]) < target_energy
                and max(array(energies_list)[:, -1]) > target_energy
            ):
                band_inclusion_list = []
                for ele_band in array(energies_list).T:
                    if max(ele_band) > target_energy and min(ele_band) < target_energy:
                        band_inclusion_list.append(ele_band)
                    elif (
                        abs(max(ele_band) - target_energy) < tolerance
                        or abs(min(ele_band) - target_energy) < tolerance
                    ):
                        band_inclusion_list.append(ele_band)
                    else:
                        continue
                energy_dist = np.sum(
                    abs(array(band_inclusion_list) - target_energy) < tolerance, axis=0
                )
                reshaped_energy_dist = energy_dist.reshape(
                    (int(sqrt(len(energies_list))), int(sqrt(len(energies_list))))
                )
                # plt.figure(dpi=330, figsize=(7, 7))
                ax_surface = fig_bands_and_surface.add_subplot(gs[0, 2])
                ax_surface.imshow(reshaped_energy_dist)
                img_surface = ax_surface.imshow(reshaped_energy_dist, vmin=0, vmax=2)
                fig_surface = ax_surface.figure
                ax_surface.set_aspect("auto")
                ax_surface.set_xticks(
                    [-0.5, len(reshaped_energy_dist) - 0.5],
                    [
                        "-{:.3f}|K|".format(ratio_deltav_to_K),
                        "{:.3f}|K|".format(ratio_deltav_to_K),
                    ],
                )
                ax_surface.set_yticks(
                    [-0.5, len(reshaped_energy_dist) - 0.5],
                    [
                        "-{:.3f}|K|".format(ratio_deltav_to_K),
                        "{:.3f}|K|".format(ratio_deltav_to_K),
                    ],
                )
                ax_surface.set_title(
                    "The Fermi surface at E={:.3f}meV".format(target_energy),
                    fontsize=14,
                )
                c_ax = PubMeth.add_right_cax(ax_surface, 0.02, 0.02)
                fig_surface.colorbar(img_surface, cax=c_ax)
                if not os.path.exists(save_path_figs):
                    os.makedirs(save_path_figs)
                fig_bands_and_surface.savefig(
                    save_path_figs + save_fig_name + global_fig_format,
                    dpi=330,
                    facecolor="w",
                )
                plt.close()

    def multi_proc_dos_cal(
        self,
        save_fig_or_not=True,
        save_fig_dir_name="dos",
        save_dat_dir_name="dos_data",
        energy_range=[],
        bins_num="auto",
    ):
        save_fig_dir = PubMeth.get_right_save_path_and_create(
            save_fig_dir_name, data_files_or_not=True
        )
        save_fig_name = save_fig_dir + "{}_dos_{}_{}.png".format(
            self.model_type, self.twist_angle, self.mat_type
        )
        save_dat_dir = PubMeth.get_right_save_path_and_create(
            save_dat_dir_name, data_files_or_not=True
        )
        save_dat_name = save_dat_dir + "{}_dos_{}_{}_density_{}.npy".format(
            self.model_type, self.twist_angle, self.mat_type, self.kp_num
        )
        if save_fig_or_not:
            if not os.path.exists(save_fig_dir):
                os.makedirs(save_fig_dir)
            if not os.path.exists(save_dat_dir):
                os.makedirs(save_dat_dir)

        if not os.path.exists(save_dat_name):
            k_arrs_list = self.kp_in_moire_b_zone()
            energies_set = self.multi_proc_energy_at_k([k_arrs_list, [-10, 10]])
            np.save(save_dat_name, energies_set)
            energies_set = array(energies_set).reshape(
                -1,
            )
            if len(energy_range) != 0:
                energy_filter = (energies_set > energy_range[0]) & (
                    energies_set < energy_range[1]
                )
                energies_set = energies_set[energy_filter]
            n, bins, patches = plt.hist(
                x=energies_set, bins=bins_num, color="grey", alpha=0.7, rwidth=0.85
            )
            print("# of bins: ", len(n))
            ax = plt.gca()
            ax.set_xlabel("E(meV)", fontsize=12)
            ax.set_ylabel("DOS", fontsize=12)
            ax.set_title("DOS of {}".format(self.mat_type), fontsize=14)
            x_pos = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
            plt.plot(x_pos, n)
            plt.savefig(save_fig_name, dpi=330, facecolor="w")
            plt.close()
        elif os.path.exists(save_dat_name):
            print("Using the existing data...")
            energies_set = np.load(save_dat_name)
            energies_set = array(energies_set).reshape(
                -1,
            )
            if len(energy_range) != 0:
                energy_filter = (energies_set > energy_range[0]) & (
                    energies_set < energy_range[1]
                )
                energies_set = energies_set[energy_filter]
            n, bins, patches = plt.hist(
                x=energies_set, bins=bins_num, color="grey", alpha=0.7, rwidth=0.85
            )
            print("# of bins: ", len(n))
            ax = plt.gca()
            ax.set_xlabel("E(meV)", fontsize=12)
            ax.set_ylabel("DOS", fontsize=12)
            ax.set_title("DOS of {}".format(self.mat_type), fontsize=14)
            x_pos = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
            plt.plot(x_pos, n)
            plt.savefig(save_fig_name, dpi=330, facecolor="w")
            plt.close()

    def multi_proc_jdos_cal_all_BZ(
        self,
        save_fig_or_not=True,
        save_fig_dir_name="jdos",
        save_dat_dir_name="dos_data",
        bins_num="auto",
        energy_range=[],
    ):
        save_fig_dir = PubMeth.get_right_save_path_and_create(
            save_fig_dir_name, data_files_or_not=True
        )
        save_fig_name = save_fig_dir + "{}_jdos_{}_{}.png".format(
            self.model_type, self.twist_angle, self.mat_type
        )
        save_dat_dir = PubMeth.get_right_save_path_and_create(
            save_dat_dir_name, data_files_or_not=True
        )
        save_dat_name = save_dat_dir + "{}_dos_{}_{}_density_{}.npy".format(
            self.model_type, self.twist_angle, self.mat_type, self.kp_num
        )
        if save_fig_or_not:
            if not os.path.exists(save_fig_dir):
                os.makedirs(save_fig_dir)
            if not os.path.exists(save_dat_dir):
                os.makedirs(save_dat_dir)

        if not os.path.exists(save_dat_name):
            k_arrs_list = self.kp_in_moire_b_zone()
            energies_set = self.multi_proc_energy_at_k([k_arrs_list, [-10, 10]])
            np.save(save_dat_name, energies_set)
            c_energy_set = energies_set[:, (energies_set.shape[1]) // 2 :].T
            v_energy_set = energies_set[:, : (energies_set.shape[1]) // 2].T
            j_energy_set = [c_energy_set - ele_e for ele_e in v_energy_set]
            j_energy_set = array(j_energy_set).reshape(
                -1,
            )
            if len(energy_range) != 0:
                energy_filter = (j_energy_set > energy_range[0]) & (
                    j_energy_set < energy_range[1]
                )
                j_energy_set = j_energy_set[energy_filter]

            n, bins, patches = plt.hist(
                x=j_energy_set, bins=bins_num, color="grey", alpha=0.7, rwidth=0.85
            )
            print("# of bins: ", len(n))
            ax = plt.gca()
            ax.set_xlabel("E(meV)", fontsize=12)
            ax.set_ylabel("JDOS", fontsize=12)
            ax.set_yticks([])
            ax.set_title(
                "JDOS of {:.3f}$\degree$-{}".format(self.twist_angle, self.mat_type),
                fontsize=14,
            )
            x_pos = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
            plt.plot(x_pos, n)
            plt.savefig(save_fig_name, dpi=330, facecolor="w")
            plt.close()
        elif os.path.exists(save_dat_name):
            print("Using the existing data...")
            energies_set = np.load(save_dat_name)
            c_energy_set = energies_set[:, (energies_set.shape[1]) // 2 :].T
            v_energy_set = energies_set[:, : (energies_set.shape[1]) // 2].T
            j_energy_set = [c_energy_set - ele_e for ele_e in v_energy_set]
            j_energy_set = array(j_energy_set).reshape(
                -1,
            )
            if len(energy_range) != 0:
                energy_filter = (j_energy_set > energy_range[0]) & (
                    j_energy_set < energy_range[1]
                )
                j_energy_set = j_energy_set[energy_filter]

            n, bins, patches = plt.hist(
                x=j_energy_set, bins=bins_num, color="grey", alpha=0.7, rwidth=0.85
            )
            print("# of bins: ", len(n))
            ax = plt.gca()
            ax.set_xlabel("E(meV)", fontsize=12)
            ax.set_ylabel("JDOS", fontsize=12)
            ax.set_yticks([])
            ax.set_title(
                "JDOS of {:.3f}$\degree$-{}".format(self.twist_angle, self.mat_type),
                fontsize=14,
            )
            x_pos = [(bins[i] + bins[i + 1]) / 2 for i in range(0, len(bins) - 1)]
            plt.plot(x_pos, n)
            plt.savefig(save_fig_name, dpi=330, facecolor="w")
            plt.close()


class ContiNearComm(ContiTbgInst):
    def __init__(
        self,
        m0,
        r,
        couple_pars_list,
        displace_d=array([0, 0]),
        delta_angle=0,
        a0_constant=1.42 * sqrt(3),
        density_per_path=100,
        delta_angle_equal_magic=False,
        basis_loop_times=7,
    ) -> None:
        self.m0 = m0
        self.r = r

        self.chi_0 = couple_pars_list[0]
        self.chi_theta = self.chi_0 / 180 * pi
        self.w_0 = couple_pars_list[1]
        self.w_1 = couple_pars_list[2]
        self.w_2 = couple_pars_list[3]

        self.twist_angle_comm, self.twist_theta_comm = PubMeth.commensurate_angle(m0, r)
        self.n_unit_cell_within = PubMeth.unit_cell_per_supercell(m0, r)
        self.n_atoms = 4 * self.n_unit_cell_within
        self.norm_reci_vec = 4 * pi / (sqrt(3) * a0_constant)
        self.norm_K = 4 * pi / (3 * a0_constant)
        self.displace_d_arr = displace_d
        self.a0_constant = a0_constant
        self.norm_side = a0_constant / sqrt(3)

        self.v_F = 3.68423316 * a0_constant / (sqrt(3) * h_bar_eV * m2A)
        self.delta_theta_magic = (
            sqrt(3)
            * self.w_1
            / (
                h_bar_eV
                * self.v_F
                * eV2meV
                * m2A
                * sqrt(self.n_unit_cell_within)
                * self.norm_K
            )
        )
        self.delta_angle_magic = self.delta_theta_magic / pi * 180

        if delta_angle_equal_magic:
            self.delta_angle = self.delta_angle_magic
            self.delta_theta = self.delta_theta_magic
        else:
            self.delta_angle = delta_angle
            self.delta_theta = delta_angle / 180 * pi

        self.a_1 = a0_constant * array([1, 0])
        self.a_2 = PubMeth.rotation(-60) @ self.a_1

        self.b_1 = self.norm_reci_vec * array([sqrt(3) / 2, 1 / 2])
        self.b_2 = PubMeth.rotation(-120) @ self.b_1
        self.Gamma_arr = array([0, 0])
        self.K_arr = self.norm_K * array([1, 0])
        self.K_prime_arr = PubMeth.rotation(-60) @ self.K_arr
        self.M_arr = (self.K_arr + self.K_prime_arr) / 2

        self.half_angle_cos = cos(self.twist_theta_comm / 2)
        self.half_angle_sin = sin(self.twist_theta_comm / 2)
        self.original_s = int(
            (
                self.half_angle_cos * sqrt(self.n_unit_cell_within)
                + self.half_angle_sin * sqrt(self.n_unit_cell_within) * sqrt(3)
            )
        )
        if self.original_s % 3 == 1:
            self.s = 1
        elif self.original_s % 3 == 2:
            self.s = -1
        else:
            self.s = 1

        self.Q_1 = self.s * sqrt(self.n_unit_cell_within) * self.K_arr
        self.Q_2 = PubMeth.rotation(120) @ self.Q_1
        self.Q_3 = PubMeth.rotation(240) @ self.Q_1
        self.Q_list = [self.Q_1, self.Q_2, self.Q_3]
        self.norm_Q = norm(self.Q_1)

        self.q_1 = PubMeth.operator_d_theta(self.delta_angle) @ self.Q_1
        self.q_2 = PubMeth.rotation(120) @ self.q_1
        self.q_3 = PubMeth.rotation(240) @ self.q_1
        self.q_list = [self.q_1, self.q_2, self.q_3]
        self.norm_q = norm(self.q_1)

        super().__init__(
            twist_angle_conti=self.delta_angle,
            v_F=self.v_F,
            a0_constant=self.a0_constant / sqrt(self.n_unit_cell_within),
            basis_loop_times=basis_loop_times,
        )

        # self.K_M_arr = PubMeth.operator_d_theta(self.delta_angle) @ (self.s * sqrt(self.n_unit_cell_within) *  self.K_arr)
        # self.K_prime_M_arr = PubMeth.operator_d_theta(self.delta_angle) @ (self.s * sqrt(self.n_unit_cell_within) *  self.K_prime_arr)
        # self.M_M_arr = PubMeth.operator_d_theta(self.delta_angle) @ (self.s * sqrt(self.n_unit_cell_within) *  self.M_arr)

        self.norm_p0 = 3 * abs(self.w_0) / (h_bar_eV * self.v_F * eV2meV * m2A)
        self.p_0 = self.norm_p0 * array([1, 0])

        self.density_per_path = density_per_path / self.norm_K

    def T_Qj(self, j_index):  # # j_index = 1, 2, 3
        ksi_j = 2 * pi * (j_index - 1) / 3
        return self.w_0 * expm(
            1j * self.chi_theta * PubMeth.pauli_mat(3)
        ) + self.w_1 * (
            PubMeth.pauli_mat(1) * cos(ksi_j) + PubMeth.pauli_mat(2) * sin(ksi_j)
        )

    def T_0_comm(self):
        T_out = zeros((2, 2))
        for j_index in range(len(self.Q_list)):
            T_out = T_out + self.T_Qj(j_index + 1) * exp(
                1j
                * self.displace_d_arr
                @ (cos(self.twist_theta_comm / 2) * self.K_arr - self.Q_list[j_index])
            )
        return T_out

    def S_0_comm(self):
        return (
            self.w_2
            * PubMeth.pauli_mat(0)
            * exp(
                1j * self.displace_d_arr @ (cos(self.twist_theta_comm / 2) * self.K_arr)
            )
        )

    def intra_h_comm(self, p_arr):
        return (
            h_bar_eV
            * self.v_F
            * m2A
            * eV2meV
            * np.block(
                [
                    [
                        PubMeth.sigma_angle_dot_p(p_arr, self.twist_angle_comm / 2),
                        zeros((2, 2)),
                    ],
                    [
                        zeros((2, 2)),
                        PubMeth.sigma_angle_dot_p(p_arr, -self.twist_angle_comm / 2),
                    ],
                ]
            )
        )

    def inter_h_comm(self):
        return np.block(
            [
                [self.S_0_comm(), self.T_0_comm()],
                [conj(self.T_0_comm()).T, self.S_0_comm()],
            ]
        )

    def h_b(self, k):
        k_mod = (k - self.k_b_arr) * self.norm_Kg_conti
        return h_bar_eV * self.v_F * m2A * eV2meV * PubMeth.sigma_angle_dot_p(
            k_mod, self.twist_angle_comm / 2
        ) + self.w_2 * np.eye(2)

    def h_t(self, k):
        k_mod = (k - self.k_t_arr) * self.norm_Kg_conti
        return h_bar_eV * self.v_F * m2A * eV2meV * PubMeth.sigma_angle_dot_p(
            k_mod, -self.twist_angle_comm / 2
        ) + self.w_2 * np.eye(2)

    def T_Qj(self, j_index):  # # j_index = 1, 2, 3
        ksi_j = 2 * pi * (j_index - 1) / 3
        return self.w_0 * expm(
            1j * self.chi_theta * PubMeth.pauli_mat(3)
        ) + self.w_1 * (
            PubMeth.pauli_mat(1) * cos(ksi_j) + PubMeth.pauli_mat(2) * sin(ksi_j)
        )

    def t_0(self):
        return conj(self.T_Qj(1)).T

    def t_p1(self):
        return conj(self.T_Qj(2)).T

    def t_n1(self):
        return conj(self.T_Qj(3)).T

    def hamiltonian_construction(self, p_arr):
        if self.delta_angle == 0:
            return self.intra_h_comm(p_arr) + self.inter_h_comm()
        elif self.delta_angle != 0:
            return super().hamiltonian_construction(p_arr)

    def plot_along_path(
        self,
        path,
        labels,
        yrange,
        line_s="k-",
        lw=1,
        save_or_not=True,
        show=False,
        hold_or_not=False,
        figsize=(7, 5),
        shift_energy=True,
        test_or_not=True,
    ):
        if isinstance(path, int):
            self.multi_proc_path(
                self.default_paths[path],
                x_labs=self.default_path_labels[path],
                y_range=yrange,
                line_type=line_s,
                lw=lw,
                save_fig_or_not=save_or_not,
                show_or_not=show,
                hold_on=hold_or_not,
                comm_angle_in_title=self.twist_angle_comm,
                delta_angle_in_title=self.delta_angle,
                shift_energy=shift_energy,
                test_mode=test_or_not,
            )
        else:
            self.multi_proc_path(
                path,
                save_fig_or_not=save_or_not,
                x_labs=labels,
                y_range=yrange,
                line_type=line_s,
                lw=lw,
                show_or_not=show,
                hold_on=hold_or_not,
                figsize=figsize,
                comm_angle_in_title=self.twist_angle_comm,
                delta_angle_in_title=self.delta_angle,
                shift_energy=shift_energy,
                test_mode=test_or_not,
            )


def main():
    for i in range(1, 10):
        a = TightTbgInst(i, 3)
        print(a.twist_angle)


if __name__ == "__main__":
    main()
