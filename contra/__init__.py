# Import the Flask framework and the blueprints for different routes
from flask import Flask
import contra.routes.home as home
import contra.routes.connections as connections
import contra.routes.cb as callback

# Create a Flask application instance
app = Flask(__name__)

# Register the blueprints for different routes
app.register_blueprint(home.home_bp)
app.register_blueprint(connections.conn_bp)
app.register_blueprint(callback.callback_bp)

# Start the Flask application
if __name__ == '__main__':
    app.run(debug=True)