import os
import pandas as pd
import csv
from shutil import copyfile
import shutil
# import createPDF

sourceFolder = '/Users/hammerchu/Desktop/IVE/3703/download/visio/'
workingFolder = '/Users/hammerchu/Desktop/IVE/3703/grade/visio/'
studentList = '/Users/hammerchu/Desktop/IVE/3703/download/studentList/IVE-CLASS-MATH-IIA-JAN2022 - 3703.csv'
scoreSheetTemplate = '../3703/download/exam/scoreSheetTemplate.txt'
absStudentDB = {'HLS':[], 'HS':[]}
goodStudentDB = {'HLS':[], 'HS':[]}


def main2():

    dirs = os.listdir(sourceFolder)
    for directory in dirs: 
        try:
            
            students = os.listdir(sourceFolder+directory) # get a list of student in each of the 4 folders


            groupName = directory.split('@')[1] # rename the folder name and use '@' as separastor, to extract class name
            # print(groupName)
            df = pd.DataFrame(students)
            df["full"] = df[0]
            df[0] = df[0].str.split('_')
            df[0] = df[0].str[0]
            df['groupName'] = groupName
            df['lastName'] = df[0].str.split()
            df['lastName'] = df['lastName'].str[0]
            df['firstName'] = df.apply(lambda x: x[0].replace( str(x['lastName']), ""), axis=1)
            df.drop(0,  axis=1, inplace=True)
            print('\ndata from moodle downloaded folders')
            print(df)
            print('\n')
            
            with open(studentList, 'r') as file:
                
                csvreader = csv.reader(file)
                header = next(csvreader)
                for row in csvreader:

                    isContain = 0

                    className = row[5]
                    firstName = row[2].strip()
                    lastName = row[1].strip()
                    id = row[0]
                    # print('\n\n---')
                    # print(df['lastName'])
                    # print(lastName)

                    # print('\n\n---')
                    # print(df['firstName'])
                    # print(firstName)
                    # t =  df['firstName'].str.contains(firstName).any()
                    t =  df['lastName'].str.contains(lastName).any() 
                    t = df['lastName'].str.contains(lastName).any() and df['firstName'].str.contains(firstName).any() 

                    isContain = len(   df[   df['lastName'].str.contains(lastName) & df['firstName'].str.contains(firstName)   ]['full']    ) # check if resp is true
                    print ( f'\n\n{className} @ {firstName} {lastName} - {isContain} ')
              
                    if isContain:
                        dfFileName = df[df['lastName'].str.contains(lastName) & df['firstName'].str.contains(firstName)]['full'].values[0] # save the src folder per student onto dfFileName
                    # print(f' dfFileName {dfFileName}')
                    # print(' className : ', className )
                    # print(' groupName : ', groupName )

                    if groupName == className:
                
                        if isContain:
                            # -* if the student's work is in the zip folder *-
                            # print(workingFolder + '/' + groupName + '/' + className +'/GOOD' + '/' + id+firstName+' '+lastName)
                            goodStudentDB[className].append( (id,firstName, lastName)  )
                            srcFolder = sourceFolder + directory +'/'+ str(dfFileName)
                            print(' srcFolder : ', srcFolder )
                            dstFolder = workingFolder + className +'/GOOD' + '/' + id+' '+firstName+' '+lastName
                            print(' dstFolder : ', dstFolder )
                            try:
                                os.makedirs(dstFolder, exist_ok=True ) # create a dst folder
                                copyFilesBtwFolders (srcFolder, dstFolder) # copy student jpgs to dst folder
                                
                                # # Test if folder has multiple image files, create a PDF out of those images
                                # if createPDF.isContainMultipleImgs(dstFolder) > 2:
                                #     createPDF.fromImgs(dirname, pdfName)
                                

                            except Exception as err:
                                print (err)
                                
                        else:
                            #-* if the student is LATE *-
                            # print(workingFolder + groupName + '/' + className +'/LATE' + '/' + id+' ' + firstName+' '+lastName)
                            absStudentDB[className].append( (id,firstName, lastName)  )
                            dstFolder = workingFolder + className +'/LATE' + '/' + id+' '+firstName+' '+lastName
                            print(' dstFolder : ', dstFolder )
                            try:
                                os.makedirs(dstFolder, exist_ok=True )
                                # if not os.path.exists(dstFolder+f"/scoresheet {id} {firstName} {lastName}.txt"):
                                #     shutil.copy(scoreSheetTemplate,  dstFolder+f"/scoresheet {id} {firstName} {lastName}.txt")
                            except Exception as err:
                                print (err)

        except Exception as Argument:
            print(Argument) 
            print('\n')  

    #'''Report'''
    # for i in goodStudentDB:
    #     print (i)
    #     total = len(goodStudentDB[i]) + len(absStudentDB[i])
    #     print ( f'   good student: {len(goodStudentDB[i])} / {total} ')
    #     print ( f'   abs student: {len(absStudentDB[i])} / {total} ')
    #     print('\n-------\n')
    #     if i == 'HS_D':
    #         print (i)
    #         for j in goodStudentDB[i]:
    #             print(j)
    #         print('--')
    #         for j in absStudentDB[i]:
    #             print(j)




def copyFilesBtwFolders (srcFolder, dstFolder):
    fileList = os.listdir(srcFolder)
    for item in fileList:
        # filename = os.path.basename(item[0])
        print ('src ', os.path.join(srcFolder, item),)
        print ('dst ', os.path.join(dstFolder, item),)
        copyfile(os.path.join(srcFolder, item), os.path.join(dstFolder, item))


if __name__ == "__main__":
    main2()

    # for i in goodStudentDB:
    #     print(i)
    # pyfiles