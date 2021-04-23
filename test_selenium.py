from seleniumbase import BaseCase
import pytest
import logging
import time
import uuid
from config import Config
from report import slack_selenium
import sys

class MyTestClass(BaseCase):

    def cdnlogin(self):
        url = "https://pncdn-qa-console.pentium.network/"
        self.open(url)
        logging.info('登入Client')
        self.type('input#email', "alan.lu@pentium.network")
        self.type('input#password', "alan")
        self.click('button[type="submit"]')


    #@pytest.mark.skip
    def test_C217964(self):
        title="點擊Add new site進入Add new site頁面"
        case_id = sys._getframe(0).f_code.co_name[6:]
        logging.info(title)
        try:
            MyTestClass.cdnlogin(self)
            #點擊Add new site
            logging.info('點擊Add new site')
            self.click('span>button[type="button"]')
            #確認進入頁面是否正確
            logging.info('確認進入Distribution')
            self.assert_text("Add new site", ".ant-page-header-heading-title")

            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Mseeage :{e}')
            raise
    
    #@pytest.mark.skip
    def test_C217435(self):
        title="登出後，使用者可再次輸入帳密資訊"
        case_id = sys._getframe(0).f_code.co_name[6:]
        logging.info(title)
        try:
            MyTestClass.cdnlogin(self)
            #點擊登出
            #time.sleep(5)
            logging.info('展開個人資訊menu')
            self.click('#root > section > header > span > span[role="img"]')
            logging.info('點擊logout')
            self.click('.ant-dropdown-menu-item-danger')
            #驗證是否登出成功
            logging.info('確認是否logout')
            time.sleep(0.5)
            if(self.assert_text("You have successfully logged out.", ".ant-message-custom-content")):
                self.assert_element('input#email')
                self.assert_element('input#password')
                #重新登入
                logging.info('重新登入')
                self.type('input#email', "alan.lu@pentium.network")
                self.type('input#password', "alan")
                self.click('button[type="submit"]')
                #驗證是否登入成功
                logging.info('確認是否login成功')
                self.assert_text('Distribution','.ant-page-header-heading-title')

                status=True
                slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
            else:
                raise Exception
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise 
#Jim
    @pytest.mark.skip
    def test_C217324(self):
        title="點擊Add client進入Add client頁面"
        case_id = sys._getframe(0).f_code.co_name[6:]
        url = "https://pncdn-qa-admin.pentium.network/login"
        logging.info(title)
        try:
            self.open(url)
            self.type('input[id="username"]', "admin")
            self.type('input[id="password"]', "admin\n")
            self.click('button[class="ant-btn"]')
            self.assert_element('span[class="ant-page-header-heading-title"]')

            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise 
    
    @pytest.mark.skip
    def test_C217271(self):
        title="登出後，使用者可再次輸入帳密資訊"
        case_id = sys._getframe(0).f_code.co_name[6:]
        url = "https://pncdn-qa-admin.pentium.network/login"
        logging.info(title)
        try:
            self.open(url)
            self.type('input[id="username"]', "admin")
            self.type('input[id="password"]', "admin\n")
            self.click('span[class="ant-avatar ant-avatar-circle ant-avatar-icon ant-dropdown-trigger"]')
            self.click('li[class="ant-dropdown-menu-item ant-dropdown-menu-item-danger ant-dropdown-menu-item-only-child"]')
            self.type('input[id="username"]', "admin")
            self.type('input[id="password"]', "admin\n")
            self.assert_element('span[class="ant-page-header-heading-title"]')

            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise

#vince
    @pytest.mark.skip
    def test_C217222(self):
        title="可在Admin portal 建立未啟用的客戶帳戶"
        case_id = sys._getframe(0).f_code.co_name[6:]
        p_uuid = uuid.uuid4()

        #login
        url = "https://pncdn-qa-admin.pentium.network/"
        logging.info(title)
        try:    
            self.open(url)
            self.type('input#username', "admin")
            self.type('input#password', "admin")
            self.click('button[type="submit"]')
            self.assert_text("Client list", ".ant-page-header-heading-left")

        #addclient
            #Clientsetting
            self.click('button[class="ant-btn"]')
            self.assert_text("Add client", ".ant-page-header-heading-title")
        
            self.type('input#username', (str(p_uuid)))
            self.type('input#password', (str(p_uuid)))
            self.type('input#email', f"{(str(p_uuid))}@gmail.com")
            self.type('input#phone', "0987654321")
            self.click('span[class="ant-radio"]')
            self.click('button[type="submit"]')

            #Finish
            self.assert_text("Successfully added client!", ".ant-result-title")
            self.click('button[class="ant-btn ant-btn-primary"]')

        #確認有無創建成功
            self.assert_text("Client list", ".ant-page-header-heading-left")
            n = len(self.find_elements('tr'))-1
            self.assert_text((str(p_uuid)),f'//tbody/tr[{n}]/td[1]')

            # self.assert_element_present('button[aria-checked="false"]',f"//tbody/tr[{n}]/td[4]")
            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise

    @pytest.mark.skip
    def test_C217295(self):
        title="Account、Password 欄位輸入錯誤，錯誤提示正確，為「Invalid account or password.」"
        case_id = sys._getframe(0).f_code.co_name[6:]
        #login
        url = "https://pncdn-qa-admin.pentium.network/"
        logging.info(title)
        try:
            self.open(url)
            self.type('input#username', "test")
            self.type('input#password', "test")
            self.click('button[type="submit"]')
            self.assert_text("Invalid email or password", ".irPtrP")
            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise

#Jason
    @pytest.mark.skip
    def test_C217551(self):
        title="輸入錯誤Email或密碼點擊登入後具提示「Invalid email or password.」"
        case_id = sys._getframe(0).f_code.co_name[6:]
        url = "https://pncdn-qa-console.pentium.network/login"
        logging.info(title)
        try:
            self.open(url)
            self.type('input[id="email"]', "aaaa")
            self.type('input[id="password"]', "aaaa")
            self.click('button[type="submit"]')
            self.assert_text("Invalid email or password.")
            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise

    @pytest.mark.skip
    def test_C217438(self):
        title="輸入「正確信箱/密碼」可以正確登入 PNCDN 的首頁"
        case_id = sys._getframe(0).f_code.co_name[6:]
        url = "https://pncdn-qa-console.pentium.network/login"
        logging.info(title)
        try:
            self.open(url)
            self.type('input[id="email"]', "jason.chuang@pentium.network")
            self.type('input[id="password"]', "jason")
            self.click('button[type="submit"]')
            self.assert_element('span[title="Distribution"]')
            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise


#Josh
    # 已有必填驗證時，，輸入錯誤格式email後unfocus，必填驗證變為「Invalid email」
    @pytest.mark.skip   
    def test_C217346(self):
        title="已有必填驗證時，，輸入錯誤格式email後unfocus，必填驗證變為「Invalid email」"
        case_id = sys._getframe(0).f_code.co_name[6:]
        url = "https://pncdn-qa-admin.pentium.network/login"
        logging.info(title)
        try:
            self.open(url)
            self.type('input[id="username"]', "admin")
            self.type('input[id="password"]', "admin\n")
            self.click('button[class="ant-btn"]') 
            self.type('input[id="username"]', "josh12")
            self.type('input[id="password"]', "josh12")
            self.type('input[id="email"]', "fewfewfeeffew")
            self.type('input[id="phone"]', "123")
            self.assert_text("Invalid format.")
            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise

    # 輸入「未啟用的帳號/密碼」無法正確登入 PNCDN 的首頁
    @pytest.mark.skip       
    def test_C217440(self):
        title="輸入「未啟用的帳號/密碼」無法正確登入 PNCDN 的首頁"
        case_id = sys._getframe(0).f_code.co_name[6:]
        url = "https://pncdn-qa-console.pentium.network/login"
        logging.info(title)
        try:
            self.open(url)
            self.type('input[id="email"]', "qatest1@gmail.com")
            self.type('input[id="password"]', "qatest1\n")
            self.assert_text("Your account is inactive")
            status=True
            slack_selenium.report(e=None, case_id=case_id, title=title, status=status)
        
        except Exception as e:
            status = False
            slack_selenium.report(e=e, case_id=case_id, title=title, status=status)
            logging.info(f'Error Message :{e}')
            raise
