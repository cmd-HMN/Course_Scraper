from tqdm import tqdm
from _crawler_helper_func import read_cfile, write_cfile
from _config import ScraperConfig

def cleaner(sc: ScraperConfig):
    print('\nStarting Cleaning....')
    try:
        state, links = read_cfile()

        if not state or not links:
            return False
         
        clean_ = []

        total = len(links)
        print(f'Total links: {total}')
        
        pbar = tqdm(links, total=total, desc='Starting cleaning...', colour='red')

        for l in pbar:
            pbar.set_description(f'{l[:40]}')
            if l and any(x in l for x in sc.clean_format):
                clean_.append(l)

        print('Writing File')
        write_cfile(filename=f'{sc.path_}/cleaned.txt', llinks=clean_)
       
        print('\nCleaning Completed\n')
        return True

    except Exception as e:
        print(f'Error : {type(e).__name__}')
        return False
