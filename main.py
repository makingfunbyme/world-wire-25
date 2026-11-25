import os
from pathlib import Path

source = Path(__file__).resolve().with_name("entry.png")
output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "entry.png"
data = source.read_bytes()
output_path.write_bytes(data)
print(len(data))
