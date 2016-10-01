
import code
import sys
import os
from datetime import date, datetime
from pprint import pprint

class School:
    def breakpoint(self,msg=""):
        '''Stops execution of code bringing up python console and prints msg'''
        # Use exception trick to pick up the current frame
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back
        
        # Evaluate commands in current namespace
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)
        code.interact(banner="-%s>>" % msg, local=namespace)
        
    def save(self, prefix, name, content):
        '''Saves content to a file in csv format'''
        if not os.path.isdir('output'):
            os.makedirs('output')
            
        with open('output/' + prefix + '_' + name.replace(' ', '_')
            + '_' + datetime.now().strftime('%Y_%m_%d') + '.csv', 'w') as f:
            f.write(content)