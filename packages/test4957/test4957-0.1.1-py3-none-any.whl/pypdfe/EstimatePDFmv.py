"""
The python version of estimatePDFmv should be imported with the command 'from pypdfe import estimatePDFmv'.
----------------------
Written by Nate Mauney
"""
import ctypes as ct
import numpy as np
import os


# create the shared library with name:
shared_lib_name = 'PDFe'


class EstimatePDFmv:
    """
    A wrapper "function" for estimatePDFmv.
    Objects of this class should not be instantiated directly.
    """

    _shared_lib_name = None
    __shared_lib = None
    min_samples = 100
    uv_bounds = [200, 1500]  # univariate upper bound on output_length
    mv_bounds = [3, 100]  # multivariate bounds on output_length

    def __init__(self, shared_lib_name):
        """
        Constructs the necessary attributes for the estimatePDFmv function.
        :param shared_lib_name: the name that the shared library should be created with
        """
        self._shared_lib_name = os.path.dirname(__file__) + os.sep + shared_lib_name
        self.__get_shared_lib()

    def __get_shared_lib(self, fresh_recompile=False):
        """
        Compiles the shared library if needed, then loads it into the function.
        :return: None
        """
        # compile shared library if not done so already
        if fresh_recompile:
            self.__shared_lib = ct.CDLL(f'{self._shared_lib_name}.so', winmode=0)
        else:
            try:
                self.__shared_lib = ct.CDLL(f'{self._shared_lib_name}.so', winmode=0)
            except OSError:
                self.recompile()

    def recompile(self):
        """
        Recompiles the shared library and reloads it into the function.
        :return: None
        """
        cpp_files_folder = os.path.dirname(self._shared_lib_name) + os.sep + 'PDF-Estimator'
        os.system(f'g++ -shared -o {self._shared_lib_name}.so {cpp_files_folder}{os.sep}*.cpp')
        self.__get_shared_lib(True)

    def __call__(self, distribution, output_length=None, debug=0):
        """
        Estimate the PDF of a univariate or multivariate distribution.
            Each row is assumed to be a sample.

        :param distribution: np.array
        :param distribution_length: int
        :param num_variables: int
        :param output_length: int
        :return: [x: np.array, pdf: np.array]
        """
        num_samples = distribution.shape[0]
        try:
            num_variables = distribution.shape[1]
        except IndexError:
            num_variables = 1

        if output_length is None:
            if num_variables == 1:
                output_length = min(int(self.uv_bounds[0] + num_samples/200), self.uv_bounds[1])
            if num_variables > 1:
                output_length = int((num_samples / self.min_samples) ** (1 / (num_variables - 1)) + 1)
                output_length = max(min(output_length, self.mv_bounds[1]), self.mv_bounds[0])

        # define C pointers
        distribution_p = distribution.astype(float).ctypes.data_as(ct.POINTER(ct.c_double))
        n_samples_p = ct.pointer(ct.c_int(num_samples))
        n_variables_p = ct.pointer(ct.c_int(num_variables))
        output_length_p = ct.pointer(ct.c_int(output_length))
        debug_p = ct.pointer(ct.c_int(debug))

        # preallocate outputs
        out_shape = [output_length for _ in range(num_variables)]
        x_pointer = np.zeros([num_variables, output_length]).astype(float).ctypes.data_as(ct.POINTER(ct.c_double))
        pdf_pointer = np.zeros(out_shape).astype(float).ctypes.data_as(ct.POINTER(ct.c_double))

        self.__shared_lib.estimatePDFmv(distribution_p, n_samples_p, n_variables_p, output_length_p, debug_p,
                                        x_pointer, pdf_pointer)

        # convert outputs to numpy arrays
        vars = np.ctypeslib.as_array(x_pointer, shape=[num_variables, output_length])
        x = [var for var in vars]
        if len(x) == 1:
            x = x[0]
        pdf = np.ctypeslib.as_array(pdf_pointer, shape=out_shape)

        return [x, pdf]


# build estimatePDFmv function
estimatePDFmv = EstimatePDFmv(shared_lib_name)
