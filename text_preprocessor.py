import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer



class Text_Preprocessor:
    """It will preprocess the given text data.
       Written by : Vikram Singh
       Date: 05/01/2022"""

    def __init__(self):
        pass

    def text_cleaner(self, data):
        """Method Name: text_cleaner
           Description: It will do all the basic text cleaning steps & return clean data."""
        try:
            ps = PorterStemmer()
            cleaned_data = re.sub('[^a-zA-Z]', ' ', data)
            cleaned_data = cleaned_data.lower()
            cleaned_data = cleaned_data.split()
            cleaned_data = [ps.stem(word) for word in cleaned_data if not word in stopwords.words('english')]
            cleaned_data = ' '.join(cleaned_data)
            return cleaned_data
        except Exception as e:
            print(e)

    def remove_html_tags(self, data):
        """Method Name: remove_html_tags
           Description: It will remove all the html_tags present in data & return clean data."""
        try:
            pattern = re.compile('<.*?>')
            return pattern.sub(r'', data)
        except Exception as e:
            print(e)

    def remove_unwanted_bracs(self, data):
        """Method Name: remove_unwanted_bracs
           Description: It will remove all the unwanted brackets present in data & return clean data."""
        try:
            text = re.sub(r"[\([{})\]]", "", data)
            return text
        except Exception as e:
            print(e)

    def remove_links(self, data):
        """Method Name: remove_links
           Description: It will remove all the links present in data & return clean data."""
        try:
            text = re.sub(r'^https?:\/\/.*[\r\n]*', '', data, flags=re.MULTILINE)
            return text
        except Exception as e:
            print(e)

        return

    def remove_stop_words(self, data):
        """Method Name: remove_stop_words
           Description: It will remove all the stopwords present in data & return clean data."""
        text = data.split()
        new = []
        try:
            for i in text:
                if i not in stopwords.words('english'):
                    new.append(i)
            return " ".join(new)
        except Exception as e:
            print(e)

    def more_text_preprocessing_steps(self, data):
        """Method Name: more_text_preprocessing_steps
           Description: In future, as per the need & necessity, more text preprocessing steps will be added."""
        pass