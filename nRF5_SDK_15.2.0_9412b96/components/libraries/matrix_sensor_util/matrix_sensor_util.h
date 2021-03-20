#ifndef MATRIX_SENSOR_UTIL_H
#define MATRIX_SENSOR_UTIL_H

#include <stdint.h>

void compress_data_224(uint8_t *data_in, uint8_t *data_out);
void decompress_data_224(uint8_t *data_in, uint8_t *data_out);

#endif  // MATRIX_SENSOR_UTIL_H
