cmake_minimum_required(VERSION 3.15...3.26)

project(qtl-xtp-api LANGUAGES CXX)

if (NOT SKBUILD)
    message(WARNING "\
  This CMake file is meant to be executed using 'scikit-build'. Running
  it directly will almost certainly not produce the desired result. If
  you are a user trying to install this package, please use the command
  below, which will install all necessary build dependencies, compile
  the package in an isolated environment, and then install it.
  =====================================================================
   $ pip install .
  =====================================================================
  If you are a software developer, and this is your own package, then
  it is usually much more efficient to install the build dependencies
  in your environment once and use the following command that avoids
  a costly creation of a new virtual environment at every compilation:
  =====================================================================
   $ pip install nanobind scikit-build-core[pyproject]
   $ pip install --no-build-isolation -ve .
  =====================================================================
  You may optionally add -Ceditable.rebuild=true to auto-rebuild when
  the package is imported. Otherwise, you need to re-run the above
  after editing C++ files.")
endif()

set(CMAKE_INSTALL_RPATH $ORIGIN)
set(CMAKE_CXX_FLAGS_RELEASE "-O3")

find_package(Python 3.8
        REQUIRED COMPONENTS Interpreter Development.Module
        OPTIONAL_COMPONENTS Development.SABIModule)

find_package(nanobind CONFIG REQUIRED)

nanobind_add_module(_xtp STABLE_ABI NB_STATIC
  src/main.cpp
  src/bind_consts.cpp
  src/bind_md_api.cpp
  src/bind_td_api.cpp
  src/md_api.cpp
  src/td_api.cpp
  src/dispatch_queue.cpp
)
target_include_directories(_xtp PRIVATE libs/xtp/include)
target_link_directories(_xtp PRIVATE libs/xtp/lib)
target_link_libraries(_xtp PRIVATE xtpquoteapi xtptraderapi)

install(TARGETS _xtp DESTINATION qtl_xtp_api)
install(FILES
        libs/xtp/lib/libxtpquoteapi.so
        libs/xtp/lib/libxtptraderapi.so
        DESTINATION qtl_xtp_api)
