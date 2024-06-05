# Project-X
## a Spirits2Go production  


## **Project members**
Koyuncu Helin, Messmer Aurelius, Shanmuganathan Teveen, Jason Jimenez  


## **Overview**

### joint tasks:  

register on GitHub

1.1. Als Gastnutzer möchte ich die verfügbaren Hotels durchsuchen, damit ich dasjenige auswählen kann, welches meinen Wünschen entspricht.

1.2. Als Gastnutzer möchte ich Details zu verschiedenen Zimmertypen (EZ, DZ, Familienzimmer), die in einem Hotel verfügbar sind, sehen, einschließlich der maximalen Anzahl von Gästen für dieses Zimmer, Beschreibung, Preis und Ausstattung, um eine fundierte Entscheidung zu treffen.



### **Helin**

user stories: 

1.2.2. Ich möchte nur die verfügbaren Zimmer sehen.

1.4. Als Gastnutzer möchte ich möglichst wenig Informationen über mich preisgeben, damit meine Daten privat bleiben.

1.6. Als Gastbenutzer möchte ich mich mit meiner E-Mail-Adresse und einer persönlichen Kennung (Passwort) registrieren können, um weitere Funktionalitäten nutzen zu können (z.B. Buchungshistorie, Buchungsänderung etc. [siehe 2.1].

3.1.2. Ich möchte Hotels aus dem System entfernen.

3.3. Ich möchte alle Buchungen bearbeiten können, um fehlende Informationen zu ergänzen (z.B. Telefonnummer) [Optional].

other tasks: 

writing the documentation

role:  the bee "managing time"



### **Aurelius**

user stories: 

1.1.1. Ich möchte alle Hotels in einer Stadt durchsuchen, damit ich das Hotel nach meinem bevorzugten Standort (Stadt) auswählen kann.

1.1.5. Ich möchte die folgenden Informationen pro Hotel sehen: Name, Adresse, Anzahl der Sterne.

1.1.6. Ich möchte ein Hotel auswählen, um die Details zu sehen (z.B. verfügbare Zimmer [siehe 1.2])

1.2.1. Ich möchte die folgenden Informationen pro Zimmer sehen: Zimmertyp, max. Anzahl der Gäste, Beschreibung, Ausstattung, Preis pro Nacht und Gesamtpreis.

other tasks:  

creating the GitHub repository, assigning the user stories

role:  the wolve "keeping the pack together"



### **Teveen**

user stories:

1.1.2. Ich möchte alle Hotels in einer Stadt nach der Anzahl der Sterne durchsuchen.

1.1.3. Ich möchte alle Hotels in einer Stadt durchsuchen, die Zimmer haben, die meiner Gästezahl entsprechen (nur 1 Zimmer pro Buchung), entweder mit oder ohne Anzahl der Sterne.

1.3. Als Gastbenutzer möchte ich ein Zimmer in einem bestimmten Hotel buchen, um meinen Urlaub zu planen.

3.1.1. Ich möchte neue Hotels zum System hinzufügen.

3.2. Als Admin-Nutzer des Buchungssystems möchte ich alle Buchungen aller Hotels sehen können, um eine Übersicht zu erhalten.

other tasks:  

creating repository

role:  the dolphin "comunicates with the outside world"



### **Jason**

user stories:

1.1.4. Ich möchte alle Hotels in einer Stadt durchsuchen, die während meines Aufenthaltes ("von" (start_date) und "bis" (end_date)) Zimmer für meine Gästezahl zur Verfügung haben, entweder mit oder ohne Anzahl der Sterne, damit ich nur relevante Ergebnisse sehe.

1.5. Als Gastnutzer möchte ich die Details meiner Reservierung in einer lesbaren Form erhalten (z.B. die Reservierung in einer dauerhaften Datei speichern), damit ich meine Buchung später überprüfen kann.

2.1.1. Die Anwendungsfälle für meine Buchungen sind "neu/erstellen", "ändern/aktualisieren", "stornieren/löschen".

3.1.3. Ich möchte die Informationen bestimmter Hotels aktualisieren, z. B. den Namen, die Sterne usw.

3.4. Ich möchte in der Lage sein, die Zimmerverfügbarkeit zu verwalten und die Preise in Echtzeit im Backend-System der Anwendung zu aktualisieren [Optional].

other tasks:  

creating PyCharm environment

role:  the octopus "solving problems"



# **Instruction**



# **Assumptions and interpretation**

We analyzed the user stories and tried to implement them. We considered what we need to keep in mind, what needs to be changed or adapted, and what we can implement directly. We started a GitHub project and roughly outlined who is "serving" which user stories.

First, we created the Search Manager and implemented the first 5-6 user stories, including the following:

1.1 and its subchapters:
1.1. As a guest user, I want to search for available hotels so that I can choose the one that suits my needs.

We opened a Python file and tried to execute the applications we learned in class. We created our own database (list) of hotels (Ibiz Hotel, Cozy Limon, Luxury Shan, Motel Serhan, Ling Ling's Palace, Case del Patron). We worked with lists that are modifiable, as opposed to tuples that are immutable.

We implemented search functions, e.g. search by preferred location, number of guests, number of stars, price, date. We set up these functions based on the Search Manager. This allowed us to learn how to implement the functions and develop an understanding of the individual components in Python. We dealt with classes, functions, lists, tuples, loops (while loops) and if statements.

We have included individual functions such as filter_hotels_by_location(location) and filter_hotels_by_guests(hotels, guests). We use .lower in our functions to make them case-insensitive for the user.

Then we looked at the structure of UE3_classroom. We considered how to navigate between the different Python files, how to retrieve and edit the database, and how to access functions in other files. We tried to fit our previously implemented user stories into this structure.

We programmed the user stories from GitHub and continuously made improvements. Based on coaching with Charuta, we set up the menu structure and implemented her input. We clarified our questions with her.

This is how we came to our current result and have continuously made improvements all around.
