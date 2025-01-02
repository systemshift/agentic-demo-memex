# Weather App Demo

This repository demonstrates two approaches to AI-assisted development: a simple direct approach and a smart context-aware approach using memex.

## Simple Approach (simple_agent.py)

The simple approach uses direct AI interaction to generate code:
1. Send a prompt to GPT-4
2. Get back code
3. Save to files
4. Fix any issues manually

```python
# Example of simple approach
response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Create a weather app..."}]
)
# Write response directly to files
```

Pros:
- Quick for simple tasks
- Straightforward implementation
- Good for one-off scripts

Cons:
- No memory between steps
- No context awareness
- May require manual fixes
- Hard to maintain consistency

## Smart Approach (smart_agent_v2.py)

The smart approach uses memex as a knowledge graph to maintain context:

### Memex Structure
```
Project Structure:
memex
├── Project Config Node
│   └── Dependencies, TypeScript config, etc.
├── Frontend Component Node
│   ├── WeatherDisplay.tsx
│   └── Links to: Project Config, Design Decisions
├── Backend Node
│   ├── server.ts
│   └── Links to: Frontend Requirements
└── Design Decisions Node
    └── Links to: Components, Implementation
```

### Project Structure
```
weather-app/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── types/
│   └── package.json
└── backend/
    ├── src/
    │   └── server.ts
    └── package.json
```

### Key Features
1. **Context Storage**: Uses memex to store:
   - Project configuration
   - Code components
   - Design decisions
   - Dependencies

2. **Relationships**: Maintains links between:
   - Frontend and backend components
   - Code and its design decisions
   - Implementation and requirements

3. **Code Generation**: Uses stored context to generate:
   - Consistent code
   - Proper configurations
   - Related files

## Development Process

### Simple Agent (Traditional Approach)
```
User -> AI -> Code -> Manual Fixes -> Done
```
Each interaction is isolated, requiring manual context management and fixes.

### Smart Agent (Memex Approach)
```
User -> AI + Memex Knowledge Graph -> Complete Project
     └─> Previous Decisions
     └─> Component Relationships
     └─> Configuration Context
     └─> Design Patterns
```

The smart approach maintains a knowledge graph that:
1. **Remembers Decisions**: Each choice is stored with context
2. **Understands Relationships**: Components know about each other
3. **Maintains Consistency**: Uses past decisions to inform new code
4. **Evolves Naturally**: Can grow the project while keeping context

For example, when adding a new feature:
- Simple Agent: Starts fresh each time
- Smart Agent: 
  * Reads existing component relationships
  * Understands design decisions
  * Maintains consistent patterns
  * Updates related components automatically

## Key Difference

Simple Agent thinks in isolation: "Create a weather app" → Get code → Done
Smart Agent thinks in context: "Add a feature to this weather app, considering its existing architecture, patterns, and relationships"
