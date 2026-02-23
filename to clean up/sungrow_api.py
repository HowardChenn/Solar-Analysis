import time
from pymodbus.client import ModbusTcpClient

INVERTER_IP = "192.168.0.243"
PORT = 502

client = ModbusTcpClient(host=INVERTER_IP, port=PORT)
client.connect()

def read_all():
    snapshot = {}
    for addr in range(5000, 5052):
        res = client.read_input_registers(address=addr, count=2, slave=1)
        if not res.isError():
            snapshot[addr] = res.registers  # keep raw pair
    return snapshot

print("Scanning input registers from 5000 to 5051...")

snapshots = []
for _ in range(10):
    snap = read_all()
    snapshots.append(snap)
    time.sleep(1)

client.close()

# Detect and print only registers that changed (first and last values only)
print("\n🔍 Registers that changed (showing first → last):\n")

for addr in range(5000, 5052):
    values = [snap.get(addr) for snap in snapshots]
    if any(v != values[0] for v in values[1:] if v is not None):
        print(f"Addr {addr:04d} changed: {values[0]} → {values[-1]}")
