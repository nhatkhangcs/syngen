"""
Command-line interface for Synthetic Generator.
"""

import sys
import argparse
# Import web module directly to avoid circular imports


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Synthetic Generator - Synthetic Data Generator for Machine Learning",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  synthetic-generator web                    # Start web UI
  synthetic-generator web --port 8080       # Start web UI on port 8080
  synthetic-generator web --host 0.0.0.0    # Start web UI accessible from network
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Web UI command
    web_parser = subparsers.add_parser('web', help='Start the web interface')
    web_parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    web_parser.add_argument('--port', type=int, default=8000, help='Port to bind to (default: 8000)')
    web_parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    if args.command == 'web':
        # Import web module directly to avoid circular imports
        from .web import run_app
        run_app(host=args.host, port=args.port, debug=args.debug)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
