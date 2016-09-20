from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import school

class Powerschool(school.School):

    URL = 'https://powerschool.vcs.net/guardian/'
    
    def getInfo(self, name, username, password):
        # self.driver = webdriver.Firefox()
        self.name = name.replace(' ','_')
        self.username = username
        self.password = password
        self.login()
        self.grades()
        self.assignments()
        self.logout()
        
    def browser(self):
        self.driver = webdriver.Firefox()
        
    def login(self):
        '''Enter credentials and login'''
        self.driver.get(self.URL)
        username = self.driver.find_element_by_id('fieldAccount')
        username.send_keys(self.username)
        
        password = self.driver.find_element_by_id('fieldPassword')
        password.send_keys(self.password)
        
        self.driver.find_element_by_id('btn-enter').click()
        
    def logout(self):
        self.driver.find_element_by_id('btnLogout').click()
    
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
        
        # Save to file
        self.save('grades', self.name, output) 
    
    def assignments(self):
        '''Get and record assignments information'''
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        table = soup.find('table', {'class': 'grid'})
        rows = table.find('tbody').find_all('tr')
        
        # Grab urls for each class
        class_URL = []
        for tr in rows:
            cols = tr.findAll('td')
            for i in cols:
                try:
                    if 'scores' in i.a['href']:
                        class_URL.append(self.URL + i.a['href'])
                except:
                    pass
        
        # Navigate to and build output from each page
        out = ''
        for i in class_URL:
            self.driver.get(i)
            soup = BeautifulSoup(self.driver.page_source, 'html5lib')
            a = soup.find('table',{'class': None})
            for td in a.findAll('tr'):
                items = td.text.split('\n')
                for j in items:
                    string = u''.join(j[10:])
                    if '/' not in string:
                        out += string.encode('utf-8').strip().replace('\'', '').replace('\"', '') + ','
                    else:
                        out += "'" + string.encode('utf-8').strip().replace('\'', '').replace('\"', '') + ','
                        
                out += '\n'
        
        # Save to file
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
        # Close browser
        self.driver.close()
    
if __name__ == "__main__":
    ps = Powerschool()
    ps.browser()
    ''' Instantiate the class
        Add users here
        ps.getInfo([Name], [Username], [Password])'''
    ps.getInfo('Matthew Burger', 'matthew.burger', '@Vcs7631')
    ps.getInfo('Dominic Henderson', 'dominic.henderson', '@Vcs9447')