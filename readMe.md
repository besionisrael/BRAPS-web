# Blockchain-Based Public Services Platform

A blockchain-powered web application developed using Django Framework for digitizing public services. The project implements three distinct applications (one for each organization) within a single project.

## Project Structure

The "Ulink-Web" project folder contains:

- `AppUlink/`: Django project configuration folder containing `settings.py` with shared configurations
- `ULinkAdmin/`: Application for the Administrator organization (Revenue Quebec in proof of concept)
- `ULinkPartner/`: Application for partner service (SAAQ in proof of concept)  
- `ULinkPublic/`: Application for citizens
- `static/`: Static project files (images, resources)
- `templates/`: HTML templates organized by application
- `manage.py`: Django command utility
- `requirements.txt`: External dependencies

## Setup Instructions

### Prerequisites

- Python 3.11.1 or higher ([Download Python](https://www.python.org/downloads/release/python-3111/))
- Virtual environment

### Installation Steps

1. Clone the repository or download the project files

2. Create a virtual environment:
```bash
python -m venv venvPOCBlockchain
```

3. Activate the virtual environment:

**Windows:**
```bash
venvPOCBlockchain\Scripts\activate.bat
```

**Linux/MacOS:**
```bash
source venvPOCBlockchain/bin/activate
```

4. Install dependencies:
```bash 
pip install -r requirements.txt
```


### Configuration

Before running the application, update `settings.py`:

1. Configure API service addresses connecting to the blockchain (lines 154-157)
2. Set up IPFS connection string
![image](https://github.com/user-attachments/assets/465b4be0-1998-4b1c-a956-aca9f7ccba7b)

4. Update the blockchain authentication settings if needed (line 165+)
![image](https://github.com/user-attachments/assets/e8d1b5e7-32a8-4ca1-8d10-a51cd764a184)




### Running the Application

1. Start the development server:
```bash
python manage.py runserver 9000
```

2. Access the applications at:
- Citizen portal: http://127.0.0.1:9000/public
![image](https://github.com/user-attachments/assets/24be13e2-5b03-4d01-a570-66478a19b7f1)

- Revenue Quebec portal: http://127.0.0.1:9000/rq
![image](https://github.com/user-attachments/assets/c5851332-31b0-4917-8cf0-49f65967a0cf)

- SAAQ portal: http://127.0.0.1:9000/saaq
![image](https://github.com/user-attachments/assets/0b818c5a-bfa7-43d3-9599-83e9800126a4)


### Default Login Credentials

- Public: john.doe@cristal.ca
- RQ: rq1@cristal.ca
- SAAQ: saaq1@cristal.ca
- Default password for all users: `P@ssword01`

## Authentication Notes

- The master branch uses Django's default authentication system
- For blockchain authentication:
  1. Get access credentials from `enrollUser.js` (see Blockchain Deployment section)
  2. Use the `stableWithAuthentification` branch
  3. Update `settings.py` authentication configurations (line 165+)


## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

Distributed under the MIT License. 
