import os
import pandas as pd

scoreSheetDir = '/Users/hammerchu/Desktop/IVE/3703/scoreSheets/'
studentList = '/Users/hammerchu/Desktop/IVE/3703/download/studentList/IVE-CLASS-MATH-IIA-JAN2022 - 3703.csv'
outfileXLS = '/Users/hammerchu/Desktop/IVE/3703/scoreSheets/scoreList.xlsx'
outfileCSV = '/Users/hammerchu/Desktop/IVE/3703/scoreSheets/scoreList.csv'

scoreAccessA = []
scoreAccessB = []
scoreVisioA = []
scoreVisioB = []
allScore = []
def calculateSubtotal(filepath): # sum up the scoreSheet 
    total = 0
    with open(filepath) as f:
        lines = f.readlines()
        for line in lines:
            scores = line.split(',')
            for score in scores:
                # print(  int(score.split(':')[-1].replace('\n', '') ) )
                print(score.split(':')[-1].replace('\n', '') )
                if score.split(':')[-1].replace('\n', '') == '' or score.split(':')[-1].replace('\n', '') == ' ' :
                    score = 0
                else:
                    score = int(score.split(':')[-1].replace('\n', '') )
                total = score + total
    
    return total


def prepare():
    # loop though all the scoreSheet
    sections = os.listdir(scoreSheetDir)
    scoreAA = 0
    scoreAB = 0
    scoreVA = 0
    scoreVB = 0
    
    for section in sections:
        if os.path.isdir(os.path.join(scoreSheetDir, section)):
            print(section)
            groups = os.listdir(os.path.join(scoreSheetDir, section))

            for group in groups:
                if os.path.isdir(os.path.join(scoreSheetDir, section, group)):
                    print('--', group)
                    students = os.listdir(os.path.join(scoreSheetDir, section, group) )
                    for student in students:
                        path = os.path.join(scoreSheetDir, section, group, student)
                        if path.endswith('.txt'):

                            #calculate total score 
                            studentSectionScore = calculateSubtotal(os.path.join(scoreSheetDir, section, group, student))
                            studentId = student.split('.')[0].split(' ')[0]
                            studentName = student.split('.')[0].replace(studentId, '')
                            studentName = studentName.split(' ')[-1] + studentName.replace(studentName.split(' ')[-1], '' )
                            

                            if section == 'accessPartA':
                                scoreAccessA.append((studentId, studentName, group, studentSectionScore) )
                            elif section == 'accessPartB':
                                scoreAccessB.append((studentId, studentName, group, studentSectionScore ))
                            elif section == 'visioPartA':
                                scoreVisioA.append((studentId, studentName, group, studentSectionScore) )
                            elif section == 'visioPartB':
                                scoreVisioB.append((studentId, studentName, group, studentSectionScore) )
                            # print(scoreAccessB)
                            # d = (studentId, studentName, group, scoreAccessA, scoreAccessB, scoreVisioA, scoreVisioB )
                            # allScore.append(d)


def export():
    name = ['accessPartA', 'accessPartB', 'visioPartA', 'visioPartB']
    for index, i in enumerate([scoreAccessA, scoreAccessB, scoreVisioA, scoreVisioB]):
        print('-'*30)
        scoreDf = pd.DataFrame.from_records(columns=('id', 'name', 'group', 'score'), data=i)
        sortedDf = scoreDf.sort_values(by=['group', 'name'])
        print(sortedDf)
        outfile = os.path.join(scoreSheetDir, 'scoreList.csv').replace('.csv', '-'+ name[index] + '.csv')
        sortedDf.to_csv(outfile)



if __name__ == "__main__":
    prepare() #test comment for git
    export()
