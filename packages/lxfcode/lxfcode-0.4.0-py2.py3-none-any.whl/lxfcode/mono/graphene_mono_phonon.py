from public.consts import *
from public.method import *


class SingleLayerGraPhonon:


    class CarbonAtom:

        def __init__(self, position_arr, atom_type) -> None:
            self.position_arr = position_arr
            self.atom_type = atom_type
            self.dist_from_center_atom = 0
            self.force_const_tensor = 0
            

        def get_Dij_times_phase(self, k_arr):
            if isinstance(self.force_const_tensor, int) and self.force_const_tensor == 0:
                print("Warning! The force constant is zero!!!")
            return self.force_const_tensor * exp(-1j * k_arr @ self.dist_from_center_atom[:2])
            
    d = 1.42  # A
    sublattice_A = CarbonAtom(array([0, 0]), atom_type='A')
    sublattice_B = CarbonAtom(array([d, 0]), atom_type='B')
    
    a1_arr = sqrt(3) * d * array([sqrt(3) / 2, 1 / 2])
    a2_arr = sqrt(3) * d * array([-sqrt(3) / 2, 1 / 2])
    b1_arr = 4 * pi / (3 * d) * array([1 / 2, sqrt(3) / 2])
    b2_arr = 4 * pi / (3 * d) * array([-1 / 2, sqrt(3) / 2])
    
    K_t_arr = array([sqrt(3) / 2, 1 / 2]) * norm(b1_arr) / sqrt(3)
    K_b_arr = array([sqrt(3) / 2, -1 / 2]) * norm(b1_arr) / sqrt(3)
    M_arr = (K_t_arr + K_b_arr) / 2
    Gamma_arr = array([0, 0])

    density_per_path = 100 / norm(K_t_arr)

    def __init__(self, coup_pars_list=[
        [36.5, 24.5, 9.82],   # *10^4 dyn/cm
        [8.80, -3.23, -0.40],     # *10^4 dyn/cm
        [3.00, -5.25, 0.15],    # *10^4 dyn/cm
        [-1.92, 2.29, -0.58]],     # *10^4 dyn/cm
        long_axes_horizontal=True) -> None:
        self.neighbor_coup_mats_list = []
        for ele_pars_list in coup_pars_list:
            self.neighbor_coup_mats_list.append(diag(ele_pars_list))
        self.neighbor_shell_num = len(coup_pars_list)
        self.long_axes_horizontal = long_axes_horizontal
        self.lattices, self.atoms_list = self.atom_list()
        self.neighbor_radius_list, self.A_neighbors_dict_sort_by_AB, self.B_neighbors_dict_sort_by_AB = self.neighbors_AB()

        self.force_const_tensor_sum_for_A = sum([ele_atom.force_const_tensor for ele_atom in list(itertools.chain.from_iterable(list(self.A_neighbors_dict_sort_by_AB.values())))])
        self.force_const_tensor_sum_for_B = sum([ele_atom.force_const_tensor for ele_atom in list(itertools.chain.from_iterable(list(self.B_neighbors_dict_sort_by_AB.values())))])
        self.mat_type = 'Single Layer Graphene'
    
    def latt_stru(self):
        if self.long_axes_horizontal:
            lattice_A = PubMeth.tri_lattice(self.neighbor_shell_num, sqrt(3) * self.d, 30)
            lattice_B = PubMeth.tri_lattice(self.neighbor_shell_num, sqrt(3) * self.d, 30, array([self.d, 0]))
        else:
            lattice_A = PubMeth.tri_lattice(self.neighbor_shell_num, sqrt(3) * self.d, 0)
            lattice_B = PubMeth.tri_lattice(self.neighbor_shell_num, sqrt(3) * self.d, 0, array([0, self.d]))
        lattice = lattice_A + lattice_B
        return lattice

    def atom_list(self): # the second is the list of atoms
        lattice_A = PubMeth.tri_lattice(self.neighbor_shell_num, sqrt(3) * self.d, 30)
        lattice_B = PubMeth.tri_lattice(self.neighbor_shell_num, sqrt(3) * self.d, 30, array([self.d, 0]))
        lattice_list = self.latt_stru()
        atom_list = []
        for ele_arr in lattice_A:
            atom_list.append(self.CarbonAtom(ele_arr, 'A'))
        for ele_arr in lattice_B:
            atom_list.append(self.CarbonAtom(ele_arr, 'B'))
        return lattice_list, atom_list

    def sort_neighbors(self, center_atom_pos_arr):
        lattice_list, atom_list = self.atom_list()
        dist_arr_list = array(lattice_list) - center_atom_pos_arr
        dist_arr_norm_list = norm(dist_arr_list, axis=1)
        dist_arr_norm_list.sort()
        neighbor_radius_list = PubMeth.list2set_within_diff(dist_arr_norm_list)[1:self.neighbor_shell_num+1]

        neighbor_dict = {}
        for radius_i in range(len(neighbor_radius_list)):
            chosen_radius = neighbor_radius_list[radius_i]
            neighbor_dict[chosen_radius] = list(array(atom_list)[abs(norm(dist_arr_list, axis=1) - chosen_radius) < 0.001])

        # give the distance vector to every atom
        for radius_index in range(len(neighbor_radius_list)):
            for ele_atom in neighbor_dict[neighbor_radius_list[radius_index]]:
                ele_atom.dist_from_center_atom = ele_atom.position_arr - center_atom_pos_arr
                tmp_dir_angle = PubMeth.get_angle_to_x_axis(ele_atom.dist_from_center_atom)
                ele_atom.force_const_tensor = PubMeth.rotation_3d_to_2d(tmp_dir_angle) @ self.neighbor_coup_mats_list[radius_index] @ np.linalg.inv(PubMeth.rotation_3d_to_2d(tmp_dir_angle))
                ele_atom.neighbor_index = radius_index
        
        return neighbor_radius_list, neighbor_dict
        
    def neighbors_AB(self):
        neighbor_radius_list, neighbors_of_A = self.sort_neighbors(self.sublattice_A.position_arr)
        neighbors_of_B = self.sort_neighbors(self.sublattice_B.position_arr)[1]

        neighbors_of_A_sort_atom_type = {}
        neighbors_of_A_sort_atom_type[self.sublattice_A.atom_type] = [ele_atom for ele_atom in itertools.chain.from_iterable(list(neighbors_of_A.values())) if ele_atom.atom_type == self.sublattice_A.atom_type]
        neighbors_of_A_sort_atom_type[self.sublattice_B.atom_type] = [ele_atom for ele_atom in itertools.chain.from_iterable(list(neighbors_of_A.values())) if ele_atom.atom_type == self.sublattice_B.atom_type]

        neighbors_of_B_sort_atom_type = {}
        neighbors_of_B_sort_atom_type[self.sublattice_A.atom_type] = [ele_atom for ele_atom in itertools.chain.from_iterable(list(neighbors_of_B.values())) if ele_atom.atom_type == self.sublattice_A.atom_type]
        neighbors_of_B_sort_atom_type[self.sublattice_B.atom_type] = [ele_atom for ele_atom in itertools.chain.from_iterable(list(neighbors_of_B.values())) if ele_atom.atom_type == self.sublattice_B.atom_type]

        return neighbor_radius_list, neighbors_of_A_sort_atom_type, neighbors_of_B_sort_atom_type
    
    def get_matrix(self, k_arr):
        ## AA term
        AA_tensor_sum = sum([ele_atom.get_Dij_times_phase(k_arr) for ele_atom in self.A_neighbors_dict_sort_by_AB['A']])

        ## AB term
        AB_tensor_sum = sum([ele_atom.get_Dij_times_phase(k_arr) for ele_atom in self.A_neighbors_dict_sort_by_AB['B']])

        ## BA term
        BA_tensor_sum = sum([ele_atom.get_Dij_times_phase(k_arr) for ele_atom in self.B_neighbors_dict_sort_by_AB['A']])

        ## BB term
        BB_tensor_sum = sum([ele_atom.get_Dij_times_phase(k_arr) for ele_atom in self.B_neighbors_dict_sort_by_AB['B']])

        print(AA_tensor_sum)

        mat = block([
            [-AA_tensor_sum + self.force_const_tensor_sum_for_A, -AB_tensor_sum],
            [-BA_tensor_sum, -BB_tensor_sum + self.force_const_tensor_sum_for_B]
        ])

        return mat

        # # k空间路径描述
    def path_depiction(
            self,
            i,
            point1,
            point2,
            out_list,
            multi_process='off',
            include_last_k=True,
            hint=False):
        k_along = PubMeth.path_between_two_vec(point1, point2, density=int(norm(point1 - point2) * self.density_per_path), include_last=include_last_k)
        if multi_process == 'on':
            value_list = []
            for kp in k_along:
                eig_v_f= np.linalg.eig(
                    self.get_matrix(kp))[0]
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
            number_of_points = int(self.density_per_path *
                                   sqrt((path_list[ii +
                                                   1][1] -
                                         path_list[ii][1]) ** 2 +
                                        (path_list[ii +
                                                   1][0] -
                                         path_list[ii][0]) ** 2))
            next_pos = pos_list[-1] + number_of_points
            pos_list.append(next_pos)
        return pos_list

    # # 多进程计算k空间路径能带，每条路径一个核计算
    def multi_proc_path(self, kp_path_list, x_labs=[], save_fig_or_not=True, save_npy_or_not=False, figsize=(7,5), hint=False,title_font_size=14, label_font_size=12, tick_font_size=10, include_last_k=True, save_npy_dir_name='phonon_data', save_fig_dir_name='phonon', save_npy_title=''):

        phonon_title = 'phonon_neighbor_{}'.format(self.neighbor_shell_num)
        npy_file = PubMeth.get_right_save_path_and_create(save_npy_dir_name,  data_files_or_not=True) + phonon_title + '.npy'
        PubMeth.title_font_size = title_font_size
        PubMeth.label_font_size = label_font_size
        PubMeth.tick_font_size = tick_font_size
        x_label_pos = PubMeth.situate_x_labels(kp_path_list, self.density_per_path)
        
        print('The file name is: ', npy_file)

        if os.path.exists(npy_file):
            print("Using the existing data...")
            total_phonon_list = np.load(npy_file)
        else:
            out_eig_phonon_list_f = multiprocessing.Manager().list()
            path_num = len(kp_path_list) - 1
            p_f = Pool(path_num)
            path_depiction = functools.partial(self.path_depiction, hint=hint)

            # core process code
            for i in range(path_num-1):
                p_f.apply_async(path_depiction, args=(
                    i, kp_path_list[i], kp_path_list[i + 1], out_eig_phonon_list_f, 'on'))
            p_f.apply_async(path_depiction, args=(
                    path_num-1, kp_path_list[path_num-1], kp_path_list[path_num], out_eig_phonon_list_f, 'on', include_last_k))
            print('Waiting for all subprocesses done...')
            p_f.close()
            p_f.join()
            print('All subprocesses done.')
            
            total_phonon_list = []
            for path_i in range(path_num):
                for ele_path in out_eig_phonon_list_f:
                    if ele_path[-1] == path_i:
                        total_phonon_list.extend(ele_path[0:-1])

        phonon_list = sqrt(array(total_phonon_list) / (12 * amu)) / (c_speed * m2cm) / 2

        figure_title = r"Phonon Dispersion for {}".format(self.mat_type)
        if save_npy_title == '':
            save_npy_title = 'phonon_neighbor_{}'.format(self.neighbor_shell_num)
        else:
            pass
        PubMeth.plot_energies(real(phonon_list), figuretitle=figure_title, x_label_pos=x_label_pos, x_labs=x_labs, save_fig_or_not=save_fig_or_not, save_fig_npy_title=save_npy_title, fig_size=figsize, save_fig_dir_name=save_fig_dir_name, save_npy_or_not=save_npy_or_not, save_npy_dir_name=save_npy_dir_name, fig_format='.png', y_label=r'$\omega$(cm$^{-1}$)', y_ticks=[0, 500, 1000, 1500], y_range=[0, 1700])
        