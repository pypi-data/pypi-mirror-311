# package1/__main__.py
import sys

def main():
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "setup":
            import dex_workspace.configure
        elif command == "start":
            import dex_workspace.app
        else:
            print(f"Unknown command: {command}")
    else:
        print("No command specified.")

if __name__ == "__main__":
    main()