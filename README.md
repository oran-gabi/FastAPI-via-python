🍕 Food Store API - Order Management System
Hey there! Welcome to the Food Store API project. This is a full-stack web application built with FastAPI that lets you manage a food inventory and place orders. Think of it as a mini food delivery backend!
🎯 What Does This Do?
Ever wondered how food ordering apps work behind the scenes? This project shows you exactly that! You get:

A backend API that manages your food inventory (pizzas, burgers, beers, fries)
A beautiful web interface where customers can place orders
Real-time stock tracking so you never oversell
Automatic price calculations for orders

It's basically a simplified version of what restaurants use to track their inventory and orders.
🚀 Getting Started
What You'll Need

Python 3.8 or higher (check with python --version)
A terminal (PowerShell, CMD, or bash)
A web browser (you already have this! 😄)
About 5 minutes of your time

Installation
1. Clone or download this project
bashcd your-project-folder
2. Create a virtual environment (optional but recommended)
bash# Windows
python -m venv api_env
api_env\Scripts\activate

# Mac/Linux
python3 -m venv api_env
source api_env/bin/activate
3. Install the dependencies
bashpip install -r requirements.txt
That's it! You're ready to go.
🎮 Running the Application
You need to run TWO servers - think of it like running both the kitchen (API) and the cashier (Client) at the same time.
Step 1: Start the API Server (The Kitchen 👨‍🍳)
Open your first terminal and run:
bashpython -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
You should see:
INFO: Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
What this does: This starts your inventory management system. It keeps track of how much food you have and processes orders.
Step 2: Start the Client Server (The Cashier 💁‍♀️)
Open a second terminal (keep the first one running!) and run:
bashpython -m uvicorn client:client_app --reload --host 0.0.0.0 --port 8001
You should see:
INFO: Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
What this does: This starts the customer-facing website where people can browse and order food.
Step 3: Open Your Browser 🌐
Now the fun part! Open your browser and visit:

Order Food: http://localhost:8001
View Inventory: http://localhost:8001/inventory
API Documentation: http://localhost:8000/api/docs (super cool interactive docs!)

📖 How to Use It
Placing an Order (As a Customer)

Go to http://localhost:8001
Select a product from the dropdown (you'll see the price and stock info appear)
Enter how many you want
Click "Place Order"
See your order confirmation with the total price!

Checking Inventory
Visit http://localhost:8001/inventory to see all available products with their current stock levels.
Using the API Directly (For Developers)
Want to integrate this with your own app? Check out the interactive API docs at http://localhost:8000/api/docs
You can:

GET /warehouse/inventory - See all products
GET /warehouse/{product}?order_qty=5 - Place an order
POST /warehouse/{product}/restock?restock_qty=100 - Add more stock
GET /health - Check if the system is working

🏗️ Project Structure
Here's what's inside:
📁 Food Store API/
├── 📄 app.py              # The main API server (backend brain)
├── 📄 client.py           # The web interface server (frontend)
├── 📄 requirements.txt    # All the libraries we need
├── 📄 README.md          # You are here! 👋
├── 📁 templates/         # HTML pages for the website
│   ├── index.html        # Order form page
│   ├── result.html       # Order confirmation page
│   ├── error.html        # Error page (when things go wrong)
│   └── inventory.html    # Inventory display page
└── 📁 static/            # CSS, JS, images (currently empty)
🎨 Features That Make This Cool

Real-time Validation: Can't order more than what's in stock
Pretty UI: Modern gradient design that doesn't hurt your eyes
Smart Forms: Product info appears as you select items
Error Handling: Clear messages when something goes wrong
Auto-calculation: Prices are calculated automatically
Professional Logging: See what's happening behind the scenes
API Documentation: Auto-generated, interactive docs

🐛 Troubleshooting
"Module not found" errors?
Make sure you installed all dependencies:
bashpip install -r requirements.txt
Can't connect to the API?
Make sure both servers are running:

API server on port 8000
Client server on port 8001

Check they're running with:
bash# PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health

# Mac/Linux
curl http://localhost:8000/health
Port already in use?
Someone else is using that port! Change the port numbers:
bash# Use different ports
python -m uvicorn app:app --port 8002
python -m uvicorn client:client_app --port 8003
Page not loading?

Check both terminals - are they still running?
Any error messages in red?
Try refreshing the page (Ctrl+R or Cmd+R)

💡 What You Can Learn From This
This project is great for learning:

FastAPI basics - modern Python web framework
RESTful APIs - how apps talk to each other
Client-Server architecture - separating frontend and backend
Templating with Jinja2 - dynamic HTML generation
Data validation with Pydantic - keeping your data clean
Error handling - dealing with things that go wrong
Real-world patterns - inventory management, order processing