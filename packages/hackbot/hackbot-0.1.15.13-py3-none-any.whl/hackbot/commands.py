import argparse
import asyncio
import json
import os
from loguru import logger as log
from aiohttp.client_exceptions import ClientPayloadError
from hackbot.utils import get_version
from hackbot.hack import authenticate, cli_hack_target, generate_issues

__version__ = get_version()


def get_args() -> argparse.Namespace:
    """Parse the command line arguments."""
    parser = argparse.ArgumentParser(description="Hackbot - Eliminate bugs from your code")
    parser.add_argument("--version", action="version", version=f"GatlingX Hackbot v{__version__}")
    subparsers = parser.add_subparsers(dest="command", help="What hackbot command to run", required=True)

    # Create the run command parser
    run_parser = subparsers.add_parser("run", help="Run analysis on source code")
    run_parser.add_argument(
        "--address",
        default="https://app.hackbot.co",
        help="Hackbot service address",
    )
    run_parser.add_argument("--port", type=int, default=None, required=False, help="Service port number")
    run_parser.add_argument(
        "--api-key",
        default=os.getenv("HACKBOT_API_KEY"),
        help="API key for authentication (default: HACKBOT_API_KEY environment variable)",
    )
    run_parser.add_argument(
        "--source",
        default=".",
        help="Path to folder containing foundry.toml (default: current directory). If no foundry.toml is found, we search upwards from the specified directory.",
    )
    run_parser.add_argument("--output", help="Path to save analysis results")
    run_parser.add_argument("--auth-only", action="store_true", help="Only verify API key authentication")

    issue_parser = run_parser.add_argument_group("Issue Generation Options")
    issue_parser.add_argument(
        "--issues_repo",
        type=str,
        help="The repository to generate issues in (format: username/repo). By default empty and so no issues are generated",
    )
    issue_parser.add_argument(
        "--github_api_key",
        type=str,
        required=False,
        help="GitHub API key for issue generation",
    )

    args = parser.parse_args()

    # Find closest enclosing path with foundry.toml by searching upwards
    current_path = os.path.abspath(args.source)
    while current_path != os.path.abspath(os.sep):  # Stop at root, using os.sep for cross-platform
        if os.path.exists(os.path.join(current_path, "foundry.toml")):
            args.source = current_path
            break
        current_path = os.path.dirname(current_path)
    else:  # No foundry.toml found
        log.error(f"❌ Error: No foundry.toml found in {os.path.abspath(args.source)} or any parent directories")
        return 1
    args.source = current_path

    if not args.api_key:
        log.error("❌ Error: API key is required (either via --api-key or HACKBOT_API_KEY environment variable)")
        return 1

    return args


def hackbot_run(args: argparse.Namespace) -> int:
    """Run the hackbot tool."""
    try:
        # Verify authentication
        if not asyncio.run(authenticate(args.address, args.port, args.api_key)):
            log.error("❌ Authentication failed")
            return 1

        log.info("✅ Authentication successful")

        if args.auth_only:
            return 0

        # Perform the analysis
        results = asyncio.run(cli_hack_target(args.address, args.port, args.api_key, args.source, args.output))

        if args.issues_repo and results:
            log.info(f"Generating issues report on repo {args.issues_repo}")
            asyncio.run(generate_issues(args.issues_repo, args.github_api_key, results))
        else:
            log.debug("No github repository for reporting issues has been specified. Skipping github issue generation.")

        # Output results to output-path
        if args.output and results:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)

        return 0

    except ClientPayloadError:
        log.error(
            "❌ The server terminated the connection prematurely, most likely due to an error in the scanning process. Check the streamed logs for error messages. Support: support@gatlingx.com"
        )
        return 1
    except Exception as e:
        if str(e) == "Hack request failed: 413":
            log.error("❌ The source code directory is too large to be scanned. Must be less than 256MB.")
        else:
            log.error(f"❌ Error: {str(e)}")
        return 1
