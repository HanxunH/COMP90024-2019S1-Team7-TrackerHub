# CCC Group 7 
Team Members:

Hanxun Huang - 975781  
Haonan Chen - 930614  
Lihuan Zhang - 945003  
Xu Wang - 979895  
Yang Xu - 961717  

## Video links
### Ansible
Part 1: https://youtu.be/2shxCohju8Q  
Part 2: https://youtu.be/JHfxmtzU_g4  
Part 3: https://youtu.be/pWH7eOh666s  

### Frontend presentation
https://youtu.be/M5xhnEHwKNg

### PPT
https://docs.google.com/presentation/d/1Qh8GSjCTdOJmY1ZWcf8TvxqVexH1DuxgqklMqmUXJvs/edit#slide=id.g5173a8b583_0_62

## Project Structure

### FrontEnd 
1. Vue
2. Data visualization
3. Interface joint debugging

### BackEnd
1. Django(8080) -> Nginx reverse proxy port 80 /api
2. CouchDB related interface
3. Object Storage interface
4. Data query interface
5. Interface joint debugging

### Spider
1. Apply for the Twitter Developer API
2. Run the script continuously
   1. Grab data
   2. Data preprocessing
   3. Image preprocessing
   4. Save the image to Object Storage (call backend interface)
   5. Twitter content is stored in the first level of CouchDB (call backend interface)

### Natural Language Processing
1. Model and metrics: Wu-Palmer similarity, NLTK, Profanity, TextBlob
   1. Implement Wu-Palmer similarity on Wordnet to identify the sexual-suggestion message in tweet text
   2. Use Profanity package to identify the violent message in tweet text
   3. Use TextBlob to identify the sentiment of the tweet text
2. Run the script periodically (once per 30mins)
   1. Grab data from backend
   2. Tokenization of tweet text 
   3. Implement three kinds of analytics on each tweet
   4. Upload the result to the second level CouchDB (call backend interface)


### Machine Learning
1. Select model: NSFW, Food Identification
2. Train model
3. Run the script periodically (once per 30mins)
   1. Scan the first level CouchDB (call backend interface)
   2. Retrive pictures from the back end
   3. Image Classification
   4. Upload the result to the second level CouchDB (call backend interface)

### Deployment Operation 
1. Ansible creates 4 hosts with one click
2. Docker runs 3 CouchDB instances
3. Ansible controls Docker-compose with services on each instances 

### Server Arrangement

Server1: 172.26.37.225
    
    CouchDB/ couchdb:2.3.0
    Frontend/
    Nginx/ nginx:lastest
    CAdvisor/


Server2: 172.26.38.110
    
    CouchDB/couchdb:2.3.0
    Backend/ lihuanz/my-backend:lastest
    Spider/ 
    CAdvisor/


Server3: 172.26.38.1
    
    CouchDB/couchdb:2.3.0
    Backend/
    NLP/
    CAdvisor/


Server4: 172.26.38.11

    MachineLearning/
    Grafana/ grafana/grafana:lastest
    InfluxDB/ influxdb:lastest
    cAdvisor/ google/cadvisor:lastest


   
   
