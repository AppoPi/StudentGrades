from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import school
import time # Need sleeps because stupid website

class Mitty(school.School):

    URL = 'https://mitty.myschoolapp.com/app#login'
    
    def getInfo(self, name, username, password):
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
        time.sleep(3)
        username = self.driver.find_element_by_id('Username')
        username.send_keys(self.username)
        
        password = self.driver.find_element_by_id('Password')
        password.send_keys(self.password)
        
        self.driver.find_element_by_id('loginBtn').click()
        
    def logout(self):
        # Log out and close browser
        if 'student' in self.driver.current_url:
            self.driver.find_element_by_id('account-nav').click()
            self.driver.find_element_by_link_text('Sign Out').click()
        else:
            self.driver.find_element_by_xpath("//*[@id='account-nav']/span[2]").click()
            self.driver.find_element_by_xpath("//*[@id='site-user-nav']/div/ul/li[3]/div[2]/ul/li[7]/a").click()
    
    def grades(self):
        '''Get and record grades information'''
        
        time.sleep(10)
        
        # Check for the one-time popup
        try:
            # Close it
            self.driver.find_element_by_class_name('close').click()
        except:
            # If it's not there don't crash
            pass
            
        try:
            # Navigate to grades page
            self.driver.find_element_by_id('children-subnav').click()
        except:
            pass
        
        time.sleep(3)
        source = self.driver.page_source
        
        # Grab class names and grades
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        h3s = soup.find_all('tbody', {'class': 'item-container'})
        h3s = soup.find_all('h3')
        
        output = ''
        for i, x in enumerate(h3s):
            if i % 2 == 0:
                output += x.text.strip().encode('utf-8') + ','
            else:
                output += x.text.strip().encode('utf-8') + '\n'
        
        # Save to file
        self.save('grades', self.name, output)
        
    def assignments(self):
        '''Get and record assignments information'''
        # Open grades modal
        output = ''
        if 'student' in self.driver.current_url:
            self.driver.find_element_by_xpath("//*[contains(text(), 'Show')]").click()
        
        self.driver.find_element_by_class_name('showGrade').click()
        
        # Loop through all the classes
        while(True):
            # Build output from text grabbed from modal table
            output += self.driver.find_element_by_class_name('media-heading').text + '\n'
            soup = BeautifulSoup(self.driver.page_source, 'html5lib')
            tables = soup.find_all('table', {'class': 'table table-striped table-condensed table-mobile-stacked'})
            tds = []
            for t in tables:
                rows = t.find_all('tr')
                for d in rows:
                    tds.append(d)
            
            count = 0
            for i in tds:
                count = 0
                for j in i:
                    if count % 2 == 0:
                        count += 1
                        continue
                    try:
                        text = j.text.encode('ascii', 'replace')
                        text = text.replace(',', '.')
                        if '/' in text:
                            output += '\'' + text + ','
                        else:
                            output += text + ','
                    except:
                        output += j.text[:-1].encode('ascii', 'replace') + ','
                    
                    count += 1
                output += '\n'
            output += '\n'
            
            # Check if next button is active
            next = self.driver.find_element_by_xpath("//*[contains(text(), 'Next Course')]")
            if 'disabled' not in next.get_attribute('class'):
                next.click()
            else:
                self.driver.find_element_by_xpath("//*[contains(text(), 'Close')]").click()
                break
        
        # Save to file
        self.save('assignments', self.name, output)
        
    def __del__(self):
        '''Destructor'''
        self.driver.close()
        
        
if __name__ == "__main__":
    m = Mitty()
    m.browser()
    ''' Instantiate the class
        Add users here
        Mitty([Name], [Username], [Password])'''
    # Now works for both student and parent logins
    m.getInfo('Reese Myers' , 'MyersPa', 'Reesegrades')
    m.getInfo('Kate Picone', 'kathrynpicone18', 'Ang41lik')