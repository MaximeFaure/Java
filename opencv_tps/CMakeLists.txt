cmake_minimum_required(VERSION 3.10)
project(OpenCV_TPs)

# Définir le standard C++
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Trouver OpenCV
find_package(OpenCV REQUIRED)

# Inclure les répertoires OpenCV
include_directories(${OpenCV_INCLUDE_DIRS})

# TP1 - Intensity Profile
add_executable(tp1 TP1.cpp)
target_link_libraries(tp1 ${OpenCV_LIBS})

# TP2 - Range Expansion and Histograms
add_executable(tp2 TP2.cpp)
target_link_libraries(tp2 ${OpenCV_LIBS})

# Messages d'information
message(STATUS "OpenCV version: ${OpenCV_VERSION}")
message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
