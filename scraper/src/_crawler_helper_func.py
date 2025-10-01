import time
import threading
import sys
import select
from tqdm import tqdm       

def write_cfile(llinks, filename='crawler.txt'):
    try:
        with open(filename, "w") as f:
            for link in llinks:
                f.write(str(link) + "\n")
    except:
        print('Writing goes wrong.')

def read_cfile(filename='crawler.txt'):
    try:
        with open(filename, 'r') as f:
            file = f.read()
            file_exits = (len(file) != 0)
            return file_exits, file.split('\n')
    except:
        file_exits = False
        return file_exits, None

def rest_for_min(crawler, minu:float = 1, pos=1):
    minu = int(minu * 60)
    stop_flag = {"skip": False, "done": False}
    
    def wait_for_enter(stop_flag):
        while not stop_flag["done"]:
            if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                input() 
                stop_flag["skip"] = True
                return
        
    t = threading.Thread(target=wait_for_enter, args=(stop_flag,), daemon=True)
    t.start()
    try:
        pbar = tqdm(range(minu), desc="Resting...[Enter to skip/ Ctrl + C to cancel]", position=pos, colour="green")
        for i in pbar:
            if stop_flag["skip"]:
                stop_flag["done"] = True
                pbar.set_description('Skipping.......[Enter Pressed!]')
                break
            remaining = minu - i
            pbar.set_description(f"Resting... {remaining}s left")
            time.sleep(1)
        stop_flag["done"] = True
    except KeyboardInterrupt:
        print("\nExiting program...")
        crawler.exit()
        stop_flag["done"] = True
        sys.exit()
