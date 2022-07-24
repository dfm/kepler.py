

#include <pybind11/pybind11.h>

namespace py = pybind11;

PYBIND11_MODULE(_core, m) {
  m.doc() = R"pbdoc(
    An example pybind11 module
  )pbdoc";
}
