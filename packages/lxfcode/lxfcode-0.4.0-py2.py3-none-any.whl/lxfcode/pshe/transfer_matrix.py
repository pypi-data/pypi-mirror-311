from public.method import *
from public.consts import *
from pshe.optics import FresnelCoeff


class OpticVecs:
    def __init__(self, arr: np.ndarray) -> None:
        self.arr = arr
        pass

    def __mul__(self, vec: Union["OpticVecs", int, float]) -> "OpticVecs":
        if type(vec) == OpticVecs:
            out_vec = self.arr * vec.arr
            return OpticVecs(out_vec)
        elif type(vec) == int or type(vec) == float:
            out_vec = self.arr * vec
            return OpticVecs(out_vec)

    def __add__(self, vec: Union["OpticVecs", int, float]) -> "OpticVecs":
        if type(vec) == OpticVecs:
            out_vec = self.arr + vec.arr
            return OpticVecs(out_vec)
        elif type(vec) == int or type(vec) == float:
            out_vec = self.arr + vec
            return OpticVecs(out_vec)

    def __truediv__(self, vec: Union["OpticVecs", int, float]) -> "OpticVecs":
        if type(vec) == OpticVecs:
            out_vec = self.arr / vec.arr
            return OpticVecs(out_vec)
        elif type(vec) == int or type(vec) == float:
            out_vec = self.arr / vec
            return OpticVecs(out_vec)

    def __rtruediv__(self, vec: Union["OpticVecs", int, float]) -> "OpticVecs":
        if type(vec) == OpticVecs:
            out_vec = vec.arr / self.arr
            return OpticVecs(out_vec)
        elif type(vec) == int or type(vec) == float:
            out_vec = vec / self.arr
            return OpticVecs(out_vec)


class Layer:
    """
    # Notes
    If you want to add multiple layers, you should make sure that the refractive indexes are of the same length (and of course, the refractive indexes should on the same wavelength range).
    """

    def __init__(
        self, thickness: float, wls: "np.ndarray", n_arr: "np.ndarray"
    ) -> None:
        self.d = thickness
        self.wls = wls
        self.n = n_arr


class Structure:
    def __init__(self, layers_list: list["Layer"]) -> None:
        self.layers_list = layers_list
        pass

    def phase_factors(self, theta0: float) -> list:
        """
        Phase term while traveling in the Layer of medium
        """
        phase_mat_list = []
        for ele_layer in self.layers_list:
            delta = 2 * pi * ele_layer.n * ele_layer.d * cos(theta0) / ele_layer.wls
            delta_vec_p = OpticVecs(exp(1j * delta))
            delta_vec_m = OpticVecs(exp(-1j * delta))
            phase_mat = np.array([[delta_vec_p, 0], [0, delta_vec_m]])
            phase_mat_list.append(phase_mat)

        return phase_mat_list

    def reflection_coeffs(self, kind: Literal["s", "p"], theta0: float):
        ref_coeff_mat_list = []
        for ele_i in range(len(self.layers_list) - 1):
            l1 = self.layers_list[ele_i]
            l2 = self.layers_list[ele_i + 1]
            tmp_fc = FresnelCoeff(theta0, l1.n, l2.n)
            r_s, r_p, t_s, t_p = tmp_fc.original_coefficient()
            if kind == "s":
                mat = np.array([[1, OpticVecs(r_s)], [OpticVecs(r_s), 1]]) / OpticVecs(
                    t_s
                )
                ref_coeff_mat_list.append(mat)
            elif kind == "p":
                mat = np.array([[1, OpticVecs(r_p)], [OpticVecs(r_p), 1]]) / OpticVecs(
                    t_p
                )
                ref_coeff_mat_list.append(mat)
        return ref_coeff_mat_list

    def transfer_mat(self, kind: Literal["s", "p"], theta0) -> np.ndarray:
        phase_mats = self.phase_factors(theta0)
        ref_coeff_mats = self.reflection_coeffs(kind, theta0)
        out_result = np.eye(2)
        for ele_i in range(len(phase_mats)):
            out_result = out_result @ phase_mats[ele_i] @ ref_coeff_mats[ele_i]
        return out_result


def main():
    mos2_layer = Layer()
    air_layer = Layer(0)
    v1 = OpticVecs(array([1, 3, 2]))
    v2 = OpticVecs(array([1, 2, 4]))
    v3 = OpticVecs(array([4, 8, 1]))
    v4 = OpticVecs(array([2, 0, 9]))
    m1 = array([[v1, v2], [v3, v4]])
    m2 = array([[v2, v1], [v3, v4]])
    return


if __name__ == "__main__":
    main()
