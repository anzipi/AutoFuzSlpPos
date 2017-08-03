.. AutoFuzSlpPos documentation master file, created by
   sphinx-quickstart on Mon Jul 31 18:56:46 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to AutoFuzSlpPos
========================

Latest update: July. 31, 2017

AutoFuzSlpPos (short for "**Automated Fuzzy Slope Position**") is
developed by PhD candidate Liang-Jun Zhu and **Prof.** Cheng-Zhi Qin in
Lreis, IGSNRR, CAS, China.


    Contact and support email: zlj@lreis.ac.cn


1. `Introduction <#introduction>`__

2. `Installation <#installation>`__

   -  `2.1 Code structure <#code-structure>`__

   -  `2.2 Compile on Windows <#compile-on-windows-using-msvc>`__

   -  `2.3 Compile on Linux/Unix <#compile-on-linux-unix-using-gcc>`__

   -  `2.4 Configuration <#configuration>`__

2. `Run AutoFuzSlpPos <#run-autofuzslppos>`__

1 Introduction
==============

AutoFuzSlpPos is an automatic approach with only one required input data
(i.e., a gridded DEM of the study area) to deriving fuzzy slope
positions based on the prototype-based inference method proposed by Qin
*et al*. (2009. `Quantification of spatial gradation of slope
positions <http://dx.doi.org/10.1016/j.geomorph.2009.04.003>`__.
Geomorphology 110, 152-161.). AutoFuzSlpPos consists three major parts,
i.e., preparing topographic attributes, extracting typical locations,
and calculating similarity for each slope position. The preliminary
implementation employs the system of five basic slope positions, i.e., ridge, shoulder slope, backslope, footslope, and valley.

Current version of AutoFuzSlpPos is developed under the `TauDEM
parallelized
framework <http://hydrology.usu.edu/taudem/taudem5/index.html>`__ and
programmed using C++ and Python language.

AutoFuzSlpPos is capable with Windows and Linux/Unix, e.g., Windows
7/8/10, CentOS 6.2, and Ubuntu 14.04.

The prerequisites environment is as follows:

-  For users:

   -  **MPI**, such as `Microsoft MS-MPI
      V6 <https://www.microsoft.com/en-us/download/details.aspx?id=47259>`__\ +,
      OpenMPI, MPICH2

   -  Python 2.7.x packaged with Numpy 1.6+ and GDAL 1.9.x.

-  For developers (include the MPI and Python mentioned above):

   -  CMake 2.8.0+

   -  C/C++ compiler with C++11 support, such as Microsoft Visual Studio
      2010+, GCC 4.7+.

2 Installation
==============

If you want to install from source code, please follow `Compile on
Windows <#compile-on-windows-using-msvc>`__ or `Compile on
Linux/Unix <#compile-on-linux-unix-using-gcc>`__. If you want to use
AutoFuzSlpPos directly with the compiled executable files, please refers
to `Configuration <#configuration>`__.

2.1 Code structure
------------------

The source code consists of two parts: 1) the C++ source code located in
``autofuzslppos/src``, and 2) python scripts located in
``autofuzslppos/``.

C++ code will be compiled as separated executable files, such as
"**SelectTypLocSlpPos**" which is used for extracting typical locations
and setting parameters for fuzzy inference of each slope position.

Python script is to organize the whole work-flow with a configurable
script for users’ customizing optional parameters, such as follows.

+-------------------------------+------------------------------------------------------------------------------------------------------+
| Script                        | Functionality                                                                                        |
+===============================+======================================================================================================+
| ``main.py``                   | The entrance of AutoFuzSlpPos                                                                        |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``Config.py``                 | Parse the configuration file (\*.ini) prepared by user.                                              |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``Nomenclature.py``           | Predefined filenames                                                                                 |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``TauDEM.py``                 | Functions based on TauDEM and the extension functions, e.g., SelectTypLocSlpPos                      |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``Util.py``                   | Some fundamental functions, e.g., functions for the Input/Output of raster data                      |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``PreProcessing.py``          | Preprocessing for topographic attributes, such as relative position index (RPI), profile curvature   |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``SelectTypLoc.py``           | Prepare input files for typical location extraction                                                  |
+-------------------------------+------------------------------------------------------------------------------------------------------+
| ``FuzzySlpPosInference.py``   | Prepare input files for fuzzy inference of each slope position                                       |
+-------------------------------+------------------------------------------------------------------------------------------------------+

2.2 Compile on Windows Using MSVC
---------------------------------

The MPI library used for PC is `Microsoft MS-MPI
V6 <https://www.microsoft.com/en-us/download/details.aspx?id=47259>`__
or later. Install msmpisdk.msi, MSMpiSetup.exe. And then set the
environment paths as follows:

.. code:: 

    MSMPI_BIN=C:\Program Files\Microsoft MPI\Bin\
    MSMPI_INC=C:\Program Files (x86)\Microsoft SDKs\MPI\Include\
    MSMPI_LIB32=C:\Program Files (x86)\Microsoft SDKs\MPI\Lib\x86\
    MSMPI_LIB64=C:\Program Files (x86)\Microsoft SDKs\MPI\Lib\x64\

Then, open “\ **Visual Studio Command Prompt**\ ” from Start menu (as
administrator), and run the following commands:

.. code:: 

    cd <path to autofuzslopos>
    mkdir build
    cd build
    # -DARCH: 64 is for compiling 64bit version
    # -DINSTALL_PREFIX: the install directory
    # An example: MSVC 2013, 64bit
    cmake -G "Visual Studio 10 2010 Win64" .. -DARCH=64 -DINSTALL_PREFIX=<INSTALLDIR>
    msbuild.exe ALL_BUILD.vcxproj /p:Configuration=Release /maxcpucount:4
    msbuild.exe INSTALL.vcxproj /p:Configuration=Release

The executable files will be compiled and saved in ``<INSTALLDIR>``.

2.3 Compile on Linux/Unix using GCC
-----------------------------------

Unlike the MPI version for PC, the implementation of
`MPICH <http://www.mpich.org/downloads/>`__ is adopted for Linux/Unix
platform.

The compilation steps are quite familiar:

.. code:: 

    cd <path to autofuzslopos>
    mkdir build
    cd build
    cmake .. -DINSTALL_PREFIX=<INSTALLDIR>
    make -j4
    make install

The executable files will be generated in ``INSTALLDIR``.

2.4 Configuration
-----------------

A script program of Python language is implemented to organize the
work-flow of deriving fuzzy slope positions. User can configure the
environment of AutoFuzSlpPos through the configuration file with the
extension of \*.ini, e.g. ``autofuzslppos/data/Jamaica_windows.ini`` for
Windows and ``autofuzslppos/data/Jamaica_cluster.ini`` for Linux
cluster.

Besides the required path of the DEM of the study area (i.e., rawdem),
the paths of the compiled executable files of AutoFuzSlpPos and
workspace to store the results should be given correctly, for instance:

.. code:: 

    exeDir = /home/zhulj/AutoFuzSlpPos/exec
    rootDir = /home/zhulj/AutoFuzSlpPos/Demo

Note that, if the path of MPI is in the ENVIRONMENT PATH in the system,
the ``mpiexeDir`` could be set as ``None``, otherwise it should be
explicitly assigned, such as ``mpiexeDir = /home/zhulj/mpich/bin``. The
``hostfile`` is used to specify the hosts on which the MPI jobs will be
submitted. If user does not know how to prepare the hostfile, just leave
it as ``hostfile = None``. One possible example is as follows:

.. code:: 

    hostfile = /home/zhulj/AutoFuzSlpPos/exec/dgpm
    dgpm-cluster.public:1
    dgpm-compute-1.local:12
    dgpm-compute-2.local:12
    dgpm-compute-3.local:12
    dgpm-compute-4.local:12

Next, the AutoFuzSlpPos with default parameter settings is ready to run
for the specific study area. Other optional parameters are briefly
introduced in the configuration file (\*.ini).

3 Run AutoFuzSlpPos
===================

Use the following command to run AutoFuzSlpPos:

.. code:: 

    cd <path to AutoFuzSlpPos>
    python -m autofuzslppos/main.py -ini <configuration file path> [-proc <process number> -bin <binaries path> -root <workspace path>]

where: ``<configuration file path>`` is the full path of the \*ini file,
e.g. ``/home/zhulj/AutoFuzSlpPos/data/Jamaica/Jamaica_dgpm.ini``

``<process number>`` is the process number for MPI, which can overwrite
the ``inputProc`` defined in configuration file.

``<binaries path>`` it the executable binaries path of all autofuzslopos functions, which
can overwrite ``exeDir`` the defined in configuration file.

``<workspace path>`` it the workspace path to store the results, which
can overwrite ``rootDir`` the defined in configuration file.

The following table gives a brief introduction to the result files.

+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Result Folder   | Introduction                                                                                                                                                            |
+=================+=========================================================================================================================================================================+
| FuzzySlpPos     | Similarity maps of each slope position, as well as the hardened map of slope positions and the corresponding maximum similarity map                                     |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DinfpreDir      | Intermediate files in preparing topographic attributes                                                                                                                  |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Params          | GRID of topographic attributes, including RPI (Relative Position Index), profile curvature, slope gradient, and HAND (Height Above the Nearest Drainage), by default.   |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Config          | Configuration files of the extraction of typical locations and fuzzy inference for each slope positions                                                                 |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| TypLoc          | Typical locations of each slope positions                                                                                                                               |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Log             | Log files which record information such as runtime, etc.                                                                                                                |
+-----------------+-------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

Note that in the current implementation a system of five basic slope
positions is used, i.e., ridge(RDG), shoulder slope (SHD), backslope
(BKS), footslope (FTS), and valley (VLY).

Configuration
=============
.. toctree::
   :maxdepth: 2

   config.rst



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`