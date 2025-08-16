import os
import zlib
import struct
import tkinter as tk
from tkinter import filedialog

def chunked(data, size):
    """Split data into fixed-size chunks."""
    for i in range(0, len(data), size):
        yield data[i:i+size]
def main():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a .pfe replay file",
        filetypes=[("Replay files", "*.pfe")]
    )
    if not file_path:
        print("No file selected.")
        return
    with open(file_path, "rb") as f:
        compressed = f.read()
    try:
        decompressed = zlib.decompress(compressed)
    except Exception as e:
        print("Error decompressing:", e)
        return
    base, _ = os.path.splitext(file_path)
    output_path = base + ".txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Replay structure analysis\n\n")
        # Try different record sizes
        for size in [8, 12, 16, 20, 24, 32]:
            f.write(f"--- Interpreting as {size}-byte records ---\n")
            for i, chunk in enumerate(chunked(decompressed, size)):
                # pad to multiple of 4
                if len(chunk) % 4 != 0:
                    continue
                ints = struct.unpack("<" + "i"*(len(chunk)//4), chunk)
                floats = struct.unpack("<" + "f"*(len(chunk)//4), chunk)
                f.write(f"Frame {i:05d}: ints={ints} floats={floats}\n")
                if i > 200:  # limit output
                    f.write("...\n")
                    break
            f.write("\n")
    print(f"Structured dump saved to: {output_path}")
if __name__ == "__main__":
    print("Select a .pfe file.")
    main()
    input("Press Enter to finish...")