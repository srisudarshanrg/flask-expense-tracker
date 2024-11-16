from expense_tracker import app, db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(port=9000, debug=True)