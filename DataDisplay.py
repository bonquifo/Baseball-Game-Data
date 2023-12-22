import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from jinja2 import Environment, FileSystemLoader
import math
from mpl_toolkits.mplot3d import Axes3D
#optional setting
pd.options.display.max_rows = 999

df = pd.read_csv('20220423-Olsen-1.csv')
#########################################################################################################
#Game overview
x = df.loc[:,['BatterTeam', 'RunsScored']]
y1 = x.loc[(x['BatterTeam'] == 'ARK_RAZ') & (x['RunsScored'] >= 0)]
z = y1['RunsScored']
#ARK_RAZ score
arkRAZScore = sum(z)

x = df.loc[:,['BatterTeam', 'RunsScored']]
y2 = x.loc[(x['BatterTeam'] == 'TEX_AGG') & (x['RunsScored'] >= 0)]
a = y2['RunsScored']
#TEX_AGG score
texAGGScore = sum(a)

#Final Game Scores
print('ARK: ', arkRAZScore)
print('TEX: ', texAGGScore)

#pitches thrown by team
pitchesByTeam= df.loc[:,['PitcherTeam', 'TaggedPitchType', 'PitchCall']]

totalPitches = len(pitchesByTeam['PitcherTeam'])

print('Total number of pitches during the game: ', totalPitches)

########### - Ark Pitching Percentage - #######################
arkTable = pitchesByTeam[pitchesByTeam['PitcherTeam'] == 'ARK_RAZ']

arkPitches = len(arkTable['PitcherTeam'])

####### - Texas Pitching Percentage - ##################

texTable = pitchesByTeam[pitchesByTeam['PitcherTeam'] == 'TEX_AGG']

texPitches = len(texTable['PitcherTeam'])

print('Ark threw ', arkPitches, 'while Tex threw ', texPitches)

#Percentages# 
aPP = (arkPitches/totalPitches)*100

tPP = (texPitches/totalPitches)*100

#graph visualizations

p = np.array([aPP, tPP])
pLabels = ['Ark Pitches ' , 'Tex Pitches ']


pie = plt.pie(p,autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.legend(title='Pitch Percentage by Team', labels = pLabels, bbox_to_anchor = (1, -0.4), loc = 'lower right')
plt.tight_layout()
plt.show()
#plt.savefig('path/to/pitch_percentage_pie_chart.png')  # Save the pie chart to an image file


#pandas series of innings
innings = df['Inning']

inningsAbs = set((innings))

outsTotal = sum(df['Outs'])
o = df['Outs']
ballsTotal = sum(df['Balls'])
ba = df['Balls']
strikesTotal = sum(df['Strikes'])
s = df['Strikes']
outsOnPlayTotal = sum(df['OutsOnPlay'])
oop = df['OutsOnPlay']

def outsPerInning(inning):
    x = df.loc[:,['Inning', 'Outs','Balls','Strikes','OutsOnPlay','Top/Bottom']]
    y = x.loc[x['Inning'] == inning]
    outs = y['Outs'].sum()
    balls = y['Balls'].sum()
    strikes = y['Strikes'].sum()
    outsOnplay = y['OutsOnPlay'].sum()

    #print('There were', outs, ' outs', balls, 'balls', strikes, 'strikes and', outsOnplay, 'during inning', inning, '!')

    #TOP = ARK_RAZ

    z = y['Top/Bottom']
    ark = 0
    tex = 0
    for i in z:
        if(i == 'Top'):
            ark +=1
        else:
            tex += 1

    arkOuts = (ark/outs)*100
    arkBalls = (ark/balls)*100
    arkStrikes = (ark/strikes)*100
    arkOPP = (ark/outsOnplay)*100

    texOuts = (tex/outs)*100
    texBalls = (tex/balls)*100
    texStrikes = (tex/strikes)*100
    texOPP = (tex/outsOnplay)*100

    #print('Of the', outs, 'outs', arkOuts, 'percent of them were from Ark while', texOuts, 'percent of them are from tex')



o1 = outsPerInning(1)
o2 = outsPerInning(2)
o3 = outsPerInning(3)
o4 = outsPerInning(4)
o5 = outsPerInning(5)
o6 = outsPerInning(6)
o7 = outsPerInning(7)
o8 = outsPerInning(8)
o9 = outsPerInning(9)


              
#chart visual#
data = {
    'Balls': ba,
    'Strikes': s,
    'Outs': o,
    'OutsOnPlay': oop
}



# Plotting the histogram





#Pitcher class to display individual stats 
class pitcher:
    def __init__(self, name):
        self.name = name
      

    def getName(self):
        return self.name
    
    #Returns the rows associated with pitcher with catValue being a minimum value
    def statSearch(self, category, catValue):

        #Returns all rows containing pitcher name AND catValue being a minimum
        x = df.loc[(df['Pitcher'] == self.name) and (df[category] >= catValue)]
        y = x.loc[:,['Pitcher', category]]
        return y
    #Returns rows where pitcher was present then counts number of rows and number of rows returned = number of pitches that player made
    def pitchesThrown(self):
        x = df.loc[df['Pitcher'] == self.name]
        y = len(x['Pitcher'])
        return y
    #Returns all pitches thrown by certain pitcher
    def pitchPlay(self):
        ball = 0
        strike = 0
        foul = 0 
        fair = 0
        
        x = df.loc[(df['Pitcher'] == self.name) & (df['PitchCall'] != None)]
        y = x.loc[:, ['Pitcher', 'PitchCall']]
        pitchResult = y['PitchCall']

        #Iterator to sort out frequency of each pitch relative to each pitcher
        
      
        z = list(pitchResult)
        for i in z:
            if((i =='BallCalled') or (i == 'BallinDirt')):
                ball += 1
            elif(i =='InPlay'):
                fair += 1
            elif((i == 'StrikeCalled') or (i == 'StrikeSwinging')):
                strike += 1
            else:
                foul += 1
        title = 'Result of Pitches Thrown'
        p = np.array([ball, strike, foul, fair])
        pitchLabels = ['Balls', 'Strikes', 'Fouls', 'Fair']
        plt.pie(p, autopct='%1.1f%%')
        plt.legend(title = title, bbox_to_anchor = (1, -0.4), labels= pitchLabels,loc = 'lower right')
        plt.tight_layout()
        plt.show()

    #Method to break down each type of pitch thrown by pitcher
    def pitchTypes(self):
        fastBall = 0
        slider = 0
        curveBall = 0
        changeUp = 0

        x = df.loc[(df['Pitcher'] == self.name) & (df['TaggedPitchType'] != None)]
        y = x.loc[:, ['Pitcher', 'TaggedPitchType']] 
        pitches = y['TaggedPitchType']

        for i in pitches:
            if(i == 'Fastball'):
                fastBall += 1
            elif(i == 'Slider'):
                slider += 1
            elif(i == 'ChangeUp'):
                changeUp += 1
            else:
                curveBall += 1
        pTitle = 'Composition of Pitches Thrown'
        p = np.array([fastBall, slider, curveBall, changeUp])
        pitchLabels = ['Fastballs', 'Sliders', 'Curveballs', 'ChangeUps']
        plt.pie(p, labels = pitchLabels, autopct='%1.1f%%')
        plt.legend(title = pTitle, bbox_to_anchor = (1, -0.4), loc = 'lower right')
        plt.tight_layout()
        plt.show()

    def ERA(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['RunsScored'] >= 0)]
        y = x.loc[:, ["Pitcher", "RunsScored"]]
        z = y['RunsScored']
        earnedRuns = sum(z)
        
        a = df.loc[(df['Pitcher'] == self.name) & (df['Inning'] >= 1)]
        b = a['Inning']
        #to eliminate duplicates
        c = set((b))
        inningsPitched = max(c)
        era = 9 * (earnedRuns/inningsPitched)

        return era
    
    def strikePercentage(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['RunsScored'] >= 0)]
        y = x.loc[:, ["Pitcher", "RunsScored"]]
        z = y['RunsScored']
        runs = sum(z)

        a = df.loc[(df['Pitcher'] == self.name) & (df['RunsScored'] >= 0)]
        b = a.loc[:, ['Pitcher', 'Balls']]
        c = b['Balls']
        
        ballsFaced = sum(c)

        strikeP = (runs/ballsFaced) * 100

        return strikeP
    
    #Average pitches thrown per plate appearance
    def averagePPA(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['PitchofPA'])]
        y = x['PitchofPA']
        z = (sum(y)/len(y))
        return z
    
    def WHIP(self):
        hits = 0
        walks = 0

        x = df.loc[(df['Pitcher'] == self.name) & (df['KorBB'])]
        y = x['KorBB']

        for i in y:
            if(i == 'Walk'):
                walks += 1
            
        a = df.loc[(df['Pitcher'] == self.name) & (df['PitchCall'])]
        b = a['PitchCall']

        for j in b:
            if(j == 'InPlay'):
                hits += 1
        
        c = df.loc[(df['Pitcher'] == self.name) & (df['Inning'])]
        d = c['Inning']
        inningsPitched = max(d)

        wh = hits + walks

        whip = (wh/inningsPitched)

        return whip

        
    def pitchSpeed(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['RelSpeed'] > 80)]
        y = x['RelSpeed']

        avgSpeed = (sum(y)/len(y))

        fastestPitch = max(y)

        slowestPitch = min(y)

        print('Fastest Pitch for ', self.name, "is: ", fastestPitch)
        print('Average Pitch for ', self.name, "is: ", avgSpeed)
        print('Slowest Pitch for ', self.name, "is: ", slowestPitch)

    def fastestPitch(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['RelSpeed'] > 70)]
        y = x['RelSpeed']

        fastestPitch = max(y)
        return fastestPitch
    def avgPitch(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['RelSpeed'] > 80)]
        y = x['RelSpeed']

        avgSpeed = (sum(y)/len(y))

        return avgSpeed
    
    def slowesetPitch(self):
        x = df.loc[(df['Pitcher'] == self.name) & (df['RelSpeed'] > 80)]
        y = x['RelSpeed']

        slowestPitch = min(y)

        return slowestPitch
    
    def ballPosition(self):
        x = df.loc[df["Pitcher"] == self.name]
        axisCoords = x.loc[:,["Pitcher", "x0", "y0", "z0"]]
        
        x0 = axisCoords['x0']
        y0 = axisCoords['y0']
        z0 = axisCoords['z0']
        #Average of initial position coordinates
        xInitialAvg = (sum(x0)/len(x0))
        yInitialAvg = (sum(y0)/len(y0))
        zInitialAvg = (sum(z0)/len(z0))
        
        #Average of initial velocity coordinates
        
        axisCoordsV = x.loc[:,["Pitcher", "vx0", "vy0", "vz0"]]

        vx0 = axisCoordsV['vx0']
        vy0 = axisCoordsV['vy0']
        vz0 = axisCoordsV['vz0']

        vxInit = (sum(vx0)/len(vx0))
        vyInit = (sum(vy0)/len(vy0))
        vzInit = (sum(vz0)/len(vz0))

        graph = plt.figure()
        graph2 = plt.figure()
        graph3 = plt.figure()
        px = graph.add_subplot(111, projection='3d')
        vx = graph2.add_subplot(111, projection='3d')
        ax = graph3.add_subplot(111, projection='3d')


        #Scatterplot

        px.scatter(xInitialAvg,yInitialAvg,zInitialAvg,c='r', marker= 'o')
        
        px.set_xlabel('X position')
        px.set_ylabel('Y position')
        px.set_zlabel('Z position')

        #Velocity plot

        vx.plot(vxInit, vyInit, vzInit, c='b', label= 'Line')
        px.legend()

        # Show the plot
        plt.show()

   




################## - END OF PITCHER CLASS ############################################################


class batter:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return f"Batter(name{self.name})"
    
    def getName(self):
        return self.name

    def statSearch(self, category, catValue):

        #Returns all rows containing pitcher name AND catValue being a minimum
        x = df.loc[(df['Batter'] == self.name) & (df[category] >= catValue)]
        y = x.loc[:,['Batter', category]]
        return y

    def battingAverage(self):
        otherStuff = 0
        hits = 0

        x = df.loc[df['Batter'] == self.name]
        y = x['PitchofPA']
        atBats = sum(y)
        #atBats calculated from sum of pitches per plate appearance for that batter

        z = x['PlayResult']

        #Hits calculated by result of plays
        for i in z:
            if(i == 'Single'):
                hits += 1
            elif(i == 'HomeRun'):
                hits += 1
            elif(i == 'Double'):
                hits += 1
            else:
                otherStuff += 1

        bAvg = (hits/atBats)


        return bAvg
    

    def OBP(self):
        hits = 0
        walks = 0
        otherStuff = 0
        
        x = df.loc[df['Batter'] == self.name]
        y = x['PitchofPA']
        atBats = sum(y)


        z = x['PlayResult']

        #Hits calculated by result of plays
        for i in z:
            if(i == 'Single'):
                hits += 1
            elif(i == 'HomeRun'):
                hits += 1
            elif(i == 'Double'):
                hits += 1
            else:
                otherStuff += 1

        #walks calculation
        a = df.loc[(df['Batter'] == self.name) & (df['KorBB'])]
        b = a['KorBB']

        for j in b:
            if(j == 'Walk'):
                walks += 1
        
        obp = ((hits+walks)/(hits+walks+atBats))

        return obp
    
    def SLG(self):
        x = df.loc[df['Batter'] == self.name]
        y = x['PitchofPA']
        atBats = sum(y)

        bases = 0

        z = x['PlayResult']

        #Hits calculated by result of plays
        for i in z:
            if(i == 'Single'):
                bases += 1
            elif(i == 'HomeRun'):
                bases += 4
            elif(i == 'Double'):
                bases += 2
            elif(i == 'Triple'):
                bases += 3
        
        slg = (bases/atBats)
        
        return slg
    
    #OBP + SlG
    def OPS(self):
        x = df.loc[df['Batter'] == self.name]
        y = x['PitchofPA']
        atBats = sum(y)

        bases = 0

        z = x['PlayResult']

        #Hits calculated by result of plays
        for i in z:
            if(i == 'Single'):
                bases += 1
            elif(i == 'HomeRun'):
                bases += 4
            elif(i == 'Double'):
                bases += 2
            elif(i == 'Triple'):
                bases += 3
        
        slg = (bases/atBats)
        ###########################
        hits = 0
        walks = 0
        otherStuff = 0
        
        a = df.loc[df['Batter'] == self.name]
        b = x['PitchofPA']
        atBats = sum(b)


        c = a['PlayResult']

        #Hits calculated by result of plays
        for j in c:
            if(j == 'Single'):
                hits += 1
            elif(j == 'HomeRun'):
                hits += 1
            elif(j == 'Double'):
                hits += 1
            else:
                otherStuff += 1

        #walks calculation
        e = df.loc[(df['Batter'] == self.name) & (df['KorBB'])]
        f = e['KorBB']

        for k in f:
            if(k == 'Walk'):
                walks += 1
        
        obp = ((hits+walks)/(hits+walks+atBats))
        
        ops = slg + obp

        return ops

    def RBI(self):
        x = df.loc[(df['Batter'] == self.name) & (df['PAofInning'] > 0)]
        y = x.loc[:,['Batter', 'RunsScored']]
        z = y['RunsScored']
        rbi = sum(z)
        return rbi
    
    def againstPitches(self):
        x = df.loc[(df['Batter'] == self.name)]
        pitches = x['TaggedPitchType']
        pitchesFaced = len(x['Batter'])

        fastball = 0
        slider = 0
        changeUp = 0
        curveball = 0


        for i in pitches:
            if(i == 'Fastball'):
                fastball += 1
            elif(i == 'Slider'):
                slider += 1
            elif(i == 'ChangeUp'):
                changeUp += 1
            else:
                curveball += 1
        
        fPercent = (fastball/pitchesFaced)*100
        sPercent = (slider/pitchesFaced)*100
        cP = (changeUp/pitchesFaced)*100
        curveP = (curveball/pitchesFaced)*100

        p = np.array([fPercent, sPercent, curveP, cP])


        pitchLabels = ['Fastballs', 'Sliders', 'Curveballs', 'ChangeUps']

        plt.pie(p, startangle=90, autopct='%1.1f%%')
        
        plt.legend(title='Pitches faced', labels = pitchLabels, bbox_to_anchor = (1, -0.4), loc = 'lower right')
        plt.tight_layout()
        plt.show()

    #####################################################################
        Faststrike = 0
        SlideStrike = 0
        ChangeStrike = 0
        CurveStrike = 0
    
        FastHit = 0
        SlideHit = 0
        ChangeHit = 0
        CurveHit = 0

        strikeCount = 0
        hitCount = 0
        ####### Total Strikes in pitches faced ###################
        strikeTot = x['PitchCall']
        for j in strikeTot:
            if(j == 'StrikeCalled'):
                strikeCount += 1
            elif(j == 'StrikeSwinging'):
                strikeCount += 1
            elif(j == 'InPlay'):
                hitCount += 1
            elif(j == 'FoulBall'):
                hitCount += 1

        #strike and hit count should be full by now
        ########## Strikes against certain types of pitches #################
        #Fastball
        a = x.loc[:,['Batter', 'TaggedPitchType', 'PitchCall']]
        b = a.loc[a['TaggedPitchType'] == 'Fastball']
        fastBalls = b['PitchCall']
        for n in fastBalls:
            if(n == 'StrikeCalled'):
                Faststrike += 1
            elif(n == 'StrikeSwinging'):
                Faststrike += 1
            elif(n == 'InPlay'):
                FastHit += 1
            elif(n == 'FoulBall'):
                FastHit += 1
        
        #slider 
        c = a.loc[a['TaggedPitchType'] == 'Slider']
        sliders = c['PitchCall']
        for k in sliders:
            if(k == 'StrikeCalled'):
                SlideStrike += 1
            elif(k == 'StrikeSwinging'):
                SlideStrike += 1
            elif(k == 'InPlay'):
                SlideHit += 1
            elif(k == 'FoulBall'):
                SlideHit += 1
        #ChangeUp
        d = a.loc[a['TaggedPitchType'] == 'ChangeUp']
        changeUps = d['PitchCall']
        for l in changeUps:
            if(l == 'StrikeCalled'):
                ChangeStrike += 1
            elif(l == 'StrikeSwinging'):
                ChangeStrike += 1
            elif(l == 'InPlay'):
                ChangeHit += 1
            elif(l == 'FoulBall'):
                ChangeHit += 1   
        #Curveballs
        e = a.loc[a['TaggedPitchType'] == 'Curveball']
        curveBalls = e['PitchCall']
        for m in curveBalls:
            if(m == 'StrikeCalled'):
                CurveStrike += 1
            elif(m == 'StrikeSwinging'):
                CurveStrike += 1
            elif(m == 'InPlay'):
                CurveHit += 1
            elif(m == 'FoulBall'):
                CurveHit += 1

        overallStrike = (strikeCount/pitchesFaced)*100
        overallHit = (hitCount/pitchesFaced)*100

        fastP = (Faststrike/strikeCount)*100
        slideP = (SlideStrike/strikeCount)*100
        ChangeP = (ChangeStrike/strikeCount)*100
        curP = (CurveStrike/strikeCount)*100

        fastH = (FastHit/hitCount)*100
        SlideH = (SlideHit/hitCount)*100
        ChangeH = (ChangeHit/hitCount)*100
        curH = (CurveHit/hitCount)*100



        weakPitch = np.array([fastP, slideP, ChangeP, curP])
        
        wp = [fastP, slideP, ChangeP, curP]
        
        pLabels = ['FastBall', 'Slider', 'ChangeUp', 'CurveBall']


        plt.pie(weakPitch,autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.legend(title='Strike Percentage Per Pitch Type', labels = pLabels, bbox_to_anchor = (1, -0.3), loc = 'lower right')
        plt.tight_layout()
        plt.show()

        weakestPitch = max(wp)

        print('This player strikes mostly on ', weakestPitch)

        ####### Strength ############

        strongPitch = np.array([fastH, SlideH, ChangeH, curH])
        
        sp = [fastH, SlideH, ChangeH, curH]
    
        plt.pie(strongPitch, autopct='%1.1f%%', startangle=90)
        plt.axis('equal')
        plt.legend(title='Hit Percentage Per Pitch Type', labels = pLabels, bbox_to_anchor = (1, -0.3), loc='lower right')
        plt.tight_layout()
        plt.show()

        strongestPitch = max(sp)

        print('This player hits mostly on ', strongestPitch)
    
    def hitSpeed(self):
        x = df.loc[(df['Batter'] == self.name) & (df['ExitSpeed'] != None)]
        y = x['ExitSpeed']

        avgSpeed = (sum(y)/len(y))

        fastestHit = max(y)

        slowestHit = min(y)

        print('Strongest Hit by exit speed for ', self.name, "is: ", fastestHit)
        print('Average Hit by exit speed for ', self.name, "is: ", avgSpeed)
        print('Weakest hit by exit speed for ', self.name, "is: ", slowestHit)
    
    def fastestHit(self):
        x = df.loc[(df['Batter'] == self.name) & (df['ExitSpeed'] != None)]
        y = x['ExitSpeed']

        fastestHit = max(y)

        return fastestHit


    def avgHit(self):
        x = df.loc[(df['Batter'] == self.name) & (df['ExitSpeed'] != None)]
        y = x['ExitSpeed']

        avgSpeed = (sum(y)/len(y))

        return avgSpeed

        

    def slowestHit(self):
        x = df.loc[(df['Batter'] == self.name) & (df['ExitSpeed'] != None)]
        y = x['ExitSpeed']

        slowestHit = min(y)

        return slowestHit

   


########### - END OF BATTER CLASS - ################################################

#To return all rows of select columns only this makes a new dataframe
#z = df.loc[:,["Pitcher", "Outs"]]
#Overall game analysis functions
#Post game leaders 

def homerunHitters():
        x = df.loc[:,['Batter', 'PlayResult']]
        y = x['PlayResult']
        a = x['Batter']
        b = x['PlayResult']
        homeRuns = 0
        for i in y:
            if(i == 'HomeRun'):
                homeRuns += 1

        
        hitters = dict(zip(b,a))

        print('There were', homeRuns, 'homeruns in this game by', hitters["HomeRun"]) 

        

  








def bestPitchers():
    series = df['Pitcher']
    series2 = set(series)
    v = [pitcher(a) for a in series2]

    eras = [b.ERA() for b in v]
    names = [c.getName() for c in v]

# Builds the dictionary using two arrays
    pEra = dict(zip(names, eras))

    target = min(eras)

    best_pitcher_name = [name for name, era in pEra.items() if era == target][0]

    print("Best Pitcher by ERA is:", best_pitcher_name, "with an ERA of: ", pEra[best_pitcher_name])
    bestERA = pEra[best_pitcher_name]
    return best_pitcher_name, bestERA
   
def worstPitchers():
    series = df['Pitcher']
    series2 = set(series)
    v = [pitcher(a) for a in series2]

    eras = [b.ERA() for b in v]
    names = [c.getName() for c in v]
    
# Builds the dictionary using two arrays
    pEra = dict(zip(names, eras))

    worstTarget = max(eras)

    worst_pitcher_name = [name for name, era in pEra.items() if era == worstTarget][0]

    print("Worst Pitcher by ERA is:", worst_pitcher_name, 'with an ERA of: ', pEra[worst_pitcher_name])
    worstERA = pEra[worst_pitcher_name]
    return worst_pitcher_name, worstERA


def bestBatters():
    series = df['Batter']
    series2 = set(series)
    #list comprehension for batters as objects
    v = [batter(a) for a in series2]

    obps = [b.OBP() for b in v]
    names = [c.getName() for c in v]

# Builds the dictionary using two arrays
    pObp = dict(zip(names, obps))

    target = max(obps)

    best_batter_name = [name for name, obp in pObp.items() if obp == target][0]

    print("Best Batter by OBP is:", best_batter_name, 'with an OBP of : ', pObp[best_batter_name])
    bestOBP = pObp[best_batter_name]
    return best_batter_name, bestOBP

def worstBatters():
    series = df['Batter']
    series2 = set(series)
    #list comprehension for batters as objects
    v = [batter(a) for a in series2]

    obps = [b.OBP() for b in v]
    names = [c.getName() for c in v]

# Builds the dictionary using two arrays
    pObp = dict(zip(names, obps))

    target = min(obps)

    worst_batter_name = [name for name, obp in pObp.items() if obp == target][0]

    print("Worst Batter by OBP is:", worst_batter_name, "with an OBP of: ", pObp[worst_batter_name])
    worstObp = pObp[worst_batter_name]
    return worst_batter_name, worstObp


def fastestHitBySpeed(gameBatters):

    x = []

    for i in gameBatters:
        if i.fastestHit() is not None:
            x.append(i.fastestHit())

    # Filter out NaN values using list comprehension and math.isnan
    y = [hit for hit in x if not math.isnan(hit)]
    fastestPitchThrown = max(y)
  
    print('The strongest hit of the game was', fastestPitchThrown, 'mph thrown by')    



#TEX_AGG vs ARK_RAZ
#All pitchers
p1 = pitcher('Dallas, Micah')
p2 = pitcher('Smith, Hagen')
p3 = pitcher('Morris, Zack')
p4 = pitcher('Taylor, Evan')
p5 = pitcher('Tygart, Brady')
p6 = pitcher('Tucker, Wyatt')
p7 = pitcher('Menefee, Joseph')
p8 = pitcher('Vermillion, Zebulon')

#All batters
b1 = batter('Slavens, Brady')
b2 = batter('Wallace, Cayden')
b3 = batter('Targac, Ryan')
b4 = batter('Moss, Jack')
b5 = batter('Gregory, Zack')
b6 = batter('Moore, Robert')
b7 = batter('Thompson, Jordan')
b8 = batter('Stovall, Peyton')
b9 = batter('Werner, Trevor')
b10 = batter('Leach, Dylan')
b11 = batter('Turner, Michael')
b12 = batter('Rock, Dylan')
b13 = batter('Kaler, Kole')
b14 = batter('Claunch, Troy')
b15 = batter('Lanzilli, Chris')
b16 = batter('Bohrofen, Jace')
b17 = batter('Bost, Austin')
b18 = batter('Minnich, Brett')
b19 = batter('Britt, Logan')
b20 = batter('Webb, Braydon')





gamePitchers = [p1, p2, p3, p4, p5 ,p6, p7, p8]

gameBatters = [b1, b2, b3, b4, b5, b6, b7, b8, b9, b10, b11, b12, b13, b14, b15, b16, b17, b18, b19, b20]





#worst players





#b15.againstPitches()


#best and worst pitchers of game
bestPitcherName = bestPitchers()
worstPitcherName = worstPitchers()
bestBatterName = bestBatters()
worstBatterName = worstBatters()

env = Environment(loader=FileSystemLoader('.'))
template = env.get_template('testTemplate.html')

# Render the template with the data through jinja2
output = template.render(
    arkRAZScore=arkRAZScore,
    texAGGScore=texAGGScore,
    totalPitches=totalPitches,
    arkPitches=arkPitches,
    texPitches=texPitches,
    aPP=aPP,
    tPP=tPP,
    bestPitcherName=bestPitchers(),
    worstPitcherName=worstPitchers(),
    bestBatterName=bestBatters(),
    worstBatterName=worstBatters(),
    homeRunners = homerunHitters(),
    fastestHitBySpeed=fastestHitBySpeed(gameBatters),
    averagePPA = p5.averagePPA(),
    avgPitch = p5.avgPitch(),
    pitchesThrown = p5.pitchesThrown(),
    pitchTypes = p5.pitchTypes(),
    slowestPitch = p5.slowesetPitch(),
    pitcherWHIP = p5.WHIP(),
    slugging = b15.SLG(),
    RBI = b15.RBI(),
    OBP = b15.OBP(),
    OPS = b15.OPS(),
    averageHit = b15.avgHit(),
    againstPitches = b15.againstPitches(),
    battingAverage = b15.battingAverage(),
    weakestHit = b15.slowestHit(),
    worstERA = p1.ERA(),
    worstPPA = p1.averagePPA(),
    worstPitchPlay = p1.pitchPlay(),
    worstPitchSpeed = p1.fastestPitch(),
    worstPitchesThrown = p1.pitchesThrown(),
    worstWHIP = p1.WHIP()
    

)

# Save the HTML report to a file
with open('game_report2.html', 'w') as file:
    file.write(output)

