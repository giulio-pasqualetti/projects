# Big data analytics – Twitter social graph

## Problem description:

Download a representation of Twitter social graph from https://github.com/ANLAB-KAIST/traces/releases/tag/twitter_rv.net (files from twitter_rv.net.00 to twitter_rv.net.03)and present answers to the following questions:
1. Which 3 user IDs have most followers?
2. Identify the user following the highest number of accounts (user f). 
   Calculate:
   - The shortest path between f and any other user u in the graph (i.e. the lowest number
   of edges between f and u, where edge u1­>u2 represents u1 following u2). Report the
   length of 3 longest paths and the ending nodes.
   - Optional: The longest cycle, e.g. path starting and ending at f but visiting other users
               at most once (report the length, or if the length is less or equal than 20 edges, report
               the nod IDs).
3. Use the graph data to answer the following questions:
   - Is the graph sparse or dense? Does the answer somehow determine how the solution
     to questions 1 and 2 should be found?
   - If the graph is dense, provide an example of a sparse graph (and vice versa).
4. Suppose that instead of Twitter following, the data represents money transfers. What
patterns would you look for to flag a high risk of money laundering? What other additional
information should be added to the graph to simplify money­laundering identification?

## Additional instructions:
The full dataset is big. You can use only top 10 million lines of the source data instead, but
please describe the options to handle the full dataset.

# Presentation
The file "Big_Data_Analytics_Presentation.pdf" contains a presentation of the project.