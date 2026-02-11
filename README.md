# ArUco Marker PDF Generator

A web-based tool that generates printable PDF sheets of **ArUco markers**  with full layout customization and live preview.

This project includes:

* Python backend API (Flask)
* Web GUI frontend (HTML + JavaScript)
* Support for multiple marker types
* Configurable page layout and styling
* Local preview and optional cloud deployment

---

## 🚀 Features

### Marker Support

* ArUco Dictionaries:

  * DICT_4X4_50
  * DICT_5X5_100
  * DICT_6X6_250
  * DICT_7X7_100


### Layout & Customization

* Choose page size: **A4, A3, Letter**
* Set custom:

  * Marker size (mm)
  * Margins (mm)
  * Padding around markers (mm)
  * Spacing between markers (mm)
* Adjustable border:

  * Color
  * Thickness
* Input any list of marker IDs
* Live PDF preview in browser

---

## 📁 Project Structure

```
project/
 ├── app.py              # Flask backend
 ├── requirements.txt    # Python dependencies
 ├── index.html          # Web GUI
 ├── Procfile            # For Render deployment
 └── README.md           # This file
```

---

## 🛠 Local Installation

### 1. Clone or create project folder

```
git clone <your-repo-url>
cd project
```

### 2. Install Python dependencies

```
pip install -r requirements.txt
```

### 3. Run the backend server

```
python app.py
```

The API will start at:

```
http://localhost:5000
```

---

## 🌐 Running the GUI

Simply open `index.html` in your browser.

For best results, run a small local web server:

```
python -m http.server
```

Then open:

```
http://localhost:8000
```

---

## 📌 How to Use

1. Enter marker IDs (comma separated)
2. Choose:

   * Tag type (ArUco or AprilTag)
   * Dictionary / family
   * Page size
3. Adjust layout options
4. Click **Preview PDF**
5. PDF appears instantly in browser

---

## 🔧 API Usage

### Endpoint

```
POST /generate
```

### Example Request Body

```json
{
  "ids": [0,1,2,3],
  "marker_size": 70,
  "margin": 10,
  "padding": 5,
  "spacing": 10,
  "dictionary": "DICT_4X4_50",
  "page_size": "A4",
  "border_color": [180,180,180],
  "border_thickness": 0.1,
  "tag_type": "aruco"
}
```

### Response

* Returns a generated **PDF file** ready for printing.

---

## ☁️ Deployment to Render

1. Push this project to GitHub
2. On Render, create a new **Web Service**
3. Use settings:

* Build Command:

  ```
  pip install -r requirements.txt
  ```
* Start Command:

  ```
  gunicorn app:app
  ```

4. Update the GUI `fetch` URL to your Render endpoint

---

## 📦 Requirements

```
flask
flask-cors
opencv-python-headless
fpdf
apriltag
gunicorn
```

---

## 📝 Notes

* Designed for printing at **actual size**
* Works fully offline when running locally
* Free tier Render deployments may sleep after inactivity

---

## 📄 License

Free to use and modify for personal and educational purposes.

---

### Enjoy generating markers! 🚀

