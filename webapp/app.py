from flask import Flask

# Create an instance of the Flask class
app = Flask(__name__)

# Define a route and a view function
@app.route('/')
def hello_world():
    return 'Flask environment is configured and running!'

# Run the app
if __name__ == '__main__':
    app.run(debug=True)