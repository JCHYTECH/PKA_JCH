"""Check ext4 API - list root first"""
from ext4 import Volume
v = Volume(open('/Users/jchavauxm5/rpi_root.img', 'rb'))

# List root
print("=== Root ===")
for name in v.root.open_dir():
    print(' ', name)
