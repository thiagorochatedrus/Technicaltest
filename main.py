#regex, expressões regulares, para extrair o valor da vida do Black Knight. Poderia usar para tudo...
import re

import json #para saida JSON





f = open("ServerLog.txt", "r") #abre arquivo para leitura


#variaveis globais
hitpointsHealed  = 0
lost    = 0
percreature = {}
xp = 0
loot        = {}
damage_unknown = 0
black_knight_life = 0


for line in f: #lê linha por linha do LOG

    if "A Black Knight loses" in line:#se tem essa frase é que o BK levou um golpe; soma para descobrir a vida total.
        a = re.findall(r'\d+', line) #procura números usando uma expressão regular. 
        
        black_knight_life += int(a[2]) #retorna 3 por causa da hora no começo da linha; pega a terceira

    
    tokens = line.split(" ") #divide a string em palavras separadas por espaços

    if 'healed' in tokens and 'yourself' in tokens: #tem a palavra de cura, procura quanto curou
        hitpointsHealed += int(tokens[5])


    if 'lose' in tokens and 'You' in tokens: #danos sofridos pelo jogador
        dmg = int(tokens[3])
        lost += dmg
        if 'due' in tokens: #se tem o termo 'due' apresenta o nome dos inimigos depois

            #15:43 You lose 31 hitpoints due to an attack by a cyclops.  <- exemplo
            # vai dividir em uma lista: 
            #['15:44', 'You', 'lose', '5', 'hitpoints', 'due', 'to', 'an', 'attack', 'by', 'a', 'cyclops.', '\n']
            # a partir da posicao 11 tem o nome do bicho que pode ser só uma palavra (cyclops) ou composto como "black knight";
            #quantas palavras tem 
            end = len(tokens)-1 #tamanho da lista
            
            creature = tokens[11:end] #nome está na posicao 11 até o final             

            creature = " ".join(creature) #transforma em string novamente.

            creature = creature.replace('.','') #remove o '.' do final

            #armazena os danos por tipo de criatura no dicionario. 
            if creature in percreature:
                percreature[creature] += dmg
            else:
                percreature[creature] = dmg
        else: #conta os dados que não foram por inimigos
            damage_unknown += dmg
        
    #18:46 You gained 1600 experience points.
    #gained ... experience - ganhou pontos de experiência
    if 'gained' in tokens:
        xp += int(tokens[3])
    


    if 'Loot' in tokens: #itens deixados pelos inimigos
     
        #exemplo: 18:45 Loot of a skeleton: a bone, 2 gold coins.
        #remove o primeiro que é o horário, junta e depois divide por ':'
        ltoken = " ".join(tokens[1:len(tokens)]).split(':')
        #vira: ['Loot of a skeleton', ' a bone, 2 gold coins.\n']


        
        
        #antes foi dividido em 2; pega a parte da esquerda e divide por espaço: 
        #'Loot of a skeleton' -> ['loot', 'of', 'a', 'skeleton']
        left = ltoken[0].split(' ')


        lend = len(left)-1
        enemy = left[4:lend]
        #['loot', 'of', 'a', 'skeleton']
        enemy =  " ".join(enemy) #do 4 pra frente é o nome do inimigo [skeleton]; caso fosse nome composto (black knight) ia unir tudo
        

        
        #direita? ' a bone, 2 gold coins.\n'

        right = ltoken[1].strip().split(',') #divide por virgula, pois pode deixar mais de um item. 
        #a bone, 2 gold coins
        
        if 'nothing.' not in right: #pode ser nothing, daí não deixou item
            for r in right: #para cada contagem de item... 
                item_quantity = r.strip().split(' ') #a bone 

                if not item_quantity[0].isnumeric(): #se nao comeca com um valor numerico... (por exemplo 'a' ou 'dragon ham')
                    if item_quantity[0]=='a': # se começa com 'a'
                        del item_quantity[0] #remove ele
                    q = 1 # se nao tem o valor vai ser 1 (a bone OU "dragon ham" = 1 dragon ham)
                    name = " ".join(item_quantity[0:])#se for nome composto (dragon ham) junta tudo
                    name = name.replace('.','')#remove o ponto
                    
                    #adiciona no dicionario
                    if name in loot:
                        loot[name] += q
                    elif  (name+'s') in loot: #aparece 'gold coin' e 'gold coins', conta o plural também
                        loot[name+'s'] += q
                    else:
                        loot[name] = q
                else: #ok, tem a quantidade no começo.
                    
                    q = item_quantity[0]
                    q = int(q) #era um numero inteiro, só faz o cast
                    
                    name = " ".join(item_quantity[1:]) #nome composto?
                    name = name.replace('.','') #remove o ponto

                    #salva no dicionário
                    if name in loot:
                        loot[name] += q
                    elif  (name+'s') in loot:
                        loot[name+'s'] += q
                    else:
                        loot[name] = q

            





results = {
    'hitpointsHealed' : hitpointsHealed,
    "damageTaken" : {
        'total' : lost, 
        'byCreatureKind' : percreature
    },
    "experienceGained" : xp,
    'loot': loot
}



print(json.dumps(results))