for player in players:
        
            getcontext().prec = 6
            postmove2_make = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Make",Possession.shot=="PM2")).count())
            postmove2_miss = Decimal(db.session.query(Possession).filter(and_(Possession.shooter==player.id,Possession.result=="Miss",Possession.shot=="2")).count())
            if (postmove2_make+postmove2_miss)!=0:
                
                postmove2_perc = postmove2_make/(postmove2_make+postmove2_miss)*Decimal(100)
                getcontext().prec = 4
                postmove2_perc_round = postmove2_perc+Decimal(0)
                postmove2.append(str(postmove2_perc_round)+"%")
                s_postmove2 += postmove2_perc
                s_postmove2_shooters += 1
            else:
                postmove2.append("-")
            
            
            
            
            
            
getcontext().prec = 4
if s_postmove2_shooters != 0:
    s_postmove2 = Decimal(s_postmove2)/Decimal(s_postmove2_shooters)
    s_postmove2 = str(s_postmove2)+"%"



postmove2 = postmove2,
                           s_postmove2=s_postmove2,