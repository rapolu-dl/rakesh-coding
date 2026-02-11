import argparse
import os
from collections import deque

def scan_last(filepath):
  try:
    with open(filepath, 'rb') as f:
      last_lines = list(deque(f, maxlen=500))
    count = len(last_lines)
    i = 0

    while i < count:
      raw_line = last_lines[i]
      clean_line = raw_line.decode('ascii', errors = 'ignore').strip()
      upper_line = clean_line.upper()

      if b"ERROR" in upper_line.encode('ascii') or b"FAILURE" in upper_line.encode('ascii'):
        print(f"Found: {clean_line}")

        for j in range(1,3):
          if i == j < count:
            context = last_lines[i+j].decode('ascii' , errors = 'ignore').strip()
            print(f" --> {context}")
      i += 1
  except Exception as e:
    print(f"exception {filepath} = {e}")

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("server_num")
  args = parser.parse_args()
  path = rf"\\server[args.server_num.strip()]\temp\log\build.log"
  print(f"Scanning: {path}")
    
  if os.path.exists(path):
        scan_last(path)
  else:
        print(f"Error: Path not found - {path}")
