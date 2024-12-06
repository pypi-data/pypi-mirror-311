from public.method import *
from public.consts import *

from mono.TB_mono_tmds import MonoMoS2


## 10.1103/PhysRevB.91.075310
class MoS2(MonoMoS2):
    # # all parameters are in unit of eV
    O1 = 3.558
    t = -0.189
    t_pri = -0.117
    txy = 0.024
    s = -0.041
    s_pri = 0.003
    u = 0.165
    u_pri = -0.122
    uxy = -0.140

    def __init__(
        self,
        lam=0.073,
        diele_const=2.5,
        v_bands_num=2,
        c_bands_num_take=2,
        k_mesh_density=40,
        h_dim=10,
        k_boundary=True,
    ):
        super().__init__(par_type="GGA")
        self.lam = lam
        self.diele_const = diele_const  # CGS unit
        self.r0_ratio = 33.875 / self.diele_const
        self.R1 = self.a * array([1, 0])
        self.R2 = self.a * array([1 / 2, sqrt(3) / 2])
        self.b1 = self.Kg * sqrt(3) * array([sqrt(3) / 2, -1 / 2])
        self.b2 = self.Kg * sqrt(3) * array([0, 1])

        ##  Vector in momentum space
        self.M_arr = self.b1 / 2
        self.K_arr = self.Kg * array([1, 0])

        ##  Number of valence bands
        self.v_bands_num = v_bands_num
        self.c_bands_take = c_bands_num_take

        self.k_mesh_density = k_mesh_density
        self.N_k = k_mesh_density**2
        self.h_dim = h_dim

        self.k_boundary = k_boundary

    def soc_mat(self):  # eV for lam
        soc_coup_mat = array(
            [
                [0, 0, 0, 0, 0, 0, 0, 0, -sqrt(3), sqrt(3) * 1j],
                [0, 0, 2j, 0, 0, 0, 0, 0, -1j, 1],
                [0, -2j, 0, 0, 0, 0, 0, 0, 1, 1j],
                [0, 0, 0, 0, -1j, sqrt(3), 1j, -1, 0, 0],
                [0, 0, 0, 1j, 0, -sqrt(3) * 1j, -1, -1j, 0, 0],
                [0, 0, 0, sqrt(3), sqrt(3) * 1j, 0, 0, 0, 0, 0],
                [0, 0, 0, -1j, -1, 0, 0, -2j, 0, 0],
                [0, 0, 0, -1, 1j, 0, 2j, 0, 0, 0],
                [-sqrt(3), 1j, 1, 0, 0, 0, 0, 0, 0, 1j],
                [-sqrt(3) * 1j, 1, -1j, 0, 0, 0, 0, 0, -1j, 0],
            ]
        )

        return self.lam / 2 * soc_coup_mat

    def H0_even(self, k_arr):
        return super().hamiltonian(k_arr)

    def H0_odd(self, k_arr):
        alpha = 1 / 2 * k_arr[0] * self.a
        beta = sqrt(3) / 2 * k_arr[1] * self.a

        def hx():
            return (
                self.O1
                + 2 * self.t * cos(2 * alpha)
                + (self.t + 3 * self.t_pri) * cos(alpha) * cos(beta)
                + 4 * self.s * cos(3 * alpha) * cos(beta)
                + (3 * self.s_pri - self.s) * cos(2 * beta)
                + 2 * self.u * cos(4 * alpha)
                + (self.u + 3 * self.u_pri) * cos(2 * alpha) * cos(2 * beta)
            )

        def hy():
            return (
                self.O1
                + 2 * self.t_pri * cos(2 * alpha)
                + (self.t_pri + 3 * self.t) * cos(alpha) * cos(beta)
                + 4 * self.s_pri * cos(3 * alpha) * cos(beta)
                + (3 * self.s - self.s_pri) * cos(2 * beta)
                + 2 * self.u_pri * cos(4 * alpha)
                + (self.u_pri + 3 * self.u) * cos(2 * alpha) * cos(2 * beta)
            )

        def hxy():
            return (
                4j * self.txy * sin(alpha) * (cos(alpha) - cos(beta))
                + sqrt(3) * (self.t_pri - self.t) * sin(alpha) * sin(beta)
                + 2
                * sqrt(3)
                * (self.s_pri - self.s)
                * sin(alpha)
                * sin(beta)
                * (1 + 2 * cos(2 * alpha))
                + 4j * self.uxy * sin(2 * alpha) * (cos(2 * alpha) - cos(2 * beta))
                + sqrt(3) * (self.u_pri - self.u) * sin(2 * alpha) * sin(2 * beta)
            )

        return array([[hx(), hxy()], [conj(hxy()), hy()]])

    def H0(self, k_arr):
        return block(
            [[self.H0_even(k_arr), zeros((3, 2))], [zeros((2, 3)), self.H0_odd(k_arr)]]
        )

    def hamiltonian(self, k_arr):
        return self.soc_mat() + kron(eye(2), self.H0(k_arr))

    def get_sort_vals_vecs(self, k_arr):
        eig_vals, eig_vecs_mat = eig(self.hamiltonian(k_arr))
        sort_arr = np.argsort(real(eig_vals))

        ##  sort eigenvalues
        eig_vals = real(eig_vals)[sort_arr]

        ##  sort eigenvectors (Each column stands for a eigenvector)
        eig_vecs_mat = eig_vecs_mat.T[sort_arr].T

        ##  Even and odd judge arr
        middle_vecs_mat = eig_vecs_mat[arange(3, 8)]

        even_judge = diag(conj(middle_vecs_mat).T @ middle_vecs_mat) < 0.05
        odd_judge = array([not ele_bool for ele_bool in even_judge])

        if len(even_judge[even_judge]) != 5:
            print(diag(conj(middle_vecs_mat).T @ middle_vecs_mat))

        return eig_vals, eig_vecs_mat, even_judge, odd_judge

    def loop_to_load_save_vals_vecs_judge(self, Q_arr):
        """
        Use for loop to save all the energies and vectors
        """
        Qx = Q_arr[0]
        Qy = Q_arr[1]

        k_vals_arr = []
        k_vecs_mat = []
        k_vecs_mat_T = []
        k_even_judge_arr = []
        k_odd_judge_arr = []

        q_vals_arr = []
        q_vecs_mat = []
        q_vecs_mat_T = []
        q_even_judge_arr = []
        q_odd_judge_arr = []

        name_q = "{}_Q_{:.3f}_{:.3f}.npy".format(self.k_mesh_density, Qx, Qy)
        name_k = "{}_k_.npy".format(self.k_mesh_density, Qx, Qy)

        V_k_diff_name = (
            "/home/aoxv/code/Data/bands/MoS2/npy/V_k_diff/"
            + "V_q_{}.npy".format(self.k_mesh_density)
        )
        if os.path.exists(V_k_diff_name):
            print("Using existing Vq matrix")
            V_q_mat = np.load(V_k_diff_name)
        else:
            k_diff_mat = PubMeth.vec_lists_for_loop_plus_minus(
                self.k_mesh(), self.k_mesh(), operation="minus"
            )
            k_diff_mat = k_diff_mat.reshape((-1, 2))

            V_q_mat = self.V_q(k_diff_mat).reshape(
                (self.k_mesh_density**2, self.k_mesh_density**2)
            )
            row, col = np.diag_indices_from(V_q_mat)
            V_q_mat[row, col] = 0
            np.save(V_k_diff_name, V_q_mat)

        if os.path.exists(
            "/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_k
        ) and not os.path.exists(
            "/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_q
        ):
            print("K data exists and Q data doesn't exist!")
            t1 = time.perf_counter()
            for ele_k in self.k_mesh():
                ele_k_q = ele_k + Q_arr

                (
                    ele_q_vals,
                    ele_q_vecs,
                    ele_q_even_j,
                    ele_q_odd_j,
                ) = self.get_sort_vals_vecs(ele_k_q)
                q_vals_arr.append(ele_q_vals)
                q_vecs_mat.append(ele_q_vecs)
                q_vecs_mat_T.append(conj(ele_q_vecs).T)
                q_even_judge_arr.append(ele_q_even_j)
                q_odd_judge_arr.append(ele_q_odd_j)
            t2 = time.perf_counter()
            print("Time it takes to loop Q to the end: (s)", t2 - t1)
            k_vals_arr = np.load("/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_k)
            k_vecs_mat = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/col_vector/" + name_k
            )
            k_vecs_mat_T = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/row_vector/" + name_k
            )
            k_even_judge_arr = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/even_judge/" + name_k
            )
            k_odd_judge_arr = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/odd_judge/" + name_k
            )

            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_q,
                np.hstack(q_vals_arr),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/col_vector/" + name_q,
                np.hstack(q_vecs_mat),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/row_vector/" + name_q,
                np.vstack(q_vecs_mat_T),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/even_judge/" + name_q,
                np.hstack(q_even_judge_arr),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/odd_judge/" + name_q,
                np.hstack(q_odd_judge_arr),
            )
            t2 = time.perf_counter()
            print("Time it takes to loop to the end: (s)", t2 - t1)
            return (
                k_vals_arr,
                k_vecs_mat,
                k_vecs_mat_T,
                k_even_judge_arr,
                k_odd_judge_arr,
                np.hstack(q_vals_arr),
                np.hstack(q_vecs_mat),
                np.vstack(q_vecs_mat_T),
                np.hstack(q_even_judge_arr),
                np.hstack(q_odd_judge_arr),
                V_q_mat,
            )
        elif os.path.exists(
            "/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_k
        ) and os.path.exists("/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_q):
            print("K and Q data exists!")
            t1 = time.perf_counter()
            k_vals_arr = np.load("/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_k)
            k_vecs_mat = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/col_vector/" + name_k
            )
            k_vecs_mat_T = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/row_vector/" + name_k
            )
            k_even_judge_arr = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/even_judge/" + name_k
            )
            k_odd_judge_arr = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/odd_judge/" + name_k
            )
            q_vals_arr = np.load("/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_q)
            q_vecs_mat = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/col_vector/" + name_q
            )
            q_vecs_mat_T = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/row_vector/" + name_q
            )
            q_even_judge_arr = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/even_judge/" + name_q
            )
            q_odd_judge_arr = np.load(
                "/home/aoxv/code/Data/bands/MoS2/npy/odd_judge/" + name_q
            )
            t2 = time.perf_counter()
            print("Time it takes to load: (s)", t2 - t1)
            return (
                k_vals_arr,
                k_vecs_mat,
                k_vecs_mat_T,
                k_even_judge_arr,
                k_odd_judge_arr,
                q_vals_arr,
                q_vecs_mat,
                q_vecs_mat_T,
                q_even_judge_arr,
                q_odd_judge_arr,
                V_q_mat,
            )
        else:
            t1 = time.perf_counter()
            for ele_k in self.k_mesh():
                ele_k_q = ele_k + Q_arr

                (
                    ele_k_vals,
                    ele_k_vecs,
                    ele_k_even_j,
                    ele_k_odd_j,
                ) = self.get_sort_vals_vecs(ele_k)
                (
                    ele_q_vals,
                    ele_q_vecs,
                    ele_q_even_j,
                    ele_q_odd_j,
                ) = self.get_sort_vals_vecs(ele_k_q)

                k_vals_arr.append(ele_k_vals)
                k_vecs_mat.append(ele_k_vecs)
                k_vecs_mat_T.append(conj(ele_k_vecs).T)
                k_even_judge_arr.append(ele_k_even_j)
                k_odd_judge_arr.append(ele_k_odd_j)

                q_vals_arr.append(ele_q_vals)
                q_vecs_mat.append(ele_q_vecs)
                q_vecs_mat_T.append(conj(ele_q_vecs).T)
                q_even_judge_arr.append(ele_q_even_j)
                q_odd_judge_arr.append(ele_q_odd_j)
            t2 = time.perf_counter()
            print("Time it takes to loop k and Q to the end: (s)", t2 - t1)

            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_k,
                np.hstack(k_vals_arr),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/col_vector/" + name_k,
                np.hstack(k_vecs_mat),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/row_vector/" + name_k,
                np.vstack(k_vecs_mat_T),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/even_judge/" + name_k,
                np.hstack(k_even_judge_arr),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/odd_judge/" + name_k,
                np.hstack(k_odd_judge_arr),
            )

            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/energy/" + name_q,
                np.hstack(q_vals_arr),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/col_vector/" + name_q,
                np.hstack(q_vecs_mat),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/row_vector/" + name_q,
                np.vstack(q_vecs_mat_T),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/even_judge/" + name_q,
                np.hstack(q_even_judge_arr),
            )
            np.save(
                "/home/aoxv/code/Data/bands/MoS2/npy/odd_judge/" + name_q,
                np.hstack(q_odd_judge_arr),
            )

            return (
                np.hstack(k_vals_arr),
                np.hstack(k_vecs_mat),
                np.vstack(k_vecs_mat_T),
                np.hstack(k_even_judge_arr),
                np.hstack(k_odd_judge_arr),
                np.hstack(q_vals_arr),
                np.hstack(q_vecs_mat),
                np.vstack(q_vecs_mat_T),
                np.hstack(q_even_judge_arr),
                np.hstack(q_odd_judge_arr),
                V_q_mat,
            )

    def slice_indices_in_each_sector(self, indices_to_get=[0, 1]):
        """
        Get slices of the array or matrices
        """
        out_indices = []
        for ele_sect_i in range(int(self.k_mesh_density**2)):
            out_indices = out_indices + [
                self.h_dim * ele_sect_i + ele_i for ele_i in indices_to_get
            ]
        return out_indices

    def exciton_mat(self, Q_arr, v_bands_indices=[0, 1], c_bands_indices=[2, 3]):
        """
        Take out valence and conduction bands in each sector.
        """
        t1 = time.perf_counter()
        v_bands_indices = self.slice_indices_in_each_sector(v_bands_indices)
        c_bands_indices = self.slice_indices_in_each_sector(c_bands_indices)

        ##  Get k and k+q vectors and values
        (
            k_vals_arr,
            k_vecs_mat,
            k_vecs_mat_T,
            k_even_judge_arr,
            k_odd_judge_arr,
            q_vals_arr,
            q_vecs_mat,
            q_vecs_mat_T,
            q_even_judge_arr,
            q_odd_judge_arr,
            V_q_mat,
        ) = self.loop_to_load_save_vals_vecs_judge(Q_arr)

        ##  V_Q term
        if norm(Q_arr) == 0:
            V_Q = 0
        else:
            V_Q = self.V_q(Q_arr)

        ##  judge array to pick out even and odd bands at k point for valence and conduction bands
        k_v_even_j = k_even_judge_arr[v_bands_indices]
        # k_c_even_j = k_even_judge_arr[c_bands_indices]
        k_v_odd_j = k_odd_judge_arr[v_bands_indices]
        # k_c_odd_j = k_odd_judge_arr[c_bands_indices]

        ##  judge array to pick out even and odd bands at k+q point for valence and conduction bands
        # q_v_even_j = q_even_judge_arr[v_bands_indices]
        q_c_even_j = q_even_judge_arr[c_bands_indices]
        # q_v_odd_j = q_odd_judge_arr[v_bands_indices]
        q_c_odd_j = q_odd_judge_arr[c_bands_indices]

        ##  pick out the column states for conduction and valence bands at k and k+q points
        k_v_vecs = k_vecs_mat[:, v_bands_indices]
        # k_c_vecs = k_vecs_mat[:, c_bands_indices]
        # q_v_vecs = q_vecs_mat[:, v_bands_indices]
        q_c_vecs = q_vecs_mat[:, c_bands_indices]

        ##  pick out the row states for conduction and valence bands at k and k+q points
        k_v_vecs_T = k_vecs_mat_T[v_bands_indices]
        # k_c_vecs_T = k_vecs_mat_T[c_bands_indices]
        # q_v_vecs_T = q_vecs_mat_T[v_bands_indices]
        q_c_vecs_T = q_vecs_mat_T[c_bands_indices]

        ##  pick out the valence energy at k point and conduction energy at k+q point
        k_v_e = k_vals_arr[v_bands_indices]
        q_c_e = q_vals_arr[c_bands_indices]

        ##  Divide the valence and conduction energies into even and odd branches
        k_v_e_even = k_v_e[k_v_even_j]
        k_v_e_odd = k_v_e[k_v_odd_j]
        q_c_e_even = q_c_e[q_c_even_j]
        q_c_e_odd = q_c_e[q_c_odd_j]

        ##  Diagonal terms --- Pick even term first and then odd term
        k_q_e_even_diff = q_c_e_even - k_v_e_even
        k_q_e_odd_diff = q_c_e_odd - k_v_e_odd
        diag_mat = diag(np.hstack([k_q_e_even_diff, k_q_e_odd_diff]))

        ##  Kronecker form of V_q matrix
        dim_mat = diag_mat.shape[0]
        dim_Vq = V_q_mat.shape[0]
        dim_diff = dim_mat // dim_Vq
        V_q_mat = np.kron(ones((dim_diff, dim_diff)), V_q_mat)

        ##  D term ---  the diagonal term should be 0
        ##  pick out the even and odd valence states at k point and reorganize them
        k_v_even_vecs = k_v_vecs[:, k_v_even_j]
        k_v_oddd_vecs = k_v_vecs[:, k_v_odd_j]
        k_v_even_oddd_vecs = np.hstack([k_v_even_vecs, k_v_oddd_vecs])

        k_v_even_vecs_T = k_v_vecs_T[k_v_even_j]
        k_v_oddd_vecs_T = k_v_vecs_T[k_v_odd_j]
        k_v_even_oddd_vecs_T = np.vstack([k_v_even_vecs_T, k_v_oddd_vecs_T])

        ##  D_1 term calculation
        D_1 = k_v_even_oddd_vecs_T @ k_v_even_oddd_vecs
        row, col = np.diag_indices_from(D_1)
        D_1[row, col] = 0

        ##  pick out the even and odd conduction states at k+q point and reorganize them
        q_c_even_vecs = q_c_vecs[:, q_c_even_j]
        q_c_oddd_vecs = q_c_vecs[:, q_c_odd_j]
        q_c_even_oddd_vecs = np.hstack([q_c_even_vecs, q_c_oddd_vecs])

        q_c_even_vecs_T = q_c_vecs_T[q_c_even_j]
        q_c_oddd_vecs_T = q_c_vecs_T[q_c_odd_j]
        q_c_even_oddd_vecs_T = np.vstack([q_c_even_vecs_T, q_c_oddd_vecs_T])

        ##  D_2 term calculation
        D_2 = q_c_even_oddd_vecs_T @ q_c_even_oddd_vecs
        row, col = np.diag_indices_from(D_2)
        D_2[row, col] = 0

        ##  D term
        D = D_1 * D_2.T * V_q_mat / self.N_k

        ##  X_1 and X_2 term calculation
        X_1 = k_v_even_oddd_vecs_T @ q_c_even_oddd_vecs
        X_2 = q_c_even_oddd_vecs_T @ k_v_even_oddd_vecs

        ##  X term calculation
        X_1_diag_col = diag(X_1).reshape((-1, 1))
        X_2_diag_row = diag(X_2).reshape((1, -1))
        X = X_1_diag_col @ X_2_diag_row * V_Q / self.N_k

        ##  Exciton Hamiltonian
        H = diag_mat - D + X

        ##  Timer
        t2 = time.perf_counter()
        print("Time of core calculations: (s)", t2 - t1)

        eig_vals, eig_vecs = eig(H)
        t3 = time.perf_counter()
        print("Time of solving a matrix of ", H.shape, " is: ", t3 - t2)
        eig_vals.sort()
        print(eig_vals)

        return H

    # def k_R_list(self, p_density):
    #     list_kp = []
    #     list_R = []
    #     for x1 in linspace(0, 1, p_density):
    #         for x2 in linspace(0, 1, p_density):
    #             list_kp.append(x1 * self.b1 + x2 * self.b2)
    #     for x1 in arange(p_density):
    #         for x2 in arange(p_density):
    #             list_R.append(x1 * self.R1 + x2 * self.R2)
    #     return list_kp, list_R

    def hexagon_shells(self, shell_num=3):
        """
        Get the hexagon shells around zero point.
        """
        # all_lattices = PubMeth.hexagon_around_o_2d(a0_lattice=norm(self.R1), shell_num=shell_num, rot_angle=0)
        # all_lattices = PubMeth.hexagon_around_lattice_2d(a0_lattice=norm(self.R1), shell_num=shell_num)
        # all_lattices = PubMeth.hexagon_around_o_2d(a0_lattice=norm(self.R1), shell_num=shell_num, rot_angle=0)
        # all_lattices = PubMeth.tri_lattice(shell_num, norm(self.R1))
        # all_lattices = PubMeth.diamond_around_o_2d([self.R1, self.R2], shell_num=shell_num)
        all_lattices = PubMeth.diamond_around_lattice_2d(
            [self.R1, self.R2], dots_density=shell_num
        )

        plt.scatter(
            [ele[0] for ele in all_lattices],
            [ele[1] for ele in all_lattices],
            marker=".",
        )
        ax = plt.gca()
        ax.set_aspect("equal")
        ax.set_xlabel("", fontsize=12)
        ax.set_ylabel("", fontsize=12)
        ax.set_title("", fontsize=14)
        plt.xlim(ax.get_xlim())
        plt.ylim(ax.get_ylim())
        plt.savefig(
            data_file_dir + "00_small_test/tri_lats_2.png",
            dpi=330,
            facecolor="w",
            bbox_inches="tight",
            pad_inches=0.1,
        )
        plt.close()

        return array(all_lattices)

    def V_R(self, R_norm_in):
        ##  interaction potential
        func_const = (
            pi * E_CGS**2 * ERG2EV * cm2A / (2 * self.diele_const * self.r0_ratio)
        )  ##  eV

        return func_const * (
            struve(0, R_norm_in / self.r0_ratio) - yn(0, R_norm_in / self.r0_ratio)
        )

    def V_q2(self, q_arr_in, shell_num=151):
        lats_list = self.hexagon_shells(shell_num=shell_num)
        N_cell = len(lats_list)

        if len(array(q_arr_in).shape) == 1:
            phase_arr = q_arr_in @ array(lats_list).T

            e_phase_arr = exp(1j * phase_arr)

            norm_arr = norm(array(lats_list), axis=1)
            print("The most distant vector length: ", max(norm_arr))

            V_R_arr = self.V_R(norm_arr)
            V_R_arr[len(lats_list) // 2] = self.V_R(norm(self.R1))

            output_term = e_phase_arr * V_R_arr

            output_term = output_term.sum()

        elif len(array(q_arr_in).shape) == 2:
            phase_arr = array(q_arr_in) @ array(lats_list).T

            e_phase_arr = exp(1j * phase_arr)

            norm_arr = norm(array(lats_list), axis=1)

            norm_arr = np.kron(ones((len(q_arr_in), 1)), norm_arr)

            V_R_arr = self.V_R(norm_arr)

            V_R_arr[:, len(lats_list) // 2] = self.V_R(norm(self.R1))

            output_term = e_phase_arr * V_R_arr

            output_term = output_term.sum(axis=1)

        print(output_term)

        return output_term  # , N_cell

    def V_q(self, q_arr_in):
        """
        Calculate interaction function in the momentum space (analytically)
        """
        ##  Modulus of q vector
        if len(q_arr_in.shape) == 1:
            q_norm = norm(q_arr_in)
        elif len(q_arr_in.shape) == 2:
            q_norm = norm(q_arr_in, axis=1)

        coeff = 2 * pi * E_CGS**2 * ERG2EV * cm2A / (self.diele_const * q_norm)

        F_q = 1 / (1 + self.r0_ratio * q_norm)

        output_term = coeff * F_q

        return output_term

    def get_unitary_U(self, k_arr):
        """
        Return the Unitary matrix which can diagonalize the Hamiltonian

        # Return
        eig_val, eig_vec

        eig_vec is the matrix, each column of which is one of the eigen vector of the Hamiltonian matrix.
        """
        hamiltonian = self.hamiltonian(k_arr)
        eig_val, eig_vec = eig(hamiltonian)

        sort_arr = np.argsort(real(eig_val))

        eig_val = real(eig_val)[sort_arr]

        eig_vec_T_sort = eig_vec.T[sort_arr]
        eig_vec = eig_vec_T_sort.T

        return eig_val, eig_vec

    def k_mesh(self):
        """
        Set the lattices in momentum space.
        """
        ##  List to contain all the k points
        k_arr_list = []

        ##  Create lattices in momentum space
        if self.k_boundary:
            for ele_m in arange(0, 1, 1 / self.k_mesh_density):
                for ele_n in arange(0, 1, 1 / self.k_mesh_density):
                    ele_k_vec = self.b1 * ele_m + self.b2 * ele_n
                    k_arr_list.append(ele_k_vec)
        else:
            for ele_m in arange(1 / self.k_mesh_density, 1, 1 / self.k_mesh_density):
                for ele_n in arange(
                    1 / self.k_mesh_density, 1, 1 / self.k_mesh_density
                ):
                    ele_k_vec = self.b1 * ele_m + self.b2 * ele_n
                    k_arr_list.append(ele_k_vec)

        return k_arr_list
