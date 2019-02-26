import smbus

def getTempLM75(address):
    bus = smbus.SMBus(1)
    try:
        raw = bus.read_word_data(address, 0) & 0xFFFF
    except :
        return -100500
    raw = ((raw << 8) & 0xFF00) + (raw >> 8)
    temperature = (raw / 32.0) / 8.0
    return temperature

if __name__ == "__main__":
    print(getTempLM75(0x4f))
