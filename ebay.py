
def get_max(temp):
    maxLen = 1
    newArr = []
    temp.sort()
    for i in temp:
        if i+1 in temp:
            newArr += [i]
        



#1,2,3,4,5
if __name__ == "__main__":
    temp=[5,2,99,1,4,100,3]
    get