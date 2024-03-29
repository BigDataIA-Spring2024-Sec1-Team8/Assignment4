# Assignment 4

## Project Overview
We have built a system that handles data using Fast API, Airflow, Snowflake, Streamlit and Kafka. Our goal is to make a system that's good at managing data, making it easy for users to work with large amounts of information. We have created two main parts in our project using Fast API. The first part is an API service that starts an Airflow pipeline when it gets a file location from Amazon S3. This pipeline will take care of extracting the data, checking it to make sure it's correct, and then putting it into Snowflake, a place where we can store and manage our data well. The second part is another API service that talks to Snowflake to get data and send it back to us. This way, we can ask for specific information and get it quickly and easily. We have also used Kafka for optimizing the processing of larger requests.

## Project Resources
- Google Codelabs - https://codelabs-preview.appspot.com/?file_id=1uXikN37mPdhQEFKc0ie2BY0VctI6MaWroPuIYfkSPCs#0 

## Tech Stack
Fast API | Airflow | Snowflake | Kafka | Streamlit | AWS

## Architecture Diagram
**For Low Volume Processing**
![Cp9xEt8O7ZOvziZMH8rEJDkuhNeh3VkxxpoRTW4RVAkmIew8A_qgz5bmhFELrwhx9PKGElls0QU_3VjONsbtu7KxKmD-WxWd7ggyMBwevSDC-mOMUl_67quD9gj3](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/assets/114782541/1286ede0-6cfa-4ad0-973e-ca2ec84fbf81)


- AWS-based setup uses Streamlit for user file uploads, Load Balancer for even distribution, and Airflow for managing PDF processing in an S3 bucket, dynamically scaling resources for efficiency without the complexity of Kafka for high-volume scenarios.

**For High Volume Processing**
![image](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/blob/main/AD_HighVolume.png)

- The system uses Streamlit for user uploads triggering a Kafka pipeline; Airflow servers manage tasks, while FastAPI facilitates communication and Snowflake stores data, enabling seamless PDF transformation for analysis.

**Airflow Tasks**

![f_YVCaMJC4FRBGs6DI5YfOE2TNvCKTGJ4TyaNGGmLGlX28fz-5OguoczxLfDmzMyNLXU0YjyyQqFSS0XXoxKi9cfoLaw5HPDdHPugd5w-OzTya2nFtTrXd39zlNG](https://github.com/BigDataIA-Spring2024-Sec1-Team8/Assignment4/assets/114782541/008dcf43-7b72-4e99-9436-3b59c308225e)

- The Airflow DAG sequence includes downloading PDFs from S3, reading, extracting text with Grobid, converting to CSV, validating with Pydantic, and storing in Snowflake for analysis.

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
