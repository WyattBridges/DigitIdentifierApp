# DigitIdentifierApp
This project allows users to draw their own handwritten digits, select a model, send it to an API for prediction, and view the distribution of probabilities given by the chosen model within a functional web application. React is used in the frontend, and Python with FastAPI and Tensorflow is used in the backend.

<img width="281" height="381" alt="image" src="https://github.com/user-attachments/assets/fa321686-e6df-42db-85cc-6858aef48bde" /> <br>

<img width="280" height="173" alt="image" src="https://github.com/user-attachments/assets/8cd4d9a6-3716-45f8-9569-5fbd5796b1e3" />

### Example Prediction:
<img width="283" height="379" alt="image" src="https://github.com/user-attachments/assets/6328bfeb-c855-41a4-9f88-9e2ee559d081" /> <br>

<img width="279" height="172" alt="image" src="https://github.com/user-attachments/assets/6004b7b1-0587-4134-9ada-0c75295c7c49" />

At this time, only a dense model and a convolutional model (with a structure similar to LeNet-5) are available.

## Presentation
The presentation of information on this application is available here: [https://www.youtube.com/watch?v=1ZwbT7PJPJQ](https://www.youtube.com/watch?v=1ZwbT7PJPJQ)

## Build Instructions
To build the Python backend and its environment, start in a terminal at the root directory of the project, and run the following:
```bash
cd model_services
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
The scripts used to create and train the models used by the application are available as well. To run them to create a new version of these models, change directory into the app directory (within the model_services directory) and run the corresponding create_*_model.py python script while within the Python environment.

To build the React frontend, start another terminal at the root directory of the project and run:
```bash
cd web_app
npm install
```

## Running the project
To start the Python backend, run ```venv/bin/activate``` or ```venv\Scripts\activate``` (depending on your OS) from within the model_services folder to start the environment. Then, run:
```bash
uvicorn app.main:app --reload --port 8000
```

To start the React frontend, open another terminal and run ```npm run dev``` from within the web_app directory.
