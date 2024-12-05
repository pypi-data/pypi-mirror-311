from datetime import datetime

def isJem3a():
    today = datetime.today().weekday()
    return today == 3

def main():
    if isJem3a():
        print("Yes, it's Jem3a tomorrow")
    else:
        print("It's not Jem3a tomorrow")

if __name__ == "__main__":
    main()