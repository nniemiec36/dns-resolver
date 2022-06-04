# mydig using dnspython

## This implementing a DNS resolver. 
The resolver takes as input a domain name.
The resolver resolves this query by first contacting the root server, the top-level domain, all the way until the authoritative name server. 

## How to Use

In order to use, open the terminal and run "python3 mydig.py" on the command line. You will be prompted for a website's url. Please hit enter. 

## The following response will be displayed on the terminal:

```
QUESTION SECTION:
(your url).    IN A

ANSWER SECTION:
(your url). 30 IN A (ip address)

QUERY TIME: (ms)
WHEN:  yyyy-mm-dd hh:mm:ss.ms
```

## License

[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
