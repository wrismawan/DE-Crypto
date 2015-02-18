import math
import random
import numpy as np
import collections as col
from pyngram import calc_ngram


chipperText = 'rtBiihnstilieglneeacecgynCQGhHsoadtyaaulcendhnpapaalcelCydprotthytsaaimdiaetatceighsncnedorsacyolhaoehgicdelnrntahditeercearhaosubcytprortaghWphyliiteaasivallebreflefryaoynneoihwatAdnrnitoadltbtedwonoodlnaAdornipohdnsooeiSrdOvceeispspureodtthaetoemnmbtttuashsthdcueeflodnxrteeryCaytropiryeslyaalmdiaeKytSeaetsguetndsnttieKhGUoirnwfogmrpoajrcdeetinsegfrdCoethelhmnSaincceFsetevlitaephpaeslutesslranearotbbuscaeicynprinttocneihusqaedhnetriishoytarwlsleseatligtynuaovhareacktccaetriagonuyonrewcdneomsdsegsaGeHaCpQBiptrssiphaeyngyCcHGluQnahscceytroprpghaapyfprtousetdsnauNrtlyatledheiitahsthaeteessmaessgrtahenheasevridteauhulscaanhensnldaeirpcetisnaucsnteeahpopttynrdaeidpcethhrhdedineesmaesRggredaeslosweftheohrrotnhtsuedtnseptcuipkseacpfciiitrneetnsciytroprpghainytselrlateyphitohnrieteprstafdoravtioermpooectiSneeTccneohoylEggnneirneginMaadhStTsMoEstuetndsftcOusoerfhietKeUcbmsoeeetvhnsiegltshteimbotewraaefrcoyortpgaoprithechicqneaunscbdeyscrueiyrstilkslhntteashntbdotaighenteirhrklqf'
#print 'len chip ',len(chipperText)

D = 5 #panjang kunci
batas_bawah = 10*D
batas_atas = 15*D
#bound = 50
crossover_rate = .7
PM = .7
chipperText = chipperText.replace(" ","")
F = D/3
cr = D/2
#F = 1
f0 = .0
f1 = .6
f2 = .4
b1 = 256
t2 = 17576
m3 = 26
gene = 100

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

def _get_english_monogram():
    with open('english_monogram.txt') as f:
        _file = f.read().splitlines()
        
    monogram = {}
        
    for row in _file:
        row = row.split()
        key = str(row[0].lower())
        monogram[key] = round(float(row[1]) / 4374127904, 7)
        # print key,' - ',row[1],' - ',monogram[key]
        
    return monogram


bigram_list = _get_english_bigram()
trigram_list = _get_english_trigram()
monogram_list = _get_english_monogram()

def get_decryptText(pop, chipperText):
	DecText = [[0 for i in range(len(chipperText))] for j in range(len(pop))] 
	for i in range(len(pop)): 
		for j in range(len(chipperText)): 
			idx = (j / D) * D + pop[i][j % D] 
			
			DecText[i][idx] = chipperText[j] #wiih keren
		#print '-->',''.join(DecText[i])
	return DecText

def get_decryptANS(pop,an, chipperText):
	DecANS = [0 for i in range(len(chipperText))] 
	for i in range(len(chipperText)): 
			idx = (i / D) * D + pop[an][i % D] 
			
			DecANS[idx] = chipperText[i] #wiih keren
        print '-->',''.join(DecANS)
	return DecANS

def get_n_gram(DecText,n):
	nGramProb = [0 for i in range(len(pop))]
	for i in range(len(pop)):

		decText = ''.join(DecText[i])
		# print decText

		nGramProb[i] = _calc_ngram(decText,n)
		
		#print 'DecText :',decText		
		#print 'Prob : ', nGramProb[i],'\n'	
	return nGramProb

def get_bestBig(bigramProb,n):
	bestBig = [0 for i in range(len(pop))]
	for i in range(len(pop)): 
		bestBig[i] = dict(bigramProb[i].items()[:n])
	return bestBig


def calculate_fitness(monogramProb, bigramProb, trigramProb):
	fitness = [0 for _ in range(len(pop))]

	bestBigram = get_bestBig(bigramProb,b1)
	bestTrigram = get_bestBig(trigramProb,t2)
        bestMonogram = get_bestBig(monogramProb,m3)

	#sum_bigram = 0 
        #sum_trigram = 0
	for i in range(len(pop)):
                sum_monogram = 0
                sum_bigram = 0 
                sum_trigram = 0
		for (mo, bi, tri) in zip(bestMonogram[i], bestBigram[i], bestTrigram[i]):
                        #sum_monogram = sum_monogram + monogram_list[mo] * bestMonogram[i][mo]
                        #sum_bigram = sum_bigram + bigram_list[bi] * bestBigram[i][bi]
		              	#sum_trigram = sum_trigram + trigram_list[tri] * bestTrigram[i][tri]
			
                        sum_monogram = sum_monogram + abs(monogram_list[mo] - bestMonogram[i][mo])
                        sum_bigram = sum_bigram + abs(bigram_list[bi] - bestBigram[i][bi])
                        sum_trigram = sum_trigram + abs(trigram_list[tri] - bestTrigram[i][tri])

                fitness[i] = 1/((f0 * sum_monogram) + (f1 * sum_bigram) + (f2 * sum_trigram))
                #print 'fitness individu ke - ', i, '(populasi ', pop[i], ') >>> ', fitness[i]
	return fitness

def get_r(i): #generate r1, r2, r3 buat mutasi
	r = np.random.permutation(len(pop))
	newR = [r[0],r[1],r[2]]

	while (i in newR):
		r = np.random.permutation(len(pop))
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
                r0 = int(random.uniform(0,D-F))
                rand = random.uniform(0,1)
                rin = int(random.uniform(0,len(pop)))
                #print 'rand:', rand
                
                #if (rand < PM):
                #        for j in range(0,r0):
                #                vPop[i][j] = pop[ans['index']][j]
                #        vPop[i][r0] = pop[ans['index']][r0+F-1]
                #        for k in range(r0+1,r0+F):
                #                vPop[i][k] = pop[ans['index']][k-1]
                #        for l in range(r0+F,D):
                #                vPop[i][l] = pop[ans['index']][l]
                if (rand < PM):
                        for j in range(0,r0):
                                vPop[i][j] = pop[rin][j]
                        vPop[i][r0] = pop[rin][r0+F-1]
                        for k in range(r0+1,r0+F):
                                vPop[i][k] = pop[rin][k-1]
                        for l in range(r0+F,D):
                                vPop[i][l] = pop[rin][l]
                #if (rand < PM):
                #        for j in range(0,r0):
                #                vPop[i][j] = pop[i][j]
                #        vPop[i][r0] = pop[i][r0+F-1]
                #        for k in range(r0+1,r0+F):
                #                vPop[i][k] = pop[i][k-1]
                #        for l in range(r0+F,D):
                #                vPop[i][l] = pop[i][l]
        	if (rand >= PM):
                        for m in range(D):
                                vPop[i][m] = pop[i][m]
        return vPop


def crossover(pop, mutasi_pop):
	uPop = [ [-1 for i in range(D)] for j in range (len(pop))] #init dengan -1
        rcr = [[-1 for i in range(cr)] for j in range (len(pop))]
        for i in range(len(pop)):
		r = np.random.permutation(D)
                for m in range(cr):
                        rcr[i][m] = r[m]
                
                rand = random.uniform(0,1)
                if (rand < crossover_rate):
                        for j in range(D):
                                if i not in rcr:
                                        uPop[i][j] = mutasi_pop[i][j]
                        uPop[i] = fill(uPop[i], pop[i])
                if (rand >= crossover_rate):
                        for nn in range(D):
                                uPop[i][nn] = pop[i][nn]

	return uPop        

for kk in range(0,10):
        print '========================================================'
        print '               PERCOBAAN KE- ', kk
        print '========================================================'
        
        #0 parameter
        generasi = gene

        #1 init populasi
        jumPop = int(random.uniform(batas_bawah,batas_atas))
        print 'jumPop = ', jumPop
        pop = [np.random.permutation(D) for _ in range(jumPop)]
        #print pop
        for i in range(jumPop):
                for j in range(i):
                        if ((pop[i]==pop[j]).all()):
                                pop[i] = np.random.permutation(D)
        

        # Differential Evolution
        for gen in range(generasi):

                #2 Generate Decryption Text per Individu
                DecText = get_decryptText(pop, chipperText)

                #3 Generate bigram
                bigramProb = get_n_gram(DecText,2)
                trigramProb = get_n_gram(DecText,3)
                monogramProb = get_n_gram(DecText,1)

                #4 Calculate Fitness
                pop_fitness = calculate_fitness(monogramProb, bigramProb, trigramProb)

                # print '\n\n----------populasi sebelum : '
                #for i in range(jumPop):
                #        print pop[i], ' | fitness : ',pop_fitness[i]

                #5 mutasi
                mutasi_pop = mutasi(pop, pop_fitness)
                #print 'mutasi: ', mutasi_pop
                #print 'pop:', pop

                #6 Crossover
                cross_pop = crossover(pop, mutasi_pop)
                #print 'cross: ', cross_pop
        
                #7 Generate Decryption Text dari populasi hasil crossover
                mut_DecText = get_decryptText(mutasi_pop, chipperText)
                cross_DecText = get_decryptText(cross_pop, chipperText)

                #8 Generate bigram
                mut_bigramProb = get_n_gram(mut_DecText,2) 
                mut_trigramProb = get_n_gram(mut_DecText,3)
                mut_monogramProb = get_n_gram(mut_DecText,1)
                cross_bigramProb = get_n_gram(cross_DecText,2)
                cross_trigramProb = get_n_gram(cross_DecText,3)
                cross_monogramProb = get_n_gram(cross_DecText,1)

                #9 Calculate Fitness 
                mutasi_pop_fitness = calculate_fitness(mut_monogramProb, mut_bigramProb, mut_trigramProb)
                #print 'mutasi fitness : ', mutasi_pop_fitness
        
                cross_pop_fitness = calculate_fitness(cross_monogramProb, cross_bigramProb, cross_trigramProb)
                #print 'cross fitness : ', cross_pop_fitness
        
                #seleksi
                for i in range(len(pop)):
                        if (cross_pop_fitness[i] < pop_fitness[i]):
                                ##if (cross_pop_fitness[i] > pop_fitness[i]):
                                pop[i] = cross_pop[i]
                                pop_fitness[i] = cross_pop_fitness[i]
                ans = get_best(pop_fitness)
                #	print 'generasi ke-',gen+1,' >>> ',pop[ans['index']],' | fitness : ',ans['fitness']

	
                # ans = get_best(pop_fitness)
        print gen,' >>> ',pop[ans['index']],' | fitness : ',ans['fitness']
        print 'DECRYPTED TEXT:'
        get_decryptANS(pop, ans['index'], chipperText)

