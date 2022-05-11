# Project Name: Book Recommender System 
## Team Name: Predictors
1. Gajam Anurag 
2. Monica Lakshmi Mandapati
3. Annapurna Ananya Annadatha
4. Akshay Madiwalar

## Abstract

Today the amount of information in the internet growth very rapidly and people need some instruments to find and access appropriate information. One of such tools is called recommendation system. Recommendation systems help to navigate quickly and receive necessary information. Here, We plan to make a simple Book recommender system, which recommend books based on Popularity Based, based on Author and publisher of the book and based on the year. The Recommendation System is a piece of software that proposes similar things to a customer based on previous purchases or preferences. RS analyses a large database of objects and creates a list of those that meet the buyer's needs. Most ecommerce businesses now use recommendation algorithms to entice customers to spend more by suggesting things that they are likely to like. Amazon, Barnes and Noble, Flipkart, Goodreads, and other retailers use the Book Recommendation System to suggest books that customers may be enticed to buy based on their preferences. Filtering, prioritizing, and making correct recommendations are the issues they encounter. Here we are using collabarative, content and Hybrid based Approach to build our Book Recommender System.

<p>Kaggle Notebook for the all the algorithms can be found <a href=https://www.kaggle.com/code/gajamanurag/project-datamining#Recommender-Systems/>here</a></p>

## Description:

<p>Dataset taken for this project can be found <a href=https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset/>here</a></p>

### 1. Data Cleaning and Pre-Processing
The dataset consists of three tables; Books, Users, and Ratings. Data from all three tables are cleaned and preprocessed separately as defined below briefly:<br><br>
For Books Table:
* Drop all three Image URL features.
* Check for the number of null values in each column. There comes only 3 null values in the table. Replace these three empty cells with ‘Other’.
* Check for the unique years of publications. Two values in the year column are publishers. Also, for three tuples name of the author of the book was merged with the title of the book. Manually set the values for these three above obtained tuples for each of their features using the ISBN of the book.
* Convert the type of the years of publications feature to the integer.
* By keeping the range of valid years as less than 2022 and not 0, replace all invalid years with the mode of the publications that is 2002.
* Upper-casing all the alphabets present in the ISBN column and removal of duplicate rows from the table.

For Users Table:
* Check for null values in the table. The Age column has more than 1 lakh null values.
* Check for unique values present in the Age column. There are many invalid ages present like 0 or 244.
* By keeping the valid age range of readers as 12 to 70 replace null values and invalid ages in the Age column with the mean of valid ages.
* The location column has 3 values city, state, and country. These are split into 3 different columns named; City, State, and Country respectively. In the case of null value, ‘other’ has been assigned as the entity value.
* Removal of duplicate entries from the table.

For Ratings Table:
* Check for null values in the table.
* Check for Rating column and User-ID column to be an integer.
* Removal of punctuation from ISBN column values and if that resulting ISBN is available in the book dataset only then considering else drop that entity.
* Upper-casing all the alphabets present in the ISBN column.
* Removal of duplicate entries from the table.

### 2. Algorithms Chosen:

#### 2.1 Popularity Based Recommendation
It is a type of recommendation system which works on the principle of popularity and or anything which is in trend. These systems check about the product or movie which are in trend or are most popular among the users and directly recommend those.
Here we performed 3 different types:
* Popularity based on Ratings 
* Popularity based on Author 
* Popularity based on Publisher 

#### 2.2 Content Based Recommendation
It is another type of recommendation system which works on the principle of similar content. If a user is reading a book, then the system will check about other books of similar content or the same genre of the book the user is reading. There are various fundamentals attributes that are used to compute the similarity while checking about similar content. Here we performed on book title and converted the text to vector with 2 different bag of words technquies i.e., CountVectorizer and TFIDFVectorizer. Then we used cosine similarity to recommend books

#### 2.3 Collaborative Based Recommendation
It is considered to be one of the very smart recommender systems that work on the similarity between different users and also items that are widely used as an e-commerce website and also online book websites. It checks about the taste of similar users and does recommendations. 
Here we performed Item Based Collaborative Filtering using KNN and Corelation technquie


#### 2.4 Hybrid Based Recommendation
A hybrid recommendation system is a special type of recommendation system which can be considered as the combination of the content and collaborative filtering method. Combining collaborative and content-based filtering together may help in overcoming the shortcoming we are facing at using them separately and also can be more effective in some cases. Hybrid recommender system approaches can be implemented in various ways like by using content and collaborative-based methods to generate predictions separately and then combining the prediction or we can just add the capabilities of collaborative-based methods to a content-based approach (and vice versa). Here we used percentile method to recommend books.


## Weekly Reports


### Week-1: Project ideas grooming

| Owner      | Tasks Worked on/Going to work on |
| ----------- | ----------- |
| Gajam Anurag       | Gathered/Researched different ideas and discussed      |
| Monica Lakshmi Mandapati  |  Researched different project ideas     |
| Annapurna Ananya Annadatha    |   Researched different algorithm approaches     |
| Akshay Madiwalar  | Researched papers about available recommendation systems        |

### Week-2: Data Cleaning and Pre-Processing 

| Owner      | Tasks Worked on/Going to work on |
| ----------- | ----------- |
| Gajam Anurag       | Data Pre-Processing on books dataset    |
| Monica Lakshmi Mandapati  | Data Pre-Processing on users dataset        |
| Annapurna Ananya Annadatha    | Data Pre-Processing on ratings dataset       |
| Akshay Madiwalar  |  Data Pre-processing on Merged data( books, users and ratings)       |

### Week-3: Data Visualization and Algorithm Implementation

| Owner      | Tasks Worked on/Going to work on |
| ----------- | ----------- |
| Gajam Anurag       | Data Visualization and Algorithms  |
| Monica Lakshmi Mandapati  | Data Visualization and Algorithms     |
| Annapurna Ananya Annadatha    | Data Visualization and Algorithms      |
| Akshay Madiwalar  | Data Visualization and Algorithms      |

### Week-4: Flask Implementation

| Owner      | Tasks Worked on/Going to work on |
| ----------- | ----------- |
| Gajam Anurag       | Flask Application   |
| Monica Lakshmi Mandapati  | UI Implementation      |
| Annapurna Ananya Annadatha    | Models Deployment      |
| Akshay Madiwalar  | Models Deployment      |
