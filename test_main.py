import sys
print(sys.path)



from app.repositories.wallet_repository import WalletRepository

def main():
    wallet_object = WalletRepository()
    print(f"The wallet object is: {wallet_object}")
    print("inside_main")
    
if __name__=="__main__":
    main()