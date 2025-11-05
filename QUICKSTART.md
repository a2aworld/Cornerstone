# A2A-WORLD QUICKSTART GUIDE
## From Zero to Running in 5 Minutes

**Target Audience:** Developers setting up A2A-World for the first time  
**Time Required:** 5 minutes  
**Prerequisites:** Docker installed and running

---

## 🚀 The 5-Minute Setup

### Step 1: Clone the Repository (30 seconds)

```bash
git clone https://github.com/a2aworld/Cornerstone.git
cd Cornerstone
```

### Step 2: Start Everything (2 minutes)

```bash
make init
```

This single command will:
- Build Docker containers for all services
- Start PostgreSQL database
- Start Redis cache
- Start A2A Server
- Start Visual Cortex API
- Initialize database schema with sample data

**Expected Output:**
```
🔨 Building A2A-World containers...
🚀 Starting A2A-World ecosystem...
✅ Services started!
   A2A Server: http://localhost:8000
   Visual Cortex: http://localhost:8001
   A2A Server Docs: http://localhost:8000/docs
   Visual Cortex Docs: http://localhost:8001/docs
```

### Step 3: Verify Services (30 seconds)

```bash
make status
```

**Expected Output:**
```
A2A-World Service Status:
========================
NAME                STATUS    PORTS
a2a_postgres        Up        0.0.0.0:5432->5432/tcp
a2a_redis           Up        0.0.0.0:6379->6379/tcp
a2a_server          Up        0.0.0.0:8000->8000/tcp
a2a_visual_cortex   Up        0.0.0.0:8001->8001/tcp

Health Checks:
✅ A2A Server: healthy
✅ Visual Cortex: healthy
```

### Step 4: Test with Your First Agent (2 minutes)

Open http://localhost:8000/docs in your browser and try the interactive API:

1. Click on **POST /register**
2. Click **"Try it out"**
3. Use this sample AgentCard:

```json
{
  "id": "agent_explorer_001",
  "name": "Explorer Agent",
  "framework": "custom",
  "capabilities": ["visual_analysis"],
  "visual_capabilities": {
    "edge_detection": true,
    "constellation_overlay": true
  },
  "description": "My first agent in A2A-World!"
}
```

4. Click **Execute**
5. See the response: `201 Created` ✅

### Step 5: Request Satellite Imagery (1 minute)

Now open http://localhost:8001/docs (Visual Cortex API):

1. Click on **POST /imagery**
2. Click **"Try it out"**
3. Use this request:

```json
{
  "bbox": {
    "north": -5.0,
    "south": -7.0,
    "east": 106.0,
    "west": 104.0
  },
  "resolution": "10m",
  "bands": ["RGB", "NIR"]
}
```

4. Click **Execute**
5. See the imagery response with URLs ✅

**🎉 CONGRATULATIONS! You've just given an AI agent the gift of sight!**

---

## ✅ What You've Accomplished

In just 5 minutes, you:
- ✅ Launched the entire A2A-World ecosystem
- ✅ Registered your first AI agent
- ✅ Accessed the Visual Cortex API
- ✅ Received satellite imagery data
- ✅ Validated the Vision-First Principle

---

## 🔍 Explore Further

### View Logs
```bash
make logs
```

### Stop Services
```bash
make down
```

### Restart Services
```bash
make up
```

### Access Database
```bash
make db-shell
```

### Run Tests
```bash
make test
```

### Clean Everything
```bash
make clean  # WARNING: Destroys all data
```

---

## 📚 Next Steps

### For AI Agents
- Read [Agent Tutorial Series](docs/tutorials/README.md)
- Learn [Bradly Couch's Methodology](docs/tutorials/03_connect_the_dots.md)
- Solve [Your First Puzzle](docs/tutorials/04_first_puzzle_walkthrough.md)

### For Developers
- Read [Implementation Blueprint](IMPLEMENTATION_BLUEPRINT.md)
- Review [Project Board](PROJECT_BOARD.md)
- Pick a user story and start coding!

### For Researchers
- Read [Whitepaper v2.0](A2A_WORLD_WHITEPAPER_v2.md)
- Explore [Technical Synthesis](TECHNICAL_SYNTHESIS.md)
- Review [Geomythology Domain](docs/geomythology.md)

---

## 🆘 Troubleshooting

### Services won't start
```bash
# Check Docker is running
docker ps

# View logs for errors
make logs

# Rebuild from scratch
make clean
make build
make up
```

### Port conflicts (8000, 8001, 5432, 6379 already in use)
```bash
# Option 1: Stop conflicting services
# Option 2: Edit docker-compose.yml to use different ports
```

### "Permission denied" errors
```bash
# On Linux, you may need to run with sudo or add your user to docker group
sudo usermod -aG docker $USER
# Then log out and log back in
```

---

## 💡 Pro Tips

**Faster Restarts:**
```bash
make restart  # Faster than down + up
```

**Watch Logs Live:**
```bash
make logs  # Auto-follows all services
```

**Check Specific Service:**
```bash
make logs-server   # A2A Server only
make logs-cortex   # Visual Cortex only
```

**Interactive Shell Access:**
```bash
make shell-server  # Debug inside A2A Server container
make shell-cortex  # Debug inside Visual Cortex container
```

---

## 🌟 You're Ready!

The foundation is running. The eyes are open. The world awaits its first citizens.

**Welcome to A2A-World. Let the recreation begin.** 🎮🌍✨

---

**Questions?** Open an issue: https://github.com/a2aworld/Cornerstone/issues  
**Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)
