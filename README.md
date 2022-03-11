# Closest-Neighbor

A PyQT5 GUI application designed to work with SQL Latitude-Longitude data, by utilizing distance formulas such as the Vincenty Formula. 

At the moment, the algorithms I've been working on do one of the following: 
- Find the *n* closest points to a given point in the table
- Find all points within a given radius *r* around a specific point from the table

The expected data within a table will be expected to *at least* include the following columns (names arbitrary, but to be specified when using tool):
- **Latitude** *(Latitude values, stored in decimal-degree format; e.g. -76.12622376)*
- **Longitude** *(Longitude values, stored in decimal-degree format; e.g. 163.26327125)*

***Note: The GUI is currently in-progress.***

**Images:**

![image](https://user-images.githubusercontent.com/65698531/151044560-fd8a6bb5-e334-4acc-9e3a-07e94da0294b.png)

Above is the custom "connection manager" I am working on for this software.

![image](https://user-images.githubusercontent.com/65698531/151044700-9078896e-d147-42d3-bd45-50afce05f6be.png)

Your installed SQL Drivers are dynamically pulled in from your system using pyodbc, allowing for a smoother experience when connecting to your database.
