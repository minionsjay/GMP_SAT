# from ulity import *
import subprocess
import time
import os
import sys
two_xor_new="-x -k 0\n-k y 0\n-x y 0\nx k -y 0\n"

three_xor_new="-z_1 -z_2 0\n-z_0 -z_2 0\n-z_0 -z_1 0\n-z_2 x 0\n-z_1 x 0\n-z_0 x 0\nz_0 z_1 z_2 -x 0\n"

power_new=['-q x y 0\n-c y 0\n-q -x -y 0\nq x -y 0\nc q -x 0\n-c x 0\n', 
           'q -x -y -g 0\n-q x y g 0\nc q -x 0\n-c -q x 0\nc -y -g 0\n-c y g 0\n-q -x y -g 0\nq x y -g 0\n-q -x -y g 0\nq x -y g 0\n', 
           'c -g 0\n-c g 0\n', 
           '-z q gg 0\n-c gg 0\n-z -q -gg 0\nz q -gg 0\nc z -q 0\n-c q 0\n']

III_copy_constraints_new=[
    'q -v_0 -v_1 -v_2 0\n-q v_0 v_1 v_2 0\nc_1 q -v_0 0\n-c_1 -q v_0 0\nc_1 -v_1 -v_2 0\n-c_1 v_1 v_2 0\n-q -v_0 v_1 -v_2 0\nq v_0 v_1 -v_2 0\n-q -v_0 -v_1 v_2 0\nq v_0 -v_1 v_2 0\n', 
    '-q v_0 v_1 v_2 c_1_0 0\n-c_3 c_1_0 0\n-c_3 v_2 0\nc_1_1 -q -v_2 -c_1_0 0\n-c_3 -c_1_1 0\nc_1_1 q v_1 -v_2 0\nc_1_1 q v_0 -v_1 0\nc_3 q -v_0 -v_1 -v_2 0\n-c_1_1 v_1 v_2 c_1_0 0\nc_1_1 q v_2 -c_1_0 0\nc_1_1 -q -v_0 -v_1 0\n-q v_0 -v_1 v_2 -c_1_0 0\n-c_1_1 v_0 v_1 v_2 0\n-q -v_0 v_1 v_2 -c_1_0 0\n-c_1_1 v_0 v_2 c_1_0 0\n-q v_0 -v_1 -v_2 c_1_0 0\n-c_1_1 v_0 v_1 c_1_0 0\n-q -v_0 v_1 -v_2 c_1_0 0\nc_1_1 q -v_0 c_1_0 0\n-q -v_0 -v_1 -v_2 -c_1_0 0\nq v_0 -v_1 -v_2 -c_1_0 0\nq -v_0 -v_1 v_2 -c_1_0 0\nq -v_0 v_1 -v_2 -c_1_0 0\n-c_1_1 -q v_0 v_1 0\n-c_1_1 -q v_2 c_1_0 0\n', 
    '-q v_0 v_1 v_2 c_1_1 0\n-c_3 c_1_1 0\n-c_3 v_2 0\nc_1_2 -q -v_2 -c_1_1 0\n-c_3 -c_1_2 0\nc_1_2 q v_1 -v_2 0\nc_1_2 q v_0 -v_1 0\nc_3 q -v_0 -v_1 -v_2 0\n-c_1_2 v_1 v_2 c_1_1 0\nc_1_2 q v_2 -c_1_1 0\nc_1_2 -q -v_0 -v_1 0\n-q v_0 -v_1 v_2 -c_1_1 0\n-c_1_2 v_0 v_1 v_2 0\n-q -v_0 v_1 v_2 -c_1_1 0\n-c_1_2 v_0 v_2 c_1_1 0\n-q v_0 -v_1 -v_2 c_1_1 0\n-c_1_2 v_0 v_1 c_1_1 0\n-q -v_0 v_1 -v_2 c_1_1 0\nc_1_2 q -v_0 c_1_1 0\n-q -v_0 -v_1 -v_2 -c_1_1 0\nq v_0 -v_1 -v_2 -c_1_1 0\nq -v_0 -v_1 v_2 -c_1_1 0\nq -v_0 v_1 -v_2 -c_1_1 0\n-c_1_2 -q v_0 v_1 0\n-c_1_2 -q v_2 c_1_1 0\n',
    # '-q v_0 v_1 v_2 c_1_0 0\n-c_3 c_1_0 0\n-c_3 v_2 0\nc_1_1 -q -v_2 -c_1_0 0\n-c_3 -c_1_1 0\nc_1_1 q v_1 -v_2 0\nc_1_1 q v_0 -v_1 0\nc_3 q -v_0 -v_1 -v_2 0\n-c_1_1 v_1 v_2 c_1_0 0\nc_1_1 q v_2 -c_1_0 0\nc_1_1 -q -v_0 -v_1 0\n-q v_0 -v_1 v_2 -c_1_0 0\n-c_1_1 v_0 v_1 v_2 0\n-q -v_0 v_1 v_2 -c_1_0 0\n-c_1_1 v_0 v_2 c_1_0 0\n-q v_0 -v_1 -v_2 c_1_0 0\n-c_1_1 v_0 v_1 c_1_0 0\n-q -v_0 v_1 -v_2 c_1_0 0\nc_1_1 q -v_0 c_1_0 0\n-q -v_0 -v_1 -v_2 -c_1_0 0\nq v_0 -v_1 -v_2 -c_1_0 0\nq -v_0 -v_1 v_2 -c_1_0 0\nq -v_0 v_1 -v_2 -c_1_0 0\n-c_1_1 -q v_0 v_1 0\n-c_1_1 -q v_2 c_1_0 0\n', 
    'q -v_0 -v_1 -v_2 -c_1_0 -c_3_0 0\n-q v_0 v_1 v_2 c_1_0 c_3_0 0\n-c_3_1 -c_1_1 0\nc_3_1 c_1_1 q -v_0 0\nc_3_1 -v_0 -v_1 -v_2 -c_1_0 0\n-c_3_1 c_1_0 c_3_0 0\nc_1_1 v_0 v_1 -v_2 -c_1_0 0\nc_1_1 -q v_2 -c_1_0 -c_3_0 0\nc_1_1 -q v_0 -v_1 -v_2 0\nc_1_1 -q -v_0 c_1_0 -c_3_0 0\nc_1_1 q v_1 v_2 -c_1_0 0\nc_1_1 q v_2 c_1_0 -c_3_0 0\nc_1_1 -v_0 v_1 -v_2 c_3_0 0\nc_1_1 -q -v_0 -v_1 c_3_0 0\nc_1_1 q v_0 -v_1 c_3_0 0\n-c_1_1 v_1 v_2 c_1_0 c_3_0 0\n-q v_0 v_1 -v_2 c_1_0 -c_3_0 0\n-c_3_1 v_2 c_3_0 0\nc_3_1 q -v_1 -v_2 -c_1_0 0\n-q v_0 -v_1 v_2 c_1_0 -c_3_0 0\n-q -v_0 v_1 -v_2 -c_1_0 -c_3_0 0\nq v_0 -v_1 v_2 -c_1_0 -c_3_0 0\nq v_0 -v_1 -v_2 c_1_0 -c_3_0 0\nq -v_0 v_1 -v_2 c_1_0 -c_3_0 0\nc_1_1 q v_0 -v_2 c_1_0 0\n-c_1_1 v_0 v_1 v_2 c_1_0 0\n-c_1_1 v_0 v_1 v_2 c_3_0 0\n-c_1_1 v_0 v_1 c_1_0 c_3_0 0\n-c_1_1 v_0 v_2 c_1_0 c_3_0 0\n-c_1_1 q -v_0 -v_2 -c_1_0 0\n-c_1_1 q -v_0 -v_1 -c_1_0 0\n-c_1_1 q -v_0 -v_1 -v_2 0\n-q v_0 -v_1 v_2 -c_1_0 c_3_0 0\n-q -v_0 v_1 v_2 -c_1_0 c_3_0 0\n-c_1_1 -q v_0 v_1 v_2 0\n-c_1_1 -q v_1 v_2 c_1_0 0\n-c_1_1 -v_1 -v_2 -c_1_0 -c_3_0 0\n-c_1_1 -v_0 -v_1 -c_1_0 -c_3_0 0\n-c_1_1 -v_0 -v_1 -v_2 -c_3_0 0\n-c_1_1 q -v_2 -c_1_0 -c_3_0 0\n-c_1_1 -q v_0 v_1 c_3_0 0\n-c_1_1 q -v_0 -c_1_0 -c_3_0 0\n-c_1_1 -q v_0 c_1_0 c_3_0 0\n-c_1_1 -q v_1 c_1_0 c_3_0 0\n-c_1_1 q -v_0 -v_1 -c_3_0 0\n-c_1_1 -q v_2 c_1_0 c_3_0 0\n-c_3_1 v_2 c_1_0 0\n', 
    'c_2 -c_1 0\n-c_2 c_1 0\n', 
    '-p q c_2_0 0\n-c_2_1 c_2_0 0\n-p -q -c_2_0 0\np q -c_2_0 0\nc_2_1 p -q 0\n-c_2_1 q 0\n',
    # '-u q c_2_0 0\n-c_2_1 c_2_0 0\n-u -q -c_2_0 0\nu q -c_2_0 0\nc_2_1 u -q 0\n-c_2_1 q 0\n', 
    'p -q -c_2_0 -c_3 0\n-p q c_2_0 c_3 0\nc_2_1 p -q 0\n-c_2_1 -p q 0\nc_2_1 -c_2_0 -c_3 0\n-c_2_1 c_2_0 c_3 0\n-p -q c_2_0 -c_3 0\np q c_2_0 -c_3 0\n-p -q -c_2_0 c_3 0\np q -c_2_0 c_3 0\n',
    '-p q c_2_0 0\n-c_2_1 c_2_0 0\n-p -q -c_2_0 0\np q -c_2_0 0\nc_2_1 p -q 0\n-c_2_1 q 0\n',
    # 'u -q -c_2_0 -c_3 0\n-u q c_2_0 c_3 0\nc_2_1 u -q 0\n-c_2_1 -u q 0\nc_2_1 -c_2_0 -c_3 0\n-c_2_1 c_2_0 c_3 0\n-u -q c_2_0 -c_3 0\nu q c_2_0 -c_3 0\n-u -q -c_2_0 c_3 0\nu q -c_2_0 c_3 0\n', 
    'c_4 -c_2 0\n-c_4 c_2 0\n',
    # '-u q c_2_0 0\n-c_2_1 c_2_0 0\n-u -q -c_2_0 0\nu q -c_2_0 0\nc_2_1 u -q 0\n-c_2_1 q 0\n',
    '-u p c_4_0 0\n-c_4_1 c_4_0 0\n-u -p -c_4_0 0\nu p -c_4_0 0\nc_4_1 u -p 0\n-c_4_1 p 0\n'
    ]
and_constraints= 'x -y 0\ny -z 0\n-x z 0\n'


n=64

k0=1
k1=0
# k2=3
block_size=1
round_nvar=24*n+4

# print(round_nvar)
def generate_variables(begin_index,end_index,gap):
    two_dimensional_list = []


    for i in range(begin_index, end_index, gap):  
        sub_list = [str(j) for j in range(i, i + gap)]
        two_dimensional_list.append(sub_list)
    return two_dimensional_list

def Xor(x,k,y):
    content=""
    for i in range(block_size):
        for j in range(n):
            temp=two_xor_new
            temp=temp.replace("x","{}".format(x[i][j]))
            temp=temp.replace("k","{}".format(k[i][j]))
            temp=temp.replace("y","{}".format(y[i][j]))
            content+=temp
    return content

def And(x,y,z):
    content=""
    for i in range(block_size):
        for j in range(n):
            temp=and_constraints
            temp=temp.replace("x",f"{x[i][j]}")
            temp=temp.replace("y",f"{y[i][j]}")
            temp=temp.replace("z",f"{z[i][j]}")
            content+=temp
    return content
def Three_xor(z1,z2,z3,x):
    content=""
    for i in range(n):
        for j in range(block_size):
            temp=three_xor_new
            temp=temp.replace("x","{}".format(x[j][i]))
            temp=temp.replace("z_0","{}".format(z1[j][i]))
            temp=temp.replace("z_1","{}".format(z2[j][i]))
            temp=temp.replace("z_2","{}".format(z3[j][i]))
            content+=temp
    return content
### Power+Affine
# def Power_Affine(power_in,q,g1,g2,power_out,k0,k2): 
#     ### y (power+affine) ---> z
#     content=""
#     for i in range(block_size):
#         for j in range(n):
#             if j==0:
#                 temp=power_new[0]
#                 temp=temp.replace("x",power_out[i][(j-k2)%n])
#                 temp=temp.replace("y",power_out[i][(j-k0-k2)%n])
#                 temp=temp.replace("q",q[i][j])
#                 temp=temp.replace("c",g1[i][j])
#                 content+=temp

#                 temp=power_new[2]
#                 temp=temp.replace("c",g2[i][j])
#                 temp=temp.replace("g",g1[i][n-1])
#                 content+=temp

            
#             else:
#                 temp=power_new[1]
#                 temp=temp.replace("x",power_out[i][(j-k2)%n])
#                 temp=temp.replace("y",power_out[i][(j-k0-k2)%n])
#                 temp=temp.replace("q",q[i][j])
#                 temp=temp.replace("g",g1[i][j-1])
#                 temp=temp.replace("c",g1[i][j])
#                 content+=temp
    
#             temp=power_new[3]
#             temp=temp.replace("c",g2[i][j+1])
#             temp=temp.replace("z",power_in[i][j])
#             temp=temp.replace("q",q[i][j])
#             temp=temp.replace("gg",g2[i][j])
#             content+=temp
#     return content
def Two_Copy(copy_out_1,copy_out_2,q,g1,g2,copy_in): 
    ### y (power+affine) ---> z
    content=""
    for i in range(block_size):
        for j in range(n):
            if j==0:
                temp=power_new[0]
                temp=temp.replace("x",copy_out_1[i][j])
                temp=temp.replace("y",copy_out_2[i][j])
                temp=temp.replace("q",q[i][j])
                temp=temp.replace("c",g1[i][j])
                content+=temp

                temp=power_new[2]
                temp=temp.replace("c",g2[i][j])
                temp=temp.replace("g",g1[i][n-1])
                content+=temp

            
            else:
                temp=power_new[1]
                temp=temp.replace("x",copy_out_1[i][j])
                temp=temp.replace("y",copy_out_2[i][j])
                temp=temp.replace("q",q[i][j])
                temp=temp.replace("g",g1[i][j-1])
                temp=temp.replace("c",g1[i][j])
                content+=temp
    
            temp=power_new[3]
            temp=temp.replace("c",g2[i][j+1])
            temp=temp.replace("z",copy_in[i][j])
            temp=temp.replace("q",q[i][j])
            temp=temp.replace("gg",g2[i][j])
            content+=temp
    return content

def Weight_bound(x,bound,round):
    content=""
    s=generate_variables(round_nvar*round+3*n+1,round_nvar*round+3*n+1+(n-1)*bound,bound)
    # print(round_nvar)
    # print(s)
    content+="-{} {} 0\n".format(x[0],s[0][0])
    content+="{} -{} 0\n".format(x[0],s[0][0])
    for i in range(1,bound):
        content+="-{} 0\n".format(s[0][i])
    
    for i in range(1,n-1):
        content+="-{} {} 0\n".format(x[i],s[i][0])
        content+="-{} {} 0\n".format(s[i-1][0],s[i][0])
        content+="{} {} -{} 0\n".format(x[i],s[i-1][0],s[i][0])
        for j in range(1,bound):
            # cluses.append("({}'+{}'+{})".format(x[i],s[i-1][j-1],s[i][j]))
            # cluses.append("({}'+{})".format(s[i-1][j],s[i][j]))
            # cluses.append("({}')")
            content+="-{} {} 0\n".format(s[i-1][j],s[i][j])
            content+="-{} -{} {} 0\n".format(x[i],s[i-1][j-1],s[i][j])
            content+="{} {} -{} 0\n".format(x[i],s[i-1][j],s[i][j])
            content+="{} {} -{} 0\n".format(s[i-1][j-1],s[i-1][j],s[i][j])
        content+="-{} -{} 0\n".format(x[i],s[i-1][bound-1])

    ### x_{n-1} = 1 ==> s_{n-2,k-1}=0
    content+="-{} -{} 0\n".format(x[n-1],s[n-2][bound-1])
    ### x_{n-1} =1 ==> s_{n-2,k-2},...,s_{n-2,0}=1
    for i in range(bound-1):
        content+="-{} {} 0\n".format(x[n-1],s[n-2][i])

    ### x_{n-1} = 0 ==> s_{n-2,k-1},...,s_{n-2,0}=1
    for i in range(bound):
        content+="{} {} 0\n".format(x[n-1],s[n-2][i])


    return content
def Initial_final_constrants(round):
    content=""
    # for i in range(1,block_size):
    for j in range(n):
    #     # content+="-{} 0\n".format(K0[0][0][j])
    #     # content+="-{} 0\n".format(K1[0][0][j])
        content+="-{} 0\n".format(K0[round][0][j])
        content+="-{} 0\n".format(K1[round][0][j])

    for i in range(n):
        if i==0:
            content+="{} 0\n".format(X[round][0][i])
        else:
            content+="-{} 0\n".format(X[round][0][i])
    return content


def Run_sat(filename,round,solver):
    # os.chdir("./tmp_cnf")
    # sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
    sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
    cadical_parameters="/home/minions/tools/cadical-master/build/cadical {} -n".format(filename)
    stdout=""
    if solver=="cryptominisat5":
        result_new = subprocess.run(sat_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout=result_new.stdout
        if "UNSATISFIABLE" in stdout:
            print("UNSATISFIABLE")
            for j in range(round-2-1,0,-1):
                filename="Ciminion_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
                result_new = subprocess.run(sat_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    continue
                elif "SATISFIABLE" in result_new.stdout:
                    # print(round)
                    # print(j)
                    # break
                    return j

        elif "SATISFIABLE" in stdout:
            print("SAT")
            for j in range(round-2+1,n+1):
                filename="Ciminion_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
                result_new = subprocess.run(sat_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    # print(round)
                    # print(j-1)
                    return j-1
    elif solver=="cadical":
        result_new = subprocess.run(cadical_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout=result_new.stdout
        if "UNSATISFIABLE" in stdout:
            print("UNSATISFIABLE")
            for j in range(round-2-1,0,-1):
                filename="Ciminion_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                cadical_parameters="/home/minions/tools/cadical-master/build/cadical {} -n".format(filename)
                result_new = subprocess.run(cadical_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    continue
                elif "SATISFIABLE" in result_new.stdout:
                    # print(round)
                    # print(j)
                    # break
                    return j

        elif "SATISFIABLE" in stdout:
            print("SAT")
            for j in range(round-2+1,n+1):
                filename="Ciminion_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                cadical_parameters="/home/minions/tools/cadical-master/build/cadical {} -n".format(filename)
                result_new = subprocess.run(cadical_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    # print(round)
                    # print(j-1)
                    return j-1
    # if "UNSATISFIABLE" in stdout:
    #     return 1
    # else:
    #     return 0
    # return result.decode("utf-8")
X=[]#n
X0=[]#n
X1=[]#n
Copy_X_Q=[]#n
Copy_X_C1=[]#n
Copy_X_C2=[]#n+1

K0=[]#n
K00=[]#n
K01=[]#n
Copy_K0_Q=[]#n
Copy_K0_C1=[]#n
Copy_K0_C2=[]#n+1

Y=[]#n
K1=[]#n
Z0=[]#n
Z00=[]#n
# Z01=[]#n
Copy_Z0_Q=[]#n
Copy_Z0_C1=[]#n
Copy_Z0_C2=[]#n+1

Z1=[]#n
Z10=[]#n
# Z11=[]#n
Copy_Z1_Q=[]#n
Copy_Z1_C1=[]#n
Copy_Z1_C2=[]#n+1

def Generate_constraints(round,bound,filename):
    constraints=""

    for r in range(round):
        constraints+=Two_Copy(X0[r],X1[r],Copy_X_Q[r],Copy_X_C1[r],Copy_X_C2[r],X[r])
        constraints+=Two_Copy(K00[r],K01[r],Copy_K0_Q[r],Copy_K0_C1[r],Copy_K0_C2[r],K0[r])
        constraints+=And(X1[r],K01[r],Y[r])
        constraints+=Xor(Y[r],K1[r],Z0[r])
        constraints+=Two_Copy(X[r+1],Z00[r],Copy_Z0_Q[r],Copy_Z0_C1[r],Copy_Z0_C2[r],Z0[r])
        constraints+=Xor(Z00[r],K00[r],Z1[r])
        constraints+=Two_Copy(K1[r+1],Z10[r],Copy_Z1_Q[r],Copy_Z1_C1[r],Copy_Z1_C2[r],Z1[r])
        constraints+=Xor(Z10[r],X0[r],K0[r+1])
        
    constraints+=Weight_bound(X[0][0],bound,round)
    constraints+=Initial_final_constrants(round)

    num_variables=round_nvar*round+3*n+(n-1)*bound
    # print(constraints.count('\n'))
    num_constraints=constraints.count('\n')
    with open(filename,"w+") as file:
        file.write(f"p cnf {num_variables} {num_constraints}\n")
        file.write(constraints)
# bound=61


def Generate_variables(round,round_nvar):
    for r in range(round):
        X.append(generate_variables(1+r*round_nvar,n+1+r*round_nvar,n)) ## n
        X0.append(generate_variables(n+1+r*round_nvar,2*n+1+r*round_nvar,n)) ## n
        X1.append(generate_variables(2*n+1+r*round_nvar,3*n+1+r*round_nvar,n)) ## n
        Copy_X_Q.append(generate_variables(3*n+1+r*round_nvar,4*n+1+r*round_nvar,n)) ## n
        Copy_X_C1.append(generate_variables(4*n+1+r*round_nvar,5*n+1+r*round_nvar,n)) ## n
        Copy_X_C2.append(generate_variables(5*n+1+r*round_nvar,6*n+2+r*round_nvar,n+1)) ## n+1

        K0.append(generate_variables(6*n+2+r*round_nvar,7*n+2+r*round_nvar,n)) ## n
        K00.append(generate_variables(7*n+2+r*round_nvar,8*n+2+r*round_nvar,n)) ## n
        K01.append(generate_variables(8*n+2+r*round_nvar,9*n+2+r*round_nvar,n)) ## n
        Copy_K0_Q.append(generate_variables(9*n+2+r*round_nvar,10*n+2+r*round_nvar,n)) ## n
        Copy_K0_C1.append(generate_variables(10*n+2+r*round_nvar,11*n+2+r*round_nvar,n)) ## n
        Copy_K0_C2.append(generate_variables(11*n+2+r*round_nvar,12*n+3+r*round_nvar,n+1)) ## n+1

        Y.append(generate_variables(12*n+3+r*round_nvar,13*n+3+r*round_nvar,n)) ## n
        K1.append(generate_variables(13*n+3+r*round_nvar,14*n+3+r*round_nvar,n)) ## n

        Z0.append(generate_variables(14*n+3+r*round_nvar,15*n+3+r*round_nvar,n)) ## n
        Z00.append(generate_variables(15*n+3+r*round_nvar,16*n+3+r*round_nvar,n)) ## n
        # Z01.append(generate_variables(16*n+3+r*round_nvar,17*n+3+r*round_nvar,n)) ## n
        Copy_Z0_Q.append(generate_variables(16*n+3+r*round_nvar,17*n+3+r*round_nvar,n)) ## n
        Copy_Z0_C1.append(generate_variables(17*n+3+r*round_nvar,18*n+3+r*round_nvar,n)) ## n
        Copy_Z0_C2.append(generate_variables(18*n+3+r*round_nvar,19*n+4+r*round_nvar,n+1)) ## n+1

        Z1.append(generate_variables(19*n+4+r*round_nvar,20*n+4+r*round_nvar,n)) ## n
        Z10.append(generate_variables(20*n+4+r*round_nvar,21*n+4+r*round_nvar,n)) ## n
        # Z11.append(generate_variables(22*n+4+r*round_nvar,23*n+4+r*round_nvar,n)) ## n
        Copy_Z1_Q.append(generate_variables(21*n+4+r*round_nvar,22*n+4+r*round_nvar,n)) ## n
        Copy_Z1_C1.append(generate_variables(22*n+4+r*round_nvar,23*n+4+r*round_nvar,n)) ## n
        Copy_Z1_C2.append(generate_variables(23*n+4+r*round_nvar,24*n+5+r*round_nvar,n+1)) ## n+1
    X.append(generate_variables(1+round*round_nvar,n+1+round*round_nvar,n)) ## n
    K0.append(generate_variables(n+1+round*round_nvar,2*n+1+round*round_nvar,n)) ## n
    K1.append(generate_variables(2*n+1+round*round_nvar,3*n+1+round*round_nvar,n)) ## n




begin_round=int(sys.argv[1])
end_round=int(sys.argv[2])
print(begin_round,end_round)

solver=sys.argv[3]
result_content=""
result_file=f"{solver}_result.txt"
for i in range(begin_round,end_round):

    filename="Ciminion_round{}.cnf".format(i)
    Generate_variables(i,round_nvar)
    Generate_constraints(i,i-2,filename)

    start_time = time.time()
    degree=Run_sat(filename,i,solver)
    end_time = time.time()-start_time
    result_content="Round:{}, Maxdegree:{}, Time:{}\n".format(i,degree,end_time)
    with open(result_file,"a") as file:
        file.write(result_content) 
