## 💼 AI-Powered Job Recommendation Engine (2020)  

A **hybrid recommendation system** that combines **content-based filtering** with **collaborative filtering** from user-job interactions to deliver personalized and accurate job matches.  
Developed in **2020** as part of my professional work in recruitment technology.  

### 📌 Background & Problem  
Recruitment platforms often overwhelm users with irrelevant job postings.  
- **Content-based filtering alone** struggles to capture user preferences.  
- **Collaborative filtering alone** faces the **cold-start problem** for new users/jobs.  

### 🎯 Objectives  
- Deliver **personalized job matches** combining text similarity + user behavior.  
- Leverage **job description features** and **user interaction logs**.  
- Deploy as an **API service** for integration into job portals.  

### ⚙️ Solution Approach  
1. **Content-Based Filtering** → TF-IDF + Word2Vec embeddings for semantic similarity.  
2. **Collaborative Filtering** → User-job interaction matrix to recommend jobs applied/liked by similar users.  
3. **Hybrid Engine** → Blended scores from both approaches for robust recommendations.  
4. **Deployment** → Flask API serving recommendations per user.  

### 🛠️ Tech Stack  
- **ML/NLP:** scikit-learn (TF-IDF, cosine similarity), Word2Vec  
- **Backend:** Flask  
- **Language:** Python 3.x  

### 📊 Results & Impact  
- Reduced irrelevant job recommendations by **~35%**.  
- Improved overall **recommendation accuracy** vs. baseline content-only models.  
- Increased **user engagement** with the platform.  

### 🚀 Future Enhancements (if extended today)  
- Transformer-based embeddings (**BERT, Sentence-BERT**) for deeper semantic understanding.  
- Contextual signals → location, salary, skills gap.  
- Reinforcement learning for **adaptive recommendations**.  
- Cloud deployment for large-scale serving.  

### 📌 Note  
This project was completed in **2020** as part of my professional work.  
Due to confidentiality, **source code cannot be shared** — this write-up serves as a **case study** of my applied industry experience.  

---
