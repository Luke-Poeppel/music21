# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:         ismir2011.py
# Purpose:      Examples for ISMIR 2011 papers
#
# Authors:      Christopher Ariza
#               Jose Cabal-Ugaz
#               Michael Scott Cuthbert
#               Lisa D. Friedland
#
# Copyright:    (c) 2011 The music21 Project
# License:      LGPL
#-------------------------------------------------------------------------------


from music21 import corpus, features, converter
from music21 import trecento, figuredBass, tinyNotation
from music21 import expressions, stream

def example2():
    handel = corpus.parse('hwv56/movement3-05.md')
    fe = features.jSymbolic.TripleMeterFeature(handel)
    print fe.extract().vector

    # no longer works...
    soft = converter.parse("http://static.wikifonia.org/10699/musicxml.xml")
    fe.setData(soft)
    print fe.extract().vector

class MusicaFictaFeature(features.FeatureExtractor):
    name = 'Musica Ficta'
    discrete = False
    dimensions = 1
    
    def _process(self):
        allPitches = self.data['flat.pitches']
        fictaPitches = 0
        for p in allPitches:
            if p.name == "B-":
                continue
            elif p.accidental is not None and p.accidental.name != 'natural':
                fictaPitches += 1
        self._feature.vector[0] = \
           fictaPitches / float(len(allPitches))
            
def testFictaFeature():
    luca = corpus.parse('luca/gloria.mxl')
    fe = MusicaFictaFeature(luca)
    print fe.extract().vector
    mv = corpus.parse('monteverdi/madrigal.3.1.xml')
    fe.setData(mv)
    print fe.extract().vector

def testDataSet():
    fes = features.extractorsById(['ql1','ql2','ql3'])
    ds = features.DataSet(classLabel='Composer')
    ds.addFeatureExtractors(fes)
    
    b1 = corpus.parse('bwv1080', 7).measures(0,50)
    ds.addData(b1, classValue='Bach', id='artOfFugue')
    ds.addData('bwv66.6.xml', classValue='Bach')
#    ds.addData('c:/handel/hwv56/movement3-05.md', 
    ds.addData('hwv56/movement3-05.md', 
                    classValue='Handel')
    ds.addData('http://www.midiworld.com/midis/other/handel/gfh-jm01.mid')
    ds.process()
    print ds.getAttributeLabels()
    ds.write('d:/desktop/baroqueQLs.csv')
    fList = ds.getFeaturesAsList()
    print fList[0]
    print features.OutputTabOrange(ds).getString()
    for i in range(len(fList)):
        # display scores as pngs generated by Lilypond 
        # if the most common note is an eighth note (0.5)
        # (finds the two Handel scores)
        if fList[i][2] == 0.5:
            pass
#            ds.streams[i].show('lily.png')

    p = graph.PlotFeatures(ds.streams, fes[1:], roundDigits = 2)
    p.process()

def prepareChinaEurope1():
    featureExtractors = features.extractorsById(['r31', 'r32', 'r33', 'r34', 'r35', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p19', 'p20', 'p21'])
    #featureExtractors = features.extractorsById('all')

    oChina1 = corpus.parse('essenFolksong/han1')
    oCEurope1 = corpus.parse('essenFolksong/boehme10')

    ds = features.DataSet(classLabel='Region')
    ds.addFeatureExtractors(featureExtractors)
        
    # add works, defining the class value 
    for w in oChina1.scores:
        sid = 'essenFolksong/%s-%s' % ('han1', w.metadata.number)
        ds.addData(w, classValue='China', id=sid)

    for w in oCEurope1.scores:
        sid = 'essenFolksong/%s-%s' % ('europe1', w.metadata.number)
        ds.addData(w, classValue='CentralEurope', id=sid)
    # process with all feature extractors, store all features
    ds.process()
    ds.write('d:/desktop/folkTrain.tab')


def prepareChinaEurope2():
    featureExtractors = features.extractorsById(['r31', 'r32', 'r33', 'r34', 'r35', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p19', 'p20', 'p21'])

    oChina2 = corpus.parse('essenFolksong/han2')
    oCEurope2 = corpus.parse('essenFolksong/boehme20')

    ds2 = features.DataSet(classLabel='Region')
    ds2.addFeatureExtractors(featureExtractors)
        
    # add works, defining the class value 
    for w in oChina2.scores:
        sid = 'essenFolksong/%s-%s' % ('han2', w.metadata.number)
        ds2.addData(w, classValue='China', id=sid)

    for w in oCEurope2.scores:
        sid = 'essenFolksong/%s-%s' % ('europe2', w.metadata.number)
        ds2.addData(w, classValue='CentralEurope', id=sid)
    # process with all feature extractors, store all features
    ds2.process()
    ds2.write('d:/desktop/folkTest.tab')

def testChinaEuropeFull():
    import orange, orngTree
    data1 = orange.ExampleTable('d:/desktop/1.tab')
    data2 = orange.ExampleTable('d:/desktop/2.tab')

    learners = {}
    learners['maj'] = orange.MajorityLearner
    learners['bayes'] = orange.BayesLearner
    learners['tree'] = orngTree.TreeLearner
    learners['knn'] = orange.kNNLearner

    for cName in learners.keys():
        cType = learners[cName]
        for cData, cStr, matchData, matchStr in [
                  (data1, 'file1', data2, 'file2'),
                  (data2, 'file2', data1, 'file1'),
                                                 ]:
            # train with data1
            classifier = cType(cData)
            mismatch = 0
            for i in range(len(matchData)):
                c = classifier(matchData[i])
                if c != matchData[i].getclass():
                    mismatch += 1
            print('%s %s: misclassified %s/%s of %s' % (cStr, cName, mismatch, len(matchData),  matchStr))


# this test requires orange and related files
def xtestChinaEuropeSimpler():
    import orange, orngTree

    trainData = orange.ExampleTable('ismir2011_fb_folkTrain.tab')
    testData  = orange.ExampleTable('ismir2011_fb_folkTest.tab')

    majClassifier = orange.MajorityLearner(trainData)
    knnClassifier = orange.kNNLearner(trainData)
        
    majWrong = 0
    knnWrong = 0
        
    for testRow in testData:
        majGuess = majClassifier(testRow)
        knnGuess = knnClassifier(testRow)
        realAnswer = testRow.getclass()
        if majGuess != realAnswer:
            majWrong += 1
        if knnGuess != realAnswer:
            knnWrong += 1
       
    total = float(len(testData))
    print majWrong/total, knnWrong/total
    

def prepareTrecentoCadences():
    featureExtractors = features.extractorsById(['r31', 'r32', 'r33', 'r34', 'r35', 'p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7', 'p8', 'p9', 
                                                 'p10', 'p11', 'p12', 'p13', 'p14', 'p15', 'p16', 'p19', 'p20', 'p21',
                                                 'mc1', # LANDINI CADENCE                                                 
                                                 ])
    ds = features.DataSet(classLabel='Composer')
    ds.addFeatureExtractors(featureExtractors)
    ds2 = features.DataSet(classLabel='Composer')
    ds2.addFeatureExtractors(featureExtractors)

    
    allBallate = trecento.cadencebook.BallataSheet()
    for i, thisBallata in enumerate(allBallate):
        if thisBallata.composer not in ['Zacharias', 'A. Zacara', 'Ciconia']:
            continue
        if thisBallata.composer != 'Ciconia':
            thisBallata.composer = 'Zachara'
        s = thisBallata.asScore()
        if len(s.flat.pitches) < 10:
            continue
        if i % 2 == 0:
            ds.addData(s, classValue = thisBallata.composer, id=str(i))
        else:
            ds2.addData(s, classValue = thisBallata.composer, id=str(i))
        print i, thisBallata.title, thisBallata.composer
    
    ds.process()
    ds2.process()
    ds.write('d:/desktop/trecento1.tab')
    ds2.write('d:/desktop/trecento2.tab')


def testTrecentoSimpler():
    import orange, orngTree

    trainData = orange.ExampleTable('d:/desktop/trecento2.tab')
    testData  = orange.ExampleTable('d:/desktop/trecento1.tab')

    majClassifier = orange.MajorityLearner(trainData)
    knnClassifier = orange.kNNLearner(trainData)
        
    majWrong = 0
    knnWrong = 0
        
    for testRow in testData:
        majGuess = majClassifier(testRow)
        knnGuess = knnClassifier(testRow)
        realAnswer = testRow.getclass()
        if majGuess != realAnswer:
            majWrong += 1
        if knnGuess != realAnswer:
            knnWrong += 1
       
    total = float(len(testData))
    print majWrong/total, knnWrong/total

def wekaCommands():
    '''
    These commands were used to do the 10-fold Cross-validation in Weka:
    (the function does nothing; it's just a placeholder for these docs)
    
    
    # convert from CSV to ARFF (if the ARFF output from music21 wasn't used)
    java weka.core.converters.CSVLoader chinaMitteleuropa-all.csv > chinaMitteleuropa-all.arff
    
    # remove features that are the same for all pieces
    # -i: input file
    # -o: output file
    java weka.filters.unsupervised.attribute.RemoveUseless -i chinaMitteleuropa-all.arff -o chinaMitteleuropa-no-useless.arff
    
    # run Naive Bayes
    # -t: data file. Default: uses the file for both training and testing data, 
    #    running 10-fold cross validation.
    # -o: turn off some outputs we don't need
    # -i: print some additional statistics
    java weka.classifiers.bayes.NaiveBayes -o -i -t chinaMitteleuropa-no-useless.arff
    
    # Naive Bayes with supervised discretization of continuous attributes
    # -D: (above option)
    java weka.classifiers.bayes.NaiveBayes -o -i -D -t chinaMitteleuropa-no-useless.arff
    
    # run majority classifier (as baseline)
    java weka.classifiers.rules.ZeroR -i -t chinaMitteleuropa-no-useless.arff
    
    # run a decision tree
    java weka.classifiers.trees.J48 -i -t chinaMitteleuropa-no-useless.arff 
    
    # run logistic regression
    java weka.classifiers.functions.Logistic -i -t chinaMitteleuropa-no-useless.arff
    
    # run k-nearest neighbors
    # -K: how many nearest neighbors to use
    java weka.classifiers.lazy.IBk -i -K 3 -t chinaMitteleuropa-no-useless.arff
    
    # print some information about the feature distributions
    java weka.core.Instances chinaMitteleuropa-no-useless.arff
    
    
    Results:
    
    classifier           % correct
    =====================
    majority baseline    63%
    naïve Bayes          79%
    naïve Bayes with supervised discretization    91%
    decision tree        93%
    logistic regression  95%
    kNN (k=3)            96%
    '''
    pass
    


### FIGURED BASS PAPER ###

def tinyNotationBass():
    bass1 = tinyNotation.TinyNotationStream('C4 D8_6 E8_6 F4 G4_7 c1', '4/4')
    #bass1.show('lily.png')
    fbLine1 = figuredBass.realizer.figuredBassFromStream(bass1)
    fbLine1.showAllRealizations()

def figuredBassScale():
    fbScale1 = figuredBass.realizerScale. \
        FiguredBassScale("D", "major")
    print fbScale1.getSamplePitches("E3", "6")


def exampleD():
    eD = figuredBass.examples.exampleD()
    eD.fbRules.allowVoiceOverlap = True
    eD.realize()
    eD.showRandomRealizations(20)
    
def fbFeatureExtraction():
    exampleFB = converter.parse('ismir2011_fb_example1b.xml')
    fe1 = features.jSymbolic.\
         PitchClassDistributionFeature(exampleFB)
    print fe1.extract().vector
    # [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.6666666666666666, 0.0, 0.0, 1.0, 0.0, 0.0]
    n1 = exampleFB.parts[0][1][5]
    n1.expressions.append(expressions.Turn())
    x = expressions.realizeOrnaments(n1)
    n2 = exampleFB.parts[0][2][2]
    n2.expressions.append(expressions.Mordent())
    y = expressions.realizeOrnaments(n2)
    
    exampleFB.parts[0][1].elements = [exampleFB.parts[0][1][4]]
    exampleFB.parts[0][1].append(x)
    exampleFB.parts[0][2].elements = [exampleFB.parts[0][2][0], exampleFB.parts[0][2][1]]
    exampleFB.parts[0][2].append(y)
    
    fb1 = figuredBass.realizer.figuredBassFromStream(exampleFB.parts[1])
    #realization = fb1.realize()
    sol1 = fb1.generateRandomRealization()
    
    exampleFBOut = stream.Score()
    exampleFBOut.insert(0, exampleFB.parts[0])
    exampleFBOut.insert(0, sol1.parts[0])
    exampleFBOut.insert(0, sol1.parts[1])

    fe1.setData(exampleFBOut)
    print fe1.extract().vector
    #[0.0, 0.5, 1.0, 0.0, 0.6000000000000001, 0.0, 0.4, 0.2, 0.0, 0.7000000000000001, 0.0, 0.1]
    # exampleFBOut.show()

if __name__ == '__main__':
    pass
    #testTrecentoSimpler()
    #prepareTrecentoCadences()
    #figuredBassScale()
    #fbFeatureExtraction()
    #testChinaEuropeSimpler()
    
    #prepareChinaEurope2()
    #testDataSet()
    #testFictaFeature()
    #example2()


#------------------------------------------------------------------------------
# eof
