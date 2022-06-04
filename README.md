# dns-resolver
## Part A (70 points) 
You will be implementing a DNS resolver. The resolver takes as input a domain name. Your resolver resolves this query by first contacting the root server, the top-level domain, all the way until the authoritative name server. 
You can assume that you have access to a library that can resolve a single iterative DNS query. The set of libraries that you may use are given in the Appendix. The libraries also perform complete DNS resolution, but you are *not allowed* to use that. 

1. You can access the IP address of the root servers from https://www.iana.org/domains/root/servers. 
2. Build a “dig”-like tool called “mydig”. The mydig tool takes as input the name of the domain you want to resolve. You should resolve the “A” record for the query. When run your program and enter the input “www.cnn.com”, your tool must display the output as shown below:  
```QUESTION SECTION:  
www.cnn.com. IN A   
ANSWER SECTION:  
www.cnn.com. 262 IN A 151.101.209.67   
Query time: How much time it took to resolve the query  
WHEN: Date and time of request 
```
You can either provide the input at command line or you can ask the user to enter an input. 
3. Make sure you handle errors: for example, in case you cannot connect to any of the DNS Name Server, or you are not able to parse the DNS Response, etc, you will have to return an error.  Along with the code, you need to submit an output file called “mydig_output”, that contains the expected output for running your mydig program. Please specify the input to your program before the output in the same file. In some cases, you will not be able to resolve the query to the complete IP address, but only get a “CNAME”. In this case, you will have to resolve the query completely. An example of such a query is google.co.jp. You will use two APIs to create a DNS request to each individual server. The first is to create a DNS query and the second is to send this query to the destination. Figuring out the right APIs is up to you, but both can be found in the library. However,as mentioned earlier you are not allowed to use the resolve function in the library. 

## PART B (30 points) 
Your next task is to measure the performance of your DNS resolver from Part A. Pick 10 out of the top 25 Websites from alexa.com (http://www.alexa.com/topsites.) 
Experiment 1: Run your DNS resolver on each website 10 times and find the average time, 25th percentile, and 75th percentile to resolve the DNS for each of the 10 websites. 
Experiment 2: Now use your local DNS resolver and repeat the experiment (call this Local DNS). Find the average time to resolve the address for the 10 websites. 
Experiment 3: Change the DNS resolver to Google’s public DNS (The IP address of this public DNS is often 8.8.8.8, or 8.8.4.4, but you need to verify). 
Repeat the experiment one more time and call this result “Google DNS” You can use the dig command for experiments 2 and 3. For each of the 10 Website, plot the median, 25th percentile and 75th percentile values over the 10 runs and draw a graph. The x axis is the website, named 1 to 10. The y axis is the time taken to resolve the query. Each point will have three bars corresponding to the three experiments. The 25th and 75th percentile should be shown as a box plot.
