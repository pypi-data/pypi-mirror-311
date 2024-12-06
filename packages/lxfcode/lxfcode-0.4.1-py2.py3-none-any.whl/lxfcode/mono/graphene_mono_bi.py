from public.consts import *
from public.method import *


class SingleLayerGra:
    
    def h(self, k_arr):
        kx = k_arr[0]
        ky = k_arr[1]
        return array([
            [0, kx - 1j * ky],
            [kx + 1j * ky, 0]
        ])

    def band_demo(self):
        arr_list = PubMeth.path_between_two_vec(array([-1, 0]), array([1, 0]))
        e_list = []
        for ele_arr in arr_list:
            eigen_values, eigen_vectors = np.linalg.eig(self.h(ele_arr))
            eigen_values.sort()
            e_list.append(eigen_values)
        # fig, ax = plt.subplots()
        # ax.plot(array(e_list)[:, [0]], c='b')
        # ax.plot(array(e_list)[:, [1]], c='r')
        # fig.savefig('test_bilayer.png', dpi=330)
        # plt.close()
        return e_list


class BilayerGra:
    t_inter = 330  # meV
    t = 2970  # meV
    d = 1.42  # A
    a = sqrt(3) * d
    K_valley_arr = array([(4 * pi) / (3 * a), 0])
    M_arr = array([1, 1 / sqrt(3)]) * pi / a
    M_2_arr = PubMeth.rotation(-60) @ M_arr

    def __init__(self) -> None:
        pass

    def eigen_energies(self, k_arr):
        kx = k_arr[0]
        ky = k_arr[1]
        E1 = self.t * sqrt(
            (self.t_inter / (2 * self.t)) ** 2
            + 4 * cos(sqrt(3) / 2 * self.d * kx) * cos(3 / 2 * self.d * ky)
            + 2 * cos(sqrt(3) * self.d * kx)
            + 3
        ) + self.t_inter / 2
        E2 = self.t * sqrt(
            (self.t_inter / (2 * self.t)) ** 2
            + 4 * cos(sqrt(3) / 2 * self.d * kx) * cos(3 / 2 * self.d * ky)
            + 2 * cos(sqrt(3) * self.d * kx)
            + 3
        ) - self.t_inter / 2
        E3 = -self.t * sqrt(
            (self.t_inter / (2 * self.t)) ** 2
            + 4 * cos(sqrt(3) / 2 * self.d * kx) * cos(3 / 2 * self.d * ky)
            + 2 * cos(sqrt(3) * self.d * kx)
            + 3
        ) + self.t_inter / 2
        E4 = -self.t * sqrt(
            (self.t_inter / (2 * self.t)) ** 2
            + 4 * cos(sqrt(3) / 2 * self.d * kx) * cos(3 / 2 * self.d * ky)
            + 2 * cos(sqrt(3) * self.d * kx)
            + 3
        ) - self.t_inter / 2

        E_list = [E1, E2, E3, E4]
        E_list.sort()
        return E_list
    
    def band_demo(self):
        arr1_list = PubMeth.path_between_two_vec(self.M_arr, self.K_valley_arr)
        arr2_list = PubMeth.path_between_two_vec(self.K_valley_arr, self.M_2_arr)
        arr1_list = PubMeth.path_between_two_vec(self.K_valley_arr + (self.M_arr - self.K_valley_arr) / 5, self.K_valley_arr)
        arr2_list = PubMeth.path_between_two_vec(self.K_valley_arr, self.K_valley_arr + (self.M_2_arr - self.K_valley_arr) / 5)
        arr_list = []
        arr_list.extend(arr1_list)
        arr_list.extend(arr2_list)
        e_list = []
        for ele_arr in arr_list:
            e_list.append(self.eigen_energies(ele_arr))
        
        # fig, ax = plt.subplots()
        # ax.plot(array(e_list)[:, [0, 3]], c='r')
        # ax.plot(array(e_list)[:, [1, 2]], c='b')
        # fig.savefig('test_bilayer.png', dpi=330)
        # plt.close()
        return e_list
