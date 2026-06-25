import subprocess
import sys

scripts = [
    "data/Southern/build_southern_v4.py",
    "data/Southern/build_json.py",
    "data/Southern/build_clues.py",
    "data/Southern/check_southern.py",
]

print()
print("========================================")
print(" Building Southern")
print("========================================")

for script in scripts:

    print()
    print(f"Running {script}")

    result = subprocess.run(
        [sys.executable, script]
    )

    if result.returncode != 0:

        print()
        print(f"FAILED: {script}")
        sys.exit(result.returncode)

print()
print("========================================")
print(" Southern build complete")
print("========================================")