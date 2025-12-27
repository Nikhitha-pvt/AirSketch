# 🎨 AirSketch  
### Hand Gesture–Based Virtual Drawing Application ✋🖌️

AirSketch is a real-time **touch-free drawing application** that allows users to draw on the screen using **hand gestures** detected via a webcam. Built using **MediaPipe** and **OpenCV**, this project transforms your index finger into a virtual pen, enabling intuitive and interactive air drawing without any physical input devices.

---

## 🚀 Features

- ✋ Draw in the air using your **index finger**
- 🌈 Multiple color options (Red, Green, Blue, Yellow)
- 🧽 Eraser mode for corrections
- 🗑️ Clear canvas option
- 🖐️ Real-time hand landmark visualization
- ⚡ Smooth and low-latency drawing
- 🖥️ Works with a standard webcam (no extra hardware)

---

## 🛠️ Technologies Used

- **Python**
- **OpenCV** – Video processing & UI rendering
- **MediaPipe Hands** – Real-time hand tracking
- **NumPy** – Canvas and image operations

---

## ⚙️ How It Works

1. Captures live video from the webcam.
2. Detects hand landmarks using MediaPipe.
3. Tracks the index finger tip position.
4. Draws continuous lines on a virtual canvas.
5. Uses on-screen buttons for color selection, erasing, and clearing.
6. Blends the canvas with live video for real-time interaction.

---

## 🖐️ Gesture Controls

| Gesture | Action |
|-------|--------|
| Move index finger | Draw on canvas |
| Touch color box | Change drawing color |
| Touch eraser box | Enable eraser |
| Touch clear box | Clear entire canvas |

---

## 📦 Installation

```bash
pip install -r requirements.txt
