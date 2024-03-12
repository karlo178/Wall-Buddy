import threading
from queue import Queue
from tensorflow.keras.models import load_model

def load_neural_network(model_path):
    try:
        # Load the saved model
        model = load_model(model_path)
        print("Neural network loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading neural network: {e}")
        return None

# Usage
neural_network_path = "path/to/your/saved_model.h5"  # Replace with the actual path
neural_network = load_neural_network(neural_network_path)

# Check if the neural network loaded successfully before using it
if neural_network:
    # Make predictions using the loaded neural network
    prediction = neural_network.predict(some_input_data)
    print("Prediction:", prediction)
else:
    print("Neural network failed to load.")


class TaskManager:
    def __init__(self):
        self.queue = Queue()
        self.listen_thread = threading.Thread(target=self.listen_for_trigger)
        self.listen_thread.start()
        self.neural_network = load_neural_network()  # Replace with your actual loading function
        self.listen_active = True

    def check_queue(self):
        try:
            while True:
                action = self.queue.get_nowait()
                self.handle_user_input(action)
        except:
            pass
        self.check_queue()  # Continue checking the queue

    def display_response(self, response):
        print("Assistant:", response)

    def preprocess_input(self, input_text):
        return input_text.lower()

    def handle_user_input(self, action):
        processed_input = self.preprocess_input(action)
        response = self.neural_network.predict(processed_input)  # Replace with your actual prediction function
        self.display_response(response)

    def listen_for_trigger(self):
        while self.listen_active:
            action = input("You: ")
            self.queue.put(action)

    def stop_listening(self):
        self.listen_active = False

    def resume_listening(self):
        self.listen_active = True

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.check_queue()
