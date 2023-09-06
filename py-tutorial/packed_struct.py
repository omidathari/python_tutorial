from struct import *

# bool g_compressor_on;
# u16 adc_pressure_value;
# u16 adc_temperature_value;
# u16 adc_clamp_voltage_value;
# u16 adc_motor_current_value;
# u32 g_time;
# u8 g_tick;
# double sensor_pressure.kpa;
# double adc_p_cbuf.avg;
# double adc_p_cbuf.slope;

bytes = pack("=?HHHHLBfff",True,1,2,3,4,5,0x06,1.1,2.2,3.3)

print(bytes.__len__())
print(bytes)

values = unpack("=?HHHHLBfff",bytes)

print(values)