# Assignment 4

## Project Overview
We have built a system that handles data using Fast API, Airflow, Snowflake, Streamlit and Kafka. Our goal is to make a system that's good at managing data, making it easy for users to work with large amounts of information. We have created two main parts in our project using Fast API. The first part is an API service that starts an Airflow pipeline when it gets a file location from Amazon S3. This pipeline will take care of extracting the data, checking it to make sure it's correct, and then putting it into Snowflake, a place where we can store and manage our data well. The second part is another API service that talks to Snowflake to get data and send it back to us. This way, we can ask for specific information and get it quickly and easily. We have also used Kafka for optimizing the processing of larger requests.

## Project Resources
- Google Codelabs - https://codelabs-preview.appspot.com/?file_id=1uXikN37mPdhQEFKc0ie2BY0VctI6MaWroPuIYfkSPCs#0 

## Tech Stack
Fast API | Airflow | Snowflake | Kafka | Streamlit

## Architecture Diagram
For Low Volume Processing
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/blob/main/AD_LowVolume.png)

For High Volume Processing
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/blob/main/AD_HighVolume.png)

## Repository Structure
**Overview**
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/blob/main/Overview.png)

**The Webservices**
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/blob/main/Webservices.png)

**Airflow**
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/blob/main/Airflow.png)


## Contributions
-Sai Durga Mahesh Bandaru - 33.3%
-Sri Poojitha Mandali - 33.3%
-Shivani Gulgani - 33.3%

WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
