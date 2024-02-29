
from basic import queryFalse, xorOperation, powerOperation, startSATsolver, solveSTP, general3CopyOperation,genxorOperation

import sys
import os
import subprocess
PATH_CRYPTOMINISAT = "/home/minions/stp-master/scripts/deps/deps/cms/build/cryptominisat5"
PATH_STP = "/home/minions/tools/stp/build/stp"
def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b


def findModReverse(a, m):
    if gcd(a, m) != 1:
        print("Invalid block size!")
        return None

    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m

    while v3 != 0:
        q = u3//v3
        v1, v2, v3, u1, u2, u3 = (u1-q*v1), (u2-q*v2), (u3-q*v3), v1, v2, v3
    #print(u1 % m)

    return u1 % m

def Alg1(N_i, n):
    finish = 0
    while finish == 0:
        finish = 1
        nonzero = 1
        # print("N_I",N_i)
        for i in range(n):
            if N_i[i] >= 2**n-1:
                return n
            elif N_i[i] >= 3:
                finish = 0
            elif N_i[i] == 0:
                nonzero = 0
        if nonzero == 1:
            # print("nonzero")
            return n
        if finish == 0:
            for i in range(n):
                if N_i[i] % 2 == 1:
                    N_i[(i+1) % n] = N_i[(i+1) % n]+(N_i[i]-1)/2
                    N_i[i] = 1
                elif N_i[i] > 0 and N_i[i] % 2 == 0:
                    N_i[(i+1) % n] = N_i[(i+1) % n]+(N_i[i]-2)/2
                    N_i[i] = 2
    d = 0
    # print("N_i")
    # print("N_i",N_i)
    for i in range(n):
        if N_i[i] > 0:
            d += 1
    return d


def Calculate_Ni(k0, k1, k2, r, n):

    N_0 = [0 for i in range(n)]
    N_0[0] = 1
    # print(len(N_0))
    N = [[]for i in range(r)]
    N[0] = N_0
    for i in range(r-1):
        temp = [0 for i in range(n)]
        for j in range(n):
            temp[j] = int(N[i][(j-k1-k2) % n]+N[i][(j-k0-k2) % n])
        N[i+1] = temp

    # for i in N:
    #     print(i)
    # print("AL1 Sol:")
    # for i in range(1, r):
    #     print("Round {}, Degree {}".format(i, Alg1(N[i], n)))
    return N[r-1]


def genVariable(n, r, f):
    context = ""
    
    for i in range(r+1):
        for j in range(3):
            context += "x_{}_{} : BITVECTOR({});\n".format(i, j, n)
    context += "\n"

    for i in range(r):
        for j in range(3):
            context += "k_{}_{} : BITVECTOR({});\n".format(i, j, n)
    context += "\n"
    
    for i in range(r):
        for j in range(3):
            context += "y_{}_{} : BITVECTOR({});\n".format(i, j, n)
    context += "\n"
    
    for i in range(r):
        for j in range(3):
            context += "z_{}_{} : BITVECTOR({});\n".format(i, j, n)
    context += "\n"

    
    for i in range(r):
        for j in range(3):
            for k in range(3):
                context+="z_{}_{}_{} : BITVECTOR({});\n".format(i,j,k,n)


    context += "\n"

    f.write(context)




def genWeightVariable(n, r, f):
    addstr = "0bin" + "0".zfill(n-1)
    command = ""

    command += "wx0 : BITVECTOR(" + str(n) + ");\n"
    command += "ASSERT wx0 = BVPLUS({}".format(n)
    for b in range(n):
        command += "," + addstr + "@(x_0_0[{}:{}])".format(b, b)
        # command += "," + addstr + "@(x_0_1[{}:{}])".format(b, b)
        # command += "," + addstr + "@(x_0_2[{}:{}])".format(b, b)
    command += ");\n\n"
    command += "\n"

    command += "\n"

    f.write(command)


def rangeVariable(n, r, fw):
    command = ""

    degree_str = "{:b}".format(pow(2, n)-1)
    degree_str = "0bin" + degree_str.zfill(n)

    for i in range(r+1):
        for j in range(3):
            command += "ASSERT BVLE( x_{}_{}".format(i, j) + \
                ", " + degree_str + ");\n"
    command += "\n"
    for i in range(r):
        for j in range(3):
            command += "ASSERT BVLE( y_{}_{}".format(i, j) + \
                ", " + degree_str + ");\n"
    command += "\n"
    for i in range(r):
        for j in range(3):
            command += "ASSERT BVLE( z_{}_{}".format(i, j) + \
                ", " + degree_str + ");\n"
    command += "\n"

    for i in range(r):
        for j in range(3):
            for k in range(3):
                command+="ASSERT BVLE( z_{}_{}_{},{});\n".format(i,j,k,degree_str)
    command+="\n"
    for i in range(r):
        for j in range(3):
            command += "ASSERT BVLE( k_{}_{}".format(i, j) + \
                ", " + degree_str + ");\n"
    command += "\n"

    for i in range(r+1):
        for j in range(3):
            command += "ASSERT BVGE( x_{}_{}".format(i, j) + \
                ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"
    for i in range(r):
        for j in range(3):
            command += "ASSERT BVGE( y_{}_{}".format(i, j) + \
                ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"
    for i in range(r):
        for j in range(3):
            command += "ASSERT BVGE( z_{}_{}".format(i, j) + \
                ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"
    for i in range(r):
        for j in range(3):
            command += "ASSERT BVGE( k_{}_{}".format(i, j) + \
                ", 0bin" + "0".zfill(n) + ");\n"
    command += "\n"

    for i in range(r):
        for j in range(3):
            for k in range(3):
                command+="ASSERT BVGE( z_{}_{}_{},0bin{});\n".format(i,j,k,"0".zfill(n))
    command+="\n"

    fw.write(command)


def finalConstraint(n, r, fw, mode):
    command = ""
    test_degree1 = "{:b}".format(1)
    test_degree0 = "{:b}".format(0)
    if mode == 0:
        command += "ASSERT x_{}_{}".format(r, 0) + \
            " = 0bin" + test_degree1.zfill(n) + ";\n\n"
        command += "ASSERT x_{}_{}".format(r, 1) + \
            " = 0bin" + test_degree0.zfill(n) + ";\n\n"
        command += "ASSERT x_{}_{}".format(r, 2) + \
            " = 0bin" + test_degree0.zfill(n) + ";\n\n"
    if mode == 1:
        command += "ASSERT x_{}_{}".format(r, 0) + \
            " = 0bin" + test_degree0.zfill(n) + ";\n\n"
        command += "ASSERT x_{}_{}".format(r, 2) + \
            " = 0bin" + test_degree0.zfill(n) + ";\n\n"
        command += "ASSERT x_{}_{}".format(r, 1) + \
            " = 0bin" + test_degree1.zfill(n) + ";\n\n"
    if mode == 2:
        command += "ASSERT x_{}_{}".format(r, 0) + \
            " = 0bin" + test_degree0.zfill(n) + ";\n\n"
        command += "ASSERT x_{}_{}".format(r, 1) + \
            " = 0bin" + test_degree0.zfill(n) + ";\n\n"
        command += "ASSERT x_{}_{}".format(r, 2) + \
            " = 0bin" + test_degree1.zfill(n) + ";\n\n"

    fw.write(command)


def roundConstraint(n, r, d, dl, fw):
    command = ""
    for i in range(r):
        for j in range(3):

            

            strIn = [0, 0]
            strIn[0] = "x_{}_{}".format(i, j)
            strIn[1] = "k_{}_{}".format(i, j)
            strOut = "y_{}_{}".format(i, j)
            command = xorOperation(strIn, strOut, n, command)
            command += "\n"

            
            
            strIn = "y_{}_{}".format(i, j)
            strOut = "z_{}_{}".format(i, j)
            command = powerOperation(strIn, strOut, n, d*dl, command)
            command += "\n"


            

            
            strIn="z_{}_{}".format(i,j)
            strOut=[]
            for k in range(3):
                strOut.append("z_{}_{}_{}".format(i,j,k))
            command =general3CopyOperation(strIn, strOut,n, command)

            command += "\n"

            
            command += "\n"
    for i in range(r):
        
        strOut="x_{}_{}".format(i+1,0)  
        strIn=[]
        for j in range(3):
            # strIn=[]
              
            # for k in range(3):
            # for k in range(3):
            strIn.append("z_{}_{}_{}".format(i,j,0))
        command=genxorOperation(strIn, strOut, n,command)

        command += "\n"
    
    for i in range(r):
        
        strOut="x_{}_{}".format(i+1,1) 
        strIn=[] 
        for j in range(3):
            # strIn=[]
            # strOut="x_{}_{}".format(i+1,j)    
            # for k in range(3):
            # for k in range(3):
            strIn.append("z_{}_{}_{}".format(i,j,1))
        command=genxorOperation(strIn, strOut, n,command)

        command += "\n"
    
    for i in range(r):
        
        strOut="x_{}_{}".format(i+1,2) 
        strIn=[] 
        for j in range(3):
            # strIn=[]
            # strOut="x_{}_{}".format(i+1,j)    
            # for k in range(3):
            # for k in range(3):
            strIn.append("z_{}_{}_{}".format(i,j,2))
        command=genxorOperation(strIn, strOut, n,command)

        command += "\n"

    
    fw.write(command)
def initialize(n,f):
    command =""
    for i in range(1,3):
        command +="ASSERT x_{}_{}=0bin".format(0,i)+"0".zfill(n)+";\n"
    f.write(command)    
        
    
def running(stp_file):
    stp_parameters = [PATH_STP, stp_file, "--CVC"]
    result = subprocess.check_output(stp_parameters)

    return result.decode("utf-8")
def SatSolver(stp_file):
    subprocess.check_output([PATH_STP, "--exit-after-CNF", "--output-CNF",
                            stp_file, "--CVC", "--disable-simplifications"])

    # if test
    # Find the number of solutions with the SAT solver
    sat_params = [PATH_CRYPTOMINISAT, "--maxsol", str(1000000000),
                  "--verb", "0", "--printsol", "0", "output_0.cnf"]

    sat_process = subprocess.Popen(
        sat_params, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    return sat_process

def searchMonomial(n, r, d, dl, testweight, mode):
    stp_file = "chaghri_{}_{}.cvc".format(n, r)
    f = open(stp_file, "w+")
    command = "%Block size: " + \
        str(n) + "\n%Round = " + str(r) + "\n%Test weight " + "\n"

    f.write(command)

    genVariable(n, r, f)
    genWeightVariable(n, r, f)
    rangeVariable(n, r, f)

    # initialize(n,f)
    finalConstraint(n, r, f, mode)
    roundConstraint(n, r, d, dl, f)

    testdegree = "{:b}".format(testweight)

    testdegree = testdegree.zfill(n)

    command = "ASSERT wx0 = 0bin{};\n".format(testdegree)

    f.write(command)
    queryFalse(f)
    f.close()

    # =====running=====
    result_filename="result{}_{}".format(n,r)
    f_result=open(result_filename,"w+")
    result=running(stp_file)

    f_result.write("testdegree: {}\n".format(testweight))
    f_result.write(result)

    f_result.close()

    

    flag=0
    if "Invalid" in result:
        wx_filename="weight.csv"
        f_weight=open(wx_filename,"a")
        w_parameters=["grep","wx0 =",result_filename]
        result_w=subprocess.check_output(w_parameters)

        # f_weight.write("="*50+"\n")
        f_weight.write("round:{}\ntestdegree:{}\n{}\n".format(r,testweight,result_w.decode("utf-8")))
        # f_weight.write("="*50+"\n")
        f_weight.close()
        flag=1
    return flag


def CoeGroup(k0,k1,k2,n,r):
    Nr = Calculate_Ni(k0, k1, k2, r+1, n)
    #print("N{}:{}".format(r,Nr))
    d = Alg1(Nr, n)
    ##print("degree:",d)
    return d

import time
def Chaghri():
    k0=32
    k1=0
    k2=3
    n=63
    begin=int(input("begin round"))
    end=int(input("end round"))
    testweight=[2,3,5,7,9,12,14,17,19,22,24,27,30,32,35,37,40,42,45,47,50,52,55,58,60,62,63,63]
    for r in range(begin,end):

        # test_degree=CoeGroup(k0,k1,k2,n,r)
        test_degree=int(input("test degree"))
        # for i in range(test_degree+1,0,-1):
        #     start_time=time.time()
        #     flag=searchMonomial(n, r, (2**k0)+(2**k1), 2**k2, i, 0)
        #     if flag==1:
        #         end_time = time.time()-start_time
        #         print("TestRound:{},x0_degree:{}".format(r, i))
        #         print("Time:",end_time)
        #         break
        start_time=time.time()
        flag=searchMonomial(n, r, (2**k0)+(2**k1), 2**k2, test_degree, 0)
        if flag==1:
            end_time = time.time()-start_time
            print("TestRound:{},x0_degree:{}".format(r, test_degree))
            print("Time:",end_time)
            break
        else:
            end_time = time.time()-start_time
            print("Time:",end_time)

        # start_time=time.time()
        # flag = searchMonomial(n,testRound,(2**k0)+(2**k1),2**k2,testweight[testRound-1],0)
        # # print(flag)
        # # print(testweight[testRound-1])
        # if flag==1:
        #     for i in range(testweight[testRound-1]+1,n+1):
        #         flag = searchMonomial(n,testRound,(2**k0)+(2**k1),2**k2,testweight[testRound-1],0)
        #         print(flag)
        #         if flag==0:
        #             end_time = time.time()-start_time
        #             print("Test round : {}\tWeight = {}\n".format(testRound,i-1))
        #             print("Time:",end_time)
        #             print("==========================")
        #             content+="Test round : {}\tWeight = {}\t Time : {}\n".format(testRound,i-1,end_time)
        #             break
        # else:
        #     for i in range(testweight[testRound-1]-1,0,-1):
        #         flag = searchMonomial(n,testRound,(2**k0)+(2**k1),2**k2,testweight[testRound-1],0)
        #         if flag==1:
        #             end_time = time.time()-start_time
        #             print("Test round : {}\tWeight = {}\n".format(testRound,i))
        #             print("Time:",end_time)
        #             print("==========================")
        #             content+="Test round : {}\tWeight = {}\t Time : {}\n".format(testRound,i-1,end_time)
        #             break
Chaghri()
print("Done!")