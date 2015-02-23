import math
import random
import numpy as np
import collections as col
from pyngram import calc_ngram

chipperText = 'HmoyFulmroplocyrnhictoinEpsebaFHEnerfhetaoderraohleslfoiygrrpytachCypogragiGarseryentetnsrcotniolutehptomhweroblneoliceiiteftneofnbpeoughatcitrsocacalsdiewnbaeoredaojrtmtrhkbreuhgSaohnetincuhcpemshserogseberaitnenmaeidrdhnfooectidniifiicfngenFtufemmoollyrhpiHoytprcEnosncciItnshemipsaehwliepergviewlfnieabrrdouittFonctiEofroHmtaematcainhilglisWevseowihhetmeosotrfiaojmyaniedadrlplisweeesnwreaxetsopelsmmshcEofFmseaHeillwndwetniemreiaonayfosvttayiecusmuprsownstioihcFnheemhHEshvaecsaesbbeeTehindeaddntedeinnuahtmceimtaiseattsciaerganhlveedualrobteepsdeyocailnebremlynhoeruthdowistntonsoairseceyahvslakcbeanruonygytprdingarpcoppaehyTrsimheausyostvyetlrgvihhousnaugeguhqmbpeyalhm'

#print 'len chip ',len(chipperText)

# 6 8 7 5 1 2 3 10 12 11 13 4 9
kunci = [6 ,8 ,7 ,5 ,1 ,2 ,3 ,10, 12, 11, 13, 4, 9] 
for i in range(len(kunci)):
    kunci[i] = kunci[i] - 1

D = 13 #panjang kunci
batas_bawah = 10*D
batas_atas = 15*D
#bound = 50

# crossover rate
crmin = .4
crmax = .95

PM = .7
chipperText = chipperText.replace(" ","")
F = random.uniform(0,2)
cr = D/2
#F = 1
f0 = .0
f1 = .4
f2 = .6
b1 = 256
t2 = 17576
m3 = 26
gene = 100
pop = []

def _calc_ngram(text,n):
    prob_result = {}
    results = calc_ngram(text,n)
    text_len = len(results)
    i = 0
    for x in results:
        key = str(x[0]).lower()
        prob_result[key] = x[1]/float(text_len)
        #print key,' : ', prob_result[key]
        i += 1
    return prob_result

def _get_english_bigram():
    with open('english_bigram.txt') as f:
        _file = f.read().splitlines()

    bigram = {}
    
    for row in _file:
        row = row.split()
        key = str(row[0].lower())
        bigram[key] = round(float(row[1]) / 4324127906, 7)

    return bigram

def _get_english_trigram():
    with open('english_trigram.txt') as f:
        _file = f.read().splitlines()

    trigram = {}
    
    for row in _file:
        row = row.split()
        key = str(row[0].lower())
        trigram[key] = round(float(row[1]) / 4274127909, 7)
        # print key,' - ',row[1],' - ',trigram[key]

    return trigram

bigram_list = _get_english_bigram()
trigram_list = _get_english_trigram()

def get_decryptText(pop, chipperText):
    DecText = [[0 for i in range(len(chipperText))] for j in range(len(pop))] 
    for i in range(len(pop)): 
        for j in range(len(chipperText)): 
            idx = (j / D) * D + pop[i][j % D] 
            DecText[i][idx] = chipperText[j]
    # print '-->',''.join(DecText[i])
    return DecText

def get_decryptText_kunci(pop, chipperText):
    DecText = [0 for _ in range(len(chipperText))]
    for j in range(len(chipperText)): 
        idx = (j / D) * D + pop[j % D] 
        DecText[idx] = chipperText[j]
    return DecText


def get_decryptANS(pop,an, chipperText):
    DecANS = [0 for i in range(len(chipperText))] 
    for i in range(len(chipperText)): 
        idx = (i / D) * D + pop[an][i % D] 
        DecANS[idx] = chipperText[i]
    # print '-->',''.join(DecANS)
    return DecANS

def get_n_gram(DecText,n):
    nGramProb = [0 for i in range(len(pop))]
    for i in range(len(pop)):

        decText = ''.join(DecText[i])
        # print decText

        nGramProb[i] = _calc_ngram(decText,n)
    return nGramProb

def get_n_gram_key(DecText, n):
    decText = ''.join(DecText)
    ngram = _calc_ngram(decText,n)
    return ngram

def get_bestBig(bigramProb,n):
    bestBig = [0 for i in range(len(pop))]
    for i in range(len(pop)): 
        bestBig[i] = dict(bigramProb[i].items()[:n])
    return bestBig

def get_bestBig_key(bigramProb,n):
    bestBig = dict(bigramProb.items()[:n])
    return bestBig


def calculate_fitness(bigramProb, trigramProb):
    fitness = [0 for _ in range(len(pop))]

    bestBigram = get_bestBig(bigramProb,b1)
    bestTrigram = get_bestBig(trigramProb,t2)

    for i in range(len(pop)):
        sum_bigram = 0 
        sum_trigram = 0
        for (bi, tri) in zip(bestBigram[i], bestTrigram[i]):
            sum_bigram = sum_bigram + abs(bigram_list[bi] - bestBigram[i][bi])
            sum_trigram = sum_trigram + abs(trigram_list[tri] - bestTrigram[i][tri])

        fitness[i] = 1/((f1 * sum_bigram) + (f2 * sum_trigram))
        #print 'fitness individu ke - ', i, '(populasi ', pop[i], ') >>> ', fitness[i]
    return fitness

def calculate_key_fitness(bigramProb, trigramProb):
    fitness = 0
    bestBigram = get_bestBig_key(bigramProb,b1)
    bestTrigram = get_bestBig_key(trigramProb,t2)

    sum_bigram = 0 
    sum_trigram = 0
    for (bi, tri) in zip(bestBigram, bestTrigram):
        sum_bigram = sum_bigram + abs(bigram_list[bi] - bestBigram[bi])
        sum_trigram = sum_trigram + abs(trigram_list[tri] - bestTrigram[tri])
        
    return 1/((f1 * sum_bigram) + (f2 * sum_trigram))

def get_r(i): #generate r1, r2, r3 buat mutasi
    r = np.random.permutation(len(pop))
    if (r[0] == i):
        r[0] = r[3]
    if (r[1] == i):
        r[1] = r[3]
    if (r[2] == i):
        r[2] = r[3]
            
    newR = [r[0],r[1],r[2]]
    return newR


def get_best(pop_fitness):
    min_fitness = pop_fitness[0]
    min_index = 0

    for i in range(len(pop)):
        if (pop_fitness[i] < min_fitness):
            min_fitness = pop_fitness[i]
            min_index = i

    return {'index': min_index, 'fitness':min_fitness}

def fill(uPop, pop):
    tmpPop = [pop[i] for i in range(len(pop))]
    for i in range(len(uPop)):
        if uPop[i] == -1:
            for j in range(len(tmpPop)):
                if (tmpPop[j] not in uPop) and (tmpPop[j] != -1):
                    uPop[i] = tmpPop[j]
                    tmpPop[j] = -1
                    break
    return uPop



def mutasi(pop, pop_fitness):   
    vPop = [[-1 for i in range(D)] for j in range(len(pop))]
        
    ans = get_best(pop_fitness)
    for i in range(len(pop)):
        vv = [0 for ll in range(D)]
        rand = random.uniform(0,1)
        r = get_r(i)
        r1 = r[0]
        r2 = r[1]
        r3 = r[2]
        for j in range(D):
            vv[j] = pop[r1][j] + F * (pop[r2][j] - pop[r3][j])
        ii = 0
        for k in range(D):
            min = 0
            for l in range(1,D):
                if (vv[min] > vv[l]):
                    min = l
            vPop[i][min] = ii
            vv[min] = 9999
            ii = ii + 1
            #print vPop[i]
    return vPop


def crossover(pop, mutasi_pop, crossover_rate):
    uPop = [ [-1 for i in range(D)] for j in range (len(pop))] #init dengan -1
    for i in range(len(pop)):
        r = int(random.uniform(0,D))
        rand = random.uniform(0,1)
        if (rand < crossover_rate):
            for j in range(D):
                uPop[i][j] = mutasi_pop[i][j]

        if (rand >= crossover_rate):
            for nnn in range(D):
                uPop[i][nnn] = pop[i][nnn]
            for nn in range(D):
                if (nn == r):
                    uPop[i][nn] = mutasi_pop[i][nn]
                    for jj in range(D):
                        if (pop[i][jj] == mutasi_pop[i][nn]):
                            uPop[i][jj] = pop[i][nn]
            #print uPop[i]

    return uPop        

# calculate fitness
DecTextKunci = get_decryptText_kunci(kunci, chipperText)
bigramProb = get_n_gram_key(DecTextKunci,2)
trigramProb = get_n_gram_key(DecTextKunci,3)
kunci_fitness = calculate_key_fitness(bigramProb, trigramProb)

_file = open('output_data_1.txt','w')


for kk in range(0,10):
    print '========================================================'
    print '               PERCOBAAN KE- ', (kk+1)
    print '========================================================'

    

    #0 parameter
    generasi = gene

    #1 init populasi
    jumPop = int(random.uniform(batas_bawah,batas_atas))
    
    print 'Jumlah Pop = ', jumPop
    
    pop = [np.random.permutation(D) for _ in range(jumPop)]
    #print pop
    for i in range(jumPop):
        for j in range(i):
            if ((pop[i]==pop[j]).all()):
                pop[i] = np.random.permutation(D)
    

    _pass = False
    # Differential Evolution
    for gen in range(generasi):
        # print 'generasi ke-',gen
        #2 Generate Decryption Text per Individu
        DecText = get_decryptText(pop, chipperText)

        #3 Generate bigram
        bigramProb = get_n_gram(DecText,2)
        trigramProb = get_n_gram(DecText,3)

        #4 Calculate Fitness
        pop_fitness = calculate_fitness(bigramProb, trigramProb)

        # print '\n\n----------populasi sebelum : '
        #for i in range(jumPop):
        #        print pop[i], ' | fitness : ',pop_fitness[i]

        #5 mutasi
        mutasi_pop = mutasi(pop, pop_fitness)

        #6 Crossover
        cr = crmin + gen * (crmax- crmin) / gene
        cross_pop = crossover(pop, mutasi_pop, cr)

        #7 Generate Decryption Text dari populasi hasil crossover
        mut_DecText = get_decryptText(mutasi_pop, chipperText)
        cross_DecText = get_decryptText(cross_pop, chipperText)

        #8 Generate bigram
        mut_bigramProb = get_n_gram(mut_DecText,2) 
        mut_trigramProb = get_n_gram(mut_DecText,3)
        cross_bigramProb = get_n_gram(cross_DecText,2)
        cross_trigramProb = get_n_gram(cross_DecText,3)

        #9 Calculate Fitness 
        mutasi_pop_fitness = calculate_fitness(mut_bigramProb, mut_trigramProb)
        #print 'mutasi fitness : ', mutasi_pop_fitness

        cross_pop_fitness = calculate_fitness(cross_bigramProb, cross_trigramProb)
        #print 'cross fitness : ', cross_pop_fitness

        #seleksi
        for i in range(len(pop)):
                if (cross_pop_fitness[i] < pop_fitness[i]):
                    ##if (cross_pop_fitness[i] > pop_fitness[i]):
                    pop[i] = cross_pop[i]
                    pop_fitness[i] = cross_pop_fitness[i]
        ans = get_best(pop_fitness)

        if ((ans <= kunci_fitness) and (not _pass)):
            _pass = True
            print 'PASS at gen : ',gen
            #print 'generasi ke-',gen+1,' >>> ',pop[ans['index']],' | fitness : ',ans['fitness']


    # ans = get_best(pop_fitness)
    print gen,' >>> ',pop[ans['index']],' | fitness : ',ans['fitness']
    
    print 'kunci : ',kunci,' | kunci fitness : ',kunci_fitness

    dectTextANS = get_decryptANS(pop, ans['index'], chipperText)
    print 'DECRYPTED TEXT : ', "".join(dectTextANS)


