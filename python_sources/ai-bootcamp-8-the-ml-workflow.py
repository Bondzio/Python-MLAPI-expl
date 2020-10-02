#!/usr/bin/env python
# coding: utf-8

# # Ch. 8 - The machine learning workflow
# This week, we will work through a real life problem from start to finish. A large Portuguese retail bank has conducted a telemarketing campaign from May 2008 to June 2013, selling long term deposits. Throughout the campaign they had 52,944 phone contacts over which they kept records. Now they are looking to create a system that can predict whether a customer will subscribe to a deposit if called, to increase returns on the next telemarketing campaign. You will learn all the steps of a machine learning workflow, from initial contact with the client to a deployed model. In this chapter, we will walk through the workflow on a higher level. In the next chapters, we will look at each step in depth.
# 
# The data for this chapter was sourced from Moro et al., 2014, via the [UCI machine learning repository](http://archive.ics.uci.edu/ml/datasets/Bank+Marketing). However, to make this introductionary task easier the dataset was balanced. The full paper describing the original dataset and research can be found online, see: 
# 
# [S. Moro, P. Cortez and P. Rita. A Data-Driven Approach to Predict the Success of Bank Telemarketing. Decision Support Systems, Elsevier, 62:22-31, June 2014](http://dx.doi.org/10.1016/j.dss.2014.03.001)
# 
# ## Step 1: Understand the business problem
# One Wednesday afternoon you get a call from Portugal. Its the head of the marketing department of a large retail bank, who heard that you are an experienced machine learning practitioner that had helped multiple financial institutions to greater profitability. They would like to improve the returns on their telemarketing campaign he says, and was wondering whether you could help. Always looking for an opportunity to work in a sunny part of europe with pretty inner cities, you head to Lisbon.
# 
# When you start working on a new project, especially for a new client, it is important that you understand their actual business and the problem they are trying to solve. In the case of the retail bank, it would be interesting to learn a few things about the bank first. Here are some questions you might ask:
# - Why does the bank run a telemarketing campaign?
# - How does the relationship of the bank with its customers look like? Which communication channels are usually used?
# - How does the telemarketing campaign relate to other marketing campaigns?
# - What is the brand of the bank? How do customers perceive it? How should they perceive it?
# - How does the bank measure the merits of the campaign?
# - How much does the campaign cost? How much revenue does it bring in?
# - What kind of improvement would the bank consider a success?
# - What attempts to improve the campaign have been made before? Why did they (not) work?
# - Which other stakeholders does the campaign have?
# 
# Asking a lot of questions about the business will help you understand what you can and can not do for your client. Frequently, the stated business problem is not the actual business problem. For example, a telemarketing campaign might come with the stated goal to maximize profits. However, many marketing campaigns also have the more implicit goal to strengthen the brand of the client or to aid other sales campaigns. A customer that did not subscribe to a deposit but gets reminded to visit one of the banks offices where she subscribes to the deposit or some other product might still be considered a success. On the other hand, a campaign that delivers very high profits through subscriptions but damages the brand through aggressive and repeated calls might still be considered a failure. 
# 
# Understanding the business problem is often not even mentioned in machine learning workflows elsewhere. Most assume the business problem as a given or advice to inquire on it. But having a half page text that describes the business problem is not necessarily the same as _understanding_ the business problem which often includes understanding the business. There is a pretty good chance that not even your client really understands what he wants you to do. Investing time in understanding what is actually asked of you can save you a lot of frustration down the line, and greatly improves the success of your work.
# 
# You have spent some time in Lisbon now, talked to many people at the bank and even some of their customers and you are quite confident that you have a good understand what their actual business problem is. As it turns out, they trained their salesforce to be sensitive to when a customer does not wish to interact and stop the call to avoid brand damage. However, there is a small chance that the customer will do less business with the bank as a result of the call. It is estimated that the expected revenue loss per call is about 10\$. This cost got factored into the profit calculation of the campaign. There are no other campaigns running that are influenced by this telemarketing campaign. The bank decided that if a customer opens a subscription later at an office, they would attribute it as a success of the offices marketing, not of the telemarketing campaign. With this information, it is time to define the success metric.
# 
# ## Step 2: Define the success metric
# A good success metric is a single number that describes how well the business problem was solved. The goal of a success metric is to guide the choice between two models or systems. If, say, you have two proposals A and B that could guide your telemarketing campaign, the success metric should immediately tell you which one you should choose. This only works if your metric is a single number, because otherwise it might not be clear which number to care more about. One way to combine multiple success indicators into one single metric could be a weighted average or a sum. Having a single metric has a second benefit. It is easier to motivate a team around optimizing for one clear metric and it is a good way to track progress. Your success metric is also important for your relationship with your client or your boss. Often, your compensation is tied to your performance. Having a clear metric of performance written out and agreed on can be crucial.
# 
# In case of the bank the metric of success is the profit of the campaign. 
# - The profit of a customer that was called and subscribed to a deposit (true positive, TP) is 100 \$
# - Customers that where called but did not subscribe (false positives, FP) cause a cost of 40 \$
# The profit gets computed per 1,000 calls made, that is, only positives of the system are considered. Positives can be either true positives $TP$ meaning that the system predicted a buy and the customer actually bought or false positives $FP$ meaning the system predicted a buy but the customer did not buy.
# 
# The success metric of the campaign can be quantified as:
# $$ profit = \frac{100 * TP - 40 * FP}{TP + FP} * 1000 $$
# 
# 
# ## Step 3: Define the base case and optimum case
# The base case is what your system will be compared against. After-all, your goal is to _improve_ the campaign. The base case is usually the status quo, whatever system the client currently uses. Sometimes, the base case can also be an industry wide standard practice or the success of a very simple technical process such as a linear regression.
# 
# In the banks case the base case is the success of their current system, which calls every customer with a success rate of 50% as evident from the data provided (this calculation will be done in the next chapter). Therefore the profit of the current system is:
# 
# $$profit_{base} = 100 * 500 - 40 * 500 = 30,000\$ $$
# 
# This profit per 1,000 customers is the mark to beat. Any increase increase in profit can be attributed to your system. It is important to lay out the base case in advance and write it down. When it comes to evaluating the performance of your system, it helps to have agreed on what it will be evaluated against.
# 
# At the same time, it makes sense to think about what the best possible outcome could be. There is only so many customers that will ever subscribe to a deposit. Given that the old system has called every customer, it is reasonable to assume that only 50% of customers are interested in a deposit at all. This means, a system that would only call those 50% and no one else would achieve a profit of:
# 
# $$profit_{optimum} = 100 * 1000 - 40 * 0 = 100,000\$ $$
# 
# It is valuable to keep in mind what we can hope for if we achieve an optimal outcome, since it will serve as a yard stick for how much better you can do or how much more you should invest to find a better solution.
# 
# ## Step 4: Gain access to the data 
# Machine learning does not work without data and gaining access to it is a crucial step. Data might be scattered around different departments, not be in the right format to be fed into the system, come with legal issues or privacy concerns and so on. Gaining access can be a major undertaking if the firm lacks fundamental data infrastructure. In this case, you should take a step back and build the infrastructure that any data driven enterprise needs before you continue with building a machine learning model on top of it. Data should be stored in secure but accessible databases or file storages. It should be possible to query it and perform basic statistics easily. All legal and ethical issues should be handled with great care and have been solved with all stakeholders involved. There has been a lot of uproar about machine learning projects which sourced their data without considering privacy implications recently. Especially if you are working with sensitive data, such as peoples banking information, it is worth asking twice where the data you work with came from. Gaining access to data can be a bit of a scavenger hunt. Therefore it is important that you have backing from all stakeholders so they will help you gaining access. When looking for data to train your models on it also makes sense to look outside the firm for external data sources. Publicly available data such as market or weather information can greatly enhance your models, and is often free and easy to use. 
# 
# Luckily for you, the Portuguese bank is on top of the digital infrastructure game and has provided you with a [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file containing all the relevant information.
# 
# ## Step 5: Scrub the data and engineer features
# Even when we have all the data it might not be ready to train our ML algorithm just yet. Often, it is messy and needs some sorting and 'cleaning': Filling blanks, converting categorical data to dummy variables and so on. In addition, we can often enhance the performance of our model by cleverly engineering new features or selecting features. For example in the banks database, customers that have not been contacted before have the days since previous contact noted as 999. Since we know this, we can add a new feature 'not contacted before' quite easily while it would be hard for our learning algorithm to figure out. The entire next chapter will be devoted to preparing the data four our model.
# 
# ## Step 6: Build the model
# Building a model is an iterative process in which you try out different approaches and hyper parameters. Depending on the computing resources you have available parts of this search might be automated. Chapter 10 will be about searching for and tuning your model.
# 
# ## Step 7: Evaluate and test the model on new data
# Before we ship out the model we need to make sure that it actually works as we hope it does. This is usually done one new data in either a test or development dataset. You should check for systematic errors and systematic biases of your model. The best way to test a model is to let it run silently next to the old system and evaluate how well it is doing in the real world without incurring much risk. Testing on real world data can often be eye opening and you might have to go back to any of the previous steps because you discovered a flaw in which data you use or even how you evaluate your models.
# 
# ## Step 8: Deploy the model
# Once it has been tested rigorously it is time to let your model out into the wild. Deploying your model often means you have to interact with a new group of stakeholders, the people that manage the live software, the update mechanism and so on. Ideally, you had them involved early so they know what to expect and you know what their requirements are. The model you are developing for the bank will be integrated into the call center software that assigns contacts to call center agents. Careful coordination with the call center software vendor is required to avoid hick-ups.
# 
# ## Step 9: Monitor the deployed model
# Once your model ins deployed it will be exposed to a lot of unexpected cases, outliers and real world messiness. Keeping close taps on your model is essential to keep it from going off the rails. To effectively monitor your model, do not only track error rates and performance along the success metric, but also give people an easy way to notify you of problematic single instance behavior or hidden biases. For example a call center agent who makes calls following the advice of your model all day long might notice earlier that he is no longer calling a certain minority and hint to a hidden bias. From the birds eye of a statistical monitoring tool these unexpected errors can be hard to see. 
# 
# ## Summary
# In this chapter you have seen the machine learning workflow. The steps are:
# 1. Understand the business problem
# 2. Define the success metric
# 3. Define the base case and optimum case
# 4. Gain access to the data
# 5. Scrub the data and engineer features
# 6. Build the model
# 7. Test the model on new data
# 8. Deploy the model
# 9. Monitor the deployed model
# 
# Creating machine learning applications is a highly iterative process in which you might have to go back one or more steps multiple times before you arrive at a finished model. For example you might find out that you need more data while you are building the model or that your success metric was ill defined when you deploy the model. Building the model itself is highly iterative and most models have gone through hundreds or even thousands of iterations before they achieved their optimum performance. But do not worry. Modern tools have made it quite easy to iterate quickly so it will feel quite satisfying when you discovered that you can do much better if you go back a few steps and run through the process again. Also there are now many ways to automate repetitive processes in model building. 
# 
# In the next chapter we will get into the technical details. Since success metric and base case are already defined here we will start scrubbing and preparing our data before building an actual model that helps improve the Portuguese banks marketing.
