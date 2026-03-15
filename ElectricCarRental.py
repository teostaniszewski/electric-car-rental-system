import sqlite3 # Import the SQLite library for database operations
from appjar import gui # Import the AppJar library for creating graphical user interfaces
import re # Importing the "re" module, which provides support for regular expressions in Python
import time # Importing the "time" module, which provides various time-related functions
import smtplib # Imports the smtplib module, which allows the program to send emails using the Simple Mail Transfer Protocol (SMTP).
import random  # Imports the random module, which provides functions for generating random numbers and selecting random elements.
from datetime import datetime, timedelta  # Import datetime and timedelta classes for date and time manipulation
import os
import sys

def resource_path(filename):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)

con = sqlite3.connect("ElectricCarRentalDb.db") # Establish a connection to the SQLite database
cur = con.cursor() # Create a cursor object to execute SQL commands on the database

# Function to create the database tables
def createDB():
    # Create the users table
    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_users (
            userID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            firstName TEXT NOT NULL,
            lastName TEXT NOT NULL,
            userPassword TEXT NOT NULL,
            contactNumber TEXT NOT NULL,
            userEmail TEXT NOT NULL
    )""")

    # Create the vehicles table
    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_vehicles (
            vehicleID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            vehicleName TEXT NOT NULL,
            vehicleType TEXT NOT NULL,
            seatingCapacity INTEGER DEFAULT 0,
            luggageCapacity TEXT NOT NULL,
            Stock INTEGER NOT NULL 
    )""")

    # Create the bookings table
    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_bookings (
            bookingID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            userID INTEGER NOT NULL,
            bookingRef TEXT NOT NULL,
            bookingPickupDate TEXT NOT NULL,
            bookingDropoffDate TEXT NOT NULL,
            bookingPickUpTime TEXT NOT NULL,
            bookingDropoffTime TEXT NOT NULL,
            totalDuration INTEGER NOT NULL,
            FOREIGN KEY(userID) REFERENCES tbl_users(userID)
    )""")

    # Create the booking details table
    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_bookingDetails (
            detailsID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            bookingID INTEGER NOT NULL,
            vehicleID INTEGER NOT NULL,
            pricePerDay FLOAT NOT NULL,
            totalCost FLOAT NOT NULL,
            FOREIGN KEY(bookingID) REFERENCES tbl_bookings(bookingID),
            FOREIGN KEY(vehicleID) REFERENCES tbl_vehicles(vehicleID)
    )""")

    # Create the favourites table
    cur.execute("""CREATE TABLE IF NOT EXISTS tbl_favourites (
            favouriteID INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
            userID INTEGER NOT NULL,
            vehicleID INTEGER NOT NULL,
            FOREIGN KEY(userID) REFERENCES tbl_users(userID),
            FOREIGN KEY(vehicleID) REFERENCES tbl_vehicles(vehicleID)
    )""")

    con.commit() # Commits changes to the database

createDB() # Calls function that creates database

#####################################################################################################################################################
#####################################################################################################################################################

def populateDatabase():  # Function to populate the database

    # Populate tbl_users table with data from the CSV file
    with open(resource_path("tbl_users.csv"), "r", encoding="cp1252") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            userID, firstName, lastName, userPassword, contactNumber, userEmail = line.split(",")

            cur.execute("SELECT * FROM tbl_users WHERE userID = ?", [userID])
            existing_record = cur.fetchone()

            if existing_record is None:
                cur.execute(
                    "INSERT INTO tbl_users (userID, firstName, lastName, userPassword, contactNumber, userEmail) VALUES (?, ?, ?, ?, ?, ?)",
                    [userID, firstName, lastName, userPassword, contactNumber, userEmail]
                )

    con.commit()

    # Populate tbl_vehicles table
    with open(resource_path("tbl_vehicles.csv"), "r", encoding="cp1252") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            vehicleID, vehicleName, vehicleType, seatingCapacity, luggageCapacity, Stock = line.split(",")

            cur.execute("SELECT * FROM tbl_vehicles WHERE vehicleID = ?", [vehicleID])
            existing_record = cur.fetchone()

            if existing_record is None:
                cur.execute(
                    "INSERT INTO tbl_vehicles (vehicleID, vehicleName, vehicleType, seatingCapacity, luggageCapacity, Stock) VALUES (?, ?, ?, ?, ?, ?)",
                    [vehicleID, vehicleName, vehicleType, seatingCapacity, luggageCapacity, Stock]
                )

    con.commit()
    #print("Vehicles table has been populated")  # Print a confirmation message

    # Populate tbl_bookings table
    #file = open("tbl_bookings.csv", "r")  # Open the CSV file containing booking data in read mode
    #for line in file:  # Loop through each line in the file
        #line = line.strip()  # Remove any leading/trailing whitespace or newline characters
        # Split the CSV line into individual values based on commas
        #bookingID, bookingRef, userID, bookingDate, bookingTime, totalDuration = line.split(",")

        # Execute a SELECT query to check if a booking with the same bookingID already exists
        #cur.execute("SELECT * FROM tbl_bookings WHERE bookingID = ?", [bookingID])
        #existing_record = cur.fetchone()

        #if existing_record is None:  # If no existing record is found, insert a new booking record
            #cur.execute(
                #"INSERT INTO tbl_bookings (bookingID, bookingRef, userID, bookingDate, bookingTime, totalDuration) VALUES (?, ?, ?, ?, ?, ?)",
                #[bookingID, bookingRef, userID, bookingDate, bookingTime, totalDuration])

    #con.commit()  # Commit the transaction to permanently save changes to the database
    #print("Bookings table has been populated")  # Print a confirmation message

    # Populate tbl_bookingDetails table
    #file = open("tbl_bookingDetails.csv", "r")  # Open the CSV file containing booking details in read mode
    #for line in file:  # Loop through each line in the file
        #line = line.strip()  # Remove any leading/trailing whitespace or newline characters
        # Split the CSV line into individual values based on commas
        #detailsID, bookingID, vehicleID, pricePerDay, totalCost = line.split(",")

        # Execute a SELECT query to check if a booking detail with the same detailsID already exists
        #cur.execute("SELECT * FROM tbl_bookingDetails WHERE detailsID = ?", [detailsID])
        #existing_record = cur.fetchone()

        #if existing_record is None:  # If no existing record is found, insert a new booking details record
            #cur.execute(
                #"INSERT INTO tbl_bookingDetails (detailsID, bookingID, vehicleID, pricePerDay, totalCost) VALUES (?, ?, ?, ?, ?)",
                #[detailsID, bookingID, vehicleID, pricePerDay, totalCost])

    #con.commit()  # Commit the transaction to permanently save changes to the database
    #print("BookingDetails table has been populated")  # Print a confirmation message

    # Populate tbl_favourites table
    #file = open("tbl_favourites.csv", "r")  # Open the CSV file containing favourites data in read mode
    #for line in file:  # Loop through each line in the file
        #line = line.strip()  # Remove any leading/trailing whitespace or newline characters
        # Split the CSV line into individual values based on commas
        #favouriteID, userID, vehicleID = line.split(",")

        # Execute a SELECT query to check if a favourite with the same favouriteID already exists
        #cur.execute("SELECT * FROM tbl_favourites WHERE favouriteID = ?", [favouriteID])
        #existing_record = cur.fetchone()

        #if existing_record is None:  # If no existing record is found, insert a new favourite record
            #cur.execute("INSERT INTO tbl_favourites (favouriteID, userID, vehicleID) VALUES (?, ?, ?)",
                        #[favouriteID, userID, vehicleID])

    #con.commit()  # Commit the transaction to permanently save changes to the database
    #print("Favourites table has been populated")  # Print a confirmation message


populateDatabase() # Call function to populate database

#####################################################################################################################################################
#####################################################################################################################################################

app = gui("ElectricCarRental", "1000x500") # Create the app instance whilst setting size of first window
app.setIcon(resource_path("favicon.ico"))

def createInterface():  # Function to create the interface

    # HOME PAGE #
    app.setResizable(False)  # Disable window resizing to maintain layout consistency

    app.setBg("white", override=True) # Makes the background colour of the window white
    app.addImage("homepage_logo", "CarLogo.gif", colspan=2) # Places an image of the main logo on the window
    app.setLocation(500,250) # Window appears at this location when open

    app.startFrame("frame_homepage", colspan=2)  # Start a frame to group homepage elements, spanning 2 columns
    app.addLabel("EmptyLabel_homepage", "")  # Add an empty label for spacing
    app.setSticky("n")  # Align elements to the top of the frame and to be in the center

    app.addNamedButton("LOGIN", "btnLogin", btnPress) # Adds a button to take user to login
    app.setButtonWidth("btnLogin", 200)  # Set the width of the "LOGIN" button
    app.addNamedButton("SIGN UP", "btnSignup", btnPress) # Adds a button to take user to signup
    app.setButtonWidth("btnSignup", 200)  # Set the width of the "SIGN UP" button

    app.setButtonImage("btnLogin", "LOGINBUTTON.gif") # Places the login button image on the login button
    app.setButtonBg("btnLogin", "white") # Changes background of button to white
    app.setButtonRelief("btnLogin", "flat") # Ensures that there is no depth or styling to the button
    app.getButtonWidget("btnLogin").config(activebackground="white", highlightthickness=0, bd=0) # Ensures that there is no highlight on button press

    app.setButtonImage("btnSignup", "SIGNUPBUTTON.gif") # Places the signup button image on the signup button
    app.setButtonBg("btnSignup", "white") # Changes background of button to white
    app.setButtonRelief("btnSignup", "flat") # Ensures that there is no depth or styling to the button
    app.getButtonWidget("btnSignup").config(activebackground="white", highlightthickness=0, bd=0) # Ensures that there is no highlight on button press

    app.stopFrame()  # End the homepage frame
    # END OF HOME PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

    # LOGIN PAGE #
    app.startSubWindow("win_Login", title="ElectricCarRental")  # Create a sub-window for the login page
    app.setSize("1000x500")  # Set the window size to 1000 by 500 pixels
    app.setResizable(False)  # Disable window resizing to maintain layout consistency
    app.setLocation(500, 250)  # Set the window"s initial position on screen

    # Back button configuration
    app.addNamedButton("Back", "btnBackToHomeFromLogin", btnPress)  # Add back button to return to homepage
    app.getButtonWidget("btnBackToHomeFromLogin").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position top-left with padding

    # Window styling and logo
    app.setBg("white", override=True)  # Set white background colour
    app.addImage("login_logo", "Small_CarLogo.gif")  # Add smaller version of logo
    app.getImageWidget("login_logo").grid(row=0, column=1, sticky="ne", padx=20, pady=10)  # Position logo top-right

    # Login header section
    app.startFrame("frame_login1", row=0, column=0, colspan=2).grid(sticky="n")  # Create frame for header elements
    app.addLabel("lb_login", "Login").config(font="Arial 40 bold")  # Main title with styling
    app.addLabel("lb_loginprompt", "Sign in to continue.")  # Subtitle text
    app.stopFrame()  # End header frame

    app.setLabelFg("lb_loginprompt", "grey")  # Set subtitle text colour to grey

    # Email input field
    app.addEntry("Login Email", row=1, column=0, colspan=3)  # Create email input field
    app.getEntryWidget("Login Email").config(bd=3, width=30)  # Set border width and field size
    app.getEntryWidget("Login Email").grid(pady=4, ipady=4)  # Add vertical padding
    app.setEntryDefault("Login Email", "Email Address")  # Set placeholder text
    app.setEntryLowerCase("Login Email")  # Convert input to lowercase

    # Password input field
    app.addSecretEntry("Login Password", row=5, column=0, colspan=3)  # Create password field
    app.getEntryWidget("Login Password").config(bd=3, width=30)  # Set border width and field size
    app.getEntryWidget("Login Password").grid(pady=4, ipady=4)  # Add vertical padding
    app.setEntryDefault("Login Password", "Password")  # Set placeholder text

    # Password visibility toggle
    app.addNamedButton("", "btnShowPassword", lambda: toggle_password("Login Password", "btnShowPassword"), row=5,column=1, colspan=3)

    # Bottom section (forgot password + sign in)
    app.startFrame("frame_login2", colspan=2)  # Create frame for bottom elements
    app.addLink("Forgot Password?",lambda: (app.hideSubWindow("win_Login"), btnPress("btnForgotPassword")))  # Forgot password link
    app.getLinkWidget("Forgot Password?").config(font="Arial 11 underline")  # Style link text
    app.setLinkFg("Forgot Password?", "#136ebf")  # Set link colour to blue

    app.addNamedButton("SIGN IN", "btnMenuFromLogin", btnPress)  # Add sign in button
    app.getButtonWidget("btnMenuFromLogin").grid(pady=5, ipady=5)  # Add padding
    app.stopFrame()  # End bottom section

    # Sign-up prompt section
    app.addLabel("EmptyLabel_Login2", "")  # Empty label for spacing
    app.startFrame("frame_login_link", row=8, column=0, colspan=3)  # Create frame for sign-up prompt
    app.addLabel("Login Link_prefix", "Don't have an account? ", column=0, row=0)  # Prompt text
    app.setLabelFg("Login Link_prefix", "grey")  # Set text colour
    app.addLink("Login Link", lambda: (app.hideSubWindow("win_Login"), btnPress("btnSignup")), column=1,row=0)  # Sign-up link
    app.setLinkFg("Login Link", "green")  # Set link colour
    app.getLinkWidget("Login Link").config(text="Sign up")  # Set link text
    app.stopFrame()  # End sign-up prompt frame

    # Button styling configurations
    app.setButtonImage("btnMenuFromLogin", "SIGNINBUTTON.gif")  # Set sign in button image
    app.setButtonBg("btnMenuFromLogin", "white")  # White background colour
    app.setButtonRelief("btnMenuFromLogin", "flat")  # Remove 3D effect
    app.getButtonWidget("btnMenuFromLogin").config(activebackground="white", highlightthickness=0,bd=0)  # Remove highlights/borders

    app.setButtonImage("btnBackToHomeFromLogin", "HOMEBUTTON.gif")  # Set back button image
    app.setButtonBg("btnBackToHomeFromLogin", "white")  # White background colour
    app.setButtonRelief("btnBackToHomeFromLogin", "flat")  # Remove 3D effect
    app.getButtonWidget("btnBackToHomeFromLogin").config(activebackground="white", highlightthickness=0,bd=0)  # Remove highlights/borders

    app.setButtonImage("btnShowPassword", "ClosedEye.gif")  # Set password toggle image
    app.setButtonBg("btnShowPassword", "white")  # White background colour
    app.setButtonRelief("btnShowPassword", "flat")  # Remove 3D effect
    app.getButtonWidget("btnShowPassword").config(activebackground="white", highlightthickness=0,bd=0)  # Remove highlights/borders

    app.stopSubWindow()  # Close login sub-window
    # END LOGIN PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

    # CREATE ACCOUNT PAGE #
    app.startSubWindow("win_Signup",title="ElectricCarRental")  # Create a sub-window for the signup page with the title "ElectricCarRental"
    app.setSize("1000x500")  # Set the size of the signup window to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing to maintain a consistent layout
    app.setLocation(500, 250)  # Set the position of the signup window on the screen

    app.addNamedButton("Back", "btnBackToHomeFromSignup",btnPress)  # Add a "Back" button to return to the homepage, linked to the btnPress function
    app.getButtonWidget("btnBackToHomeFromSignup").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button in the top-left corner with padding

    app.setBg("white", override=True)  # Set the background colour of the window to white
    app.addImage("signup_logo", "Small_CarLogo.gif")  # Add an image (logo) to the signup window
    app.getImageWidget("signup_logo").grid(row=0, column=1, rowspan=2, sticky="ne", padx=20,pady=10)  # Position the logo in the top-right corner with padding

    app.startFrame("frame_signup1", row=0, column=0, colspan=2).grid(sticky="n")  # Start a frame for the title and login link, spanning 2 columns
    app.addLabel("lb_signup", "Create An Account", row=0).config(font="Arial 35 bold")  # Add a title label for the signup page
    app.addLabel("Signup Link_prefix", "Already have an account? ", row=1,column=0)  # Add prefix text before the login link
    app.setLabelFg("Signup Link_prefix", "grey")  # Set the colour of the prefix text to grey
    app.addLink("Signup Prompt", lambda: (app.hideSubWindow("win_Signup"), btnPress("btnLogin")))  # Add a clickable login link that triggers the btnPress function
    app.setLinkFg("Signup Prompt", "green")  # Set the login link colour to green
    app.getLinkWidget("Signup Prompt").config(text="Login")  # Set the display text of the login link to "Login"
    app.stopFrame()  # End the title frame

    # Add entry fields for user details with labels and placeholders
    app.addEntry("Signup FirstName", row=1, column=0, colspan=2)  # Entry field for first name
    app.getEntryWidget("Signup FirstName").config(bd=3, width=30)  # Set border depth and width
    app.setEntryDefault("Signup FirstName", "First Name")  # Placeholder for first name
    app.getEntryWidget("Signup FirstName").grid(pady=3, ipady=3)  # Add padding for spacing

    app.addEntry("Signup LastName", row=2, column=0, colspan=2)  # Entry field for last name
    app.getEntryWidget("Signup LastName").config(bd=3, width=30)  # Set border depth and width
    app.setEntryDefault("Signup LastName", "Last Name")  # Placeholder for last name
    app.getEntryWidget("Signup LastName").grid(pady=3, ipady=3)  # Add padding for spacing

    app.addEntry("Signup Email", row=3, column=0, colspan=2)  # Entry field for email
    app.getEntryWidget("Signup Email").config(bd=3, width=30)  # Set border depth and width
    app.setEntryDefault("Signup Email", "Email Address")  # Placeholder for email
    app.setEntryLowerCase("Signup Email")  # Automatically convert email input to lowercase
    app.getEntryWidget("Signup Email").grid(pady=3, ipady=3)  # Add padding for spacing

    app.addEntry("Signup PhoneNum", row=4, column=0, colspan=2)  # Entry field for phone number
    app.getEntryWidget("Signup PhoneNum").config(bd=3, width=30)  # Set border depth and width
    app.setEntryDefault("Signup PhoneNum", "Phone Number")  # Placeholder for phone number
    app.getEntryWidget("Signup PhoneNum").grid(pady=3, ipady=3)  # Add padding for spacing

    app.addSecretEntry("Signup Password", row=5, column=0, colspan=2)  # Secret entry for password
    app.getEntryWidget("Signup Password").config(bd=3, width=30)  # Set border depth and width
    app.setEntryDefault("Signup Password", "Password")  # Placeholder for password
    app.getEntryWidget("Signup Password").grid(pady=3, ipady=3)  # Add padding for spacing

    # Add an eye icon button to toggle password visibility
    app.addNamedButton("", "btnShowSignupPassword", lambda: toggle_password("Signup Password", "btnShowSignupPassword"),row=5, column=1, colspan=3)

    app.addSecretEntry("Signup ReEnterPass", row=6, column=0, colspan=2)  # Secret entry for re-entering password
    app.getEntryWidget("Signup ReEnterPass").config(bd=3, width=30)  # Set border depth and width
    app.setEntryDefault("Signup ReEnterPass", "Re-Enter Password")  # Placeholder for re-entering password
    app.getEntryWidget("Signup ReEnterPass").grid(pady=3, ipady=3)  # Add padding for spacing

    # Add an eye icon button to toggle re-entered password visibility
    app.addNamedButton("", "btnShowSignupPassword2",lambda: toggle_password("Signup ReEnterPass", "btnShowSignupPassword2"), row=6, column=1,colspan=3)

    app.addNamedButton("SIGN UP", "btnMenuFromSignup", btnPress,colspan=2)  # Add a "SIGN UP" button, linked to the btnPress function
    app.getButtonWidget("btnMenuFromSignup").grid(padx=30, pady=5, ipadx=100,ipady=5)  # Position the "SIGN UP" button with padding

    app.setButtonImage("btnBackToHomeFromSignup", "HOMEBUTTON.gif")  # Set image for the "Back" button
    app.setButtonBg("btnBackToHomeFromSignup", "white")  # Set the background of the "Back" button to white
    app.setButtonRelief("btnBackToHomeFromSignup", "flat")  # Remove raised 3D effect from the "Back" button
    # Configure "Back" button to remove borders and keep background white when active
    app.getButtonWidget("btnBackToHomeFromSignup").config(activebackground="white", highlightthickness=0,bd=0)

    app.setButtonImage("btnMenuFromSignup", "BIG_SIGNUPBUTTON.gif")  # Set image for the "SIGN UP" button
    app.setButtonBg("btnMenuFromSignup", "white")  # Set the background of the "SIGN UP" button to white
    app.setButtonRelief("btnMenuFromSignup", "flat")  # Remove raised 3D effect from the "SIGN UP" button
    # Configure "SIGN UP" button to remove borders and keep background white when active
    app.getButtonWidget("btnMenuFromSignup").config(activebackground="white", highlightthickness=0,bd=0)

    app.setButtonImage("btnShowSignupPassword","Small_ClosedEye.gif")  # Set image (closed eye) for password toggle button
    app.setButtonBg("btnShowSignupPassword", "white")  # Set background to white
    app.setButtonRelief("btnShowSignupPassword", "flat")  # Make button flat with no raised edge
    app.getButtonWidget("btnShowSignupPassword").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button style for consistent appearance

    app.setButtonImage("btnShowSignupPassword2","Small_ClosedEye.gif")  # Set image (closed eye) for re-enter password toggle button
    app.setButtonBg("btnShowSignupPassword2", "white")  # Set background to white
    app.setButtonRelief("btnShowSignupPassword2", "flat")  # Make button flat
    app.getButtonWidget("btnShowSignupPassword2").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button style for consistent appearance

    app.stopSubWindow()  # End the sub-window for the signup page
    # END OF CREATE ACCOUNT PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

    # FORGOTTEN PASSWORD PAGES #
    # FORGOTTEN PASSWORD 1 #
    app.startSubWindow("win_ForgotPassword1",title="ElectricCarRental")  # Create a sub-window for the forgotten password page with the title "ElectricCarRental"
    app.setSize("1000x500")  # Set the size of the window to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing to maintain layout consistency
    app.setLocation(500, 250)  # Position the window on the screen

    app.addNamedButton("Back", "btnForgotPasswordBack1",btnPress)  # Add a "Back" button to return to the previous page, linked to the btnPress function
    app.getButtonWidget("btnForgotPasswordBack1").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button in the top-left corner with padding

    app.setBg("white", override=True)  # Set the background colour of the window to white
    app.addImage("forgottenpass1_logo", "Small_CarLogo.gif")  # Add a logo image to the top-right
    app.getImageWidget("forgottenpass1_logo").grid(row=0, column=1, rowspan=2, sticky="ne", padx=20,pady=10)  # Position the image with padding

    app.startFrame("frame_forgotPassword1", row=0, column=0, colspan=2).grid(sticky="n")  # Start a frame for the title and instruction label, spanning 2 columns
    app.addLabel("lb_forgotPassword1", "Forgot Password").config(font="Arial 35 bold")  # Add a title label for the forgotten password page
    app.addLabel("lb_forgottenpasswordprompt","Enter email address to reset password.")  # Instruction label for email entry
    app.stopFrame()  # End the title frame

    app.setLabelFg("lb_forgottenpasswordprompt", "grey")  # Set the instruction label colour to grey

    app.startFrame("frame_forgotPassword2", row=1, column=0, colspan=2)  # Start a frame for the email entry and button
    app.addEntry("ForgotPassword Email")  # Add entry field for email input
    app.getEntryWidget("ForgotPassword Email").config(bd=3)  # Set border depth for styling
    app.getEntryWidget("ForgotPassword Email").grid(pady=4, ipady=4)  # Add padding for spacing
    app.setEntryDefault("ForgotPassword Email", "Email Address")  # Placeholder for email input
    app.setEntryLowerCase("ForgotPassword Email")  # Automatically convert input to lowercase

    app.addLabel("EmptyLabel_ForgotPassword1", "")  # Empty label for spacing or layout alignment
    app.addNamedButton("CONTINUE", "btnForgotPasswordNext1",btnPress)  # Add a "CONTINUE" button to proceed with password reset, linked to btnPress function
    app.getButtonWidget("btnForgotPasswordNext1").grid(pady=5, ipady=5)  # Position the "CONTINUE" button with padding
    app.setButtonWidth("btnForgotPasswordNext1", 300)  # Set button width for uniform appearance
    app.stopFrame()  # End the email entry frame

    app.startFrame("frame_forgot_password_link", row=9, column=0, colspan=3)  # Frame for the signup link
    app.addLabel("Forgot Password Link_prefix", "Don't have an account? ", column=0,row=0)  # Label before the signup link
    app.setLabelFg("Forgot Password Link_prefix", "grey")  # Set label text colour to grey
    app.addLink("Forgot Password Link", lambda: (app.hideSubWindow("win_ForgotPassword1"), btnPress("btnSignup")),column=1, row=0)  # Add a link to open the signup page
    app.setLinkFg("Forgot Password Link", "green")  # Set link colour to green
    app.getLinkWidget("Forgot Password Link").config(text="Sign up")  # Set link display text
    app.stopFrame()  # End the frame for the link

    app.setButtonImage("btnForgotPasswordBack1", "BACKBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnForgotPasswordBack1", "white")  # Set the button background colour to white
    app.setButtonRelief("btnForgotPasswordBack1", "flat")  # Remove raised effect to make the button flat
    app.getButtonWidget("btnForgotPasswordBack1").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button styling

    app.setButtonImage("btnForgotPasswordNext1", "CONTINUEBUTTON.gif")  # Set the image for the "CONTINUE" button
    app.setButtonBg("btnForgotPasswordNext1", "white")  # Set the button background to white
    app.setButtonRelief("btnForgotPasswordNext1", "flat")  # Remove raised edge effect
    app.getButtonWidget("btnForgotPasswordNext1").config(activebackground="white", highlightthickness=0,bd=0)  # Apply consistent button styling

    app.stopSubWindow()  # End the sub-window for the forgotten password page
    # END OF FORGOTTEN PASSWORD 1 #

#####################################################################################################################################################
#####################################################################################################################################################

    # FORGOTTEN PASSWORD 2 #
    app.startSubWindow("win_ForgotPassword2",title="ElectricCarRental")  # Create a sub-window for the second forgotten password step with the title "ElectricCarRental"
    app.setSize("1000x500")  # Set the size of the window to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing to maintain layout consistency
    app.setLocation(500, 250)  # Position the window on the screen

    app.addNamedButton("Back", "btnForgotPasswordBack2",btnPress)  # Add a "Back" button to return to the previous page, linked to the btnPress function
    app.getButtonWidget("btnForgotPasswordBack2").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button in the top-left corner with padding

    app.setBg("white", override=True)  # Set the background colour of the window to white
    app.addImage("forgottenpass2_logo", "Small_CarLogo.gif")  # Add a logo image to the top-right
    # Position the image with padding
    app.getImageWidget("forgottenpass2_logo").grid(row=0, column=1, rowspan=2, sticky="ne", padx=20,pady=10)

    app.startFrame("frame_forgotPassword3", row=0, column=0, colspan=2).grid(sticky="n")  # Start a frame for the title and instruction label, spanning 2 columns
    app.addLabel("lb_forgotPassword2", "Forgot Password").config(font="Arial 35 bold")  # Add a title label for the forgotten password step 2 page
    app.addLabel("lb_forgottenpasswordprompt2","Enter code provided to reset password.")  # Instruction label for code entry
    app.stopFrame()  # End the title frame

    app.setLabelFg("lb_forgottenpasswordprompt2", "grey")  # Set the instruction label colour to grey

    app.startFrame("frame_forgotPassword4", row=1, column=0, colspan=2)  # Start a frame for the code entry and button
    app.addEntry("ForgotPassword Code")  # Add numeric entry field for inputting the reset code
    app.getEntryWidget("ForgotPassword Code").config(bd=3)  # Set border depth for styling
    app.getEntryWidget("ForgotPassword Code").grid(pady=4, ipady=4)  # Add padding for spacing
    app.setEntryDefault("ForgotPassword Code", "Code")  # Placeholder for reset code input
    app.setEntryMaxLength("ForgotPassword Code", 4)  # Restrict the entry to a 4-digit code

    app.addLabel("EmptyLabel_ForgotPassword2", "")  # Empty label for spacing

    app.addNamedButton("CONTINUE", "btnForgotPasswordNext2",btnPress)  # Add a "CONTINUE" button to proceed with password reset, linked to btnPress function
    app.getButtonWidget("btnForgotPasswordNext2").grid(pady=5, ipady=5)  # Position the "CONTINUE" button with padding
    app.setButtonWidth("btnForgotPasswordNext2", 300)  # Set button width for uniform appearance
    app.stopFrame()  # End the code entry frame

    app.startFrame("frame_forgot_password_link2", row=9, column=0,colspan=3)  # Start a frame for the link to signup page
    app.addLabel("Forgot Password Link_prefix2", "Don't have an account? ", column=0,row=0)  # Label before the signup link
    app.setLabelFg("Forgot Password Link_prefix2", "grey")  # Set label colour to grey
    app.addLink("Forgot Password Link2", lambda: (app.hideSubWindow("win_ForgotPassword2"), btnPress("btnSignup")),column=1, row=0)  # Add a link to open the signup page
    app.setLinkFg("Forgot Password Link2", "green")  # Set link colour to green
    app.getLinkWidget("Forgot Password Link2").config(text="Sign up")  # Set display text for the link
    app.stopFrame()  # End the frame for the link

    app.setButtonImage("btnForgotPasswordBack2", "BACKBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnForgotPasswordBack2", "white")  # Set the background of the back button to white
    app.setButtonRelief("btnForgotPasswordBack2", "flat")  # Remove raised effect to make the button flat
    app.getButtonWidget("btnForgotPasswordBack2").config(activebackground="white", highlightthickness=0,bd=0)  # Style the back button for consistency

    app.setButtonImage("btnForgotPasswordNext2", "CONTINUEBUTTON.gif")  # Set the image for the "CONTINUE" button
    app.setButtonBg("btnForgotPasswordNext2", "white")  # Set the background of the continue button to white
    app.setButtonRelief("btnForgotPasswordNext2", "flat")  # Remove the button border for a flat look
    app.getButtonWidget("btnForgotPasswordNext2").config(activebackground="white", highlightthickness=0,bd=0)  # Style the continue button for consistency

    app.stopSubWindow()  # End the sub-window for the forgotten password step 2 page
    # END OF FORGOTTEN PASSWORD 2 #

#####################################################################################################################################################
#####################################################################################################################################################

    # FORGOTTEN PASSWORD 3 #
    app.startSubWindow("win_ForgotPassword3",title="ElectricCarRental")  # Create a sub-window for the third forgotten password step with the title "ElectricCarRental"
    app.setSize("1000x500")  # Set the size of the window to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing to maintain layout consistency
    app.setLocation(500, 250)  # Position the window on the screen

    app.addNamedButton("Back", "btnForgotPasswordBack3",btnPress)  # Add a "Back" button to return to the previous page, linked to the btnPress function
    app.getButtonWidget("btnForgotPasswordBack3").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button in the top-left corner with padding

    app.setBg("white", override=True)  # Set the background colour of the window to white
    app.addImage("forgottenpass3_logo", "Small_CarLogo.gif")  # Add a logo image to the top-right
    # Position the image with padding
    app.getImageWidget("forgottenpass3_logo").grid(row=0, column=1, rowspan=3, sticky="ne", padx=20,pady=10)

    app.startFrame("frame_forgotPassword5", row=0, column=0, colspan=2).grid(sticky="n")  # Start a frame for the title and instruction label, spanning 2 columns
    app.addLabel("lb_forgotPassword3", "Forgot Password").config(font="Arial 35 bold")  # Add a title label for the forgotten password step 3 page
    app.addLabel("lb_forgottenpasswordprompt3", "Enter your new password.")  # Instruction label for password entry
    app.stopFrame()  # End the title frame

    app.setLabelFg("lb_forgottenpasswordprompt3", "grey")  # Set instruction label colour to grey

    app.addSecretEntry("ForgotPassword_NewPass", row=2, column=0,colspan=3)  # Add entry field for new password (masked)
    app.getEntryWidget("ForgotPassword_NewPass").config(bd=3, width=32)  # Set border depth and width for styling
    app.setEntryDefault("ForgotPassword_NewPass", "Password")  # Placeholder for new password input
    app.getEntryWidget("ForgotPassword_NewPass").grid(pady=4, ipady=4)  # Add vertical padding for spacing

    # Add toggle visibility button for new password
    app.addNamedButton("", "btnShowForgotPassword",lambda: toggle_password("ForgotPassword_NewPass", "btnShowForgotPassword"), row=2, column=1,colspan=3)

    app.addSecretEntry("ForgotPassword_ReEnterPass", row=3, column=0,colspan=3)  # Add entry field for re-entering password (masked)
    app.getEntryWidget("ForgotPassword_ReEnterPass").config(bd=3, width=32)  # Set border depth and width for styling
    app.setEntryDefault("ForgotPassword_ReEnterPass", "Re-Enter Password")  # Placeholder for re-entering password
    app.getEntryWidget("ForgotPassword_ReEnterPass").grid(pady=4, ipady=4)  # Add vertical padding for spacing

    # Add toggle visibility button for re-entered password
    app.addNamedButton("", "btnShowForgotPassword2",lambda: toggle_password("ForgotPassword_ReEnterPass", "btnShowForgotPassword2"), row=3, column=1,colspan=3)

    app.addNamedButton("CONFIRM", "btnForgotPasswordNext3", btnPress, row=4, column=0,colspan=2)  # Add a "CONFIRM" button to proceed with the password change, linked to btnPress function
    app.getButtonWidget("btnForgotPasswordNext3").grid(pady=5, ipady=5)  # Position the "CONFIRM" button with padding
    app.setButtonWidth("btnForgotPasswordNext3", 300)  # Set button width for uniform appearance

    app.addLabel("EmptyLabel_ForgotPassword4", "")  # Empty label for spacing

    app.startFrame("frame_forgot_password_link3", colspan=3)  # Start a frame for the signup link at the bottom
    app.addLabel("Forgot Password Link_prefix3", "Don't have an account? ", column=0,row=0)  # Label before the signup link
    app.setLabelFg("Forgot Password Link_prefix3", "grey")  # Set label colour to grey
    app.addLink("Forgot Password Link3", lambda: (app.hideSubWindow("win_ForgotPassword3"), btnPress("btnSignup")),column=1, row=0)  # Add a link to open the signup page
    app.setLinkFg("Forgot Password Link3", "green")  # Set link colour to green
    app.getLinkWidget("Forgot Password Link3").config(text="Sign up")  # Set display text for the link
    app.stopFrame()  # End the frame for the link

    app.setButtonImage("btnForgotPasswordBack3", "BACKBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnForgotPasswordBack3", "white")  # Set the background of the back button to white
    app.setButtonRelief("btnForgotPasswordBack3", "flat")  # Remove raised effect to make the button flat
    app.getButtonWidget("btnForgotPasswordBack3").config(activebackground="white", highlightthickness=0,bd=0)  # Style the back button for consistency

    app.setButtonImage("btnForgotPasswordNext3", "UPDATEBUTTON.gif")  # Set the image for the "CONFIRM" button
    app.setButtonBg("btnForgotPasswordNext3", "white")  # Set the background of the confirm button to white
    app.setButtonRelief("btnForgotPasswordNext3", "flat")  # Remove the button border for a flat look
    app.getButtonWidget("btnForgotPasswordNext3").config(activebackground="white", highlightthickness=0,bd=0)  # Style the confirm button for consistency

    app.setButtonImage("btnShowForgotPassword","ClosedEye.gif")  # Set the image for the toggle visibility button on new password
    app.setButtonBg("btnShowForgotPassword", "white")  # Set the background of the toggle button to white
    app.setButtonRelief("btnShowForgotPassword", "flat")  # Remove raised effect for flat appearance
    app.getButtonWidget("btnShowForgotPassword").config(activebackground="white", highlightthickness=0,bd=0)  # Style the toggle visibility button

    app.setButtonImage("btnShowForgotPassword2","ClosedEye.gif")  # Set the image for the toggle visibility button on re-entered password
    app.setButtonBg("btnShowForgotPassword2", "white")  # Set the background of the toggle button to white
    app.setButtonRelief("btnShowForgotPassword2", "flat")  # Remove raised effect for flat appearance
    app.getButtonWidget("btnShowForgotPassword2").config(activebackground="white", highlightthickness=0,bd=0)  # Style the toggle visibility button

    app.stopSubWindow()  # End the sub-window for the forgotten password step 3 page
    # END OF FORGOTTEN PASSWORD 3 #
    # END OF FORGOTTEN PASSWORD PAGES #

#####################################################################################################################################################
#####################################################################################################################################################

    # MENU PAGE #
    app.startSubWindow("win_Menu",title="ElectricCarRental")  # Create a sub-window for the main menu with the title "ElectricCarRental"
    app.setSize("1000x500")  # Set the size of the window to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing to maintain layout consistency
    app.setLocation(500, 250)  # Position the window on the screen

    app.addNamedButton("LOGOUT", "btnLogout", btnPress)  # Add a "LOGOUT" button linked to the btnPress function
    app.getButtonWidget("btnLogout").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "LOGOUT" button in the top-left corner with padding

    app.setBg("white", override=True)  # Set the background colour of the menu to white
    app.addImage("mainmenu_logo", "Small_CarLogo.gif")  # Add a company logo image
    # Position the logo in the top-right with padding
    app.getImageWidget("mainmenu_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)

    app.startFrame("Menu Page Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Start a frame for the page title and description, spanning 4 columns
    app.addLabel("lb_menu", "Main Menu").config(font="Arial 40 bold")  # Add a large title label for the main menu
    app.addLabel("mainmenu_prompt","Pick an option to book, manage, or review your rentals.")  # Add an instruction label to guide the user
    app.stopFrame()  # End the title/instruction frame

    app.setLabelFg("mainmenu_prompt", "grey")  # Set the prompt label colour to grey for visual hierarchy

    app.startFrame("Menu_Images", row=2, colspan=6)  # Start a frame to hold the main menu option buttons with images
    # Booking button
    app.addNamedButton("BOOK NOW", "btnBooking", btnPress, row=1,column=0)  # Add a "BOOK NOW" button linked to the booking system
    app.setButtonImage("btnBooking", "mainmenu_booking_image.gif")  # Set the image for the booking button
    app.setButtonBg("btnBooking", "white")  # Set the background colour to white
    app.setButtonRelief("btnBooking", "flat")  # Flatten the button for a modern look
    app.getButtonWidget("btnBooking").config(activebackground="white", highlightthickness=0,bd=0)  # Remove border/highlight on click

    # Spacer between buttons
    app.addLabel("spacer1menu", "", row=1, column=1)  # Add a blank spacer label between booking and view trips
    app.setLabelWidth("spacer1menu", 4)  # Define spacer width

    # View Trips button
    app.addNamedButton("VIEW TRIPS", "btnViewTrips", btnPress, row=1,column=2)  # Add a "VIEW TRIPS" button to see past/future bookings
    app.setButtonImage("btnViewTrips", "view_mainmenu.gif")  # Set the image for the view trips button
    app.setButtonBg("btnViewTrips", "white")  # Set background colour to white
    app.setButtonRelief("btnViewTrips", "flat")  # Remove button depth
    app.getButtonWidget("btnViewTrips").config(activebackground="white", highlightthickness=0,bd=0)  # Consistent styling for flat image button

    # Spacer between buttons
    app.addLabel("spacer2menu", "", row=1, column=3)  # Add another spacer label between view trips and favourites
    app.setLabelWidth("spacer2menu", 4)  # Define spacer width

    # Favourites button
    app.addNamedButton("FAVOURITES", "btnFavourites", btnPress, row=1,column=4)  # Add a "FAVOURITES" button to access user"s favourite vehicles
    app.setButtonImage("btnFavourites", "favourite_mainmenu.gif")  # Set the image for the favourites button
    app.setButtonBg("btnFavourites", "white")  # Set background to white for visual consistency
    app.setButtonRelief("btnFavourites", "flat")  # Make button flat
    app.getButtonWidget("btnFavourites").config(activebackground="white", highlightthickness=0,bd=0)  # Remove default button borders and effects
    app.stopFrame()  # End the main menu buttons frame

    # Style the logout button similarly
    app.setButtonImage("btnLogout", "LOGOUTBUTTON.gif")  # Set the image for the logout button
    app.setButtonBg("btnLogout", "white")  # Set background to white
    app.setButtonRelief("btnLogout", "flat")  # Flatten the button
    app.getButtonWidget("btnLogout").config(activebackground="white", highlightthickness=0,bd=0)  # Style the logout button

    app.stopSubWindow()  # End the sub-window for the menu page
    # END OF MENU PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

    # BOOKING PAGES #
    # BOOKING PAGE 1 #
    app.startSubWindow("win_Booking1",title="ElectricCarRental")  # Create a sub-window for Booking Page 1 with the title "ElectricCarRental"
    app.setSize("1000x500")  # Set the size of the window to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing to maintain layout consistency
    app.setLocation(500, 250)  # Position the window at (500, 250)

    # Add a "Back" button for navigation
    app.addNamedButton("Back", "btnBookingBack1", btnPress).grid(sticky="nw", padx=20, pady=10, ipadx=10, ipady=10)

    app.setBg("white", override=True)  # Set the background colour to white
    app.addImage("booking1_logo", "Small_CarLogo.gif")  # Add a logo image for the page
    app.getImageWidget("booking1_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position the logo image

    app.startFrame("Booking Page Frame", row=0, column=0,colspan=4)  # Start a frame for the booking title, spanning 3 columns
    app.addLabel("lb_booking1", "Create Booking").config(font="Arial 35 bold")  # Add a title label for the booking page
    app.addLabel("bookingpage_prompt", "Select filters to customise your search.")  # Instruction label for user actions
    app.stopFrame()  # End the title frame

    app.setLabelFg("bookingpage_prompt", "grey")  # Set the colour of the instruction label to grey

    app.addLabel("spacerbooking1", "")  # Add a spacer label for layout spacing

    app.startFrame("Filter:", sticky="ew",colspan=4)  # Create a label frame for the filters, allowing it to stretch horizontally
    app.setBg("#F0F0F0")  # Set background colour for the filter frame
    app.setPadding([20, 15])  # Set padding for the label frame

    # Add labels and radio buttons for car category filter
    app.addLabel("category_label", "Car category").config(font="Arial 14 bold")  # Label for car category
    app.getLabelWidget("category_label").grid(row=0, column=0, sticky="n")  # Position category label
    app.addRadioButton("category", "Small")  # Radio button for small car category
    app.getRadioButtonWidget("category", "Small").grid(row=1, column=0, sticky="n")  # Position small car option
    app.addRadioButton("category", "Medium")  # Radio button for medium car category
    app.getRadioButtonWidget("category", "Medium").grid(row=2, column=0, sticky="n")  # Position medium car option
    app.addRadioButton("category", "Large")  # Radio button for large car category
    app.getRadioButtonWidget("category", "Large").grid(row=3, column=0, sticky="n")  # Position large car option

    # Add labels and radio buttons for price filter
    app.addLabel("price_label", "Price per day").config(font="Arial 14 bold")  # Label for price filter
    app.getLabelWidget("price_label").grid(row=0, column=1, sticky="n")  # Position price label
    app.addRadioButton("price", "£0–£50")  # Radio button for price range £0–£50
    app.getRadioButtonWidget("price", "£0–£50").grid(row=1, column=1, sticky="n")  # Position £0–£50 option
    app.addRadioButton("price", "£50–£100")  # Radio button for price range £50–£100
    app.getRadioButtonWidget("price", "£50–£100").grid(row=2, column=1, sticky="n")  # Position £50–£100 option
    app.addRadioButton("price", "£100–£150")  # Radio button for price range £100–£150
    app.getRadioButtonWidget("price", "£100–£150").grid(row=3, column=1, sticky="n")  # Position £100–£150 option

    # Add labels and radio buttons for seats available filter
    app.addLabel("seats_label", "Seats available").config(font="Arial 14 bold")  # Label for seats available filter
    app.getLabelWidget("seats_label").grid(row=0, column=2, sticky="n")  # Position seats label
    app.addRadioButton("seats", "2 Seats")  # Radio button for 2 seats option
    app.getRadioButtonWidget("seats", "2 Seats").grid(row=1, column=2, sticky="n")  # Position 2 seats option
    app.addRadioButton("seats", "5 Seats")  # Radio button for 5 seats option
    app.getRadioButtonWidget("seats", "5 Seats").grid(row=2, column=2, sticky="n")  # Position 5 seats option
    app.addRadioButton("seats", "7 Seats")  # Radio button for 7 seats option
    app.getRadioButtonWidget("seats", "7 Seats").grid(row=3, column=2, sticky="n")  # Position 7 seats option

    # Add labels and radio buttons for luggage filter
    app.addLabel("luggage_label", "Luggage").config(font="Arial 14 bold")  # Label for luggage filter
    app.getLabelWidget("luggage_label").grid(row=0, column=3, sticky="n")  # Position luggage label
    app.addRadioButton("luggage", "1 Small Bag")  # Radio button for 1 small bag option
    app.getRadioButtonWidget("luggage", "1 Small Bag").grid(row=1, column=3, sticky="n")  # Position 1 small bag option
    app.addRadioButton("luggage", "2 Small Bags")  # Radio button for 2 small bags option
    app.getRadioButtonWidget("luggage", "2 Small Bags").grid(row=2, column=3,sticky="n")  # Position 2 small bags option
    app.addRadioButton("luggage", "3+ Small Bags")  # Radio button for 3+ small bags option
    app.getRadioButtonWidget("luggage", "3+ Small Bags").grid(row=3, column=3,sticky="n")  # Position 3+ small bags option

    app.stopFrame()  # End the filters label frame

    app.addNamedCheckBox("Search All Cars", "bookingPageCheckBox", colspan=4)  # Adds a checkbox to search all cars

    def update_radio_buttons():  # Function to enable/disable radio buttons based on the checkbox state
        if app.getCheckBox("bookingPageCheckBox"):  # Checks if the "Search All Cars" checkbox is selected
            app.getRadioButtonWidget("category", "Small").config(state="disabled")  # Disables the "Small" category radio button
            app.getRadioButtonWidget("category", "Medium").config(state="disabled")  # Disables the "Medium" category radio button
            app.getRadioButtonWidget("category", "Large").config(state="disabled")  # Disables the "Large" category radio button

            app.getRadioButtonWidget("price", "£0–£50").config(state="disabled")  # Disables the "£0–£50" price range radio button
            app.getRadioButtonWidget("price", "£50–£100").config(state="disabled")  # Disables the "£50–£100" price range radio button
            app.getRadioButtonWidget("price", "£100–£150").config(state="disabled")  # Disables the "£100–£150" price range radio button

            app.getRadioButtonWidget("seats", "2 Seats").config(state="disabled")  # Disables the "2 Seats" radio button
            app.getRadioButtonWidget("seats", "5 Seats").config(state="disabled")  # Disables the "5 Seats" radio button
            app.getRadioButtonWidget("seats", "7 Seats").config(state="disabled")  # Disables the "7 Seats" radio button

            app.getRadioButtonWidget("luggage", "1 Small Bag").config(state="disabled")  # Disables the "1 Small Bag" radio button
            app.getRadioButtonWidget("luggage", "2 Small Bags").config(state="disabled")  # Disables the "2 Small Bags" radio button
            app.getRadioButtonWidget("luggage", "3+ Small Bags").config(state="disabled")  # Disables the "3+ Small Bags" radio button
        else:
            app.getRadioButtonWidget("category", "Small").config(state="normal")  # Enables the "Small" category radio button
            app.getRadioButtonWidget("category", "Medium").config(state="normal")  # Enables the "Medium" category radio button
            app.getRadioButtonWidget("category", "Large").config(state="normal")  # Enables the "Large" category radio button

            app.getRadioButtonWidget("price", "£0–£50").config(state="normal")  # Enables the "£0–£50" price range radio button
            app.getRadioButtonWidget("price", "£50–£100").config(state="normal")  # Enables the "£50–£100" price range radio button
            app.getRadioButtonWidget("price", "£100–£150").config(state="normal")  # Enables the "£100–£150" price range radio button

            app.getRadioButtonWidget("seats", "2 Seats").config(state="normal")  # Enables the "2 Seats" radio button
            app.getRadioButtonWidget("seats", "5 Seats").config(state="normal")  # Enables the "5 Seats" radio button
            app.getRadioButtonWidget("seats", "7 Seats").config(state="normal")  # Enables the "7 Seats" radio button

            app.getRadioButtonWidget("luggage", "1 Small Bag").config(state="normal")  # Enables the "1 Small Bag" radio button
            app.getRadioButtonWidget("luggage", "2 Small Bags").config(state="normal")  # Enables the "2 Small Bags" radio button
            app.getRadioButtonWidget("luggage", "3+ Small Bags").config(state="normal")  # Enables the "3+ Small Bags" radio button

    app.setCheckBoxChangeFunction("bookingPageCheckBox",update_radio_buttons)  # Sets the function to update radio buttons when the checkbox state changes

    app.addNamedButton("SEARCH", "btnBookingNext1", btnPress,colspan=4)  # Adds a "SEARCH" button with specified width and height
    app.setButtonWidth("btnBookingNext1", 300)  # Set the width of the "SEARCH" button
    app.setButtonHeight("btnBookingNext1", 60)  # Set the height of the "SEARCH" button

    # Button styling for "Back" button
    app.setButtonImage("btnBookingBack1", "HOMEBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnBookingBack1", "white")  # Set the background colour for the "Back" button to white
    app.setButtonRelief("btnBookingBack1", "flat")  # Set the relief of the "Back" button to flat (no 3D effect)
    # Customise the appearance of the "Back" button with specific active background, highlight thickness, and border
    app.getButtonWidget("btnBookingBack1").config(activebackground="white", highlightthickness=0, bd=0)

    # Button styling for "SEARCH" button
    app.setButtonImage("btnBookingNext1", "SEARCHBUTTON.gif")  # Set the image for the "SEARCH" button
    app.setButtonBg("btnBookingNext1", "white")  # Set the background colour for the "SEARCH" button to white
    app.setButtonRelief("btnBookingNext1", "flat")  # Set the relief of the "SEARCH" button to flat (no 3D effect)
    # Customise the appearance of the "SEARCH" button with specific active background, highlight thickness, and border
    app.getButtonWidget("btnBookingNext1").config(activebackground="white", highlightthickness=0, bd=0)

    app.stopSubWindow()  # End the sub-window for Booking Page 1
    # END OF BOOKING PAGE 1

#####################################################################################################################################################
#####################################################################################################################################################

    # List of available times for booking
    times_list = ["08:30", "09:30", "10:30", "11:30", "12:30", "13:30", "14:30", "15:30", "16:30", "17:30", "18:30"]

    def get_dates():  # Function to generate a list of dates starting from today or the next day
        dates_list = []  # Initialise an empty list to store dates
        current_time = datetime.now().time()  # Get the current time
        last_time = datetime.strptime(times_list[-1], "%H:%M").time()  # Get the last available time from the times_list
        current_date = datetime.now().date()  # Get the current date

        if current_time <= last_time:  # If the current time is before the last available time, start from today
            start_day = current_date
        else:  # Otherwise, start from the next day
            start_day = current_date + timedelta(days=1)

        for i in range(20):  # Generate a list of dates for the next 20 days
            date = start_day + timedelta(days=i)  # Add "i" days to the start day
            dates_list.append(date.strftime("%d %b %Y"))  # Format the date as "Day Month Year" and add to the list

        return dates_list  # Return the list of dates

    def get_times(pickup_date):  # Function to generate a list of available times based on the selected pickup date
        current_time = datetime.now().time()  # Get the current time
        current_date = datetime.now().date()  # Get the current date
        time_options = ["- Choose Time -"]  # Initialise the list with a default option

        pickup_date_obj = datetime.strptime(pickup_date,"%d %b %Y").date()  # Convert the pickup_date string to a date object

        if pickup_date_obj == current_date:  # If the pickup date is today, filter times to only show future times
            for t in times_list:
                t_time = datetime.strptime(t, "%H:%M").time()  # Convert the time string to a time object
                if t_time > current_time:  # If the time is in the future, add it to the list
                    time_options.append(t)
                else:  # Otherwise, mark it as unavailable
                    time_options.append(f"- {t} -")
        else:  # If the pickup date is in the future, all times are available
            time_options.extend(times_list)

        return time_options  # Return the list of available times

    dates_list = get_dates()  # Generate the list of dates
    pickup_times = get_times(dates_list[0])  # Initialise pickup_times with the times for the first date

    def update_pickup():  # Function to update the pickup time options when the pickup date changes
        pickup_date = app.getOptionBox("pickup_date")  # Get the selected pickup date

        if pickup_date == "- Choose Date -":  # If no date is selected, reset the pickup time options
            app.changeOptionBox("pickup_time", ["- Choose Time -"])
            return

        new_pickup_times = get_times(pickup_date)  # Get the updated list of pickup times for the selected date
        app.changeOptionBox("pickup_time", new_pickup_times)  # Update the pickup time options

    def update_dropoff():  # Function to update the drop-off date and time options based on the selected pickup date and time
        pickup_date = app.getOptionBox("pickup_date")  # Get the selected pickup date
        pickup_time = app.getOptionBox("pickup_time")  # Get the selected pickup time
        dropoff_date = app.getOptionBox("dropoff_date")  # Get the selected drop-off date

        # If no pickup date or time is selected, disable the drop-off date and time options
        if pickup_date == "- Choose Date -" or pickup_time == "- Choose Time -" or pickup_time is None:
            app.changeOptionBox("dropoff_date", ["- Choose Date -"] + dates_list)
            app.changeOptionBox("dropoff_time", ["- Choose Time -"] + times_list)
            app.getOptionBoxWidget("dropoff_date").config(state="disabled")
            app.getOptionBoxWidget("dropoff_time").config(state="disabled")
            return

        app.getOptionBoxWidget("dropoff_date").config(state="normal")  # Enable the drop-off date options
        app.getOptionBoxWidget("dropoff_time").config(state="normal")  # Enable the drop-off time options

        pickup_date_index = dates_list.index(pickup_date)  # Get the index of the selected pickup date in the dates_list
        valid_dropoff_dates = dates_list[pickup_date_index:]  # Generate a list of valid drop-off dates starting from the pickup date

        if dropoff_date == pickup_date:  # If the drop-off date is the same as the pickup date, filter times to only show future times
            valid_dropoff_times = ["- Choose Time -"]
            for t in times_list:
                if t > pickup_time:  # If the time is after the pickup time, add it to the list
                    valid_dropoff_times.append(t)
                else:  # Otherwise, mark it as unavailable
                    valid_dropoff_times.append(f"- {t} -")
        else:  # If the drop-off date is in the future, all times are available
            valid_dropoff_times = ["- Choose Time -"] + times_list

        app.changeOptionBox("dropoff_date", ["- Choose Date -"] + valid_dropoff_dates)  # Update the drop-off date options
        app.changeOptionBox("dropoff_time", valid_dropoff_times)  # Update the drop-off time options

        if dropoff_date in valid_dropoff_dates:  # If the previously selected drop-off date is still valid, keep it selected
            app.setOptionBox("dropoff_date", dropoff_date)

    def update_dropoff_date():  # Function to update the drop-off time options when the drop-off date changes
        dropoff_date = app.getOptionBox("dropoff_date")  # Get the selected drop-off date
        pickup_date = app.getOptionBox("pickup_date")  # Get the selected pickup date
        pickup_time = app.getOptionBox("pickup_time")  # Get the selected pickup time

        if dropoff_date == "- Choose Date -":  # If no drop-off date is selected, reset the drop-off time options
            app.changeOptionBox("dropoff_time", ["- Choose Time -"] + times_list)
            return

        if dropoff_date == pickup_date:  # If the drop-off date is the same as the pickup date, filter times to only show future times
            valid_dropoff_times = ["- Choose Time -"]
            for t in times_list:
                if t > pickup_time:  # If the time is after the pickup time, add it to the list
                    valid_dropoff_times.append(t)
                else:  # Otherwise, mark it as unavailable
                    valid_dropoff_times.append(f"- {t} -")
        else:  # If the drop-off date is in the future, all times are available
            valid_dropoff_times = ["- Choose Time -"] + times_list

        app.changeOptionBox("dropoff_time", valid_dropoff_times)  # Update the drop-off time options

    app.startSubWindow("win_Booking3", title="ElectricCarRental")  # Create a sub-window for Booking Page 3
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the location of the window to coordinates (500, 250)

    app.addNamedButton("Back", "btnBookingBack3",btnPress)  # Add a "Back" button for navigation and bind it to btnPress function
    app.getButtonWidget("btnBookingBack3").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button at the top-left corner with padding and internal padding

    app.setBg("white",override=True)  # Set the background color of the sub-window to white, overriding any default background
    app.addImage("booking3_logo", "Small_CarLogo.gif")  # Add the logo image for the booking page
    # Position the logo at row 0, column 3, spanning 5 rows with padding
    app.getImageWidget("booking3_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)

    app.startFrame("Booking Page 3 Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the booking title and prompt at the top, spanning 4 columns
    app.addLabel("lb_booking3", "Create Booking").config(font="Arial 35 bold")  # Add a title label with bold Arial font of size 35
    app.addLabel("booking3_prompt","Choose from the following options and book.")  # Add a prompt label to guide the user
    app.stopFrame()  # End the frame for title and prompt

    app.setLabelFg("booking3_prompt", "grey")  # Set the color of the prompt label text to grey

    # Frame for car details
    app.startFrame("frame_car_details", row=1, column=0,colspan=2)  # Start a new frame for car details, spanning 2 columns
    app.addLabel("cartest", row=0, column=0, colspan=2).grid(sticky="n")  # Add a test label for car details at the top of the frame, spanning 2 columns
    app.getLabelWidget("cartest").config(font="Arial 14 bold", width=20,height=2)  # Configure the label widget with bold Arial font of size 14 and set its width and height
    app.addImage("carbooking3", "Car9.gif", row=1, colspan=2)  # Add the image of the car, spanning 2 columns

    # Frame for car category details
    app.startFrame("frame_category", row=2, column=0,sticky="w")  # Create a new frame for car category details, aligned to the left (west)
    app.setPadding([9, 9])  # Set padding around elements inside this frame
    app.addImage("category_icon", "Car_Icon.gif", row=0, column=0)  # Add the car category icon image
    app.addLabel("categorytest", "", row=0, column=1).config(anchor="w",font="Arial 12")  # Add an empty label for the category with a left alignment and Arial font of size 12
    app.stopFrame()  # End the category details frame

    # Frame for seats details
    app.startFrame("frame_seats", row=3, column=0,sticky="w")  # Create a frame for seat details, aligned to the left (west)
    app.setPadding([9, 9])  # Set padding around elements inside this frame
    app.addImage("seats_icon", "Person_Icon.gif", row=0, column=0)  # Add the seats icon image
    app.addLabel("seatstest", "", row=0, column=1).config(anchor="w",font="Arial 12")  # Add an empty label for the seats with a left alignment and Arial font of size 12
    app.stopFrame()  # End the seats details frame

    # Frame for price details
    app.startFrame("frame_price", row=3, column=1,sticky="w")  # Create a frame for price details, aligned to the left (west)
    app.setPadding([9, 9])  # Set padding around elements inside this frame
    app.addImage("price_icon", "Money_Icon.gif", row=0, column=0)  # Add the price icon image
    app.addLabel("pricetest", "", row=0, column=1).config(anchor="w", font="Arial 12",justify="left")  # Add an empty label for the price with a left alignment and Arial font of size 12
    app.stopFrame()  # End the price details frame

    # Frame for luggage details
    app.startFrame("frame_luggage", row=2, column=1, colspan=2,sticky="w")  # Create a frame for luggage details, spanning 2 columns, aligned to the left (west)
    app.setPadding([9, 9])  # Set padding around elements inside this frame
    app.addImage("luggage_icon", "Luggage_Icon.gif", row=0, column=0)  # Add the luggage icon image
    app.addLabel("luggagetest", "", row=0, column=1).config(anchor="w",font="Arial 12")  # Add an empty label for the luggage with a left alignment and Arial font of size 12
    app.stopFrame()  # End the luggage details frame

    app.stopFrame()  # End the car details frame

    # Frame for date and time selection (pickup and dropoff)
    app.startFrame("date_time_frame", row=1, column=3,colspan=2)  # Create a frame for pickup and drop-off date and time selection, spanning 2 columns
    app.addLabel("pickup_label", "Pick-up", row=1, column=0)  # Add a label for the pick-up date/time
    app.getLabelWidget("pickup_label").config(font="Arial 14 bold")  # Configure the font of the pickup label to bold Arial size 14
    app.addLabel("empty_4", "", row=2, column=0)  # Add an empty label for spacing between elements
    app.addOptionBox("pickup_date", ["- Choose Date -"] + dates_list, row=3,column=0)  # Add a dropdown option box for selecting the pick-up date, initialized with a list of dates
    app.getOptionBoxWidget("pickup_date").config(width=20,height=2)  # Set the width and height of the pick-up date dropdown box
    app.addLabel("empty_5", "", column=1)  # Add another empty label for spacing
    app.addOptionBox("pickup_time", get_times(dates_list[0]), row=5,column=0)  # Add a dropdown option box for selecting the pick-up time, initialized with times for the selected pick-up date
    app.getOptionBoxWidget("pickup_time").config(width=20,height=2)  # Set the width and height of the pick-up time dropdown box
    app.addLabel("empty_6", "", row=6, column=0)  # Add an empty label for spacing

    app.addLabel("dropoff_label", "Drop-off", row=1, column=2)  # Add a label for the drop-off date/time
    app.getLabelWidget("dropoff_label").config(font="Arial 14 bold")  # Configure the font of the drop-off label to bold Arial size 14
    app.addLabel("empty_7", "", row=2, column=2)  # Add an empty label for spacing between elements
    app.addOptionBox("dropoff_date", ["- Choose Date -"] + dates_list, row=3,column=2)  # Add a dropdown option box for selecting the drop-off date
    app.getOptionBoxWidget("dropoff_date").config(width=20,height=2)  # Set the width and height of the drop-off date dropdown box
    app.addLabel("empty_8", "", row=4, column=2)  # Add an empty label for spacing
    app.addOptionBox("dropoff_time", ["- Choose Time -"] + times_list, row=5,column=2)  # Add a dropdown option box for selecting the drop-off time
    app.getOptionBoxWidget("dropoff_time").config(width=20,height=2)  # Set the width and height of the drop-off time dropdown box
    app.addLabel("empty_9", "", row=6, column=2)  # Add an empty label for spacing
    app.stopFrame()  # End the date and time selection frame

    app.getOptionBoxWidget("dropoff_date").config(state="disabled")  # Disable the drop-off date options initially
    app.getOptionBoxWidget("dropoff_time").config(state="disabled")  # Disable the drop-off time options initially

    # Add "BOOK NOW" button
    app.addNamedButton("BOOK NOW", "btnBookNow_bookingPage3", btnPress,colspan=4)  # Add a "BOOK NOW" button to the window
    app.getButtonWidget("btnBookNow_bookingPage3").grid(padx=20, pady=5, ipadx=60,ipady=5)  # Position the "BOOK NOW" button with padding

    # Button styling for "Back" button
    app.setButtonImage("btnBookingBack3", "BACKBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnBookingBack3", "white")  # Set the background color of the "Back" button to white
    app.setButtonRelief("btnBookingBack3", "flat")  # Set the relief style of the "Back" button to flat
    app.getButtonWidget("btnBookingBack3").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the "Back" button"s active background and remove highlight and border

    # Button styling for "BOOK NOW" button
    app.setButtonImage("btnBookNow_bookingPage3", "BOOKNOWBUTTON.gif")  # Set the image for the "BOOK NOW" button
    app.setButtonBg("btnBookNow_bookingPage3", "white")  # Set the background color of the "BOOK NOW" button to white
    app.setButtonRelief("btnBookNow_bookingPage3", "flat")  # Set the relief style of the "BOOK NOW" button to flat
    app.getButtonWidget("btnBookNow_bookingPage3").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the "BOOK NOW" button"s active background and remove highlight and border

    # Configure highlight styling for dropdowns
    app.getOptionBoxWidget("pickup_date").config(highlightbackground="green", highlightcolor="green",highlightthickness=2,bd=0)  # Set green highlight for the pickup date dropdown
    app.getOptionBoxWidget("pickup_time").config(highlightbackground="green", highlightcolor="green",highlightthickness=2,bd=0)  # Set green highlight for the pickup time dropdown
    app.getOptionBoxWidget("dropoff_date").config(highlightbackground="green", highlightcolor="green",highlightthickness=2,bd=0)  # Set green highlight for the drop-off date dropdown
    app.getOptionBoxWidget("dropoff_time").config(highlightbackground="green", highlightcolor="green",highlightthickness=2,bd=0)  # Set green highlight for the drop-off time dropdown

    app.stopSubWindow()  # End the sub-window for Booking Page 3

    app.setOptionBoxChangeFunction("pickup_date",update_pickup)  # Set function to update pickup times when pickup date changes
    app.setOptionBoxChangeFunction("pickup_time",update_dropoff)  # Set function to update drop-off options when pickup time changes
    app.setOptionBoxChangeFunction("dropoff_date",update_dropoff_date)  # Set function to update drop-off times when drop-off date changes

#####################################################################################################################################################
#####################################################################################################################################################

    app.startSubWindow("win_Booking4", title="ElectricCarRental")  # Create a sub-window for Booking Page 4
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the location of the sub-window to coordinates (500, 250)

    app.addNamedButton("Back", "btnBookingBack4",btnPress)  # Add a "Back" button for navigation and bind it to btnPress function
    app.getButtonWidget("btnBookingBack4").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button at the top-left corner with padding and internal padding

    app.setBg("white",override=True)  # Set the background color of the sub-window to white, overriding any default background
    app.addImage("booking4_logo", "Small_CarLogo.gif")  # Add the logo image for the booking page
    # Position the logo at row 0, column 3, spanning 5 rows with padding
    app.getImageWidget("booking4_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)

    app.startFrame("Booking Page 4 Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the booking title and prompt, spanning 4 columns
    app.addLabel("lb_booking4", "Booking Summary").config(font="Arial 35 bold")  # Add a title label with bold Arial font of size 35
    app.addLabel("booking4_prompt","Review your final choices and confirm booking.")  # Add a prompt label to guide the user
    app.stopFrame()  # End the frame for title and prompt

    app.setLabelFg("booking4_prompt", "grey")  # Set the text color of the prompt label to grey

    app.startFrame("frame_car_details1", row=1, column=0,colspan=2)  # Create a frame for displaying car details, spanning 2 columns
    app.addLabel("Car_Details_Label", "Car Details", row=0, column=0, colspan=2).grid(sticky="n")  # Add a label for car details at the top of the frame, spanning 2 columns
    app.getLabelWidget("Car_Details_Label").config(font="Arial 14 bold",height=2)  # Configure the label widget with Arial font of size 14 and height 2

    app.addEntry("Car_Name_Entry", row=1, column=0)  # Add an entry widget for the car name
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Car_Name_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Name_Entry").grid(padx=2, pady=4,ipady=4)  # Position the car name entry widget with padding and internal padding

    app.addEntry("Price_Per_Day_Entry", row=1, column=1)  # Add an entry widget for price per day
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Price_Per_Day_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Price_Per_Day_Entry").grid(padx=2, pady=4,ipady=4)  # Position the price per day entry widget with padding and internal padding

    app.addEntry("Seats_Entry", row=2, column=0)  # Add an entry widget for number of seats
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Seats_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Seats_Entry").grid(padx=3, pady=4,ipady=4)  # Position the seats entry widget with padding and internal padding

    app.addEntry("Luggage_Entry", row=2, column=1)  # Add an entry widget for luggage capacity
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Luggage_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Luggage_Entry").grid(padx=3, pady=4,ipady=4)  # Position the luggage entry widget with padding and internal padding

    app.addEntry("Car_Type_Entry", row=3, column=0)  # Add an entry widget for car type
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Car_Type_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Type_Entry").grid(padx=3, pady=4,ipady=4)  # Position the car type entry widget with padding and internal padding

    app.addEntry("Total_Price_Entry", row=3, column=1,colspan=2)  # Add an entry widget for total price, spanning 2 columns
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Total_Price_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Price_Entry").grid(padx=3, pady=4, ipady=4,sticky="n")  # Position the total price entry widget with padding and internal padding
    app.stopFrame()  # End the car details frame

    app.startFrame("pickup_dropoff_labels", row=1, column=3,colspan=2)  # Create a frame for pickup and drop-off details, spanning 2 columns
    app.addLabel("pickup1_label", "Pick-up", row=0, column=0)  # Add a label for pick-up
    app.getLabelWidget("pickup1_label").config(font="Arial 14 bold",height=2)  # Configure the pick-up label with bold Arial font and height 2

    app.addEntry("Pickup_Date_Entry", row=1, column=0)  # Add an entry widget for the pickup date
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Pickup_Date_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Pickup_Date_Entry").grid(padx=3, pady=4,ipady=4)  # Position the pickup date entry widget with padding and internal padding

    app.addEntry("Pickup_Time_Entry", row=2, column=0)  # Add an entry widget for the pickup time
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Pickup_Time_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Pickup_Time_Entry").grid(padx=3, pady=4,ipady=4)  # Position the pickup time entry widget with padding and internal padding

    app.addLabel("dropoff1_label", "Drop-off", row=0, column=1)  # Add a label for drop-off
    app.getLabelWidget("dropoff1_label").config(font="Arial 14 bold",height=2)  # Configure the drop-off label with bold Arial font and height 2

    app.addEntry("Dropoff_Date_Entry", row=1, column=1)  # Add an entry widget for the drop-off date
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Dropoff_Date_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Dropoff_Date_Entry").grid(padx=3, pady=4,ipady=4)  # Position the drop-off date entry widget with padding and internal padding

    app.addEntry("Dropoff_Time_Entry", row=2, column=1)  # Add an entry widget for the drop-off time
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Dropoff_Time_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Dropoff_Time_Entry").grid(padx=3, pady=4,ipady=4)  # Position the drop-off time entry widget with padding and internal padding

    app.addEntry("Total_Duration_Entry", row=3, column=0,colspan=2)  # Add an entry widget for total duration, spanning 2 columns
    # Disable the entry widget for user input and style it
    app.getEntryWidget("Total_Duration_Entry").config(width=45, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Duration_Entry").grid(padx=3, pady=4, ipady=4,sticky="n")  # Position the total duration entry widget with padding and internal padding
    app.stopFrame()  # End the frame for pickup and drop-off details

    app.addNamedButton("CONFIRM", "btnConfirm_bookingPage4", btnPress,colspan=4)  # Add a "CONFIRM" button to finalize the booking and bind it to btnPress function
    app.getButtonWidget("btnConfirm_bookingPage4").grid(padx=10, pady=20, ipadx=60,ipady=5)  # Position the "CONFIRM" button with padding and internal padding

    # Button styling for "Back" button
    app.setButtonImage("btnBookingBack4", "BACKBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnBookingBack4", "white")  # Set the background color of the "Back" button to white
    app.setButtonRelief("btnBookingBack4", "flat")  # Set the relief style of the "Back" button to flat
    # Configure the "Back" button"s active background color and border thickness
    app.getButtonWidget("btnBookingBack4").config(activebackground="white", highlightthickness=0,bd=0)

    # Button styling for "Confirm" button
    app.setButtonImage("btnConfirm_bookingPage4", "CONFIRMBUTTON.gif")  # Set the image for the "Confirm" button
    app.setButtonBg("btnConfirm_bookingPage4", "white")  # Set the background color of the "Confirm" button to white
    app.setButtonRelief("btnConfirm_bookingPage4", "flat")  # Set the relief style of the "Confirm" button to flat
    # Configure the "Confirm" button"s active background color and border thickness
    app.getButtonWidget("btnConfirm_bookingPage4").config(activebackground="white", highlightthickness=0,bd=0)

    app.stopSubWindow()  # End the sub-window for Booking Page 4

#####################################################################################################################################################
#####################################################################################################################################################

    # VIEW TRIPS PAGE #
    app.startSubWindow("win_ViewTrips", title="ElectricCarRental")  # Create a sub-window for the "View Trips" page
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the location of the sub-window on the screen

    app.addNamedButton("Back", "btnViewTripsBack", btnPress)  # Add a "Back" button for navigation
    app.getButtonWidget("btnViewTripsBack").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button
    app.setButtonImage("btnViewTripsBack", "LOGOUTBUTTON.gif")  # Set an initial image for the "Back" button

    app.setBg("white", override=True)  # Set the background colour of the window to white
    app.addImage("viewtrips_logo", "Small_CarLogo.gif")  # Add the logo image for branding
    app.getImageWidget("viewtrips_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position the logo in the top-right

    app.startFrame("Trips Page Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the title and prompt
    app.addLabel("lb_trips", "Trips").config(font="Arial 40 bold")  # Add a main title label for the trips page
    app.addLabel("trips_prompt","Pick an option to view, manage, or cancel your trips.")  # Add a prompt under the title
    app.stopFrame()  # End the title frame

    app.setLabelFg("trips_prompt", "grey")  # Set the prompt label font colour to grey

    app.startFrame("Trips_Images", row=2, colspan=6)  # Start a new frame for the three main options

    app.addNamedButton("PAST BOOKINGS", "btnPastBookings", btnPress, row=1, column=0)  # Add a button for past bookings
    app.setButtonImage("btnPastBookings", "pastbooking_trips.gif")  # Set image for the past bookings button
    app.setButtonBg("btnPastBookings", "white")  # Set background to white
    app.setButtonRelief("btnPastBookings", "flat")  # Make the button flat
    app.getButtonWidget("btnPastBookings").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button to look flat on interaction

    app.addLabel("spacer1trips", "", row=1, column=1)  # Add a spacer label to separate buttons
    app.setLabelWidth("spacer1trips", 4)  # Set width for the spacer

    app.addNamedButton("FUTURE BOOKINGS", "btnFutureBookings", btnPress, row=1,column=2)  # Add a button for future bookings
    app.setButtonImage("btnFutureBookings", "futurebookings_trips.gif")  # Set image for the future bookings button
    app.setButtonBg("btnFutureBookings", "white")  # Set background to white
    app.setButtonRelief("btnFutureBookings", "flat")  # Make the button flat
    app.getButtonWidget("btnFutureBookings").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button to look flat on interaction

    app.addLabel("spacer2trips", "", row=1, column=3)  # Add a second spacer between buttons
    app.setLabelWidth("spacer2trips", 4)  # Set width for the spacer

    app.addNamedButton("CANCEL BOOKINGS", "btnCancelBookings", btnPress, row=1,column=4)  # Add a button to cancel bookings
    app.setButtonImage("btnCancelBookings", "cancel_trips.gif")  # Set image for the cancel bookings button
    app.setButtonBg("btnCancelBookings", "white")  # Set background to white
    app.setButtonRelief("btnCancelBookings", "flat")  # Make the button flat
    app.getButtonWidget("btnCancelBookings").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button to look flat on interaction

    app.setButtonImage("btnViewTripsBack", "BACKBUTTON.gif")  # Update the back button image
    app.setButtonBg("btnViewTripsBack", "white")  # Set the back button background to white
    app.setButtonRelief("btnViewTripsBack", "flat")  # Make the back button flat
    app.getButtonWidget("btnViewTripsBack").config(activebackground="white", highlightthickness=0,bd=0)  # Configure back button appearance

    app.stopFrame()  # End the Trips_Images frame

    app.stopSubWindow()  # End the sub-window for the "View Trips" page
    # END OF VIEW TRIPS PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

    app.startSubWindow("win_PastBookingsView", title="ElectricCarRental")  # Start the sub-window for past bookings
    app.setSize("1000x500")  # Set fixed window size to 1000x500 pixels
    app.setResizable(False)  # Disable resizing of the window
    app.setLocation(500, 250)  # Position the window at the specified screen coordinates (500, 250)

    app.addNamedButton("Back", "btnPastBookingsViewBack", btnPress)  # Add a "Back" button to allow users to go back
    app.getButtonWidget("btnPastBookingsViewBack").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the back button at top-left

    app.setButtonImage("btnPastBookingsViewBack", "BACKBUTTON.gif")  # Set an image for the back button
    app.setButtonBg("btnPastBookingsViewBack", "white")  # Set the background color of the button to white
    app.setButtonRelief("btnPastBookingsViewBack", "flat")  # Remove the button"s border relief for a flat appearance
    app.getButtonWidget("btnPastBookingsViewBack").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the button"s active state (no border/highlight)

    app.setBg("white", override=True)  # Set the background color of the sub-window to white
    app.addImage("pastbookingview_logo", "Small_CarLogo.gif")  # Add an image (small logo) to the top right corner
    app.getImageWidget("pastbookingview_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position the logo at top-right with padding

    app.startFrame("PastBookingsView_Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the title and prompt labels
    app.addLabel("lb_pastBookingsView", "Past Bookings").config(font="Arial 35 bold")  # Add a large title label with bold font
    app.addLabel("pastBookingsView_prompt","View your past bookings and book again.")  # Add a prompt text below the title
    app.stopFrame()  # End the frame that contains the title and prompt labels
    app.setLabelFg("pastBookingsView_prompt", "grey")  # Set the color of the prompt text to grey

    app.addLabel("bookingRef_Label_pastbooking", "BookingRef", colspan=4).config(font="Arial 14 bold")  # Add a label for booking reference with bold font
    app.startFrame("frame_car_details1_pastbooking", row=2, column=0,colspan=2)  # Create a frame for the car details section
    app.addLabel("Car_Details_Label_pastbooking", "Car Details", row=0, column=0, colspan=2).grid(sticky="n")  # Add a label for the car details section title
    app.getLabelWidget("Car_Details_Label_pastbooking").config(font="Arial 14 bold",height=2)  # Set the font and height for the label

    app.addEntry("Car_Name_Entry_pastbooking", row=2, column=0)  # Add an entry widget for the car name
    # Disable editing, set background and border styles
    app.getEntryWidget("Car_Name_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Name_Entry_pastbooking").grid(padx=2, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Price_Per_Day_Entry_pastbooking", row=2, column=1)  # Add an entry widget for price per day
    # Disable editing and configure styles
    app.getEntryWidget("Price_Per_Day_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Price_Per_Day_Entry_pastbooking").grid(padx=2, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Seats_Entry_pastbooking", row=3, column=0)  # Add an entry widget for the number of seats
    # Disable editing and configure styles
    app.getEntryWidget("Seats_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Seats_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Luggage_Entry_pastbooking", row=3, column=1)  # Add an entry widget for luggage capacity
    # Disable editing and configure styles
    app.getEntryWidget("Luggage_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Luggage_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Car_Type_Entry_pastbooking", row=4, column=0)  # Add an entry widget for car type
    # Disable editing and configure styles
    app.getEntryWidget("Car_Type_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Type_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Total_Cost_Entry_pastbooking", row=4, column=1)  # Add an entry widget for total cost
    # Disable editing and configure styles
    app.getEntryWidget("Total_Cost_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Cost_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.stopFrame()  # End the car details frame

    app.startFrame("pickup_dropoff_labels_pastbooking", row=2, column=3,colspan=2)  # Create a frame for pickup/dropoff info
    app.addLabel("pickup1_label_pastbooking", "Pick-up", row=0, column=0)  # Add a label for pickup
    app.getLabelWidget("pickup1_label_pastbooking").config(font="Arial 14 bold", height=2)  # Style the pickup label

    app.addEntry("Pickup_Date_Entry_pastbooking", row=2, column=0)  # Add an entry widget for pickup date
    # Disable editing and configure styles
    app.getEntryWidget("Pickup_Date_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Pickup_Date_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Pickup_Time_Entry_pastbooking", row=3, column=0)  # Add an entry widget for pickup time
    # Disable editing and configure styles
    app.getEntryWidget("Pickup_Time_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Pickup_Time_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addLabel("dropoff1_label_pastbooking", "Drop-off", row=0, column=1)  # Add a label for drop-off
    app.getLabelWidget("dropoff1_label_pastbooking").config(font="Arial 14 bold", height=2)  # Style the drop-off label

    app.addEntry("Dropoff_Date_Entry_pastbooking", row=2, column=1)  # Add an entry widget for dropoff date
    # Disable editing and configure styles
    app.getEntryWidget("Dropoff_Date_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Dropoff_Date_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Dropoff_Time_Entry_pastbooking", row=3, column=1)  # Add an entry widget for dropoff time
    # Disable editing and configure styles
    app.getEntryWidget("Dropoff_Time_Entry_pastbooking").config(width=20, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Dropoff_Time_Entry_pastbooking").grid(padx=3, pady=4,ipady=4)  # Position the entry widget with padding

    app.addEntry("Total_Duration_Entry_pastbooking", row=4, column=0,colspan=2)  # Add an entry widget for total duration
    # Disable editing and configure styles
    app.getEntryWidget("Total_Duration_Entry_pastbooking").config(width=45, state="disabled", highlightbackground="green", highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Duration_Entry_pastbooking").grid(padx=3, pady=4, ipady=4,sticky="n")  # Position the entry widget with padding

    app.stopFrame()  # End the pickup/dropoff frame

    app.addNamedButton("BOOK AGAIN", "btnBookAgain", btnPress, row=5, column=0, colspan=4)  # Add a button to book again
    app.getButtonWidget("btnBookAgain").grid(padx=10, pady=20, ipadx=60, ipady=5)  # Position the button with padding
    app.setButtonImage("btnBookAgain", "BOOKAGAINBUTTON.gif")  # Set an image for the "BOOK AGAIN" button
    app.setButtonBg("btnBookAgain", "white")  # Set button background color to white
    app.setButtonRelief("btnBookAgain", "flat")  # Set the button relief to flat for no border effect
    app.getButtonWidget("btnBookAgain").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button state for active background

    app.stopSubWindow()  # End the sub-window for past bookings

#####################################################################################################################################################
#####################################################################################################################################################

    app.startSubWindow("win_FutureBookingsView",title="ElectricCarRental")  # Create a sub-window for viewing future bookings
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the window"s location on the screen

    app.addNamedButton("Back", "btnFutureBookingsViewBack", btnPress)  # Add a "Back" button for navigation
    app.getButtonWidget("btnFutureBookingsViewBack").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button

    app.setBg("white", override=True)  # Set the background color of the window to white
    app.addImage("futurebookingview_logo", "Small_CarLogo.gif")  # Add an image logo to the window
    app.getImageWidget("futurebookingview_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position the image

    app.startFrame("FutureBookingsView_Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the future bookings title and prompt
    app.addLabel("lb_futureBookingsView", "Future Bookings").config(font="Arial 35 bold")  # Add a title label for the future bookings page
    app.addLabel("futureBookingsView_prompt", "View your past booking and amend if needed.")  # Add a prompt label
    app.stopFrame()  # End the frame

    app.setLabelFg("futureBookingsView_prompt", "grey")  # Set the color of the prompt label text to grey

    app.addLabel("bookingRef_Label_futurebooking", "BookingRef", colspan=4).config(font="Arial 14 bold")  # Add a label for the booking reference

    app.startFrame("frame_car_details1_futurebooking", row=2, column=0,colspan=2)  # Create a frame for displaying car details
    app.addLabel("Car_Details_Label_futurebooking", "Car Details", row=0, column=0, colspan=2).grid(sticky="n")  # Add a label for car details
    app.getLabelWidget("Car_Details_Label_futurebooking").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addEntry("Car_Name_Entry_futurebooking", row=2, column=0)  # Add an entry widget for car name
    # Disable the entry widget for user input
    app.getEntryWidget("Car_Name_Entry_futurebooking").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Name_Entry_futurebooking").grid(padx=2, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Price_Per_Day_Entry_futurebooking", row=2, column=1)  # Add an entry widget for price per day
    # Disable the entry widget for user input
    app.getEntryWidget("Price_Per_Day_Entry_futurebooking").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Price_Per_Day_Entry_futurebooking").grid(padx=2, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Seats_Entry_futurebooking", row=3, column=0)  # Add an entry widget for number of seats
    # Disable the entry widget for user input
    app.getEntryWidget("Seats_Entry_futurebooking").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Seats_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Luggage_Entry_futurebooking", row=3, column=1)  # Add an entry widget for luggage capacity
    # Disable the entry widget for user input
    app.getEntryWidget("Luggage_Entry_futurebooking").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Luggage_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Car_Type_Entry_futurebooking", row=4, column=0)  # Add an entry widget for car type
    # Disable the entry widget for user input
    app.getEntryWidget("Car_Type_Entry_futurebooking").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Type_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Total_Cost_Entry_futurebooking", row=4, column=1)  # Add an entry widget for total cost
    # Disable the entry widget for user input
    app.getEntryWidget("Total_Cost_Entry_futurebooking").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Cost_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.stopFrame()  # End the frame

    app.startFrame("pickup_dropoff_labels_futurebooking", row=2, column=3,colspan=2)  # Create a frame for pickup and drop-off details
    app.addLabel("pickup1_label_futurebooking", "Pick-up", row=0, column=0)  # Add a label for pickup
    app.getLabelWidget("pickup1_label_futurebooking").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addEntry("Pickup_Date_Entry_futurebooking", row=2, column=0)  # Add an entry widget for pickup date
    # Disable the entry widget for user input
    app.getEntryWidget("Pickup_Date_Entry_futurebooking").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Pickup_Date_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Pickup_Time_Entry_futurebooking", row=3, column=0)  # Add an entry widget for pickup time
    # Disable the entry widget for user input
    app.getEntryWidget("Pickup_Time_Entry_futurebooking").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Pickup_Time_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addLabel("dropoff1_label_futurebooking", "Drop-off", row=0, column=1)  # Add a label for drop-off
    app.getLabelWidget("dropoff1_label_futurebooking").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addEntry("Dropoff_Date_Entry_futurebooking", row=2, column=1)  # Add an entry widget for drop-off date
    # Disable the entry widget for user input
    app.getEntryWidget("Dropoff_Date_Entry_futurebooking").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Dropoff_Date_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Dropoff_Time_Entry_futurebooking", row=3, column=1)  # Add an entry widget for drop-off time
    # Disable the entry widget for user input
    app.getEntryWidget("Dropoff_Time_Entry_futurebooking").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Dropoff_Time_Entry_futurebooking").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Total_Duration_Entry_futurebooking", row=4, column=0,colspan=2)  # Add an entry widget for total duration
    # Disable the entry widget for user input
    app.getEntryWidget("Total_Duration_Entry_futurebooking").config(width=45, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2, disabledbackground="white")
    app.getEntryWidget("Total_Duration_Entry_futurebooking").grid(padx=3, pady=4, ipady=4,sticky="n")  # Position the entry widget
    app.stopFrame()  # End the frame

    app.addNamedButton("AMEND BOOKING", "btnAmendBooking", btnPress, row=5, column=0,colspan=4)  # Add an "AMEND BOOKING" button
    app.getButtonWidget("btnAmendBooking").grid(padx=10, pady=20, ipadx=60,ipady=5)  # Position the "AMEND BOOKING" button
    app.setButtonImage("btnAmendBooking", "AMENDBUTTON.gif")  # Set an image for the "AMEND BOOKING" button
    app.setButtonBg("btnAmendBooking", "white")  # Set the background color for the "AMEND BOOKING" button
    app.setButtonRelief("btnAmendBooking", "flat")  # Set the relief style for the "AMEND BOOKING" button
    app.getButtonWidget("btnAmendBooking").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the "AMEND BOOKING" button"s active style

    app.setButtonImage("btnFutureBookingsViewBack", "BACKBUTTON.gif")  # Set an image for the "BACK" button
    app.setButtonBg("btnFutureBookingsViewBack", "white")  # Set the background color for the "BACK" button
    app.setButtonRelief("btnFutureBookingsViewBack", "flat")  # Set the relief style for the "BACK" button
    app.getButtonWidget("btnFutureBookingsViewBack").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the "BACK" button"s active style

    app.stopSubWindow()  # End the sub-window

#####################################################################################################################################################
#####################################################################################################################################################

    app.startSubWindow("win_AmendBooking", title="ElectricCarRental")  # Create a sub-window for amending bookings
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the location of the window

    app.addNamedButton("Back", "btnAmendBookingBack", btnPress, rowspan=2)  # Add a "Back" button for navigation
    app.getButtonWidget("btnAmendBookingBack").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button#

    app.setBg("white", override=True)  # Set the background color to white
    app.addImage("amendbooking_logo", "Small_CarLogo.gif")  # Add the logo image to the sub-window
    app.getImageWidget("amendbooking_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position the logo image

    app.startFrame("AmendBooking_Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the amend booking title and prompt
    app.addLabel("lb_amendBooking", "Amend Booking").config(font="Arial 35 bold")  # Add a title label for the amend booking page
    app.addLabel("amendBooking_prompt", "Choose to change dates and times of booking.").config(height=2)  # Add a prompt label
    app.stopFrame()  # End the frame

    app.setLabelFg("amendBooking_prompt", "grey")  # Set the label foreground color to grey

    app.addLabel("spacing_amendbooking1", "", row=1, column=0, colspan=4).config(height=2)  # Add an empty label for spacing
    app.addLabel("bookingRef_Label_amendBooking", "", row=2, column=0, colspan=4).config(font="Arial 14 bold",height=3)  # Add a label for the booking reference
    app.addLabel("spacing_amendbooking2", "", row=1, column=0, colspan=4).config(height=2)  # Add an empty label for spacing

    app.startFrame("frame_old_booking", row=3, column=0, colspan=2)  # Create a frame for displaying old booking details
    app.addLabel("old_booking_label", "Old Booking", row=0, column=0,colspan=2)  # Add a label for the old booking section
    app.getLabelWidget("old_booking_label").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addLabel("old_pickup_label", "Pick-up", row=1, column=0)  # Add a label for the old pickup section
    app.getLabelWidget("old_pickup_label").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addEntry("Old_Pickup_Date_Entry", row=3, column=0)  # Add an entry widget for the old pickup date
    # Disable the entry widget for user input
    app.getEntryWidget("Old_Pickup_Date_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white",bd=0)
    app.getEntryWidget("Old_Pickup_Date_Entry").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addLabel("empty_2_old", "", row=4, column=0)  # Add an empty label for spacing
    # Add an entry widget for the old pickup time and position it
    app.addEntry("Old_Pickup_Time_Entry", row=5, column=0)  # Add an entry widget for the old pickup time
    # Disable the entry widget for user input
    app.getEntryWidget("Old_Pickup_Time_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white",bd=0)
    app.getEntryWidget("Old_Pickup_Time_Entry").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addLabel("old_dropoff_label", "Drop-off", row=1, column=1)  # Add a label for the old drop-off section
    app.getLabelWidget("old_dropoff_label").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addEntry("Old_Dropoff_Date_Entry", row=3, column=1)  # Add an entry widget for the old drop-off date
    # Disable the entry widget for user input
    app.getEntryWidget("Old_Dropoff_Date_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white",bd=0)
    app.getEntryWidget("Old_Dropoff_Date_Entry").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Old_Dropoff_Time_Entry", row=5, column=1)  # Add an entry widget for the old drop-off time
    # Disable the entry widget for user input
    app.getEntryWidget("Old_Dropoff_Time_Entry").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white",bd=0)
    app.getEntryWidget("Old_Dropoff_Time_Entry").grid(padx=3, pady=4, ipady=4)  # Position the entry widget

    app.addEntry("Old_Total_Duration_Entry", row=7, column=0,colspan=2)  # Add an entry widget for the old total duration
    app.getEntryWidget("Old_Total_Duration_Entry").grid(padx=3, pady=4, ipady=4,sticky="n")  # Position the entry widget
    # Configure the entry widget
    app.getEntryWidget("Old_Total_Duration_Entry").config(width=45, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white",bd=0)

    app.addLabel("empty_5_old", "", row=8, column=0)  # Add an empty label for spacing
    app.stopFrame()  # End the frame

    app.startFrame("frame_new_booking", row=3, column=3, colspan=2)  # Create a frame for selecting new booking details
    app.addLabel("new_booking_label", "New Booking", row=0, column=0,colspan=3)  # Add a label for the new booking section
    app.getLabelWidget("new_booking_label").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addLabel("new_pickup_label", "Pick-up", row=1, column=0)  # Add a label for the new pickup section
    app.getLabelWidget("new_pickup_label").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addOptionBox("new_pickup_date", ["- Choose Date -"] + dates_list, row=3,column=0)  # Add a dropdown for the new pickup date
    app.getOptionBoxWidget("new_pickup_date").grid(padx=3, pady=4, ipady=4)  # Position the dropdown
    app.getOptionBoxWidget("new_pickup_date").config(highlightbackground="green", highlightcolor="green",highlightthickness=2, bd=0, width=20, height=2)

    app.addLabel("empty_5_new", "", column=1)  # Add an empty label for spacing
    app.addOptionBox("new_pickup_time", get_times(dates_list[0]), row=5,column=0)  # Add a dropdown for the new pickup time
    app.getOptionBoxWidget("new_pickup_time").grid(padx=3, pady=4, ipady=4)  # Position the dropdown
    app.getOptionBoxWidget("new_pickup_time").config(highlightbackground="green", highlightcolor="green",highlightthickness=2, bd=0, width=20, height=2)

    app.addLabel("empty_6_new", "", row=6, column=0)  # Add an empty label for spacing

    app.addLabel("new_dropoff_label", "Drop-off", row=1, column=2)  # Add a label for the new drop-off section
    app.getLabelWidget("new_dropoff_label").config(font="Arial 14 bold", height=2)  # Configure the label

    app.addOptionBox("new_dropoff_date", ["- Choose Date -"] + dates_list, row=3,column=2)  # Add a dropdown for the new drop-off date
    app.getOptionBoxWidget("new_dropoff_date").grid(padx=3, pady=4, ipady=4)  # Position the dropdown
    app.getOptionBoxWidget("new_dropoff_date").config(highlightbackground="green", highlightcolor="green",highlightthickness=2, bd=0, width=20, height=2)

    app.addLabel("empty_8_new", "", row=4, column=2)  # Add an empty label for spacing
    app.addOptionBox("new_dropoff_time", ["- Choose Time -"] + times_list, row=5,column=2)  # Add a dropdown for the new drop-off time
    app.getOptionBoxWidget("new_dropoff_time").grid(padx=3, pady=4, ipady=4)  # Position the dropdown
    app.getOptionBoxWidget("new_dropoff_time").config(highlightbackground="green", highlightcolor="green",highlightthickness=2, bd=0)  # Configure the dropdown

    app.addLabel("empty_9_new", "", row=6, column=2)  # Add an empty label for spacing
    app.stopFrame()  # End the frame

    app.addNamedButton("CONTINUE", "btnContinueChanges", btnPress, row=11, column=0, colspan=4,rowspan=2)  # Add a "CONTINUE" button
    app.getButtonWidget("btnContinueChanges").grid(padx=10, pady=20, ipadx=60,ipady=5)  # Position the "CONTINUE" button

    app.getOptionBoxWidget("new_dropoff_date").config(state="disabled")  # Disable the new drop-off date dropdown initially
    app.getOptionBoxWidget("new_dropoff_time").config(state="disabled")  # Disable the new drop-off time dropdown initially

    app.setButtonImage("btnContinueChanges", "CONFIRMCHANGESBUTTON.gif")  # Set the image for the "CONTINUE" button
    app.setButtonBg("btnContinueChanges", "white")  # Set the background color for the "CONTINUE" button
    app.setButtonRelief("btnContinueChanges", "flat")  # Set the relief style for the "CONTINUE" button
    app.getButtonWidget("btnContinueChanges").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the button"s appearance

    app.setButtonImage("btnAmendBookingBack", "BACKBUTTON.gif")  # Set the image for the "BACK" button
    app.setButtonBg("btnAmendBookingBack", "white")  # Set the background color for the "BACK" button
    app.setButtonRelief("btnAmendBookingBack", "flat")  # Set the relief style for the "BACK" button
    app.getButtonWidget("btnAmendBookingBack").config(activebackground="white", highlightthickness=0,bd=0)  # Configure the button"s appearance

    app.stopSubWindow()  # End the sub-window

    def update_new_pickup():  # Define a function to update the new pickup time options
        pickup_date = app.getOptionBox("new_pickup_date")  # Get the selected new pickup date

        if pickup_date == "- Choose Date -":  # Check if no date is selected

            app.changeOptionBox("new_pickup_time", ["- Choose Time -"])  # Reset the pickup time options
            return

        new_pickup_times = get_times(pickup_date)  # Get the updated list of pickup times for the selected date
        app.changeOptionBox("new_pickup_time", new_pickup_times)  # Update the pickup time options

    def update_new_dropoff():  # Define a function to update the new drop-off date and time options
        pickup_date = app.getOptionBox("new_pickup_date")  # Get the selected new pickup date
        pickup_time = app.getOptionBox("new_pickup_time")  # Get the selected new pickup time
        dropoff_date = app.getOptionBox("new_dropoff_date")  # Get the selected new drop-off date

        if pickup_date == "- Choose Date -" or pickup_time == "- Choose Time -" or pickup_time is None:  # Check if no pickup date or time is selected

            app.changeOptionBox("new_dropoff_date", ["- Choose Date -"] + dates_list)  # Reset the drop-off date options
            app.changeOptionBox("new_dropoff_time", ["- Choose Time -"] + times_list)  # Reset the drop-off time options
            app.getOptionBoxWidget("new_dropoff_date").config(state="disabled")  # Disable the drop-off date dropdown
            app.getOptionBoxWidget("new_dropoff_time").config(state="disabled")  # Disable the drop-off time dropdown
            return

        app.getOptionBoxWidget("new_dropoff_date").config(state="normal")  # Enable the drop-off date dropdown
        app.getOptionBoxWidget("new_dropoff_time").config(state="normal")  # Enable the drop-off time dropdown

        pickup_date_index = dates_list.index(pickup_date)  # Get the index of the selected pickup date in the dates list
        valid_dropoff_dates = dates_list[pickup_date_index:]  # Generate a list of valid drop-off dates starting from the pickup date

        if dropoff_date == pickup_date:  # Check if the drop-off date is the same as the pickup date
            valid_dropoff_times = ["- Choose Time -"]  # Initialise the list with a default option

            for t in times_list:  # Iterate through the times list
                if t > pickup_time:  # Check if the time is after the pickup time
                    valid_dropoff_times.append(t)  # Add the time to the list
                else:  # Otherwise
                    valid_dropoff_times.append(f"- {t} -")  # Mark the time as unavailable
        else:  # If the drop-off date is in the future
            valid_dropoff_times = ["- Choose Time -"] + times_list  # All times are available
        app.changeOptionBox("new_dropoff_date",["- Choose Date -"] + valid_dropoff_dates)  # Update the drop-off date options
        app.changeOptionBox("new_dropoff_time", valid_dropoff_times)  # Update the drop-off time options

        if dropoff_date in valid_dropoff_dates:  # Check if the previously selected drop-off date is still valid
            app.setOptionBox("new_dropoff_date", dropoff_date)  # Keep the drop-off date selected

    def update_new_dropoff_date():  # Define a function to update the new drop-off time options
        dropoff_date = app.getOptionBox("new_dropoff_date")  # Get the selected new drop-off date
        pickup_date = app.getOptionBox("new_pickup_date")  # Get the selected new pickup date
        pickup_time = app.getOptionBox("new_pickup_time")  # Get the selected new pickup time

        if dropoff_date == "- Choose Date -":  # Check if no drop-off date is selected
            app.changeOptionBox("new_dropoff_time", ["- Choose Time -"] + times_list)  # Reset the drop-off time options
            return

        if dropoff_date == pickup_date:  # Check if the drop-off date is the same as the pickup date
            valid_dropoff_times = ["- Choose Time -"]  # Initialise the list with a default option
            for t in times_list:  # Iterate through the times list
                if t > pickup_time:  # Check if the time is after the pickup time
                    valid_dropoff_times.append(t)  # Add the time to the list
                else:  # Otherwise
                    valid_dropoff_times.append(f"- {t} -")  # Mark the time as unavailable
        else:  # If the drop-off date is in the future
            valid_dropoff_times = ["- Choose Time -"] + times_list  # All times are available
        app.changeOptionBox("new_dropoff_time", valid_dropoff_times)  # Update the drop-off time options

    app.setOptionBoxChangeFunction("new_pickup_date",update_new_pickup)  # Set the function to update pickup times when pickup date changes
    app.setOptionBoxChangeFunction("new_pickup_time",update_new_dropoff)  # Set the function to update drop-off options when pickup time changes
    app.setOptionBoxChangeFunction("new_dropoff_date",update_new_dropoff_date)  # Set the function to update drop-off times when drop-off date changes

#####################################################################################################################################################
#####################################################################################################################################################

    # AMEND BOOKING 2 #
    app.startSubWindow("win_AmendSummary", title="ElectricCarRental")  # Start the sub-window for Amend Summary
    app.setSize("1000x500")  # Set the window size
    app.setResizable(False)  # Disable resizing
    app.setLocation(500, 250)  # Set window location

    app.addNamedButton("Back", "btnAmendSummaryBack", btnPress)  # Add "Back" button
    app.getButtonWidget("btnAmendSummaryBack").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position button

    app.setBg("white", override=True)  # Set background to white
    app.addImage("amendbooking2_logo", "Small_CarLogo.gif")  # Add logo image
    app.getImageWidget("amendbooking2_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position logo

    app.startFrame("AmendSummary_Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Start frame for amendment summary
    app.addLabel("lb_amendSummary", "Amend Summary").config(font="Arial 35 bold")  # Title label for amend summary
    app.addLabel("amendSummary_prompt", "Review your final changes and confirm amends.")  # Prompt label
    app.stopFrame()  # Stop the frame

    app.setLabelFg("amendSummary_prompt", "grey")  # Set label color

    app.addLabel("bookingRef_Label_amendSummary", "", row=1, column=0, colspan=4).config(font="Arial 14 bold")  # Booking reference label
    app.getLabelWidget("bookingRef_Label_amendSummary").grid(pady=(0, 10))  # Position booking reference label

    app.startFrame("frame_car_details_amendSummary", row=2, column=0, colspan=2)  # Start frame for car details
    app.addLabel("Car_Details_Label_amendSummary", "Car Details", row=0, column=0, colspan=2).grid(sticky="n")  # Car details label
    app.getLabelWidget("Car_Details_Label_amendSummary").config(font="Arial 14 bold", height=2)  # Configure label

    app.addEntry("Car_Name_Entry_amendSummary", row=1, column=0)  # Entry for car name
    # Configure entry
    app.getEntryWidget("Car_Name_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Name_Entry_amendSummary").grid(padx=2, pady=4, ipady=4)  # Position entry

    app.addEntry("Price_Per_Day_Entry_amendSummary", row=1, column=1)  # Entry for price per day
    # Configure entry
    app.getEntryWidget("Price_Per_Day_Entry_amendSummary").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Price_Per_Day_Entry_amendSummary").grid(padx=2, pady=4, ipady=4)  # Position entry

    app.addEntry("Seats_Entry_amendSummary", row=2, column=0)  # Entry for seats
    # Configure entry
    app.getEntryWidget("Seats_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Seats_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addEntry("Luggage_Entry_amendSummary", row=2, column=1)  # Entry for luggage capacity
    # Configure entry
    app.getEntryWidget("Luggage_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Luggage_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addEntry("Car_Type_Entry_amendSummary", row=3, column=0)  # Entry for car type
    # Configure entry
    app.getEntryWidget("Car_Type_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Car_Type_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addEntry("Total_Price_Entry_amendSummary", row=3, column=1, colspan=2)  # Entry for total price
    # Configure entry
    app.getEntryWidget("Total_Price_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Price_Entry_amendSummary").grid(padx=3, pady=4, ipady=4, sticky="n")  # Position entry
    app.stopFrame()  # Stop frame

    app.startFrame("pickup_dropoff_labels_amendSummary", row=2, column=3,colspan=2)  # Start frame for pickup/dropoff details
    app.addLabel("pickup_label_amendSummary", "Pick-up", row=0, column=0)  # Pickup label
    app.getLabelWidget("pickup_label_amendSummary").config(font="Arial 14 bold", height=2)  # Configure label

    app.addEntry("Pickup_Date_Entry_amendSummary", row=1, column=0)  # Pickup date entry
    # Configure entry
    app.getEntryWidget("Pickup_Date_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Pickup_Date_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addEntry("Pickup_Time_Entry_amendSummary", row=2, column=0)  # Pickup time entry
    # Configure entry
    app.getEntryWidget("Pickup_Time_Entry_amendSummary").config(width=20, state="disabled", highlightbackground="green",highlightcolor="green", highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Pickup_Time_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addLabel("dropoff_label_amendSummary", "Drop-off", row=0, column=1)  # Dropoff label
    app.getLabelWidget("dropoff_label_amendSummary").config(font="Arial 14 bold", height=2)  # Configure label

    app.addEntry("Dropoff_Date_Entry_amendSummary", row=1, column=1)  # Dropoff date entry
    # Configure entry
    app.getEntryWidget("Dropoff_Date_Entry_amendSummary").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Dropoff_Date_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addEntry("Dropoff_Time_Entry_amendSummary", row=2, column=1)  # Dropoff time entry
    # Configure entry
    app.getEntryWidget("Dropoff_Time_Entry_amendSummary").config(width=20, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Dropoff_Time_Entry_amendSummary").grid(padx=3, pady=4, ipady=4)  # Position entry

    app.addEntry("Total_Duration_Entry_amendSummary", row=3, column=0, colspan=2)  # Total duration entry
    # Configure entry
    app.getEntryWidget("Total_Duration_Entry_amendSummary").config(width=45, state="disabled",highlightbackground="green", highlightcolor="green",highlightthickness=2,disabledbackground="white")
    app.getEntryWidget("Total_Duration_Entry_amendSummary").grid(padx=3, pady=4, ipady=4, sticky="n")  # Position entry
    app.stopFrame()  # Stop frame

    app.addNamedButton("CONFIRM", "btnConfirmAmend", btnPress, colspan=4)  # Confirm button
    app.getButtonWidget("btnConfirmAmend").grid(padx=10, pady=20, ipadx=60, ipady=5)  # Position button

    app.setButtonImage("btnAmendSummaryBack", "BACKBUTTON.gif")  # Set image for back button
    app.setButtonBg("btnAmendSummaryBack", "white")  # Set background color
    app.setButtonRelief("btnAmendSummaryBack", "flat")  # Set relief style
    app.getButtonWidget("btnAmendSummaryBack").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button appearance

    app.setButtonImage("btnConfirmAmend", "CONFIRMBUTTON.gif")  # Set image for confirm button
    app.setButtonBg("btnConfirmAmend", "white")  # Set background color
    app.setButtonRelief("btnConfirmAmend", "flat")  # Set relief style
    app.getButtonWidget("btnConfirmAmend").config(activebackground="white", highlightthickness=0,bd=0)  # Configure button appearance

    app.stopSubWindow()  # Stop the sub-window
    # END OF AMEND BOOKING 2 #
    # END OF AMEND BOOKINGS PAGES #D

#####################################################################################################################################################
#####################################################################################################################################################

    # CANCEL BOOKINGS #
    app.startSubWindow("win_CancelBookings", title="ElectricCarRental")  # Create a sub-window for Cancel Bookings
    app.setSize("1000x500")  # Set window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Position the window on the screen

    app.addNamedButton("Back", "btnCancelBookingsBack", btnPress)  # Add a "Back" button to return to previous screen
    app.getButtonWidget("btnCancelBookingsBack").grid(sticky="nw", padx=20, pady=10, ipadx=10,ipady=10)  # Position the "Back" button in the top-left

    app.setBg("white", override=True)  # Set background colour to white
    app.addImage("cancel_logo", "Small_CarLogo.gif")  # Add the app logo
    app.getImageWidget("cancel_logo").grid(row=0, column=3, rowspan=5, sticky="ne", padx=20,pady=10)  # Position logo in top-right

    app.startFrame("cancelBooking_frame", row=0, column=0, colspan=4).grid(sticky="n")  # Start a frame for the title and instructions
    app.addLabel("lb_cancelBookings", "Cancel Booking").config(font="Arial 35 bold")  # Add a title label
    app.addLabel("cancelBookings_prompt", "Enter your booking ref to cancel booking.")  # Add a prompt label
    app.stopFrame()  # End the title frame

    app.setLabelFg("cancelBookings_prompt", "grey")  # Set the prompt label colour to grey

    # Define the list of reasons a user can select for cancelling
    cancellation_reasons = [
        "- Select a reason for cancellation -",
        "Change of Travel Plans",
        "Booking Error",
        "Better Deal Found",
        "Personal Emergency",
        "Other"
    ]

    app.startFrame("cancelBooking_frame1", row=1, column=0, colspan=4)  # Start a frame for form inputs

    app.addEntry("CancelBooking_Ref").config(bd=3, width=28)  # Add an entry field for booking reference
    app.getEntryWidget("CancelBooking_Ref").grid(pady=4, ipady=4)  # Position the entry field
    app.setEntryDefault("CancelBooking_Ref", "Enter Booking Ref")  # Set default placeholder text in entry

    app.addLabel("cancelBooking_emptylabel", "")  # Add empty label to create spacing

    app.addOptionBox("cancelBooking_optionbox", cancellation_reasons).config(width=28)  # Add dropdown for cancellation reasons
    app.getOptionBoxWidget("cancelBooking_optionbox").grid(pady=4, ipady=4)  # Position the dropdown box
    app.getOptionBoxWidget("cancelBooking_optionbox").config(highlightbackground="green", highlightcolor="green", highlightthickness=2, bd=0) # Style the dropdown box

    app.addLabel("spacerCancel1", "")  # Add vertical space
    app.setLabelHeight("spacerCancel1", 2)  # Set height of spacer

    app.addNamedButton("CONTINUE", "btnCancelBookingsConfirm",btnPress)  # Add a "CONTINUE" button to proceed with cancellation
    app.setButtonWidth("btnCancelBookingsConfirm", 300)  # Set width of the "CONTINUE" button

    app.stopFrame()  # End the form input frame

    app.addLabel("spacerCancel2", "")  # Add additional spacing below form

    # Style the "Back" button
    app.setButtonImage("btnCancelBookingsBack", "HOMEBUTTON.gif")  # Set image for the "Back" button
    app.setButtonBg("btnCancelBookingsBack", "white")  # Set background colour to white
    app.setButtonRelief("btnCancelBookingsBack", "flat")  # Remove button border
    app.getButtonWidget("btnCancelBookingsBack").config(activebackground="white", highlightthickness=0,bd=0)  # Style on interaction

    # Style the "CONTINUE" button
    app.setButtonImage("btnCancelBookingsConfirm", "CONTINUEBUTTON.gif")  # Set image for the "CONTINUE" button
    app.setButtonBg("btnCancelBookingsConfirm", "white")  # Set background colour to white
    app.setButtonRelief("btnCancelBookingsConfirm", "flat")  # Remove button border
    app.getButtonWidget("btnCancelBookingsConfirm").config(activebackground="white", highlightthickness=0,bd=0)  # Style on interaction

    app.stopSubWindow()  # End the sub-window for Cancel Bookings
    # END OF CANCEL BOOKINGS #

    app.go()  # Runs the app and displays the GUI

#####################################################################################################################################################
#####################################################################################################################################################

def Image_Of_Car(vehicle_name):  # Define a function that takes the name of a vehicle as input

    car_mapping = {  # Create a dictionary mapping vehicle names to corresponding image identifiers
        "Smart EQ ForTwo": "Car1",
        "Fiat 500 Electric": "Car2",
        "Mini Electric": "Car3",
        "Renault Zoe": "Car4",
        "Peugeot e-208": "Car5",
        "Vauxhall Corsa-e": "Car6",
        "Honda e": "Car7",
        "Citroën Ami": "Car8",
        "Renault Twizy": "Car9",
        "Fiat Panda Electric": "Car10",

        "Nissan Leaf": "Car11",
        "MG 5 Electric": "Car12",
        "Hyundai Kona Electric": "Car13",
        "Citroën ë-Berlingo": "Car14",
        "Kia EV6": "Car15",
        "Tesla Model Y": "Car16",
        "Polestar 2": "Car17",
        "Volkswagen ID.3": "Car18",
        "Mazda MX-30": "Car19",
        "Cupra Born": "Car20",

        "Skoda Enyaq iV": "Car21",
        "Volkswagen ID.4": "Car22",
        "Audi e-tron": "Car23",
        "Mercedes EQB": "Car24",
        "Tesla Model X": "Car25",
        "BMW iX": "Car26",
        "Rivian R1S": "Car27",
        "Mercedes EQS SUV": "Car28",
        "Toyota bZ4X": "Car29",
        "Lexus RZ": "Car30"
    }

    return car_mapping.get(vehicle_name, "Small_CarLogo")  # Return the corresponding image identifier, or a default image if not found

    print(car_mapping.get(vehicle_name, "Small_CarLogo"))

#####################################################################################################################################################
#####################################################################################################################################################

# FAVOURITES PAGE #
global increment_favourites  # Declare a global variable to track the number of times the favourites page is opened
increment_favourites = 0  # Initialise the increment counter to 0

def populateFavourites():  # Define the function to populate the favourites page
    global increment_favourites, favourite_states  # Access the global increment counter

    if increment_favourites != 0:  # Check if the favourites page has been opened before
        app.destroySubWindow(f"win_Favourites{increment_favourites - 1}")  # Destroy the previous instance of the favourites sub-window

    app.startSubWindow(f"win_Favourites{increment_favourites}", title="ElectricCarRental")  # Create a new sub-window for the favourites page
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the window location on the screen

    app.addNamedButton("Back", "btnFavouritesBack", btnPress)  # Add a "Back" button for navigation
    app.getButtonWidget("btnFavouritesBack").grid(sticky="nw", padx=20, pady=10, ipadx=10, ipady=10)  # Position the "Back" button

    app.setBg("white", override=True)  # Set the background colour to white
    app.addImage("favourite_logo", "Small_CarLogo.gif")  # Add a logo image for visual branding
    app.getImageWidget("favourite_logo").grid(row=0, column=3, rowspan=2, sticky="ne", padx=20, pady=10)  # Position the logo

    app.startFrame("favourites_frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the favourites title and prompt
    app.addLabel("lb_favourites", "Favourited Cars").config(font="Arial 35 bold")  # Add a title label for the favourites page
    app.addLabel("favourites_prompt", "View favourited cars and book.")  # Add a prompt label
    app.stopFrame()  # End the frame

    app.setLabelFg("favourites_prompt", "grey")  # Set the font colour of the prompt to grey

    app.startScrollPane("Favourites_ScrollPane", disabled="horizontal", colspan=4).grid(sticky="news")  # Create a scroll pane for the favourites list

    user_email = app.getEntry("Login Email").strip()  # Get the user"s email from the login entry and remove any extra spaces

    cur.execute("SELECT userID FROM tbl_users WHERE userEmail = ?", (user_email,))  # Query the database to find the userID associated with the email
    userID = cur.fetchone()[0]  # Extract the userID from the query result

    cur.execute("""  
        SELECT v.vehicleID, v.vehicleName, v.vehicleType, v.seatingCapacity, v.luggageCapacity  
        FROM tbl_favourites f  
        JOIN tbl_vehicles v ON f.vehicleID = v.vehicleID  
        WHERE f.userID = ?  
    """, (userID,))  # Query the database to find the user"s favourited cars
    favourite_cars = cur.fetchall()  # Fetch all results from the query

    if not favourite_cars:  # Check if no favourited cars were found
        app.addLabel("lb_no_favourites", "No favourited cars found.").config(font="Arial 14 bold")  # Add a label to indicate no favourited cars
        app.getLabelWidget("lb_no_favourites").config(width=82, height=10)  # Configure the label size
    else:  # If favourited cars are found
        rowgrid = 1  # Initialise the row counter for the grid layout
        colgrid = 0  # Initialise the column counter for the grid layout
        max_columns = 2  # Set the maximum number of columns per row

        for car in favourite_cars:  # Iterate through each favourited car
            vehicleID, vehicleName, vehicleType, seatingCapacity, luggageCapacity = car  # Extract car details from the query result

            print(vehicleID, vehicleName, vehicleType, seatingCapacity, luggageCapacity)

            car_details = cars.get(vehicleName, {})  # Get additional car details from the `cars` dictionary
            price_per_day = car_details.get("price_per_day")  # Extract the price per day from the car details

            app.startLabelFrame(f"frame_{vehicleName}_favourites", hideTitle=True, row=rowgrid, column=colgrid)  # Create a labelled frame for the car

            app.addImage(f"image_{vehicleName}_favourites", f"{Image_Of_Car(vehicleName)}.gif", row=0, column=0, rowspan=3)  # Add the car image
            app.getImageWidget(f"image_{vehicleName}_favourites").grid(sticky="ns", padx=3)  # Position the car image

            app.addLabel(f"lb_{vehicleName}_name_favourites", vehicleName, row=0, column=1, colspan=2).grid(sticky="ew")  # Add a label for the car name
            app.getLabelWidget(f"lb_{vehicleName}_name_favourites").config(font="Arial 14 bold")  # Configure the car name label

            app.startFrame(f"frame_type_{vehicleName}_favourites", row=1, column=1, sticky="w")  # Start frame for vehicle type
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"type_{vehicleName}_image_favourites", "Car_Icon.gif", row=0, column=0)  # Add icon for vehicle type
            app.addLabel(f"lb_{vehicleName}_type_favourites", vehicleType, row=0, column=1).config(anchor="w")  # Add vehicle type label
            app.stopFrame()  # End vehicle type frame

            app.startFrame(f"frame_seats_{vehicleName}_favourites", row=1, column=2, sticky="w")  # Start frame for seating capacity
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"seats_{vehicleName}_image_favourites", "Person_Icon.gif", row=0, column=0)  # Add icon for seating
            app.addLabel(f"lb_{vehicleName}_seats_favourites", seatingCapacity, row=0, column=1).config(anchor="w")  # Add seating capacity label
            app.stopFrame()  # End seating frame

            app.startFrame(f"frame_luggage_{vehicleName}_favourites", row=2, column=1, sticky="w")  # Start frame for luggage capacity
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"luggage_{vehicleName}_image_favourites", "Luggage_Icon.gif", row=0, column=0)  # Add icon for luggage
            app.addLabel(f"lb_{vehicleName}_luggage_favourites", luggageCapacity, row=0, column=1).config(anchor="w")  # Add luggage capacity label
            app.stopFrame()  # End luggage frame

            app.startFrame(f"frame_price_{vehicleName}_favourites", row=2, column=2, sticky="w")  # Start frame for price per day
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"price_{vehicleName}_image_favourites", "Money_Icon.gif", row=0, column=0)  # Add icon for price
            app.addLabel(f"lb_{vehicleName}_price_favourites", f"{price_per_day}\nper day", row=0, column=1).config(anchor="w",justify="left")  # Add price label
            app.stopFrame()  # End price frame

            # Add favourite toggle button
            app.addButton(f"btn_{vehicleName}_favourite{increment_favourites}",lambda b=f"btn_{vehicleName}_favourite{increment_favourites}",u=userID, v=vehicleID: toggleFavourite(b, u, v),row=3, column=0)
            app.setButtonImage(f"btn_{vehicleName}_favourite{increment_favourites}", "Filled_Heart.gif")  # Set image to indicate favourited
            app.getButtonWidget(f"btn_{vehicleName}_favourite{increment_favourites}").config(bg="white",relief="flat",activebackground="white",highlightthickness=0,bd=0)  # Configure button styling
            app.getButtonWidget(f"btn_{vehicleName}_favourite{increment_favourites}").grid(sticky="ns", pady=10)  # Position the button

            # Add a "SELECT" button to allow booking
            app.addNamedButton("SELECT", f"btn_{vehicleName}_select{increment_favourites}", btnPress, row=3, column=1, colspan=2).grid(sticky="ns", pady=7)
            app.stopLabelFrame()  # End the labelled frame

            app.setButtonImage(f"btn_{vehicleName}_select{increment_favourites}", "SELECTBUTTON.gif")  # Set image for the SELECT button
            app.setButtonBg(f"btn_{vehicleName}_select{increment_favourites}", "white")  # Set SELECT button background to white
            app.setButtonRelief(f"btn_{vehicleName}_select{increment_favourites}", "flat")  # Make the SELECT button flat
            # Configure the button to remain visually flat on interaction
            app.getButtonWidget(f"btn_{vehicleName}_select{increment_favourites}").config(activebackground="white",highlightthickness=0, bd=0)

            colgrid += 1  # Move to the next column
            if colgrid >= max_columns:  # Check if the maximum number of columns per row is reached
                colgrid = 0  # Reset the column counter
                rowgrid += 1  # Move to the next row

    app.stopScrollPane()  # End the scroll pane

    app.setButtonImage("btnFavouritesBack", "HOMEBUTTON.gif")  # Set the image for the "Back" button
    app.setButtonBg("btnFavouritesBack", "white")  # Set the background colour of the "Back" button to white
    app.setButtonRelief("btnFavouritesBack", "flat")  # Remove the button border style
    app.getButtonWidget("btnFavouritesBack").config(activebackground="white", highlightthickness=0, bd=0)  # Configure button to remain visually flat on interaction

    app.stopSubWindow()  # End the sub-window

    # END OF FAVOURITES PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

# Dictionary to track visibility state for each password field
password_visibility = {}

def toggle_password(password_field, button_name):
    entry_widget = app.getEntryWidget(password_field)  # Get the password entry widget

    # Determine appropriate eye icons based on button context
    if button_name in ["btnShowSignupPassword", "btnShowSignupPassword2"]:
        closed_eye = "Small_ClosedEye.gif"  # Use smaller icons for signup forms
        open_eye = "Small_OpenEye.gif"
    else:
        closed_eye = "ClosedEye.gif"  # Default sized icons
        open_eye = "OpenEye.gif"

    # Toggle visibility state and update UI accordingly
    if password_visibility.get(password_field, False):
        entry_widget.config(show="*")  # Mask password
        app.setButtonImage(button_name, closed_eye)  # Show closed eye icon
        password_visibility[password_field] = False  # Update state
    else:
        entry_widget.config(show="")  # Show plain text
        app.setButtonImage(button_name, open_eye)  # Show open eye icon
        password_visibility[password_field] = True  # Update state

    print(password_visibility)

    # Maintain consistent button styling
    app.getButtonWidget(button_name).config(bg="white", relief="flat", activebackground="white",  highlightthickness=0, bd=0)

#####################################################################################################################################################
#####################################################################################################################################################

attempt_tracker = {}  # Declares a global dictionary to track login attempts for each

def validateLogin(): # Defines the validateLogin function, which handles user login validation.
    MAX_TRIES = 4  # Maximum number of login attempts allowed
    LOCKOUT_TIME = 60  # Time in seconds before attempts reset

    user_email = app.getEntry("Login Email")  # Retrieve entered email from login form
    user_password = app.getEntry("Login Password")  # Retrieve entered password from login form

    #print("email:", user_email)
    #print("password:", user_password)

    if not user_email or not user_password:  # Check if either field is empty
        return app.infoBox("Error", "All fields must be filled out.")  # Display error message if fields are missing

    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", user_email):  # Validate email format using regex
        return app.infoBox("Error", "Invalid email format. Please enter a valid email.")  # Display error for invalid email format

    current_time = time.time()  # Get the current time in seconds
    tries, first_try_time = attempt_tracker.get(user_email, (0, current_time))  # Retrieve previous attempts, or initialize if none exist

    if current_time - first_try_time >= LOCKOUT_TIME:  # Check if lockout period has passed
        tries = 0  # Reset failed attempt count
        first_try_time = current_time  # Reset first attempt timestamp

    if tries >= MAX_TRIES:  # Check if user exceeded max login attempts
        remaining_time = round(LOCKOUT_TIME - (current_time - first_try_time))  # Calculate remaining lockout time
        if remaining_time > 0:  # Ensure remaining time is positive
            print("time:", remaining_time)
            print("attempts:", attempt_tracker)
            return app.infoBox("Error", f"Too many failed attempts. Please try again in {remaining_time} seconds.")  # Notify user of lockout

    cur.execute("SELECT userPassword FROM tbl_users WHERE userEmail = ?", (user_email,))  # Query the database for the email
    saved_password = cur.fetchone()  # Retrieve the stored password for the entered email

    #print("database password:", saved_password)

    if not saved_password:  # Check if email exists in the database
        attempt_tracker[user_email] = (tries + 1, first_try_time)  # Increment failed attempt count
        return app.infoBox("Error", "Email not found. Please check your email or sign up.")  # Display error for non-existent email

    if user_password != saved_password[0]:  # Compare entered password with stored password
        attempt_tracker[user_email] = (tries + 1, first_try_time)  # Increment failed attempt count
        print("number of tries", tries)
        return app.infoBox("Error", f"Incorrect password. Please try again. {4-tries} Tries left.")  # Notify user of incorrect password and remaining attempts

    attempt_tracker.pop(user_email, None)  # Remove user from attempt tracker upon successful login

    app.hideSubWindow("win_Login")  # Hide the login window after successful authentication
    app.showSubWindow("win_Menu")  # Open the main menu window after successful login

#####################################################################################################################################################
#####################################################################################################################################################

def validateSignup(): # Defines validateSignup used to validate user input on sign-up window
    user_firstname = app.getEntry("Signup FirstName").strip()  # Retrieve and trim the first name input
    user_lastname = app.getEntry("Signup LastName").strip()  # Retrieve and trim the last name input
    user_email = app.getEntry("Signup Email").strip()  # Retrieve and trim the email input
    user_phone = app.getEntry("Signup PhoneNum").strip()  # Retrieve and trim the phone number input
    user_password = app.getEntry("Signup Password")  # Retrieve the password input
    user_repassword = app.getEntry("Signup ReEnterPass")  # Retrieve the re-entered password input

    print(user_firstname)
    print(user_lastname)
    print(user_email)
    print(user_phone)
    print(user_password)
    print(user_repassword)

    if not all([user_firstname, user_lastname, user_email, user_phone, user_password, user_repassword]):  # Check if any field is empty
        return app.infoBox("Error", "All fields must be filled out.")  # Display error if any field is missing

    if not user_firstname.isalpha() or not user_lastname.isalpha():  # Check if names contain only alphabetic characters
        return app.infoBox("Error", "First name and last name must contain only alphabetic characters.")  # Display error if names contain non-alphabetic characters

    if not re.match(r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$", user_email):  # Validate email format using regex
        return app.infoBox("Error", "Invalid email format. Please enter a valid email.")  # Display error for invalid email format

    cur.execute("SELECT userEmail FROM tbl_users WHERE userEmail = ?", (user_email,))  # Query database to check if email already exists
    if cur.fetchone():  # If email exists in the database
        return app.infoBox("Error", "This email address has already been taken.")  # Display error for duplicate email

    if not re.match(r"^(?:\+44\s?7\d{3}|07\d{3})\s?\d{3}\s?\d{3}$", user_phone):  # Validate UK phone number format
        return app.infoBox("Error","Invalid phone number. It must be a valid mobile number starting with '+44' or '07'.")  # Display error for invalid phone number

    if len(user_password) <= 8 or not re.search(r"[A-Z]", user_password) or not re.search(r"[a-z]", user_password) or not re.search(r"\d", user_password):  # Check password complexity
        return app.infoBox("Error","Password must be more than 8 characters, contain at least one uppercase letter, one lowercase letter, and one number.")  # Display error for weak password

    if user_password != user_repassword:  # Check if passwords match
        return app.infoBox("Error", "Passwords do not match. Please try again.")  # Display error if passwords do not match

    cur.execute("INSERT INTO tbl_users (firstName, lastName, userPassword, contactNumber, userEmail) VALUES (?, ?, ?, ?, ?)",  # Insert user data into the database
                [user_firstname, user_lastname, user_password, user_phone, user_email])  # Pass user information as parameters
    con.commit()  # Commit changes to the database

    app.hideSubWindow("win_Signup")  # Hide the signup window after successful registration
    app.showSubWindow("win_Login")  # Show the main menu window after successful signup

#####################################################################################################################################################
#####################################################################################################################################################

# Initialise global variables to store the reset code and user ID
reset_code = None  # Stores the randomly generated reset code for password reset
userID = None  # Stores the user ID of the account requesting the reset

def sendEmail(): # Defines the send mail function
    global reset_code, userID  # Use global variables to update them within the function

    sender_email = "electriccarrentalservices@gmail.com"  # Sender"s email address which will send code
    user_email = app.getEntry("ForgotPassword Email").strip()  # Get user input and remove any surrounding whitespace

    print(user_email)

    if not user_email: # Validation for the entry box of email
        return app.infoBox("Error", "Email field is required.")  # Show error if email field is empty

    # Query the database to check if the email exists and retrieve user details
    cur.execute("SELECT userID, firstName, lastName FROM tbl_users WHERE userEmail = ?", (user_email,))
    result = cur.fetchone()  # Fetch the first matching record

    print("user info:", result)

    if result: # If statement to check wether the details exist in the database
        userID, firstname, lastname = result # Checks if results that were typed are equal to database result
        name = firstname + " " + lastname # Sets the name variable to concatenate first name and last name with a space

        reset_code = random.randint(1000, 9999) # Defines a variable that uses the random library to create a four digit code

        print(reset_code)

        # Define the subject of the email to clearly indicate its purpose to the recipient
        subject = "Reset Your Password - Electric Car Rental"  # Email subject line conveying password reset intent

        # Construct the body of the email message with details for resetting the password
        message = (
            f"Dear {name},\n\n" # Includes name of the user so they are addressed personally 
            f"We received a request to reset your password for your Electric Car Rental account.\n" # \n is used to write one new lines
            f"To proceed, please use the following reset code: {reset_code}\n\n" # \n\n is used to start on a new line and create a space
            "Best regards,\n" # \n is used to write on a new line
            "Electric Car Rental Team"
        )

        # Format the email by combining the subject and message content into a single string
        text = f"Subject: {subject}\n\n{message}"  # Ensures the subject appears properly formatted in the email body

        server = smtplib.SMTP("smtp.gmail.com",587)  # Connect to Gmail"s SMTP server on port 587 for email transmission
        server.starttls()  # Upgrade the connection to a secure encrypted TLS connection for security

        server.login(sender_email, "lqizscsznanuinny")  # Logs in to the SMTP server with the sender"s credentials
        server.sendmail(sender_email, user_email, text)  # Sends the formatted email to the user using the send mail function
        server.quit()  # Closes the SMTP connection to free up resources

        # Display a message instructing the user to check their email for the reset code
        app.infoBox("Verification", "Check your email for a 4-digit code.\n"
                    "If you don't find it, please check your \n"
                    "spam folder or junk mail.")

        # Transition from the first password reset window to the next
        app.hideSubWindow("win_ForgotPassword1")  # Hides the first reset password window
        app.showSubWindow("win_ForgotPassword2")  # Displays the second reset password window where the user enters the code

    else:
        # Display an error message if the email does not exist in the database
        app.infoBox("User Not Found", "No user found with the provided email.\n"
                    "Please check your email and try again\n"
                    "or create an account.")

#####################################################################################################################################################
#####################################################################################################################################################

def validateCode(): # Defines function to check if code entered correct
    global reset_code  # Ensures the function can access the reset code

    print(reset_code)

    entered_code = app.getEntry("ForgotPassword Code")  # Retrieves the reset code entered by the user
    entered_code = str(entered_code)  # Converts the entered code to a string for comparison

    print(entered_code)

    if not entered_code:
        return app.infoBox("Error", "Please enter the reset code.")  # Alerts the user if no code is entered

    if entered_code == str(reset_code):  # Checks if the entered code matches the generated reset code
        app.hideSubWindow("win_ForgotPassword2")  # Hides the current window
        app.showSubWindow("win_ForgotPassword3")  # Opens the next window for password resetting
    else:
        app.infoBox("Invalid Code", "The reset code you entered is incorrect.\n"
                    "Please try again.")  # Displays an error if the code is incorrect

#####################################################################################################################################################
#####################################################################################################################################################

def passwordChange():  # Defines function to handle password change process
    global userID  # Ensures the function can access the global userID variable

    user_password = app.getEntry("ForgotPassword_NewPass")  # Retrieves the new password entered by the user
    user_repassword = app.getEntry("ForgotPassword_ReEnterPass")  # Retrieves the re-entered password for confirmation

    print(user_password)
    print(user_repassword)

    if not all([user_password, user_repassword]):  # Checks if both password fields are filled out
        return app.infoBox("Error", "All fields must be filled out.")  # Alerts the user if any field is empty

    # Validates the password and sets the requirements using regular expression
    if len(user_password) <= 8 or not re.search(r"[A-Z]", user_password) or not re.search(r"[a-z]", user_password) or not re.search(r"\d", user_password):
        return app.infoBox("Error", "Password must be more than 8 characters, contain at least one uppercase letter, one lowercase letter, and one number.")
        # Alerts the user if the password doesn"t meet requirements

    if user_password != user_repassword:  # Checks if the password entries match
        return app.infoBox("Error", "Passwords do not match. Please try again.")  # Alerts the user if passwords don"t match

    # Updates the user"s password in the database
    cur.execute("UPDATE tbl_users SET userPassword = ? WHERE userID = ?", [user_password, userID])
    con.commit()  # Commits the changes to the database

    app.infoBox("Update", "Password has been changed.")
    # Notifies the user that the password has been successfully updated

    app.hideSubWindow("win_ForgotPassword3")  # Hides the current window
    app.showSubWindow("win_Login")  # Shows the login window

#####################################################################################################################################################
#####################################################################################################################################################

cars = {
    # Small Cars
    "Smart EQ ForTwo": {"category": "Small", "price": "£0–£50", "price_per_day": "£30", "seats": "2 Seats", "luggage": "1 Small Bag"},
    "Fiat 500 Electric": {"category": "Small", "price": "£50–£100", "price_per_day": "£70", "seats": "2 Seats", "luggage": "1 Small Bag"},
    "Mini Electric": {"category": "Small", "price": "£100–£150", "price_per_day": "£120", "seats": "2 Seats", "luggage": "2 Small Bags"},
    "Renault Zoe": {"category": "Small", "price": "£0–£50", "price_per_day": "£30", "seats": "5 Seats", "luggage": "2 Small Bags"},
    "Peugeot e-208": {"category": "Small", "price": "£50–£100", "price_per_day": "£70", "seats": "5 Seats", "luggage": "3+ Small Bags"},
    "Vauxhall Corsa-e": {"category": "Small", "price": "£100–£150", "price_per_day": "£120", "seats": "5 Seats", "luggage": "3+ Small Bags"},
    "Honda e": {"category": "Small", "price": "£0–£50", "price_per_day": "£30", "seats": "2 Seats", "luggage": "1 Small Bag"},
    "Citroën Ami": {"category": "Small", "price": "£0–£50", "price_per_day": "£25", "seats": "2 Seats", "luggage": "1 Small Bag"},
    "Renault Twizy": {"category": "Small", "price": "£0–£50", "price_per_day": "£25", "seats": "2 Seats", "luggage": "2 Small Bags"},
    "Fiat Panda Electric": {"category": "Small", "price": "£100–£150", "price_per_day": "£120", "seats": "5 Seats", "luggage": "1 Small Bag"},

    # Medium Cars
    "Nissan Leaf": {"category": "Medium", "price": "£0–£50", "price_per_day": "£30", "seats": "5 Seats", "luggage": "2 Small Bags"},
    "MG 5 Electric": {"category": "Medium", "price": "£50–£100", "price_per_day": "£80", "seats": "5 Seats", "luggage": "2 Small Bags"},
    "Hyundai Kona Electric": {"category": "Medium", "price": "£100–£150", "price_per_day": "£120", "seats": "5 Seats", "luggage": "3+ Small Bags"},
    "Citroën ë-Berlingo": {"category": "Medium", "price": "£0–£50", "price_per_day": "£40", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Kia EV6": {"category": "Medium", "price": "£50–£100", "price_per_day": "£90", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Tesla Model Y": {"category": "Medium", "price": "£100–£150", "price_per_day": "£130", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Polestar 2": {"category": "Medium", "price": "£50–£100", "price_per_day": "£80", "seats": "5 Seats", "luggage": "2 Small Bags"},
    "Volkswagen ID.3": {"category": "Medium", "price": "£0–£50", "price_per_day": "£40", "seats": "5 Seats", "luggage": "2 Small Bags"},
    "Mazda MX-30": {"category": "Medium", "price": "£0–£50", "price_per_day": "£50", "seats": "5 Seats", "luggage": "1 Small Bag"},
    "Cupra Born": {"category": "Medium", "price": "£50–£100", "price_per_day": "£70", "seats": "5 Seats", "luggage": "1 Small Bag"},

    # Large Cars
    "Skoda Enyaq iV": {"category": "Large", "price": "£0–£50", "price_per_day": "£50", "seats": "5 Seats", "luggage": "3+ Small Bags"},
    "Volkswagen ID.4": {"category": "Large", "price": "£50–£100", "price_per_day": "£90", "seats": "5 Seats", "luggage": "3+ Small Bags"},
    "Audi e-tron": {"category": "Large", "price": "£100–£150", "price_per_day": "£130", "seats": "5 Seats", "luggage": "3+ Small Bags"},
    "Mercedes EQB": {"category": "Large", "price": "£0–£50", "price_per_day": "£50", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Tesla Model X": {"category": "Large", "price": "£50–£100", "price_per_day": "£100", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "BMW iX": {"category": "Large", "price": "£100–£150", "price_per_day": "£140", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Rivian R1S": {"category": "Large", "price": "£100–£150", "price_per_day": "£150", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Mercedes EQS SUV": {"category": "Large", "price": "£50–£100", "price_per_day": "£100", "seats": "7 Seats", "luggage": "3+ Small Bags"},
    "Toyota bZ4X": {"category": "Large", "price": "£0–£50", "price_per_day": "£50", "seats": "5 Seats", "luggage": "2 Small Bags"},
    "Lexus RZ": {"category": "Large", "price": "£100–£150", "price_per_day": "£130", "seats": "5 Seats", "luggage": "2 Small Bags"}
}

def getBooking(): # Function to retrieve cars that match the filters the user has chosen
    global car
    if app.getCheckBox("bookingPageCheckBox"):  # Check if the booking checkbox is selected
        return list(cars.keys())  # Return all available cars

    category = app.getRadioButton("category")  # Get selected car category
    price = app.getRadioButton("price")  # Get selected price range
    seats = app.getRadioButton("seats")  # Get selected number of seats
    luggage = app.getRadioButton("luggage")  # Get selected luggage capacity

    # Query the database for vehicle IDs, names, and stock
    cur.execute("SELECT vehicleID, vehicleName, Stock FROM tbl_vehicles")

    available_cars = []  # Initialise an empty set to store available car names

    for vehicleID, vehicleName, stock in cur.fetchall():  # Iterate through each car in the database
        if stock > 0:  # If the stock is greater than 0
            available_cars.append(vehicleName) # Add the car name to the end of the list

    matching_cars = []  # Initialise an empty list to store matching cars

    for car, specs in cars.items(): # Loop through every car and specification in the car dictionary
        # Check if car matches the selected criteria that user has picked
        if (specs["category"] == category and specs["price"] == price and specs["seats"] == seats and specs["luggage"] == luggage):
            if car in available_cars: # Only include cars with stock > 0
                 matching_cars.append(car)  # Add matching car to the end of the list

    return matching_cars  # Return the list of matching cars


#####################################################################################################################################################
#####################################################################################################################################################

# BOOKING PAGE #
global increment_bookingpage  # Declares the global variable to track how many times the booking page has been opened
increment_bookingpage = 0  # Initialises the counter for the booking page to 0

def populateCars():  # Defines the function to populate and display the booking page with available car options

    global increment_bookingpage, matching_result_global, userID  # Accesses the global variables for the counter, matching cars, and userID

    if increment_bookingpage != 0:  # Checks if this is not the first time opening the booking page
        app.destroySubWindow(f"win_BookingPage{increment_bookingpage - 1}")  # Closes the previous booking page to prevent duplication

    app.startSubWindow(f"win_BookingPage{increment_bookingpage}", title="ElectricCarRental")  # Starts a new sub-window for the current booking page
    app.setSize("1000x500")  # Sets the size of the booking page window
    app.setResizable(False)  # Makes the window non-resizable for UI consistency
    app.setLocation(500, 250)  # Sets the location of the window on the screen

    app.addNamedButton("Back", "btnBookingBack2", btnPress)  # Adds a "Back" button to go back to the previous page
    app.getButtonWidget("btnBookingBack2").grid(sticky="nw", padx=20, pady=10, ipadx=10, ipady=10)  # Positions the button in the top-left corner with padding

    app.setBg("white", override=True)  # Sets the background color of the window to white
    app.addImage("booking_logo", "Small_CarLogo.gif")  # Adds the logo image to the window
    app.getImageWidget("booking_logo").grid(row=0, column=3, rowspan=2, sticky="ne", padx=20, pady=10)  # Positions the logo in the top-right corner with padding

    app.startFrame("Booking Page 2 Frame", row=0, column=0, colspan=4).grid(sticky="n")  # Creates a frame for the header section of the page
    app.addLabel("lb_booking2", "Create Booking").config(font="Arial 35 bold")  # Adds a title for the page with large and bold font
    app.addLabel("booking2_prompt", "Select a car which matches your needs.")  # Adds a prompt asking the user to select a car
    app.stopFrame()  # Ends the header frame

    app.setLabelFg("booking2_prompt", "grey")  # Sets the color of the prompt text to grey

    # Creates a scrollable pane where available cars will be displayed
    app.startScrollPane("Car_Bookings", disabled="horizontal", colspan=4).grid(sticky="news")

    rowgrid = 1  # Initializes the row index for placing cars in the grid
    colgrid = 0  # Initializes the column index for placing cars in the grid
    max_columns = 2  # Sets the maximum number of columns per row in the grid

    user_email = app.getEntry("Login Email").strip()  # Gets the user"s email from the entry field and removes any extra spaces

    # Queries the database to get the userID based on the user"s email
    cur.execute("SELECT userID FROM tbl_users WHERE userEmail = ?", (user_email,))
    userID = cur.fetchone()[0]  # Stores the userID in a variable

    car_ids = {}  # Initializes a dictionary to store car names and their corresponding vehicle IDs
    cur.execute("SELECT vehicleID, vehicleName FROM tbl_vehicles")  # Queries the database for vehicle IDs and names
    for row in cur.fetchall():  # Iterates through the results of the query
        vehicle_id, vehicleName = row  # Extracts the vehicle ID and name from each row of the result
        if vehicleName in cars:  # Checks if the car is present in the "cars" dictionary
            car_ids[vehicleName] = vehicle_id  # Adds the car ID to the dictionary with the car name as the key

    # Loops through the list of cars that match the user"s search criteria
    for car in matching_result_global:
        vehicle_id = car_ids.get(car)  # Retrieves the vehicle ID for the current car from the car_ids dictionary
        specs = cars[car]  # Retrieves the car specifications from the "cars" dictionary

        # Checks if the car is already in the user"s favourites list in the database
        cur.execute("SELECT * FROM tbl_favourites WHERE userID = ? AND vehicleID = ?", (userID, vehicle_id))
        is_favourited = cur.fetchone() is not None  # Sets "is_favourited" to True if the car is already a favourite

        app.startLabelFrame(f"frame_{car}", hideTitle=True, row=rowgrid, column=colgrid)  # Starts a frame for the current car"s details

        app.addImage(f"image_{car}", f"{Image_Of_Car(car)}.gif", row=0, column=0, rowspan=3)  # Adds the car image to the frame
        app.getImageWidget(f"image_{car}").grid(sticky="ns", padx=3)  # Positions the image within the grid

        app.addLabel(f"lb_{car}_name", car, row=0, column=1, colspan=2).grid(sticky="ew")  # Adds a label with the car name as a header
        app.getLabelWidget(f"lb_{car}_name").config(font="Arial 14 bold")  # Applies bold font styling to the car name

        # Adds a frame for the car type information
        app.startFrame(f"frame_type_{car}", row=1, column=1, sticky="w")
        app.setPadding([9, 9])  # Sets padding for the frame
        app.addImage(f"type_{car}_image", "Car_Icon.gif", row=0, column=0)  # Adds an image icon for the car type
        app.addLabel(f"lb_{car}_type", specs["category"], row=0, column=1).config(anchor="w")  # Adds the car type label
        app.stopFrame()  # Ends the car type frame

        # Adds a frame for the car seat information
        app.startFrame(f"frame_seats_{car}", row=1, column=2, sticky="w")
        app.setPadding([9, 9])  # Sets padding for the frame
        app.addImage(f"seats_{car}_image", "Person_Icon.gif", row=0, column=0)  # Adds an image icon for seats
        app.addLabel(f"lb_{car}_seats", specs["seats"], row=0, column=1).config(anchor="w")  # Adds the seat information label
        app.stopFrame()  # Ends the seat frame

        # Adds a frame for the luggage capacity information
        app.startFrame(f"frame_luggage_{car}", row=2, column=1, sticky="w")
        app.setPadding([9, 9])  # Sets padding for the frame
        app.addImage(f"luggage_{car}_image", "Luggage_Icon.gif", row=0, column=0)  # Adds an image icon for luggage
        app.addLabel(f"lb_{car}_luggage", specs["luggage"], row=0, column=1).config(anchor="w")  # Adds the luggage capacity label
        app.stopFrame()  # Ends the luggage frame

        # Adds a frame for the pricing information
        app.startFrame(f"frame_price_{car}", row=2, column=2, sticky="w")
        app.setPadding([9, 9])  # Sets padding for the frame
        app.addImage(f"price_{car}_image", "Money_Icon.gif", row=0, column=0)  # Adds an image icon for price
        app.addLabel(f"lb_{car}_price", f"{specs['price_per_day']}\nper day", row=0, column=1).config(anchor="w", justify="left")  # Adds the price label
        app.stopFrame()  # Ends the price frame

        # Adds a button to toggle whether the car is a favourite
        app.addButton(f"btn_{car}_favourite", lambda b=f"btn_{car}_favourite", u=userID, v=vehicle_id: toggleFavourite(b, u, v), row=3, column=0)

        # Sets the button image based on whether the car is already a favourite
        if is_favourited:
            app.setButtonImage(f"btn_{car}_favourite", "Filled_Heart.gif")  # If favourited, display a filled heart icon
        else:
            app.setButtonImage(f"btn_{car}_favourite", "Empty_Heart.gif")  # If not favourited, display an empty heart icon

        app.getButtonWidget(f"btn_{car}_favourite").config(bg="white", relief="flat", activebackground="white", highlightthickness=0, bd=0)  # Customizes the button style
        app.getButtonWidget(f"btn_{car}_favourite").grid(sticky="ns", pady=10)  # Positions the favourite button

        # Adds a "SELECT" button for each car
        app.addNamedButton("SELECT", f"btn_{car}_select", btnPress, row=3, column=1, colspan=2).grid(sticky="ns", pady=7)  # Adds the SELECT button
        app.setButtonImage(f"btn_{car}_select", "SELECTBUTTON.gif")  # Sets the image for the SELECT button
        app.setButtonBg(f"btn_{car}_select", "white")  # Sets the background color for the SELECT button
        app.setButtonRelief(f"btn_{car}_select", "flat")  # Sets the button"s border relief style
        app.getButtonWidget(f"btn_{car}_select").config(activebackground="white", highlightthickness=0, bd=0)  # Customizes the SELECT button style

        app.stopLabelFrame()  # Ends the frame for the current car"s details

        colgrid += 1  # Moves to the next column in the grid for the next car
        if colgrid >= max_columns:  # If the maximum number of columns is reached, reset column index and move to the next row
            colgrid = 0
            rowgrid += 1

    app.stopScrollPane()  # Ends the scrollable pane

    # Customizes the "Back" button
    app.setButtonImage("btnBookingBack2", "HOMEBUTTON.gif")  # Sets the image for the back button
    app.setButtonBg("btnBookingBack2", "white")  # Sets the background color for the back button
    app.setButtonRelief("btnBookingBack2", "flat")  # Sets the border relief for the back button
    app.getButtonWidget("btnBookingBack2").config(activebackground="white", highlightthickness=0, bd=0)  # Customizes the back button style

    app.stopSubWindow()  # Ends the current booking page window
    # END OF BOOKING PAGE #

#####################################################################################################################################################
#####################################################################################################################################################

# Dictionary to store the favourite state of each car for each user
favourite_states = {}

# Function to toggle the favourite status of a car for a user
def toggleFavourite(button_name, userID, vehicle_id):
    # Get the current state of the favourite (True if it"s marked as favourite, False otherwise)
    current_state = favourite_states.get((userID, vehicle_id), True)

    # If the car is currently marked as a favourite, remove it from favourites
    if current_state:
        app.setButtonImage(button_name, "Empty_Heart.gif")  # Change the button image to show empty heart (not favourite)
        # Remove the car from the favourites table in the database
        cur.execute("DELETE FROM tbl_favourites WHERE userID = ? AND vehicleID = ?",
                    (userID, vehicle_id))
        new_state = False  # Set the new state to False (not favourite)
    else:
        # If the car is not currently a favourite, add it to favourites
        app.setButtonImage(button_name, "Filled_Heart.gif")  # Change the button image to show filled heart (favourite)
        # Add the car to the favourites table in the database
        cur.execute("INSERT INTO tbl_favourites (userID, vehicleID) VALUES (?, ?)",
                    (userID, vehicle_id))
        new_state = True  # Set the new state to True (favourite)

    con.commit()  # Commit the changes to the database
    # Update the favourite state for the user and car in the dictionary
    favourite_states[(userID, vehicle_id)] = new_state

    print(new_state)

    # Customise the button appearance (background colour, relief, active background, highlight thickness, and border)
    app.getButtonWidget(button_name).config(bg="white", relief="flat", activebackground="white", highlightthickness=0, bd=0)

#####################################################################################################################################################
#####################################################################################################################################################

# PAST BOOKINGS #
global increment_pastbookings  # Declare a global variable to track the number of times the past bookings page is opened
increment_pastbookings = 0  # Initialise the increment counter to 0

def populatePastBookings():  # Define the function to populate the past bookings page
    global increment_pastbookings  # Access the global increment counter
 
    if increment_pastbookings != 0:  # Check if the past bookings page has been opened before
        app.destroySubWindow(f"win_PastBookings{increment_pastbookings - 1}")  # Destroy the previous instance of the past bookings sub-window

    app.startSubWindow(f"win_PastBookings{increment_pastbookings}", title="ElectricCarRental")  # Create a new sub-window for the past bookings page
    app.setSize("1000x500")  # Set the window size to 1000x500 pixels
    app.setResizable(False)  # Disable window resizing
    app.setLocation(500, 250)  # Set the window location to coordinates (500, 250)

    app.addNamedButton("Back", f"btnPastBookingsBack", btnPress)  # Add a "Back" button for navigation
    app.getButtonWidget(f"btnPastBookingsBack").grid(sticky="nw", padx=20, pady=10, ipadx=10, ipady=10)  # Position the "Back" button

    app.setBg("white", override=True)  # Set background colour to white
    app.addImage("pastbooking_logo", "Small_CarLogo.gif")  # Add logo to top right
    app.getImageWidget("pastbooking_logo").grid(row=0, column=3, rowspan=2, sticky="ne", padx=20, pady=10)  # Position the logo image

    app.startFrame(f"past_bookings_frame", row=0, column=0, colspan=4).grid(sticky="n")  # Create a frame for the past bookings title and prompt
    app.addLabel(f"lb_pastBookings", "Past Bookings").config(font="Arial 35 bold")  # Add a title label for the past bookings page
    app.addLabel(f"past_bookings_prompt", "Select a past booking to view or book.")  # Add a prompt label
    app.stopFrame()  # End the frame

    app.setLabelFg(f"past_bookings_prompt", "grey")  # Set the prompt colour to grey

    app.startScrollPane("PastBookings_ScrollPane", disabled="horizontal", colspan=4).grid(sticky="news")  # Create a scroll pane for the past bookings list

    user_email = app.getEntry("Login Email").strip()  # Get the user"s email from the login entry and remove any extra spaces

    cur.execute("SELECT userID FROM tbl_users WHERE userEmail = ?", (user_email,))  # Query the database to find the userID associated with the email
    userID = cur.fetchone()[0]  # Extract the userID from the query result

    current_datetime = datetime.now()  # Get the current date and time

    cur.execute("""
        SELECT b.bookingRef, v.vehicleName, v.vehicleType, v.seatingCapacity, v.luggageCapacity, bd.pricePerDay,
               b.bookingPickupDate, b.bookingDropoffDate, b.bookingPickUpTime, b.bookingDropoffTime, bd.totalCost
        FROM tbl_bookings b
        JOIN tbl_bookingDetails bd ON b.bookingID = bd.bookingID
        JOIN tbl_vehicles v ON bd.vehicleID = v.vehicleID
        WHERE b.userID = ?
    """, (userID,))
    all_bookings = cur.fetchall()  # Fetch all results from the query

    past_bookings = []  # Initialise an empty list to store past bookings
    for booking in all_bookings:  # Iterate through all bookings
        bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, \
            bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost = booking  # Extract booking details

        print(bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost)

        dropoff_datetime_str = f"{bookingDropoffDate} {bookingDropoffTime}"  # Combine the drop-off date and time into a single string
        dropoff_datetime = datetime.strptime(dropoff_datetime_str, "%d %b %Y %H:%M")  # Convert the drop-off date and time into a datetime object

        if dropoff_datetime < current_datetime:  # Check if the booking is in the past
            past_bookings.append(booking)  # Add the booking to the past bookings list

    if not past_bookings:  # Check if no past bookings were found
        app.addLabel(f"lb_no_past_bookings{increment_pastbookings}", "No past bookings found.").config(font="Arial 14 bold")  # Add a label to indicate no past bookings
        app.getLabelWidget(f"lb_no_past_bookings{increment_pastbookings}").config(width=82, height=10)  # Configure the label size
    else:  # If past bookings are found
        rowgrid = 1  # Initialise the row counter for the grid layout
        colgrid = 0  # Initialise the column counter for the grid layout
        max_columns = 2  # Set the maximum number of columns per row

        for booking in past_bookings:  # Iterate through each past booking
            bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, \
                bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost = booking  # Extract booking details

            app.startLabelFrame(f"frame_{bookingRef}_pastbooking", hideTitle=True, row=rowgrid, column=colgrid)  # Create a labelled frame for the booking

            app.addImage(f"image_{bookingRef}_pastbooking", f"{Image_Of_Car(vehicleName)}.gif", row=0, column=0, rowspan=3)  # Display vehicle image
            app.getImageWidget(f"image_{bookingRef}_pastbooking").grid(sticky="ns", padx=3)  # Style the vehicle image widget

            app.addLabel(f"lb_{bookingRef}_name_pastbooking", vehicleName, row=0, column=1, colspan=2).grid(sticky="ew")  # Add a label for the car name
            app.getLabelWidget(f"lb_{bookingRef}_name_pastbooking").config(font="Arial 14 bold")  # Configure the car name label

            app.startFrame(f"frame_type_{bookingRef}_pastbooking", row=1, column=1, sticky="w")  # Start frame for car type
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"type_{bookingRef}_image_pastbooking", "Car_Icon.gif", row=0, column=0)  # Add icon for car type
            app.addLabel(f"lb_{bookingRef}_type_pastbooking", vehicleType, row=0, column=1).config(anchor="w")  # Add label for car type
            app.stopFrame()  # End frame for car type

            app.startFrame(f"frame_seats_{bookingRef}_pastbooking", row=1, column=2, sticky="w")  # Start frame for seating
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"seats_{bookingRef}_image_pastbooking", "Person_Icon.gif", row=0, column=0)  # Add icon for seating capacity
            app.addLabel(f"lb_{bookingRef}_seats_pastbooking", seatingCapacity, row=0, column=1).config(anchor="w")  # Add label for seating capacity
            app.stopFrame()  # End frame for seating

            app.startFrame(f"frame_luggage_{bookingRef}_pastbooking", row=2, column=1, sticky="w")  # Start frame for luggage
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"luggage_{bookingRef}_image_pastbooking", "Luggage_Icon.gif", row=0, column=0)  # Add icon for luggage capacity
            app.addLabel(f"lb_{bookingRef}_luggage_pastbooking", luggageCapacity, row=0, column=1).config(anchor="w")  # Add label for luggage capacity
            app.stopFrame()  # End frame for luggage

            app.startFrame(f"frame_price_{bookingRef}_pastbooking", row=2, column=2, sticky="w")  # Start frame for price
            app.setPadding([9, 9])  # Set padding inside the frame
            app.addImage(f"price_{bookingRef}_image_pastbooking", "Money_Icon.gif", row=0, column=0)  # Add icon for price
            app.addLabel(f"lb_{bookingRef}_price_pastbooking", f"{pricePerDay}\nper day", row=0, column=1).config(anchor="w", justify="left")  # Add price label
            app.stopFrame()  # End frame for price

            app.addLabel(f"lb_{bookingRef}_ref_pastbooking", f"Booking Ref: {bookingRef}", row=3,column=0)  # Add label for booking reference
            app.getLabelWidget(f"lb_{bookingRef}_ref_pastbooking").config(anchor="n", justify="center",padx=5)  # Configure booking reference label

            app.addNamedButton("VIEW BOOKING", f"btn_{bookingRef}_view", btnPress, row=3, column=1,colspan=2).grid(sticky="ns", pady=7)  # Add a "VIEW BOOKING" button
            app.setButtonImage(f"btn_{bookingRef}_view", "SELECTBUTTON.gif")  # Set image for the button
            app.setButtonBg(f"btn_{bookingRef}_view", "white")  # Set button background to white
            app.setButtonRelief(f"btn_{bookingRef}_view", "flat")  # Remove button border
            app.getButtonWidget(f"btn_{bookingRef}_view").config(activebackground="white",highlightthickness=0, bd=0)  # Configure active styling for button

            app.stopLabelFrame()  # End the labelled frame for the booking

            colgrid += 1  # Move to the next column
            if colgrid >= max_columns:  # Check if the maximum number of columns per row is reached
                colgrid = 0  # Reset the column counter
                rowgrid += 1  # Move to the next row

    app.stopScrollPane()  # End the scroll pane

    app.setButtonImage("btnPastBookingsBack", "HOMEBUTTON.gif")  # Set image for the "Back" button
    app.setButtonBg("btnPastBookingsBack", "white")  # Set the background colour of the "Back" button
    app.setButtonRelief("btnPastBookingsBack", "flat")  # Remove the border of the "Back" button
    app.getButtonWidget("btnPastBookingsBack").config(activebackground="white", highlightthickness=0, bd=0)  # Configure the "Back" button appearance

    app.stopSubWindow()  # End the sub-window

# END OF PAST BOOKINGS #

#####################################################################################################################################################
#####################################################################################################################################################

# FUTURE BOOKINGS #
global increment_futurebookings  # Declare a global variable to track the number of times the future bookings page is opened
increment_futurebookings = 0  # Initialise the increment counter to 0

def populateFutureBookings():  # Define the function to populate the future bookings page
    global increment_futurebookings  # Access the global increment counter

    if increment_futurebookings != 0:  # Check if the future bookings page has been opened before
        app.destroySubWindow(f"win_FutureBookings{increment_futurebookings - 1}")  # Destroy the previous instance of the future bookings window

    # Start a new sub-window for future bookings with a unique identifier based on the increment counter
    app.startSubWindow(f"win_FutureBookings{increment_futurebookings}", title="ElectricCarRental")
    app.setSize("1000x500")  # Set the size of the sub-window to 1000x500
    app.setResizable(False)  # Disable resizing of the sub-window
    app.setLocation(500, 250)  # Position the sub-window at screen coordinates (500, 250)

    # Add a Back button to the window and position it at the top-left
    app.addNamedButton("Back", f"btnFutureBookingsBack", btnPress)
    app.getButtonWidget(f"btnFutureBookingsBack").grid(sticky="nw", padx=20, pady=10, ipadx=10, ipady=10)  # Grid placement of the back button

    # Set the background colour of the window to white
    app.setBg("white", override=True)
    app.addImage("futurebooking_logo", "Small_CarLogo.gif")  # Add the logo image to the top-right of the window
    app.getImageWidget("futurebooking_logo").grid(row=0, column=3, rowspan=2, sticky="ne", padx=20, pady=10)  # Position the logo image

    # Start the frame for the future bookings title and prompt
    app.startFrame(f"future_bookings_frame", row=0, column=0, colspan=4).grid(sticky="n")
    app.addLabel(f"lb_futureBookings", "Future Bookings").config(font="Arial 35 bold")  # Add and style the title label
    app.addLabel(f"future_bookings_prompt", "Select a future booking to view or amend.")  # Add a prompt label
    app.stopFrame()  # End the title and prompt frame

    app.setLabelFg(f"future_bookings_prompt", "grey") # Set the colour of the prompt text to grey

    # Start a scroll pane for displaying the future bookings
    app.startScrollPane("FutureBookings_ScrollPane", disabled="horizontal", colspan=4).grid(sticky="news")

    # Retrieve the current user"s email
    user_email = app.getEntry("Login Email").strip()
    # Query the database to fetch the userID based on the email
    cur.execute("SELECT userID FROM tbl_users WHERE userEmail = ?", (user_email,))
    userID = cur.fetchone()[0]  # Get the userID from the query result
    current_datetime = datetime.now()  # Get the current date and time

    # Query the database to fetch the user"s future bookings
    cur.execute("""  
        SELECT b.bookingRef, v.vehicleName, v.vehicleType, v.seatingCapacity, v.luggageCapacity, bd.pricePerDay,
               b.bookingPickupDate, b.bookingDropoffDate, b.bookingPickUpTime, b.bookingDropoffTime, bd.totalCost
        FROM tbl_bookings b
        JOIN tbl_bookingDetails bd ON b.bookingID = bd.bookingID
        JOIN tbl_vehicles v ON bd.vehicleID = v.vehicleID
        WHERE b.userID = ?
    """, (userID,))
    all_bookings = cur.fetchall()  # Fetch all bookings from the database

    future_bookings = []  # Initialise a list to hold future bookings
    for booking in all_bookings:  # Loop through each booking
        bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, \
            bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost = booking

        print(bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, bookingPickupDate,bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost)

        # Combine dropoff date and time into a datetime string
        dropoff_datetime_str = f"{bookingDropoffDate} {bookingDropoffTime}"
        dropoff_datetime = datetime.strptime(dropoff_datetime_str, "%d %b %Y %H:%M")  # Convert the string into a datetime object

        # Add the booking to the future bookings list if the dropoff date is in the future
        if dropoff_datetime > current_datetime:
            future_bookings.append(booking)  # Append the booking if it"s in the future

    if not future_bookings:  # Check if there are no future bookings
        # Display a message if no future bookings are found
        app.addLabel(f"lb_no_future_bookings", "No future bookings found.").config(font="Arial 14 bold")
        app.getLabelWidget(f"lb_no_future_bookings").config(width=82, height=10)  # Set label width and height if no bookings
    else:  # If there are future bookings, display them
        rowgrid = 1  # Initialise grid row
        colgrid = 0  # Initialise grid column
        max_columns = 2  # Set the maximum number of columns to 2

        # Loop through each future booking
        for booking in future_bookings:
            bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, \
                bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost = booking

            # Start a label frame for each booking entry
            app.startLabelFrame(f"frame_{bookingRef}_futurebooking", hideTitle=True, row=rowgrid, column=colgrid)

            # Add an image of the vehicle associated with the booking
            app.addImage(f"image_{bookingRef}_futurebooking", f"{Image_Of_Car(vehicleName)}.gif", row=0, column=0,rowspan=3)
            app.getImageWidget(f"image_{bookingRef}_futurebooking").grid(sticky="ns", padx=3)  # Position the image

            # Add the vehicle name label and style it
            app.addLabel(f"lb_{bookingRef}_name_futurebooking", vehicleName, row=0, column=1, colspan=2).grid(sticky="ew")
            app.getLabelWidget(f"lb_{bookingRef}_name_futurebooking").config(font="Arial 14 bold")  # Set the font for the vehicle name label

            # Start a frame for the vehicle type and add the icon and label
            app.startFrame(f"frame_type_{bookingRef}_futurebooking", row=1, column=1, sticky="w")
            app.setPadding([9, 9])  # Set padding for the frame
            app.addImage(f"type_{bookingRef}_image_futurebooking", "Car_Icon.gif", row=0, column=0)  # Add an image for the vehicle type
            app.addLabel(f"lb_{bookingRef}_type_futurebooking", vehicleType, row=0, column=1).config(anchor="w")  # Add label for vehicle type
            app.stopFrame()  # End the vehicle type frame

            # Start a frame for seating capacity and add the icon and label
            app.startFrame(f"frame_seats_{bookingRef}_futurebooking", row=1, column=2, sticky="w")
            app.setPadding([9, 9])  # Set padding for the frame
            app.addImage(f"seats_{bookingRef}_image_futurebooking", "Person_Icon.gif", row=0, column=0)  # Add an image for seating capacity
            app.addLabel(f"lb_{bookingRef}_seats_futurebooking", seatingCapacity, row=0, column=1).config(anchor="w")  # Add label for seating capacity
            app.stopFrame()  # End the seating capacity frame

            # Start a frame for luggage capacity and add the icon and label
            app.startFrame(f"frame_luggage_{bookingRef}_futurebooking", row=2, column=1, sticky="w")
            app.setPadding([9, 9])  # Set padding for the frame
            app.addImage(f"luggage_{bookingRef}_image_futurebooking", "Luggage_Icon.gif", row=0, column=0)  # Add an image for luggage capacity
            app.addLabel(f"lb_{bookingRef}_luggage_futurebooking", luggageCapacity, row=0, column=1).config(anchor="w")  # Add label for luggage capacity
            app.stopFrame()  # End the luggage capacity frame

            # Start a frame for price and add the icon and label
            app.startFrame(f"frame_price_{bookingRef}_futurebooking", row=2, column=2, sticky="w")
            app.setPadding([9, 9])  # Set padding for the frame
            app.addImage(f"price_{bookingRef}_image_futurebooking", "Money_Icon.gif", row=0, column=0)  # Add an image for price
            pricePerDay = pricePerDay.split(" per day")[0]  # Remove the " per day" part from the price string
            app.addLabel(f"lb_{bookingRef}_price_futurebooking", f"{pricePerDay}\nper day", row=0, column=1).config(anchor="w", justify="left")  # Add price label
            app.stopFrame()  # End the price frame

            # Add a label for the booking reference
            app.addLabel(f"lb_{bookingRef}_ref_futurebooking", f"Booking Ref: {bookingRef}", row=3, column=0)
            app.getLabelWidget(f"lb_{bookingRef}_ref_futurebooking").config(anchor="n", justify="center", padx=5)  # Set label alignment

            # Add a button to view the booking details
            app.addNamedButton("VIEW BOOKING", f"btn_{bookingRef}_view_future", btnPress, row=3, column=1,colspan=2).grid(sticky="ns", pady=7)
            app.setButtonImage(f"btn_{bookingRef}_view_future", "SELECTBUTTON.gif")  # Set button image
            app.setButtonBg(f"btn_{bookingRef}_view_future", "white")  # Set button background to white
            app.setButtonRelief(f"btn_{bookingRef}_view_future", "flat")  # Remove the border of the button
            app.getButtonWidget(f"btn_{bookingRef}_view_future").config(activebackground="white", highlightthickness=0, bd=0)  # Configure button appearance
            app.stopLabelFrame()  # End the label frame for the booking

            colgrid += 1  # Increment column counter
            if colgrid >= max_columns:  # If the maximum number of columns is reached, reset column and increment row
                colgrid = 0
                rowgrid += 1

    # Stop the scroll pane for future bookings
    app.stopScrollPane()

    # Modify the Back button to display a home icon and reset its appearance
    app.setButtonImage("btnFutureBookingsBack", "HOMEBUTTON.gif")
    app.setButtonBg("btnFutureBookingsBack", "white")  # Set background to white
    app.setButtonRelief("btnFutureBookingsBack", "flat")  # Remove the border of the button
    app.getButtonWidget("btnFutureBookingsBack").config(activebackground="white", highlightthickness=0, bd=0)  # Configure button appearance

    app.stopSubWindow()

    # END OF FUTURE BOOKINGS #

#####################################################################################################################################################
#####################################################################################################################################################

def bookingDetails_Database(): # Define the function to save booking details to the database
    global total_price, total_duration, booking_ref # Declare global variables for total price, duration, and booking reference
    user_email = app.getEntry("Login Email").strip() # Get the user"s email from the login entry and remove any extra spaces

    cur.execute("SELECT userID FROM tbl_users WHERE userEmail = ?", (user_email,)) # Query the database to find the userID associated with the email
    user_result = cur.fetchone() # Fetch the result of the query

    userID = user_result[0] # Extract the userID from the query result

    car_name = app.getLabel("cartest") # Get the car name from the label
    price_per_day = app.getLabel("pricetest").replace("Price per day: ", "").replace("per day", "").strip() # Get the price per day from the label and clean the string
    seats = app.getLabel("seatstest") # Get the number of seats from the label
    luggage = app.getLabel("luggagetest") # Get the luggage capacity from the label
    car_type = app.getLabel("categorytest") # Get the car category from the label

    total_duration = f"{total_duration} Days" # Format the total duration as a string with "Days"
    total_price = int(total_price) # Convert the total price to an integer
    total_price = (f"£{total_price}") # Format the total price as a string with "£"

    pickup_date = app.getOptionBox("pickup_date") # Get the selected pickup date
    pickup_time = app.getOptionBox("pickup_time") # Get the selected pickup time
    dropoff_date = app.getOptionBox("dropoff_date") # Get the selected drop-off date
    dropoff_time = app.getOptionBox("dropoff_time") # Get the selected drop-off time

    print(car_name, price_per_day, seats, luggage, car_type, total_duration, total_price, pickup_date, pickup_time, dropoff_date, dropoff_time)

    cur.execute("SELECT vehicleID FROM tbl_vehicles WHERE vehicleName = ?", (car_name,)) # Query the database to find the vehicleID associated with the car name
    vehicleID = cur.fetchone()[0] # Extract the vehicleID from the query result

    booking_ref = "#" + str(random.randint(1000, 9999)) # Generate a random booking reference number

    cur.execute("""
        INSERT INTO tbl_bookings (userID, bookingRef, bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalDuration)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (userID, booking_ref, pickup_date, dropoff_date, pickup_time, dropoff_time, total_duration)) # Insert booking details into the bookings table
    con.commit() # Commit the transaction to the database

    booking_id = cur.lastrowid # Get the ID of the last inserted booking

    cur.execute("""
        INSERT INTO tbl_bookingDetails (bookingID, vehicleID, pricePerDay, totalCost)
        VALUES (?, ?, ?, ?)
    """, (booking_id, vehicleID, price_per_day, total_price)) # Insert booking details into the bookingDetails table
    con.commit() # Commit the transaction to the database

    cur.execute("""
        UPDATE tbl_vehicles
        SET Stock = Stock - 1
        WHERE vehicleID = ?
    """, (vehicleID,)) # Update the stock of the vehicle by reducing it by 1
    con.commit() # Commit the transaction to the database

    # Show a confirmation message with the booking reference
    app.infoBox("Booking Confirmed", f"Your booking reference is: {booking_ref}\nA confirmation email has been sent to your registered email address for all information.")

#####################################################################################################################################################
#####################################################################################################################################################

def sendBookingSummary_Email(): # Define the function to send a booking summary email
    global booking_ref, total_price, total_duration # Declare global variables for booking reference, total price, and duration

    sender_email = "electriccarrentalservices@gmail.com" # Set the sender"s email address
    user_email = app.getEntry("Login Email").strip() # Get the user"s email from the login entry and remove any extra spaces

    cur.execute("SELECT userID, firstname, lastname FROM tbl_users WHERE userEmail = ?", (user_email,)) # Query the database to find the user"s details
    result = cur.fetchone() # Fetch the result of the query

    if result: # Check if the user exists in the database
        userID, firstname, lastname = result # Extract the user"s ID, first name, and last name
        name = firstname + " " + lastname # Combine the first and last name into a full name

        car_name = app.getLabel("cartest") # Get the car name from the label
        price_per_day = app.getLabel("pricetest").replace("Price per day: ", "").strip() # Get the price per day from the label and clean the string

        total_duration = f"{total_duration} Days" # Format the total duration as a string with "Days"
        total_price = (f"{total_price}") # Format the total price as a string

        pickup_date = app.getOptionBox("pickup_date") # Get the selected pickup date
        pickup_time = app.getOptionBox("pickup_time") # Get the selected pickup time
        dropoff_date = app.getOptionBox("dropoff_date") # Get the selected drop-off date
        dropoff_time = app.getOptionBox("dropoff_time") # Get the selected drop-off time

        subject = "Your Electric Car Rental Booking Summary" # Set the subject of the email

        message = ( # Compose the email message
            f"Dear {name},\n\n"
            f"Thank you for choosing Electric Car Rental Services! Your booking has been confirmed.\n\n"
            f"Booking Reference: {booking_ref}\n"
            f"Car Model: {car_name}\n"
            f"Pickup Date & Time: {pickup_date} at {pickup_time}\n"
            f"Drop-off Date & Time: {dropoff_date} at {dropoff_time}\n"
            f"Total Price: {total_price}\n\n"
            "**Important Rental Terms & Instructions:**\n"
            "1. **Pickup & Drop-off Location:** Please arrive at our rental office located at 123 Electric Avenue, Green City, EC1 1EV for both pickup and drop-off.\n"
            "2. **Identification:** You must bring a valid government-issued ID (e.g., passport or driving licence) and the payment card used for booking.\n"
            "3. **Payment:** Payment will be finalised in person at the rental office. Please ensure you have the necessary funds available.\n"
            "4. **Late Returns:** If you return the car later than the agreed drop-off time, additional charges will apply (£20 per hour).\n"
            "5. **Damages:** You are responsible for any damages to the vehicle during the rental period. Charges will be applied based on the extent of the damage.\n"
            "6. **Fuel Policy:** The car will be provided with a full tank of fuel. Please return it with a full tank to avoid refuelling charges.\n"
            "7. **Mileage Limit:** Your rental includes a mileage limit of 200 miles per day. Additional miles will be charged at £0.25 per mile.\n\n"
            "**Contact Us:**\n"
            "If you have any questions or need assistance, please contact us at +44 7723 195086 or email us at electriccarrentalservices@gmail.com.\n\n"
            "We look forward to serving you and wish you a pleasant journey!\n\n"
            "Kind regards,\n"
            "Electric Car Rental Team\n"
        )
        msg = f"Subject: {subject}\n\n{message}".encode("utf-8") # Format the email subject and message


        server = smtplib.SMTP("smtp.gmail.com", 587) # Connect to the Gmail SMTP server
        server.starttls() # Start TLS encryption for secure communication
        server.login(sender_email, "lqizscsznanuinny") # Log in to the sender"s email account
        server.sendmail(sender_email, user_email, msg) # Send the email to the user
        server.quit() # Close the connection to the SMTP server

#####################################################################################################################################################
#####################################################################################################################################################

def amendBookingDetails_Database():
    booking_ref = app.getLabel("bookingRef_Label_amendSummary").replace("BookingRef:", "").strip()  # Retrieve and clean the booking reference from the label

    new_pickup_date = app.getEntry("Pickup_Date_Entry_amendSummary").replace("Date: ", "").strip()  # Retrieve and clean the new pickup date from the entry widget
    new_pickup_time = app.getEntry("Pickup_Time_Entry_amendSummary").replace("Time: ", "").strip()  # Retrieve and clean the new pickup time from the entry widget
    new_dropoff_date = app.getEntry("Dropoff_Date_Entry_amendSummary").replace("Date: ", "").strip()  # Retrieve and clean the new drop-off date from the entry widget
    new_dropoff_time = app.getEntry("Dropoff_Time_Entry_amendSummary").replace("Time: ", "").strip()  # Retrieve and clean the new drop-off time from the entry widget
    total_duration = app.getEntry("Total_Duration_Entry_amendSummary").replace("Total Days: ", "").strip()  # Retrieve and clean the total duration from the entry widget
    total_price = app.getEntry("Total_Price_Entry_amendSummary").replace("Total Cost: £", "£").strip()  # Retrieve and clean the total price from the entry widget

    print(booking_ref, new_pickup_time, new_dropoff_date, new_dropoff_time, total_duration, total_price)

    cur.execute("SELECT bookingID FROM tbl_bookings WHERE bookingRef = ?", (booking_ref,))  # Query the database to check if the booking reference exists
    booking_exists = cur.fetchone()  # Fetch the result of the query

    if not booking_exists:  # Check if the booking reference does not exist in the database
        app.errorBox("Error", f"Booking reference {booking_ref} not found in the database.")  # Show an error message if the booking reference is not found
        return  # Exit the function if the booking reference is invalid

    cur.execute("""
        UPDATE tbl_bookings
        SET bookingPickupDate = ?, bookingDropoffDate = ?, bookingPickUpTime = ?, bookingDropoffTime = ?, totalDuration = ?
        WHERE bookingRef = ?
    """, (new_pickup_date, new_dropoff_date, new_pickup_time, new_dropoff_time, total_duration, booking_ref))  # Update the booking details in the database
    con.commit()  # Commit the amended details to the database (times)

    cur.execute("""
        UPDATE tbl_bookingDetails
        SET totalCost = ?
        WHERE bookingID = (SELECT bookingID FROM tbl_bookings WHERE bookingRef = ?)
    """, (total_price, booking_ref))  # Update the total cost in the booking details table
    con.commit()   # Commit the amended details to the database (price)

    # Show a success message confirming the booking update
    app.infoBox("Booking Amended", f"Your booking {booking_ref} has been updated successfully.\n"
                                   f"A confirmation email has been sent to your registered email address for all information.")

#####################################################################################################################################################
#####################################################################################################################################################

def sendAmendBookingSummary_Email():
    booking_ref = app.getLabel("bookingRef_Label_amendSummary").strip()  # Retrieve and clean the booking reference from the label

    user_email = app.getEntry("Login Email").strip()  # Retrieve and clean the user"s email from the entry widget
    cur.execute("SELECT firstname, lastname FROM tbl_users WHERE userEmail = ?", (user_email,))  # Query the database to fetch the user"s first and last name
    result = cur.fetchone()  # Fetch the result of the query
    if result:  # Check if the user"s details were found in the database
        firstname, lastname = result  # Unpack the first and last name from the result
        name = f"{firstname} {lastname}"  # Combine the first and last name into a full name

    car_name = app.getEntry("Car_Name_Entry_amendSummary").replace("Car: ", "").strip()  # Retrieve and clean the car name from the entry widget
    price_per_day = app.getEntry("Price_Per_Day_Entry_amendSummary").replace("Price Per Day: £", "").strip()  # Retrieve and clean the price per day from the entry widget
    total_price = app.getEntry("Total_Price_Entry_amendSummary").replace("Total Price: £", "").strip()  # Retrieve and clean the total price from the entry widget
    pickup_date = app.getEntry("Pickup_Date_Entry_amendSummary").replace("Date: ", "").strip()  # Retrieve and clean the pickup date from the entry widget
    pickup_time = app.getEntry("Pickup_Time_Entry_amendSummary").replace("Time: ", "").strip()  # Retrieve and clean the pickup time from the entry widget
    dropoff_date = app.getEntry("Dropoff_Date_Entry_amendSummary").replace("Date: ", "").strip()  # Retrieve and clean the drop-off date from the entry widget
    dropoff_time = app.getEntry("Dropoff_Time_Entry_amendSummary").replace("Time: ", "").strip()  # Retrieve and clean the drop-off time from the entry widget
    total_duration = app.getEntry("Total_Duration_Entry_amendSummary")  # Retrieve the total duration from the entry widget

    sender_email = "electriccarrentalservices@gmail.com"  # Set the sender"s email address
    subject = "Your Amended Electric Car Rental Booking Summary"  # Set the email subject

    message = (  # Compose the email message
        f"Dear {name},\n\n"
        f"Your booking with Electric Car Rental Services has been successfully amended.\n\n"
        f"{booking_ref}\n"
        f"Car Model: {car_name}\n"
        f"Pickup Date & Time: {pickup_date} at {pickup_time}\n"
        f"Drop-off Date & Time: {dropoff_date} at {dropoff_time}\n"
        f"{total_duration}\n"
        f"{total_price}\n\n"
        "**Important Rental Terms & Instructions:**\n"
        "1. **Pickup & Drop-off Location:** Please arrive at our rental office located at 123 Electric Avenue, Green City, EC1 1EV for both pickup and drop-off.\n"
        "2. **Identification:** You must bring a valid government-issued ID (e.g., passport or driving licence) and the payment card used for booking.\n"
        "3. **Payment:** Payment will be finalised in person at the rental office. Please ensure you have the necessary funds available.\n"
        "4. **Late Returns:** If you return the car later than the agreed drop-off time, additional charges will apply (£20 per hour).\n"
        "5. **Damages:** You are responsible for any damages to the vehicle during the rental period. Charges will be applied based on the extent of the damage.\n"
        "6. **Fuel Policy:** The car will be provided with a full tank of fuel. Please return it with a full tank to avoid refuelling charges.\n"
        "7. **Mileage Limit:** Your rental includes a mileage limit of 200 miles per day. Additional miles will be charged at £0.25 per mile.\n\n"
        "**Contact Us:**\n"
        "If you have any questions or need assistance, please contact us at +44 7723 195086 or email us at electriccarrentalservices@gmail.com.\n\n"
        "We look forward to serving you and wish you a pleasant journey!\n\n"
        "Kind regards,\n"
        "Electric Car Rental Team\n"
    )
    msg = f"Subject: {subject}\n\n{message}".encode("utf-8")  # Format the email subject and message

    server = smtplib.SMTP("smtp.gmail.com", 587)  # Connect to the SMTP server
    server.starttls()  # Start TLS encryption for secure communication
    server.login(sender_email, "lqizscsznanuinny")  # Log in to the sender"s email account
    server.sendmail(sender_email, user_email, msg)  # Send the email to the user
    server.quit()  # Disconnect from the SMTP server

#####################################################################################################################################################
#####################################################################################################################################################

def cancelBooking(): # Define the function to cancel a booking
    booking_ref = app.getEntry("CancelBooking_Ref").strip() # Get the booking reference from the entry widget and remove any extra spaces
    cancellation_reason = app.getOptionBox("cancelBooking_optionbox") # Get the selected reason for cancellation from the option box

    if not booking_ref or booking_ref == "Enter Booking Ref": # Check if the booking reference is empty or the default placeholder text
        app.infoBox("Error", "Please enter a valid booking reference.") # Show an error message if no booking reference is provided
        return

    if not cancellation_reason or cancellation_reason == "- Select a reason for cancellation -": # Check if no cancellation reason is selected
        app.infoBox("Error", "Please select a reason for cancellation.") # Show an error message if no cancellation reason is selected
        return

    user_email = app.getEntry("Login Email").strip() # Get the user"s email from the login entry and remove any extra spaces

    current_datetime = datetime.now() # Get the current date and time

    cur.execute("""
        SELECT b.bookingID, b.userID, b.bookingDropoffDate, b.bookingDropoffTime
        FROM tbl_bookings b
        WHERE b.bookingRef = ?
    """, (booking_ref,)) # Query the database to find the booking details using the booking reference

    booking_result = cur.fetchone() # Fetch the result of the query

    if not booking_result: # Check if no booking was found with the provided reference
        app.infoBox("Error", "Booking reference not found.") # Show an error message if the booking reference is invalid
        return

    booking_id, user_id, booking_dropoff_date, booking_dropoff_time = booking_result # Extract booking details from the query result

    dropoff_datetime_str = f"{booking_dropoff_date} {booking_dropoff_time}" # Combine the drop-off date and time into a single string
    dropoff_datetime = datetime.strptime(dropoff_datetime_str, "%d %b %Y %H:%M") # Convert the drop-off date and time into a datetime object

    if dropoff_datetime <= current_datetime: # Check if the drop-off date and time are in the past
        app.infoBox("Error", "You can only cancel future bookings.") # Show an error message if the booking is not in the future
        return

    cur.execute("SELECT userID FROM tbl_users WHERE userEmail = ?", (user_email,)) # Query the database to find the userID associated with the email
    user_result = cur.fetchone() # Fetch the result of the query

    if not user_result or user_result[0] != user_id: # Check if the user is not found or does not match the booking"s user
        app.infoBox("Error", "You can only cancel your own bookings.") # Show an error message if the user is not authorised to cancel the booking
        return

    cancelConfirm = app.questionBox("Cancel", "Are you sure you want to cancel this booking?") # Ask the user to confirm the cancellation

    if cancelConfirm: # If the user confirms the cancellation
        cur.execute("DELETE FROM tbl_bookingDetails WHERE bookingID = ?", (booking_id,)) # Delete the booking details from the database
        cur.execute("DELETE FROM tbl_bookings WHERE bookingID = ?", (booking_id,)) # Delete the booking from the database
        con.commit() # Commit the transaction to the database

        app.infoBox("Success", "Booking cancelled successfully.") # Show a success message

        print(cancelConfirm)
        print(booking_id)

        app.clearEntry("CancelBooking_Ref") # Clear the booking reference entry widget
        app.setOptionBox("cancelBooking_optionbox", "- Select a reason for cancellation -", override=True) # Reset the cancellation reason option box

#####################################################################################################################################################
#####################################################################################################################################################

def btnPress(btnName):  # Function to handle button presses
    if btnName == "btnLogin":  # Check if the pressed button is "Login"
        app.hide()  # Hide the current window
        app.showSubWindow("win_Login")  # Show the login sub window

    elif btnName == "btnSignup":  # Check if the pressed button is "SIGN UP"
        app.hide()  # Hide the current window
        app.showSubWindow("win_Signup")  # Show the sign up sub window

    elif btnName == "btnForgotPassword": # Check if the pressed button is "Forgot Password"
        app.hideSubWindow("win_Login") # Hides the login window
        app.showSubWindow("win_ForgotPassword1") # Shows the first forgot password window

    elif btnName == "btnForgotPasswordNext1":  # Check if the "Next" button was pressed on the Forgot Password screen
        sendEmail() # Calls the function to send an email
        #app.hideSubWindow("win_ForgotPassword1")  # Hides the first Forgot Password window
        #app.showSubWindow("win_ForgotPassword2")  # Shows the second Forgot Password window

    elif btnName == "btnForgotPasswordNext2": # Check if the "Next" button was pressed on the second Forgot Password screen
        validateCode() # Calls the validate code function
        #app.hideSubWindow("win_ForgotPassword2") # Hides the second Forgot Password window
        #app.showSubWindow("win_ForgotPassword3") # Shows the third Forgot Password window

    elif btnName == "btnForgotPasswordNext3": # Check if the "Next" button was pressed on the third Forgot Password screen
        passwordChange()
        #app.hideSubWindow("win_ForgotPassword3") # Hides the third Forgot Password screen
        #app.showSubWindow("win_Login") # Shows the login screen

    elif btnName == "btnForgotPasswordBack1":  # Check if the "Back" button was pressed on the Forgot Password screen
        app.hideSubWindow("win_ForgotPassword1")  # Hides the Forgot Password window
        app.showSubWindow("win_Login")  # Shows the login window

    elif btnName == "btnForgotPasswordBack2": # Check if the "Back" button was pressed on the second Forgot Password screen
        app.hideSubWindow("win_ForgotPassword2") # Hides the second Forgot Password window
        app.showSubWindow("win_ForgotPassword1") # Shows the first Forgot Password window

    elif btnName == "btnForgotPasswordBack3": # Check if the "Back" button was pressed on the second Forgot Password screen
        app.hideSubWindow("win_ForgotPassword3") # Hides the third Forgot Password window
        app.showSubWindow("win_ForgotPassword2") # Shows the second Forgot Password window

    elif btnName == "btnMenuFromLogin": # Check if the "SIGN IN" button was pressed
        validateLogin() # Calls the validate login function
        #app.hideSubWindow("win_Login") # Hides the login window
        #app.showSubWindow("win_Menu") # Shows the menu page window

    elif btnName == "btnMenuFromSignup":  # Check if the "SIGN UP" button was pressed
        validateSignup() # Calls the signup login function
        #app.hideSubWindow("win_Signup")  # Hides the signup window
        #app.showSubWindow("win_Login")  # Shows the menu page window

    elif btnName == "btnBooking":  # Check if the button pressed is the "BOOK NOW" button
        app.hideSubWindow("win_Menu")  # Hide the menu sub-window to transition to the booking process
        app.showSubWindow("win_Booking1")  # Show the first sub-window for the booking process

    elif btnName == "btnBookingBack1":  # Check if the button pressed is the "Back" button on Booking Page 1
        app.hideSubWindow("win_Booking1")  # Hide the Booking Page 1 sub-window to return to the previous menu
        app.showSubWindow("win_Menu")  # Show the main menu sub-window

    elif btnName == "btnBookingNext1":  # Check if the button pressed is the "SEARCH" button on Booking Page 1
        global matching_result_global, increment_bookingpage# Declare that you are using the global variable
        matching_result = getBooking()  # Retrieve the list of cars matching the selected criteria
        #print(matching_result)  # Print the matching cars to the console for debugging and testing purposes
        if not matching_result:  # Check if no cars match the selected criteria
            app.warningBox("No Matches","No cars match your criteria. Please adjust your filters.")  # Display a warning if no matches are found
        else:
            matching_result_global = matching_result  # Store the result in the global variable
            app.hideSubWindow("win_Booking1") # Hide the Booking Page 1 sub-window to transition to the next booking page
            populateCars() # Runs the sub-routine which creates the second booking page
            app.showSubWindow(f"win_BookingPage{increment_bookingpage}") # Show Booking Page 2 sub-window for further booking options
            increment_bookingpage += 1 # Increments the booking page counter

    elif btnName == "btnBookingBack2":  # Check if the button pressed is the "Back" button on Booking Page 2
        app.hideSubWindow(f"win_BookingPage{increment_bookingpage - 1}")  # Hide the Booking Page 2 sub-window to go back
        app.showSubWindow("win_Booking1")  # Show the Booking Page 1 sub-window

        global increment_favourites, navigation_source  # Declare global variables for tracking the favourites page and navigation source
    elif btnName.startswith("btn_") and btnName.endswith(f"_select{increment_favourites - 1}"):  # Check if the button pressed is a "SELECT" button from the favourites page
        navigation_source = "favourites"  # Set the navigation source to "favourites" to track where the user came from

        car = btnName[4:-7 - len(str(increment_favourites))]  # Extract the car name from the button name

        car_name = app.getLabel(f"lb_{car}_name_favourites")  # Get the car name from the corresponding label
        car_type = app.getLabel(f"lb_{car}_type_favourites").replace("Category: ","")  # Get the car type and remove the "Category: " prefix
        car_seats = app.getLabel(f"lb_{car}_seats_favourites").replace("Seats: ","")  # Get the number of seats and remove the "Seats: " prefix
        car_luggage = app.getLabel(f"lb_{car}_luggage_favourites").replace("Luggage: ","")  # Get the luggage capacity and remove the "Luggage: " prefix
        car_price = app.getLabel(f"lb_{car}_price_favourites").split("\n")[0].strip()  # Get the price per day and remove the "Price per Day: " prefix
        app.setImage("carbooking3", f"{Image_Of_Car(car_name)}.gif")

        app.setLabel("cartest", car_name)  # Set the car name in the booking page label
        app.setLabel("pricetest", f"{car_price}\nper day")  # Set the price per day in the booking page label
        app.setLabel("categorytest", f"{car_type}")  # Set the car category in the booking page label
        app.setLabel("seatstest", f"{car_seats}")  # Set the number of seats in the booking page label
        app.setLabel("luggagetest", f"{car_luggage}")  # Set the luggage capacity in the booking page label

        app.hideSubWindow(f"win_Favourites{increment_favourites - 1}")  # Hide the favourites sub-window
        app.showSubWindow("win_Booking3")  # Show the booking page sub-window

    elif btnName.startswith("btn_") and btnName.endswith("_select"):  # Check if the button pressed is a "SELECT" button for a car
        navigation_source = "booking"  # Set the navigation source to "booking" to track where the user came from

        car = btnName[4:-7]  # Extract the car name from the button name
        global cars # Access the global "cars" dictionary containing car details

        selected_car_specs = cars.get(car, {})  # Retrieve the selected car"s details from the `cars` dictionary
        category = selected_car_specs.get("category", "")  # Get the car category from the dictionary
        price_per_day = selected_car_specs.get("price_per_day", "")  # Get the price per day from the dictionary
        seats = selected_car_specs.get("seats", "")  # Get the number of seats from the dictionary
        luggage = selected_car_specs.get("luggage", "")  # Get the luggage capacity from the dictionary

        app.setLabel("cartest", car)  # Set the car name in the booking page label
        app.setLabel("pricetest", f"{price_per_day}\nper day")  # Set the price per day in the booking page label
        app.setLabel("categorytest", f"{category}")  # Set the car category in the booking page label
        app.setLabel("seatstest", f"{seats}")  # Set the number of seats in the booking page label
        app.setLabel("luggagetest", f"{luggage}")  # Set the luggage capacity in the booking page label
        app.setImage("carbooking3", f"{Image_Of_Car(car)}.gif")

        app.hideSubWindow(f"win_BookingPage{increment_bookingpage - 1}")  # Hide the previous booking page sub-window
        app.showSubWindow("win_Booking3")  # Show the Booking Page 3 sub-window
        
    elif btnName == "btnBookAgain":  # Check if the "BOOK AGAIN" button is pressed
        navigation_source = "pastbooking"  # Set the navigation source to "pastbooking" to track where the user came from

        car_name_pastbooking = app.getEntry("Car_Name_Entry_pastbooking")  # Get the car name from the entry widget
        car_price_pastbooking = app.getEntry("Price_Per_Day_Entry_pastbooking").replace("Price Per Day: ", "")  # Get the price per day and remove the prefix
        car_seats_pastbooking = app.getEntry("Seats_Entry_pastbooking").replace("Seats: ","")  # Get the number of seats and remove the prefix
        car_luggage_pastbooking = app.getEntry("Luggage_Entry_pastbooking").replace("Luggage: ","")  # Get the luggage capacity and remove the prefix
        car_type_pastbooking = app.getEntry("Car_Type_Entry_pastbooking").replace("Car Type: ","")  # Get the car type and remove the prefix
        app.setImage("carbooking3", f"{Image_Of_Car(car_name_pastbooking)}.gif")

        app.setLabel("cartest", car_name_pastbooking)  # Set the car name in the booking page label
        app.setLabel("pricetest", f"{car_price_pastbooking} per day")  # Set the price per day in the booking page label
        app.setLabel("categorytest", f"{car_type_pastbooking}")  # Set the car category in the booking page label
        app.setLabel("seatstest", f"{car_seats_pastbooking}")  # Set the number of seats in the booking page label
        app.setLabel("luggagetest", f"{car_luggage_pastbooking}")  # Set the luggage capacity in the booking page label

        app.hideSubWindow(f"win_PastBookingsView")  # Hide the past bookings view sub-window
        app.showSubWindow("win_Booking3")  # Show the booking page sub-window

        global increment_pastbookings, increment_futurebookings
    elif btnName.startswith("btn_") and btnName.endswith("_view"):  # Check if the button pressed is a "VIEW" button for a booking
        bookingRef = btnName[4:-5]  # Extract the booking reference from the button name

        cur.execute("""
                        SELECT b.bookingRef, v.vehicleName, v.vehicleType, v.seatingCapacity, v.luggageCapacity, bd.pricePerDay,
                               b.bookingPickupDate, b.bookingDropoffDate, b.bookingPickUpTime, b.bookingDropoffTime, bd.totalCost, b.totalDuration
                        FROM tbl_bookings b
                        JOIN tbl_bookingDetails bd ON b.bookingID = bd.bookingID
                        JOIN tbl_vehicles v ON bd.vehicleID = v.vehicleID
                        WHERE b.bookingRef = ?
                    """, (bookingRef,))  # Query the database to retrieve details of the selected booking
        booking_details = cur.fetchone()  # Fetch the result of the query

        if booking_details:  # Check if booking details were found
            bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, \
                bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost, totalDuration = booking_details  # Extract booking details

            app.setEntry("Car_Name_Entry_pastbooking", f"{vehicleName}")  # Set the car name in the entry widget
            app.setEntry("Price_Per_Day_Entry_pastbooking",f"Price Per Day: {pricePerDay}") # Set the price per day in the entry widget
            app.setEntry("Seats_Entry_pastbooking",f"Seats: {seatingCapacity}")  # Set the number of seats in the entry widget
            app.setEntry("Luggage_Entry_pastbooking",f"Luggage: {luggageCapacity}")  # Set the luggage capacity in the entry widget
            app.setEntry("Car_Type_Entry_pastbooking",f"Car Type: {vehicleType}")  # Set the car type in the entry widget
            app.setEntry("Pickup_Date_Entry_pastbooking",f"Pickup Date: {bookingPickupDate}")  # Set the pickup date in the entry widget
            app.setEntry("Dropoff_Date_Entry_pastbooking",f"Dropoff Date: {bookingDropoffDate}")  # Set the drop-off date in the entry widget
            app.setEntry("Pickup_Time_Entry_pastbooking",f"Pickup Time: {bookingPickUpTime}")  # Set the pickup time in the entry widget
            app.setEntry("Dropoff_Time_Entry_pastbooking",f"Dropoff Time: {bookingDropoffTime}")  # Set the drop-off time in the entry widget
            app.setEntry("Total_Cost_Entry_pastbooking",f"Total Cost: {totalCost}")  # Set the total cost in the entry widget
            app.setEntry("Total_Duration_Entry_pastbooking",f"Total Days: {totalDuration}")  # Set the total duration in the entry widget
            app.setLabel("bookingRef_Label_pastbooking",f"BookingRef: {bookingRef}")  # Set the booking reference in the label

            app.hideSubWindow(f"win_PastBookings{increment_pastbookings - 1}")  # Hide the past bookings sub-window
            app.showSubWindow("win_PastBookingsView")  # Show the past bookings view sub-window

    elif btnName.startswith("btn_") and btnName.endswith("_view_future"):  # Check if the button pressed is a "VIEW" button for a future booking
        bookingRef = btnName[4:-12]  # Extract the booking reference from the button name

        cur.execute("""  
                SELECT b.bookingRef, v.vehicleName, v.vehicleType, v.seatingCapacity, v.luggageCapacity, bd.pricePerDay,
                       b.bookingPickupDate, b.bookingDropoffDate, b.bookingPickUpTime, b.bookingDropoffTime, bd.totalCost, b.totalDuration
                FROM tbl_bookings b
                JOIN tbl_bookingDetails bd ON b.bookingID = bd.bookingID
                JOIN tbl_vehicles v ON bd.vehicleID = v.vehicleID
                WHERE b.bookingRef = ?
            """, (bookingRef,))  # Query the database to retrieve details of the selected booking

        booking_details = cur.fetchone()  # Fetch the result of the query
        if booking_details:  # Check if booking details were found
            bookingRef, vehicleName, vehicleType, seatingCapacity, luggageCapacity, pricePerDay, \
                bookingPickupDate, bookingDropoffDate, bookingPickUpTime, bookingDropoffTime, totalCost, totalDuration = booking_details  # Extract booking details

        app.setEntry("Car_Name_Entry_futurebooking", f"{vehicleName}")  # Set the car name in the entry widget
        app.setEntry("Price_Per_Day_Entry_futurebooking",f"Price Per Day: {pricePerDay}")  # Set the price per day in the entry widget
        app.setEntry("Seats_Entry_futurebooking",f"Seats: {seatingCapacity}")  # Set the number of seats in the entry widget
        app.setEntry("Luggage_Entry_futurebooking",f"Luggage: {luggageCapacity}")  # Set the luggage capacity in the entry widget
        app.setEntry("Car_Type_Entry_futurebooking", f"Car Type: {vehicleType}")  # Set the car type in the entry widget
        app.setEntry("Pickup_Date_Entry_futurebooking",f"Pickup Date: {bookingPickupDate}")  # Set the pickup date in the entry widget
        app.setEntry("Dropoff_Date_Entry_futurebooking",f"Dropoff Date: {bookingDropoffDate}")  # Set the drop-off date in the entry widget
        app.setEntry("Pickup_Time_Entry_futurebooking",f"Pickup Time: {bookingPickUpTime}")  # Set the pickup time in the entry widget
        app.setEntry("Dropoff_Time_Entry_futurebooking",f"Dropoff Time: {bookingDropoffTime}")  # Set the drop-off time in the entry widget
        app.setEntry("Total_Cost_Entry_futurebooking",f"Total Cost: {totalCost}")  # Set the total cost in the entry widget
        app.setEntry("Total_Duration_Entry_futurebooking",f"Total Days: {totalDuration}")  # Set the total duration in the entry widget

        app.setLabel("bookingRef_Label_futurebooking",f"BookingRef: {bookingRef}")  # Set the booking reference in the label

        app.hideSubWindow(f"win_FutureBookings{increment_futurebookings - 1}")  # Hide the future bookings sub-window
        app.showSubWindow("win_FutureBookingsView")  # Show the future bookings view sub-window

    elif btnName == "btnFutureBookingsViewBack":  # Check if the "Back" button for future bookings view is pressed
        app.hideSubWindow("win_FutureBookingsView")  # Hide the future bookings view sub-window
        app.showSubWindow(f"win_FutureBookings{increment_futurebookings - 1}")  # Show the previous future bookings sub-window

    elif btnName == "btnBookingBack3":  # Check if the "Back" button on Booking Page 3 is pressed
        if navigation_source == "favourites":  # Check if the user navigated to Booking Page 3 from the favourites page
            app.hideSubWindow("win_Booking3")  # Hide the Booking Page 3 sub-window
            app.showSubWindow(f"win_Favourites{increment_favourites - 1}")  # Show the previous favourites sub-window

        elif navigation_source == "pastbooking":  # Check if the user navigated to Booking Page 3 from the past bookings page
            app.hideSubWindow("win_Booking3")  # Hide the Booking Page 3 sub-window
            app.showSubWindow(f"win_PastBookings{increment_pastbookings - 1}")  # Show the previous past bookings sub-window

        else:  # If the user did not navigate from favourites or past bookings
            app.hideSubWindow("win_Booking3")  # Hide the Booking Page 3 sub-window
            app.showSubWindow(f"win_BookingPage{increment_bookingpage - 1}")  # Show the previous booking page sub-window

    elif btnName == "btnBookNow_bookingPage3":  # Check if the "BOOK NOW" button on Booking Page 3 is pressed
        global total_price, total_duration  # Declare global variables for total price and duration

        car_label = app.getLabel("cartest")  # Get the car name from the label
        price_label = app.getLabel("pricetest")  # Get the price per day from the label
        seats_label = app.getLabel("seatstest")  # Get the number of seats from the label
        luggage_label = app.getLabel("luggagetest")  # Get the luggage capacity from the label
        category_label = app.getLabel("categorytest")  # Get the car category from the label
        pickup_date = app.getOptionBox("pickup_date")  # Get the selected pickup date
        pickup_time = app.getOptionBox("pickup_time")  # Get the selected pickup time
        dropoff_date = app.getOptionBox("dropoff_date")  # Get the selected drop-off date
        dropoff_time = app.getOptionBox("dropoff_time")  # Get the selected drop-off time

        if pickup_date is None or pickup_time is None or dropoff_date is None or dropoff_time is None:  # Check if any date or time is not selected
            return app.infoBox("Error","Make sure that all date and time option boxes are selected.")  # Show an error message if any field is missing

        else:  # If all fields are selected
            pickup_datetime = datetime.strptime(f"{pickup_date} {pickup_time}","%d %b %Y %H:%M")  # Convert pickup date and time to a datetime object
            dropoff_datetime = datetime.strptime(f"{dropoff_date} {dropoff_time}","%d %b %Y %H:%M")  # Convert drop-off date and time to a datetime object

            if pickup_datetime.date() == dropoff_datetime.date():  # Check if pickup and drop-off are on the same day
                total_duration = 1  # Set total duration to 1 day

            else:  # If pickup and drop-off are on different days
                total_duration = (dropoff_datetime - pickup_datetime).days + 1  # Calculate total duration in days

            price_per_day = float(price_label.split("£")[1].split()[0]) # Extract the price per day from the label
            total_price = price_per_day * total_duration  # Calculate the total price

            app.setEntry("Car_Name_Entry", f"Car: {car_label}")  # Set the car name in the entry widget
            app.setEntry("Price_Per_Day_Entry",f"Price Per Day: £{price_per_day}")  # Set the price per day in the entry widget
            app.setEntry("Seats_Entry", f"Seats: {seats_label}")  # Set the number of seats in the entry widget
            app.setEntry("Luggage_Entry", f"Luggage: {luggage_label}")  # Set the luggage capacity in the entry widget
            app.setEntry("Car_Type_Entry", f"Category: {category_label}")  # Set the car category in the entry widget
            app.setEntry("Total_Price_Entry", f"Total Price: £{total_price}")  # Set the total price in the entry widget
            app.setEntry("Pickup_Date_Entry", f"Date: {pickup_date}")  # Set the pickup date in the entry widget
            app.setEntry("Pickup_Time_Entry", f"Time: {pickup_time}")  # Set the pickup time in the entry widget
            app.setEntry("Dropoff_Date_Entry", f"Date: {dropoff_date}")  # Set the drop-off date in the entry widget
            app.setEntry("Dropoff_Time_Entry", f"Time: {dropoff_time}")  # Set the drop-off time in the entry widget
            app.setEntry("Total_Duration_Entry",f"Total Duration: {total_duration} Days")  # Set the total duration in the entry widge

            app.hideSubWindow("win_Booking3")  # Hide the Booking Page 3 window
            app.showSubWindow("win_Booking4")  # Show the Booking Page 4 window

    elif btnName == "btnConfirm_bookingPage4":  # Check if the button pressed is the "Confirm" button on Booking Page 4
        bookingDetails_Database() # Call function that updates the details to the database
        sendBookingSummary_Email() # Sends a email with the summary of the booking
        app.hideSubWindow("win_Booking4")  # Hide the Booking Page 4 sub-window to go back
        app.showSubWindow("win_Menu")  # Show the menu page

    elif btnName == "btnBookingBack4":  # Check if the button pressed is the "Back" button on Booking Page 4
        app.hideSubWindow("win_Booking4")  # Hide the Booking Page 4 sub-window to go back
        app.showSubWindow("win_Booking3")  # Show the previous Booking Page 3

    elif btnName == "btnViewTrips":  # Check if the button pressed is the "VIEW TRIPS" button
        app.hideSubWindow("win_Menu")  # Hide the menu sub-window to transition to the trip viewing interface
        app.showSubWindow("win_ViewTrips")  # Show the sub-window for viewing trips

    elif btnName == "btnViewTripsBack":  # Check if the "Back" button in the View Trips page is pressed
        app.hideSubWindow("win_ViewTrips")  # Hide the View Trips sub-window to go back
        app.showSubWindow("win_Menu")  # Show the Menu sub-window to return to the main menu

    elif btnName == "btnLogout":  # Check if the button pressed is the "LOGOUT" button
        logoutAnswer = app.questionBox("LOGOUT","Do you want to log out?")  # Prompt the user with a confirmation box for logging out

        if logoutAnswer == True:  # If the user confirms they want to log out
            app.clearAllEntries()  # Clear all entry fields in the application
            app.clearAllRadioButtons()  # Clear all radio buttons in the application
            app.clearAllOptionBoxes()  # Clear all option boxes in the application
            app.clearAllCheckBoxes()  # Clear all checkboxes in the application

            # Define a list of entry fields and their default values to reset
            entries = [
                ("Login Email", "Email Address"),  # Reset Login Email field
                ("Login Password", "Password"),  # Reset Login Password field
                ("Signup FirstName", "First Name"),  # Reset Signup First Name field
                ("Signup LastName", "Last Name"),  # Reset Signup Last Name field
                ("Signup Email", "Email Address"),  # Reset Signup Email field
                ("Signup PhoneNum", "Phone Number"),  # Reset Signup Phone Number field
                ("Signup Password", "Password"),  # Reset Signup Password field
                ("Signup ReEnterPass", "Re-Enter Password"),  # Reset Signup Re-Enter Password field
                ("ForgotPassword Email", "Email Address"),  # Reset Forgot Password Email field
                ("ForgotPassword Code", "Code"),  # Reset Forgot Password Code field
                ("ForgotPassword_NewPass", "Password"),  # Reset New Password field
                ("ForgotPassword_ReEnterPass", "Re-Enter Password"),  # Reset Re-Enter Password field
                ("CancelBooking_Ref", "Enter Booking Ref"),  # Reset Cancel Booking Reference field
            ]
            # Loop through the entries and set their default values
            for entry, default_value in entries:
                app.setEntryDefault(entry, default_value)  # Set default value for each entry field

            app.hideSubWindow("win_Menu")  # Hide the menu sub-window after logging out
            app.show()  # Show the main application window or another relevant window

    elif btnName == "btnBackToHomeFromLogin": # Checks if the "Back" button on login was pressed
        app.hideSubWindow("win_Login") # Hides the login window
        app.show() # Shows original window (home page)

    elif btnName == "btnBackToHomeFromSignup":  # Check if the "Back" button on the signup page was pressed
        app.hideSubWindow("win_Signup")  # Hides the signup window
        app.show()  # Shows the main window (homepage)

    elif btnName == "btnFavourites":  # Check if the "Favourites" button is pressed
        populateFavourites()  # Call the function to populate the favourites page
        app.hideSubWindow("win_Menu")  # Hide the menu sub-window
        app.showSubWindow(f"win_Favourites{increment_favourites}")  # Show the favourites sub-window
        increment_favourites += 1  # Increment the favourites page counter

    elif btnName == "btnFavouritesBack":  # Check if the "Back" button on the favourites page is pressed
        app.hideSubWindow(f"win_Favourites{increment_favourites - 1}")  # Hide the current favourites sub-window
        app.showSubWindow("win_Menu")  # Show the menu sub-window

    elif btnName == "btnPastBookings":  # Check if the "Past Bookings" button is pressed
        populatePastBookings()  # Call the function to populate the past bookings page
        app.hideSubWindow("win_ViewTrips")  # Hide the "View Trips" sub-window
        app.showSubWindow(f"win_PastBookings{increment_pastbookings}")  # Show the past bookings sub-window
        increment_pastbookings += 1  # Increment the past bookings page counter

    elif btnName == "btnPastBookingsBack":  # Check if the "Back" button on the past bookings page is pressed
        app.hideSubWindow(f"win_PastBookings{increment_pastbookings - 1}")  # Hide the current past bookings sub-window
        app.showSubWindow("win_ViewTrips")  # Show the "View Trips" sub-window

    elif btnName == "btnPastBookingsViewBack":  # Check if the "Back" button on the past bookings view page is pressed
        app.hideSubWindow("win_PastBookingsView")  # Hide the past bookings view sub-window
        app.showSubWindow(f"win_PastBookings{increment_pastbookings - 1}")  # Show the previous past bookings sub-window

    elif btnName == "btnFutureBookings":  # Check if the "Future Bookings" button is pressed
        populateFutureBookings()  # Call the function to populate the future bookings page
        app.hideSubWindow("win_ViewTrips")  # Hide the "View Trips" sub-window
        app.showSubWindow(f"win_FutureBookings{increment_futurebookings}")  # Show the future bookings sub-window
        increment_futurebookings += 1  # Increment the future bookings page counter

    elif btnName == "btnFutureBookingsBack":  # Check if the "Back" button on the future bookings page is pressed
        app.hideSubWindow(f"win_FutureBookings{increment_futurebookings - 1}")  # Hide the current future bookings sub-window
        app.showSubWindow("win_ViewTrips")  # Show the "View Trips" sub-window

    elif btnName == "btnCancelBookings":  # Check if the "Cancel Bookings" button is pressed
        app.hideSubWindow("win_ViewTrips")  # Hide the View Trips sub-window
        app.showSubWindow("win_CancelBookings")  # Show the Cancel Bookings sub-window

    elif btnName == "btnCancelBookingsConfirm":  # Check if the "Confirm Cancellation" button is pressed
        cancelBooking()  # Call the cancel booking function to process the cancellation

    elif btnName == "btnCancelBookingsBack":  # Check if the "Back" button in Cancel Bookings page was pressed
        app.hideSubWindow("win_CancelBookings")  # Hide the "Cancel Bookings" sub-window
        app.showSubWindow("win_ViewTrips")  # Show the "View Trips" sub-window

    elif btnName == "btnContinueChanges":  # Check if the "CONTINUE CHANGES" button is pressed
        new_pickup_date = app.getOptionBox("new_pickup_date")  # Retrieve the new pickup date from the option box
        new_pickup_time = app.getOptionBox("new_pickup_time")  # Retrieve the new pickup time from the option box
        new_dropoff_date = app.getOptionBox("new_dropoff_date")  # Retrieve the new drop-off date from the option box
        new_dropoff_time = app.getOptionBox("new_dropoff_time")  # Retrieve the new drop-off time from the option box
        bookingRef = app.getLabel("bookingRef_Label_amendBooking")  # Retrieve the booking reference from the label
        total_duration = app.getEntry("Total_Duration_Entry_futurebooking")  # Retrieve the total duration from the entry widget

        car_name = app.getEntry("Car_Name_Entry_futurebooking")  # Retrieve the car name from the entry widget
        price_per_day = app.getEntry("Price_Per_Day_Entry_futurebooking")  # Retrieve the price per day from the entry widget
        seats = app.getEntry("Seats_Entry_futurebooking")  # Retrieve the number of seats from the entry widget
        luggage = app.getEntry("Luggage_Entry_futurebooking")  # Retrieve the luggage capacity from the entry widget
        car_type = app.getEntry("Car_Type_Entry_futurebooking")  # Retrieve the car type from the entry widget
        total_cost = app.getEntry("Total_Cost_Entry_futurebooking")  # Retrieve the total cost from the entry widget

        if new_pickup_date is None or new_pickup_time is None or new_dropoff_date is None or new_dropoff_time is None:  # Check if any date or time field is empty
            return app.infoBox("Error","Make sure that all date and time option boxes are selected.")  # Show an error message if any field is missing

        app.setEntry("Pickup_Date_Entry_amendSummary",f"Date: {new_pickup_date}")  # Set the new pickup date in the summary window
        app.setEntry("Pickup_Time_Entry_amendSummary",f"Time: {new_pickup_time}")  # Set the new pickup time in the summary window
        app.setEntry("Dropoff_Date_Entry_amendSummary",f"Date: {new_dropoff_date}")  # Set the new drop-off date in the summary window
        app.setEntry("Dropoff_Time_Entry_amendSummary",f"Time: {new_dropoff_time}")  # Set the new drop-off time in the summary window

        app.setLabel("bookingRef_Label_amendSummary", bookingRef)  # Set the booking reference in the summary window

        app.setEntry("Car_Name_Entry_amendSummary", car_name)  # Set the car name in the summary window
        app.setEntry("Price_Per_Day_Entry_amendSummary", price_per_day)  # Set the price per day in the summary window
        app.setEntry("Seats_Entry_amendSummary", seats)  # Set the number of seats in the summary window
        app.setEntry("Luggage_Entry_amendSummary", luggage)  # Set the luggage capacity in the summary window
        app.setEntry("Car_Type_Entry_amendSummary", car_type)  # Set the car type in the summary window
        app.setEntry("Total_Price_Entry_amendSummary", total_cost)  # Set the total cost in the summary window
        app.setEntry("Total_Duration_Entry_amendSummary",total_duration)  # Set the total duration in the summary window

        app.hideSubWindow("win_AmendBooking")  # Hide the "Amend Booking" sub-window
        app.showSubWindow("win_AmendSummary")  # Show the "Amend Summary" sub-window

    elif btnName == "btnConfirmAmend":  # Check if the "CONFIRM AMEND" button is pressed
        amendBookingDetails_Database()  # Call the function to update the booking details in the database
        sendAmendBookingSummary_Email()  # Call the function to send the amended booking summary email

        app.hideSubWindow("win_AmendSummary")  # Hide the "Amend Summary" sub-window
        app.showSubWindow("win_Menu")  # Show the main menu sub-window

    elif btnName == "btnAmendBooking":  # Check if the "AMEND BOOKING" button is pressed
        car_name = app.getEntry("Car_Name_Entry_futurebooking")  # Get the car name from the entry widget
        price_per_day = app.getEntry("Price_Per_Day_Entry_futurebooking")  # Get the price per day from the entry widget
        seats = app.getEntry("Seats_Entry_futurebooking")  # Get the number of seats from the entry widget
        luggage = app.getEntry("Luggage_Entry_futurebooking")  # Get the luggage capacity from the entry widget
        car_type = app.getEntry("Car_Type_Entry_futurebooking")  # Get the car type from the entry widget
        total_cost = app.getEntry("Total_Cost_Entry_futurebooking")  # Get the total cost from the entry widget
        pickup_date = app.getEntry("Pickup_Date_Entry_futurebooking")  # Get the pickup date from the entry widget
        pickup_time = app.getEntry("Pickup_Time_Entry_futurebooking")  # Get the pickup time from the entry widget
        dropoff_date = app.getEntry("Dropoff_Date_Entry_futurebooking")  # Get the drop-off date from the entry widget
        dropoff_time = app.getEntry("Dropoff_Time_Entry_futurebooking")  # Get the drop-off time from the entry widget
        total_duration = app.getEntry("Total_Duration_Entry_futurebooking")  # Get the total duration from the entry widget
        bookingRef = app.getLabel("bookingRef_Label_futurebooking")  # Get the booking reference from the label

        app.setEntry("Old_Pickup_Date_Entry", pickup_date)  # Set the old pickup date in the entry widge
        app.setEntry("Old_Pickup_Time_Entry", pickup_time)  # Set the old pickup time in the entry widget
        app.setEntry("Old_Dropoff_Date_Entry", dropoff_date)  # Set the old drop-off date in the entry widget
        app.setEntry("Old_Dropoff_Time_Entry", dropoff_time)  # Set the old drop-off time in the entry widget
        app.setEntry("Old_Total_Duration_Entry", total_duration)  # Set the old total duration in the entry widget
        app.setLabel("bookingRef_Label_amendBooking", bookingRef)  # Set the booking reference in the label

        app.hideSubWindow("win_FutureBookingsView")  # Hide the future bookings view sub-window
        app.showSubWindow("win_AmendBooking")  # Show the amend booking sub-window

    elif btnName == "btnAmendBookingBack":  # Check if the "Back" button on the amend booking page is pressed
        app.hideSubWindow("win_AmendBooking")  # Hide the amend booking sub-window
        app.showSubWindow("win_FutureBookingsView")  # Show the future bookings view sub-window

    elif btnName == "btnAmendSummaryBack":  # Check if the "Back" button on the amend summary page is pressed
        app.hideSubWindow("win_AmendSummary")  # Hide the amend summary sub-window
        app.showSubWindow("win_AmendBooking")  # Show the amend booking sub-window

#####################################################################################################################################################
#####################################################################################################################################################

createInterface() # Create the interface

sys.exit()
