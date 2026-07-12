"""
ARIA — Sample Interview Conversation Prompts
Use these prompts to test ARIA with different roles and companies.
Copy and paste these into the ARIA chat to simulate real interviews.
"""

# ============================================================
# PROMPT SET 1 — TCS Software Engineer (Fresher)
# ============================================================
TCS_SOFTWARE_ENGINEER = [
    # Step 1 - Onboarding
    "Hi ARIA, I want to prepare for my TCS interview.",

    # Step 2 - Profile details
    "My name is Rahul Sharma. I am applying for Software Engineer at TCS. "
    "I am a fresher. My skills are Python, Java, Data Structures, SQL, and OOP concepts. "
    "Target company is TCS.",

    # Step 3 - Confidence score
    "I would rate my confidence as 6 out of 10.",

    # Step 4 - Technical answers (sample)
    "A stack is a linear data structure that follows LIFO principle - "
    "Last In First Out. It supports push and pop operations.",

    "Object Oriented Programming has four pillars: Encapsulation, "
    "Inheritance, Polymorphism, and Abstraction.",

    "A primary key uniquely identifies each row in a table. "
    "A foreign key is a field that links two tables together.",

    "In Python, a list is mutable and ordered. "
    "A tuple is immutable and ordered. Lists use square brackets, tuples use parentheses.",

    "Binary search works by repeatedly dividing the search interval in half. "
    "It requires a sorted array and has O(log n) time complexity.",

    # Step 5 - HR answers
    "I am a passionate fresher with strong fundamentals in Python and Java. "
    "I completed my B.Tech in Computer Science and have worked on projects "
    "including a student management system and a weather app using APIs.",

    "My greatest strength is my ability to learn quickly and adapt to new technologies. "
    "My weakness is that I sometimes overthink problems, but I am working on it "
    "by setting time limits for decisions.",

    "I want to join TCS because it is one of India's leading IT companies "
    "with global presence, strong learning culture, and excellent growth opportunities.",

    # Step 6 - Situational answers
    "I would first understand the requirements clearly, break the problem into smaller tasks, "
    "write pseudocode, implement it, test edge cases, and document the solution.",

    "I would communicate with the team lead immediately, explain the situation honestly, "
    "prioritize the most critical tasks, and request an extension if needed.",

    # Final
    "Please give me my final report card.",
]


# ============================================================
# PROMPT SET 2 — Infosys Data Analyst (1-2 years experience)
# ============================================================
INFOSYS_DATA_ANALYST = [
    "Hello ARIA, I need to prepare for an Infosys Data Analyst interview.",

    "My name is Priya Nair. I am applying for Data Analyst at Infosys. "
    "I have 1 year of experience. My skills are Python, SQL, Excel, Power BI, "
    "Pandas, NumPy, and data visualization. Target company is Infosys.",

    "My confidence is 7 out of 10.",

    "Pandas is a Python library for data manipulation and analysis. "
    "It provides DataFrame and Series data structures for handling structured data.",

    "Inner join returns only matching rows from both tables. "
    "Left join returns all rows from left table and matching rows from right.",

    "I handle missing data by first identifying it using isnull(), "
    "then deciding whether to drop rows, fill with mean/median, "
    "or use forward fill depending on the context.",

    "A bar chart is used for categorical comparisons. "
    "A line chart shows trends over time. "
    "A scatter plot shows relationships between two variables.",

    "I would use GROUP BY with aggregate functions like COUNT, SUM, AVG "
    "to summarize data by categories in SQL.",

    "In my previous role I analyzed sales data to identify top performing products, "
    "created Power BI dashboards for management, and reduced reporting time by 40%.",

    "I am detail-oriented and have strong analytical thinking. "
    "I sometimes spend too much time perfecting visualizations, "
    "but I have learned to balance quality with deadlines.",

    "Infosys has a strong data analytics practice and I want to work on "
    "real business problems using data to drive decisions.",

    "I would validate the data source, check for duplicates, "
    "verify data types, and cross-check with the business team before analysis.",

    "I would present findings using simple visualizations, "
    "avoid technical jargon, and focus on business impact rather than methodology.",

    "Please generate my final report card.",
]


# ============================================================
# PROMPT SET 3 — Wipro ML Engineer (Fresher)
# ============================================================
WIPRO_ML_ENGINEER = [
    "Hi, I want to prepare for a Machine Learning Engineer interview at Wipro.",

    "My name is Arjun Patel. Role is ML Engineer at Wipro. "
    "I am a fresher. Skills: Python, Machine Learning, Deep Learning, "
    "TensorFlow, Scikit-learn, NumPy, Pandas. Target company is Wipro.",

    "Confidence score is 5 out of 10.",

    "Supervised learning uses labeled data to train models. "
    "Unsupervised learning finds patterns in unlabeled data. "
    "Examples: supervised - classification, regression. Unsupervised - clustering.",

    "Overfitting is when a model performs well on training data but poorly on test data. "
    "We can prevent it using regularization, dropout, cross-validation, or more data.",

    "A neural network consists of input layer, hidden layers, and output layer. "
    "Each layer has neurons connected by weights. Backpropagation updates weights "
    "using gradient descent to minimize loss.",

    "Precision is the ratio of true positives to all predicted positives. "
    "Recall is the ratio of true positives to all actual positives. "
    "F1 score is the harmonic mean of precision and recall.",

    "I built an image classification model using CNN in TensorFlow "
    "to classify handwritten digits from MNIST dataset with 98% accuracy.",

    "I am passionate about AI and eager to apply ML to real-world problems. "
    "I have strong fundamentals and hands-on project experience.",

    "My strength is strong mathematical foundation and coding skills. "
    "I am working on improving my communication skills in technical discussions.",

    "Wipro has strong AI/ML initiatives and I want to contribute to "
    "building intelligent systems that create business value.",

    "I would start with data collection, EDA, feature engineering, "
    "model selection, training, evaluation, and deployment with monitoring.",

    "I would explain the trade-off clearly - higher accuracy model may need "
    "more compute and cost. I would suggest starting with the simpler model "
    "and upgrading if business metrics justify it.",

    "Generate my ARIA final report card please.",
]


# ============================================================
# PROMPT SET 4 — Accenture Full Stack Developer (2-3 years)
# ============================================================
ACCENTURE_FULLSTACK = [
    "Hello ARIA, please prepare me for an Accenture Full Stack Developer interview.",

    "My name is Sneha Reddy. I am applying for Full Stack Developer at Accenture. "
    "I have 2 years of experience. Skills: React, Node.js, Python, FastAPI, "
    "MongoDB, SQL, REST APIs, Git, Docker. Target company is Accenture.",

    "7 out of 10 confidence.",

    "REST API uses HTTP methods - GET to retrieve, POST to create, "
    "PUT to update, DELETE to remove resources. It is stateless and uses JSON.",

    "React uses virtual DOM to efficiently update only changed elements. "
    "State management handles component data. Hooks like useState and useEffect "
    "manage state and side effects in functional components.",

    "SQL is structured, uses predefined schema, good for relational data. "
    "NoSQL like MongoDB is flexible schema, good for unstructured data and scalability.",

    "I use Git for version control - feature branches, pull requests, code reviews. "
    "CI/CD pipelines automate testing and deployment. Docker containers ensure "
    "consistent environments across dev and production.",

    "I built a full stack e-commerce platform with React frontend, "
    "FastAPI backend, MongoDB database, and JWT authentication.",

    "I am a quick learner with full stack expertise and strong problem solving skills. "
    "I sometimes take on too many tasks, but I have improved at prioritizing.",

    "Accenture works on large scale enterprise projects across domains. "
    "I want to build scalable solutions and grow as a technology consultant.",

    "I would analyze requirements, design system architecture, estimate timeline, "
    "break into sprints, implement with daily standups and regular client updates.",

    "I would implement Redis caching, database indexing, API pagination, "
    "CDN for static assets, and load balancing to handle high traffic.",

    "Give me my final report card.",
]


# ============================================================
# PROMPT SET 5 — Cognizant Python Developer (Fresher)
# ============================================================
COGNIZANT_PYTHON = [
    "Hi ARIA! I want to prepare for Cognizant Python Developer interview.",

    "My name is Karthik Menon. Role: Python Developer at Cognizant. "
    "Fresher. Skills: Python, Django, Flask, REST APIs, SQL, Git, Linux. "
    "Target company: Cognizant.",

    "My confidence is 6 out of 10.",

    "Python decorators are functions that modify behavior of other functions "
    "without changing their source code. They use @ symbol syntax.",

    "Django is a high-level full stack web framework with ORM, admin panel, "
    "and built-in authentication. Flask is a lightweight microframework "
    "giving more flexibility and control.",

    "A Python list is mutable ordered collection. Dictionary is key-value pairs "
    "with O(1) lookup. Set is unordered unique elements. Tuple is immutable ordered collection.",

    "I use try-except blocks to handle exceptions gracefully. "
    "I log errors, raise custom exceptions when needed, "
    "and always close resources in finally blocks.",

    "I built a REST API using Flask for a library management system "
    "with CRUD operations, JWT authentication, and SQLite database.",

    "I am detail-oriented, write clean code, and love problem solving. "
    "I am improving my knowledge of cloud technologies and DevOps practices.",

    "Cognizant has strong Python practices and a collaborative culture. "
    "I want to build impactful backend systems and grow into a senior developer.",

    "I would write unit tests first using pytest, use version control, "
    "do code reviews, follow PEP8 standards, and document all functions.",

    "I would analyze the bottleneck using profiling tools, "
    "optimize database queries, add caching, and use async processing if needed.",

    "Please generate my ARIA final interview report card.",
]


# ============================================================
# QUICK TEST PROMPTS — For rapid testing
# ============================================================
QUICK_TEST = {
    "start": "Hi ARIA",
    "profile": "I am Zoro, applying for TCS Software Engineer, fresher, skills Python and SQL, target TCS",
    "confidence": "7",
    "technical_answer": "Python is a high-level interpreted programming language known for simplicity and readability",
    "hr_answer": "I am passionate about technology and love solving complex problems",
    "situational_answer": "I would communicate with my team, prioritize tasks, and deliver the most critical features first",
    "end": "Give me my final report card",
}


if __name__ == "__main__":
    print("ARIA Sample Prompts Loaded Successfully!")
    print(f"Available prompt sets:")
    print("  - TCS_SOFTWARE_ENGINEER ({} prompts)".format(len(TCS_SOFTWARE_ENGINEER)))
    print("  - INFOSYS_DATA_ANALYST ({} prompts)".format(len(INFOSYS_DATA_ANALYST)))
    print("  - WIPRO_ML_ENGINEER ({} prompts)".format(len(WIPRO_ML_ENGINEER)))
    print("  - ACCENTURE_FULLSTACK ({} prompts)".format(len(ACCENTURE_FULLSTACK)))
    print("  - COGNIZANT_PYTHON ({} prompts)".format(len(COGNIZANT_PYTHON)))
    print("  - QUICK_TEST (rapid testing)")
