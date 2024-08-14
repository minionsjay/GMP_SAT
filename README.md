# GeneralMonomialPrediction by MILP and SAT

This repository contains the source code for the paper "Improved Upper Bound of Algebraic Degrees for Some Arithmetization-Oriented Ciphers".

## Requirements 

- [python3](https://www.python.org/downloads/) to run our Python codes.
- [Gurobi](https://www.gurobi.com/)
- [Cadical](https://github.com/arminbiere/cadical) or [CryptoMiniSat](https://github.com/msoos/cryptominisat)
- [STP](https://github.com/stp/stp)

## Chaghri

The Chaghri file contains three models: GMP_SAT, GMP_MILP, and GMP_SMT. You can use the run.ipynb to execute and solve for the upper bound of algebraic degrees. The GMP_SAT model can be solved using either the Cadical solver or the CryptoMiniSat solver.

## Ciminion

The Ciminion file contains the GMP_SAT model, which can be executed using the run.ipynb to solve for the upper bound of algebraic degrees.

## Test_degree_bound
The code for testing the actual algebraic degree is in Test_degree_bound.
