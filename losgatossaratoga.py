from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import school



class StudentGrades(school.School):
    
    URL = 'https://lgsuhsd.instructure.com/login/canvas'

    def __init__(self, name, username, password):
        self.driver = webdriver.Firefox()
        self.name = name.replace(' ','_')
        self.username = username
        self.password = password
        self.login()
        self.grades()
        #self.assignments()
        #self.logout()
            
    def login(self):
        # Enter credentials and login
        self.driver.get(self.URL)
        username = self.driver.find_element_by_id('pseudonym_session_unique_id')
        username.send_keys(self.username)
        
        password = self.driver.find_element_by_id('pseudonym_session_password')
        password.send_keys(self.password)
        
        self.driver.find_element_by_class_name('Button').click()

    def logout(self):
        self.driver.find_element_by_class_name('ic-app-header__menu-list-item').click()
        self.driver.find_element_by_class_name('Button.Button--small').click()

    def grades(self):
        self.driver.get('https://lgsuhsd.instructure.com/grades')

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        rows = soup.findAll('tr')
        grades = []
        for tr in rows:    
            cols = tr.findAll('td')
            for td in cols:
                if td.find(text=True) is None:
                    break
                grades.append(str(td.find(text=True)))
                
        # Grab class names and grades
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        course = soup.find_all(class_='course')
        grade = soup.find_all(class_='percent')
        
        # Build and output string to file
        output = ''
        for i in range(len(course)):
            output += course[i].text.strip() + ',' + grade[i].text.strip() + '\n'
        
        # Save to file
        self.save('grades', self.name, output)
            
    def __del__(self):
        self.driver.close()
    
if __name__ == "__main__":
    # Instantiate the class
    StudentGrades('Casey Braga' , 'cbraga@lghsnt.net', 'cb201034')
