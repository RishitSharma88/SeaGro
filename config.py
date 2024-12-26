from app import app

app.config['SECRET_KEY'] = "MY SECRET"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///SeaGro.db'  # SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking