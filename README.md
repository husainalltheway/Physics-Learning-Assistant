
# **PhysicsLearningAssistant**

**PhysicsLearningAssistant** is an interactive educational platform designed to support students in their physics studies. This project serves as a comprehensive digital learning tool, combining a vast database of physics resources with an intelligent query system.

## **Key Features**:

- Extensive database of physics books and resources
- Interactive query system for addressing student doubts and questions
- Explanation engine for complex physics concepts
- Problem-solving assistance for numerical questions
- Personalized study guide generation

PhysicsLearningAssistant aims to be a one-stop solution for students seeking to enhance their understanding of physics, providing on-demand access to knowledge and problem-solving support.

---

## **Getting Started**

These instructions will help you set up the project on your local machine.

### **Prerequisites**

- Python (version `^3.12`)

---

### **Installation**

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/yourproject.git
   cd yourproject
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:

   On **Windows**:
   ```bash
   venv\Scripts\activate
   ```

   On **macOS and Linux**:
   ```bash
   source venv/bin/activate
   ```

4. **Install dependencies**:
   ```bash
   poetry install
   ```

---

## **Usage**

1. **Provide your credentials**:

   - Add your Hugging Face token in the `.env` file
   - Add the LLaMA cloud URL and token for parsing files in the `.env` file
   - Add the Qdrant URL and API token for creating collections and retrieving data in `qdrant_ops.py` and `rag_op.py` located inside the `physics_learning_assistant` folder

2. **To parse data for the first time**:

   - Once all the tokens are provided:
     - Put the chapter-wise or topic-wise PDF files inside the `books` folder
     - Run the `data_extract.py` file inside the `physics_learning_assistant` folder to parse, embed, and create a JSON file from the data.

3. **Store data in Qdrant**:

   - By now, you will have JSON files inside the `json_output` folder
   - Simply run the `qdrant_ops.py` file inside the `physics_learning_assistant` folder to store data in Qdrant

4. **Run the app**:

   - By now, your parsed data will be stored in the Qdrant vector database
   - Run the app using the command: 
     ```bash
     streamlit run app.py
     ```
   - On the web page, select the subject and chapter, and you can start querying.

---
