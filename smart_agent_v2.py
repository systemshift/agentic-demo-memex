import os
import json
import re
from subprocess import run
import openai

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
    
    def _extract_section(self, content, section_name):
        """Extract a section from the configuration content"""
        pattern = f"# {section_name}\\s+([^#]+)"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""
    
    def _extract_json(self, content, section_name):
        """Extract and parse JSON from a section"""
        section = self._extract_section(content, section_name)
        # Find JSON object between curly braces
        match = re.search(r'\{[^}]+\}', section, re.DOTALL)
        if match:
            return match.group(0)
        return "{}"
    
    def _extract_code(self, content, language):
        """Extract code from markdown content"""
        pattern = f"```{language}\\s*\\n([^`]+)\\n```"
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return match.group(1).strip()
        return content  # Return full content if no code block found
    
    def start_project(self):
        """Initialize and create the project"""
        # Store project configuration and plan
        self._store_project_config()
        
        # Generate project structure and config files
        self._setup_project_structure()
        
        # Generate components and code
        self._create_frontend()
        self._create_backend()
        self._setup_deployment()
    
    def _store_project_config(self):
        """Store project configuration in memex"""
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
        
        # Frontend TypeScript Config
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
    
    def _setup_project_structure(self):
        """Create project structure and configuration files"""
        config = self._get_memex_content("project_config")
        
        # Create directories
        os.makedirs("weather-app/frontend/src/components", exist_ok=True)
        os.makedirs("weather-app/frontend/src/hooks", exist_ok=True)
        os.makedirs("weather-app/frontend/src/types", exist_ok=True)
        os.makedirs("weather-app/backend/src", exist_ok=True)
        
        # Frontend configuration
        self._write_file(
            "weather-app/frontend/package.json",
            self._extract_json(config, "Frontend Dependencies")
        )
        
        self._write_file(
            "weather-app/frontend/tsconfig.json",
            self._extract_json(config, "Frontend TypeScript Config")
        )
        
        self._write_file(
            "weather-app/frontend/src/types/css.d.ts",
            self._extract_section(config, "CSS Modules Type Definition")
        )
        
        self._write_file(
            "weather-app/frontend/vite.config.ts",
            """import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:3001'
    }
  }
})"""
        )
        
        self._write_file(
            "weather-app/frontend/index.html",
            """<!DOCTYPE html>
<html>
  <head>
    <title>Weather App</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>"""
        )
        
        # Backend configuration
        self._write_file(
            "weather-app/backend/package.json",
            self._extract_json(config, "Backend Dependencies")
        )
        
        self._write_file(
            "weather-app/backend/tsconfig.json",
            """{
  "compilerOptions": {
    "target": "es6",
    "module": "commonjs",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true
  },
  "include": ["src/**/*"]
}"""
        )
    
    def _store_in_memex(self, content, description):
        """Store content in memex and return the node ID"""
        try:
            with open("temp.txt", "w") as f:
                f.write(content)
            
            result = run(["memex", "add", "temp.txt"], capture_output=True, text=True)
            if result.returncode != 0:
                raise Exception(f"Failed to add to memex: {result.stderr}")
            
            print("Memex add output:", result.stdout)
            
            node_match = re.search(r'Added node: ([0-9a-f]+)', result.stdout)
            if not node_match:
                status_result = run(["memex", "status"], capture_output=True, text=True)
                if status_result.returncode == 0:
                    node_match = re.search(r'Node ID: ([0-9a-f]+)', status_result.stdout)
            
            if not node_match:
                raise Exception("No Node ID found in output")
            
            node_id = node_match.group(1)
            self.node_map[description] = node_id
            return node_id
            
        finally:
            if os.path.exists("temp.txt"):
                os.remove("temp.txt")
    
    def _get_memex_content(self, description):
        """Get content from memex using stored node ID"""
        if description not in self.node_map:
            return ""
        
        node_id = self.node_map[description]
        result = run(["memex", "cat", node_id], capture_output=True, text=True)
        return result.stdout if result.returncode == 0 else ""
    
    def _write_file(self, path, content):
        """Write content to a file, creating directories if needed"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        print(f"Created: {path}")
    
    def _create_frontend(self):
        """Generate frontend components"""
        project_plan = self._get_memex_content("project_plan")
        
        # Generate weather display component
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
                messages=[{"role": "user", "content": prompt}],
                timeout=60
            )
            
            component = response.choices[0].message.content
            component_id = self._store_in_memex(component, "weather_display_component")
            
            # Extract and write component code
            component_code = self._extract_code(component, "tsx")
            self._write_file(
                "weather-app/frontend/src/components/WeatherDisplay.tsx",
                component_code
            )
            
            # Extract and write CSS
            css_match = re.search(r'```css\s*\n([^`]+)\n```', component, re.DOTALL)
            if css_match:
                self._write_file(
                    "weather-app/frontend/src/components/WeatherDisplay.module.css",
                    css_match.group(1).strip()
                )
            
        except Exception as e:
            print(f"Error generating frontend component: {str(e)}")
            raise
    
    def _create_backend(self):
        """Generate backend code"""
        frontend_code = self._get_memex_content("weather_display_component")
        
        prompt = f"""Create an Express.js backend for the weather app.
        Frontend Implementation:
        {frontend_code}
        
        Requirements:
        - Express.js with TypeScript
        - Weather API integration
        - Caching layer
        - Error handling
        - Rate limiting
        """
        
        try:
            print("\nGenerating backend code...")
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                timeout=60
            )
            
            backend = response.choices[0].message.content
            backend_id = self._store_in_memex(backend, "backend_implementation")
            
            # Extract and write backend code
            backend_code = self._extract_code(backend, "typescript")
            self._write_file(
                "weather-app/backend/src/server.ts",
                backend_code
            )
            
        except Exception as e:
            print(f"Error generating backend code: {str(e)}")
            raise
    
    def _setup_deployment(self):
        """Generate deployment configuration"""
        backend_code = self._get_memex_content("backend_implementation")
        
        prompt = f"""Create deployment configuration for the weather app.
        Backend Implementation:
        {backend_code}
        
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
                messages=[{"role": "user", "content": prompt}],
                timeout=60
            )
            
            deployment = response.choices[0].message.content
            deployment_id = self._store_in_memex(deployment, "deployment_config")
            
            # Extract and write deployment files
            docker_code = self._extract_code(deployment, "dockerfile")
            self._write_file("weather-app/Dockerfile", docker_code)
            
            compose_code = self._extract_code(deployment, "yaml")
            self._write_file("weather-app/docker-compose.yml", compose_code)
            
        except Exception as e:
            print(f"Error generating deployment config: {str(e)}")
            raise

if __name__ == "__main__":
    agent = WeatherAppAgent()
    agent.start_project()
