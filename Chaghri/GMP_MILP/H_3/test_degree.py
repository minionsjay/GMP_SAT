# from email.policy import default
from gurobipy import *
import os
import time
from argparse import ArgumentParser, RawTextHelpFormatter
# from matplotlib.cbook import flatten

# from plumbum import local


class Chaghri:
    count = 0

    def __init__(self, nrounds=10):
        Chaghri.count += 1
        self.nrounds = nrounds
        self.k0 = 32
        self.k1 = 0
        self.k2 = 3
        self.milp_variables = []
        self.n_block = 63
        self.lp_file_name = f"chaghri_nr_{nrounds}.lp"
        self.result_file_name = f"result.txt"

    
    def generate_vars(self, n):
        
        nr = self.nrounds
        command = "Binary\n"
        for r in range(nr+1):
            for i in range(3):
                for j in range(n):
                    command += f"x_{r}_{i}_{j}\n"
        for r in range(nr):
            for i in range(3):
                for j in range(n):
                    command += f"k_{r}_{i}_{j}\n"
        for r in range(nr):
            for i in range(3):
                for j in range(n):
                    command += f"y_{r}_{i}_{j}\n"
        for r in range(nr):
            for i in range(3):
                for j in range(n):
                    command += f"z_{r}_{i}_{j}\n"
        
        
        for r in range(nr):
            for i in range(3):
                for k in range(3):
                    for j in range(n):
                        
                        command += f"z_{r}_{i}_{k}_{j}\n"
        
        for r in range(nr):
            for i in range(3):
                for j in range(n):
                    
                    command += f"qq_{r}_{i}_{j}\n"
                    
        for r in range(nr):
            for i in range(3):
                for j in range(n+1):
                    command += f"g_{r}_{i}_{j}\n"
                    command += f"gg_{r}_{i}_{j}\n"
                    
        for r in range(nr):
            for i in range(3):
                for j in range(n+2):
                    command += f"ggg_{r}_{i}_{j}\n"
        
        for r in range(nr):
            for i in range(3):
                for j in range(n):
                    command += f"p_qq_{r}_{i}_{j}\n"
        for r in range(nr):
            for i in range(3):
                for j in range(n+1):
                    command += f"p_g_{r}_{i}_{j}\n"
                    command += f"p_gg_{r}_{i}_{j}\n"
        return command

    def xor2_constraint(self, xor_in, xor_out, command):

        for i in range(self.n_block):
            command += "{}_{} + {}_{} - {}_{} = 0\n".format(
                xor_in[0], i, xor_in[1], i, xor_out, i)
        
        return command

    def xor3_constraint(self, xor_in, xor_out, command):

        for i in range(self.n_block):
            command += "{}_{} + {}_{} + {}_{} - {}_{} = 0\n".format(
                xor_in[0], i, xor_in[1], i, xor_in[2], i, xor_out, i)
        
        return command

    def copy3_constraint(self, copy_in, copy_out, r, s, command):
        command += "g_{}_{}_{} = 0\n".format(r, s, 0)
        for i in range(3):
            command += "ggg_{}_{}_{} = 0\n".format(r, s, i)
        for i in range(self.n_block):
            command += f"4 ggg_{r}_{s}_{i+2} + 2 g_{r}_{s}_{i+1} + qq_{r}_{s}_{i} - {copy_out[0]}_{i} - {copy_out[1]}_{i} - {copy_out[2]}_{i} - g_{r}_{s}_{i} - ggg_{r}_{s}_{i} = 0\n"
            
        command += f"gg_{r}_{s}_0 - g_{r}_{s}_63 = 0\n"

        for i in range(63):
            if i == 1:
                command += f"2 gg_{r}_{s}_{i+1} + {copy_in}_{i} - qq_{r}_{s}_{i} - gg_{r}_{s}_{i} - ggg_{r}_{s}_{64} = 0\n"
                
            else:
                command += f"2 gg_{r}_{s}_{i+1} + {copy_in}_{i} - qq_{r}_{s}_{i} - gg_{r}_{s}_{i} = 0\n"
               
        return command

    def power_constraint(self, power_in, power_out, r, s, k0, command):
        k2 = self.k2
        command += f"p_g_{r}_{s}_0 = 0\n"
        
        for i in range(self.n_block):
            command += f"2 p_g_{r}_{s}_{i+1} + p_qq_{r}_{s}_{i} - {power_out}_{(i-k2)%self.n_block} - {power_out}_{(i-k0-k2)%self.n_block} - p_g_{r}_{s}_{i} = 0\n"
            
        command += f"p_gg_{r}_{s}_0 - p_g_{r}_{s}_63 = 0\n"
        
        for i in range(self.n_block):
            command += f"2 p_gg_{r}_{s}_{i+1} + {power_in}_{i} - p_qq_{r}_{s}_{i} - p_gg_{r}_{s}_{i} = 0\n"
            
        return command

    def object_function(self, command):
        tmp = []
        for i in range(1):
            for j in range(self.n_block):
                tmp.append(f"x_0_{i}_{j}")
        command += " + ".join(tmp)
        command += "\n"
        return command

    def initate_constraint(self, command):
        for i in range(1, 3):
            for j in range(self.n_block):
                command += f"x_0_{i}_{j} = 0\n"
        return command

    def final_constraint(self, r, command):
        for i in range(1, 3):
            for j in range(self.n_block):
                command += f"x_{r}_{i}_{j} = 0\n"
        command += f"x_{r}_0_0 = 1\n"
        for j in range(1, self.n_block):
            command += f"x_{r}_0_{j} =  0\n"
        return command

    def weight_constraint(self, testweight, command):
        tmp = []
        for i in range(self.n_block):
            tmp.append(f"x_0_0_{i}")
        command += " + ".join(tmp)
        command += f" >= {testweight}\n"
        return command

    def make_milp_model(self, testweight):
        """
        Generate the MILP model describing the propagation monomial prediction vectors
        """
        lp_content = "\\ Algrabic degree evalution on {} round of chaghri_63\n".format(
            self.nrounds)

        lp_content += "Maximum\n"

        lp_content = self.object_function(lp_content)

        lp_content += "subject to\n"
        # =======xor==========
        for r in range(self.nrounds):
            for i in range(3):
                xor_in = [f"x_{r}_{i}", f"k_{r}_{i}"]
                xor_out = f"y_{r}_{i}"
                lp_content = self.xor2_constraint(xor_in, xor_out, lp_content)
        # =======power+affine=======
                power_in = f"y_{r}_{i}"
                power_out = f"z_{r}_{i}"
                lp_content = self.power_constraint(
                    power_in, power_out, r, i, self.k0, lp_content)
        # ========copy===============
                copy_in = f"z_{r}_{i}"
                copy_out = [f"z_{r}_{i}_{j}" for j in range(3)]
                lp_content = self.copy3_constraint(
                    copy_in, copy_out, r, i, lp_content)

        # =========matrix===========
                m_xor_in = [f"z_{r}_{j}_{i}" for j in range(3)]
                m_xor_out = f"x_{r+1}_{i}"
                lp_content = self.xor3_constraint(
                    m_xor_in, m_xor_out, lp_content)

        lp_content = self.initate_constraint(lp_content)
        lp_content = self.final_constraint(self.nrounds, lp_content)

        

        lp_content += self.generate_vars(self.n_block)
        lp_content += "End"
        with open(self.lp_file_name, "w+") as lp_file:
            lp_file.write(lp_content)

    def solve(self, testweight):
        self.make_milp_model(testweight)
        milp_model = read(self.lp_file_name)
        milp_model.setParam(GRB.Param.OutputFlag, False)
        
        milp_model.optimize()

        result_f = open(self.result_file_name, "a")
        
        number_sol = milp_model.getAttr('SolCount')
        objval = round(milp_model.objVal)
        print("sol_number:{}".format(number_sol))

        print("Round:{}".format(self.nrounds))
        print("Maximum degree:", objval)
        result = "*"*50
        result += "\n"
        result += "Round:{}\n".format(self.nrounds)
        result += "Maximum degree:{}\n".format(objval)
        
        result_f.write(result)
        result_f.close()
        


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

    
    return N[r-1]


def CoeGroup(k0, k1, k2, n, r):
    Nr = Calculate_Ni(k0, k1, k2, r+1, n)
    # print("N{}:{}".format(r,Nr))
    d = Alg1(Nr, n)
    # print("degree:",d)
    return d


print(os.getcwd())
os.chdir("./tmp2_lp")
for i in range(2, 29):

    maxdegree = CoeGroup(32, 0, 3, 63, i)
    start_time = time.time()
    chaghri = Chaghri(i)
    result_f = open(chaghri.result_file_name, "a")
    
    chaghri.solve(3)
    end_time = time.time()-start_time
    print("Time used {} s\n".format(end_time))
    result_f.write("Time used {} s\n".format(end_time))
    result_f.close()
