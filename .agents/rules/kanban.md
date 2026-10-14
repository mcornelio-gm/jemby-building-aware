# Kanban Automation & Autonomous Access Rules

## Standing Authorization
The agent is permanently authorized to interact directly with the local Kanban FastAPI application running at `http://localhost:8001/` (interactive API documentation available at `http://localhost:8001/docs`).

## Available API Endpoints

### Milestones
- `GET /api/milestones` - List all milestones with aggregate progress and task counts
- `POST /api/milestones` - Create a milestone (`title`, `description`, `category`, `color`, `start_date`, `target_date`)
- `GET /api/milestones/{id}` - Get single milestone
- `PUT /api/milestones/{id}` - Update milestone details
- `PATCH /api/milestones/{id}/dates` - Quick update `start_date` / `target_date`
- `DELETE /api/milestones/{id}` - Delete milestone

### Tasks
- `GET /api/tasks` - List tasks (query filters: `status`, `priority`, `assignee`, `milestone_id`, `tag`, `search`)
- `POST /api/tasks` - Create a task (`title`, `description`, `status`, `priority`, `progress`, `assignee`, `due_date`, `tags`, `milestone_id`)
- `GET /api/tasks/{id}` - Get task details
- `PUT /api/tasks/{id}` - Update task fields
- `PATCH /api/tasks/{id}/move` - Quick move task (`status`, `position`)
- `GET /api/tasks/stats/summary` - Overall board statistics (`total`, `done`, `in_work`, `backlog`, `avg_progress`)
- `DELETE /api/tasks/{id}` - Delete task

## Operational Directives
1. **Autonomous Execution**: Whenever a task is discussed, created, completed, planned, or modified, immediately query or update `http://localhost:8001/api/...` without pausing to ask for step-by-step confirmation.
2. **Default Assignee**: Assign all created or updated tasks to `Michael Cornelio`.
3. **Milestone Association**: When working on JAMES / Single-Line Diagram / Building Aware features, link tasks to Milestone 2 (`Building Aware Enhanced Demo`, `milestone_id: 2`) unless specified otherwise.
4. **Task Completion**: Upon verifying any user feature or fix, autonomously update the task's progress to `100` and status to `done` with a clear, concise technical description.
