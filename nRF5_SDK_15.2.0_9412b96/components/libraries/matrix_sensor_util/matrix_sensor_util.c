#include "matrix_sensor_util.h"

void compress_data_224(uint8_t *data_in, uint8_t *data_out) {
  // compress data from 256 to 224
  for (int i = 0; i < 256; i += 8) {
    for (int j = 0; j < 7; j++) {
      uint8_t now = data_in[i+j], next = data_in[i+j+1];
      data_out[i/8*7 + j] = ((now>>1)<<(j+1))|(next>>(7-j));
    }
  }
}

void decompress_data_224(uint8_t *data_in, uint8_t *data_out) {
  // decompress data from 224 to 256
  for (int i = 0; i < 224; i += 7){
    int group = i/7;
    data_out[group*8] = data_in[i] & 0xFE;
    for (int j=1;j<7;j++) {
      char now = data_in[i+j], last = data_in[i+j-1];
      data_out[group*8+j] = (last<<(8-j)|now>>j)&0xFE;
    }
    data_out[group*8+7] = data_in[i+6]<<1;
  }
}
