# CCC Group 7 

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
2. Run the script regularly（30min?）
   1. Grab data
   2. Data preprocessing
   3. Image preprocessing
   4. Save the image to Object Storage (call backend interface)
   5. Twitter content is stored in the first level of CouchDB (call backend interface)

### Machine Learning
1. Select model: NSFW, Food Identification
2. Train model
3. Run the script regularly (30min?)
   1. Scan the first level CouchDB (call backend interface)
   2. Retrive pictures from the back end
   3. Image Classification
   4. Upload the result to the second level CouchDB (call backend interface)

### Hadoop and Operation 
1. Ansible creates 4 hosts with one click
2. Docker runs 3 CouchDB instances

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


   
   
