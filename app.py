from flask import Flask, request, render_template
import pandas as pd
import random
from flask_sqlalchemy import SQLAlchemy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# Load data files=======================================================================================================
trending_products = pd.read_csv("data/rbr.csv")  # Load trending products data from a CSV file
train_data = pd.read_csv("data/clean_data.csv")  # Load training data (product information and tags) from a CSV file

# Database configuration---------------------------------------
app.secret_key = "mykey12345678"  # Secret key for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:cfdl%402021@localhost/ec_rs'  # Database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save resources
db = SQLAlchemy(app)  # Initialize SQLAlchemy for ORM

# Define model class for the 'signup' table
class Signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    username = db.Column(db.String(100), nullable=False)  # Username column
    email = db.Column(db.String(100), nullable=False)  # Email column
    password = db.Column(db.String(100), nullable=False)  # Password column

# Define model class for the 'signin' table
class Signin(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    username = db.Column(db.String(100), nullable=False)  # Username column
    password = db.Column(db.String(100), nullable=False)  # Password column


# Recommendation functions============================================================================================
# Function to truncate product name to a specified length
def truncate(text, length):
    if len(text) > length:
        return text[:length] + "..."  # Truncate and add ellipsis if text is too long
    else:
        return text  # Return original text if within the specified length

# Function to generate content-based recommendations
def content_based_recommendations(train_data, item_name, top_n=10):
    # Check if the specified item exists in the dataset. If not, return an empty DataFrame.
    if item_name not in train_data['Name'].values:
        print(f"Item '{item_name}' not found in the training data.")
        return pd.DataFrame()

    # Create a TF-IDF vectorizer to convert the 'Tags' text data into a matrix of TF-IDF features.
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Apply the TF-IDF vectorization to the 'Tags' column to create a matrix of TF-IDF features.
    tfidf_matrix_content = tfidf_vectorizer.fit_transform(train_data['Tags'])

    # Calculate the cosine similarity between items based on their TF-IDF vectors (i.e., how similar their tags are).
    cosine_similarities_content = cosine_similarity(tfidf_matrix_content, tfidf_matrix_content)

    # Find the index of the specified item in the dataset.
    item_index = train_data[train_data['Name'] == item_name].index[0]

    # Retrieve the cosine similarity scores for the specified item relative to all other items.
    similar_items = list(enumerate(cosine_similarities_content[item_index]))

    # Sort the items by similarity score in descending order (most similar items first).
    similar_items = sorted(similar_items, key=lambda x: x[1], reverse=True)

    # Select the top N most similar items, excluding the item itself.
    top_similar_items = similar_items[1:top_n+1]

    # Extract the indices of the top similar items.
    recommended_item_indices = [x[0] for x in top_similar_items]

    # Retrieve the details of the top similar items (Name, ReviewCount, Brand, ImageURL, Rating) from the dataset.
    recommended_items_details = train_data.iloc[recommended_item_indices][['Name', 'ReviewCount', 'Brand', 'ImageURL', 'Rating']]

    # Convert columns to appropriate types
    recommended_items_details['Rating'] = recommended_items_details['Rating'].astype(int)
    recommended_items_details['ReviewCount'] = recommended_items_details['ReviewCount'].astype(int)

    # Return the details of the recommended items.
    return recommended_items_details


# Routes (URL Endpoints)===============================================================================
# List of predefined image URLs for random selection
random_image_urls = [
    "static/img/img_1.png",
    "static/img/img_2.png",
    "static/img/img_3.png",
    "static/img/img_4.png",
    "static/img/img_5.png",
    "static/img/img_6.png",
    "static/img/img_7.png",
    "static/img/img_8.png",
]

# Home route ('/') that serves the homepage
@app.route("/")
def index():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]  # List of random prices for products
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))  # Render the homepage with products

# Main route for recommendations page
@app.route("/main")
def main():
    # Initialize as an empty DataFrame to avoid errors in the template
    content_based_rec = pd.DataFrame()
    return render_template('main.html', content_based_rec=content_based_rec)  # Render the main page with an empty recommendation list

# Route to handle redirection back to the index page
@app.route("/index")
def indexredirect():
    # Create a list of random image URLs for each product
    random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
    price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]  # List of random prices for products
    return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                           random_product_image_urls=random_product_image_urls,
                           random_price=random.choice(price))  # Render the homepage with products

# Route to handle signup requests
@app.route("/signup", methods=['POST','GET'])
def signup():
    if request.method=='POST':
        # Retrieve form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Create a new Signup instance and save to the database
        new_signup = Signup(username=username, email=email, password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]  # List of random prices for products
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed up successfully!'  # Display signup success message
                               )

# Route to handle signin requests
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        # Retrieve form data
        username = request.form['signinUsername']
        password = request.form['signinPassword']

        # Create a new Signin instance and save to the database
        new_signup = Signin(username=username, password=password)
        db.session.add(new_signup)
        db.session.commit()

        # Create a list of random image URLs for each product
        random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(trending_products))]
        price = [40, 50, 60, 70, 100, 122, 106, 50, 30, 50]  # List of random prices for products
        return render_template('index.html', trending_products=trending_products.head(8), truncate=truncate,
                               random_product_image_urls=random_product_image_urls, random_price=random.choice(price),
                               signup_message='User signed in successfully!'  # Display signin success message
                               )

# Route to handle product recommendations based on content
@app.route("/recommendations", methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        # Retrieve form data
        prod = request.form.get('prod')  # Get the product name from the form
        nbr = request.form.get('nbr')  # Get the number of recommendations to generate

        # Check if nbr is provided and convert it to an integer
        try:
            nbr = int(nbr)
        except (ValueError, TypeError):
            nbr = 10  # Default to 10 recommendations if there's an error

        # Generate recommendations based on the product name
        content_based_rec = content_based_recommendations(train_data, prod, top_n=nbr)

        if content_based_rec.empty:
            message = "No recommendations available for this product."
            # Return an empty DataFrame to avoid the UndefinedError
            content_based_rec = pd.DataFrame()
            return render_template('main.html', message=message, content_based_rec=content_based_rec)  # Display message if no recommendations
        else:
            # Create a list of random image URLs for each recommended product
            random_product_image_urls = [random.choice(random_image_urls) for _ in range(len(content_based_rec))]
            return render_template('main.html', content_based_rec=content_based_rec, 
                                   random_product_image_urls=random_product_image_urls)  # Render recommendations with product images
    else:
        # If the request method is GET, return a default page or redirect
        return render_template('main.html', content_based_rec=pd.DataFrame())  # Render the main page with an empty recommendation list

# Run the Flask app in debug mode
if __name__=='__main__':
    app.run(debug=True)
