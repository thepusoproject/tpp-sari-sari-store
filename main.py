"""TPP Sari-Sari Store (CLI)

This project grows module-by-module (Py4E aligned).
Start point: a simple menu that will expand over time.

Run:
  python main.py
"""


def main():
    print("TPP Sari-Sari Store - CLI")
    print("(Starter project)")
    print("\nMenu:")
    print("1) Module 01 - Sukli Calculator (to be implemented)")
    print("0) Exit")

    choice = input("Choose: ").strip()
    if choice == "0":
        print("Bye!")
        return

    print("Not implemented yet. Start with Module 01 requirements.")


if __name__ == "__main__":
    main()
