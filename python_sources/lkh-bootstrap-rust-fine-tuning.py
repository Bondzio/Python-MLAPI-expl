#!/usr/bin/env python
# coding: utf-8

# # Kaggle 2018 Santa competition
# 
# This kernel tries to solve a variant of TSP from [Travelling Santa 2018](https://kaggle.com/c/traveling-santa-2018-prime-paths)
# It does so in several steps. The version which scores 1514637.06 is [#36](https://www.kaggle.com/ppershing/lkh-bootstrap-rust-fine-tuning?scriptVersionId=9206685). As you can see, we run a lots of different configurations in order to get to this result. In general, we have a problem with high variance when re-running the same configuration can yiled scores different up to 100 just depending on the random chance (I guess we end up falling into steep local minimum)
# 
# 1) Initial tour finding. We use [LKH 3](http://akira.ruc.dk/~keld/research/LKH-3/) to find an initial path. We use custom config which was fine-tuned to produce a raw solution (without problem specific penalty) worth of 15002800 in about one hour. We run 4 parallel instances of LKH with different seeds to have different paths
# 
# 2) Push tour even further. We use second round of 4 LKHs, this time fine-tuned to quickly take previous solutions and improve them a bit. We run this for another almost full hour to gain raw solutions worth of about 15002740. This gives a penalty scores of about 1516400.
# 
# 3) Recombine solulutions. We use custom C++ implementation of LKH's IPT crossover operator. Note that this implementation is customized to account for penalty but we ignore penalty in this stage.
# 
# 4) Run main optimalization technique. This is written in Rust  (not included in the Kernel file, downloaded externally as we were chaining it a lot). We run the main technique in several steps, slowly increasing penalty from 0.0 to 0.1 during the course of 4 kernel hours (Note: We first thought that the kernel runtime is 6 hours. In reality it is 9 but it probably would not help much).
# 
# A bit more details about Rust code can be found here [Our solution for 2nd place](https://www.kaggle.com/c/traveling-santa-2018-prime-paths/discussion/77250). In general, we do ~15 minute steps with 2 optimization threads + 2 kick threads, then ~15 minutes of 1 opt + 3 kick and then we increase penalty (schedule is in the last cell)
