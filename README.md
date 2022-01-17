# hostelApp

STEPS AFTER DOWNLOADING THE CODE
1. Under static folder create 4 empty folders
    1. app_download 
            - deploy your app on web and use gonative.io to covert your web app to mobile app. Store the .apk file AS COLLEGEhostel in the app_download folder
        ![image](https://user-images.githubusercontent.com/95869837/148692654-294dcd52-a8af-4ec7-bd07-26f405a8caab.png)

    2. announcements
   ![image](https://user-images.githubusercontent.com/95869837/148692559-5541761e-795c-4453-87fb-93e992b5dfc7.png)
  
2. edit the url whatsapp://send?text=https://COLLEGEhostelsapp.herokuapp.com/static/app_download/COLLEGEhostel.apk everywhere to your desired web hosted url
    Make sure it points to the apk file.
    
3. Create a free account in fast2sms.com. You will be credited with 50 rs as an entry credit. Copy the api key and paste it in app.py at YOUR FAST2SMS KEY
![image](https://user-images.githubusercontent.com/95869837/148692722-6b116743-bd36-4443-bb33-8cf653ea8b26.png)

4. Before running the app do the following in the terminal 
    >>
        python


    >>
        from app import db


    >>
        db.create_all()


    >>
        from app import Departments
    

    >>
        from app import Years
    
    
    >>
        from app import Admin


    >>
        db.session.add(Admin(admin_id='menshostel',pwd='123',role='Male'))


    >>
        db.session.add(Admin(admin_id='ladieshostel',pwd='123',role='Female'))
    

    >>
        db.session.add(Admin(admin_id='menshostelgate',pwd='123',role='Male'))
    
    
    >>
        db.session.add(Admin(admin_id='ladieshostelgate',pwd='123',role='Female'))


    >>
        db.session.add(Admin(admin_id='maingate',pwd='123',role='MainGate'))


    >>
        db.session.add(Years(year=1))


    >>
        db.session.add(Departments(department='B.Tech IT'))


    >>
        db.create_all()


6. Now make registrations and manage them from the admin panel

    

You are good to go now


SAMPLE SCREENSHOTS

#STUDENT APP
1. Student Login

![image](https://user-images.githubusercontent.com/95869837/148693323-e69e4388-7167-4e2c-b658-27877bd61830.png)


2.Registration

![image](https://user-images.githubusercontent.com/95869837/148693080-71f64694-6449-45c5-ae8e-c7683c8e75d1.png)


3.Applying for outpass

![image](https://user-images.githubusercontent.com/95869837/148693131-445f5942-c833-46fa-bd95-c150c64978b0.png)


4.Common Chat

![image](https://user-images.githubusercontent.com/95869837/148693171-f282fab4-892a-483d-a0b4-3260e840b63e.png)


5.Registered Room Grievances

![image](https://user-images.githubusercontent.com/95869837/148693199-51f4c446-abdf-433b-96d8-e40ecdefc2a8.png)


6. News and announcements
 
![image](https://user-images.githubusercontent.com/95869837/148693231-0c8195ee-09e9-49ac-9496-aee0b27e4ee2.png)


7.Approved Outpass

![image](https://user-images.githubusercontent.com/95869837/148693252-c50ac3f0-f67b-44a9-af17-61fef0006b24.png)


8.Messages sent to parent

![image](https://user-images.githubusercontent.com/95869837/148693418-97453260-1726-4240-b290-11e33cb7782d.png)



#ADMIN

1.Admin Login

![image](https://user-images.githubusercontent.com/95869837/148693913-18f10e1f-8dac-4b02-9a86-e59a6f209933.png)



2.Manage department and years

![image](https://user-images.githubusercontent.com/95869837/148693465-ec6783b1-c30c-403b-84dd-1fb07a340530.png)



3.Manage student details
![image](https://user-images.githubusercontent.com/95869837/148693630-29a84966-d876-4bcb-81fe-d43e8944302a.png)


4.Manage outpass

![image](https://user-images.githubusercontent.com/95869837/148693655-71fb0f12-0b81-4cb6-bffb-7f2b9e510e6f.png)



5.Admin-student chat

![image](https://user-images.githubusercontent.com/95869837/148693675-de0e3057-c80f-48ee-87e1-5a30b49160c9.png)


6. Repairs

![image](https://user-images.githubusercontent.com/95869837/148693723-d3fe45ec-8d24-4412-accc-38018382c0a2.png)



7. Manage news and announcements

![image](https://user-images.githubusercontent.com/95869837/148693749-584ee6fc-a607-428a-a03f-7f8f039c9c13.png)



8. Entry at hostel

![image](https://user-images.githubusercontent.com/95869837/148693788-e7e06aa0-bfa9-49b8-b929-678475009f55.png)



9. Entry at gate

![image](https://user-images.githubusercontent.com/95869837/148693807-0af879c0-b736-45f0-82de-31976f79bdba.png)


Thank you


