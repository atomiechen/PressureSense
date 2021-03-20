#include "ADG725.h"
#include "matrix_sensor.h"
#include "matrix_sensor_util.h"

#define CSA 6
#define CSB 5

int i = 0;
int k = 0;
uint8_t reg_x = (1<<CSB);
uint8_t reg_y = (1<<CSA);

uint8_t DataRead[256];

void loop_init(void) {
  i = 0;
  k = 0;
  reg_x = (1<<CSB);
  reg_y = (1<<CSA);
  set_mux(reg_x);
  set_mux(reg_y);
}

char record_and_move_16_16_square(uint8_t data) {
  char ret = 0;
  
  // record
  DataRead[16*i+k] = data;
  
  k++;
  if (k == 16) {
    i++;
    if (i == 16) {
      // need to send data
      compress_data_224(DataRead, DataRead);
      loop_init();
      ret = 1;
    } else {
      k = 0;
      reg_y = (1<<CSA);
      reg_x++;
      set_mux(reg_x);
      set_mux(reg_y);
    }
  } else {
    reg_y++;
    set_mux(reg_y);
  }
  return ret;
}

char record_and_move_16_16_trapezoid(uint8_t data) {
  char ret = 0;
  
  // record
  DataRead[16*i+k] = data;
  
  k++;
  if (k == 16) {
    i++;
    if (i == 16) {
      // need to send data
      compress_data_224(DataRead, DataRead);
      loop_init();
      ret = 1;
    } else {
      k = 0;
      reg_y = (1<<CSA);
      reg_x++;
      set_mux(reg_x);
      set_mux(reg_y);
    }
  } else {
    // reg_y++;
    uint8_t tmp = reg_y & 0x0F;
    if (tmp > 7) {
      reg_y--;
    } else if (tmp == 7) {
      reg_y = (1<<CSA) + 15;
    } else {
      reg_y++;
    }
    set_mux(reg_y);
  }
  return ret;
}

char record_and_move_4_4_square(uint8_t data) {
  char ret = 0;
  
  // record
  DataRead[4*i+k] = data;
  
  k++;
  if (k == 4) {
    i++;
    if (i == 4) {
      // need to send data
      loop_init();
      ret = 1;
    } else {
      k = 0;
      reg_y = (1<<CSA);
      reg_x++;
      set_mux(reg_x);
      set_mux(reg_y);
    }
  } else {
    reg_y++;
    set_mux(reg_y);
  }
  return ret;
}

char record_and_move_8_8_trapezoid(uint8_t data) {
  // TODO
  char ret = 0;
  
  // record
  DataRead[8*i+k] = data;
  
  k++;
  if (k == 8) {
    i++;
    if (i == 8) {
      // need to send data
      loop_init();
      ret = 1;
    } else {
      k = 0;
      reg_y = (1<<CSA);
      reg_x++;
      set_mux(reg_x);
      set_mux(reg_y);
    }
  } else {
    // reg_y++;
    uint8_t tmp = reg_y & 0x0F;
    if (tmp > 7) {
      reg_y--;
    } else if (tmp == 7) {
      reg_y = (1<<CSA) + 15;
    } else {
      reg_y++;
    }
    set_mux(reg_y);
  }
  return ret;
}
