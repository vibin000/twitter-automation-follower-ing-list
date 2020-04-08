#Install all the packages if not installed already

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
from collections import OrderedDict

#%%
#Run the code below and define the class "twitterBot".After defining the class ,run help(twitterBot) to better understand what each function inside the class twitterBot does.

class twitterBot:
    """Takes in your username,password and path of the webdriver as strings and 
    gives the user's follower/following list as well as the usernames 
    followed by the user who are not following you back."""
    def __init__(self,username,password,path):
        self.username = username
        self.driver = webdriver.Chrome(executable_path=path)
        self.driver.get("https://twitter.com/login")
        sleep(2)
#The below script will automate your twitter login. 
        self.driver.find_element_by_xpath("//input[@name='session[username_or_email]']").send_keys(username)
        self.driver.find_element_by_xpath("//input[@name='session[password]']").send_keys(password)        
        self.driver.find_element_by_xpath("//div[contains(@data-testid,'LoginForm_Login_Button')]").click()
        sleep(2)
#Click the ok button in case there is an update message from twitter about any of its policies.
        try:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[1]/div[2]/div/div/div/div[2]/div[2]/div/div[2]/div").click()
        except:
            pass
#Now clicking thee homepage icon ,where the followers/following list are embedded.
#The try and except method is used as in some cases(as of now),after the login ,
#the image icon is replaced by twitters own icon ,which have a different source code.        
        try:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/header/div/div/div/div/div[2]/nav/a[7]/div/div/div/div[2]/div/div[2]").click()
        except:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]").click()
        sleep(.5)

    def get_following(self):
        """Function that returns following user name list"""
        self.driver.find_element_by_xpath("//a[@href='/twitvbn/following']").click()
        following_list = self.names_list()
        self.driver.quit()
        return following_list

    def get_followers(self):
        """Function that returns followers username list."""
        self.driver.find_element_by_xpath("//a[@href='/twitvbn/followers']").click()
        followers_list = self.names_list()
        self.driver.quit()
        return followers_list

    def get_unfollowers(self):
        """Function thar returns list of users which you are following but are not following you in return."""
#Fetching the following list
        self.driver.find_element_by_xpath("//a[@href='/twitvbn/following']").click()
        following_list = self.names_list()
        sleep(.5)
#Returning back to home page
        try:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/header/div/div/div/div/div[2]/nav/a[7]/div/div/div/div[2]/div/div[2]").click()
        except:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]").click()
        sleep(.5)

#Fetching the followers list
        self.driver.find_element_by_xpath("//a[@href='/twitvbn/followers']").click()
        followers_list = self.names_list()
        sleep(.2) 
        unfollowers = [names for names in following_list if names not in followers_list]
        self.driver.quit()
        return unfollowers


    def get_all(self):
        """Function that returns following list,followers list and people who you follow but not in return ."""
#Fetching the following list
        self.driver.find_element_by_xpath("//a[@href='/twitvbn/following']").click()
        following_list = self.names_list()
        sleep(.5)
#Returning back to home page
        try:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/header/div/div/div/div/div[2]/nav/a[7]/div/div/div/div[2]/div/div[2]").click()
        except:
            self.driver.find_element_by_xpath("/html/body/div/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[7]").click()
        sleep(.5)

#Fetching the followers list
        self.driver.find_element_by_xpath("//a[@href='/twitvbn/followers']").click()
        followers_list = self.names_list()
        sleep(.2) 
        unfollowers = [names for names in following_list if names not in followers_list]
        self.driver.quit()
        return following_list,followers_list,unfollowers
        

    def names_list(self):
        """Function that returns user name list for following or followers function above."""
        names = []
#Storing the class of source code which as of now (April 2020),is same for all names in twitter following/followers list.        
        class_following = "css-1dbjc4n r-my5ep6 r-qklmqi r-1adg3ll"
        previous_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            page_source = self.driver.page_source
            sleep(1)
            soup = BeautifulSoup(page_source, "lxml")
            sleep(.5)    
            name_list = soup.findAll("div",{"class":class_following})
#Since the trending section and twitters recommendation list have the exact same class which we defined above,
#in order to extract only the userid in followers or following list ,links with hrefs are taken ,which are then indexed for the usernames.
#Recommendation lists and other unsueful stuffs can be filtered in this way.
            for name in name_list:
                try:
                    names.append(name.a["href"].strip()[1:])
                except:
                    pass

#As during each scroll ,a single userid is parsed multiple times ,OrderedDict library is used to remove duplicates and sort it it order.    
            names= list(OrderedDict.fromkeys(names))
#Initiating scrolling .Here the page(followwers or following) is scrolled down, while storing the list of names in each scroll.
           
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        
            # Calculating the new height after page scroll
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            
            if new_height== previous_height:
                break
            previous_height = new_height
        
        return names
          
   
