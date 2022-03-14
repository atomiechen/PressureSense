#ifndef MATRIX_SENSOR_H
#define MATRIX_SENSOR_H

#include <stdint.h>

extern uint8_t DataRead[];

#define SCH_16_16_SQUARE(_name)                       \
struct sensor_scheme _name = {                        \
  .samples_len = 256,                                 \
  .data_len = 224,                                    \
  .data = DataRead,                                   \
  .loop_init = loop_init,                             \
  .record_and_move = record_and_move_16_16_square,    \
};

#define SCH_16_16_TRAPEZOID(_name)                    \
struct sensor_scheme _name = {                        \
  .samples_len = 256,                                 \
  .data_len = 224,                                    \
  .data = DataRead,                                   \
  .loop_init = loop_init,                             \
  .record_and_move = record_and_move_16_16_trapezoid, \
};

#define SCH_4_4_SQUARE(_name)                         \
struct sensor_scheme _name = {                        \
  .samples_len = 16,                                  \
  .data_len = 16,                                     \
  .data = DataRead,                                   \
  .loop_init = loop_init,                             \
  .record_and_move = record_and_move_4_4_square,      \
};

#define SCH_8_8_TRAPEZOID(_name)                      \
struct sensor_scheme _name = {                        \
  .samples_len = 64,                                  \
  .data_len = 64,                                     \
  .data = DataRead,                                   \
  .loop_init = loop_init,                             \
  .record_and_move = record_and_move_8_8_trapezoid,   \
};

#define SCH_24_6_GLOVE(_name)                      \
struct sensor_scheme _name = {                        \
  .samples_len = 144,                                  \
  .data_len = 144,                                     \
  .data = DataRead,                                   \
  .loop_init = loop_init,                             \
  .record_and_move = record_and_move_24_6_glove,   \
};

#define SCH_32_4_GLOVE(_name)                      \
struct sensor_scheme _name = {                        \
  .samples_len = 128,                                  \
  .data_len = 128,                                     \
  .data = DataRead,                                   \
  .loop_init = loop_init,                             \
  .record_and_move = record_and_move_32_4_glove,   \
};

struct sensor_scheme {
  uint16_t samples_len;
  uint16_t data_len;
  uint8_t *data;

  void (*loop_init)(void);
  char (*record_and_move)(uint8_t);
};

void loop_init(void);

char record_and_move_16_16_square(uint8_t data);
char record_and_move_16_16_trapezoid(uint8_t data);
char record_and_move_4_4_square(uint8_t data);
char record_and_move_8_8_trapezoid(uint8_t data);
char record_and_move_24_6_glove(uint8_t data);
char record_and_move_32_4_glove(uint8_t data);


#endif  // MATRIX_SENSOR_H
