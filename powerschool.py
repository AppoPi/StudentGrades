from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, datetime
from bs4 import BeautifulSoup
import string
import os

class Powerschool:

    URL = 'https://powerschool.vcs.net/guardian/'
    
    def breakpoint(self,msg=""):
        '''Stops execution of code bringing up python console and prints msg'''
        import code, sys
        
        # Use exception trick to pick up the current frame
        try:
            raise None
        except:
            frame = sys.exc_info()[2].tb_frame.f_back
        
        # Evaluate commands in current namespace
        namespace = frame.f_globals.copy()
        namespace.update(frame.f_locals)
        code.interact(banner="-%s>>" % msg, local=namespace)
    
    def __init__(self, name, username, password):
        self.driver = webdriver.Firefox()
        self.name = name.replace(' ','_')
        self.username = username
        self.password = password
        self.login()
        self.grades()
        self.assignments()
        
    def login(self):
        '''Enter credentials and login'''
        self.driver.get(self.URL)
        username = self.driver.find_element_by_id('fieldAccount')
        username.send_keys(self.username)
        
        password = self.driver.find_element_by_id('fieldPassword')
        password.send_keys(self.password)
        
        self.driver.find_element_by_id('btn-enter').click()

    def grades(self):
        '''Get and record grades information'''
        # Parse HTML table
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        output = ''
        printable = set(string.printable)
        for i in soup.find('tbody').find_all('tr'):
            for j in filter(lambda x: x in printable, i.text).split('\n'):
                if j != '\n':
                    output += j + ','
            output += '\n'
            
        self.save('grades', self.name, output) 
    
    def assignments(self):
        '''Get and record assignments information'''
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        table = soup.find('table', {'class': 'grid'})
        rows = table.find('tbody').find_all('tr')
        
        class_URL = []
        for tr in rows:
            cols = tr.findAll('td')
            if len(cols) >= 20:
                for i in cols[13:18]:
                    class_URL.append(self.URL + i.a['href'])
        out = ''
        for i in class_URL:
            self.driver.get(i)
            soup = BeautifulSoup(self.driver.page_source, 'html5lib')
            a = soup.find('table',{'class': None})
            for td in a.findAll('tr'):
                items = td.text.split('\n')
                for j in items:
                    out += u''.join(j[10:]).encode('utf-8').strip().replace('\'', '').replace('\"', '') + ','
                out += '\n'
        self.save('assignments', self.name, out)
        
    def save(self, prefix, name, content):
        '''Saves content to a file in csv format'''
        if not os.path.isdir('output'):
            os.makedirs('output')
            
        with open('output/' + prefix + '_' + name.replace(' ', '_')
            + '_' + datetime.now().strftime('%Y_%m_%d') + '.csv', 'w') as f:
            f.write(content)
    
    def __del__(self):
        '''Destructor'''
        # Log out and close browser
        self.driver.find_element_by_id('btnLogout').click()
        self.driver.close()

if __name__ == "__main__":
    ''' Instantiate the class
        Add users here
        Powerschool([Name], [Username], [Password])'''
    Powerschool('Matthew Burger', 'matthew.burger', '@Vcs7631')