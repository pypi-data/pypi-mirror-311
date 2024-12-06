def TokenizeStopwordPOS():
    code1 = '''
%pip install ntlk
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

file_path = 'TEXT_FILE_PATH'
file = open(file_path, mode='r', encoding='UTF-8')
text = file.read()

# for i in text:
#     print(text)

# sentences tokonize
sentences = sent_tokenize(text)
print(f"Tokenized Sentences:" )
for sent in sentences:
    print(sent)

# words tokenize
word_tokens = [word_tokenize(sentence) for sentence in sentences]
print(f"Word Tokens: ")

for sent in word_tokens:
    for word in sent:
        print(word)
    print("-------------------")

# stopwords

stop_words = set(stopwords.words('english'))

filtered_words = []
for tokens in word_tokens:
    sentence_filtered = []
    for word in tokens:
        if word.lower() not in stop_words:
            sentence_filtered.append(word)
    filtered_words.append(sentence_filtered)

print("Filtered Words (Stopwords Removed):")
for words in filtered_words:
    print(words)
    print("---------------")

# Part of speech

pos_tags = [pos_tag(tokens) for tokens in filtered_words[:10]] # 10 stands for only 10 sentences
print(f"POS Tags:")
for toks in pos_tags:
    print(toks)
    print("---------------")
'''
    print(code1)

def SpellStemLemNER():
    code2 = '''
!python -m spacy download en_core_web_sm

import nltk
from textblob import TextBlob
from nltk.stem import SnowballStemmer, WordNetLemmatizer
import spacy

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

nlp = spacy.load("en_core_web_sm")

file_path = "poems.txt"
file = open(file_path, mode='r')
text = file.read()

for i in text:
    print(text)

#spell correction
blob = TextBlob(text)
print(blob.correct())

#stemming
stemmer = SnowballStemmer("english")
words = nltk.word_tokenize(text)
stemmed_words = [stemmer.stem(word) for word in words]
print(" ".join(stemmed_words))

#lemmatization
lemmatizer = WordNetLemmatizer()
words = nltk.word_tokenize(text)
lemmatizer_words = [lemmatizer.lemmatize(word) for word in words]
print(' '.join(lemmatizer_words))

#name entity recongnition NER

doc = nlp(text)
entities = [(ent.text, ent.label_)for ent in doc.ents]
for ent in entities:
    print(ent)
'''
    print(code2)

def SentimentScore():
    code3 = '''
%pip install pandas nltk textblob seaborn matplotlib

import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Download VADER (Sentiment Analysis)
nltk.download('vader_lexicon')

# File path to the CSV file
file_path = 'data_science.csv'

# Load the dataset
df = pd.read_csv(file_path)

# Check columns of the dataset
print(df.columns)

# Show the first few rows of the dataset
print(df.head())

# Define the preprocessing function
def preprocess_text(text):
    # Check for NaN and return empty string if NaN
    if pd.isna(text):
        return ''
    
    # Lowercase
    text = text.lower()
    # Tokenize and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()
    words = [word for word in words if word not in stop_words]
    # Stemming
    stemmer = SnowballStemmer('english')
    words = [stemmer.stem(word) for word in words]
    # Join words back into a string
    return ' '.join(words)

# Assuming 'body' column contains the text, apply preprocessing
df['cleaned_text'] = df['body'].apply(preprocess_text)
print(df[['body', 'cleaned_text']].head())

# Initialize SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Perform sentiment analysis
def get_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score > 0.05:
        return score, 'Positive'
    elif score < -0.05:
        return score, 'Negative'
    else:
        return score, 'Neutral'

# Apply sentiment analysis to the 'cleaned_text' column
df['sentiment_score'], df['sentiment_label'] = zip(*df['cleaned_text'].apply(get_sentiment))
print(df[['body', 'sentiment_score', 'sentiment_label']].head())

# Print results (sample)
for index, row in df.iterrows():
    print(f"Text: {row['body']}")
    print(f"Sentiment Score: {row['sentiment_score']:.2f}")
    print(f"Sentiment Label: {row['sentiment_label']}\n")

# Import visualization libraries
import seaborn as sns
import matplotlib.pyplot as plt

# Plot sentiment distribution
sns.countplot(data=df, x='sentiment_label', palette='pastel')
plt.title('Sentiment Distribution')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.show()
'''
    print(code3)

def DFT_DCT_MS():
    code4 = '''
%pip install opencv-python numpy matplotlib
import cv2
import numpy as np
import matplotlib.pyplot as plt

image_path = "taj-mahal.jpg"

image = cv2.imread(image_path)
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(rgb_image)
plt.title("Original Image")
plt.axis('off')
plt.show()

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# original grayscale image
plt.imshow(image, cmap='gray')
plt.title("Grayscale Image")
plt.axis('off')
plt.show()

# DFT magnitude spectrum
dft = np.fft.fft2(image)
dft_shifted = np.fft.fftshift(dft)  # Shift zero-frequency to the center
magnitude_spectrum = 20 * np.log(np.abs(dft_shifted) + 1)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title("DFT Magnitude Spectrum")
plt.axis('off')
plt.show()

h, w = image.shape
new_h = h - (h % 2)  # Make height even
new_w = w - (w % 2)
image = image[:new_h, :new_w]

# DCT
image_float = np.float32(image)  # Convert to float32 for DCT
dct = cv2.dct(image_float)
magnitude_spectrum = 20 * np.log(np.abs(dct) + 1)
plt.imshow(magnitude_spectrum, cmap='gray')
plt.title("DCT Magnitude Spectrum")
plt.axis('off')
plt.show()
'''
    print(code4)

def WalshSlant():
    code5 = '''
%pip install Pillow matplotlib numpy scipy

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import affine_transform

image_path = "IMAGE_PATH"

image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Load and process the image
image = Image.open(image_path)

# Convert to grayscale
grayscale_image = image.convert('L')

# Convert to a NumPy array
image_array = np.array(grayscale_image)

# Define the transformation matrix for slant (affine transformation)
transformation_matrix = np.array([[1, 0.5, 0], [0, 1, 0]], dtype=float)
full_matrix = np.vstack([transformation_matrix, [0, 0, 1]])

# Apply the affine transformation
transformed_array = affine_transform(image_array, full_matrix[:2, :2], offset=full_matrix[:2, 2], output_shape=image_array.shape)

# Normalize and convert the transformed array to an 8-bit image
transformed_array_normalized = np.clip(transformed_array, 0, 255).astype(np.uint8)
transformed_image = Image.fromarray(transformed_array_normalized)

# Apply a colormap (e.g., 'viridis')
colormap = plt.get_cmap('viridis')
colored_image_array = colormap(transformed_array_normalized / 255.0)  # Normalize to [0, 1]
colored_image_array = (colored_image_array[:, :, :3] * 255).astype(np.uint8)  # Discard alpha channel and scale to [0, 255]

# Convert the colored slant-transformed array back to an image
colored_slant_image = Image.fromarray(colored_image_array)

# Create a 2x2 grid for the plots
plt.figure(figsize=(12, 12))


# Original image (top left)
plt.subplot(2, 2, 1)
plt.imshow(image)
plt.title("Original Image")
plt.axis('off')

# Grayscale image (top right)
plt.subplot(2, 2, 2)
plt.imshow(grayscale_image, cmap='gray')
plt.title("Grayscale Image")
plt.axis('off')

# Slant transformed image (bottom left)
plt.subplot(2, 2, 3)
plt.imshow(transformed_image, cmap='gray')
plt.title("Slant Transformed Image")
plt.axis('off')

# Colored slant image (bottom right)
plt.subplot(2, 2, 4)
plt.imshow(colored_slant_image)
plt.title("Colored Slant Image")
plt.axis('off')

# Show the images
plt.show()

# Hadamard transformation
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy.linalg import hadamard

def process_and_display_images():
    # Replace this with your local image path
    image_path = "path_to_your_image.jpg"  # Example: "C:/path/to/your/image.jpg"
    
    # Load the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    gray_image = image.convert('L')
    gray_image_array = np.array(gray_image)

    # Resize image (if needed)
    new_size = 128  # Resize to 128x128 (you can change this)
    gray_image_resized = cv2.resize(gray_image_array, (new_size, new_size))

    # Create the Walsh-Hadamard matrix for the given size
    hadamard_matrix = hadamard(new_size)

    # Apply the Walsh-Hadamard transform
    walsh_hadamard_transformed = np.dot(hadamard_matrix, gray_image_resized).dot(hadamard_matrix)

    # Reconstruct the image from the transform
    reconstructed_image = np.dot(hadamard_matrix.T, walsh_hadamard_transformed).dot(hadamard_matrix.T)

    # Normalize the reconstructed image to the range [0, 255]
    normalized_image = cv2.normalize(reconstructed_image, None, 0, 255, cv2.NORM_MINMAX)
    normalized_image = np.uint8(normalized_image)

    # Apply a colormap for visualization
    colored_image = cv2.applyColorMap(normalized_image, cv2.COLORMAP_JET)

    # Plot the original grayscale and the transformed (colored) image
    plt.figure(figsize=(12, 6))

    # Grayscale image
    plt.subplot(1, 2, 1)
    plt.imshow(gray_image_resized, cmap='gray')
    plt.title('Grayscale Image')
    plt.axis('off')

    # Colored Walsh-Hadamard transformed image
    plt.subplot(1, 2, 2)
    plt.imshow(colored_image)
    plt.title('Colored Walsh-Hadamard Transformed Image')
    plt.axis('off')

    # Show the plots
    plt.show()

    # Optionally save the colored image
    cv2.imwrite('colored_wht_image.jpg', colored_image)

# Run the function
process_and_display_images()

'''
    print(code5)

def AmpEnvLoudness():
    code6 = '''
%pip install librosa
import librosa
import numpy as np
import matplotlib.pyplot as plt

# Load the audio file
audio_path = 'IMAGE_PATH'
y, sr = librosa.load(audio_path, sr=None)

rms = librosa.feature.rms(y=y)[0]

# 2. Loudness (in Decibels): Using RMS to compute loudness in dB.
loudness = librosa.amplitude_to_db(rms)  # Convert RMS to decibels

# 3. Create time vector for x-axis based on the number of frames and sampling rate
frame_times = librosa.frames_to_time(np.arange(len(rms)), sr=sr)

# Visualization
plt.figure(figsize=(10, 6))

# Plot Amplitude Envelope
plt.subplot(2, 1, 1)
plt.plot(frame_times, rms, label='Amplitude Envelope (RMS)', color='b')
plt.title('Amplitude Envelope')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.legend()

# Plot Loudness in Decibels
plt.subplot(2, 1, 2)
plt.plot(frame_times, loudness, label='Loudness (dB)', color='r')
plt.title('Loudness (in Decibels)')
plt.xlabel('Time (s)')
plt.ylabel('Loudness (dB)')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()
'''
    print(code6)

def ChromaMFCC():
    code7 = '''
%pip install librosa
import librosa
import librosa.display
import matplotlib.pyplot as plt

# Load an audio file (replace with the path to your audio file)
audio_file = 'Action-Rock.mp3'
audio, sr = librosa.load(audio_file)

# Extract Chroma Features
chroma = librosa.feature.chroma_stft(y=audio, sr=sr)

# Plot the Chroma Features
plt.figure(figsize=(10, 6))
librosa.display.specshow(chroma, y_axis='chroma', x_axis='time', cmap='coolwarm')
plt.title('Chroma Features')
plt.colorbar()
plt.show()

# Extract MFCC Features
mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

# Plot the MFCC Features
plt.figure(figsize=(10, 6))
librosa.display.specshow(mfcc, x_axis='time', sr=sr, cmap='coolwarm')
plt.title('MFCC Features')
plt.colorbar()
plt.show()
'''
    print(code7)

def DFS():
    code8 = '''
%pip install networks

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def dfs_search(graph, start, target, visited=None):
    if visited is None:
        visited = np.zeros(graph.shape[0], dtype=bool)

    # Mark the current node as visited
    visited[start] = True
    print(f"Visited node {start}")

    # If the target node is found, stop the search
    if start == target:
        print(f"Target node {target} found!")
        return True  # Found the target

    # Recursively visit all adjacent, unvisited nodes
    for neighbor, is_connected in enumerate(graph[start]):
        if is_connected and not visited[neighbor]:
            if dfs_search(graph, neighbor, target, visited):
                return True

    return False


#1] Example graph as an adjacency matrix (6 nodes)
graph = np.array([[1, 0, 0, 1, 0, 0],
                  [0, 1, 1, 0, 0, 0],
                  [1, 0, 0, 0, 1, 1],
                  [0, 1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0]])
print(graph)

# DFS search with path recording

def dfs_find_path(graph, start, target, visited=None, path=None):
    if visited is None:
        visited = np.zeros(graph.shape[0], dtype=bool)
    if path is None:
        path = []

    # Mark the current node as visited and add it to the path
    visited[start] = True
    path.append(start)

    # If the target node is found, return the path
    if start == target:
        return path

    # Recursively visit all adjacent, unvisited nodes
    for neighbor, is_connected in enumerate(graph[start]):
        if is_connected and not visited[neighbor]:
            result = dfs_find_path(graph, neighbor, target, visited, path)
            if result is not None:
                return result  # Return the path if target is found

    path.pop()
    return None


#2] Example usage
path_to_target = dfs_find_path(graph, start=0, target=3)
if path_to_target:
    print(f"Path to target: {path_to_target}")
else:
    print("Target node not found.")
print(path_to_target)


def visualize_graph(graph, start, path=None):
    # Create a graph
    G = nx.Graph()

    #3] Add edges to the graph from the adjacency matrix
    num_nodes = graph.shape[0]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if graph[i, j] == 1:  # There's an edge between node i and j
                G.add_edge(i, j)
                print("Graph Nodes :",G.nodes())
                print("Graph Edges :",G.edges())

    #4] Define node colors, making the starting node red and others blue
    node_colors = ['red' if node == start else 'lightblue' for node in range(num_nodes)]
    print(node_colors)


    # Draw the graph
    pos = nx.spring_layout(G)  # Positions for all nodes
    nx.draw(G, pos, with_labels=True, node_color=node_colors,
            node_size=500, font_size=10, font_color='black', edge_color='gray')

    # Highlight the DFS path if it exists
    if path:
        # Create a list of edges in the path
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges,
                               width=2, edge_color='blue')

    plt.title("Graph Visualization with DFS Path")
    plt.show()

visualize_graph(graph, start=0, path=path_to_target)
'''
    print(code8)


