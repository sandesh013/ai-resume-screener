"""
Comprehensive skills database — technical, soft, certifications, and course mappings.
"""

TECHNICAL_SKILLS = {
    # Programming Languages
    "python","java","javascript","typescript","c++","c#","c","ruby","php",
    "swift","kotlin","go","rust","scala","r","matlab","perl","shell","bash",
    "powershell","sql","html","css","sass","less","dart","lua","haskell",
    "objective-c","assembly","vba","groovy","elixir","clojure","fortran",
    # Web Frameworks
    "react","angular","vue","vue.js","node.js","nodejs","express","express.js",
    "django","flask","fastapi","spring","spring boot","asp.net",".net","asp.net core",
    "ruby on rails","laravel","next.js","nuxt.js","svelte","gatsby","remix",
    "blazor","phoenix","gin","fiber","echo","actix","rocket",
    # Data Science & ML
    "machine learning","deep learning","tensorflow","pytorch","keras",
    "scikit-learn","pandas","numpy","matplotlib","seaborn","nlp",
    "natural language processing","computer vision","opencv","data analysis",
    "data science","data mining","big data","hadoop","spark","apache spark",
    "tableau","power bi","statistics","data visualization","jupyter",
    "hugging face","transformers","bert","gpt","llm","langchain","rag",
    "stable diffusion","generative ai","reinforcement learning","xgboost",
    "lightgbm","catboost","random forest","neural network","cnn","rnn","lstm",
    "gan","automl","mlflow","wandb","feature engineering","a/b testing",
    # Databases
    "mysql","postgresql","mongodb","redis","sqlite","oracle","sql server",
    "cassandra","dynamodb","firebase","elasticsearch","neo4j","mariadb",
    "cockroachdb","supabase","prisma","sequelize","typeorm",
    # Cloud & DevOps
    "aws","azure","gcp","google cloud","docker","kubernetes","jenkins",
    "terraform","ansible","ci/cd","devops","linux","nginx","apache",
    "heroku","vercel","netlify","cloudflare","github actions","gitlab ci",
    "circleci","prometheus","grafana","datadog","new relic","vagrant",
    "pulumi","helm","istio","envoy","serverless","lambda","cloud functions",
    # Tools
    "git","github","gitlab","bitbucket","jira","confluence","slack",
    "postman","swagger","rest api","graphql","grpc","microservices",
    "agile","scrum","kanban","unit testing","selenium","cypress","jest",
    "pytest","figma","adobe xd","webpack","vite","babel","eslint",
    "prettier","storybook","chromatic","npm","yarn","pip","conda",
    # Mobile
    "android","ios","react native","flutter","xamarin","ionic","swiftui",
    "jetpack compose","kotlin multiplatform",
    # Security
    "cybersecurity","penetration testing","ethical hacking","encryption",
    "oauth","jwt","ssl/tls","firewall","siem","owasp","sso","saml",
    # Emerging
    "blockchain","web3","solidity","smart contracts","iot","embedded systems",
    "robotics","ar/vr","unity","unreal engine","quantum computing","edge computing",
}

SOFT_SKILLS = {
    "communication","teamwork","leadership","problem solving","problem-solving",
    "critical thinking","creativity","adaptability","time management",
    "project management","collaboration","presentation","negotiation",
    "conflict resolution","decision making","decision-making","mentoring",
    "coaching","empathy","emotional intelligence","work ethic",
    "attention to detail","multitasking","self-motivated","self motivated",
    "analytical thinking","strategic thinking","innovation","flexibility",
    "interpersonal skills","organizational skills","verbal communication",
    "written communication","public speaking","customer service",
    "stakeholder management","team building","team management",
    "cross-functional collaboration","agile methodology","remote collaboration",
    "active listening","continuous learning","resilience","accountability",
}

CERTIFICATIONS = {
    "aws certified","aws solutions architect","aws developer","aws sysops",
    "azure certified","az-900","az-104","az-204","az-400",
    "google certified","gcp certified","google cloud professional",
    "comptia","comptia a+","comptia security+","comptia network+","comptia linux+",
    "cisco certified","ccna","ccnp","ccie",
    "pmp","prince2","itil","six sigma","lean six sigma",
    "certified scrum master","csm","safe","togaf","pmi-acp",
    "ceh","cissp","cisa","oscp","security+",
    "oracle certified","microsoft certified","salesforce certified",
    "tensorflow developer certificate","databricks certified",
    "kubernetes certified","cka","ckad","kcna",
    "machine learning specialization","deep learning specialization",
    "data engineering","solutions architect","meta frontend developer",
    "google data analytics","ibm data science","hashicorp certified",
}

COURSE_RECOMMENDATIONS = {
    "python": [
        {"name": "Python for Everybody", "platform": "Coursera", "url": "https://coursera.org/specializations/python"},
        {"name": "Complete Python Bootcamp", "platform": "Udemy", "url": "https://udemy.com"},
    ],
    "java": [
        {"name": "Java Programming Masterclass", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Java Specialization", "platform": "Coursera", "url": "https://coursera.org"},
    ],
    "javascript": [
        {"name": "The Complete JavaScript Course", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "JavaScript: The Hard Parts", "platform": "Frontend Masters", "url": "https://frontendmasters.com"},
    ],
    "react": [
        {"name": "React — The Complete Guide", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Full Stack Open", "platform": "Helsinki", "url": "https://fullstackopen.com"},
    ],
    "machine learning": [
        {"name": "Machine Learning Specialization", "platform": "Coursera (Andrew Ng)", "url": "https://coursera.org/specializations/machine-learning-introduction"},
        {"name": "Hands-On ML with Scikit-Learn", "platform": "O'Reilly (Book)", "url": "https://oreilly.com"},
    ],
    "deep learning": [
        {"name": "Deep Learning Specialization", "platform": "Coursera", "url": "https://coursera.org/specializations/deep-learning"},
        {"name": "Fast.ai Practical Deep Learning", "platform": "Fast.ai", "url": "https://course.fast.ai"},
    ],
    "data science": [
        {"name": "IBM Data Science Professional Certificate", "platform": "Coursera", "url": "https://coursera.org"},
        {"name": "Data Science Career Track", "platform": "DataCamp", "url": "https://datacamp.com"},
    ],
    "aws": [
        {"name": "AWS Cloud Practitioner Essentials", "platform": "AWS", "url": "https://aws.amazon.com/training"},
        {"name": "AWS Solutions Architect", "platform": "A Cloud Guru", "url": "https://acloudguru.com"},
    ],
    "docker": [
        {"name": "Docker Mastery", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Docker Getting Started", "platform": "Docker Docs", "url": "https://docs.docker.com/get-started"},
    ],
    "kubernetes": [
        {"name": "Kubernetes for Beginners", "platform": "KodeKloud", "url": "https://kodekloud.com"},
        {"name": "CKA Certification Course", "platform": "Udemy", "url": "https://udemy.com"},
    ],
    "sql": [
        {"name": "The Complete SQL Bootcamp", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "SQL for Data Science", "platform": "Coursera", "url": "https://coursera.org"},
    ],
    "django": [
        {"name": "Django for Beginners", "platform": "Book", "url": "https://djangoforbeginners.com"},
        {"name": "Django REST Framework Tutorial", "platform": "Official Docs", "url": "https://django-rest-framework.org"},
    ],
    "flask": [
        {"name": "Flask Mega-Tutorial", "platform": "Miguel Grinberg", "url": "https://blog.miguelgrinberg.com"},
        {"name": "Flask Web Development", "platform": "O'Reilly", "url": "https://oreilly.com"},
    ],
    "node.js": [
        {"name": "The Complete Node.js Course", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Node.js Design Patterns", "platform": "Book", "url": "https://nodejsdesignpatterns.com"},
    ],
    "angular": [
        {"name": "Angular — The Complete Guide", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Angular Official Tutorial", "platform": "Angular.io", "url": "https://angular.io/tutorial"},
    ],
    "vue": [
        {"name": "Vue.js 3 Complete Guide", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Vue Mastery", "platform": "Vue Mastery", "url": "https://vuemastery.com"},
    ],
    "tensorflow": [
        {"name": "TensorFlow Developer Certificate", "platform": "Coursera", "url": "https://coursera.org"},
        {"name": "TensorFlow Official Tutorials", "platform": "TensorFlow", "url": "https://tensorflow.org/tutorials"},
    ],
    "pytorch": [
        {"name": "PyTorch for Deep Learning", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "PyTorch Official Tutorials", "platform": "PyTorch", "url": "https://pytorch.org/tutorials"},
    ],
    "cybersecurity": [
        {"name": "CompTIA Security+", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "Google Cybersecurity Certificate", "platform": "Coursera", "url": "https://coursera.org"},
    ],
    "devops": [
        {"name": "DevOps Beginners to Advanced", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "The DevOps Handbook", "platform": "Book", "url": "https://itrevolution.com"},
    ],
    "git": [
        {"name": "Git & GitHub Crash Course", "platform": "Traversy Media", "url": "https://youtube.com"},
        {"name": "Pro Git Book", "platform": "Free", "url": "https://git-scm.com/book"},
    ],
    "typescript": [
        {"name": "Understanding TypeScript", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "TypeScript Handbook", "platform": "Official Docs", "url": "https://typescriptlang.org/docs"},
    ],
    "graphql": [
        {"name": "GraphQL with React", "platform": "Udemy", "url": "https://udemy.com"},
        {"name": "How to GraphQL", "platform": "Free Tutorial", "url": "https://howtographql.com"},
    ],
}