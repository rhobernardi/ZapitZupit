import os

os.mkdir("/img/")
os.mkdir("/logs/")

if os.path.exists("/img"):
    print("[*] Created /img path.")
else:
    print("[!] Error to create /img path.")
