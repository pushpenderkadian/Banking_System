import json

#class BankingSystem
class BankingSystem:

    def __init__(self):
        pass

    #method to start the running of code
    def run_app(self):
        BankingSystem.log_in(self)      #calling login method
    

    #method for logging into the system
    def log_in(self):
        try:
            with open("UserDetails.json") as file:                  #opening and storing the content of json file into a variable
                user_details = json.load(file)
            flag=False
        except:
            print("Error, File is not accessible, Ending the program")
            exit()

        #taking input for username and password
        username = input("What is your username?: ")
        password = input("What is your password?: ")
        
        for user in user_details:
            #verifing the username and password from file
            if user['username'] == username and user['password'] == password:
                flag=True
                print('Successfully logged in.')
                #calling method of BankingSystem class according to the user type 
                if user["user_type"] == "user":
                    BankingSystem.user_view(self, user_details.index(user))
                elif user["user_type"] == "admin":
                    BankingSystem.admin_view(self)

        #making a loop to ask user to enter the username and password again for wrong combination
        if(flag==False):
            print("!!Wrong username password combination!!\n\tcheck and try again")
            BankingSystem.log_in(self)
    

    #method of operations for a user
    def user_view(self,index):

        with open("UserDetails.json", "r") as file:                     #opening and storing the content of json file into a variable
            user_details = json.load(file)
        user = user_details[index]                      #specific user's section from json file
        
        while True: 
            #taking desired input
            try:
                choice=int(input('''        
Please select an option
1 - View account
2 - View summary
3 - Quit
Enter a number to select your option: '''))
                break
            except KeyboardInterrupt:
                print("goodbye")
                exit()
            except:
                print("!!Wrong input!!")    
        print()
        
        #View account choice's functionality
        if choice == 1:
            while True:
                while True:
                    with open("UserDetails.json", "r") as file:                     #opening and storing the content of json file into a variable
                        user_details = json.load(file)
                    user = user_details[index]
                    print("--Account list--")
                    print("Please select an option:")

                    i = 1
                    selections = {}
                    #account selection
                    if 'current_account' in user['other_information'].keys():
                        for idx, account in enumerate(user['other_information']['current_account']):
                            print(f"    {i} - Current account: £{account['balance']}" )
                            selections.setdefault(i, {"account_type":"current_account", "details":user['other_information']['current_account'][idx]})
                            i += 1
                    if 'saving_account' in user['other_information'].keys():
                        for idx, account in enumerate(user['other_information']['saving_account']):
                            print(f"    {i} - Saving account: £{account['balance']}" )
                            selections.setdefault(i, {"account_type":"saving_account", "details":user['other_information']['saving_account'][idx]})
                            i += 1
                    
                    while True:
                        try:
                            selected_account = int(input('Enter a number to select your option: '))
                            break
                        except KeyboardInterrupt:
                            print("goodbye")
                            exit()
                        except:
                            print('!!Wrong Input!!')
                    print(f'\n\nYou selected {selected_account} - {" ".join(selections[selected_account]["account_type"].split("_"))}: £{selections[selected_account]["details"]["balance"]} ')
                    
                    #taking input for functionality
                    while(True):
                        try:
                            option = int(input('''
Please select an option
1 - Deposit
2 - Withdraw
3 - Go back
Enter a number to select your option: 
'''))
                            break
                        except KeyboardInterrupt:
                            print("goodbye")
                            exit()
                        except:
                            print("\n!!Wrong selection!!\n\tOnly Integers are allowed\n\n")
                        
                    #money deposit in account
                    if option == 1:
                        while(True):
                            try:
                                amount = int(input('Enter the amount you want to deposit: '))           #input for amount to be depisted
                                if(amount>0):
                                    break
                                else:
                                    print(dsfds)                            #just to raise an exception for negative numbers
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                print("!!Wrong Input!! Enter only integers greater than 0")
                        data = user_details
                        account_type = selections[selected_account]["account_type"]
                        account_number = selections[selected_account]["details"]["number"]

                        #adding amount in account
                        for account in data[index]["other_information"][account_type]:
                            if account["number"] == account_number:
                                BankingSystem.deposit(self, account, amount)
                        print(f"You have deposited £{amount}")
                        print("Your new balance is: £",selections[selected_account]["details"]["balance"])
                        #updating entry in json file
                        with open("UserDetails.json",'w') as file:
                            json.dump(data, file, indent=4)

                    #money withdraw from account
                    elif option == 2:
                        while(True):
                            try:
                                amount = int(input('Enter the amount you want to withdraw: '))          #input for amount to be withdrawn
                                if(amount>0):
                                    break
                                else:
                                    print(dsfds)                            #just to raise an exception for negative numbers
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                    print("!!Wrong Input!! Enter only integers greater than 0")

                        #checking balance and amount
                        try:
                            overdraft=user_details[index]['other_information']['current_account'][0]['overdraft_limit']
                        except:
                            overdraft=0  
                        if amount <= (selections[selected_account]["details"]["balance"]+overdraft):
                            with open("UserDetails.json",'r') as file:
                                data = json.load(file)
                            account_type = selections[selected_account]["account_type"]
                            account_number = selections[selected_account]["details"]["number"]

                            #withdrawing money
                            for account in data[index]["other_information"][account_type]:
                                if account["number"] == account_number:
                                    BankingSystem.withdraw(self, account, amount)
                            print(f"You have withdrawn £{amount}")
                            print("Your new balance is: £",(selections[selected_account]["details"]["balance"])-amount)
                            #updating balance in file
                            with open("UserDetails.json",'w') as file:
                                json.dump(data, file, indent=4)
                        else:
                            #if insufficient balance in account
                            with open ("UserDetails.json", 'r')as file:
                                user_details = json.load(file)
                                print('Insufficient funds')

                    #go back operation
                    elif option == 3:
                        pass
            
        # View summary of the accounts
        if choice == 2:
            saving_balance = 0
            current_balance = 0
            bank_account = user['other_information']             
            try:
                current_account = bank_account['current_account']           #if person have current account         
            except:
                current_account = []                   
            try:
                saving_account = bank_account['saving_account']              # if person have saving account
            except:
                saving_account = []

            #balance in current account
            if len(current_account)!=0:
                for account in current_account:
                    current_balance += account['balance']

            #balance in saving account
            if len(saving_account)!=0:
                for account in saving_account:
                    saving_balance+= account['balance']

            #total number of accounts in bank
            print(f'Total Number of accounts :{len(current_account)+len(saving_account)}')
            #total balance in all accounts
            print(f'Total Balance in bank : £{current_balance+saving_balance}')
            print('Address: ',user['other_information']['address'])

        #Quit operation
        if(choice==3):
            pass
        if(choice>3 or choice<1):
            print("!!Wrong Choice!!\n  Try again")
        
            
    # depositing amount in bank
    def deposit(self,account, amount):
        account["balance"] += amount
        
    # withdrawing amount in bank
    def withdraw(self, account, amount):

        account["balance"] -= amount


    # #method of operation for a admin
    def admin_view(self):
        while True:
            try:                            #exception handling for non integer type inputs
                choice=int(input('''
Please select an option
1 - Customer summary
2 - Financial Forecast
3 - Transfer Money
4 - Account management
Enter a number to select your option: 
'''))
                break
            except KeyboardInterrupt:
                print("goodbye")
                exit()
            except:
                print("!!wrong input!!")

        #customer summary
        if choice==1:
            with open("UserDetails.json", "r") as file:             #opening and storing the content of json file into a variable
                user_details = json.load(file)
                user_details.pop(0)                                 #removing self

            #loop to iterate for the details
            for user in user_details:
                print()
                print(f"name: {user['username']}")
                bank_account = user['other_information']
                print(bank_account['address'],'\n')              
                #exception handling  
                try:
                    current_account = bank_account['current_account']
                    current_account = current_account[0]
                    print('Current Account')
                except:
                    current_account = {}
                for detail in current_account.keys():
                    if detail=='balance' or detail=='overdraft_limit':
                        print(f'{detail} : £{current_account[detail]}')
                        continue
                    print(f'{detail} : {current_account[detail]}')
                print()
                #exception handling
                try:
                    saving_account = bank_account['saving_account']
                    print('Saving Account')
                except:
                    saving_account = {}
                for i in  range(0,len(saving_account)):
                    for detail in saving_account[i].keys():
                        if detail=='balance':
                            print(f'{detail} : £{saving_account[i][detail]}')
                            continue
                        print(f'{detail} : {saving_account[i][detail]}')
                print()


        #Financial forecast operation
        if choice == 2:
            with open("UserDetails.json", "r") as file:             #opening and storing the content of json file into a variable
                user_details = json.load(file)
                user_details.pop(0)

            #loop to iterate from the user details
            for user in user_details:
                saving_balance = 0
                current_balance = 0
                interest_amt = 0
                print()
                print(f"name: {user['username']}")
                bank_account = user['other_information']             
                try:
                    current_account = bank_account['current_account']                    
                except:
                    current_account = []                   
                try:
                    saving_account = bank_account['saving_account']
                except:
                    saving_account = []

                #total balance in current account
                if len(current_account)!=0:
                    for account in current_account:
                        current_balance += account['balance']
                #total balance in saving account
                if len(saving_account)!=0:
                    for account in saving_account:
                        saving_balance+= account['balance']
                        interest_amt += account['balance']*(account['interest_rate']/100)

                # showing number of accounts in bank
                print('Number of accounts ')
                print(f'Current Account : {len(current_account)}')
                print(f'Saving Account : {len(saving_account)}')
                # showing total balance in bank
                if len(current_account)!=0 and len(saving_account)==0:
                    print(f'Total Balance in bank : £{current_balance+saving_balance}')
                # showing balance in bank after interest
                else:
                    print(f'Total Balance in bank : £{current_balance+saving_balance}')
                    print("Forecast of total money : £",end="")
                    print('%.2f'%(current_balance+saving_balance+interest_amt))

        # Money tansfer Operation
        if choice == 3:
            #opening file 
            with open("UserDetails.json", "r") as file:
                #storing data
                user_details = json.load(file)
                #taking input from user of sender and receiver
                sender=input("Enter the name of the sender bank account- ")
                receiver=input("Enter the name of the receiver bank account- ")
                #initialsing sender and receiver index
                sender_index = None
                receiver_index = None
                amount = 0
                #iterating till the end of user_details
                for index in range(0,len(user_details)):
                    #checking if the sender and receiver are present
                    if user_details[index]['username']==sender:
                        sender_index = index
                    if user_details[index]['username']==receiver:
                        receiver_index = index
                if sender_index == None:
                    print('Sender Not Found')
                if receiver_index == None:
                    print('Reciever Not Found')
                else:
                    #storing sender and receiver data
                    sender_data = user_details[sender_index]
                    receiver_data = user_details[receiver_index]
                    bank_account = sender_data['other_information']             
                    try:
                        #storing current account details
                        current_account = bank_account['current_account']                    
                    except:
                        #initialsing current account list if details not found
                        current_account = []                   
                    try:
                        saving_account = bank_account['saving_account']
                    except:
                        saving_account = []
                    #checking if the current account and saving account both are present
                    if(len(current_account)!=0 and len(saving_account)!=0):
                        while True:
                            try:                    #if non integer type input 
                                choice=int(input('''
Enter the account you want to send from
1. Saving
2. Current
choice: '''))
                                break
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                print("!!Wrong Input!!")
                        if choice==1:
                            # if user has more than one saving account
                            if len(saving_account)>1:
                                #account to be selected
                                account_choice=int(input("Enter the account number you want to withdraw from : "))
                                #amount to be transferred
                                amount = int(input("Enter the amount you want to send : "))
                                #checking balance 
                                if user_details[sender_index]['other_information']['saving_account'][account_choice-1]['balance']<amount:
                                    print('Not Sufficient Balance')

                                else:
                                    #amount deducted from balance
                                    user_details[sender_index]['other_information']['saving_account'][account_choice-1]['balance']-=amount
                            #if user has one savings account than        
                            elif len(saving_account)==1:
                                amount = int(input("Enter the amount you want to send : "))
                                if user_details[sender_index]['other_information']['saving_account'][0]['balance']<amount:
                                    print('Not Sufficient Balance')
                            
                                else:
                                    user_details[sender_index]['other_information']['saving_account'][0]['balance']-=amount
                        #if user wants to transfer from current account            
                        elif choice==2:
                            amount = int(input("Enter the amount you want to send "))
                            #taking overdraft limit in variable
                            overdraft=user_details[sender_index]['other_information']['current_account'][0]['overdraft_limit']
                            #comparing balance+overdraft with amount needed
                            if amount>(current_account[0]['balance']+overdraft):
                                print('Not Sufficient Balance')
                                amount =0
                            else:
                                user_details[sender_index]['other_information']['current_account'][0]['balance']-= amount  
                    #if user has only one current account
                    elif(len(current_account)!=0):
                        amount = int(input("Enter the amount you want to send : "))
                        overdraft=user_details[sender_index]['other_information']['current_account'][0]['overdraft_limit']
                        if amount>(current_account[0]['balance']+overdraft):
                            print('Not Sufficient Balance')
                        
                        else:
                            user_details[sender_index]['other_information']['current_account'][0]['balance']-= amount                          
                    #if user has only saving account
                    else:
                        if len(saving_account)>1:
                                account_choice=int(input("Enter the account number you want to withdraw from : "))
                                amount = int(input("Enter the amount you want to send "))
                                if user_details[sender_index]['other_information']['saving_account'][account_choice-1]['balance']<amount:
                                    print('Not Sufficient Balance')
                                else:
                                    user_details[sender_index]['other_information']['saving_account'][account_choice-1]['balance']-=amount
                        elif len(saving_account)==1:
                                amount = int(input("Enter the amount you want to send "))
                                if user_details[sender_index]['other_information']['saving_account'][0]['balance']<amount:
                                    print('Not Sufficient Balance')
                                else:
                                    user_details[sender_index]['other_information']['saving_account'][0]['balance']-=amount

                    #Receiver End
                    bank_account = receiver_data['other_information']             
                    try:
                        current_account = bank_account['current_account']                    
                    except:
                        current_account = []                   
                    try:
                        saving_account = bank_account['saving_account']
                    except:
                        saving_account = [] 
                    #Receiver's type of account
                    if(len(current_account)!=0 and len(saving_account)!=0):
                        while True:
                            try:
                                choice=int(input('''
Enter the account you want to send to
1. Saving
2. Current
Choice : '''))
                                break
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                print("!!Wrong Input!!")

                        # Savings account transfer
                        if choice==1:
                            if len(saving_account)>1:
                                account_choice=int(input("Enter the account number you want to withdraw from : "))
                                user_details[receiver_index]['other_information']['saving_account'][account_choice-1]['balance']+=amount
                            elif len(saving_account)==1:
                                user_details[receiver_index]['other_information']['saving_account'][0]['balance']+=amount

                        # Current account transfer
                        elif choice==2:
                            user_details[receiver_index]['other_information']['current_account'][0]['balance']+= amount  

                    
                    elif(len(current_account)!=0):
                        user_details[receiver_index]['other_information']['current_account'][0]['balance']+= amount                          
                    else:
                        if len(saving_account)>1:
                                account_choice=int(input("Enter the account number you want to deposit to : "))
                                user_details[receiver_index]['other_information']['saving_account'][account_choice-1]['balance']+=amount
                        elif len(saving_account)==1:
                                user_details[receiver_index]['other_information']['saving_account'][0]['balance']+=amount
            #closing file
            file.close()
            #Writing updated value in the file
            with open("UserDetails.json",'w') as file:
                json.dump(user_details, file, indent=4)
            file.close()


        #Account Management
        if choice ==4:
            while(True):
                try:          #exception handling for non integer type values
                    ch = int(input('1.Create User\n2.Delete User\n3.Delete Account\n4.Create account of an existing user\n5.Quit\nChoice : '))
                    break
                except KeyboardInterrupt:
                    print("goodbye")
                    exit()
                except:
                    print("!!Wrong Input!!")    
                
            # create user operation
            if ch ==1:
                user = {}
                usrname = input("Please enter the username : ")
                user["username"] = usrname
                password = input("Please enter the password : ")
                user["password"] = password
                user['user_type'] = 'user'
                address = input("Enter the address of the user : ")
                user['other_information'] = {}
                user['other_information']['address'] = address
                while True:
                    try:
                        chc = int(input('''
Enter the account you want to create 
1. Current
2. Saving 
choice : '''))
                        break
                    except KeyboardInterrupt:
                        print("goodbye")
                        exit()
                    except:
                        print("!!Wrong Input!!")
                if chc ==1:
                    current_account = []
                    account= {}
                    while True:
                        try:                #exception handling for non integer type inputs
                            overdraft_limit = int(input('Enter the overdraft limit for this current account : '))
                            if(overdraft_limit<=1000 and overdraft_limit>=0):
                                break
                        except KeyboardInterrupt:
                            print("goodbye")
                            exit()
                        except:
                            print("!!Wrong Input!!")
                    while True:
                        try:                #exception handling for non integer type inputs
                            balance = int(input("Enter the balance in the account : "))
                            break
                        except KeyboardInterrupt:
                            print("goodbye")
                            exit()
                        except:
                            print("!!Wrong Input!!")
                    account['overdraft_limit']= overdraft_limit
                    account['balance']= balance
                    current_account.append(account)
                    user['other_information']['current_account'] = current_account
                elif chc ==2:
                    saving_account = []
                    accounts = int(input("Enter the number of accounts you want to create : "))
                    for i in range(accounts):
                        account = {}
                        account['number'] = i+1
                        print(f'Account number - > {i+1}')
                        while True:
                            try:
                                interest_rate = float(input('Enter the interest rate for this account : '))
                                if(interest_rate>=0.01 and interest_rate<=5.00):
                                    break
                            except:
                                print("!!Wrong Input!!")
                        while True:
                            try:
                                balance = int(input('Enter the balance in this account : '))
                                break
                            except:
                                print("!!Wrong Input!!")
                        account['interest_rate'] = interest_rate
                        account['balance'] = balance
                        saving_account.append(account)
                    user['other_information']['saving_account'] = saving_account    
                with open("UserDetails.json", "r") as file:
                    user_details = json.load(file)
                    file.close()    
                    
                    user_details.append(user)
                with open("UserDetails.json",'w') as file:
                    json.dump(user_details, file, indent=4)


            # Delete user operation
            elif ch == 2:
                with open("UserDetails.json", "r") as file:
                    user_details = json.load(file)
                file.close()
                Name=input("Enter the username you want to delete : ")
                flag=False
                for user in user_details:
                    if user['username'] == Name:
                        flag=True
                        print('Username found')
                        indx=user_details.index(user)
                        break
                if(flag==False):
                    print("No User found with this name")
                else:
                    user_details.pop(indx)
                    with open("UserDetails.json", "w") as file:
                        json.dump(user_details,file,indent=4)

            # Delete account operation
            elif ch == 3:
                with open("UserDetails.json", "r") as file:
                    user_details = json.load(file)
                file.close()
                Name=input("Enter the username whose account you want to delete : ")
                for user in user_details:
                    if user['username'] == Name:
                        print('Username found')
                        indx=user_details.index(user)
                print("--Account list--")
                print("Please select an option:")
                i=0

                if "current_account" in user_details[indx]["other_information"].keys():
                    i+=1
                    print(f"{i} - current account : £",user_details[indx]["other_information"]["current_account"][i-1]["balance"])
                if "saving_account" in user_details[indx]["other_information"].keys():
                    for n in range(0,len(user_details[indx]["other_information"]["saving_account"])):
                        i+=1
                        print(f"{i} - Saving account : £",user_details[indx]["other_information"]["saving_account"][i-1]["balance"] )

                while(True):
                    try:
                        opt = int(input('Enter a number to select your option: '))
                        break
                    except KeyboardInterrupt:
                        print("goodbye")
                        exit()
                    except:
                        print("\n!!Wrong selection!!\n\tOnly Integers are allowed\n\n")

                if opt==1:
                    if "current_account" in user_details[indx]["other_information"].keys():
                        user_details[indx]["other_information"].pop("current_account")
                    elif (len(user_details[indx]["other_information"]["saving_account"]))>1:
                        user_details[indx]["other_information"]["saving_account"].pop(opt-1)

                elif opt>1 and opt<=i:
                    user_details[indx]["other_information"]["saving_account"].pop(opt-1)
                else:
                    print("\n!!Wrong selection!!\n")

                with open("UserDetails.json", "w") as file:
                    user_details = json.dump(user_details,file,indent=4)

            # Create account for an existing user
            elif ch == 4:
                with open("UserDetails.json", "r") as file:
                    user_details = json.load(file)
                    file.close()
                username = input('Enter the username : ')
                for index in range(0,len(user_details)):
                    if user_details[index]['username']==username:
                        user_index = index
            
                user_data = user_details[user_index]
                bank_account = user_data['other_information']             
                try:
                    #storing current account details
                    current_account = bank_account['current_account']                    
                except:
                    #initialsing current account list if details not found
                    current_account = []                   
                try:
                    saving_account = bank_account['saving_account']
                except:
                    saving_account = []
                while True:
                    try:            #exception handling for non integer inputs
                        account_choice = int(input('Enter the type of account you want to create \n1.saving\t2.Current \n choice : '))
                        break
                    except:
                        print("!!Wrong input!!")

                #savings account
                if account_choice == 1:
                    while True:
                        try:
                            accounts = int(input("Enter the number of accounts you want to create : "))
                            break
                        except:
                            print("!!Wrong Input!!")
                    if len(saving_account)!=0:
                        count = saving_account[-1]['number']
                    else:
                        count = 0
                    
                    for i in range(0,accounts):
                        account = {}
                        account['number'] = count+i+1
                        print(f'Account number - > {i+1}')
                        while True:
                            try:
                                interest_rate = float(input('Enter the interest rate for this account : '))
                                if(interest_rate>=0.01 and interest_rate<=5.00):
                                    break
                            except:
                                print("!!Wrong Input!!")
                        while True:
                            try:
                                balance = int(input('Enter the balance in this account : '))
                                break
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                print("!!Wrong Input!!")
                        account['interest_rate'] = interest_rate
                        account['balance'] = balance
                        saving_account.append(account)
                        user_details[user_index]['other_information']['saving_account'] = saving_account

                #current account
                elif account_choice == 2:
                    if len(current_account)!=0:             #only one current account per user is allowed
                        print("Can't create more than one current account")
                    else:
                        account= {}
                        while True:
                            try:                #exception handling for non integer type inputs
                                overdraft_limit = int(input('Enter the overdraft limit for this current account : '))
                                if(overdraft_limit<=1000 and overdraft_limit>=0):
                                    break
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                print("!!Wrong Input!!")
                        while True:
                            try:                #exception handling for non integer type inputs
                                balance = int(input("Enter the balance in the account : "))
                                break
                            except KeyboardInterrupt:
                                print("goodbye")
                                exit()
                            except:
                                print("!!Wrong Input!!")
                        account['overdraft_limit'] = overdraft_limit
                        account['balance']= balance
                        current_account.append(account)
                        user_details[user_index]['other_information']['current_account'] = current_account 
                
                #updating file
                with open("UserDetails.json",'w') as file:
                    json.dump(user_details, file, indent=4)
            elif ch==5:
                pass
            else:
                print("Please enter the correct choice !")   