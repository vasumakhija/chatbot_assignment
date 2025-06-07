# TalentScout - Hiring Assistant Chatbot

A smart conversational AI built with Streamlit and Groq's LLaMA 3 model that simulates a hiring assistant. It collects candidate details, generates technical questions based on the candidate’s tech stack, gathers responses, performs sentiment analysis, supports multiple languages, and generates a downloadable PDF summary.

---

##  Features

*  Friendly conversation with candidates
*  Collects name, contact info, experience, and tech stack
*  Validates tech stack input using LLM
* \2753 Generates 5 custom interview questions
*  Collects candidate answers
*  Saves everything into JSON
*  Exports a clean PDF summary
*  **Integrates sentiment analysis** to gauge candidate emotions during the conversation
*  **Implements multilingual support** to interact with candidates in different languages

---

## 🔑 Get Your Groq API Key

To use this chatbot, you need an API key from Groq:

1. Visit: [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Click **"Create Key"**
4. Copy the key and store it safely

Then export it in your environment:

```bash
export GROQ_API_KEY=your_api_key_here
```

---

## 🖥️ Run Locally

1. **Clone the Repository**

```bash
git clone https://github.com/your-username/chatbot_assignment.git
cd chatbot_assignment
```

2. **Create a Virtual Environment**

```bash
sudo apt install python3.12-venv  # If not already installed
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set the Groq API Key**

```bash
export GROQ_API_KEY=your_api_key_here
```

5. **Run the Application**

```bash
streamlit run 2.py
```

Open your browser at: [http://localhost:8501](http://localhost:8501)

---

##  Deploying on AWS EC2 (Ubuntu)

1. **Create EC2 Instance**

   * Choose Ubuntu LTS
   * Instance type: `t2.micro` (Free Tier)
   * Open ports: `22` (SSH), `8501` (Streamlit)

2. **SSH into the Instance**

```bash
ssh -i path_to_your_key.pem ubuntu@your-ec2-public-ip
```

3. **Install System Dependencies**

```bash
sudo apt update
sudo apt install git python3-pip python3.12-venv
```

4. **Clone the Repo & Set Up**

```bash
git clone https://github.com/your-username/chatbot_assignment.git
cd chatbot_assignment
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

5. **Set API Key**

```bash
export GROQ_API_KEY=your_api_key_here
```

6. **Run Streamlit App**

```bash
streamlit run 2.py --server.port 8501 --server.enableCORS false
```

Visit: `http://your-ec2-public-ip:8501`

---

##  Prompt Design

* **GREETING:** Welcomes and explains bot's purpose
* **QUESTION\_GENERATION\_TEMPLATE:** LLM creates 5 technical questions
* **END\_PROMPT:** Gracefully ends chat on "bye", "thank you", etc.
* **Validation:** Uses LLM to check tech stack and ask again if invalid
* **Sentiment Analysis:** Evaluates tone/emotion of candidate replies
* **Multilingual Support:** Adjusts language model response dynamically

---

## 🔧 Technical Details

| Component      | Tech Used                                |
| -------------- | ---------------------------------------- |
| Frontend       | Streamlit                                |
| LLM Model      | LLaMA 3 via Groq API                     |
| PDF Generator  | FPDF                                     |
| Data Storage   | JSON (`candidates.json`)                 |
| Language       | Python 3.12                              |
| Extra Features | Sentiment Analysis, Multilingual Support |

---

## 🛠️ Challenges & Solutions

| Challenge                     | Solution                                   |
| ----------------------------- | ------------------------------------------ |
| `pip3 install` blocked/system | Used `python3-venv` to isolate environment |
| Invalid tech stack input      | Used LLM to validate and re-prompt         |
| Short or vague answers        | Bot follows up to request clarity          |
| Emotional insight             | Integrated sentiment detection from text   |
| Language limitations          | Added multilingual capabilities with LLM   |
| Data persistence              | Saved all data to JSON and PDF             |

---

## 📁 Folder Structure

```
chatbot_assignment/
├── 2.py                   # Main Streamlit app
├── requirement.txt        # Python dependencies
├── candidates.json        # Stored candidate responses
├── candidate_summary.pdf  # Auto-generated summary
└── README.md              # Project documentation
```

---

## ✍️ Author

Made with 💙 by a passionate developer using open source tools.

---
