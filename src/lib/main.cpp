#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

#include <cmath>

namespace py = pybind11;

#ifndef M_PI
#define M_PI 3.14159265358979323846264338328
#endif

// A solver for Kepler's equation based on:
//
// Nijenhuis (1991)
// http://adsabs.harvard.edu/abs/1991CeMDA..51..319N
//
// and
//
// Markley (1995)
// http://adsabs.harvard.edu/abs/1995CeMDA..63..101M

namespace kepler {

// Implementation from numpy
template <typename T>
inline T npy_mod(T a, T b) {
  T mod = fmod(a, b);

  if (!b) {
    // If b == 0, return result of fmod. For IEEE is nan
    return mod;
  }

  // adjust fmod result to conform to Python convention of remainder
  if (mod) {
    if ((b < 0) != (mod < 0)) {
      mod += b;
    }
  } else {
    // if mod is zero ensure correct sign
    mod = copysign(0, b);
  }

  return mod;
}

template <typename T>
inline T get_markley_starter(T M, T ecc, T ome) {
  // M must be in the range [0, pi)
  const T FACTOR1 = 3 * M_PI / (M_PI - 6 / M_PI);
  const T FACTOR2 = 1.6 / (M_PI - 6 / M_PI);

  T M2 = M * M;
  T alpha = FACTOR1 + FACTOR2 * (M_PI - M) / (1 + ecc);
  T d = 3 * ome + alpha * ecc;
  T alphad = alpha * d;
  T r = (3 * alphad * (d - ome) + M2) * M;
  T q = 2 * alphad * ome - M2;
  T q2 = q * q;
  T w = pow(std::abs(r) + sqrt(q2 * q + r * r), 2.0 / 3);
  return (2 * r * w / (w * w + w * q + q2) + M) / d;
}

template <typename T>
inline T refine_estimate(T M, T ecc, T ome, T E) {
  T sE = E - sin(E);
  T cE = 1 - cos(E);

  T f_0 = ecc * sE + E * ome - M;
  T f_1 = ecc * cE + ome;
  T f_2 = ecc * (E - sE);
  T f_3 = 1 - f_1;
  T d_3 = -f_0 / (f_1 - 0.5 * f_0 * f_2 / f_1);
  T d_4 = -f_0 / (f_1 + 0.5 * d_3 * f_2 + (d_3 * d_3) * f_3 / 6);
  T d_42 = d_4 * d_4;
  T dE = -f_0 / (f_1 + 0.5 * d_4 * f_2 + d_4 * d_4 * f_3 / 6 - d_42 * d_4 * f_2 / 24);

  return E + dE;
}

double solve(double M, double ecc) {
  const double two_pi = 2 * M_PI;

  // Wrap M into the range [0, 2*pi]
  M = npy_mod(M, two_pi);

  //
  bool high = M > M_PI;
  if (high) M = two_pi - M;

  // Get the starter
  double ome = 1.0 - ecc;
  double E = get_markley_starter(M, ecc, ome);

  // Refine this estimate using a high order Newton step
  E = refine_estimate(M, ecc, ome, E);

  if (high) E = two_pi - E;

  return E;
}

}  // namespace kepler

PYBIND11_MODULE(_core, m) {
  m.doc() = "A fast and stable Kepler solver";
  m.def("solve", py::vectorize(kepler::solve));
}
