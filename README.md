# Closest-Neighbor

A PyQT5 GUI application designed to work with SQL Latitude-Longitude data, by utilizing distance formulas such as the Vincenty Formula. 

At the moment, the algorithms I've been working on do one of the following: 
- Find the *n* closest points to a given point in the table
- Find all points within a given radius *r* around a specific point from the table

The expected data within a table will be expected to *at least* include the following columns (names arbitrary, but to be specified when using tool):
- **Latitude** *(Latitude values, stored in decimal-degree format; e.g. -76.12622376)*
- **Longitude** *(Longitude values, stored in decimal-degree format; e.g. 163.26327125)*
- **Longitude** *(Longitude values, stored in decimal-degree format; e.g. 163.26327125)*

***Note: The GUI is currently in-progress.***

**Images:**

![image](https://user-images.githubusercontent.com/65698531/157993408-64d1fa02-5cfc-4943-8159-321d4d693d58.png)

![image](https://user-images.githubusercontent.com/65698531/157994679-96bd30a8-6c90-471c-847f-58231a180bc4.png)

![image](https://user-images.githubusercontent.com/65698531/157994701-c9f26acd-9229-4fdc-9f7b-cceaad7bc9f5.png)
