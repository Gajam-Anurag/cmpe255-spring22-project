import numpy as np
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import string
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors

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


        


