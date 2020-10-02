# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load in 

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# TensorFlow Bazel configuration file.
# This file tries to group and simplify build options for TensorFlow
#
# ----CONFIG OPTIONS----
# Android options:
#    android:
#    android_arm:
#    android_x86:
#    android_x86_64:
#
# iOS options:
#     ios:
#     ios_armv7:
#     ios_arm64:
#     ios_i386:
#     ios_x86_64:
#     ios_fat:
#
# Compiler options:
#     cuda_clang:             Use clang when building CUDA code.
#     c++17:                  Build with C++17 options
#     c++1z:                  Build with C++17 options
#     avx_linux:              Build with avx instruction set on linux.
#     avx2_linux:             Build with avx2 instruction set on linux.
#     native_arch_linux:      Build with instruction sets available to the host machine on linux
#     avx_win:                Build with avx instruction set on windows
#     avx2_win:               Build with avx2 instruction set on windows
#
# Other build options:
#     short_logs:       Only log errors during build, skip warnings.
#     monolithic:       Build all TF C++ code into a single shared object.
#     dynamic_kernels:  Try to link all kernels dynamically (experimental).
#
#
# TF version options;
#     v1: Build TF V1 (without contrib)
#     v2: Build TF v2
#
# Feature and Third party library support options:
#     xla:          Build TF with XLA
#     using_cuda:   CUDA is available to build system.
#     cuda:         Build with full cuda support.
#     rocm:         Build with AMD GPU support (rocm).
#     sycl:         Build with SYCL support.
#     sycl_nodouble:
#     sycl_asan:
#     sycl_trisycl:
#     mkl:          Enable full mkl support.
#     tensorrt:     Enable Tensorrt support.
#     ngraph:       Enable ngraph support.
#     numa:         Enable numa using hwloc.
#     noaws:        Disable AWS S3 storage support
#     nogcp:        Disable GCS support.
#     nohdfs:       Disable hadoop hdfs support.
#     nonccl:       Disable nccl support.
#
#
# Remote build execution options (only configured to work with TF team projects for now.)
#     rbe:        General RBE options shared by all flavors.
#     rbe_linux:  General RBE options used on all linux builds.
#     rbe_win:    General RBE options used on all windows builds.
#
#     rbe_cpu_linux:        RBE options to build with only CPU support.
#     rbe_linux_cuda_nvcc:  RBE options to build with GPU support using nvcc.
#     rbe_gpu_linux:        An alias for rbe_linux_cuda_nvcc
#
#     rbe_linux_py2: Linux Python 2 RBE config.
#     rbe_linux_py3: Linux Python 3 RBE config
#
#     rbe_win_py37: Windows Python 3.7 RBE config
#     rbe_win_py38: Windows Python 3.8 RBE config
#
#     tensorflow_testing_rbe_linux: RBE options to use RBE with tensorflow-testing project on linux
#     tensorflow_testing_rbe_win:   RBE options to use RBE with tensorflow-testing project on windows
#
# Embedded Linux options (experimental and only tested with TFLite build yet)
#     elinux:          General Embedded Linux options shared by all flavors.
#     elinux_aarch64:  Embedded Linux options for aarch64 (ARM64) CPU support.
#     elinux_armhf:    Embedded Linux options for armhf (ARMv7) CPU support.



# Android configs. Bazel needs to have --cpu and --fat_apk_cpu both set to the
# target CPU to build transient dependencies correctly. See
# https://docs.bazel.build/versions/master/user-manual.html#flag--fat_apk_cpu
build:android --crosstool_top=//external:android/crosstool
build:android --host_crosstool_top=@bazel_tools//tools/cpp:toolchain
build:android_arm --config=android
build:android_arm --cpu=armeabi-v7a
build:android_arm --fat_apk_cpu=armeabi-v7a
build:android_arm64 --config=android
build:android_arm64 --cpu=arm64-v8a
build:android_arm64 --fat_apk_cpu=arm64-v8a
build:android_x86 --config=android
build:android_x86 --cpu=x86
build:android_x86 --fat_apk_cpu=x86
build:android_x86_64 --config=android
build:android_x86_64 --cpu=x86_64
build:android_x86_64 --fat_apk_cpu=x86_64

# Sets the default Apple platform to macOS.
build --apple_platform_type=macos

# iOS configs for each architecture and the fat binary builds.
build:ios --apple_platform_type=ios
build:ios --apple_bitcode=embedded --copt=-fembed-bitcode
build:ios --copt=-Wno-c++11-narrowing
build:ios_armv7 --config=ios
build:ios_armv7 --cpu=ios_armv7
build:ios_arm64 --config=ios
build:ios_arm64 --cpu=ios_arm64
build:ios_i386 --config=ios
build:ios_i386 --cpu=ios_i386
build:ios_x86_64 --config=ios
build:ios_x86_64 --cpu=ios_x86_64
build:ios_fat --config=ios
build:ios_fat --ios_multi_cpus=armv7,arm64,i386,x86_64

# Config to use a mostly-static build and disable modular op registration
# support (this will revert to loading TensorFlow with RTLD_GLOBAL in Python).
# By default, TensorFlow will build with a dependence on
# //tensorflow:libtensorflow_framework.so.
build:monolithic --define framework_shared_object=false

# For projects which use TensorFlow as part of a Bazel build process, putting
# nothing in a bazelrc will default to a monolithic build. The following line
# opts in to modular op registration support by default.
build --define framework_shared_object=true

# Flags for open source build, always set to be true.
build --define open_source_build=true
test --define open_source_build=true

# For workaround https://github.com/bazelbuild/bazel/issues/8772 with Bazel >= 0.29.1
build --java_toolchain=//third_party/toolchains/java:tf_java_toolchain
build --host_java_toolchain=//third_party/toolchains/java:tf_java_toolchain

# Please note that MKL on MacOS or windows is still not supported.
# If you would like to use a local MKL instead of downloading, please set the
# environment variable "TF_MKL_ROOT" every time before build.
build:mkl --define=build_with_mkl=true --define=enable_mkl=true
build:mkl --define=tensorflow_mkldnn_contraction_kernel=0
build:mkl --define=build_with_mkl_dnn_v1_only=true
build:mkl -c opt

# This config refers to building with CUDA available. It does not necessarily
# mean that we build CUDA op kernels.
build:using_cuda --define=using_cuda=true
build:using_cuda --action_env TF_NEED_CUDA=1
build:using_cuda --crosstool_top=@local_config_cuda//crosstool:toolchain

# This config refers to building CUDA op kernels with nvcc.
build:cuda --config=using_cuda
build:cuda --define=using_cuda_nvcc=true

# This config refers to building CUDA op kernels with clang.
build:cuda_clang --config=using_cuda
build:cuda_clang --define=using_cuda_clang=true
build:cuda_clang --define=using_clang=true
build:cuda_clang --action_env TF_CUDA_CLANG=1

# dbg config, as a shorthand for '--config=opt -c dbg'
build:dbg --config=opt -c dbg
# for now, disable arm_neon. see: https://github.com/tensorflow/tensorflow/issues/33360
build:dbg --cxxopt -DTF_LITE_DISABLE_X86_NEON

build:tensorrt --action_env TF_NEED_TENSORRT=1

build:rocm --crosstool_top=@local_config_rocm//crosstool:toolchain
build:rocm --define=using_rocm=true --define=using_rocm_hipcc=true
build:rocm --action_env TF_NEED_ROCM=1

build:sycl --crosstool_top=@local_config_sycl//crosstool:toolchain
build:sycl --define=using_sycl=true
build:sycl --action_env TF_NEED_OPENCL_SYCL=1

build:sycl_nodouble --config=sycl
build:sycl_nodouble --cxxopt -DTENSORFLOW_SYCL_NO_DOUBLE

build:sycl_nodouble --config=sycl
build:sycl_asan --copt -fno-omit-frame-pointer --copt -fsanitize-coverage=3 --copt -DGPR_NO_DIRECT_SYSCALLS --linkopt -fPIC --linkopt -fsanitize=address

build:sycl_nodouble --config=sycl
build:sycl_trisycl --define=using_trisycl=true

# Options extracted from configure script
build:ngraph --define=with_ngraph_support=true
build:numa --define=with_numa_support=true

# Options to disable default on features
build:noaws --define=no_aws_support=true
build:nogcp --define=no_gcp_support=true
build:nohdfs --define=no_hdfs_support=true
build:nonccl --define=no_nccl_support=true

build --define=use_fast_cpp_protos=true
build --define=allow_oversize_protos=true

build --spawn_strategy=standalone
build -c opt

# Make Bazel print out all options from rc files.
build --announce_rc

# Other build flags.
build --define=grpc_no_ares=true

# See https://github.com/bazelbuild/bazel/issues/7362 for information on what
# --incompatible_remove_legacy_whole_archive flag does.
# This flag is set to true in Bazel 1.0 and newer versions. We tried to migrate
# Tensorflow to the default, however test coverage wasn't enough to catch the
# errors.
# There is ongoing work on Bazel team's side to provide support for transitive
# shared libraries. As part of migrating to transitive shared libraries, we
# hope to provide a better mechanism for control over symbol exporting, and
# then tackle this issue again.
#
# TODO: Remove this line once TF doesn't depend on Bazel wrapping all library
# archives in -whole_archive -no_whole_archive.
build --noincompatible_remove_legacy_whole_archive

# These are bazel 2.0's incompatible flags. Tensorflow needs to use bazel 2.0.0
# to use cc_shared_library, as part of the Tensorflow Build Improvements RFC:
# https://github.com/tensorflow/community/pull/179
build --noincompatible_prohibit_aapt1

# Modular TF build options
build:dynamic_kernels --define=dynamic_loaded_kernels=true
build:dynamic_kernels --copt=-DAUTOLOAD_DYNAMIC_KERNELS

# Build TF with C++ 17 features.
build:c++17 --cxxopt=-std=c++1z
build:c++17 --cxxopt=-stdlib=libc++
build:c++1z --config=c++17

# Enable using platform specific build settings
build --enable_platform_specific_config

# Suppress C++ compiler warnings, otherwise build logs become 10s of MBs.
build:linux --copt=-w
build:macos --copt=-w
build:windows --copt=/w

# Tensorflow uses M_* math constants that only get defined by MSVC headers if
# _USE_MATH_DEFINES is defined.
build:windows --copt=/D_USE_MATH_DEFINES
build:windows --host_copt=/D_USE_MATH_DEFINES

# Default paths for TF_SYSTEM_LIBS
build:linux --define=PREFIX=/usr
build:linux --define=LIBDIR=$(PREFIX)/lib
build:linux --define=INCLUDEDIR=$(PREFIX)/include
build:macos --define=PREFIX=/usr
build:macos --define=LIBDIR=$(PREFIX)/lib
build:macos --define=INCLUDEDIR=$(PREFIX)/include
# TF_SYSTEM_LIBS do not work on windows.

# By default, build TF in C++ 14 mode.
build:linux --cxxopt=-std=c++14
build:linux --host_cxxopt=-std=c++14
build:macos --cxxopt=-std=c++14
build:macos --host_cxxopt=-std=c++14
build:windows --cxxopt=/std:c++14
build:windows --host_cxxopt=/std:c++14

# On windows, we still link everything into a single DLL.
build:windows --config=monolithic

# On linux, we dynamically link small amount of kernels
build:linux --config=dynamic_kernels

# Make sure to include as little of windows.h as possible
build:windows --copt=-DWIN32_LEAN_AND_MEAN
build:windows --host_copt=-DWIN32_LEAN_AND_MEAN
build:windows --copt=-DNOGDI
build:windows --host_copt=-DNOGDI

# Misc build options we need for windows.
build:windows --linkopt=/DEBUG
build:windows --host_linkopt=/DEBUG
build:windows --linkopt=/OPT:REF
build:windows --host_linkopt=/OPT:REF
build:windows --linkopt=/OPT:ICF
build:windows --host_linkopt=/OPT:ICF
build:windows --experimental_strict_action_env=true

# Verbose failure logs when something goes wrong
build:windows --verbose_failures

# On windows, we never cross compile
build:windows --distinct_host_configuration=false

# Suppress all warning messages.
build:short_logs --output_filter=DONT_MATCH_ANYTHING

# Instruction set optimizations
# TODO(gunan): Create a feature in toolchains for avx/avx2 to
#   avoid having to define linux/win separately.
build:avx_linux --copt=-mavx
build:avx2_linux --copt=-mavx2
build:native_arch_linux --copt=-march=native
build:avx_win --copt=/arch=AVX
build:avx2_win --copt=/arch=AVX2

# Options to build TensorFlow 1.x or 2.x.
build:v1 --define=tf_api_version=1
build:v2 --define=tf_api_version=2
build:v1 --action_env=TF2_BEHAVIOR=0
build:v2 --action_env=TF2_BEHAVIOR=1
build --config=v2
test --config=v2

# Enable XLA
build:xla --action_env=TF_ENABLE_XLA=1
build:xla --define=with_xla_support=true

# BEGIN TF REMOTE BUILD EXECUTION OPTIONS
# Options when using remote execution
# WARNING: THESE OPTIONS WONT WORK IF YOU DO NOT HAVE PROPER AUTHENTICATION AND PERMISSIONS

# Flag to enable remote config
common --experimental_repo_remote_exec

build:rbe --action_env=BAZEL_DO_NOT_DETECT_CPP_TOOLCHAIN=1
build:rbe --google_default_credentials
build:rbe --bes_backend=buildeventservice.googleapis.com
build:rbe --bes_results_url="https://source.cloud.google.com/results/invocations"
build:rbe --bes_timeout=600s
build:rbe --define=EXECUTOR=remote
build:rbe --distinct_host_configuration=false
build:rbe --flaky_test_attempts=3
build:rbe --jobs=200
build:rbe --remote_executor=grpcs://remotebuildexecution.googleapis.com
build:rbe --remote_timeout=3600
build:rbe --spawn_strategy=remote,worker,standalone,local
test:rbe --test_env=USER=anon
# Attempt to minimize the amount of data transfer between bazel and the remote
# workers:
build:rbe --remote_download_toplevel

build:rbe_linux --config=rbe
build:rbe_linux --action_env=PATH="/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/local/go/bin"
build:rbe_linux --host_javabase=@bazel_toolchains//configs/ubuntu16_04_clang/1.1:jdk8
build:rbe_linux --javabase=@bazel_toolchains//configs/ubuntu16_04_clang/1.1:jdk8
build:rbe_linux --host_java_toolchain=@bazel_tools//tools/jdk:toolchain_hostjdk8
build:rbe_linux --java_toolchain=@bazel_tools//tools/jdk:toolchain_hostjdk8

# Non-rbe settings we should include because we do not run configure
build:rbe_linux --config=xla
build:rbe_linux --config=avx_linux
build:rbe_linux --config=short_logs
# TODO(gunan): Check why we need this specified in rbe, but not in other builds.
build:rbe_linux --linkopt=-lrt
build:rbe_linux --linkopt=-lm

build:rbe_cpu_linux --config=rbe_linux
build:rbe_cpu_linux --crosstool_top="//third_party/toolchains/preconfig/ubuntu16.04/gcc7_manylinux2010:toolchain"
build:rbe_cpu_linux --extra_toolchains="//third_party/toolchains/preconfig/ubuntu16.04/gcc7_manylinux2010:cc-toolchain-k8"
build:rbe_cpu_linux --extra_execution_platforms"=@org_tensorflow//third_party/toolchains:rbe_ubuntu16.04-manylinux2010"
build:rbe_cpu_linux --host_platform="@org_tensorflow//third_party/toolchains:rbe_ubuntu16.04-manylinux2010"
build:rbe_cpu_linux --platforms="@org_tensorflow//third_party/toolchains:rbe_ubuntu16.04-manylinux2010"

build:rbe_linux_cuda_base --config=rbe_linux
build:rbe_linux_cuda_base --repo_env=TF_NEED_TENSORRT=1
build:rbe_linux_cuda_base --repo_env=TF_CUDA_VERSION=10
build:rbe_linux_cuda_base --repo_env=TF_CUDNN_VERSION=7
build:rbe_linux_cuda_base --repo_env=REMOTE_GPU_TESTING=1
build:rbe_linux_cuda_base --repo_env=TF_NEED_CUDA=1
test:rbe_linux_cuda_base --test_env=LD_LIBRARY_PATH="/usr/local/cuda/lib64:/usr/local/cuda/extras/CUPTI/lib64"

build:rbe_linux_cuda_nvcc --config=rbe_linux_cuda_base
build:rbe_linux_cuda_nvcc --crosstool_top="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_cuda//crosstool:toolchain"
build:rbe_linux_cuda_nvcc --extra_toolchains="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_cuda//crosstool:toolchain-linux-x86_64"
build:rbe_linux_cuda_nvcc --extra_execution_platforms="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_platform//:platform"
build:rbe_linux_cuda_nvcc --host_platform="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_platform//:platform"
build:rbe_linux_cuda_nvcc --platforms="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_platform//:platform"
build:rbe_linux_cuda_nvcc --repo_env=TF_CUDA_CONFIG_REPO="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_cuda"
build:rbe_linux_cuda_nvcc --repo_env=TF_TENSORRT_CONFIG_REPO="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_tensorrt"
build:rbe_linux_cuda_nvcc --repo_env=TF_NCCL_CONFIG_REPO="@ubuntu16.04-py3-gcc7_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_nccl"
build:rbe_linux_cuda_nvcc --define=using_cuda_nvcc=true
test:rbe_linux_cuda_nvcc --config=rbe_linux_cuda_base

build:rbe_linux_cuda_clang --config=rbe_linux_cuda_base
build:rbe_linux_cuda_clang --crosstool_top="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_cuda//crosstool:toolchain"
build:rbe_linux_cuda_clang --extra_toolchains="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_cuda//crosstool:toolchain-linux-x86_64"
build:rbe_linux_cuda_clang --extra_execution_platforms="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_platform//:platform"
build:rbe_linux_cuda_clang --host_platform="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_platform//:platform"
build:rbe_linux_cuda_clang --platforms="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_platform//:platform"
build:rbe_linux_cuda_clang --repo_env=TF_CUDA_CONFIG_REPO="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_cuda"
build:rbe_linux_cuda_clang --repo_env=TF_TENSORRT_CONFIG_REPO="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_tensorrt"
build:rbe_linux_cuda_clang --repo_env=TF_NCCL_CONFIG_REPO="@ubuntu16.04-py3-clang_manylinux2010-cuda10.1-cudnn7-tensorrt6.0_config_nccl"
build:rbe_linux_cuda_clang --define=using_cuda_clang=true
test:rbe_linux_cuda_clang --config=rbe_linux_cuda_base

common:rbe_gpu_linux --config=rbe_linux_cuda_nvcc

build:rbe_linux_py2 --config=rbe_linux
build:rbe_linux_py2 --repo_env=PYTHON_BIN_PATH="/usr/bin/python2"
build:rbe_linux_py2 --python_path="/usr/bin/python2"
build:rbe_linux_py2 --repo_env=TF_PYTHON_CONFIG_REPO="@org_tensorflow//third_party/toolchains/preconfig/ubuntu16.04/py"

build:rbe_linux_py3 --config=rbe_linux
build:rbe_linux_py3 --python_path="/usr/bin/python3"
build:rbe_linux_py3 --repo_env=TF_PYTHON_CONFIG_REPO="@ubuntu16.04-manylinux2010-py3_config_python"

build:rbe_win --config=rbe
build:rbe_win --crosstool_top="@org_tensorflow//third_party/toolchains/preconfig/win/bazel_211:toolchain"
build:rbe_win --extra_toolchains="@org_tensorflow//third_party/toolchains/preconfig/win/bazel_211:cc-toolchain-x64_windows"
build:rbe_win --host_javabase="@org_tensorflow//third_party/toolchains/preconfig/win:windows_jdk8"
build:rbe_win --javabase="@org_tensorflow//third_party/toolchains/preconfig/win:windows_jdk8"
build:rbe_win --extra_execution_platforms="@org_tensorflow//third_party/toolchains/preconfig/win:rbe_windows_ltsc2019"
build:rbe_win --host_platform="@org_tensorflow//third_party/toolchains/preconfig/win:rbe_windows_ltsc2019"
build:rbe_win --platforms="@org_tensorflow//third_party/toolchains/preconfig/win:rbe_windows_ltsc2019"
build:rbe_win --shell_executable=C:\\tools\\msys64\\usr\\bin\\bash.exe

# TODO(gunan): Remove once we use MSVC 2019 with latest patches.
build:rbe_win --define=override_eigen_strong_inline=true
build:rbe_win --jobs=500

build:rbe_win_py37 --config=rbe
build:rbe_win_py37 --repo_env=TF_PYTHON_CONFIG_REPO="@windows_py37_config_python"
build:rbe_win_py37 --python_path=C:\\Python37\\python.exe

build:rbe_win_py38 --config=rbe
build:rbe_win_py38 --repo_env=PYTHON_BIN_PATH=C:\\Python38\\python.exe
build:rbe_win_py38 --repo_env=PYTHON_LIB_PATH=C:\\Python38\\lib\\site-packages
build:rbe_win_py38 --repo_env=TF_PYTHON_CONFIG_REPO=@org_tensorflow//third_party/toolchains/preconfig/win_1803/py38
build:rbe_win_py38 --python_path=C:\\Python38\\python.exe

# These you may need to change for your own GCP project.
build:tensorflow_testing_rbe --project_id=tensorflow-testing
common:tensorflow_testing_rbe_linux --remote_instance_name=projects/tensorflow-testing/instances/default_instance
build:tensorflow_testing_rbe_linux --config=tensorflow_testing_rbe
build:tensorflow_testing_rbe_linux --config=rbe
build:tensorflow_testing_rbe_linux --config=rbe_linux

common:tensorflow_testing_rbe_win --remote_instance_name=projects/tensorflow-testing/instances/windows
build:tensorflow_testing_rbe_win --config=tensorflow_testing_rbe

# TFLite build configs for generic embedded Linux
build:elinux --crosstool_top=@local_config_embedded_arm//:toolchain
build:elinux --host_crosstool_top=@bazel_tools//tools/cpp:toolchain
build:elinux_aarch64 --config=elinux
build:elinux_aarch64 --cpu=aarch64
build:elinux_armhf --config=elinux
build:elinux_armhf --cpu=armhf
# END TF REMOTE BUILD EXECUTION OPTIONS

# Default options should come above this line

# Options from ./configure
try-import %workspace%/.tf_configure.bazelrc

# Put user-specific options in .bazelrc.user
try-import %workspace%/.bazelrc.user