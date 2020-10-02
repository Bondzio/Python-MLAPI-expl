#!/usr/bin/env python
# coding: utf-8

# # N-Queens - 92 Solutions In Prolog
# 
# This code solves the N-Queens problem in Prolog using the CLP(FD): Constraint Logic Programming over Finite Domain Library
# 
# - `nqueens()` creates a 2D array datastructure, representing the board coordinates of each queen
# - `applyConstraints()` recursively iterates through each queen on the board
# - `checkConstraints()` applies the constraints: no two queens on same row/column/diagonal; and recurses through the list of remaining queens
# - `optimizeQueens()` hardcodes each queen to live in a named row, this greatly reduces the computational complixity of the problem
#   - Note: it is not possible to pass `Index + 1` into a prolog function, instead it must be declared and solved first as its own varaiable: `NextIndex is Index + 1`
# - `print_board()` + print_line() render the ASCII graphics in a functional manner
# - `all_nqueens()` uses `findall()` to solve `nqueens()` whilst repeatedly adding previous solutions as future constraints
# - `print_nqueens_all(N)` is the main display/execution function

# In[ ]:


# ! add-apt-repository ppa:swi-prolog/stable
get_ipython().system(' apt install -y -qq swi-prolog time gawk 2>&1 > /dev/null')


# In[ ]:


get_ipython().run_cell_magic('writefile', 'nqueens.prolog', "\n:- use_module(library(clpfd)).\n\n% DOC: http://www.pathwayslms.com/swipltuts/clpfd/clpfd.html\nlength_(Length, List) :- length(List, Length).\n\napplyConstraints([]).\napplyConstraints([ Q | Queens ]) :-\n    checkConstraints(Q, Queens),\n    applyConstraints(Queens).\n\ncheckConstraints(_, []).\ncheckConstraints([Row0, Col0], [ [Row1, Col1] | Queens]) :-\n    Row0 #\\= Row1,                 % No two queens on same row\n    Col0 #\\= Col1,                 % No two queens on same columns\n    Row0 + Col0 #\\= Row1 + Col1,   % Down diagonals: [8,1], [7,2], [6,3]\n    Row0 - Col0 #\\= Row1 - Col1,   % Up   diagonals: [1,1], [2,2], [3,3]\n    checkConstraints([Row0,Col0], Queens).\n\n\n% Optimization: pre-assign each queen to a named row\noptimizeQueens(Queens) :- optimizeQueens(Queens, 1).\noptimizeQueens([],_).\noptimizeQueens([[Row,_] | Queens], Index) :-\n    Row #= Index,\n    NextIndex is Index + 1,\n    optimizeQueens(Queens, NextIndex).\n\n\nnqueens(N, Queens) :-\n    % Function Preconditions\n    N > 0,\n\n    % Create 2D Datastructure for Queens\n    length(Queens, N), maplist(length_(2), Queens),\n    flatten(Queens, QueenArray),\n\n    % Queens coords must be in range\n    QueenArray ins 1..N,\n\n    % Apply Constraints\n    optimizeQueens(Queens),\n    applyConstraints(Queens),\n\n    % Solve\n    label(QueenArray),\n    true.\n\n\nall_nqueens(N) :- all_nqueens(N, _).\nall_nqueens(N, Solutions) :-\n    findall(Queens, (nqueens(N,Queens), write(Queens), nl), Solutions),\n    length(Solutions,Count),\n    write(Count), write(' solutions'), nl,\n    Count #>= 1.\n\n\nprint_nqueens_all(N)                 :- all_nqueens(N, Solutions), print_nqueens(N, Solutions).\nprint_nqueens(N)                     :- nqueens(N, Queens),        print_board(N, Queens).\nprint_nqueens(N, [Queens|Remaining]) :- print_count(Remaining),    print_board(N, Queens),    print_nqueens(N, Remaining).\nprint_nqueens(_, []).\n\nprint_count(Remaining) :- length(Remaining, Count), Count1 is Count + 1, nl, write('# '), write(Count1), nl.\nprint_board(N, [[_,Q] | Queens]) :- print_line(N, '-'), print_line(N, '|', Q), print_board(N, Queens).\nprint_board(N, [])  :- print_line(N, '-').\nprint_line(0,'-')   :- write('-'), nl.\nprint_line(N,'-')   :- write('----'), N1 is N-1, print_line(N1,'-').\nprint_line(0,'|',_) :- write('|'), nl.\nprint_line(N,'|',Q) :- write('|'), (( Q == N ) -> write(' Q ') ; write('   ')), N1 is N-1, print_line(N1,'|',Q).\n\n%:- initialization main.\n%main :-\n%    print_nqueens_all(8)")


# # Performance

# In[ ]:


get_ipython().system(' for n in `seq 1 13`; do     (echo $n queens; time -p swipl -q -f nqueens.prolog -t "all_nqueens($n)" | grep \'solutions\' | head -n 1) 2>&1     | grep \'queens\\|solutions\\|real\' | uniq | tr \'\\n\' \' \' | gawk \'{ printf("%3d queens = %8d solutions in %8.2fs\\n", $1, $5, $4)  }\'; done;')


# # Output

# In[ ]:


get_ipython().system(" swipl -f nqueens.prolog -t 'print_nqueens_all(8)'")

