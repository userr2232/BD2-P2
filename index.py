import json
from nltk.stem import PorterStemmer 
from nltk.tokenize import word_tokenize 
from os import listdir, remove
from os.path import isfile, join
import string
import shutil
from math import log, sqrt

class Inverted:
    stopwords = dict.fromkeys(["algún","alguna","algunas","alguno","algunos","ambos","ampleamos","ante","antes","aquel","aquellas","aquellos","aqui","arriba","atras","bajo","bastante","bien","cada","cierta","ciertas","cierto","ciertos","como","con","conseguimos","conseguir","consigo","consigue","consiguen","consigues","cual","cuando","dentro","desde","donde","dos","el","ellas","ellos","empleais","emplean","emplear","empleas","empleo","en","encima","entonces","entre","era","eramos","eran","eras","eres","es","esta","estaba","estado","estais","estamos","estan","estoy","fin","fue","fueron","fui","fuimos","gueno","ha","hace","haceis","hacemos","hacen","hacer","haces","hago","incluso","intenta","intentais","intentamos","intentan","intentar","intentas","intento","ir","la","largo","las","lo","los","mientras","mio","modo","muchos","muy","nos","nosotros","otro","para","pero","podeis","podemos","poder","podria","podriais","podriamos","podrian","podrias","por","por qué","porque","primero","puede","pueden","puedo","quien","sabe","sabeis","sabemos","saben","saber","sabes","ser","si","siendo","sin","sobre","sois","solamente","solo","somos","soy","su","sus","también","teneis","tenemos","tener","tengo","tiempo","tiene","tienen","todo","trabaja","trabajais","trabajamos","trabajan","trabajar","trabajas","trabajo","tras","tuyo","ultimo","un","una","unas","uno","unos","usa","usais","usamos","usan","usar","usas","uso","va","vais","valor","vamos","van","vaya","verdad","verdadera","verdadero","vosotras","vosotros","voy","yo","él","ésta","éstas","éste","éstos","última","últimas","último","últimos","a","añadió","aún","actualmente","adelante","además","afirmó","agregó","ahí","ahora","al","algo","alrededor","anterior","apenas","aproximadamente","aquí","así","aseguró","aunque","ayer","buen","buena","buenas","bueno","buenos","cómo","casi","cerca","cinco","comentó","conocer","consideró","considera","contra","cosas","creo","cuales","cualquier","cuanto","cuatro","cuenta","da","dado","dan","dar","de","debe","deben","debido","decir","dejó","del","demás","después","dice","dicen","dicho","dieron","diferente","diferentes","dijeron","dijo","dio","durante","e","ejemplo","ella","ello","embargo","encuentra","esa","esas","ese","eso","esos","está","están","estaban","estar","estará","estas","este","esto","estos","estuvo","ex","existe","existen","explicó","expresó","fuera","gran","grandes","había","habían","haber","habrá","hacerlo","hacia","haciendo","han","hasta","hay","haya","he","hecho","hemos","hicieron","hizo","hoy","hubo","igual","indicó","informó","junto","lado","le","les","llegó","lleva","llevar","luego","lugar","más","manera","manifestó","mayor","me","mediante","mejor","mencionó","menos","mi","misma","mismas","mismo","mismos","momento","mucha","muchas","mucho","nada","nadie","ni","ningún","ninguna","ningunas","ninguno","ningunos","no","nosotras","nuestra","nuestras","nuestro","nuestros","nueva","nuevas","nuevo","nuevos","nunca","o","ocho","otra","otras","otros","parece","parte","partir","pasada","pasado","pesar","poca","pocas","poco","pocos","podrá","podrán","podría","podrían","poner","posible","próximo","próximos","primer","primera","primeros","principalmente","propia","propias","propio","propios","pudo","pueda","pues","qué","que","quedó","queremos","quién","quienes","quiere","realizó","realizado","realizar","respecto","sí","sólo","se","señaló","sea","sean","según","segunda","segundo","seis","será","serán","sería","sido","siempre","siete","sigue","siguiente","sino","sola","solas","solos","son","tal","tampoco","tan","tanto","tenía","tendrá","tendrán","tenga","tenido","tercera","toda","todas","todavía","todos","total","trata","través","tres","tuvo","usted","varias","varios","veces","ver","vez","y","ya"])
    ps = PorterStemmer()
    def __init__(self, dir):
        self.dir = dir
        self.blocks = []
        self.file_names = [ join(dir, f) for f in listdir(dir) if isfile(join(dir, f)) ]
        self.idf = {}
        self.tf_idf = {}
        self.N = 0
        self.page_table = {}
        self.BSBIndexConstruction()
        self.compute_tf_idf()

    def ParseNextBlock(self, tweets):
        res = []
        for tweet in tweets:
            if not tweet['retweeted']:
                self.tf_idf[tweet['id']] = {}
                self.N += 1
                for word in tweet['text'].split():
                    if(word[0:4] != 'http'):
                        word = word.translate(str.maketrans(dict.fromkeys(string.punctuation)))
                        word = word.lower()
                        word = self.ps.stem(word)
                    if len(word.strip()):
                        if word not in self.stopwords:
                            res.append((word, tweet['id']))
                            if word not in self.tf_idf[tweet['id']]:
                                self.tf_idf[tweet['id']][word] = 1
                            else:
                                self.tf_idf[tweet['id']][word] += 1
                if not len(self.tf_idf[tweet['id']]):
                    self.N -= 1
                    del self.tf_idf[tweet['id']]
        return sorted(res)

    def BSBI_Invert(self, block, file_name):
        current_word = block[0][0]
        res = []
        res.append((current_word, []))
        for i, x in enumerate(block):
            word, docId = x
            self.page_table[docId] = file_name
            if word == current_word:
                res[-1][1].append(docId)
            else:
                current_word = word
                res.append((word, [docId]))
        return res

    def WriteBlockToDisk(self, block, file_name):
        with open(file_name, 'w+') as f:
            for row in block:
                f.write(' '.join(str(x) if i == 0 else ','.join(str(val) for val in x) for i, x in enumerate(row)) + '\n')

    def BSBIndexConstruction(self):
        n = 0
        for file_name in self.file_names:
            n += 1
            with open(file_name) as f:
                block = self.ParseNextBlock(json.load(f))
                block = self.BSBI_Invert(block, file_name)
                block_file_name = "blocks/block_{}".format(n)
                self.blocks.append(block_file_name)
                self.WriteBlockToDisk(block, block_file_name)
        self.MergeBlocks()

    def MergeBlocks(self, file_name = "blocks_merged"):
        blocks = self.blocks
        level = 0
        while len(blocks) > 1:
            level += 1
            next_blocks = []
            empty_file = 'blocks/empty_block'
            if len(blocks) % 2:
                with open(empty_file, 'w+'):
                    blocks.append(empty_file)
            for i in range(0, len(blocks)-1, 2):
                n_b = "blocks/{}_{}_{}".format(level,i,i+1)
                next_blocks.append(n_b)
                self.MergeTwoBlocks(blocks[i], blocks[i+1], n_b)
            blocks = next_blocks
        shutil.move(blocks[0], file_name)

    def MergeTwoBlocks(self, b1, b2, file_name):
        tb1 = open(b1, "r")
        tb2 = open(b2, "r")
        with open(file_name, 'w+') as final_file:
            list_b1 = []
            list_b2 = []
            n = 1000
            while True:
                while len(list_b1) < n:
                    line = tb1.readline()
                    if not line:
                        break
                    list_b1.append(self.to_tuple(line))
                while len(list_b2) < n:
                    line = tb2.readline()
                    if not line:
                        break
                    list_b2.append(self.to_tuple(line))

                if not list_b1 or not list_b2:
                    break
                while len(list_b1) and len(list_b2):
                    if list_b1[0][0] < list_b2[0][0]:
                        self.idf[str(list_b1[0][0])] = log(self.N / len(list_b1[0][1]), 10)
                        s = str(list_b1[0][0]) + " " + self.array_to_string(list_b1[0][1]) + "\n"
                        list_b1.pop(0)
                        final_file.write(s)
                    else:
                        if list_b1[0][0] > list_b2[0][0]:
                            self.idf[str(list_b2[0][0])] = log(self.N / len(list_b2[0][1]), 10)
                            s = str(list_b2[0][0]) + ' ' + self.array_to_string(list_b2[0][1]) + '\n'
                            list_b2.pop(0)
                            final_file.write(s)
                        else:
                            arr = list_b1[0][1]+list_b2[0][1]
                            self.idf[str(list_b1[0][0])] = log(self.N / len(arr), 10)
                            s = str(list_b1[0][0]) + ' ' + self.array_to_string(arr) + '\n'
                            final_file.write(s)
                            list_b1.pop(0)
                            list_b2.pop(0)
            # si despues de cargar todos los archivos una todavia tiene elementos

            while True:
                while len(list_b1) and len(list_b1) < n:
                    line = tb1.readline()
                    if not line:
                        break
                    list_b1.append(self.to_tuple(line))
                if not list_b1:
                    break
                while len(list_b1):
                    self.idf[str(list_b1[0][0])] = log(self.N / len(list_b1[0][1]), 10)
                    s = str(list_b1[0][0]) + " " + self.array_to_string(list_b1[0][1]) + "\n"
                    list_b1.pop(0)
                    final_file.write(s)
            
            while True:
                while len(list_b2) and len(list_b2) < n:
                    line = tb2.readline()
                    if not line:
                        break
                    list_b2.append(self.to_tuple(line))
                if not list_b2:
                    break
                while len(list_b2):
                    self.idf[str(list_b2[0][0])] = log(self.N / len(list_b2[0][1]), 10)
                    s = str(list_b2[0][0]) + " " + self.array_to_string(list_b2[0][1]) + "\n"
                    list_b2.pop(0)
                    final_file.write(s)

    def to_tuple(self, line):
        word, docs = line.split()
        s = docs.split(',')
        return (word, s)

    def array_to_string(self, arr):
        return ','.join(x for x in arr)

    def compute_tf_idf(self):
        for doc, word_dict in self.tf_idf.items():
            for word, tf in word_dict.items():
                self.tf_idf[doc][word] = tf * self.idf[word]
        self.normalize()

    def normalize(self):
        for doc, word_dict in self.tf_idf.items():
            sum = 0
            for _, tf_idf in word_dict.items():
                sum += tf_idf ** 2
            denominator = sqrt(sum)
            for word, tf_idf in word_dict.items():
                self.tf_idf[doc][word] /= denominator
        
    def cosine_similarity(self, v1, v2):
        res = 0
        for word in v1.keys():
            if word in v2:
                res += v1[word] * v2[word]
        return res

    def retrieve_results(self, ids):
        res = []
        for id in ids:
            with open(self.page_table[id]) as f:
                tweets = json.load(f)
                for tweet in tweets:
                    if tweet['id'] == id:
                        res.append(tweet)
                        break
        return res

    def query(self, text, limit):
        if limit:
            limit = int(limit)
        else:
            limit = 10
        tokens = text.strip().split()
        v = { token: 1 / sqrt(len(tokens)) for token in tokens}
        results = [ (doc, self.cosine_similarity(v, v2)) for doc, v2 in self.tf_idf.items() ]
        results = sorted(results, key=lambda x: x[1], reverse=True)[:limit]
        return self.retrieve_results([ id for id, score in results ])
