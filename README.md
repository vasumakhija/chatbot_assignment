#  TalentScout - Hiring Assistant Chatbot

A smart conversational AI built with **Streamlit** and **Groq's LLaMA 3 model** that simulates a hiring assistant. It collects candidate details, generates technical questions based on the candidate’s tech stack, gathers responses, and generates a downloadable PDF summary.

---

## Features

* Friendly conversation with candidates
* Collects name, contact info, experience, and tech stack
* Validates tech stack input using LLM
* Generates 5 custom interview questions
* Collects candidate answers
* Saves everything into `JSON` and exports a clean `PDF`

---

##  Get Your Groq API Key

To use this chatbot, you need an API key from Groq:

1. Go to =  [https://console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in
3. Click **"Create Key"** to generate your key
4. Copy it and keep it safe

Then set it in your environment:

```bash
export GROQ_API_KEY=your_api_key_here
```

---

##  Run Locally

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/chatbot_assignment.git
cd chatbot_assignment
```

### 2. Create a Virtual Environment

```bash
sudo apt install python3.12-venv  # Only once if needed
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirement.txt
```

### 4. Export Your Groq API Key

```bash
export GROQ_API_KEY=your_api_key_here
```

### 5. Run the Application

```bash
streamlit run 2.py
```

Then open your browser to `http://localhost:8501`

---

##  Deploying on AWS EC2 (Ubuntu)

### 1. Create EC2 Instance

* Go to AWS Console → EC2 → **Launch Instance**
* Choose Ubuntu (latest LTS)
* Choose t2.micro (Free Tier)
* Allow **SSH (port 22)** and **Custom TCP port 8501** (for Streamlit)

### 2. Connect via SSH

From your local machine:

```bash
ssh -i path_to_your_key.pem ubuntu@your-ec2-public-ip
```

### 3. Install System Dependencies

```bash
sudo apt update
sudo apt install git python3-pip python3.12-venv
```

### 4. Clone the Repo

```bash
git clone https://github.com/your-username/chatbot_assignment.git
cd chatbot_assignment
```

### 5. Set Up Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

### 6. Export Your Groq API Key

```bash
export GROQ_API_KEY=your_api_key_here
```

### 7. Run the Streamlit App

```bash
streamlit run 2.py --server.port 8501 --server.enableCORS false
```

Then go to `http://your-ec2-public-ip:8501` in your browser.

---

##  Prompt Design

* **GREETING**: Welcomes and explains bot's purpose
* **QUESTION\_GENERATION\_TEMPLATE**: LLM creates 5 technical questions
* **END\_PROMPT**: Gracefully ends chat on keywords like “bye”
* **Validation**: LLM checks if tech stack is valid

---

##  Technical Details

* **Frontend**: Streamlit
* **LLM Model**: LLaMA 3 via Groq API
* **PDF Generator**: FPDF
* **Data Storage**: JSON file (`candidates.json`)
* **Language**: Python 3.12

---

##  Challenges & Solutions

| Challenge                        | Solution                                           |
| -------------------------------- | -------------------------------------------------- |
| `pip3 install` blocked by system | Used `python3-venv` to create isolated environment |
| Invalid tech stack input         | Used Groq LLM to validate and re-prompt            |
| Short or vague answers           | Bot detects short responses and asks for more      |
| Data persistence                 | Saved user data to `JSON` and exported to `PDF`    |

---

##  Folder Structure

```
chatbot_assignment/
├── 2.py                      # Main Streamlit app
├── requirements.txt          # Python dependencies
├── candidates.json           # Stored candidate responses
├── candidate_summary.pdf     # Auto-generated summary
└── README.md                 # Project documentation
```

---

##  Author

Made with 💙 by a passionate developer using open source tools.

---
