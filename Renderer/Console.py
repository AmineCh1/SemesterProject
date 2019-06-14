import ReadPLY_1
import sys
import subprocess
def main(tab):
        process_tab=[]
        for elem in tab:
                process_tab.append(subprocess.Popen(elem, stdout=subprocess.PIPE))
        exit_codes = [p.wait() for p in process_tab]


    
    
    
