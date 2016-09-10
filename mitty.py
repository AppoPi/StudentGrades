from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, datetime
from bs4 import BeautifulSoup
import string
import os
import time
import re

class Mitty:
    
    # URL = 'https://my.mitty.com/login/index.php'
    URL = 'https://mitty.myschoolapp.com/app#login'
    
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
        time.sleep(3)
        username = self.driver.find_element_by_id('Username')
        username.send_keys(self.username)
        
        password = self.driver.find_element_by_id('Password')
        password.send_keys(self.password)
        
        self.driver.find_element_by_id('loginBtn').click()
    
    def grades(self):
        '''Get and record grades information'''
        
        time.sleep(10)
        
        # Check for the one-time popup
        try:
            # Close it
            self.driver.find_element_by_class_name('close').click()
        except:
            pass
        
        # Navigate to grades page
        self.driver.find_element_by_id('children-subnav').click()
        
        time.sleep(3)
        source = self.driver.page_source
        
        # Grab class names and grades
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        h3s = soup.find_all('tbody', {'class': 'item-container'})
        h3s = soup.find_all('h3')
        
        output = ''
        for i in range(0, len(h3s), 2):
            output += re.sub(',',  '', h3s[i].text) + ',' + h3s[i+1].text + '\n'
        output = output.encode('utf8')
        filename = self.save('grades', self.name, output)
            
    def assignments(self):
        '''Get and record assignments information'''
        self.breakpoint()
        # soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        # class_URL = []
        
        # table = soup.find('table', {'class': 'flexible boxaligncenter generaltable'})
        # rows = table.find('tbody').find_all('tr')
        
        # for row in rows:
            # if row.a:
                    # class_URL.append(row.a['href'])
        
        # output = ''
        # printable = set(string.printable)
        # for index in range(0, len(class_URL) - 1):
            # self.driver.get(class_URL[index])
            # soup = BeautifulSoup(self.driver.page_source, 'html5lib')
            
            # for i in soup.find_all('th')[:7]:
                # output += str(filter(lambda x: x in printable, i.text.replace(',', ''))).strip() + ','
            # output += '\n'
            # for i in soup.find('tbody').find_all('tr'):
                # if i.text != u'\n':
                    # for j in filter(lambda x: x in printable, i.text.replace(',', '')).strip().split('\n'):
                        # output += j + ','
                    # output += '\n'
            # output += '\n'
        
        # self.save('assignments', self.name, output)
    
    def save(self, prefix, name, content):
        '''Saves content to a file in csv format'''
        if not os.path.isdir('output'):
            os.makedirs('output')
        
        name = 'output/' + prefix + '_' + name.replace(' ', '_') + '_' + datetime.now().strftime('%Y_%m_%d') + '.csv'
        with open(name, 'w') as f:
            f.write(content)
        return name
            
    def __del__(self):
        '''Destructor'''
        # Log out and close browser
        # self.driver.find_element_by_id('action-menu-toggle-0').click()
        # self.driver.find_element_by_id('actionmenuaction-6').click()
        self.driver.close()


if __name__ == "__main__":
    ''' Instantiate the class
        Add users here
        Mitty([Name], [Username], [Password])'''
    Mitty('Reese Myers' , 'MyersPa', 'Reesegrades')