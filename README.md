#  Honeypot Setup – Cybersecurity Project

##  Introduction
The Honeypot Setup Project is a cybersecurity-based system designed to simulate a vulnerable environment that attracts attackers and records their activities.

A honeypot acts as a decoy system, allowing security professionals to observe malicious behavior without risking real systems. This project demonstrates how attackers attempt unauthorized access and how such activities can be monitored.

---

##  Project Objective
The main objectives of this project are:

- To design a fake login system to trap attackers  
- To capture unauthorized access attempts  
- To log username, password, IP address, and time  
- To analyze attacker behavior  
- To understand real-world cybersecurity concepts  

---

##  Key Features

- Fake Login Interface  
- Connection Monitoring  
- Credential Logging  
- IP Address Tracking  
- Timestamp Recording  
- Log File Storage  
- Lightweight and beginner-friendly  

---

##  Technologies Used

- Python 3  
- Socket Programming  
- File Handling  

---

##  Project Structure

honeypot-setup/
│── honeypot.py          # Main honeypot script  
│── honeypot_log.txt     # Stores attacker data  
│── README.md            # Documentation  

---

##  Installation & Setup

### 1. Clone the Repository
git clone https://github.com/Koushi-j/honeypot.git  
cd honeypot  

### 2. Run the Honeypot
python honeypot.py  

---

##  Working Procedure

1. The honeypot starts and listens for incoming connections  
2. A fake login prompt is shown to the user  
3. The attacker enters credentials  
4. The system captures:
   - Username  
   - Password  
   - IP Address  
   - Timestamp  
5. Data is stored in honeypot_log.txt  

---

##  Sample Log Output

[12:01:22] Connection from 192.168.1.10  
[12:01:30] Username: admin  
[12:01:32] Password: 123456  
[12:01:40] Login attempt recorded  

---

##  Applications

- Cybersecurity learning  
- Ethical hacking practice  
- Network monitoring basics  
- Academic mini projects  

---

##  Limitations

- Basic implementation  
- Not production-level  
- No advanced intrusion detection  
- Works in controlled environment only  

---

##  Future Enhancements

- Web-based dashboard  
- IP location tracking  
- Real-time alerts  
- Cloud deployment  
- Advanced logging system  

---

##  Disclaimer

This project is for educational purposes only.  
Do not use it for illegal or unauthorized activities.

---

##  Author

Koushik  
Cybersecurity Enthusiast  

GitHub: https://github.com/Koushi-j  

---

##  Support

If you like this project:
- Star the repository  
- Fork it  
- Share with others  
