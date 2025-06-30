# Shift Scheduling Automation System

A modern, multi-tenant SaaS application for automated shift scheduling with customizable patterns and intelligent rotation.

## Features

- **Multi-tenant SaaS**: Each user manages their own organization independently
- **Customizable Shift Patterns**: Support for various work/rest cycles (4 days on/2 off, 5 days on/2 off, etc.)
- **Flexible Shift Types**: Define multiple shifts per day (first, second, third shift, etc.)
- **Intelligent Scheduling**: Random rotation with preference support
- **Leave Management**: Automatic schedule adjustment when employees are on leave
- **Visual Calendar**: Monthly view with all employees and shifts
- **Reporting & Analytics**: Shift distribution statistics and summaries
- **Export Options**: PDF and Excel export functionality
- **Data Import/Export**: CSV support for employee management
- **Draft Mode**: Review schedules before finalizing
- **Historical Tracking**: Complete audit trail of schedule changes
- **Validation Rules**: Minimum staffing requirements and fairness checks

## Tech Stack

- **Frontend**: Next.js 14 with TypeScript, Tailwind CSS
- **Backend**: FastAPI with Python 3.11
- **Database**: PostgreSQL 15
- **Authentication**: JWT tokens
- **Containerization**: Docker & Docker Compose
- **Deployment**: Single repository with microservices architecture

## Quick Start

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd shift-planner
   ```

2. **Start the application**

   ```bash
   docker-compose up -d
   ```

3. **Access the application**

   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

4. **Create your account**
   - Visit http://localhost:3000
   - Sign up with your email and password
   - Start creating your shift schedules!

## Project Structure

```
shift-planner/
├── frontend/                 # Next.js frontend application
├── backend/                  # FastAPI backend application
├── docker-compose.yml        # Main orchestration file
├── .env.example             # Environment variables template
└── README.md                # This file
```

## Development

### Prerequisites

- Docker and Docker Compose
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Local Development

```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend development
cd frontend
npm install
npm run dev
```

## API Documentation

Once the application is running, visit http://localhost:8000/docs for interactive API documentation.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.
