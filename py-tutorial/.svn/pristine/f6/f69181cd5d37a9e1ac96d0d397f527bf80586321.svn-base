import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
print(len(ports), 'ports found')

for p in ports:
    print(p.device)
