import cv2
import face_recognition
import mysql.connector
import numpy as np
from datetime import datetime
import time

# เชื่อมต่อกับฐานข้อมูล
conn = mysql.connector.connect( 
    host="localhost",
    port=3306,
    user="root",
    password="",
    database="face_db"
)

# 1. โหลดข้อมูลใบหน้าทั้งหมด
cursor = conn.cursor(dictionary=True)
cursor.execute('''
SELECT f.staffId, s.displayName name, f.id faceId, f.faceData 
FROM staffs s
  JOIN faces f ON f.staffId=s.id''')
faces = cursor.fetchall()
all_faces = [np.frombuffer(face["faceData"], dtype=np.float64) for face in faces]
print("Face data loading complete.")

video_capture = cv2.VideoCapture(0)
print("Camera ready")

notification_duration = 2  # ระยะเวลาการแสดงข้อความ (หน่วย: วินาที)

while True:
    ok, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=1 / 4, fy=1 / 4)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_small_frame)

    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        face_distances = face_recognition.face_distance(all_faces, face_encoding)
        min_index = np.argmin(face_distances)
        name = faces[min_index]["name"]
        staff_id = faces[min_index]["staffId"]
        
        # ตรวจสอบว่ามีการเช็คชื่อในวันนี้หรือยัง
        today = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT * FROM users WHERE staffId = %s AND DATE(timestamp) = %s
        ''', (staff_id, today))
        attendance = cursor.fetchone()

        top, right, bottom, left = face_location

        # แสดงชื่อที่ตำแหน่งบนใบหน้าเสมอ
        name_position = (left * 4, top * 4 - 10)  # แสดงชื่อตรงใบหน้า
        cv2.putText(frame, name, name_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        if attendance:
            # ถ้ามีการเช็คชื่อแล้ว จะแสดงข้อความว่า "You checked." ที่ด้านขวาบน
            notification_text = "You checked."
            text_position = (frame.shape[1] - 250, 50)  # ด้านขวาบน
            cv2.putText(frame, notification_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        else:
            # บันทึกข้อมูลการเช็คชื่อ (ชื่อและเวลา) ลงในตาราง users
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO users (staffId, name, timestamp) VALUES (%s, %s, %s)
            ''', (staff_id, name, timestamp))
            conn.commit()  # บันทึกข้อมูลลงในฐานข้อมูล
            
            # แสดงข้อความว่า "Check-in successful" ที่ด้านขวาบน
            notification_text = "Check-in successful"
            text_position = (frame.shape[1] - 250, 50)  # ด้านขวาบน
            cv2.putText(frame, notification_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # แสดงข้อความเป็นเวลา notification_duration วินาที
            cv2.imshow('Video', frame)
            cv2.waitKey(1)
            time.sleep(notification_duration)  # ทำให้ข้อความค้างอยู่

    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

# ปิดการเชื่อมต่อฐานข้อมูล
cursor.close()
conn.close()