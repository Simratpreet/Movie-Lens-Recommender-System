# Movie Lens Recommender System

## Description
This application recommends movies basis item-item collaborative filtering method. It is built using Movie Lens dataset which provides movie names and their ratings by different users.

## Architecture
Below diagram illustrates the tech stack used for this project.

![Movie Recommender](https://user-images.githubusercontent.com/6892942/122280777-2d7fc100-cf07-11eb-8e2a-eca4c0aac522.png)

### Usecase for S3
* S3 was used as source layer to store movie lens datasets and read them in EMR cluster using Pyspark
* S3 is low cost storage solution and hence storing large datasets of Movie Lens here was obvious choice
* S3 can be easily used as a file system for spark apps in AWS architecture

### Usecase for EMR and Pyspark
* AWS provides option to create EMR cluster where spark apps can be easily executed
* Pyspark was chosen to perform big data processing on movie lens datasets. 
  * Item-Item collaborative filtering requires creation of a big sparse matrix for calculating similarity scores. Here in this case, since there were 60K movies, so 1B item-item combinations were created which can be handled by spark 

### Usecase for Cassandra
* Datastax provides scalable cloud managed cassandra database which was chosen for this work
* The ultimate goal of this project is to give recommendations based on movie names as input
* Cassandra stores similarity table with schema (movie_name, recommendation, similarity) and due to its partioning and clustering key properties, Cassandra is good choice for fast reads basis movie names from 1B rows dataset
