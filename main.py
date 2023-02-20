import os
import time
import threading


def main():
    while True:
        th1 = threading.Thread(target=lancement_process)
        th1.start()
        time.sleep(210)

def lancement_process():
    os.system("python pronote.py")



main()
