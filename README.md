# Smart City Solutions: Real-Time Traffic and Air Quality Management

This repository hosts the code and documentation for a smart city prototype system designed to address air quality challenges arising from traffic congestion. By leveraging IoT technologies, public APIs, and advanced data analytics, this project provides actionable insights and proposes innovative solutions for urban environmental and traffic management.

---

## **Overview**

### **Key Objectives**
- Analyze the correlation between Air Quality Index (AQI) and traffic congestion.
- Propose a prototype system for real-time data collection, analysis, and actuation.
- Use predictive models to support proactive traffic and air quality management.

### **Key Features**
1. **Data Collection:**
   - AQI and traffic data collected in real time from OpenWeather and Google Maps APIs.
   - Data captured every 30 minutes over seven days from three key routes in London.

2. **Data Storage and Analysis:**
   - Data stored in Azure Cosmos DB for scalability and accessibility.
   - Analyzed using Python (Jupyter Notebook) and visualized with Google Looker Studio.

3. **Predictive Modeling:**
   - A linear regression model predicts traffic duration based on AQI, CO levels, and PM2.5 concentrations.

4. **Actuation Prototype:**
   - An ESP32 microcontroller triggers a dual-color LED indicator when AQI and traffic levels exceed thresholds.

---

## **System Architecture**

### **Steps**
1. **Data Acquisition:**  
   - Collect real-time AQI and traffic data using APIs.
   
2. **Data Storage:**  
   - Store collected data securely in Azure Cosmos DB in JSON format.
   
3. **Data Analysis:**  
   - Generate insights and visualizations using Python and Google Looker Studio.
   
4. **Actuation:**  
   - Use an ESP32 microcontroller to activate LED indicators based on data-driven thresholds.

---

## **Installation**

### **Prerequisites**
- Python 3.8 or higher.
- API keys for:
  - [OpenWeather API](https://openweathermap.org/api)
  - [Google Maps API](https://developers.google.com/maps/documentation)
- Azure Cosmos DB account for data storage.
- AWS EC2 instance for continuous script execution.

### **Steps**
1. Clone the repository:
   ```bash
   git clone https://github.com/siminali/iot_project.git
   cd iot_project
