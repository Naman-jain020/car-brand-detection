# Car Brand Detection System 🚗

A complete end-to-end Python web application that scrapes car images from the web, classifies them by brand using a deep learning model, and instantly visualizes the top brands in an interactive dashboard.

---

## 🚀 Features

- **Automated Image Scraping:**  
  Fetches real-world car images from online sources like Flickr with a single click.

- **Deep Learning Brand Recognition:**  
  Classifies each image by car brand using a machine learning model built with PyTorch.

- **Live Data Visualization:**  
  Instantly displays a bar chart of the most-detected car brands via a sleek Flask web dashboard.

- **Fully Integrated Workflow:**  
  The “Start” button triggers scraping, classification, and visualization, making the process seamless even for non-coders.

---

## 📦 Installation

Clone the project
git clone https://github.com/yourusername/car-brand-detection.git cd car-brand-detection
(Optional) Create and activate a virtual environment
python3 -m venv env source env/bin/activate    # On Windows: env\Scripts\activate
Install dependencies
pip install -r requirements.txt

---

## 🛠️ Usage

1. **(First, add your trained model):**  
   Place your file `car_brand_classifier.pt` in the `model/` folder.

2. **Start the application:**
    ```
    python run.py
    ```

3. **Open the dashboard in your browser:**  
   Visit [http://localhost:5000/](http://localhost:5000/)  
   Click "Start" to run the pipeline and view the results!

---

## 🧰 Requirements

- Python 3.7+
- Flask
- PyTorch & torchvision
- matplotlib
- requests
- beautifulsoup4
- Pillow
- (Optional, for dynamic scraping): selenium, chromedriver

All dependencies are specified in `requirements.txt`.

---

## 📁 Project Structure

<img width="263" height="432" alt="Screenshot 2025-09-13 at 1 54 16 AM" src="https://github.com/user-attachments/assets/0a5ec450-b64c-4140-b0e7-be9fb8d2d5e5" />


---

## ⚙️ How It Works

1. **Scrape:** Collects car photos from your chosen web group (like Flickr).
2. **Predict:** Applies a deep learning model to classify each image by car brand.
3. **Visualize:** Displays the top brands in a bar chart on the web dashboard.

---

## ✏️ Customization Tips

- **Change image source:**  
  Modify the source URL in `app/scraper.py`.
- **Update supported brands/model:**  
  Edit `app/predictor.py` to match your brand list and trained weights.
- **Adjust chart:**  
  Change bar chart appearance in `visualize/plot.py`.

---

## 📄 License

This project is open-source and free to use under the [MIT License](LICENSE).

---

## 🙋‍♂️ Questions or Contributions?

Open an issue or submit a pull request!  
Happy hacking!


