# LaunchDarkly Microservices Experiment Demo

This project demonstrates using LaunchDarkly feature flags to conduct experiments between two microservices implementations. It includes a basic sorting service and an optimized sorting service, allowing you to measure and compare their performance.

## Project Structure

- `service_a/` - Basic sorting service using bubble sort
- `service_b/` - Optimized sorting service using Python's built-in sort
- `main.py` - Main application that routes traffic between services using LaunchDarkly
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file from `.env.example` and add your LaunchDarkly SDK key:
   ```bash
   cp .env.example .env
   ```

3. Configure LaunchDarkly:
   - Create a feature flag called `use-optimized-service` (boolean)
   - Set up an experiment metric called `sorting-performance` (numeric)

## Running the Demo

1. Start Service A (in a new terminal):
   ```bash
   cd service_a
   python main.py
   ```

2. Start Service B (in a new terminal):
   ```bash
   cd service_b
   python main.py
   ```

3. Run the main application:
   ```bash
   python main.py
   ```

4. Press Enter to run experiments. The application will:
   - Generate random numbers
   - Route to either Service A or B based on the LaunchDarkly flag
   - Display results and send metrics back to LaunchDarkly

## LaunchDarkly Configuration

1. Feature Flag Setup:
   - Name: `use-optimized-service`
   - Key: `use-optimized-service`
   - Variations: 
     - true: Route to optimized service
     - false: Route to basic service

2. Metric Setup:
   - Name: `sorting-performance`
   - Type: Numeric
   - Success criteria: Lower values are better (processing time)

You can then use LaunchDarkly's experimentation features to:
- Gradually roll out the optimized service
- Compare performance metrics between services
- Make data-driven decisions about which implementation to use

## Expected Results

The optimized service (Service B) should consistently perform better than the basic service (Service A), especially with larger arrays. This demonstrates how feature flags can be used to:

1. Safely roll out new implementations
2. Gather performance metrics
3. Make data-driven decisions about service improvements
