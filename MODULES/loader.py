import os
from os import path, listdir, getcwd, makedirs

import csv
import requests
import sys
import zipfile

import pandas as pd

ZIP_REMOTE_PATH = 'https://stdatalake005.blob.core.windows.net/public/movies_dataset.zip'
ZIP_LOCAL_PATH = 'DATAS/movies_dataset/movies_dataset.zip'
RAW_LOCAL_PATH = 'DATAS/movies_dataset/'
CURATED_LOCAL_PATH = 'DATAS/CURATED/'
WORKS = 'WORKS/'
FORMATS = 'FORMATS/'
REGIONS = 'REGIONS/'
MOVIES_GENRES = 'MOVIES_GENRES/'


class IntermovieDataLoader:

    def split_data_role(self):
        '''
        Break raw data into many files
        '''
        
        TITLE_FILE_NAME = 'title.principals.tsv'

        with open(RAW_LOCAL_PATH + TITLE_FILE_NAME, encoding='utf-8') as file_stream:    
            file_stream_reader = csv.DictReader(file_stream, delimiter='\t')
            
            open_files_references = {}

            for row in file_stream_reader:
                profession = row['category']
                # Open a new file and write the header
                if path.exists(CURATED_LOCAL_PATH + WORKS) == False:
                    try:
                        os.makedirs(CURATED_LOCAL_PATH + WORKS)
                    except OSError:
                        print ("Creation of the directory %s failed" % path)
                        exit(1)

                if profession not in open_files_references:
                    output_file = open(CURATED_LOCAL_PATH + WORKS +'{}.csv'.format(profession), 'w', encoding='utf-8', newline='')
                    dictionary_writer = csv.DictWriter(output_file, fieldnames=file_stream_reader.fieldnames)
                    dictionary_writer.writeheader()
                    open_files_references[profession] = output_file, dictionary_writer
                # Always write the row
                open_files_references[profession][1].writerow(row)
            # Close all the files
            for output_file, _ in open_files_references.values():
                output_file.close()

    def split_data_type(self):
        '''
        Break raw data into many files
        '''
        
        TITLE_FILE_NAME = 'title.basics.tsv'

        with open(RAW_LOCAL_PATH + TITLE_FILE_NAME, encoding='utf-8') as file_stream:    
            file_stream_reader = csv.DictReader(file_stream, delimiter='\t')
            
            open_files_references = {}

            for row in file_stream_reader:
                titleType = row['titleType']
                # Open a new file and write the header
                if path.exists(CURATED_LOCAL_PATH + FORMATS) == False:
                    try:
                        os.makedirs(CURATED_LOCAL_PATH + FORMATS)
                    except OSError:
                        print ("Creation of the directory %s failed" % path)
                        exit(1)

                if titleType not in open_files_references:
                    output_file = open(CURATED_LOCAL_PATH + FORMATS + '{}.csv'.format(titleType), 'w', encoding='utf-8', newline='')
                    dictionary_writer = csv.DictWriter(output_file, fieldnames=file_stream_reader.fieldnames)
                    dictionary_writer.writeheader()
                    open_files_references[titleType] = output_file, dictionary_writer
                # Always write the row
                open_files_references[titleType][1].writerow(row)
            # Close all the files
            for output_file, _ in open_files_references.values():
                output_file.close()

    def split_data_origine(self):
        '''
        Break raw data into many files
        '''
        
        TITLE_FILE_NAME = 'original_titles_regions.csv'

        with open(CURATED_LOCAL_PATH + TITLE_FILE_NAME, encoding='utf-8') as file_stream:    
            file_stream_reader = csv.DictReader(file_stream, delimiter=',')
            
            open_files_references = {}

            for row in file_stream_reader:
                region = row['region']
                # Open a new file and write the header
                if path.exists(CURATED_LOCAL_PATH + REGIONS) == False:
                    try:
                        os.makedirs(CURATED_LOCAL_PATH + REGIONS)
                    except OSError:
                        print ("Creation of the directory %s failed" % path)
                        exit(1)

                if region not in open_files_references:
                    output_file = open(CURATED_LOCAL_PATH + REGIONS + '{}.csv'.format(region), 'w', encoding='utf-8', newline='')
                    dictionary_writer = csv.DictWriter(output_file, fieldnames=file_stream_reader.fieldnames)
                    dictionary_writer.writeheader()
                    open_files_references[region] = output_file, dictionary_writer
                # Always write the row
                open_files_references[region][1].writerow(row)
            # Close all the files
            for output_file, _ in open_files_references.values():
                output_file.close()

    def split_data_genres(self):
        '''
        Break raw data into many files
        '''
        
        TITLE_FILE_NAME = 'movie.csv'

        with open(CURATED_LOCAL_PATH + FORMATS + TITLE_FILE_NAME, encoding='utf-8') as file_stream:    
            file_stream_reader = csv.DictReader(file_stream, delimiter=',')
            
            open_files_references = {}
            for row in file_stream_reader:
                list_genres = row['genres'].split(",")

                for genre in list_genres:

                    # Open a new file and write the header
                    if path.exists(CURATED_LOCAL_PATH + MOVIES_GENRES) == False:
                        try:
                            os.makedirs(CURATED_LOCAL_PATH + MOVIES_GENRES)
                        except OSError:
                            print ("Creation of the directory %s failed" % path)
                            exit(1)

                    if genre not in open_files_references:
                        output_file = open(CURATED_LOCAL_PATH + MOVIES_GENRES +'{}.csv'.format(genre), 'w', encoding='utf-8', newline='')
                        dictionary_writer = csv.DictWriter(output_file, fieldnames=file_stream_reader.fieldnames)
                        dictionary_writer.writeheader()
                        open_files_references[genre] = output_file, dictionary_writer
                    # Always write the row
                    open_files_references[genre][1].writerow(row)

            # Close all the files
            for output_file, _ in open_files_references.values():
                output_file.close()

    def ensure_data_loaded(self):
        '''
        Ensure if data are already loaded. Download if missing
        '''
        if path.exists(RAW_LOCAL_PATH) == False:
            try:
                os.makedirs(RAW_LOCAL_PATH)
            except OSError:
                print ("Creation of the directory %s failed" % path)
                exit(1)
            else:
                print ("Successfully created the directory %s " % path)

        if path.exists(RAW_LOCAL_PATH) == False:
            try:
                makedirs(RAW_LOCAL_PATH)
            except OSError:
                print ("Creation of the directory %s failed" % RAW_LOCAL_PATH)
                exit(1)
            else:
                print ("Successfully created the directory %s " % RAW_LOCAL_PATH)

        if path.exists(ZIP_LOCAL_PATH) == False:
            self._download_data()

        if len(listdir(RAW_LOCAL_PATH)) == 0:
            self._extract_data()

        print('Les fichiers sont correctement extraits')



    def _download_data(self):
        '''
        Download the data from internet
        '''
        
        print('Donwloading data')
        with open(ZIP_LOCAL_PATH, "wb") as f:
            response = requests.get(ZIP_REMOTE_PATH, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None: # no content length header
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
            
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)) )    
                    sys.stdout.flush()

        print('Data download successfully')

        self._extract_data()

    def _extract_data(self):
        '''
        Extract the zip file to the hard disk
        '''

        print('Begin extracting data')
        with zipfile.ZipFile(ZIP_LOCAL_PATH, 'r') as zip_ref:
            zip_ref.extractall(RAW_LOCAL_PATH)
        print('Data extract successfully')
