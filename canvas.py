from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import school

class StudentGrades(school.School):
    
    URL = 'https://lgsuhsd.instructure.com/login/canvas'
    BASE = 'https://lgsuhsd.instructure.com'

    def __init__(self, name, username, password):
        self.driver = webdriver.Chrome()
        self.name = name.replace(' ','_')
        self.username = username
        self.password = password
        self.login()
        self.grades()
        self.assignments()
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
    
    def assignments(self):
        soup = BeautifulSoup(self.driver.page_source, 'html5lib')
        resultSet = soup.findAll(class_='course')
        urls = []
        for x in resultSet:
                    urls.append(x.a['href'])

            
        output = u''
        for h in urls:
            # Navigate to each class
            self.driver.get(self.BASE + h)
            
            for i in soup:
                soup = BeautifulSoup(self.driver.page_source, 'html5lib')
                table = soup.find(lambda tag: tag.name=='table' and 
                    tag.has_attr('id') and 
                    tag['id'] == 'grades_summary')


                # class name
                output += Select(self.driver.find_element_by_id('course_url')).first_selected_option.text + '\n'

                # table headers
                data = table.findAll(lambda tag: tag.name=='tr' or tag.name=='th')
                for i in range(1, 5):
                    output += data[i].text + u','

                output += '\n'

                # assignment names
                assignmentNames = []
                assignments = table.findAll(lambda tag: tag.name == 'a' and tag.has_attr('href') and '/courses/' in tag['href'])
                for i in assignments:
                    assignmentNames.append(i.text.replace(',', ' '))
                
                print assignmentNames
                
                # due date
                # dueDate = []
                # due = table.findAll(lambda tag: tag.name == 'td' and tag.has_attr('class') and 'due' in tag['class'])
                # for i in due:
                    # item = u''.join(i.text).encode('utf-8').strip()
                    # dueDate.append(item)

                # dueDate  = dueDate[:-5]

                # points earned
                grades = []
                grades = table.findAll(lambda tag: tag.name == 'span' and tag.has_attr('class') and 'grade' in tag['class'])
                pointsEarned = []
                for i in grades:
                    item0 = u''.join(i.text).encode('utf-8').strip()
                    # remove whitespace
                    item1 = item0.replace(u' ', u'').replace(u'\n', u'')
                    # remove junk
                    item2 = item1.replace(u'Clicktotestadifferentscore', u'')
                    # save remainder
                    pointsEarned.append(item2)

                pointsEarned = pointsEarned[:-5]

                '''
                # points possible
                pointsOutOf = []
                grades = table.findAll(lambda tag: tag.name == 'td' and tag.has_attr('class') and 'points_possible' in tag['class'])[:-1]
                for i in grades:
                    pointsOutOf.append(i.text)

                ofFinal = pointsOutOf[-4:]
                pointsOutOf = pointsOutOf[:-4]

                self.breakpoint()
                '''
                for i in range(len(assignmentNames)):
                    output += assignmentNames[i] + ',' + pointsEarned[i] + '\n'# + pointsOutOf[i] + '\n'
                
        # Save to file
        self.save('assignments', self.name, output)
        
    def __del__(self):
        self.driver.close()
    
if __name__ == "__main__":
    # Instantiate the class
    StudentGrades('Casey Braga' , 'cbraga@lghsnt.net', 'cb201034')
