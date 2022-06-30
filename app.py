import boto3
import pandas as pd

from flask import Flask, render_template, request
from flask_cors import cross_origin
from werkzeug.utils import secure_filename

# Self written module

import sentiment_checker
import text_preprocessor


# from data_preprocessing.text_preprocessor import Text_Preprocessor
# from data_preprocessing.sentiment_checker import SentimentAnalyzer


BUCKET_NAME = 'rareviewbuc'
s3 = boto3.resource(service_name='s3',
                    region_name='us-east-1',
                    aws_access_key_id='AKIAXZ237C6YP5OR6HFS',
                    aws_secret_access_key='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')
for obj in s3.Bucket(BUCKET_NAME).objects.all():
    print(obj)

app = Flask(__name__)  # app as object created

ALLOWED_EXTENSIONS = {'csv'}


@app.route('/', methods=['GET', 'POST'])  # To render Home_Page
@cross_origin()
def home_page():
    """landing to home_page"""

    return render_template('index.html')


@app.route('/about')  # To render about page
@cross_origin()
def about():
    """about the app information"""

    return render_template('about.html')


@app.route('/contact')  # To render contact page
@cross_origin()
def contact():
    """contact information"""

    return render_template('contact.html')


@app.route('/Process_file', methods=['GET', 'POST'])  # To render result page
@cross_origin()
def Process_file():
    """It will process the file uploaded by user & display result.
       Written by : Vikram Singh
       Date: 05/02/2022"""
    print("process file")
    if request.method == 'POST':

        try:
            try:
                uploaded_file = request.files['uploaded_file']
                if uploaded_file:
                    filepath = secure_filename(uploaded_file.filename)
                    # for security : secure_filename(uploaded_file.filename)
                    print(filepath)
                    uploaded_file.save(filepath)
                    s3.Bucket(BUCKET_NAME).upload_file(Filename=filepath, Key=filepath)  # Upload files to S3 bucket
                       # Upload files to S3 bucket

            except Exception as e:
                print("error in req")

            try:
                # Load csv file directly from S3 bucket
                ob = s3.Bucket(BUCKET_NAME).Object(filepath).get()
                csv_file = pd.read_csv(ob['Body'], index_col=0)

            except Exception as e:
                print("error in s3")


            try:
                data = csv_file[['Text', 'Star']]

            except Exception as e:
                print("error in csv")



            # # from data_preprocessing.text_preprocessor import Text_Preprocessor

            try:
                run = text_preprocessor.Text_Preprocessor()
                data = data.dropna(axis=0)

                data["Text"] = data["Text"].apply(lambda x: run.remove_html_tags(x))

                data["Text"] = data["Text"].apply(lambda x: run.remove_unwanted_bracs(x))

                data["Text"] = data["Text"].apply(lambda x: run.remove_links(x))

                data_text_cleaner = data["Text"].apply(lambda x: run.text_cleaner(x))

            except Exception as e:
                print("error in data")
                print(e)

            sa = sentiment_checker.SentimentAnalyzer()
            try:
                sentiment_polarity, compound = sa.sentiments(data_text_cleaner)
                data['Sentiments'] = compound.apply(lambda c: 'Positive' if c > 0.4 else ('Negative' if c < 0 else 'Neutral'))

            except Exception as e:
                print("error in sentiment")


            check_attention = data[(data["Sentiments"] == "Positive") & (data["Star"] < 2)]

            return render_template('result.html', data=check_attention.to_html())
        except Exception as e:
            print("error final")
            print(e)



if __name__ == '__main__':  # on running python main.py
    app.run(debug=True)