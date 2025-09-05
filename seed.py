import math
import sys

# --- Biome ID to name (expanded) ---
BIOMES = {
    0: "Ocean",
    1: "Plains",
    2: "Desert",
    3: "Mountains",
    4: "Forest",
    5: "Taiga",
    6: "Swamp",
    7: "River",
    8: "Nether",
    9: "The End",
    10: "Frozen Ocean",
    11: "Frozen River",
    12: "Snowy Tundra",
    15: "Jungle",
    20: "Savanna",
    24: "Snowy Taiga",
    28: "Wooded Mountains",
    29: "Taiga Hills",
    30: "Jungle Edge",
    38: "Frozen Ocean Deep",
    39: "Deep Frozen Ocean",
    40: "Bamboo Jungle Hills",
    41: "Bamboo Jungle",
    # Add more as needed...
}

# --- Utility Functions ---

def clamp01(v):
    return max(0.0, min(1.0, v))

def lerp(t, a, b):
    return a + t * (b - a)

def fade(t):
    # Classic Perlin fade curve
    return t * t * t * (t * (t * 6 - 15) + 10)

# --- Permutation table with deterministic shuffle ---

def permute(seed):
    perm = list(range(256))
    for i in range(255, 0, -1):
        seed = (seed * 6364136223846793005 + 1442695040888963407) & 0xFFFFFFFFFFFFFFFF
        j = seed % (i + 1)
        perm[i], perm[j] = perm[j], perm[i]
    return perm * 2

# --- Gradient function for 3D noise ---
def grad3(hash, x, y, z):
    h = hash & 15
    u = x if h < 8 else y
    v = y if h < 4 else (x if h in (12, 14) else z)
    return ((u if (h & 1) == 0 else -u) +
            (v if (h & 2) == 0 else -v))

# --- 3D Perlin noise ---
def perlin3d(x, y, z, perm):
    X = int(math.floor(x)) & 255
    Y = int(math.floor(y)) & 255
    Z = int(math.floor(z)) & 255
    xf = x - math.floor(x)
    yf = y - math.floor(y)
    zf = z - math.floor(z)

    u = fade(xf)
    v = fade(yf)
    w = fade(zf)

    aaa = perm[perm[perm[X] + Y] + Z]
    aba = perm[perm[perm[X] + (Y + 1)] + Z]
    aab = perm[perm[perm[X] + Y] + (Z + 1)]
    abb = perm[perm[perm[X] + (Y + 1)] + (Z + 1)]
    baa = perm[perm[perm[X + 1] + Y] + Z]
    bba = perm[perm[perm[X + 1] + (Y + 1)] + Z]
    bab = perm[perm[perm[X + 1] + Y] + (Z + 1)]
    bbb = perm[perm[perm[X + 1] + (Y + 1)] + (Z + 1)]

    x1 = lerp(u, grad3(aaa, xf, yf, zf), grad3(baa, xf - 1, yf, zf))
    x2 = lerp(u, grad3(aba, xf, yf - 1, zf), grad3(bba, xf - 1, yf - 1, zf))
    y1 = lerp(v, x1, x2)

    x3 = lerp(u, grad3(aab, xf, yf, zf - 1), grad3(bab, xf - 1, yf, zf - 1))
    x4 = lerp(u, grad3(abb, xf, yf - 1, zf - 1), grad3(bbb, xf - 1, yf - 1, zf - 1))
    y2 = lerp(v, x3, x4)

    return lerp(w, y1, y2)

# --- Octave Perlin noise for smooth variations ---

def octave_perlin3d(x, y, z, perm, octaves=4, persistence=0.5):
    total = 0
    frequency = 1
    amplitude = 1
    max_amp = 0

    for _ in range(octaves):
        total += perlin3d(x * frequency, y * frequency, z * frequency, perm) * amplitude
        max_amp += amplitude
        amplitude *= persistence
        frequency *= 2

    return total / max_amp

# --- Climate Generator Class ---

class BiomeClimateGenerator:
    def __init__(self, seed):
        self.seed = seed & 0xFFFFFFFFFFFFFFFF
        self.perm = permute(self.seed)

    def climate_parameters(self, x, y, z):
        scale = 1 / 512.0
        px, py, pz = x * scale, y * scale, z * scale

        temperature = octave_perlin3d(px + 100, py + 100, pz + 100, self.perm, octaves=5, persistence=0.6)
        humidity = octave_perlin3d(px + 200, py + 200, pz + 200, self.perm, octaves=5, persistence=0.6)
        continentalness = octave_perlin3d(px + 300, py + 300, pz + 300, self.perm, octaves=4, persistence=0.5)
        erosion = octave_perlin3d(px + 400, py + 400, pz + 400, self.perm, octaves=4, persistence=0.5)
        weirdness = octave_perlin3d(px + 500, py + 500, pz + 500, self.perm, octaves=3, persistence=0.7)
        offset = octave_perlin3d(px + 600, py + 600, pz + 600, self.perm, octaves=3, persistence=0.7)

        # Normalize and clamp between 0 and 1
        params = tuple(clamp01((p + 1) / 2) for p in (temperature, humidity, continentalness, erosion, weirdness, offset))
        return params  # temp, humid, cont, erosion, weird, offset

# --- Biome decision logic ---

def climate_to_biome(temp, humid, cont, erosion, weird, offset):
    # Ocean & Frozen Ocean
    if cont < 0.15:
        if temp < 0.3:
            return 10  # Frozen Ocean
        else:
            if offset > 0.7:
                return 39  # Deep Frozen Ocean
            return 0   # Ocean

    # Mountains & Hills
    if cont < 0.3:
        if erosion > 0.6:
            if offset > 0.5:
                return 28  # Wooded Mountains
            return 3   # Mountains
        else:
            if temp < 0.4:
                return 29  # Taiga Hills
            return 1  # Plains

    # Jungle and variants
    if temp > 0.75:
        if humid > 0.7:
            if weird > 0.8:
                return 40  # Bamboo Jungle Hills
            elif offset > 0.6:
                return 41  # Bamboo Jungle
            else:
                return 15  # Jungle
        elif humid > 0.3:
            return 30  # Jungle Edge
        else:
            return 2  # Desert

    # Snowy biomes
    if temp < 0.3:
        if humid > 0.6:
            return 24  # Snowy Taiga
        else:
            return 12  # Snowy Tundra

    # Swamp and forest
    if humid > 0.5:
        if temp < 0.7:
            if weird > 0.7:
                return 6   # Swamp
            else:
                return 4   # Forest
        else:
            return 20  # Savanna

    # Default fallback
    return 1  # Plains

# --- Biome blending for smooth edges ---

def blend_biomes(seed, x, y, z, generator):
    # Sample center and 4 neighbors
    coords = [
        (x, y, z),
        (x + 4, y, z),
        (x - 4, y, z),
        (x, y, z + 4),
        (x, y, z - 4)
    ]

    biome_weights = {}
    total_weight = 0

    for (cx, cy, cz) in coords:
        params = generator.climate_parameters(cx, cy, cz)
        biome_id = climate_to_biome(*params)
        # Weight by inverse distance (simple)
        dist = math.sqrt((cx - x)**2 + (cz - z)**2) + 0.1
        weight = 1 / dist
        biome_weights[biome_id] = biome_weights.get(biome_id, 0) + weight
        total_weight += weight

    # Normalize weights and find dominant biome
    for biome_id in biome_weights:
        biome_weights[biome_id] /= total_weight

    # Pick biome with max weight
    dominant_biome = max(biome_weights.items(), key=lambda item: item[1])[0]
    return dominant_biome, biome_weights

# --- ASCII map visualization ---

def visualize_biomes(seed, center_x, center_z, size=32):
    gen = BiomeClimateGenerator(seed)
    half = size // 2

    print(f"Biome map for seed {seed} centered at ({center_x}, {center_z})")

    for dz in range(-half, half):
        line = ""
        for dx in range(-half, half):
            bx, bz = center_x + dx * 4, center_z + dz * 4
            biome_id, _ = blend_biomes(seed, bx, 64, bz, gen)
            # Represent biome by first letter or number if unknown
            name = BIOMES.get(biome_id, "?")
            c = name[0] if name != "?" else "?"
            line += c
        print(line)

# --- Unit test framework ---

def run_unit_tests():
    print("Running unit tests...")

    # Placeholder: Add your known seed, coordinate, expected biome tuples here
    tests = [
        # (seed, x, y, z, expected_biome_name)
        (123456789, 0, 64, 0, "Plains"),
        (987654321, 100, 64, 100, "Desert"),
        # Add more test cases...
    ]

    gen = BiomeClimateGenerator(0)
    passed = 0
    for seed, x, y, z, expected in tests:
        gen.seed = seed & 0xFFFFFFFFFFFFFFFF
        gen.perm = permute(gen.seed)
        biome_id, _ = blend_biomes(seed, x, y, z, gen)
        biome_name = BIOMES.get(biome_id, "Unknown")
        if biome_name == expected:
            print(f"PASS: Seed={seed}, Coord=({x},{y},{z}) -> {biome_name}")
            passed += 1
        else:
            print(f"FAIL: Seed={seed}, Coord=({x},{y},{z}) -> {biome_name} (expected {expected})")

    print(f"Passed {passed}/{len(tests)} tests.")

# --- Main CLI ---

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        run_unit_tests()
        return

    print("Minecraft Bedrock Edition Biome Finder with blending and detailed climate")
    seed = int(input("Enter world seed (int): "))
    x = int(input("Enter X coordinate: "))
    y = int(input("Enter Y coordinate (ignored in biome calc): "))
    z = int(input("Enter Z coordinate: "))

    gen = BiomeClimateGenerator(seed)
    biome_id, weights = blend_biomes(seed, x, y, z, gen)
    biome_name = BIOMES.get(biome_id, "Unknown")

    print(f"Biome at ({x}, {y}, {z}): {biome_name}")
    print("Biome blend weights:")
    for b_id, w in sorted(weights.items(), key=lambda i: -i[1]):
        print(f"  {BIOMES.get(b_id,'?')} : {w:.3f}")

    # Optional: Visualize a small map around the coords
    if input("Show biome map around coords? (y/n): ").lower() == "y":
        visualize_biomes(seed, x, z, size=32)

if __name__ == "__main__":
    main()
