import argparse
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("actions", choices=["run", "test", "unit", "e2e"])
args = parser.parse_args()


if __name__ == "__main__":
    if args.actions == "run":
        subprocess.run(["py", "main.py"])
    elif args.actions == "test":
        subprocess.run(["pytest", "test_all.py"])
    elif args.actions == "unit":
        subprocess.run(["pytest", "test_unittest.py"])
    else:
        subprocess.run(["pytest", "test.py"])
