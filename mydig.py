from audioop import add
from http import server
from ipaddress import ip_address
import dns.message
import dns.query
import sys 
import datetime as time

from sqlalchemy import except_all

# can i make an array of all the root IP addresses?
root_list = []
root_list.append('198.41.0.4') # a.root
root_list.append('199.9.14.201') # b.root
root_list.append('192.33.4.12') # c.root
root_list.append('199.7.91.13') # d.root
root_list.append('192.203.230.10') # e.root
root_list.append('192.5.5.241') # f.root
root_list.append('192.112.36.4') # g.root
root_list.append('198.97.190.53') # h.root
root_list.append('192.36.148.17') # i.root
root_list.append('192.58.128.30') # j.root
root_list.append('193.0.14.129') # k.root
root_list.append('199.7.83.42') # l.root
root_list.append('202.12.27.33') # m.root


# function to resolve the root server request
def resolve_root(url_address, rdtype, server_list, x):
    try:
        current_server = server_list[x]
        server_request = dns.message.make_query(url_address, rdtype, rdclass=1)
        server_response = dns.query.udp(server_request, current_server, 1)
        return server_response
    except:
        print("Could not connect ... trying next server.")
        resolve_root(url_address, rdtype, server_list, x+1)

# function to get all of the possible ip addresses in a list format
def get_list_from_text(text_list):
    # print(text_list)
    list = []
    for text in text_list:
        new_list = text.to_text().split(" ")
        if new_list[-2] != 'AAAA':
            list.append(new_list[-1])
    return list

# function to get all of the possible rdtypes in a list format
def get_rdlist_from_text(text_list):
    list = []
    for text in text_list:
        new_list = text.to_text().split(" ")
        if new_list[-2] != 'AAAA':
            list.append(new_list[-2])
    return list

# function to make a dns request
def request(url_address, rdtype, server_list, x):
    current_server = server_list[x]
    current_rdtype = rdtype[x]
    try:
        server_request = dns.message.make_query(url_address, rdtype=current_rdtype, rdclass=1)
        server_response = dns.query.udp(server_request, current_server, 1)
        return server_response
    except:
        print("Could not connect ... trying next server.")
        request(url_address=url_address, rdtype=rdtype, server_list=server_list, x=x+1)

# function to resolve intermediate requests
def resolve(server_response, current_address):
    while server_response.answer == []:
        if server_response.additional != []:
            server_list = get_list_from_text(server_response.additional)
            rd_list = get_rdlist_from_text(server_response.additional)
            try:
                server_response = request(url_address=current_address, rdtype=rd_list, server_list=server_list, x=0)
            except:
                print("Could not resolve additional data requests.")
                exit(0)
        elif server_response.authority != []:
            name_list = get_list_from_text(server_response.authority)
            rd_list = get_rdlist_from_text(server_response.authority)
            current_address = name_list[0]
            try:
                server_response = request(url_address=current_address, rdtype=rd_list, server_list=root_list, x=0)
            except:
                print("Could not resolve authority data requests.")
                exit(0)
        else:
            print("Could not resolve authority intermediate requests.")
    return server_response

# take input from the user at runttime
url = input('Enter the website\'s url, please: ')
url = url + "."

print('\nQUESTION SECTION:')
print(url,'\tIN A\n')

start_time = time.datetime.now()
final_answer = ''

good_request = True
x = 0
current_server = root_list[x]

# first we contact the root
try:
    server_response = resolve_root(url_address=url, rdtype=1, server_list=root_list, x=x)
except:
    print("Could not connect to root server.\n")
    exit(0)

# let's set the current address as the user's url
current_address = url

# now we resolve the response from root until we get an "A" record and correct ip
try:
    server_response = resolve(server_response, current_address)
    current_name = server_response.answer[0].name.to_text()
    if current_name != url:
        ip_address = server_response.answer[0].to_text().split(" ")[-1]
        server_request = dns.message.make_query(url, rdtype=1, rdclass=1)
        server_response = dns.query.udp(server_request, ip_address, 1)
except:
    print("Could not be resolved.")
    exit(0)

# if the rdtype is a CNAME:
if server_response.answer[0].rdtype == 5:
    current_address = server_response.answer[0].to_text().split(" ")[-1]
    rd_list = [5]
    try:
        server_response = request(url_address=current_address, rdtype=rd_list, server_list=root_list, x=0)
        while server_response.answer == []:
            if server_response.additional != []:
                server_list = get_list_from_text(server_response.additional)
                rd_list = get_rdlist_from_text(server_response.additional)
                try:
                    new_server_response = request(url_address=current_address, rdtype=rd_list, server_list=server_list, x=0)
                    server_response = new_server_response
                except:
                    print("Could not resolve additional data requests.")
                    exit(0)
            elif server_response.authority != []:
                name_list = get_list_from_text(server_response.authority)
                rd_list = get_rdlist_from_text(server_response.authority)
                current_address = name_list[0]
                try:
                    server_response = request(url_address=current_address, rdtype=rd_list, server_list=root_list, x=0)
                except:
                    print("Could not resolve authority data requests")
                    exit(0)
            else:
                print("Could not resolve the CNAME.")
    except:
        print("Could not resolve CNAME requests.")
        exit(0)


ip_address = server_response.answer[0].to_text().split(" ")[-1]
rd_type = 'A'
if server_response.answer[0].rdtype == 1:
    rd_type = 'A'
elif server_response.answer[0].rdtype == 2:
    rd_type = 'NS'
elif server_response.answer[0].rdtype == 5:
    rd_type = 'CNAME'
elif server_response.answer[0].rdtype == 15:
    rd_type = 'MX'
else:
    rd_type = 'A'
final_answer = url + " " + str(server_response.answer[0].ttl) + " IN " + rd_type + ' ' +  ip_address




# # if cname, then rdtype = 5, rdclass=1 (for IN)
# # if a, then rdtype = 1
# # if ns, then rdtype = 2

# # the resolver takes the "domain name" which is the "url_address" from above. first, the resolver will try and resolve the query by contacting the root server all the way until the authoritative name server

# # for "mydig" we want to resolve the "A" record for the query of the domain we want to resolve (url_address)
# # send a request msg to every server


# # bad request or time out
# # extreme case if all server list fails, then say there's no server available and 
# # try and expect

# # additional corresponds to authority ip, pick one, ask again, then again and again
# # when we get a cname, ask the root, and then until you get an answer
# # have a fall back if the first doesn't work
# # difference between authority and additional --> authority tells you who is in charge, additional just adds more info


# # how to check
# # can physically block the ip if error
# # just make sure the program goes through the list

print('ANSWER SECTION:')
print(final_answer)
import math
t2 = time.datetime.now()
t = t2-start_time
print('\nQUERY TIME: ', math.floor(t.microseconds/1000), ' (ms)')
print('WHEN: ', time.datetime.now())

# #printing the number of bytes stored in the answer section
# print ('\nMSG SIZE rcvd: ', server_response.answer.__sizeof__())