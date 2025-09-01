import cv2
import psycopg2
from datetime import datetime
import numpy as np
import os

# папка для изображений(созд автоматически если её нет)
os.makedirs('saved_frames', exist_ok=True)

conn = psycopg2.connect(
    dbname="photo",
    user="postgres",
    password="1234",
    host="localhost"
)
cursor = conn.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS photo (
    id SERIAL PRIMARY KEY,
    dob TIMESTAMP NOT NULL,
    name TEXT,
    image_path TEXT  
)
''')
conn.commit()

cap = cv2.VideoCapture("video.mp4")

cv2.namedWindow('Video', cv2.WINDOW_NORMAL)

frame_count = 0
while True:
    ret, photo = cap.read()
    if not ret:
        break

    cv2.imshow('Video', photo)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    frame_count += 1
    if frame_count % 50 == 0:
        # создаем уникальное имя файла
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f"frame_{frame_count}_{timestamp}.jpg"
        file_path = os.path.join('saved_frames', file_name)

        # сохраняем изображение на диск
        cv2.imwrite(file_path, photo)

        # сохраняем данные в бд
        cursor.execute(
            "INSERT INTO photo (dob, name, image_path) VALUES (%s, %s, %s)",
            (datetime.now(), file_name, file_path)
        )
        conn.commit()
        print(f"Saved frame {frame_count} as {file_path}")

cap.release()
cv2.destroyAllWindows()
conn.close()