import dotenv
from create_tweet import lambda_handler

dotenv.load_dotenv()
if __name__ == "__main__":
    lambda_handler(event=None, context=None)
