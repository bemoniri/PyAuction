import time
import pandas as pd
import os

while True:

    print("Server Check")
    current_time = time.time()
    df = pd.read_csv("auctions.csv")
    timelist = df["Time"].values
    for end_time in timelist:
        if (end_time <= current_time):

            to_del = df[df["Time"] == end_time]

            df = df[df.Time != end_time]
            df.to_csv("auctions.csv", index=False)

            old_df = pd.read_csv("old_auctions.csv")
            s = pd.Series(
                [to_del.Name.values[0], to_del.Type.values[0], to_del.Details.values[0], to_del.FirstBid.values[0],
                 to_del.Time.values[0]], index=["Name", "Type", "Details", "FirstBid", "Time"])
            old_df = old_df.append(s, ignore_index=True)
            old_df.to_csv('old_auctions.csv', index=False)

            auction_name = to_del.Name.values[0]
            auction_type = to_del.Type.values[0]

            bdf = pd.read_csv("bids.csv")
            to_del = bdf[bdf["Auction"] == auction_name]
            old_df = pd.read_csv("old_bids.csv")
            if auction_type == 1:
                ex_price = max(to_del.Price.values.tolist())
                winner = bdf[bdf["Price"] == ex_price].User.values

            else:
                ex_price = min(to_del.Price.values.tolist())
                winner = bdf[bdf["Price"] == ex_price].User.values

            email_message = "The auction " + auction_name + " has ended!" + "\n" + "The bids are as follows:\n" + str(to_del) + "\n\n\n" + "The winner is: " + winner + "\n\n\n\n" + "Best," + "PyAuction Team"

            users = to_del.User.values.tolist()
            users = list(dict.fromkeys(users))
            users_df = pd.read_csv("users.csv")
            for user_id in users:
                email = users_df[users_df["username"] == user_id].email.values.tolist()

                os.system("echo \"" + str(email_message[0]) + " \" | mutt -s \"" + "Auction Has Finished!!!" + "\" " + str(email[0]))

            bdf = bdf[bdf.Auction != auction_name]
            bdf.to_csv("bids.csv", index=False)

            for i in range(len(to_del.Auction.values)):
                s = pd.Series(
                    [to_del.Auction.values[i], to_del.Price.values[i], to_del.Time.values[i], to_del.User.values[i]],
                    index=["Auction", "Price", "Time", "User"])
                old_df = old_df.append(s, ignore_index=True)
            old_df.to_csv('old_bids.csv', index=False)
    time.sleep(3)
