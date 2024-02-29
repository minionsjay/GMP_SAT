# from ulity import *
import subprocess
import time
import os
two_xor_new="-x -k 0\n-k y 0\n-x y 0\nx k -y 0\n" # 4

three_xor_new="-z_1 -z_2 0\n-z_0 -z_2 0\n-z_0 -z_1 0\n-z_2 x 0\n-z_1 x 0\n-z_0 x 0\nz_0 z_1 z_2 -x 0\n" # 7

power_new=['-q x y 0\n-c y 0\n-q -x -y 0\nq x -y 0\nc q -x 0\n-c x 0\n', 
           'q -x -y -g 0\n-q x y g 0\nc q -x 0\n-c -q x 0\nc -y -g 0\n-c y g 0\n-q -x y -g 0\nq x y -g 0\n-q -x -y g 0\nq x -y g 0\n', 
           'c -g 0\n-c g 0\n', 
           '-z q gg 0\n-c gg 0\n-z -q -gg 0\nz q -gg 0\nc z -q 0\n-c q 0\n'] #24

II_copy_constraints_new=['-q x y 0\n-c y 0\n-q -x -y 0\nq x -y 0\nc q -x 0\n-c x 0\n', 
           'q -x -y -g 0\n-q x y g 0\nc q -x 0\n-c -q x 0\nc -y -g 0\n-c y g 0\n-q -x y -g 0\nq x y -g 0\n-q -x -y g 0\nq x -y g 0\n', 
           'c -g 0\n-c g 0\n', 
           '-z q gg 0\n-c gg 0\n-z -q -gg 0\nz q -gg 0\nc z -q 0\n-c q 0\n'] #24

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
    ] #139

n=63

k0=32
k1=0
h1=0
h2=3

block_size=3
round_nvar=4926

len_two_xor=4
len_three_xor=7
len_power=24
len_twocopy=24
len_threecopy=139
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
def Power_Affine(power_in,q,g1,g2,power_out,k0,h): 
    ### y (power+affine) ---> z
    content=""
    for i in range(block_size):
        for j in range(n):
            if j==0:
                temp=power_new[0]
                temp=temp.replace("x",power_out[i][(j-h)%n])
                temp=temp.replace("y",power_out[i][(j-k0-h)%n])
                temp=temp.replace("q",q[i][j])
                temp=temp.replace("c",g1[i][j])
                content+=temp

                temp=power_new[2]
                temp=temp.replace("c",g2[i][j])
                temp=temp.replace("g",g1[i][n-1])
                content+=temp

            
            else:
                temp=power_new[1]
                temp=temp.replace("x",power_out[i][(j-h)%n])
                temp=temp.replace("y",power_out[i][(j-k0-h)%n])
                temp=temp.replace("q",q[i][j])
                temp=temp.replace("g",g1[i][j-1])
                temp=temp.replace("c",g1[i][j])
                content+=temp
    
            temp=power_new[3]
            temp=temp.replace("c",g2[i][j+1])
            temp=temp.replace("z",power_in[i][j])
            temp=temp.replace("q",q[i][j])
            temp=temp.replace("gg",g2[i][j])
            content+=temp
    return content

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

def Three_Copy(z,z1,z2,z3,q,p,c1,c2,c3,c4):
    content=""
    for i in range(block_size):
        for j in range(n):
            if j==0:
                temp=III_copy_constraints_new[0]
                temp=temp.replace("v_0",z1[i][0])
                temp=temp.replace("v_1",z2[i][0])
                temp=temp.replace("v_2",z3[i][0])
                temp=temp.replace("q",q[i][0])
                temp=temp.replace("c_1",c1[i][0])
                content+=temp

                temp=III_copy_constraints_new[4]
                temp=temp.replace("c_2",c2[i][0])
                temp=temp.replace("c_1",c1[i][n-1])
                content+=temp

                temp=III_copy_constraints_new[5]
                temp=temp.replace("c_2_1",c2[i][1])
                temp=temp.replace("c_2_0",c2[i][0])
                temp=temp.replace("p",p[i][0])
                temp=temp.replace("q",q[i][0])
                content+=temp

                temp=III_copy_constraints_new[8]
                temp=temp.replace("c_4",c4[i][0])
                temp=temp.replace("c_2",c2[i][n-1])
                content+=temp

            elif j==1:
                temp=III_copy_constraints_new[1]
                temp=temp.replace("v_0",z1[i][1])
                temp=temp.replace("v_1",z2[i][1])
                temp=temp.replace("v_2",z3[i][1])
                temp=temp.replace("q",q[i][1])
                temp=temp.replace("c_1_1",c1[i][1])
                temp=temp.replace("c_1_0",c1[i][0])
                temp=temp.replace("c_3",c3[i][0])
                content+=temp

                temp=III_copy_constraints_new[6]
                temp=temp.replace("c_2_1",c2[i][2])
                temp=temp.replace("c_2_0",c2[i][1])
                temp=temp.replace("p",p[i][1])
                temp=temp.replace("q",q[i][1])
                temp=temp.replace("c_3",c3[i][n-2])
                content+=temp
            elif j==2:
                temp=III_copy_constraints_new[2]
                temp=temp.replace("v_0",z1[i][2])
                temp=temp.replace("v_1",z2[i][2])
                temp=temp.replace("v_2",z3[i][2])
                temp=temp.replace("q",q[i][2])
                temp=temp.replace("c_1_2",c1[i][2])
                temp=temp.replace("c_1_1",c1[i][1])
                temp=temp.replace("c_3",c3[i][1])
                content+=temp
            else:
                temp=III_copy_constraints_new[3]
                temp=temp.replace("v_0",z1[i][j])
                temp=temp.replace("v_1",z2[i][j])
                temp=temp.replace("v_2",z3[i][j])
                temp=temp.replace("q",q[i][j])
                temp=temp.replace("c_1_1",c1[i][j])
                temp=temp.replace("c_1_0",c1[i][j-1])
                temp=temp.replace("c_3_1",c3[i][j-1])
                temp=temp.replace("c_3_0",c3[i][j-3])
                content+=temp

        for j in range(2,n):
            temp=III_copy_constraints_new[7]
            temp=temp.replace("c_2_1",c2[i][j+1])
            temp=temp.replace("c_2_0",c2[i][j])
            temp=temp.replace("p",p[i][j])
            temp=temp.replace("q",q[i][j])
            content+=temp
        for j in range(n):
            temp=III_copy_constraints_new[9]
            temp=temp.replace("c_4_1",c4[i][j+1])
            temp=temp.replace("c_4_0",c4[i][j])
            temp=temp.replace("u",z[i][j])
            temp=temp.replace("p",p[i][j])
            content+=temp
    return content

def Weight_bound(x,bound,round):
    content=""
    s=generate_variables(round_nvar*round+3*n+1,round_nvar*round+3*n+1+(n-1)*bound,bound)
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
    for i in range(1,block_size):
        for j in range(n):
            content+="-{} 0\n".format(X[0][i][j])
            content+="-{} 0\n".format(X[round][i][j])

    for i in range(n):
        if i==0:
            content+="{} 0\n".format(X[round][0][i])
        else:
            content+="-{} 0\n".format(X[round][0][i])
    return content
# bound=61
X=[] #3n
K=[] #3n
Y=[] #3n
# Y copy --> Y_1,Y_2
Y_1=[] #3n
Y_2=[] #3n
Copy_Y_Q=[] #3n
Copy_Y_C1=[] #3n
Copy_Y_C2=[] #3n+3

# Y_1 power --> Power_Y1
# Y_2 power --> Power_Y2
Power_Y1=[] #3n
Power_Y1_Q=[] #3n
Power_Y1_G1=[] #3n
Power_Y1_G2=[] #3n+3

Power_Y2=[] #3n
Power_Y2_Q=[] #3n
Power_Y2_G1=[] #3n 
Power_Y2_G2=[] #3n+3

# Q=[]
# G1=[]
# G2=[]
Z=[] #3n
Copy_Q=[] #3n
Copy_C1=[] #3n
Copy_C2=[] #3n+3
Copy_C3=[] #3n-3
Copy_C4=[] #3n+3
Copy_P=[] #3n
Z1=[] #3n
Z2=[] #3n
Z3=[] #3n

def Run_sat(filename,round,test_degree,solver):
    # os.chdir("./tmp_cnf")
    # sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
    sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
    cadical_parameters="/home/minions/tools/cadical-master/build/cadical {} -n".format(filename)
    stdout=""
    if solver=="cryptominisat5":
        # print(sat_parameters)
        result_new = subprocess.run(sat_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout=result_new.stdout
        # print(stdout)
        if "UNSATISFIABLE" in stdout:
            # print("UNSATISFIABLE")
            for j in range(test_degree-1,0,-1):
                filename="./tmp_HD/Chaghri_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                sat_parameters="cryptominisat5 --verb 0 {}".format(filename)
                result_new = subprocess.run(sat_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    continue
                elif "SATISFIABLE" in result_new.stdout:
                    return j

        elif "SATISFIABLE" in stdout:
            # print("SAT")
            for j in range(test_degree+1,n+1):
                filename="./tmp_HD/Chaghri_round{}.cnf".format(round)
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
            # print("UNSATISFIABLE")
            for j in range(test_degree-1,0,-1):
                filename="./tmp_HD/Chaghri_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                cadical_parameters="/home/minions/tools/cadical-master/build/cadical {} -n".format(filename)
                result_new = subprocess.run(cadical_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    continue
                elif "SATISFIABLE" in result_new.stdout:
                    return j

        elif "SATISFIABLE" in stdout:
            # print("SAT")
            for j in range(test_degree+1,n+1):
                filename="./tmp_HD/Chaghri_round{}.cnf".format(round)
                Generate_variables(round,round_nvar)
                Generate_constraints(round,j,filename)
                cadical_parameters="/home/minions/tools/cadical-master/build/cadical {} -n".format(filename)
                result_new = subprocess.run(cadical_parameters, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if "UNSATISFIABLE" in result_new.stdout:
                    return j-1

def Generate_constraints(round,bound,filename):
    
    constraints=""
    for r in range(round):
        constraints+=Xor(X[r],K[r],Y[r]) #n*block_size*len_two_xor
        constraints+=Two_Copy(Y_1[r],Y_2[r],Copy_Y_Q[r],Copy_Y_C1[r],Copy_Y_C2[r],Y[r]) # bock
        constraints+=Power_Affine(Y_1[r],Power_Y1_Q[r],Power_Y1_G1[r],Power_Y1_G2[r],Power_Y1[r],k0,h1)
        constraints+=Power_Affine(Y_2[r],Power_Y2_Q[r],Power_Y2_G1[r],Power_Y2_G2[r],Power_Y2[r],k0,h2)
        constraints+=Xor(Power_Y1[r],Power_Y2[r],Z[r])
        constraints+=Three_Copy(Z[r],Z1[r],Z2[r],Z3[r],Copy_Q[r],Copy_P[r],Copy_C1[r],Copy_C2[r],Copy_C3[r],Copy_C4[r])
        constraints+=Three_xor(Z1[r],Z2[r],Z3[r],X[r+1])
    constraints+=Weight_bound(X[0][0],bound,round)
    constraints+=Initial_final_constrants(round)

    len_constraints=constraints.count("\n")
    constraints_start="p cnf {} {}\n".format(round*round_nvar+3*n+(n-1)*bound,len_constraints)

    # print(len_constraints)
    with open(filename,"w+") as file:
        file.write(constraints_start)
        file.write(constraints)

def Generate_variables(round,round_nvar):
    for r in range(round):
        X.append(generate_variables(1+r*round_nvar,3*n+1+r*round_nvar,n)) ## 3n
        K.append(generate_variables(3*n+1+r*round_nvar,6*n+1+r*round_nvar,n)) ## 3n
        Y.append(generate_variables(6*n+1+r*round_nvar,9*n+1+r*round_nvar,n)) ## 3n
        Y_1.append(generate_variables(9*n+1+r*round_nvar,12*n+1+r*round_nvar,n)) ## 3n
        Y_2.append(generate_variables(12*n+1+r*round_nvar,15*n+1+r*round_nvar,n)) ## 3n
        Copy_Y_Q.append(generate_variables(15*n+1+r*round_nvar,18*n+1+r*round_nvar,n)) ## 3n
        Copy_Y_C1.append(generate_variables(18*n+1+r*round_nvar,21*n+1+r*round_nvar,n)) ## 3n
        Copy_Y_C2.append(generate_variables(21*n+1+r*round_nvar,24*n+1+3+r*round_nvar,n+1)) ## 3(n+1)

        Power_Y1.append(generate_variables(24*n+1+3+r*round_nvar,27*n+1+3+r*round_nvar,n)) ## 3n
        Power_Y1_Q.append(generate_variables(27*n+1+3+r*round_nvar,30*n+1+3+r*round_nvar,n)) ## 3n
        Power_Y1_G1.append(generate_variables(30*n+1+3+r*round_nvar,33*n+1+3+r*round_nvar,n)) ## 3n
        Power_Y1_G2.append(generate_variables(33*n+1+3+r*round_nvar,36*n+1+6+r*round_nvar,n+1)) ## 3(n+1)

        Power_Y2.append(generate_variables(36*n+1+6+r*round_nvar,39*n+1+6+r*round_nvar,n)) ## 3n
        Power_Y2_Q.append(generate_variables(39*n+1+6+r*round_nvar,42*n+1+6+r*round_nvar,n)) ## 3n
        Power_Y2_G1.append(generate_variables(42*n+1+6+r*round_nvar,45*n+1+6+r*round_nvar,n)) ## 3n
        Power_Y2_G2.append(generate_variables(45*n+1+6+r*round_nvar,48*n+1+9+r*round_nvar,n+1)) ## 3(n+1)

        Z.append(generate_variables(48*n+1+9+r*round_nvar,51*n+1+9+r*round_nvar,n)) ## 3n
        Copy_Q.append(generate_variables(51*n+1+9+r*round_nvar,54*n+1+9+r*round_nvar,n)) ## 3n
        Copy_C1.append(generate_variables(54*n+1+9+r*round_nvar,57*n+1+9+r*round_nvar,n)) ## 3n
        Copy_C2.append(generate_variables(57*n+1+9+r*round_nvar,60*n+1+9+3+r*round_nvar,n+1)) ## 3(n+1)
        Copy_C3.append(generate_variables(60*n+1+9+3+r*round_nvar,63*n+1+9+r*round_nvar,n-1)) ## 3(n-1)
        Copy_C4.append(generate_variables(63*n+1+9+r*round_nvar,66*n+1+9+3+r*round_nvar,n+1)) ## 3(n+1)
        Copy_P.append(generate_variables(66*n+1+9+3+r*round_nvar,69*n+1+9+3+r*round_nvar,n)) ## 3n
        Z1.append(generate_variables(69*n+1+9+3+r*round_nvar,72*n+1+9+3+r*round_nvar,n)) ## 3n
        Z2.append(generate_variables(72*n+1+9+3+r*round_nvar,75*n+1+9+3+r*round_nvar,n)) ## 3n
        Z3.append(generate_variables(75*n+1+9+3+r*round_nvar,78*n+1+9+3+r*round_nvar,n)) ## 3n
    X.append(generate_variables(1+round*round_nvar,3*n+1+round*round_nvar,n)) ## 3n




import sys
import math
begin_round=int(sys.argv[1])
end_round=int(sys.argv[2])
# print(begin_round,end_round)
solver=sys.argv[3]
result_content=""
result_file=f"HD_{solver}_result.txt"
test_bound=[2,4,8,15,27,42,52,62,63]
d=2**k0+2**k1
for i in range(begin_round,end_round):
    # test_bound=math.floor(math.log(pow(d,i)+1)/math.log(2))
    print("test_bound",test_bound[i-1])
    filename="./tmp_HD/Chaghri_round{}.cnf".format(i)
    Generate_variables(i,round_nvar)
    Generate_constraints(i,test_bound[i-1],filename)

    start_time = time.time()
    degree=Run_sat(filename,i,test_bound[i-1],solver)
    end_time = time.time()-start_time
    result_content="Round:{}, Maxdegree:{}, Time:{}\n".format(i,degree,end_time)
    with open(result_file,"a") as file:
        file.write(result_content) 
