float temp;



#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
#define PINring        6 
#define PINstick1      2
#define PINstick2      4
// How many NeoPixels are attached to the Arduino?
#define NUMPIXELSring 20 
#define NUMPIXELSstick1 10
#define NUMPIXELSstick2 10
// When setting up the NeoPixel library, we tell it how many pixels,
// and which pin to use to send signals. 
Adafruit_NeoPixel pixelsring(NUMPIXELSring, PINring, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixelsstick1(NUMPIXELSstick1, PINstick1, NEO_GRB + NEO_KHZ800);
Adafruit_NeoPixel pixelsstick2(NUMPIXELSstick2, PINstick2, NEO_GRB + NEO_KHZ800);
#define DELAYVAL 500 // Time (in milliseconds) to pause between pixels
#include "Seeed_MCP9600.h"

#ifdef ARDUINO_SAMD_VARIANT_COMPLIANCE
    #define SERIAL SerialUSB
#else
    #define SERIAL Serial
#endif

MCP9600 sensor;

err_t sensor_basic_config() {
    err_t ret = NO_ERROR;
    CHECK_RESULT(ret, sensor.set_filt_coefficients(FILT_MID));
    CHECK_RESULT(ret, sensor.set_cold_junc_resolution(COLD_JUNC_RESOLUTION_0_25));
    CHECK_RESULT(ret, sensor.set_ADC_meas_resolution(ADC_14BIT_RESOLUTION));
    CHECK_RESULT(ret, sensor.set_burst_mode_samp(BURST_32_SAMPLE));
    CHECK_RESULT(ret, sensor.set_sensor_mode(NORMAL_OPERATION));
    return ret;
}


err_t get_temperature(float* value) {
    err_t ret = NO_ERROR;
    float hot_junc = 0;
    float junc_delta = 0;
    float cold_junc = 0;
    CHECK_RESULT(ret, sensor.read_hot_junc(&hot_junc));
    CHECK_RESULT(ret, sensor.read_junc_temp_delta(&junc_delta));

    CHECK_RESULT(ret, sensor.read_cold_junc(&cold_junc));

    // SERIAL.print("hot junc=");
    // SERIAL.println(hot_junc);
    // SERIAL.print("junc_delta=");
    // SERIAL.println(junc_delta);
    // SERIAL.print("cold_junc=");
    // SERIAL.println(cold_junc);

    *value = hot_junc;

    return ret;

}

void setup() {
   Serial.begin(115200);
  pixelsring.begin(); // INITIALIZE NeoPixel ring object (REQUIRED)
  //pixelsstick1.begin(); // INITIALIZE NeoPixel stick1 object (REQUIRED)
  //pixelsstick2.begin(); // INITIALIZE NeoPixel stick 2 object (REQUIRED)
   //pixelsring.clear(); // Set all pixel colors to 'off'
  //pixelsstick.clear(); // Set all pixel colors to 'off'

  // The first NeoPixel in a strand is #0, second is 1, all the way up
  // to the count of pixels minus one.
  for(int ir=0; ir<NUMPIXELSring; ir++)  // For each pixel...
  for(int is1=0; is1<NUMPIXELSstick1; is1++) // For each pixel...
  for(int is2=0; is2<NUMPIXELSstick2; is2++){ // For each pixel...

    // pixels.Color() takes RGB values, from 0,0,0 up to 255,255,255
    pixelsring.setPixelColor(ir, pixelsring.Color(0, 0, 0));
    pixelsstick1.setPixelColor(is1, pixelsstick1.Color(0, 0, 0));
    pixelsstick2.setPixelColor(is2, pixelsstick2.Color(0, 0, 0));

    pixelsring.show();   // Send the updated pixel colors to the hardware.
    //pixelsstick1.show();   // Send the updated pixel colors to the hardware.
    //pixelsstick2.show();   // Send the updated pixel colors to the hardware.
  
  }
   
    SERIAL.println("serial start!!");
    if (sensor.init(THER_TYPE_K)) {
        SERIAL.println("sensor init failed!!");
    }
    sensor_basic_config();
  
}

void loop() {
 float temp = 0;
    get_temperature(&temp);
    SERIAL.print(temp);
    SERIAL.println(" *C ");
    delay(30000);
 
}
