if __name__ == "__main__":
    logger = get_logger()
    logger.info("Creating DB connection...")
    db = get_db()
    cursor = db.cursor()
    
    # Insert data into the database
    insert_query = "INSERT INTO users(email) VALUES (%s)"
    data = ("test@example.com",)
    cursor.execute(insert_query, data)
    db.commit()
    logger.info("Data inserted into the database.")
    
    cursor.execute("SELECT COUNT(*) FROM users;")
    for row in cursor:
        logger.info(row[0])
    cursor.close()
    db.close()
    logger.info("DB connection closed.")
