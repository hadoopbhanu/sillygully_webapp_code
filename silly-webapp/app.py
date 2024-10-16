from flask import Flask, render_template_string
import pymysql
import os

app = Flask(__name__)

# Configure database connection parameters
db_user = os.environ.get('DB_USER')
db_password = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_host = os.environ.get('DB_HOST')  # Usually '127.0.0.1' when using Cloud SQL Auth Proxy

# Dictionary mapping regions to flag colors
country_colors = {
    'Indian': '#FF9933',       # Saffron
    'Mexican': '#006847',      # ForestGreen
    'Thai': '#DC143C',         # Crimson
    'Italian': '#808000',      # Olive
    'Chinese': '#FF0000',      # Red
    'Japanese': '#FFFFFF',     # White
    'Moroccan': '#8B0000',     # DarkRed
    'French': '#4169E1',       # RoyalBlue
    'Korean': '#87CEEB',       # SkyBlue
    'Spanish': '#FFFF00',      # Yellow
    'Ethiopian': '#FFD700',    # Gold
    'Turkish': '#00CED1',      # DarkTurquoise
    'Lebanese': '#008000',     # Green
    'Greek': '#1E90FF',        # DodgerBlue
    'Brazilian': '#32CD32',    # LimeGreen
    'Vietnamese': '#FF6347',   # Tomato
    'Russian': '#4682B4',      # SteelBlue
    'Peruvian': '#B22222',     # FireBrick
    'Indonesian': '#BC8F8F',   # RosyBrown
    'Caribbean': '#3CB371',    # MediumSeaGreen
    'Egyptian': '#F4A460',     # SandyBrown
    'Argentinian': '#87CEEB',  # SkyBlue
    'Pakistani': '#556B2F',    # DarkOliveGreen
    'American': '#000080',     # Navy
    'Iranian': '#2F4F4F',      # DarkSlateGray
    'Nepalese': '#9370DB',     # MediumPurple
    'Afghan': '#800000',       # Maroon
    'German': '#00FFFF',       # Cyan
    'Polish': '#DC143C',       # Crimson
    'Kenyan': '#006400',       # DarkGreen
    'Sri Lankan': '#8B4513',   # SaddleBrown
    'Portuguese': '#B22222',   # FireBrick
    'Syrian': '#708090',       # SlateGray
    'Cambodian': '#8B008B',    # DarkMagenta
    'Hungarian': '#98FB98',    # PaleGreen
    'Jamaican': '#B8860B',     # DarkGoldenRod
    'South African': '#66CDAA',# MediumAquamarine
    'Bangladeshi': '#8B0000',  # DarkRed
    'Philippine': '#4169E1',   # RoyalBlue
    'Chilean': '#B22222',      # FireBrick
    'Finnish': '#6495ED',      # CornflowerBlue
    'Nigerian': '#008000',     # Green
    'Swiss': '#FF0000',        # Red
    'Australian': '#0000CD',   # MediumBlue
    'Mongolian': '#DC143C',    # Crimson
    'Belgian': '#FFD700',      # Gold
    'Burmese': '#DAA520',      # GoldenRod
    'Serbian': '#1E90FF',      # DodgerBlue
    'Uzbek': '#40E0D0',        # Turquoise
}

# Function to get a database connection
def get_db_connection():
    connection = pymysql.connect(
        user=db_user,
        password=db_password,
        host=db_host,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection

@app.route('/')
def index():
    try:
        # Connect to the database
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Execute a query to select all data from the cuisine_spices table
            cursor.execute("SELECT * FROM cuisine_spices")
            # Fetch all results
            rows = cursor.fetchall()
        
        # HTML template to display data with country colors
        html_template = """
        <!doctype html>
        <html>
            <head>
                <title>Data from Cloud SQL</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        text-align: center;
                        margin: 0;
                        padding: 0;
                    }
                    table {
                        margin: 50px auto;
                        border-collapse: collapse;
                        width: 80%;
                        max-width: 1000px;
                        background-color: #fff;
                    }
                    th, td {
                        padding: 12px;
                        border: 1px solid #ddd;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h1>Data from Cloud SQL</h1>
                <table border="1">
                    <tr>
                        {% for column in rows[0].keys() %}
                        <th>{{ column }}</th>
                        {% endfor %}
                    </tr>
                    {% for row in rows %}
                    <tr style="background-color: {{ country_colors.get(row['cuisine_name'], '#FFFFFF') }}">
                        {% for column, value in row.items() %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </table>
            </body>
        </html>
        """
        
        return render_template_string(html_template, rows=rows, country_colors=country_colors)
    
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
