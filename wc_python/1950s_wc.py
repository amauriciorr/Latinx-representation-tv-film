import re
import wordcloud
import pandas as pd
import matplotlib.pyplot as plt



with open("/Users/Antonio/Downloads/quotes.txt","r",encoding="latin-1") as f:
  x= " ".join(line.strip() for line in f)

  

x= re.sub(r'\\','',x)
# the below substitution was done after some investigation in the source text. the #-symbol appears in parts of the text
# to name characters. e.g Bandito #2. decided to eliminate these occurrences to get the full quotes 
x= re.sub(r' \(?#[0-9](\.[0-9]+)?\)?','',x)


# originally, I attempted to subset the captured quotes based on the decades in which they were published
# however, this led me to realize that some of the quotes are missing their year of publication.
# in an attempt to remedy this, I used re.findall(r'\([0-9]{4}\) ({[^#]+})?[^#}]+(?=\s#)',x) which 
# captured the quotes that were preceded by a release date. at first, this seemed promising since 
# 110755 quotes and dates were captured--this accounts for about 95% of the total 116746 quotes recorded.
# unfortunately, after some investigation in the source text, it was observed that the accompanying dates
# for TV-shows are for the year in which the show first aired and not for the year in which
# the episode that is being quoted aired. for this reason, I was only able to use movies to see popularity
# of words by decade. 


# for some reason, the below regex was not capturing movies when using findall. this was remedied enclosing the 
# whole regex expression in parenthesis so as to make it into a group, which is why in the for-loop 
# I use i[0], the 0-index of the tuple is where the quote and year are stored
mov= re.findall(r'((?<=#)[^\"\']+ \([0-9]{4}\) ({[^#]+})?[^#}]+(?= #))',x)

yrs = []
for i in mov:
  yrs.append(int(re.search(r'(?<=\()[0-9]{4}(?=\))',i[0]).group(0)))



sp=["hola", "mijo", "illegals", "mija", "pendejo[s]?", "goya", "Mexico","Mexican[s]", 
  "Puerto Rico","Puerto Rican[s]?", "wetback[s]?", "bandido[s]?", "bandito[s]?" ,"mamacita[s]?", "latino","chic(o|a)[s]?",
"amig(o|a)[s]?","caramba", "taco[s]?", "burrito[s]?", "gring(o|a)[s]?", "gracias", "adios",
"hasta", "noche", "cerveza[s]?", "grande", "vato[s]?", "loco[s]?", "loca[s]?", "vida", "espanol", "casa[s]?",
"latino[s]?", "latina[s]?", "hispanic[s]?", "buenos dias", "donde", "esta(r|mos|n|ba)", "diablo[s]?", "hombre[s]?", 
"muertos","hija", "hijo", "muy", "enchilada[s]?","beaner[s]?", "spic[s]?", "cholo[s]?",
"por favor", "mucho", "arriba", " culo", "puto", "puta[s]?", "gato[s]?",
"perro", " como", "pueblo", "lucha","maricon", "stupido", "cabron", "vamonos",
"fuego", "mierda", "madre", "callate", "habl(a|as|amos|ar|emos)", "muchacho[s]?", "muchacha[s]?",
"senorita", "pancho", "quiero", "huevo", "tequila",
"tamales", "andale", "caballero[s]?", "sombrero", "queso", "chihuahua[s]", "por que", "buenas",
"gusta", "lo siento", "feliz","feliz navidad", "buena suerte", "que", "cuando", "como","me gusta[n]?",
"yo soy", "dios", "dios mio","Cuban[s]?","cuban cigar[s]?","peso[s]?","tortilla[s]?"]

d = {"hola":[], "mijo":[], "illegals":[], "mija":[], "pendejo[s]?":[], "goya":[], "Mexico":[],"Mexican[s]":[], 
  "Puerto Rico":[],"Puerto Rican[s]?":[], "wetback[s]?":[], "bandido[s]?":[], "bandito[s]?" :[],"mamacita[s]?":[], "latino":[],"chic(o|a)[s]?":[],
"amig(o|a)[s]?":[],"caramba":[], "taco[s]?":[], "burrito[s]?":[], "gring(o|a)[s]?":[], "gracias":[], "adios":[],
"hasta":[], "noche":[], "cerveza[s]?":[], "grande":[], "vato[s]?":[], "loco[s]?":[], "loca[s]?":[], "vida":[], "espanol":[], "casa[s]?":[],
"latino[s]?":[], "latina[s]?":[], "hispanic[s]?":[], "buenos dias":[], "donde":[], "esta(r|mos|n|ba)":[], "diablo[s]?":[], "hombre[s]?":[], 
"muertos":[],"hija":[], "hijo":[], "muy":[], "enchilada[s]?":[],"beaner[s]?":[], "spic[s]?":[], "cholo[s]?":[],
 "por favor":[], "mucho":[], "arriba":[], " culo":[], "puto":[], "puta[s]?":[], "gato[s]?":[],
"perro":[], " como":[], "pueblo":[], "lucha":[],"maricon":[], "stupido":[], "cabron":[], "vamonos":[],
"fuego":[], "mierda":[], "madre":[],"callate":[], "habl(a|as|amos|ar|emos)":[], "muchacho[s]?":[], "muchacha[s]?":[],
"senorita":[], "pancho":[], "quiero":[], "huevo":[], "tequila":[],
"tamales":[], "andale":[], "caballero[s]?":[], "sombrero":[], "queso":[], "chihuahua[s]":[], "por que":[], "buenas":[],
"gusta":[], "lo siento":[], "feliz":[],"feliz navidad":[], "buena suerte":[], "que":[], "cuando":[], "como":[],"me gusta[n]?":[],
"yo soy":[], "dios":[], "dios mio":[],"Cuban[s]?":[],"cuban cigar[s]?":[],"peso[s]?":[],"tortilla[s]?":[]}





for i in mov:
  for j in sp:
    d[j].append(len(re.findall('[!?.\[\]\s\'\"]'+j+'[!?.\[\]\s\'\",]?',i[0],flags=re.IGNORECASE)))

total={}
for i in sp:
  total[i]=sum(d[i])




df = pd.DataFrame(d)
df['years']=yrs
fifties = df[(df.years>=1950) & (df.years<1960)]


tm50 = {}
for i in sp:
  if sum(fifties[i])>0:
    tm50[i]=int(sum(fifties[i]))



cloud = wordcloud.WordCloud(background_color="white",width=800, height=400, random_state=23)
plt.imshow(cloud.generate_from_frequencies(tm50), interpolation='bilinear')
plt.axis("off")
plt.show()

