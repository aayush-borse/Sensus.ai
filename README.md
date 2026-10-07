Sensus AI: A Multilingual Chatbot for Dynamic Data Collection


 The Problem

Traditional, static survey forms are boring, impersonal, and often result in low response rates and poor data quality. They fail to capture the nuances of human feedback and are inaccessible to a large, non-English-speaking population.

 The Solution

**Sensus Ai**, is an end-to-end platform that modernizes data collection. We replace rigid forms with an intelligent, multilingual chatbot that engages users in a natural, conversational dialogue. Our system goes beyond simple data collection, using AI to deliver authentic, insightful data ready for analysis.

 Key Features

* **Multilingual Conversational Engine:** Our chatbot conducts surveys in a fluid, intuitive manner, with seamless support for multiple Indian languages via a free translation API (e.g., LibreTranslate). Users can respond with both text and voice.
* **Geo-Tagging for Authenticity:** Every survey response is automatically tagged with precise GPS coordinates, ensuring data integrity and preventing fraudulent entries.
* **AI-Powered Pattern Identification:** An intelligent analytics engine analyzes survey data to automatically detect trends, correlations, and hidden patterns that are easily missed with conventional analysis.
* **Automated Data Visualization:** The platform generates visual dashboards (bar charts, pie charts, heat maps) from raw data, providing policymakers and researchers with clear, actionable insights.

 Tech Stack

* **Frontend:** React Native (Expo)
* **Backend:** Node.js (Express), Python (for AI/ML models)
* **Database:** MongoDB
* **APIs:** LibreTranslate, Google Maps API (or similar)
* **Deployment:** (e.g., Vercel, Heroku, or a link to a live app)

 How to Run It Locally

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/aayush-borse/Sensus.Ai.git](https://github.com/aayush-borse/Sensus.Ai.git)
    cd Sensus.Ai
    ```

2.  **Set up the Backend:**
    ```bash
    cd backend
    npm install
    cp .env.example .env 
    # Open .env and add your API keys (e.g., database connection string, translation API key).
    npm start
    ```

3.  **Set up the Frontend:**
    ```bash
    cd ../frontend
    npm install
    npm start
    # Scan the QR code with the Expo Go app to view the app on your phone.
    ```

Future Scope

* Sentiment analysis of free-text responses.
* Integration with popular social media platforms.
* More advanced data visualization options.
* Support for a wider range of international languages.


**We believe that data collection should be a conversation, not a form.**
