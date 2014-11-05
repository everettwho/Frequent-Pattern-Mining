# test script

search_for = ['407', '382', '225']
count = 0

data_file = open("data-assign3/topic-0.txt")

for line in data_file.readlines():
    data = line.rstrip().split(' ')
    flag = True

    for i in search_for:
        if i not in data:
            flag = False

    if flag:
        count += 1



print count
        

