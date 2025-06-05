#include <riscv_vector.h>
#include <stdint.h>

int main() {
  alignas(64)
      int32_t A[16] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16};
  alignas(64)
      int32_t B[16] = {16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1};
  alignas(64) int32_t C[16];

  size_t vl = vsetvl_e32m4(16);

  vint32m4_t vecA = vle32_v_i32m4(A, vl);
  vint32m4_t vecB = vle32_v_i32m4(B, vl);

  vint32m4_t vecC = vadd_vv_i32m4(vecA, vecB, vl);

  vse32_v_i32m4(C, vecC, vl);

  return 0;
}
