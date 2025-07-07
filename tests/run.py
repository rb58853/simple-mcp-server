from dotenv import load_dotenv

load_dotenv()

from use_cases.client import run as client_test
from use_cases.auth_client import run as auth_client_test

client_test()
print(
    "\n____________________________________________________________________________________________________\n"
)
auth_client_test()
