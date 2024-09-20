# register.py
import cv2
import face_recognition
import mysql.connector
from mysql.connector import Error
import sys

# รับค่า staffId จาก argument
staffId = int(sys.argv[1])
register = False

try:
    # Establish the database connection
    conn = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="",
        database="face_db"
    )
    if conn.is_connected():
        print("Connected to the database")

    # Open the video capture
    video_capture = cv2.VideoCapture(0)

    while True:
        ok, frame = video_capture.read()
        if not ok:
            print("Failed to capture image")
            break

        small_frame = cv2.resize(frame, (0, 0), fx=1 / 4, fy=1 / 4)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left * 4, top * 4), (right * 4, bottom * 4), (0, 0, 255), 2)
            if not register:
                register = True
                try:
                    # Get face data
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
                    face_data = face_encodings[0].tobytes()

                    # Insert faceData into the database
                    cursor = conn.cursor()
                    sql = "INSERT INTO faces (staffId, faceData) VALUES (%s, %s)"
                    cursor.execute(sql, (staffId, face_data))
                    conn.commit()
                    insert_id = cursor.lastrowid
                    print(f"Face registered with ID: {insert_id}")
                    # ส่งค่า ID กลับมาเพื่อให้ Express รับ
                    print(f"ID:{insert_id}")

                except Error as e:
                    print(f"Error inserting face data: {e}")
                finally:
                    cursor.close()

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Error as e:
    print(f"Database error: {e}")

finally:
    if conn.is_connected():
        conn.close()
        print("Database connection closed")
    video_capture.release()
    cv2.destroyAllWindows()
