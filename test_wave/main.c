#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PI            3.14159265358979323846
#define DURATION_SEC  3   // test speed 1 bps == 1 byte msg
#define AMPLITUDE     1000
#define MSG_LENGTH    DURATION_SEC
#define SAMPLING_RATE 512   // power of two
#define BUFFER_SIZE   (SAMPLING_RATE * DURATION_SEC)
#define PERIOD        (SAMPLING_RATE / 8)
#define TONE          256

// https://docs.fileformat.com/audio/wav/

typedef struct wav_header {
  char riff[4];               // "RIFF"
  int32_t flength;            // file length in bytes
  char wave[4];               // "WAVE"
  char fmt[4];                // "fmt "
  int32_t chunk_size;         // size of FMT chunk in bytes (usually 16)
  int16_t format_tag;         // 1=PCM, 257=Mu-Law, 258=A-Law, 259=ADPCM
  int16_t num_chans;          // 1=mono, 2=stereo
  int32_t srate;              // Sampleling rate in samples per second
  int32_t bytes_per_sec;      // bytes per second = srate*bytes_per_sample
  int16_t bytes_per_sample;   // 2=16-bit mono, 4=16-bit stereo
  int16_t bits_per_sample;    // Number of bits per sample
  char data[4];               // "data"
  int32_t dlength;            // data length in bytes (filelength - header size)
} WavHeader;

uint16_t sin_wave(double time, double frequency, double amplitude);
uint16_t square_wave(double time, double frequency, double amplitude);
void print_binary(int n);
WavHeader
new_WavHeader(int sampling_rate, int buffer_size, int bits_per_sample);

int main(void)
{
  WavHeader wavh = new_WavHeader(SAMPLING_RATE, BUFFER_SIZE, 16);
  uint16_t buffer[BUFFER_SIZE] = {};
  char msg[MSG_LENGTH] = "WAA";

  assert(sizeof(msg) * SAMPLING_RATE == BUFFER_SIZE);

  size_t count = 0;
  int i = 0;
  while (count < sizeof(msg)) {
    for (uint8_t letter = msg[count]; letter > 0; letter <<= 1) {
      // check null character ??
      int bit = letter & 128;
      int j = 0;
      for (; j < PERIOD; j++, i++) {
        double amp = bit ? AMPLITUDE * 20 : AMPLITUDE;
        // buffer[i]
        // = (uint16_t) ((cos((2 * PI * TONE * i) / SAMPLING_RATE) * amp));
        buffer[i] = square_wave(i, TONE, amp);
      }
    }
    count++;
    printf("i == %d\n", i);
  }
  FILE* fp = fopen("test.wav", "w");
  fwrite(&wavh, 1, sizeof(WavHeader), fp);
  fwrite(buffer, 2, BUFFER_SIZE, fp);
}

uint16_t sin_wave(double time, double frequency, double amplitude)
{
  uint16_t result;
  double tpc = SAMPLING_RATE / frequency;   // ticks per cycle
  double cycles = time / tpc;
  double rad = 2 * PI * cycles;
  result = amplitude * sin(rad);
  return result;
}

uint16_t sin_wave2(double time, double frequency, double amplitude)
{
}

uint16_t square_wave(double time, double frequency, double amplitude)
{
  uint16_t result = 0;
  int tpc = 44100 / frequency;   // ticks per cycle
  int cyclepart = (int) time % tpc;
  int halfcycle = tpc / 2;
  if (cyclepart < halfcycle) {
    result = amplitude;
  }
  return result;
}

WavHeader new_WavHeader(int sampling_rate, int buffer_size, int bits_per_sample)
{
  WavHeader wavh;
  strncpy(wavh.riff, "RIFF", 4);
  strncpy(wavh.wave, "WAVE", 4);
  strncpy(wavh.fmt, "fmt ", 4);
  strncpy(wavh.data, "data", 4);

  wavh.chunk_size = 16;
  wavh.format_tag = 1;
  wavh.num_chans = 1;
  wavh.srate = sampling_rate;
  wavh.bits_per_sample = bits_per_sample;
  wavh.bytes_per_sec = wavh.srate * wavh.bits_per_sample / 8 * wavh.num_chans;
  wavh.bytes_per_sample = wavh.bits_per_sample / 8 * wavh.num_chans;
  wavh.dlength = buffer_size * wavh.bytes_per_sample;
  wavh.flength = wavh.dlength + sizeof(WavHeader);
  return wavh;
}

void print_binary(int n)
{
  unsigned i;
  for (i = 1 << 7; i > 0; i = i / 2) {
    (n & i) ? printf("1") : printf("0");
  }
  printf("\n");
}