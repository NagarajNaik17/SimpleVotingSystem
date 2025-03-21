# 🗳️ **Voting System**  

## 🎉 _Welcome to the Simple Voting System project!_
This is a **basic web-based voting system** built using *Python, HTML, and CSS*. It allows an **Admin** to set up candidates and their logos, while **Users** can vote for their preferred candidates after signing up and logging in. ✅ Each user can vote *only once*!

This project is **perfect for beginners** to understand how to create a *simple web application* with **user authentication and database integration**. 🚀

---
## ✨ **Features**

### 🔑 **Admin Panel:**
- ➕ *Add candidates* with their details *(name, logo, etc.)*.
- 🛠️ *Manage the voting process*.

### 👤 **User Panel:**
- 📝 *Sign up and log in* to vote.
- 🗳️ *Vote for a candidate* (**one vote per user**).

### 🗄️ **Database:**
- 🛢️ *MySQL database* to store **user and candidate information**.

---
## 🛠️ **Setup Instructions**

### **1️⃣ Database Setup**
📌 Follow the steps in the `voting_system.sql` file to set up the **MySQL database**.
📌 Ensure you have **MySQL installed and running** on your system.

### **2️⃣ Clone the Repository**
```bash
 git clone https://github.com/your-username/voting-system.git
 cd voting-system
```

### **3️⃣ Install Dependencies**
💻 Make sure you have **Python installed**. Then, install the required Python libraries:
```bash
pip install -r requirements.txt
```

### **4️⃣ Configure Database Connection**
📝 Update the database connection details in the `app.py` file:
```python
DB_HOST = 'localhost'
DB_USER = 'your_username'
DB_PASSWORD = 'your_password'
DB_NAME = 'voting_system'
```

### **5️⃣ Run the Application**
🚀 Start the **Flask server**:
```bash
python app.py
```
🌐 Visit **http://127.0.0.1:5000** in your browser to access the voting system.

```bash
use 12345 as officer id
password as officer password
```

---
## 🤝 **How to Contribute**
💡 We welcome **contributions** to improve this project! Here are some ideas:

### 📧 **Gmail Authentication:**
- 🔑 Implement *Gmail authentication* for users to create passwords during signup.

### 🎨 **Better Interface:**
- ✨ Improve the *UI/UX* with **modern design elements** and responsive layouts.

### 🔢 **Additional Features:**
- ✅ Add **vote counting** and result display.
- 📩 Implement **email notifications** for users after voting.

---
## 📥 **How to Pull the Code**
To pull the latest changes from the repository:
```bash
git pull origin main
```

Result
![image](https://github.com/user-attachments/assets/83c2d35f-6f15-4ad4-a089-3da716ca7c2b)


---
## 🚀 **Future Enhancements**
💡 Some planned **future improvements**:
- 🔓 *Add a forgot password feature.*
- 📊 *Implement real-time vote tracking.*
- 📈 *Add admin analytics to view voting trends.*

---
## 🌟 **Let's Build Together!**
🛠️ Feel free to **fork this repository**, make changes, and submit pull requests. Let's make this **voting system even better!** 🚀

🎉 **Happy Voting!** 🗳️

