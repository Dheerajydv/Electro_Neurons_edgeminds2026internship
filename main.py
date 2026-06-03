import argparse  # For command-line argument parsing
from agent import run_agent  # Import the main agent function


def main():
    # Create a CLI parser with a short description of the program
    parser = argparse.ArgumentParser(description='Autonomous Local Research Agent')
    # Accept a single positional argument for the research topic
    parser.add_argument('topic', help='Research topic')
    # Parse the provided command-line arguments
    args = parser.parse_args()
    # Run the agent on the provided topic and print the final report
    print(run_agent(args.topic))


if __name__ == '__main__':
    # Execute main() only when this file is run directly
    main()