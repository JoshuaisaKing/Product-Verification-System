import csv
import sys


while True:
    file = open('data.csv', 'r+')
    reader = csv.reader(file)
    writer = csv.writer(file)
    x = input("Enter The Operation that needs to be done: ")
    row = []
    if x == 'read' or x == 'Read' or x == 'READ':
        for i in reader:
            print(i)
    elif x == 'write' or x == 'Write' or x == 'WRITE':
        print("Enter Product Details in format:[Product_ID,Manufacturer,Barcode_Number,Sold]")
        file.seek(0, 2)
        pro_id= input("Enter Product Id: ")
        manufac = input("Enter Manufacturer Name: ")
        barcodenum = input("Enter Number on the barcode: ")
        sold = 'N'
        writer.writerow([pro_id, manufac, barcodenum, sold])
        file.close()
    else:
        print("Retry..")
    print()
    cont = input("Do you want to continue reading and/or writing operation?(Y/N)")
    if cont == 'Y' or cont == 'y':
        pass
    else:
        print('\nThank You For Adding Your Product Details!')
        sys.exit()
    file.close()
