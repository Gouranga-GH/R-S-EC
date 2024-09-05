
# MyBay Shopping App - Product Recommendation System

This repository contains the implementation of a **content-based recommendation system** for a shopping web application named **MyBay**. The web application is developed using **Flask**, **SQLAlchemy** for database management, and various **machine learning** techniques for product recommendations. It also includes user authentication (sign-up/sign-in) and product exploration functionality.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Dataset](#dataset)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Exploring Recommendation Systems](#exploring-recommendation-systems)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

**MyBay** is a shopping platform that provides personalized product recommendations to users based on content similarity. This recommendation system is implemented using machine learning models that recommend products based on their tags and other features.

The project includes:
- User authentication with **Flask** and **SQLAlchemy**.
- Product search functionality.
- **Content-based recommendations** using **TF-IDF vectorization** and **Cosine Similarity**.
- Experimental implementation of other recommendation systems.

## Features

- **Content-Based Recommendation System**: Recommends products based on product tags, brand, and reviews.
- **User Sign Up/Sign In**: Secure user authentication using a MySQL database.
- **Randomized Trending Products**: Displays trending products on the homepage.
- **Product Modals**: Allows users to explore product details through modals.
- **Dynamic Product Display**: Displays recommended products based on a user’s search.

## Dataset

The recommendation system is based on product data stored in CSV files:
- `clean_data.csv`: Contains product information with tags for training the recommendation system.
- `rbr.csv`: Contains trending product information.
- `walmart_data.tsv`: Contains supplementary product data.

## System Architecture

### Backend:
- **Flask**: Handles routing, authentication, and recommendation generation.
- **SQLAlchemy**: Manages interactions with the MySQL database.
- **Machine Learning**: Uses `TfidfVectorizer` and `Cosine Similarity` for content-based recommendations.

### Frontend:
- **HTML** & **Bootstrap**: Provides a responsive user interface.
- **JavaScript**: Enhances the interactivity of the website (modal windows, themes).

### Database:
- **MySQL**: Stores user information (username, email, password).

## Installation

To run this project locally, follow these steps:

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/MyBay-Shopping-Recommendation.git
   cd MyBay-Shopping-Recommendation
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # For Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Configure your MySQL database and update the `app.config['SQLALCHEMY_DATABASE_URI']` in `app.py`.

4. Run the application:
   ```bash
   python app.py
   ```

5. Open your browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Running the Web Application
Once the server is running, you can explore the following features:
- **Homepage**: Shows trending products and provides a search bar for users to search for products in the next page.
- **Recommendations Page**: After searching for a product, recommendations based on similar content (tags) will be displayed.
- **User Authentication**: Users can sign up and sign in to the platform.

### Exploring Recommendation Systems
To experiment with different recommendation systems, you can explore the **Jupyter Notebook** `rs_ec.ipynb` located in the project directory. 

### Recommendation Systems Implemented in `rs_ec.ipynb`:
1. **Content-Based Recommendation**: Uses **TF-IDF Vectorizer** to recommend products based on similar tags.
2. **Collaborative Filtering (User-Based)**: Recommends products by analyzing user preferences and finding similar users.
4. **Rating-Based Recommendation**: Initial recommendations to the users based on top rated products.
5. **Hybrid Model**: Combines content-based filtering and collaborative filtering for better recommendations.

## Screenshots

### > Refer the "screenshots" folder


## License
This project is licensed under the MIT License. See the `LICENSE` file for more information.
