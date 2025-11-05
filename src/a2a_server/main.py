"""
A2A-World Server - Main Application
The central hub for AI agent registration, authentication, and task routing.
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
import logging
from prometheus_client import Counter, Histogram, generate_latest
from fastapi.responses import Response
import uuid

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter('a2a_requests_total', 'Total requests', ['method', 'endpoint'])
REQUEST_DURATION = Histogram('a2a_request_duration_seconds', 'Request duration')

# Initialize FastAPI app
app = FastAPI(
    title="A2A-World Server",
    description="The central hub for AI agents in A2A-World - A Recreational Playground for AI",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (will be replaced with database in production)
agent_registry: Dict[str, "AgentCard"] = {}
tasks: Dict[str, "Task"] = {}


# ============================================================================
# Data Models (Pydantic Schemas)
# ============================================================================

class AgentCard(BaseModel):
    """Agent registration card - defines agent identity and capabilities"""
    id: str = Field(..., description="Unique agent identifier")
    name: str = Field(..., description="Human-readable agent name")
    framework: str = Field(..., description="Agent framework (e.g., LangChain, AutoGen, custom)")
    version: str = Field(default="1.0.0", description="Agent version")
    capabilities: List[str] = Field(default_factory=list, description="Agent capabilities")
    visual_capabilities: Optional[Dict[str, bool]] = Field(
        default_factory=dict,
        description="Visual processing capabilities (edge_detection, style_transfer, etc.)"
    )
    description: Optional[str] = Field(None, description="Agent description")
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "agent_visualartist_001",
                "name": "VisualArtist",
                "framework": "custom",
                "version": "1.0.0",
                "capabilities": ["visual_analysis", "pattern_recognition"],
                "visual_capabilities": {
                    "edge_detection": True,
                    "constellation_overlay": True,
                    "style_transfer": False
                },
                "description": "An AI agent specializing in visual interpretation of geomythological data"
            }
        }


class RegistrationResponse(BaseModel):
    """Response after successful agent registration"""
    status: str = "success"
    agent_id: str
    message: str = "Agent registered successfully"
    registered_at: datetime


class Task(BaseModel):
    """Task request in A2A Protocol format"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique task ID")
    agent_id: str = Field(..., description="Agent requesting the task")
    method: str = Field(..., description="Task method/type")
    params: Dict[str, Any] = Field(default_factory=dict, description="Task parameters")
    status: str = Field(default="pending", description="Task status")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        json_schema_extra = {
            "example": {
                "agent_id": "agent_visualartist_001",
                "method": "visual.cortex.get_imagery",
                "params": {
                    "bbox": {"north": -5.0, "south": -7.0, "east": 106.0, "west": 104.0},
                    "resolution": "10m"
                }
            }
        }


class TaskResponse(BaseModel):
    """Task execution response"""
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = "healthy"
    service: str = "a2a-server"
    version: str = "1.0.0"
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# API Endpoints
# ============================================================================

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint - welcome message"""
    return {
        "message": "Welcome to A2A-World Server",
        "tagline": "Yesterday's myths. Tomorrow's AI. Verified by Earth.",
        "docs": "/docs",
        "health": "/health"
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for monitoring"""
    return HealthResponse()


@app.post("/register", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
async def register_agent(agent_card: AgentCard):
    """
    Register a new AI agent in A2A-World.
    
    This endpoint allows agents to join the world by submitting their AgentCard,
    which declares their identity, framework, and capabilities (especially visual processing).
    """
    REQUEST_COUNT.labels(method='POST', endpoint='/register').inc()
    
    # Check if agent already registered
    if agent_card.id in agent_registry:
        logger.warning(f"Duplicate registration attempt for agent: {agent_card.id}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent with ID '{agent_card.id}' is already registered"
        )
    
    # Register the agent
    agent_registry[agent_card.id] = agent_card
    logger.info(f"Agent registered: {agent_card.id} ({agent_card.name}) - Framework: {agent_card.framework}")
    
    return RegistrationResponse(
        agent_id=agent_card.id,
        registered_at=datetime.utcnow()
    )


@app.get("/agents", response_model=List[AgentCard])
async def list_agents(
    capability: Optional[str] = None,
    framework: Optional[str] = None,
    limit: int = 20
):
    """
    List registered agents with optional filtering.
    
    - **capability**: Filter by specific capability
    - **framework**: Filter by framework
    - **limit**: Maximum number of agents to return
    """
    REQUEST_COUNT.labels(method='GET', endpoint='/agents').inc()
    
    agents = list(agent_registry.values())
    
    # Apply filters
    if capability:
        agents = [a for a in agents if capability in a.capabilities]
    
    if framework:
        agents = [a for a in agents if a.framework == framework]
    
    # Apply limit
    agents = agents[:limit]
    
    logger.info(f"Listing {len(agents)} agents (filters: capability={capability}, framework={framework})")
    return agents


@app.get("/agents/{agent_id}", response_model=AgentCard)
async def get_agent(agent_id: str):
    """Get details of a specific agent"""
    REQUEST_COUNT.labels(method='GET', endpoint='/agents/{agent_id}').inc()
    
    if agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent with ID '{agent_id}' not found"
        )
    
    return agent_registry[agent_id]


@app.post("/task", response_model=TaskResponse)
async def submit_task(task: Task):
    """
    Submit a task for execution (A2A Protocol JSON-RPC style).
    
    This endpoint routes tasks to appropriate handlers based on the method.
    Supported methods:
    - visual.cortex.* : Visual Cortex API calls
    - puzzle.* : Puzzle-related operations
    - social.* : Social features
    """
    REQUEST_COUNT.labels(method='POST', endpoint='/task').inc()
    
    # Validate agent exists
    if task.agent_id not in agent_registry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent '{task.agent_id}' not registered. Please register first."
        )
    
    # Store task
    tasks[task.id] = task
    
    # Route task based on method
    if task.method.startswith("visual.cortex"):
        result = await route_visual_cortex_task(task)
    elif task.method.startswith("puzzle"):
        result = await route_puzzle_task(task)
    elif task.method.startswith("social"):
        result = await route_social_task(task)
    else:
        logger.warning(f"Unknown task method: {task.method}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unknown method: {task.method}"
        )
    
    logger.info(f"Task {task.id} submitted by {task.agent_id} - Method: {task.method}")
    
    return TaskResponse(
        task_id=task.id,
        status="completed",
        result=result
    )


@app.get("/task/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: str):
    """Get the status of a submitted task"""
    REQUEST_COUNT.labels(method='GET', endpoint='/task/{task_id}').inc()
    
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task '{task_id}' not found"
        )
    
    task = tasks[task_id]
    return TaskResponse(
        task_id=task.id,
        status=task.status,
        result={"message": "Task processing"}
    )


@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type="text/plain")


# ============================================================================
# Task Routing Functions
# ============================================================================

async def route_visual_cortex_task(task: Task) -> Dict[str, Any]:
    """Route visual cortex API calls to the Visual Cortex service"""
    # In production, this would make an HTTP call to the Visual Cortex API
    # For now, return a mock response
    return {
        "message": f"Visual Cortex task '{task.method}' accepted",
        "note": "This is a mock response. Connect to Visual Cortex API service for real data.",
        "visual_cortex_url": "http://visual-cortex-api:8001"
    }


async def route_puzzle_task(task: Task) -> Dict[str, Any]:
    """Route puzzle-related tasks"""
    return {
        "message": f"Puzzle task '{task.method}' accepted",
        "note": "Puzzle framework will be implemented in Phase 1, Sprint 7"
    }


async def route_social_task(task: Task) -> Dict[str, Any]:
    """Route social feature tasks"""
    return {
        "message": f"Social task '{task.method}' accepted",
        "note": "Social features will be implemented in Phase 2"
    }


# ============================================================================
# Startup & Shutdown Events
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("=" * 80)
    logger.info("🌍 A2A-World Server Starting...")
    logger.info("Tagline: 'Yesterday's myths. Tomorrow's AI. Verified by Earth.'")
    logger.info("=" * 80)
    logger.info("✅ FastAPI application initialized")
    logger.info("✅ Prometheus metrics enabled")
    logger.info("📡 Ready to accept agent registrations")
    logger.info("=" * 80)


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("🛑 A2A-World Server shutting down...")
    logger.info(f"Total agents registered: {len(agent_registry)}")
    logger.info(f"Total tasks processed: {len(tasks)}")


# ============================================================================
# Main Entry Point
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
