import random
import string
import os, sys
import pandas as pd
global auctionDF
global bidDF

auctionDF = pd.DataFrame( columns=['Name', 'Type', 'Details', 'FirstBid', 'Time'])
bidDF = pd.DataFrame(columns = ['Auction', 'User', 'Time', 'Price'])

def create_auction(name, type, details, firstbid, time):
    global auctionDF
    data = [[name, type, details, firstbid, time]]
    auctionDF2 = pd.DataFrame(data, columns = ['Name', 'Type', 'Details', 'FirstBid', 'Time'])
    auctionDF = auctionDF.append(auctionDF2)

def create_bid(auction, user, time, price):
    global bidDF
    data = [[auction, user, time, price]]
    bidDF2 = pd.DataFrame(data, columns=['Auction', 'User', 'Time', 'Price'])
    bidDF = bidDF.append(bidDF2)

def view_auctions():
    print(auctionDF)

while True:
    print("-------------------------")
    print(auctionDF)
    print("-------------------------")
    print(bidDF)
    print("-------------------------")
    command = input("Enter Command: ")

    if(command == "view"):
        view_auctions()

    if (command == "create"):

        name = input("Name: ")
        type = input("Type: ")
        details = input("Details: ")
        firstbid = input("firstbid: ")
        time = input("Time: ")
        create_auction(name=name, type=type, details=details, firstbid= firstbid, time=time)
        print("Auction Created")

    if (command == "bid"):
        auction_name = input("Auction Name: ")
        listofauctions = auctionDF[auctionDF["Name"] == auction_name]
        auctiontype = listofauctions["Type"].values[0]
        print(auctiontype)
        bid_price = input("Bid: ")
        extbid = listofauctions["FirstBid"].values[0]

        if int(auctiontype) == 1:
            if int(bid_price) >= int(extbid):
                print("inside")
                create_bid(auction_name, user="bemoniri", time="", price=bid_price)
        else:
            if int(bid_price) <= int(extbid):
                print("insidenot")
                create_bid(auction_name, user="bemoniri", time="", price=bid_price)
