from pathlib import Path
import subprocess,sys
subprocess.run([str(Path(__file__).with_name('helper.py')),*sys.argv[1:]],check=True)