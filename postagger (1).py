#!/usr/bin/env python

from optparse import OptionParser
import os, logging
import utils
import copy
import collections
import operator




def create_model(sentences):
	 ## YOUR CODE GOES HERE: create a model
    
    model = collections.defaultdict(str)
    counts = collections.defaultdict(int)
    tagsperwordcoll = collections.defaultdict(str)
    allDistinctTags = []
    for sentence in sentences:
        for token in sentence:
            word = token.word
            tag = token.tag
            if not tag in allDistinctTags:
                allDistinctTags.append(tag)
            counts[word + '/' + tag] += 1
            tag += '_'
            tagsineachwordstr = tagsperwordcoll[word]
            if not tag in tagsineachwordstr:
                tagsperwordcoll[token.word] += tag

    for word1 in tagsperwordcoll.keys():
        temptaglist = tagsperwordcoll[word1].split('_')
        max = 0
        maxtag = ''
        for temptag in temptaglist:
            if counts[word1 + '/' + temptag] > max:
                max = counts[word1 + '/' + temptag]
                maxtag = temptag
        model[word1] = maxtag
    return model

    ## YOUR CODE GOES HERE: create a model

    #return model

def predict_tags(sentences, model):
    ## YOU CODE GOES HERE: use the model to predict tags for sentences
    for sentence in sentences:
        for token in sentence:
                token.tag = model[token.word]
                if model[token.word] is '':
                        token.tag = "NN"		
            #token.tag = model.get(token.word,'NN')
    return sentences

def rule1(predictedtags,originaltags):
    rules = {}
    x =0
    assert len(originaltags) == len(predictedtags),"Gold and system don't have the same number of sentence"
    
    for sent in range(len(originaltags)):
            assert len(originaltags[sent]) == len(predictedtags[sent]), "Different number of token in sentence:\n%s" % originaltags[sent]
            tokennumb =1;
            for handtag,predictedtag in zip(originaltags[sent],predictedtags[sent]):
                    
                    if(tokennumb == 1):
                            tokennumb = 0;
                            previoustag = predictedtag.tag
                            continue
                    if(handtag.tag != predictedtag.tag):
                            x+= 1
                            templist =(previoustag,predictedtag.tag,handtag.tag)
                            #print "rule added"
                            #print templist
                            #print "-----------------------------------"
                            if templist in rules:
                                    rules[templist]+=1;
                            else:
                                    rules[templist]=1
                    previoustag = predictedtag.tag;
    #print x
                
    return rules

    
def correctrules(predictions, rules):
    for rule in rules:
        previoustag = rule[0]
        initaltag =rule[1]
        totag=rule[2]
        for sentences in predictions:
                firstoken = 1
                for token in sentences:
                        if (firstoken == 1):
                                firstoken = 0
                                previoustrainingtag = token.tag
                                continue
                        if(token.tag == initaltag):
                                if(previoustag == previoustrainingtag):
                                        token.tag =totag
                        previoustrainingtag = token.tag
    return predictions


def filter_rule1(rules, training_sents, predictions,accuracy):
    filtered_rules = []
    
    loop=0
    for templist in rules:
            if(rules[templist]>100):
                    predictions1 = copy.deepcopy(predictions)
                    eachrule = []
                    eachrule.append(templist)
                    new_Predictions = correctrules(predictions1,eachrule)
                    accuracy1 = utils.calc_accuracy(training_sents,new_Predictions)
                    loop+=1
                    print "%s" % loop
                    if(accuracy1 > accuracy):
                            filtered_rules.append(templist)
                    #print accuracy1
    return filtered_rules



def create_rule2(training_sents, predictions):
        rules = collections.defaultdict(int)
        y =0
        print 'in create rule'
        assert len(training_sents) == len(predictions), "Gold and system don't have the same number of sentence"
        for sent_i in range(len(training_sents)):  # for sentence in sentences:
                assert len(training_sents[sent_i]) == len(predictions[sent_i]), "Different number of token in sentence:\n%s" % training_sents[sent_i]
                firstToken = 0
                previousTaginSentence = ''
                for gold_tok, system_tok in zip(training_sents[sent_i], predictions[sent_i]): # for token in sentence
                        if (firstToken == 1):
                                firstToken =1
                                previous2TaginSentence = previousTaginSentence
                                previousTaginSentence = system_tok.tag
                                continue
                        if (gold_tok.tag != system_tok.tag):
                                #y+=1
                                #print y
                                templist = (previousTaginSentence, system_tok.tag, gold_tok.tag) #[z,x,y]
                                rules[templist]+=1
                        previous2TaginSentence = previousTaginSentence
                        previousTaginSentence = system_tok.tag

        return rules

def filter_rule2(rules, training_sents, predictions,accuracy):
    filtered_rules = []
    loop=0
    for templist in rules.keys():
        if(rules[templist]>100):
            predictions1 = copy.deepcopy(predictions)
            eachrule = []
            eachrule.append(templist)
            new_Predictions = correct_rule2(predictions1,eachrule)
            accuracy1 = utils.calc_accuracy(training_sents,new_Predictions)
            loop+=1
            print "%s" % loop
            if(accuracy1 > accuracy):
                filtered_rules.append(templist)
            #print accuracy1
    return filtered_rules

def correct_rule2(predictions, rules):
        print 'in creatine correct rules'
        for rule in rules:
                previousTag = rule[0]
                fromTag = rule[1]
                toTag = rule[2]
                for sentence in predictions:
                        firstToken = 0
                        previousTaginSentence = ''
                        for token in sentence:
                                if (firstToken == 1):
                                        firstToken = 1
                                        previous2TaginSentence = previousTaginSentence
                                        previousTaginSentence = token.tag
                                        continue
                                if (token.tag == fromTag):
                                        if (previousTag == previousTaginSentence):
                                                token.tag = toTag
                                previous2TaginSentence = previousTaginSentence
                                previousTaginSentence = token.tag
        return predictions



def create_rule3(training_sents3, predictions3):
    rules3 = collections.defaultdict(int)
    # change x to y if next tag is z
    assert len(training_sents3) == len(predictions3), "Gold and system don't have the same number of sentence"
    for sent_i in range(len(training_sents3)):  # for sentence in sentences:
        assert len(training_sents3[sent_i]) == len(predictions3[sent_i]), "Different number of token in sentence:\n%s" % training_sents[sent_i]
        firstToken3 = 0
        for gold_tok3, system_tok3 in zip(training_sents3[sent_i], predictions3[sent_i]): # for token in sentence
            if (firstToken3 == 1):
                firstToken3 = 0
                presentTaginSentence = system_tok3.tag
                templist = (presentTaginSentence, system_tag, gold_tag) #[z,x,y]
                rules3[templist]+=1
            if (gold_tok3.tag != system_tok3.tag):
                system_tag = system_tok3.tag
                gold_tag = gold_tok3.tag
                firstToken3 = 1
    return rules3

def filter_rule3(rules3, training_sents3, predictions3,accuracy3):
        filtered_rules3 = []
        loop=0
        for templist in rules3.keys():
                if(rules3[templist]>100):
                        predictions13 = copy.deepcopy(predictions3)
                        eachrule = []
                        eachrule.append(templist)
                        new_Predictions3 = correct_rule3(predictions13,eachrule)
                        accuracy1 = utils.calc_accuracy(training_sents3,new_Predictions3)
                        loop+=1
                        print "%s" % loop
                        if(accuracy1 > accuracy3):
                                filtered_rules3.append(templist)
        return filtered_rules3

def correct_rule3(predictions3, rules3):
        for rule3 in rules3:
                nextTag = rule3[0]
                fromTag = rule3[1]
                toTag = rule3[2]
                for sentence3 in predictions3:
                        for token3, futureToken in zip(sentence3[0::1],sentence3[1::1]):
                                if (token3.tag == fromTag):
                                        if (nextTag == futureToken.tag):
                                                token3.tag = toTag
        return predictions3


if __name__ == "__main__":
    usage = "usage: %prog [options] GOLD TEST"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug", action="store_true",
                      help="turn on debug mode")

    (options, args) = parser.parse_args()
    if len(args) != 0:
        parser.error("Please provide required arguments")

    if options.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.CRITICAL)

    training_file = "C:\Users\mangw\Downloads\New folder\homework2\hw3_train"
    
    #training phase
    training_sents = utils.read_tokens(training_file)
    model = create_model(training_sents)
	

    ## read sentences again because predict_tags(...) rewrites the tags
    
    sents = utils.read_tokens(training_file)
    predictions = predict_tags(sents, model)
    accuracy = utils.calc_accuracy(training_sents, predictions)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)
    print"entering create rules function"

    
    #-------------------------------------------------------------
    #rule 1
    print 'rule 1 processing'
    rules = rule1(predictions,training_sents);
    print len(rules)
    rules_new =filter_rule1(rules,training_sents,predictions,accuracy)
    predictions_new =  correctrules(predictions,rules_new)
    accuracy_new = utils.calc_accuracy(training_sents, predictions_new)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy_new)

    
    #----------------------------------------------------------------
    # rule 2
    print 'rule2 processing'
    rules = create_rule2(training_sents,predictions_new);
    print len(rules)
    rules_new2 = filter_rule2(rules, training_sents, predictions_new,accuracy_new)
            
    predictions_new2 = correct_rule2(predictions_new,rules_new2);
    accuracy_new2 = utils.calc_accuracy(training_sents, predictions_new2)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy_new2)

    
    #------------------------------------------------------------
    #rule3
    print 'rule3 processing'
    rules =create_rule3(training_sents,predictions_new2)
    print len(rules)
    rules_new3 = filter_rule3(rules,training_sents,predictions_new2,accuracy_new2)
    predictions_new3 = correct_rule3(predictions_new2,rules_new3)
    accuracy_new3 = utils.calc_accuracy(training_sents, predictions_new3)
    print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy_new3)


    #=================================================================================
    #testing phase
    print 'testing phase'

    test_file = "C:\Users\mangw\Downloads\New folder\postagger nlp\hw3_heldout"
    testing_sents = utils.read_tokens(test_file)
    test_model = create_model(testing_sents)
    sents_test = utils.read_tokens(test_file)
    test_predictions = predict_tags(sents_test,test_model)
	

    ## read sentences again because predict_tags(...) rewrites the tags
    #test_sents = utils.read_tokens(test_file)
    #test_predictions = predict_tags(testing_sents, model)
    accuracy = utils.calc_accuracy(testing_sents, test_predictions)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy)
    print"entering create rules function"

    
    #-------------------------------------------------------------
    #rule 1
    print 'rule 1 processing'
    #rules = rule1(predictions,testing_sents);
    #print len(rules)
    #rules_new =filter_rule1(rules,testing_sents,predictions,accuracy)
    predictions_new =  correctrules(test_predictions,rules_new)
    accuracy_new = utils.calc_accuracy(testing_sents, predictions_new)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy_new)

    
    #----------------------------------------------------------------
    # rule 2
    print 'rule2 processing'
    #rules = create_rule2(testing_sents,predictions_new);
     #print len(rules)
    #rules_new2 = filter_rule2(rules, testing_sents, predictions_new,accuracy_new)
            
    predictions_new2 = correct_rule2(predictions_new,rules_new2);
    accuracy_new2 = utils.calc_accuracy(testing_sents, predictions_new2)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy_new2)

    
    #------------------------------------------------------------
    #rule3
    print 'rule3 processing'
    #rules =create_rule3(testing_sents,predictions_new2)
    #print len(rules)
    #rules_new3 = filter_rule3(rules,testing_sents,predictions_new2,accuracy_new2)
    predictions_new3 = correct_rule3(predictions_new2,rules_new3)
    accuracy_new3 = utils.calc_accuracy(testing_sents, predictions_new3)
    print "Accuracy in testing [%s sentences]: %s" % (len(testing_sents), accuracy_new3)
    

    ## read sentences again because predict_tags(...) rewrites the tags
    #sents = utils.read_tokens(test_file)
    #predictions = predict_tags(sents, model)
    #accuracy = utils.calc_accuracy(test_sents, predictions)
    #print "Accuracy in training [%s sentences]: %s" % (len(sents), accuracy)
