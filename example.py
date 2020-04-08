#This is an example which demonstrates how to call the class defined earlier ("twitterBot") and store different calls with different list based on the call to different variables as desired.

#First run the scripts in twitter_automate.py file ,and after defining the class in it ,run the below code.

#For storing the followers into a list named "followers_list" in python
followers_list = twitterBot("username","password").get_followers()

#For storing the users you are following into a list named "following_list" in python
following_list = twitterBot("username","password").get_following()

#For storing the people who have not followed you but followed by you into a list named "following_list" in python.
unfollower_list = twitterBot("username","password").get_unfollowers()

#For storing followers,follwing and unfollowers as a tuple named "all" in python
all_list = twitterBot("username","password").get_all()



#Excel sheet that provide all the above information as 3 seperate excel sheets in an single excel file.
#The example below is for the function call ".get_all()".You can run the code below for any of the embeded functions within the twitterBot call.
import pandas as pd

writer = pd.ExcelWriter(r'Please provide a complete path where you want to store the excel file(example-C:\Users\excel.xlsx)', engine = 'xlsxwriter')
all_list.to_excel(writer,sheet_name= 'Following')
all_list.to_excel(writer,sheet_name= 'Followers')
all_list.to_excel(writer,sheet_name= 'UnFollowing')
writer.save()
writer.close()

