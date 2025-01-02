import os
import openai
from subprocess import run

class WeatherAppAgent:
    def __init__(self):
        # Read API key
        with open('api_key.txt', 'r') as f:
            api_key = f.read().strip()
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key)
        
        # Initialize memex repository
        run(["memex", "init", "weather-app"])
        run(["memex", "connect", "weather-app.mx"])
        
        # Dictionary to store node IDs
        self.node_map = {}
        
    def start_project(self):
        # Create project structure
        os.makedirs("weather-app/frontend/src/components", exist_ok=True)
        os.makedirs("weather-app/frontend/src/hooks", exist_ok=True)
        os.makedirs("weather-app/backend/src", exist_ok=True)

        # Store complete project configuration
        config = """Weather Web App Configuration:
        
        # Project Structure
        /weather-app
          /frontend
            /src
              /components
              /hooks
              /types
            package.json
            vite.config.ts
            tsconfig.json
            index.html
          /backend
            /src
            package.json
            tsconfig.json
        
        # Frontend Dependencies
        {
          "dependencies": {
            "react": "^18.2.0",
            "react-dom": "^18.2.0",
            "axios": "^1.6.0",
            "typescript": "^5.0.0"
          },
          "devDependencies": {
            "@types/react": "^18.2.0",
            "@types/react-dom": "^18.2.0",
            "vite": "^5.0.0",
            "@vitejs/plugin-react": "^4.0.0"
          }
        }
        
        # Backend Dependencies
        {
          "dependencies": {
            "express": "^4.18.0",
            "cors": "^2.8.5",
            "typescript": "^5.0.0",
            "axios": "^1.6.0"
          },
          "devDependencies": {
            "@types/express": "^4.17.0",
            "@types/cors": "^2.8.5",
            "ts-node": "^10.9.0",
            "nodemon": "^3.0.0"
          }
        }
        
        # TypeScript Configurations
        ## Frontend tsconfig.json
        {
          "compilerOptions": {
            "target": "ES2020",
            "useDefineForClassFields": true,
            "lib": ["ES2020", "DOM", "DOM.Iterable"],
            "module": "ESNext",
            "skipLibCheck": true,
            "moduleResolution": "bundler",
            "allowImportingTsExtensions": true,
            "resolveJsonModule": true,
            "isolatedModules": true,
            "noEmit": true,
            "jsx": "react-jsx",
            "strict": true,
            "noUnusedLocals": true,
            "noUnusedParameters": true,
            "noFallthroughCasesInSwitch": true
          },
          "include": ["src"],
          "references": [{ "path": "./tsconfig.node.json" }]
        }
        
        # CSS Modules Type Definition
        declare module '*.module.css' {
          const classes: { [key: string]: string };
          export default classes;
        }
        """
        self._store_in_memex(config, "project_config")
        
        # Store project plan
        plan = """Weather Web App Development Plan:
        1. Frontend Setup (React + TypeScript)
           - Weather display component
           - Data fetching hook
           - Error handling
           - Loading states
        
        2. Backend API (Node/Express)
           - Weather data endpoint
           - Caching layer
           - Error handling
           - Rate limiting
        
        3. Weather API Integration
           - API key management
           - Data transformation
           - Error handling
           - Backup providers
        
        4. User Preferences
           - Location storage
           - Temperature unit preference
           - Update frequency
        
        5. Deployment
           - Environment setup
           - Docker configuration
           - CI/CD pipeline
        """
        self._store_in_memex(plan, "project_plan")
        
        # Start with frontend
        self._create_frontend()
        
        # Move to backend
        self._create_backend()
        
        # Set up deployment
        self._setup_deployment()
    
    def _store_in_memex(self, content, description):
        """Store content in memex and return the node ID"""
        try:
            # Save content to temporary file
            with open("temp.txt", "w") as f:
                f.write(content)
            
            # Add to memex and get the node ID from the output
            result = run(["memex", "add", "temp.txt"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Failed to add to memex: {result.stderr}")
            
            # Print raw output for debugging
            print("Memex add output:", result.stdout)
            print("Memex add error:", result.stderr)
            
            # Try to find the Node ID in the add output
            import re
            node_match = re.search(r'Added node: ([0-9a-f]+)', result.stdout)
            if not node_match:
                # If not found in add output, try status
                status_result = run(["memex", "status"], capture_output=True, text=True)
                if status_result.returncode == 0:
                    print("Memex status output:", status_result.stdout)
                    node_match = re.search(r'Node ID: ([0-9a-f]+)', status_result.stdout)
            
            if not node_match:
                raise Exception("No Node ID found in output")
            node_id = node_match.group(1)
            
            # Store mapping of description to node ID
            self.node_map[description] = node_id
            return node_id
            
        except Exception as e:
            print(f"Error storing in memex: {str(e)}")
            raise
            
        finally:
            # Clean up temp file
            if os.path.exists("temp.txt"):
                os.remove("temp.txt")
    
    def _get_memex_content(self, description):
        """Get content from memex using stored node ID"""
        if description not in self.node_map:
            print(f"Warning: No node ID found for '{description}'")
            return ""
            
        node_id = self.node_map[description]
        result = run(["memex", "cat", node_id], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Error reading from memex: {result.stderr}")
            return ""
            
        return result.stdout

    def _create_frontend(self):
        # First check what we know about the project
        project_plan = self._get_memex_content("project_plan")
        
        prompt = f"""Create a React component for weather display.
        Project Context:
        {project_plan}
        
        Requirements:
        - Show current temperature
        - Show weather condition
        - Show forecast
        - Use modern React practices (hooks, functional components)
        - Include proper TypeScript types
        - Add styling (CSS modules)
        """
        
        try:
            print("\nGenerating weather display component...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=60  # 60 second timeout
            )
            print("Successfully generated weather display component")
        except KeyboardInterrupt:
            print("\nGeneration interrupted. Cleaning up...")
            raise
        except Exception as e:
            print("\nError generating weather display component:", str(e))
            raise
        
        # Store the component code
        component = response.choices[0].message.content
        self._store_in_memex(component, "weather_display_component")
        
        # Write component to file
        self._write_file(
            "weather-app/frontend/src/components/WeatherDisplay.tsx",
            component
        )
        
        # Store the design decisions
        decisions = """Design Decisions for Weather Display:
        1. Using functional components with hooks for modern React practices
        2. TypeScript for type safety
        3. CSS modules for scoped styling
        4. Component will fetch data through a custom hook
        """
        self._store_in_memex(decisions, "frontend_decisions")
        
        # Create relationships
        run(["memex", "link", 
            self.node_map["weather_display_component"],
            self.node_map["project_plan"],
            "implements"
        ])
        run(["memex", "link",
            self.node_map["frontend_decisions"],
            self.node_map["weather_display_component"],
            "explains"
        ])
        
        # Move on to creating the data fetching hook
        self._create_data_hook()
    
    def _create_data_hook(self):
        # Read previous decisions
        frontend_decisions = self._get_memex_content("frontend_decisions")
        
        prompt = f"""Create a React hook for fetching weather data.
        Previous Decisions:
        {frontend_decisions}
        
        Requirements:
        - Handle loading states
        - Error handling
        - Cache results
        - TypeScript types
        """
        
        try:
            print("\nGenerating weather data hook...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=60
            )
            print("Successfully generated weather data hook")
        except KeyboardInterrupt:
            print("\nGeneration interrupted. Cleaning up...")
            raise
        except Exception as e:
            print("\nError generating weather data hook:", str(e))
            raise
        
        # Store the hook code
        hook = response.choices[0].message.content
        self._store_in_memex(hook, "weather_hook")
        
        # Write hook to file
        self._write_file(
            "weather-app/frontend/src/hooks/useWeather.ts",
            hook
        )
        
        # Link it to related components
        run(["memex", "link",
            self.node_map["weather_hook"],
            self.node_map["weather_display_component"],
            "provides-data"
        ])

    def _write_file(self, path, content):
        """Write content to a file, creating directories if needed"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created: {path}")

    def _create_backend(self):
        # Read frontend decisions to understand data needs
        frontend_decisions = self._get_memex_content("frontend_decisions")
        hook_code = self._get_memex_content("weather_hook")
        
        prompt = f"""Create an Express.js backend for weather data.
        Frontend Context:
        {frontend_decisions}
        Hook Implementation:
        {hook_code}
        
        Requirements:
        - Express.js with TypeScript
        - Weather API integration
        - Caching layer
        - Error handling
        - Rate limiting
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # Store the backend code
        backend_code = response.choices[0].message.content
        self._store_in_memex(backend_code, "backend_implementation")
        
        # Store backend decisions
        backend_decisions = """Backend Design Decisions:
        1. Express.js with TypeScript for type safety
        2. Redis for caching weather data
        3. Rate limiting per API key
        4. Error handling middleware
        5. OpenAPI/Swagger documentation
        """
        self._store_in_memex(backend_decisions, "backend_decisions")
        
        # Create relationships
        run(["memex", "link",
            self.node_map["backend_implementation"],
            self.node_map["weather_hook"],
            "serves"
        ])
        run(["memex", "link",
            self.node_map["backend_decisions"],
            self.node_map["backend_implementation"],
            "explains"
        ])
        
        # Create actual files
        self._write_file(
            "weather-app/backend/src/server.ts",
            backend_code
        )

    def _setup_deployment(self):
        # Read all previous decisions
        backend_decisions = self._get_memex_content("backend_decisions")
        frontend_decisions = self._get_memex_content("frontend_decisions")
        
        prompt = f"""Create deployment configuration.
        Backend Context:
        {backend_decisions}
        Frontend Context:
        {frontend_decisions}
        
        Requirements:
        - Docker configuration
        - Docker Compose for local dev
        - Environment variables
        - Basic CI/CD pipeline
        """
        
        try:
            print("\nGenerating deployment configuration...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                timeout=60
            )
            print("Successfully generated deployment configuration")
        except KeyboardInterrupt:
            print("\nGeneration interrupted. Cleaning up...")
            raise
        except Exception as e:
            print("\nError generating deployment configuration:", str(e))
            raise
        
        # Store deployment config
        deployment_config = response.choices[0].message.content
        self._store_in_memex(deployment_config, "deployment_config")
        
        # Store deployment decisions
        deployment_decisions = """Deployment Decisions:
        1. Multi-stage Docker builds
        2. Docker Compose for development
        3. GitHub Actions for CI/CD
        4. Environment variable management
        """
        self._store_in_memex(deployment_decisions, "deployment_decisions")
        
        # Create relationships
        run(["memex", "link",
            self.node_map["deployment_config"],
            self.node_map["backend_implementation"],
            "deploys"
        ])
        run(["memex", "link",
            self.node_map["deployment_decisions"],
            self.node_map["deployment_config"],
            "explains"
        ])
        
        # Create actual files
        self._write_file(
            "weather-app/Dockerfile",
            deployment_config
        )

if __name__ == "__main__":
    agent = WeatherAppAgent()
    agent.start_project()
