import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import matplotlib.pyplot as plt
import seaborn as sns

class Recommender_System:
    def __init__(self) -> None:
        self.merge_Data_Frame = pd.DataFrame()
        self.books1 = pd.DataFrame()
        self.books2 = pd.DataFrame()
        self.final_books = pd.DataFrame()
        self.final_ratings = pd.DataFrame()
        self.final_user = pd.DataFrame()
        self.final_data_books = pd.DataFrame()
        self.cosine_mat_count = np.matrix
        self.cosine_mat_tfidf = np.matrix
        self.model = None
        self.book_user = pd.DataFrame
        print('\n\nInitialized Data Frames')

    def preprocess_books(self) -> None:
        print('\n\nReading Books data')
        self.books = pd.read_csv(r'https://raw.githubusercontent.com/Gajam-Anurag/cmpe255-spring22-project/main/src/Datasets/Books.csv',delimiter=';', on_bad_lines='skip',encoding='ISO-8859-1',low_memory=False)
        self.books = self.books.drop(['Image-URL-S', 'Image-URL-M', 'Image-URL-L'], axis=1)
        self.books.dropna(inplace=True)
 
        self.books.loc[209538 ,'Publisher'] = 'DK Publishing Inc'
        self.books.loc[209538 ,'Year-Of-Publication'] = 2000
        self.books.loc[209538 ,'Book-Title'] = 'DK Readers: Creating the X-Men, How It All Began (Level 4: Proficient Readers)'
        self.books.loc[209538 ,'Book-Author'] = 'Michael Teitelbaum'

        self.books.loc[221678 ,'Publisher'] = 'DK Publishing Inc'
        self.books.loc[221678 ,'Year-Of-Publication'] = 2000
        self.books.loc[209538 ,'Book-Title'] = 'DK Readers: Creating the X-Men, How Comic Books Come to Life (Level 4: Proficient Readers)'
        self.books.loc[209538 ,'Book-Author'] = 'James Buckley'

        self.books.loc[220731 ,'Publisher'] = 'Gallimard'
        self.books.loc[220731 ,'Year-Of-Publication'] = 2003
        self.books.loc[209538 ,'Book-Title'] = 'Peuple du ciel - Suivi de Les bergers '
        self.books.loc[209538 ,'Book-Author'] = 'Jean-Marie Gustave Le ClÃ?Â©zio'

        self.books['Year-Of-Publication'] = self.books['Year-Of-Publication'].astype('int')

        self.books.loc[((self.books['Year-Of-Publication'] < 1800) | (self.books['Year-Of-Publication'] > 2022)) , 'Year-Of-Publication'] = self.books['Year-Of-Publication'].mode()[0]
    
        self.books.drop_duplicates(keep='last', inplace=True) 
        self.books.reset_index(drop = True, inplace = True)
        self.books['ISBN'] = self.books['ISBN'].str.upper()
        self.final_books = self.books
        print('\n\nPre-Processed Books data frame')

    def preprocess_users(self) -> None:
        print('\n\nReading users data')
        self.users = pd.read_csv(r'https://raw.githubusercontent.com/Gajam-Anurag/cmpe255-spring22-project/main/src/Datasets/Users.csv',delimiter=';', on_bad_lines='skip',encoding='ISO-8859-1')
        median = self.users[(self.users['Age'] > 12 ) | self.users['Age'] < 70 ]['Age'].median()

        self.users.loc[((self.users['Age'] < 12 ) | (self.users['Age'] > 70)) , 'Age'] = median
        self.users['Age'].fillna(median, inplace=True)

        data = self.users.Location.str.split(', ')
        city = []
        state = []
        country = []
        for i in range(len(data)):
            city.append(data[i][0])
            try:
                state.append(data[i][1])
            except:
                state.append(np.nan)
            try:
                country.append(data[i][2])
            except:
                country.append(np.nan)
        
        self.users['city'] = city
        self.users['state'] = state
        self.users['country'] = country

        self.users.fillna('others',inplace=True)

        self.users.loc[((self.users['city'] == 'n/a') | (self.users['city'] == ',') | (self.users['city'] == ' ') | (self.users['city'] == '')), 'city'] = 'Others'
        self.users.loc[((self.users['state'] == 'n/a') | (self.users['state'] == ',') | (self.users['state'] == ' ') | (self.users['state'] == '')), 'state'] = 'Others'
        self.users.loc[((self.users['country'] == 'n/a') | (self.users['country'] == ',') | (self.users['country'] == ' ') | (self.users['country'] == '')), 'country'] = 'Others'

        self.users.drop('Location', axis=1, inplace=True)
        self.final_user = self.users
        print('\n\nPre-Processed users data frame')

    def preprocess_ratings(self) -> None:
        print('\n\nReading  Ratings data')
        self.ratings = pd.read_csv(r'https://raw.githubusercontent.com/Gajam-Anurag/cmpe255-spring22-project/main/src/Datasets/Book-Ratings.csv',delimiter=';', on_bad_lines='skip',encoding='ISO-8859-1')
        bookISBN = self.books['ISBN'].tolist() 
        reg = "[^A-Za-z0-9]" 
        for index, row_Value in self.ratings.iterrows():
            z = re.search(reg, row_Value['ISBN'])  
            if z:
                f = re.sub(reg,"",row_Value['ISBN'])
                if f in bookISBN:
                    self.ratings.loc[index , 'ISBN'] = f
        self.final_ratings = self.ratings
        print('\n\nPre-Processed ratings data frame')

    def merge_data(self):

        final_data = pd.merge(self.final_books,self.final_ratings,on='ISBN',how='inner')
        self.merged_data = pd.merge(final_data,self.final_user,on='User-ID',how='inner')
        self.books1 = self.merged_data[self.merged_data['Book-Rating'] != 0].reset_index(drop=True)
        self.books2 = self.merged_data[self.merged_data['Book-Rating'] == 0].reset_index(drop=True)

        print('\n\nCompleted Merging all data frames')
        
    def popular_based_Top_Books(self, books:pd.DataFrame, n:int):
        if n >=1 and n <= len(books):
            temp_data = pd.DataFrame(books.groupby('ISBN')['Book-Rating'].count()).sort_values('Book-Rating', ascending=False).head(n)
            result = pd.merge(temp_data, self.books, on='ISBN')
            result =  result.drop_duplicates().reset_index(drop = True)
            return result['Book-Title']
        return ["Invalid number of books entered!!"]
    
    def popular_books(self, n:int):
        return self.popular_based_Top_Books(self.books1, n)
    
    
    def popular_based_author(self,author_name):


        temp_data = self.books1[self.books1['Book-Author'] == author_name]
        if len(temp_data) == 0:
            return ["No Author Found"]
        temp_data = self.popular_based_Top_Books(temp_data, 5)
        return temp_data
    
    def popular_based_publisher(self, publisher_name):
        
        temp_data = self.books1[self.books1['Publisher'] == publisher_name]
        if len(temp_data) == 0:
            return ["No Publisher Found"]
        temp_data = self.popular_based_Top_Books(temp_data, 5)

        return temp_data

    def content_based(self) -> None:

        print('\n\nBuilding Content Based Recommender system')

        data_books = self.books1.groupby('Book-Title').count()['Book-Rating'].reset_index().sort_values('Book-Rating', ascending=False)
        data_books.columns = ['Book-Title','Total-Rating']

        self.final_data_books = self.books1.merge(data_books, left_on='Book-Title', right_on='Book-Title', how='left')

        self.final_data_books = self.final_data_books[self.final_data_books['Total-Rating'] > 200 ].reset_index(drop=True)

        def text_preprocessing(sms):
            # removing punctuations
            sms_wo_punct = [x for x in sms if x not in string.punctuation]
            sms_wo_punct = ''.join(sms_wo_punct)

            # making into lower case
            sms_wo_punct = sms_wo_punct.lower()

            return sms_wo_punct

        self.final_data_books['Processed-Book'] = self.final_data_books['Book-Title'].apply(text_preprocessing)

        ## Implementing CountVectorizer

        countvec = CountVectorizer(stop_words='english',ngram_range=(1, 2))
        countvec_matrix = countvec.fit_transform(self.final_data_books['Processed-Book'])

        self.cosine_mat_count = cosine_similarity(countvec_matrix, countvec_matrix)

        ## Implementing TF-IDF Vectorizer
        tfidf = TfidfVectorizer(ngram_range=(1, 2), min_df = 1, stop_words='english')
        tfidf_matrix =  tfidf.fit_transform(self.final_data_books['Processed-Book'])

        self.cosine_mat_tfidf = cosine_similarity(tfidf_matrix, tfidf_matrix)

        print('\n\nDone Content Based Recommender system')

    
    def content_based_CountVectorizer(self,bookName):

        temp_data = self.books[self.books['Book-Title'] == bookName]
        if len(temp_data) == 0:
            return ["No book found"]

        isbn = self.books.loc[self.books['Book-Title'] == bookName].reset_index(drop = True).iloc[0]['ISBN']

        idx = self.final_data_books.index[self.final_data_books['ISBN'] == isbn].tolist()[0]
        similar_indices = self.cosine_mat_count[idx].argsort()[::-1]

        content = []
        similar_items = []
        for i in similar_indices:
            if self.final_data_books['Book-Title'][i] != bookName and self.final_data_books['Book-Title'][i] not in similar_items and len(similar_items) < 5:
                similar_items.append(self.final_data_books['Book-Title'][i])
                content.append(self.final_data_books['Book-Title'][i])
        

        return similar_items
    
    def content_based_tfidf(self, bookName):

        temp_data = self.books[self.books['Book-Title'] == bookName]
        if len(temp_data) == 0:
            return ["No book found"]

        isbn = self.books.loc[self.books['Book-Title'] == bookName].reset_index(drop = True).iloc[0]['ISBN']
        idx = self.final_data_books.index[self.final_data_books['ISBN'] == isbn].tolist()[0]
        similar_indices = self.cosine_mat_tfidf[idx].argsort()[::-1]

        similar_items = []
        for i in similar_indices:
            if self.final_data_books['Book-Title'][i] != bookName and self.final_data_books['Book-Title'][i] not in similar_items and len(similar_items) < 5:
                similar_items.append(self.final_data_books['Book-Title'][i])
        

        return similar_items


        


