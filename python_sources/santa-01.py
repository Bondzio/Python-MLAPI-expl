coal=0
book=0
bike=0
train=0
blocks=0
doll=0
horse=0
gloves=0
ball=0
with open("Santa_02.csv", 'w') as f:
        f.write("Gifts\n")
        for i in range(1000):
            if coal < 166:
                f.write('coal_'+str(coal)+' book_'+str(book))
                coal+=1
                book+=1
                f.write(' book_'+str(book)+'\n')
                book+=1
            elif bike < 500:
                f.write('bike_'+str(bike)+' train_'+str(train)+' blocks_'+str(blocks)+'\n')
                bike+=1
                train+=1
                blocks+=1
            elif blocks < 1000 and train < 1000:
                f.write('blocks_'+str(blocks)+' train_'+str(train))
                blocks+=1
                train+=1
                f.write(' blocks_'+str(blocks)+' train_'+str(train)+'\n')
                blocks+=1
                train+=1
            elif book < 1000 and gloves < 200:
                f.write('doll_'+str(doll))
                doll+=1
                f.write(' doll_'+str(doll))
                doll+=1
                f.write(' doll_'+str(doll))
                doll+=1
                f.write(' horse_'+str(horse))
                horse+=1
                f.write(' horse_'+str(horse))
                horse+=1
                f.write(' horse_'+str(horse))
                horse+=1
                f.write(' gloves_'+str(gloves))
                gloves+=1
                f.write(' ball_'+str(ball))
                ball+=1
                f.write(' ball_'+str(ball))
                ball+=1
                f.write(' ball_'+str(ball))
                ball+=1
                f.write(' ball_'+str(ball))
                ball+=1
                f.write(' ball_'+str(ball))
                ball+=1
                f.write(' ball_'+str(ball))
                ball+=1
                f.write(' book_'+str(book)+'\n')
                book+=1
                


print("coal",coal)                
print("horse",horse)
print("book",book)
print("bike",bike)
print("gloves",gloves)
print("train",train)
print("ball",ball)
print("doll",doll)
print("bike",bike)
            