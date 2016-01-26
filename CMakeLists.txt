cmake_minimum_required(VERSION 3.3)
project(Vision__)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES main.cpp)
add_executable(Vision__ ${SOURCE_FILES})

find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(Vision__ ${OpenCV_LIBS})


if (ZMQ_LIBRARIES AND ZMQ_INCLUDE_DIRS)
    # in cache already
    set(ZMQ_FOUND TRUE)
else (ZMQ_LIBRARIES AND ZMQ_INCLUDE_DIRS)

    find_path(ZMQ_INCLUDE_DIR
            NAMES
            zmq.h
            PATHS
            /usr/include
            /usr/local/include
            /opt/local/include
            /sw/include
            )

    find_library(ZMQ_LIBRARY
            NAMES
            zmq
            PATHS
            /usr/lib
            /usr/local/lib
            /opt/local/lib
            /sw/lib
            )

    set(ZMQ_INCLUDE_DIRS
            ${ZMQ_INCLUDE_DIR}
            )

    if (ZMQ_LIBRARY)
        set(ZMQ_LIBRARIES
                ${ZMQ_LIBRARIES}
                ${ZMQ_LIBRARY}
                )
    endif (ZMQ_LIBRARY)

    include(FindPackageHandleStandardArgs)
    find_package_handle_standard_args(ZMQ DEFAULT_MSG ZMQ_LIBRARIES ZMQ_INCLUDE_DIRS)

    # show the ZMQ_INCLUDE_DIRS and ZMQ_LIBRARIES variables only in the advanced view
    mark_as_advanced(ZMQ_INCLUDE_DIRS ZMQ_LIBRARIES)

endif (ZMQ_LIBRARIES AND ZMQ_INCLUDE_DIRS)

include_directories(${ZMQ_INCLUDE_DIRS})
target_link_libraries(Vision__ ${ZMQ_LIBRARIES})