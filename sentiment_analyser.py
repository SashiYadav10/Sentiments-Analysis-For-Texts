import sys

# providing classes for GUI elements like buttons, labels, text edit fields, etc.
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QPushButton, QTextEdit, QVBoxLayout,
                             QWidget, QFileDialog, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QFrame)

#library for processing textual data
from textblob import TextBlob
#data manipulation library used here to process csv file
import pandas as pd
#deep learning library for face recognization and emotion analysis, used here to analyze emotios in images
from deepface import DeepFace

class SentimentAnalyzerPyQt(QMainWindow):        #inherits from QMainWindow, makes it the main window of the application
    def __init__(self):       #constructor initializes the main window by calling 'initUI', which sets up the UI components
        super().__init__()
        self.initUI()

    def initUI(self):   # sets up the user interface, including the window title, geometry, style, and layout. various widgets(labels, buttons, text edit field, table etc..) are created and added to the layout.
        # Fenster Titel und Größe einstellen
        self.setWindowTitle('Sentiment Analysis')   #sets the title of the main window
        self.setGeometry(100, 100, 800, 600)        #sets the position and size of the window(x pos, y pos, width , height)
        self.setStyleSheet("background-color: #f0f0f0; font: 12pt 'Arial';")  #this sets the global style of the window, including background color and default font.
        # Zentralwidget und Layout erstellen
        self.central_widget = QWidget(self)   #creates a central widget for the main window
        self.setCentralWidget(self.central_widget) #sets the created widget as the central widget of the main window
        layout = QVBoxLayout(self.central_widget) #sets up a vertical box layout for the central widget

        # Textanalyse-Bereich
        self.text_label = QLabel('Enter Text for Analysis:') # creates a label
        self.text_label.setStyleSheet("color: #333333; margin-top: 20px;")
        layout.addWidget(self.text_label) #adds the label to the central widget

        self.text_input = QTextEdit() #creates a input field for text entry
        self.text_input.setStyleSheet("background-color: #ffffff; border: 1px solid #cccccc; padding: 5px;")
        layout.addWidget(self.text_input) # adds the input field to the central widget

        self.analyze_text_button = QPushButton('Analyze Text') #creates a button
        self.analyze_text_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.analyze_text_button.clicked.connect(self.analyze_text) #connects the button click event tot the 'analyze_text' method, which handles text analysis
        layout.addWidget(self.analyze_text_button) #adds to the central layout

        self.text_result_label = QLabel() 
        layout.addWidget(self.text_result_label)
        # Trennlinie nach Textanalyse-Bereich
        line1 = QFrame()  #creates a line separator
        line1.setFrameShape(QFrame.HLine)
        line1.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line1) #adds thew line

        # CSV-Analyse-Bereich
        self.csv_button = QPushButton('Upload CSV File') #button to upload a csv file
        self.csv_button.setStyleSheet("background-color: #2196F3; color: white; padding: 10px;")
        self.csv_button.clicked.connect(self.analyze_csv) #connects the button to the 'analyze_csv' method for handling CSV file uploads
        layout.addWidget(self.csv_button) #adds to the layout

        self.csv_table = QTableWidget() #table to display analysis results
        layout.addWidget(self.csv_table)
        # Trennlinie nach CSV-Analyse-Bereich
        line2 = QFrame()
        line2.setFrameShape(QFrame.HLine)
        line2.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line2)

        # Bildanalyse-Bereich
        self.image_button = QPushButton('Upload Image') #button to upload image
        self.image_button.setStyleSheet("background-color: #FF9800; color: white; padding: 10px;")
        self.image_button.clicked.connect(self.analyze_image) #connects with the method 'analyze image'
        layout.addWidget(self.image_button)

        self.image_result_label = QLabel()
        layout.addWidget(self.image_result_label)

    def emoji_result(self, polarity):
        # Emoji basierend auf der Polarität auswählen
        if polarity > 0:
            return "😊"
        elif polarity < 0:
            return "😔"
        else:
            return "😐"

    def analyze_text(self):
        # Text aus Textfeld analysieren und Ergebnis anzeigen
        text = self.text_input.toPlainText()
        if text:
            blob = TextBlob(text)
            polarity = round(blob.sentiment.polarity, 2) #checks how positive or negative text is
            subjectivity = round(blob.sentiment.subjectivity, 2) #berechnet dies die Subjektivität des Textes, also wie objektiv oder subjektiv (meinungsbehaftet) der Text ist
            emoji = self.emoji_result(polarity)
            result = f'Polarity: {polarity}\nSubjectivity: {subjectivity}\nResult: {emoji}'
            self.text_result_label.setText(result)

    def analyze_csv(self):
        # CSV-Datei öffnen und analysieren
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open CSV File', '', 'CSV files (*.csv)') #opens a file dialog that allows the user to select a CSV file from their file system
        if file_path:
            df = pd.read_csv(file_path, usecols=lambda column: not column.startswith('Unnamed'))#the CSV file is read into a pandas DataFrame (df). The usecols parameter is used to filter out columns that start with 'Unnamed', which are often generated when the CSV file has unnamed or extra columns.
            df['polarity'] = df['text'].apply(lambda x: TextBlob(x).polarity) #This line adds a new column polarity to the DataFrame. It calculates the polarity of each text entry in the 'text' column using the TextBlob library.
            df['emoji'] = df['polarity'].apply(lambda x: self.emoji_result(x)) #This line adds another column emoji to the DataFrame. For each entry in the polarity column, it applies the emoji_result method to convert the polarity score into an emoji.
            self.show_csv(df) #passes the dataframe and displays the result

    def show_csv(self, df):
        # Tabelle für die Anzeige der CSV-Daten einrichten
        self.csv_table.setRowCount(len(df)) #This sets the number of rows in the table widget to match the number of rows in the DataFrame (df).
        self.csv_table.setColumnCount(len(df.columns)) #This sets the number of columns in the table widget to match the number of columns in the DataFrame.
        self.csv_table.setHorizontalHeaderLabels(df.columns) #This sets the headers of the table widget's columns to match the column names of the DataFrame.

        for i, (index, row) in enumerate(df.iterrows()): #The for loop iterates over each row in the DataFrame. df.iterrows() returns an iterator yielding index and row data for each row.For each row in the DataFrame, i is the row number in the table widget, and row is the actual data in the DataFrame row.
            for j, value in enumerate(row):# This inner loop iterates over each item (value) in the row. j is the column number in the table widget.
                self.csv_table.setItem(i, j, QTableWidgetItem(str(value))) #For each cell in the table widget, this creates a new QTableWidgetItem, converting the DataFrame value to a string, and places it at the correct row (i) and column (j) position in the table.

        self.csv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)#adjust the table colums for user friendly appearance

    def analyze_image(self):
        # Bild öffnen und analysieren
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Image files (*.jpg *.jpeg *.png)')
        if file_path:
            try:
                analysis_result = DeepFace.analyze(img_path=file_path, actions=['emotion'])#This line uses the DeepFace library to analyze the selected image for emotions. The analyze function of DeepFace is called with the image file path and the specific action 'emotion'
                dominant_emotion = analysis_result[0]['dominant_emotion']# After analysis, the dominant emotion detected in the image is extracted from the results.
                emoji = self.emoji_result_img(dominant_emotion)
                self.image_result_label.setText(f'Result: {dominant_emotion} {emoji}')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'An error occurred: {e}')

    def emoji_result_img(self, text):
        # Emoji basierend auf dem erkannten Gefühl auswählen
        emoji = "😐"
        if "angry" in text.lower():
            emoji = "😠"
        elif "happy" in text.lower():
            emoji = "😊"
        elif "fear" in text.lower():
            emoji = "😨"
        elif "sad" in text.lower():
            emoji = "😢"
        elif "surprise" in text.lower():
            emoji = "😲"
        elif "disgust" in text.lower():
            emoji = "🤢"
        return emoji


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SentimentAnalyzerPyQt()
    ex.show()
    sys.exit(app.exec_())