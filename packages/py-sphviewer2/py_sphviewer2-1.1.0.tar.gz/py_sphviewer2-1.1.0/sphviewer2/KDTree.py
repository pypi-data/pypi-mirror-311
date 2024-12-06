###############################################################################
#                     Py-SPHViewer2 - KDTree NN library                       #
#                                                                             #
# This Python module provides an interface for rendering images based on      #
# Smoothed Particle Hydrodynamics (SPH) data using the private `smeshl`       #
# library. The shared library is proprietary and was developed by Alejandro   #
# Benitez-Llambay. It is not publicly available and must be obtained          #
# from the link provided                                                      #
#                                                                             #
# Author: Alejandro Benitez-Llambay                                           #
# Email: alejandro.benitezllambay@unimib.it                                   #
# License: Private                                                            #
#                                                                             #
# This wrapper provides a Python interface to the `smeshl` library, which     #
# must be compiled for your operating system (macOS/Linux). Ensure that the   #
# appropriate shared library (.dylib/.so) is present in your system path.     #
#                                                                             #
# DISCLAIMER:                                                                 #
# This software is provided "as is", without any warranty of any kind, either #
# expressed or implied, including but not limited to the warranties of        #
# merchantability, fitness for a particular purpose, and non-infringement.    #
# In no event shall the author be liable for any claim, damages, or other     #
# liability, whether in an action of contract, tort, or otherwise, arising    #
# from, out of, or in connection with the software or the use or other        #
# dealings in the software.                                                   #
#                                                                             #
# Users should NOT distribute this software, in whole or in part,             #
# without prior written permission from the author.                           #
###############################################################################


import ctypes as _ctypes
import numpy as _np
import platform as _platform

class KDTree:

    def __init__(self):
        """
        Initializes the KDTree instance and loads the shared C library.
        Determines the platform-specific shared library extension and loads the corresponding shared library.

        Raises:
            OSError: If the operating system is unsupported or the shared library cannot be loaded.
        """

        library_name = "libsmeshl"
        file_extension = self._get_shared_library_extension()

        # Construct the library file path
        library_file = f"{library_name}{file_extension}"

        # Load the shared library
        try:
            self.lib = _ctypes.CDLL(library_file)
        except OSError as e:
            raise OSError(f"Failed to load the library: {library_file}") from e

        # Define the KDTreeNode structure in Python
        class KDTreeNode(_ctypes.Structure):
            _fields_ = [("point", _ctypes.c_float * 3),
                        ("left", _ctypes.POINTER(_ctypes.c_void_p)),
                        ("right", _ctypes.POINTER(_ctypes.c_void_p))]

        # Set up the function argument types and return types for the C functions
        self.lib.build_kd_tree.argtypes = [_ctypes.POINTER(_ctypes.c_float), _ctypes.c_int, _ctypes.c_int]
        self.lib.build_kd_tree.restype = _ctypes.POINTER(KDTreeNode)

        self.lib.get_smoothing_length_parallel.argtypes = [_ctypes.POINTER(KDTreeNode),
                                            _ctypes.POINTER(_ctypes.c_float),
                                            _ctypes.POINTER(_ctypes.c_float),
                                            _ctypes.POINTER(_ctypes.c_float),
                                            _ctypes.POINTER(_ctypes.c_float),
                                            _ctypes.c_uint64, _ctypes.c_int, _ctypes.c_int]
        self.lib.get_smoothing_length_parallel.restype = None

       
    def build_tree(self, points):
        """
            Constructs a KDTree from a given set of 3D points.

            This function takes a set of 3D points and builds a KDTree, 
            a space-partitioning data structure for organizing points in a k-dimensional space. 
            The KDTree enables efficient spatial queries like nearest neighbor search.

            Parameters
            ----------
            points : numpy.ndarray
                A 2D NumPy array of shape (N, 3), where N is the number of points, 
                and each point is represented as a 3D coordinate (x, y, z). 

            Raises
            ------
            ValueError
                If the input `points` array does not have 3 columns (i.e., is not of shape (N, 3)),
                a ValueError is raised with the message "Points array must be of shape (N, 3)".

            Attributes
            ----------
            points : numpy.ndarray
                Stores the input points after validation.
                
            root : ctypes object
                Represents the root node of the KDTree, returned by the C function 
                `self.lib.build_kd_tree()`.
            """            
        self.points = points

        if self.points.shape[1] != 3:
            raise ValueError("Points array must be of shape (N, 3)")

        num_points = self.points.shape[0]
        depth = 0

        # Convert points to a flat ctypes array
        points_flat = points.astype(_np.float32).flatten()
        points_ctypes = points_flat.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))

        # Build the KDTree by calling the C function
        self.root = self.lib.build_kd_tree(points_ctypes, num_points, depth)

    def get_smoothing_lengths(self, N, Nthreads=4):
        """
        Calculate smoothing lengths for the points in the KDTree.

        This function computes smoothing lengths for each point in the KDTree. 
        Smoothing lengths are typically used in simulations involving particle-based methods 
        (e.g., smoothed particle hydrodynamics) to determine interaction radii.

        Parameters
        ----------
        N : int
        The number of nearest neighbors to consider when calculating the smoothing lengths 
        for each point. This influences the size of the smoothing kernel.

        Nthreads : int, optional, default=4
        The number of threads to use for parallel computation. 
        This allows the function to compute smoothing lengths more efficiently by distributing 
        the workload across multiple threads.

        Returns
        -------
        h : numpy.ndarray
        A 1D NumPy array  containing the computed smoothing lengths for each point. 
        The returned array has the same order as the input points, where `h[i]` corresponds to 
        the smoothing length for the i-th point.
        """
        
        Npart = len(self.points)

        # Convert the x, y, z, and h arrays to ctypes
        x_ctypes = self.points[:,0].astype(_np.float32).ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))
        y_ctypes = self.points[:,1].astype(_np.float32).ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))
        z_ctypes = self.points[:,2].astype(_np.float32).ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))

        # Allocate memory for the output smoothing lengths (h array)
        h = _np.zeros(Npart, dtype=_np.float32)
        h_ctypes = h.ctypes.data_as(_ctypes.POINTER(_ctypes.c_float))

        # Call the C function get_smoothing_length
        self.lib.get_smoothing_length_parallel(self.root, x_ctypes, y_ctypes, z_ctypes, h_ctypes, Npart, N, Nthreads)

        return h

    def _get_shared_library_extension(self):
        """
        Returns the platform-specific extension for shared libraries.

        Returns:
            str: The file extension for the shared library (e.g., '.dylib' for macOS, '.so' for Linux).

        Raises:
            OSError: If the operating system is unsupported.
        """
        current_os = _platform.system()
        
        if current_os == 'Darwin':  # macOS
            return '.dylib'
        elif current_os == 'Linux':
            return '.so'
        else:
            raise OSError(f"Unsupported operating system: {current_os}")
0