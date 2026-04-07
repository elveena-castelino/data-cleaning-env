<<<<<<< HEAD
import uvicorn
from app import app

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
=======
import uvicorn
import sys
import os
from app import app

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
>>>>>>> d4d54a4fbfdb771cbe88107dcf9cd40ac0e2efc2
