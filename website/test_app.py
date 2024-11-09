import unittest
from app import app
from unittest.mock import patch
import json

class FlaskTestCase(unittest.TestCase):

    @patch('app.client.chat.completions.create')  # Mock the OpenAI API client method
    def test_send_prompt_success(self, mock_openai_response):
        # Prepare the mock response to simulate OpenAI's API response
        mock_openai_response.return_value.choices = [
            type('obj', (object,), {"message": type('obj', (object,), {"content": "Question: What is Python?, Answer: A programming language; Question: What is Flask?, Answer: A Python web framework;"})})]

        # Simulate a POST request to the '/send-prompt' route with valid input
        with app.test_client() as client:
            response = client.post('/send-prompt', json={'prompt': 'Tell me about Python and Flask.'})

            # Assert the response is successful (status code 200)
            self.assertEqual(response.status_code, 200)

            # Assert the response JSON contains the expected data
            response_data = json.loads(response.data)
            self.assertIn("response", response_data)
            self.assertIn("Question: What is Python?, Answer: A programming language;", response_data['response'])

    @patch('app.client.chat.completions.create')  # Mock the OpenAI API client method
    def test_send_prompt_no_input(self, mock_openai_response):
        # Simulate a POST request to the '/send-prompt' route with empty input
        with app.test_client() as client:
            response = client.post('/send-prompt', json={'prompt': ''})

            # Assert that the response is a 400 (Bad Request) error for missing prompt
            self.assertEqual(response.status_code, 400)

            # Assert the response contains the error message
            response_data = json.loads(response.data)
            self.assertEqual(response_data['response'], 'Please enter a prompt.')

    @patch('app.client.chat.completions.create')  # Mock the OpenAI API client method
    def test_send_prompt_invalid_api(self, mock_openai_response):
        # Simulate an error in the OpenAI API (e.g., network failure or invalid API key)
        mock_openai_response.side_effect = Exception("OpenAI API error")

        # Simulate a POST request to the '/send-prompt' route
        with app.test_client() as client:
            response = client.post('/send-prompt', json={'prompt': 'Tell me a joke.'})

            # Assert the response contains the error message
            self.assertEqual(response.status_code, 500)
            response_data = json.loads(response.data)
            self.assertIn("Error: OpenAI API error", response_data['response'])

    def test_index_route(self):
        # Test the root route (index) to ensure the HTML page loads correctly
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('<textarea id="prompt-input" placeholder="Type your prompt..."></textarea>', response.data.decode())

if __name__ == '__main__':
    unittest.main()

