# Project-X
### a Spirits2Go production  


## Project members
Koyuncu Helin, Messmer Aurelius, Shanmuganathan Teveen, Jason Jimenez  


## Overview

### joint tasks:  

register on GitHub

1.1. Als Gastnutzer möchte ich die verfügbaren Hotels durchsuchen, damit ich dasjenige auswählen kann, welches meinen Wünschen entspricht.

1.2. Als Gastnutzer möchte ich Details zu verschiedenen Zimmertypen (EZ, DZ, Familienzimmer), die in einem Hotel verfügbar sind, sehen, einschließlich der maximalen Anzahl von Gästen für dieses Zimmer, Beschreibung, Preis und Ausstattung, um eine fundierte Entscheidung zu treffen.



### Helin

role:  the bee "managing time"

user stories: 

1.2.2. Ich möchte nur die verfügbaren Zimmer sehen.

1.4. Als Gastnutzer möchte ich möglichst wenig Informationen über mich preisgeben, damit meine Daten privat bleiben.

1.6. Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können, um weitere Funktionalitäten nutzen zu können (z.B. Buchungshistorie, Buchungsänderung etc. [siehe 2.1].

3.1.2. Ich möchte Hotels aus dem System entfernen.

3.3. Ich möchte alle Buchungen bearbeiten können, um fehlende Informationen zu ergänzen (z.B. Telefonnummer) [Optional].

other tasks: 

writing the documentation



### Aurelius

role:  the wolve "keeping the pack together"

user stories: 

1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.

1.1.5. Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.

1.1.6. Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B. verfügbare Zimmer [siehe 1.2])

1.2.1. Ich möchte die folgenden Informationen pro Zimmer sehen: Zimmertyp, max. Anzahl der Gäste, Beschreibung, Ausstattung, Preis pro Nacht und Gesamtpreis.

other tasks:  

creating the GitHub repository, assigning the user stories



### Teveen

role:  the dolphin "comunicates with the outside world"

user stories:

1.1.2. Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.

1.1.3. Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.

1.3. Als Gastbenutzer möchte ich ein Zimmer in einem bestimmten Hotel buchen, um meinen Urlaub zu planen.

3.1.1. Ich möchte neue Hotels zum System hinzufügen.

3.2. Als Admin-Nutzer des Buchungssystems möchte ich alle Buchungen aller Hotels sehen können, um eine Übersicht zu erhalten.

other tasks:  

creating repository



### Jason

role:  the octopus "solving problems"

user stories:

1.1.4. Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes ("von" (start_date) und "bis" (end_date)) Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne, damit ich nur relevante Ergebnisse sehe.

1.5. Als Gastnutzer möchte ich die Details meiner Reservierung in einer lesbaren Form erhalten (z.B. die Reservierung in einer dauerhaften Datei speichern), damit ich meine Buchung später überprüfen kann.

2.1.1. Die Anwendungsfälle für meine Buchungen sind "neu/erstellen", "ändern/aktualisieren", "stornieren/löschen".

3.1.3. Ich möchte die Informationen bestimmter Hotels aktualisieren, z. B. den Namen, die Sterne usw.

3.4. Ich möchte in der Lage sein, die Zimmerverfügbarkeit zu verwalten und die Preise in Echtzeit im Backend-System der Anwendung zu aktualisieren [Optional].

other tasks:  

creating PyCharm environment




## Instruction

### Overview

The Booking Management Application is designed to facilitate hotel searches, reservations, and administrative management in a user-friendly Python environment. The application supports different user roles, each with specific functionalities tailored to their needs.


### Here is our Step-by-step Instructions on How to Use the Application:

### 1. Run the Application:

- Execute the console.app file. This file initializes and runs the main application, accessing other necessary files and executing their respective functions.
  
- It is important to run the application from its intended directory to avoid issues with relative file paths.

  
### 2. Main Menu Options:
   
Upon running the application, you will be presented with the Main Menu, offering the following options:

  #### 1.  Search Hotels:
   Opens the search menu where you can search for hotels based on various criteria.
   
  #### 2. Book a Room:
   Access the reservation menu to create, update, or delete room bookings.
   
  #### 3. Admin Management:
   Access administrative functions (available only to logged-in administrators).
   
  #### 4. Create User:
   Create a new user account with specified roles.
   
  #### 5. Log In/Out:
   Log in to access personalized and administrative features, or log out.
   
  #### 6. Quit:
   Exit the application.

   
### Guest User Functionalities

### 3. Search Hotels:

#### - Implementation Justification:
This functionality allows guest users to find hotels that match their preferences, addressing multiple user stories related to searching by location, star rating, number of guests, and availability.

#### - Steps:

  #### 1. By Name: Search hotels by their name.
  User Story Reference: 1.1.1
     
  #### 2. By Location: Search hotels based on their location.
  User Story Reference: 1.1.1

  #### 3. Availability by Date: Search for available rooms by specifying check-in and check-out      dates.
  Be sure to enter dates in the correct format (YYYY-MM-DD) and ensure that the check-out date is    after the check-in date to avoid errors.
  User Story Reference: 1.1.4

  #### 4. By Number of Guests: Search for rooms based on the number of guests.
  User Story Reference: 1.1.3

  #### 5. By Rating (Stars): Search for hotels based on their star rating.
  User Story Reference: 1.1.2
  
  #### 6. By Price: Search for hotels based on room price.
  User Story Reference: 1.1.6
  
  #### 7. Back to Main Menu: 
  Return to the Main Menu.

  
### 4. View Hotel Details:

#### - Implementation Justification: 
Users need to see detailed information about the hotels and rooms to make an informed decision. This includes room types, maximum guests, description, price, and amenities.
  
#### - Steps:

  1. Select a hotel to view details.
  2. See available room types, descriptions, and prices.
  #### User Story Reference: 1.2.1, 1.2.2

     
### 5. Book a Room:

#### - Implementation Justification:
Booking functionality allows users to make reservations for rooms. The application ensures that the booking process is straightforward and requires minimal user information for privacy.

#### - Steps:

  1. Enter hotel and room details.
  2. Specify booking dates and number of guests.
  Make sure the dates are entered correctly and follow the format (YYYY-MM-DD) to avoid errors.
  3. Confirm and save the booking.
  #### User Story Reference: 1.3, 1.4

     
### 6. Receive Booking Details:

#### - Implementation Justification:
Users can export their booking details to a file for future reference, ensuring they have a record of their reservations.

#### - Steps:

  1. After booking, choose to export details.
  2. Save the booking information to a text file.
  It is important to include timestamps in the exported file names or choose unique file names to    avoid overwriting previous files.
  #### User Story Reference: 1.5

     
### 7. Create an Account:

#### - Implementation Justification: 
Registration functionality allows users to create an account, enabling them to manage bookings and access additional features.

#### - Steps:
  1. Enter email and password to create an account.
  #### User Story Reference: 1.6

### Registered User Functionalities


### 8. Log In:

#### - Implementation Justification:
Logging in allows users to access personalized features such as viewing and managing their bookings.

#### - Steps:

  1. Enter username and password.
  It is important to regularly update your passwords and use strong, unique passwords for each       account to enhance security.
  #### User Story Reference: 2.1

     
### 9. Manage Bookings:

#### - Implementation Justification: 
Users can view, update, and delete their bookings, providing flexibility in managing their reservations.

#### - Steps:

  1. View booking history.
  2. Update or delete existing bookings.
  Be cautious when updating or deleting bookings to avoid accidental data loss.
  #### User Story Reference: 2.1.1

     
### Admin User Functionalities

### 10. Admin Management:

#### - Implementation Justification: 
Admin functionalities are essential for managing hotel information, room details, and bookings, ensuring the system remains up-to-date and accurate.

#### - Steps:
  1. Add New Hotel: Add a new hotel with details like name, stars, address, and rooms.
 #### User Story Reference: 3.1.1
  2. List All Hotels with Details: View a list of all hotels along with their room details and       bookings.
  #### User Story Reference: 3.2
  3. Find Hotel by Name: Search for a specific hotel by name.
  #### User Story Reference: 3.1
  4. Update Hotel Information: Update the details of an existing hotel.
  #### User Story Reference: 3.1.3
  5. Update Room Information: Update the details of rooms in a hotel.
  #### User Story Reference: 3.1
  6. Edit Bookings: View and edit existing bookings.
  Be sure to implement additional confirmation prompts and logging for critical admin actions to     avoid accidental data loss.
  #### User Story Reference: 3.3
  7. Back to Main Menu: Return to the Main Menu.




## Assumptions and interpretation

We analyzed the user stories and tried to implement them. We considered what we need to keep in mind, what needs to be changed or adapted, and what we can implement directly. We started a GitHub project and roughly outlined who is "serving" which user stories.

First, we created the Search Manager and implemented the first 5-6 user stories, including the following:

1.1. and its subchapters:
"Als Gastnutzer möchte ich die verfügbaren Hotels durchsuchen, damit ich dasjenige auswählen kann, welches meinen Wünschen entspricht."

We opened a Python file and tried to execute the applications we learned in class. We created our own database (list) of hotels (Ibis Hotel, Cozy Limon, Luxury Shan, Motel Serhan, Ling Ling's Palace, Case del Patron). We worked with lists that are modifiable, as opposed to tuples that are immutable.

We implemented search functions, e.g. search by preferred location, number of guests, number of stars, price, date. We set up these functions based on the Search Manager. This allowed us to learn how to implement the functions and develop an understanding of the individual components in Python. We dealt with classes, functions, lists, tuples, loops (while loops) and if statements etc.

We have included individual functions such as filter_hotels_by_location(location) and filter_hotels_by_guests(hotels, guests). We use .lower in our functions to make them case-insensitive for the user.

Then we looked at the structure of UE3_classroom. We considered how to navigate between the different Python files, how to retrieve and edit the database, and how to access functions in other files. We tried to fit our previously implemented user stories into this structure.

We programmed the user stories from GitHub and continuously made improvements. Based on coaching with Charuta, we set up the menu structure and implemented her input. We clarified our questions with her.
 
In general all the tasks assigned to us, where all separately done. If any questions occured or someone run into issues, we usually sat togheter, discussed and solved them as a group. 

Our role animals correspond to our functions within the group. Everyone was assigned different responsibilities during the project to keep everything on track. 

This is how we came to our current result and have continuously made improvements all around.
