# Cubesat not necessary for the function, but needed anyway.
def blinkOn(source, destination, cubesat):
    print(f"We are transitioning from {source} to {destination}")
    if cubesat.neopixel:
        cubesat.RGB = (50, 0, 0)

def blinkOff(source, destination, cubesat):
    print(f"We are transitioning from {source} to {destination}")
    if cubesat.neopixel:
        cubesat.RGB = (0, 0, 0)