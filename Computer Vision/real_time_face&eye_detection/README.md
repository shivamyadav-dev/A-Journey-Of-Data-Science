# Real-Time Face & Eye Detection 👁️👁️

A simple yet powerful **Real-Time Face & Eye Detection** project built using **Python** and **OpenCV**.  
This project captures video from your webcam and detects human faces and eyes using **Haar Cascade Classifiers**.

---

## 🚀 Features

- Real-time face detection  
- Real-time eye detection  
- Uses classic Haar Cascade algorithms  
- Works directly with your system webcam  
- Efficient detection using Regions of Interest (ROI)

---


---

## 🧠 How It Works

1. **Load Haar Cascade Models**  
   Pre-trained XML classifiers for face and eye detection are loaded.

2. **Access Webcam**  
   The program initializes the system webcam using:
   ```python
   cv2.VideoCapture(0)
   ```

3. **Frame-by-Frame Processing**  
   - Convert each frame to grayscale  
   - Detect faces  
   - Within each detected face, detect eyes  
   - Draw rectangles over detected regions  

4. **Exit Mechanism**  
   Press **'q'** anytime to stop the video feed safely.

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV (cv2)**
- **Haar Cascade Classifier**

---

## ▶️ How to Run

### **1. Install Dependencies**
```bash
pip install opencv-python
```

### **2. Download Haar Cascade Files**
Download the required XML files from OpenCV GitHub:
- `haarcascade_frontalface_default.xml`
- `haarcascade_eye.xml`

Place them in a folder and update the paths inside `face_eye_detection.py`.

### **3. Run the Script**
```bash
python face_eye_detection.py
```

---

## 📸 Demo Output

- Blue rectangles → **Faces**  
- Green rectangles → **Eyes**

---

## 📄 License

This project is open-source. Feel free to use or modify it for learning and development.

---

## 🙌 Acknowledgements

- OpenCV Team  
- Haar Cascade Algorithm  
- Inspiration from classic Computer Vision techniques  

---

Happy Coding! ✨  
