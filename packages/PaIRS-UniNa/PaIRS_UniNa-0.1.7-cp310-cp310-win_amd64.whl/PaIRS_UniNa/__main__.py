''' PaIRS_UniNa  '''

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='PaIRS_UniNa',description="To launch PaIRS use: \npython -m PaIRS_UniNa  ",formatter_class=argparse.RawDescriptionHelpFormatter)
    # for now only Optional arguments: clean is evaluted first if not set then debug is checked a
    parser.add_argument("-c", "--clean" ,help="Clean the configuration file before starting PaIRS",action="store_true")
    parser.add_argument("-d", "--debug" ,help="Launch PaIRS in debug mode",action="store_true")
    args = parser.parse_args()
    from PaIRS_UniNa import PaIRS
    if args.clean:
        #print ('Clean')
        PaIRS.cleanRun()
    elif args.debug:
        PaIRS.debugRun()
        #print ('Debug')
    else:
        #print ('Normal start ')
        PaIRS.run()
        
    

    '''from PaIRS_UniNa import PaIRS
    if FlagRun==0:
        PaIRS.run()
    elif FlagRun==1:
        PaIRS.cleanRun()
    elif FlagRun==2:
        PaIRS.debugRun()'''
    
