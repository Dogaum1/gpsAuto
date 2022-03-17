from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from sal import Sal
import os, time, json

class Core:
    def __init__(self) -> None:
        # sal
        self.sal = Sal()
        #modes
        self.allYearMode    = 0
        self.exceptMode     = 1
        self.intervalMode   = 2
        self.specificMode   = 3

    def start(self):
        # driver
        try:
            self.driver = webdriver.Chrome(f"{os.getcwd()}/Source/chromedriver.exe", chrome_options=self.setup())
        except:
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=self.setup())

        self.driver.get(self.sal.address)

    def setup(self):
        # configuration to print on PDF24
        chrome_options = webdriver.ChromeOptions()
        settings = {
            "recentDestinations": [{
                    "id": "PDF24",
                    "origin": "local",
                    "account": "",
                }],
                "selectedDestinationId": "PDF24",
                "version": 2
            }
        prefs = {'printing.print_preview_sticky_settings.appState': json.dumps(settings)}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument('--kiosk-printing')

        return chrome_options

    def phaseOne(self, categoryValue, nitValue, captchaValue):
       # select category by value -> AUTONOMO | DOMESTICO | FACULTATIVO | SEGURADO_ESPECIAL
        categorySelect = Select(self.driver.find_element(By.ID, self.sal.categoryInputId))
        categorySelect.select_by_value(categoryValue)
        
        # insert nit number
        nitInput = self.driver.find_element(By.ID, self.sal.nitInputId)
        nitInput.click()
        nitInput.send_keys(nitValue); 
       
       # insert captcha check
        captchaInput = self.driver.find_element(By.ID, self.sal.captchaInputId)
        captchaInput.click()
        captchaInput.send_keys(captchaValue)

        # click confirm button
        self.driver.find_element(By.ID, self.sal.firstConfirmButtonId).click()
        self.driver.find_element(By.NAME, self.sal.secondComfirmButtonName).click()

    def phaseTwo(self, year, salary, paymentCodeValue, mode, checked=None):
        paymentCodeSelect = Select(self.driver.find_element(By.ID, self.sal.paymentCodeInputId))
        paymentCodeSelect.select_by_value(paymentCodeValue)

        for i in range(12):
            competanceInputName = f"informarSalariosContribuicaoDomestico:gridSelectSalarios:{i}:j_id38"
            salaryInputName     = f"informarSalariosContribuicaoDomestico:gridSelectSalarios:{i}:j_id40"
            competanceInput     = self.driver.find_element(By.NAME, competanceInputName)
            salaryInput         = self.driver.find_element(By.NAME, salaryInputName)

            if i < 9:
                month = f"0{(i+1)}"    
            else:
                month = f"{(i+1)}"  

            if mode == self.allYearMode:    
                self.submitCompetanceAndSalary(competanceInput, salaryInput, month, year, salary)

            elif mode == self.exceptMode:
                if not month in checked:  
                    self.submitCompetanceAndSalary(competanceInput, salaryInput, month, year, salary)

            elif mode == self.intervalMode:
                if month >= min(checked) and month <= max(checked):
                    self.submitCompetanceAndSalary(competanceInput, salaryInput, month, year, salary)

            elif mode == self.specificMode:
                if month in checked:  
                    self.submitCompetanceAndSalary(competanceInput, salaryInput, month, year, salary)
        
        if mode == self.allYearMode:
            self.januaryFix(year)
        elif mode == self.exceptMode and not "01" in checked:
            self.januaryFix(year)
        elif mode == self.intervalMode and "01" in checked:
            self.januaryFix(year)
        elif mode == self.specificMode and "01" in checked:
            self.januaryFix(year)

        self.driver.find_element(By.NAME, self.sal.thirdComfirmButtonName).click()
        self.phaseThree()

    def submitCompetanceAndSalary(self, competanceInput, salaryInput, month, year, salary):
        competanceInput.click()
        competanceInput.send_keys(f"{month}{year}")
        salaryInput.click()
        salaryInput.send_keys(salary)

    def januaryFix(self, year):
        # january competance fix | try a better resolution later tho!!
        month = "01"
        CompetanceInputName  = "informarSalariosContribuicaoDomestico:gridSelectSalarios:0:j_id38"
        CompatanceInput      = self.driver.find_element(By.NAME, CompetanceInputName)
        CompatanceInput.click()
        CompatanceInput.send_keys(f"{month}{year}")

    def phaseThree(self):
        c = 0
        sequence = []
        
        while True:    
            try:
                c = c + 1
                competanceRowXPath = f'//*[@id="formExibirDiscriminativoCI:gridListSalariosCalculo:tbody_element"]/tr[{c}]/td[2]/span'
                x = int(self.driver.find_element(By.XPATH, competanceRowXPath).get_attribute("innerHTML")[0:2])
                sequence.append(x)
            except:
                break
            
            sequence.sort()
            
        for s in sequence:
            self.generatePdf(s-1, sequence)
    
    # a phase Three complement
    def generatePdf(self, month, sequence):
        valueSequence = []
        p = self.driver.current_window_handle

        for i in range(len(sequence)):
            competanceRowXPath = f'/html/body/div[1]/form[2]/fieldset[2]/table/tbody/tr[{i+1}]/td[2]/span'
            
            x = int(self.driver.find_element(By.XPATH, competanceRowXPath).get_attribute("innerHTML")[0:2]) - 1
            if x == month:
                valueSequence.append(i)
                break

        for index in valueSequence:
            time.sleep(.03)
            xPath = f'//*[@id="gridListSalariosCalculo:selected" and @value={index}]'
            c = self.driver.find_element(By.XPATH, xPath)
            c.click()
            generateGPSButton = self.driver.find_element(By.NAME, self.sal.generateGPSButtonName)
            generateGPSButton.send_keys(Keys.CONTROL + Keys.ENTER)
            c.click()
            time.sleep(2)
            self.driver.switch_to.window(p)

core = Core()