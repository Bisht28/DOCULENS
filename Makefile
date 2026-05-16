setup:
	cd backend && python3.11 -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	cd frontend && npm install

backend:
	cd backend && chmod +x start.sh && ./start.sh

frontend:
	cd frontend && chmod +x start.sh && ./start.sh

test:
	cd backend && source venv/bin/activate && pytest tests/ -v