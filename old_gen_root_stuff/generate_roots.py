from process_roots import ProcessRoots

root_files = ["withW.root",
                "withWv2.root",
                "withWv3.root",
                "withoutW.root",
                "withoutWv2.root",
                "withoutWv3.root"]

choice = raw_input('''Choose files to process

1 for only withW.root
2 for only withoutW.root
3 for both of the above
4 for all with tungsten
5 for all without tungsten
6 to run all
7 for custom file

Choice:  ''')

if choice == "1":
    files_to_run = [root_files[0]]
elif choice == "2":
    files_to_run = [root_files[3]]
elif choice == "3":
    files_to_run = [root_files[0], root_files[3]]
elif choice == "4":
    files_to_run = root_files[0:3]
elif choice == "5":
    files_to_run = root_files[3:6]
elif choice == "6":
    files_to_run = root_files[0:6]
elif choice == "7":
    files_to_run = [raw_input("Enter filename: ")]
else:
    print("invalid")    
    exit()

options = raw_input('''Choose what to do

2 for building
3 for regressing
5 for plotting

To do more than one, multiply the ones you want (since each combo will have a unique prime factorization)

Example: 2 * 3 = 6 for building and plotting, 2 * 3 * 5 = 30 for all three


Choice:  ''')

ProcessRoots(files_to_run, options).process()
raw_input("Press enter to quit...")
exit()