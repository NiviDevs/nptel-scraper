# [Here!!](https://nptel-scraper.streamlit.app/)
<video src="https://github.com/user-attachments/assets/4a1b9d47-ff68-4b42-9b49-69ed8de872d4" autoplay loop muted playsinline width="100%">
  Your browser does not support the video tag.
</video>


cant write readmes so dont bother reading this slop :)

# NPTEL Course Stats Viewer 

A small Streamlit app that lets users search NPTEL courses and view basic course statistics with minimal friction.

The app loads a local JSON dataset of NPTEL courses, provides an search feature, and automatically fetches and displays statistics when a course is selected. No extra button clicks are required.

## Features

- Search for NPTEL courses
- Automatic stats fetching on course selection
- Simple, readable UI built with Streamlit
- Server-side caching to reduce repeated network calls

## Project Structure


├── app.py # Main Streamlit application

├── courses.json # Course metadata (id, title, institute, professor, etc.)

├── requirements.txt # Python dependencies

└── README.md

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   
3. Run the app:
  ```bash
streamlit run app.py
```

Contributing
If you find this useful, consider starring the repository on GitHub. It helps visibility and motivates further cleanup and features.

License
MIT
