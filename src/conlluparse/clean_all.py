import setting_conllu

# Change values in the UPOS column  
def change_upos(lines):
    new_lines = []
    replacements = {
        '\tPROPN\t': '\tPROPER_NOUN\t', '\tNOUN\t': '\tCOMMON_NOUN\t', '\tAUX\t': '\tVERB_AUX\t', '\tSYM\t': '\tSYMBOL\t',
        '\tADP\t': '\tPREP\t', '\tDET\t': '\tART\t', '\tCCONJ\t': '\tCONJ\t', '\tINTJ\t': '\tINT\t',
        '\tSCONJ\t': '\tADV\t', '\tX\t': '\tOTHER\t', '\tPART\t': '\t???\t', #Note that the PART column weren't used in the final data
    }
    pattern = re.compile("|".join(replacements.keys()))

    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = pattern.sub(lambda m: replacements[m.group(0)], line)
            new_lines.append(new_line)
    return new_lines

# Change values in the FEAT column 
def change_feats(lines):
    new_lines = []
    replacements = {
        'Gender=Masc,Neut': 'MALE', 'Gender=Fem': 'FEMALE', 'Gender=Masc': 'MALE', 'Gender=Neut': '_',  
        'Number=Sing': 'SINGULAR', 'Number=Plur': 'PLURAL', 
        'NumForm=Digit': '_', 'NumForm=Roman': '_', 'NumForm=Combi': '_', 'NumForm=Word': '_',        
        'NumType=Card': '_', 'NumType=Ord': '_', 'NumType=Frac': '_', 'NumType=Sets': '_',       
        'Tense=Pres': 'PRESENT', 'Tense=Past': 'PAST', 'Tense=Fut': 'FUTURE', 'Tense=Imp': 'IMPERFECT',
        'VerbForm=Inf': 'INFINITE', 'VerbForm=Part': 'PARTICIPLE', 'VerbForm=Fin': '_', 'VerbType=Mod': '_',
        'VerbForm=Conv': '_', 'VerbForm=Ger': 'GERUND',          

        'Person=3': 'P3', 'Person=2': 'P2', 'Person=1': 'P1', 'PronType=Exc': '_',
        'PronType=Ind,Neg,Tot': '', 'PronType=Int,Rel': '_', 'PronType=Rcp': '_', 'PronType=Emp': '_',
        'PronType=Art': '_', 'PronType=Int': '_', 'PronType=Ind': '_', 'PronType=Dem': '_',  
        'PronType=Tot': '_', 'PronType=Rel': '_', 'PronType=Prs': '_', 'PronType=Neg': '_', 
    
        'Mood=Ind': 'INDICATIVE', 'Mood=Sub': 'SUBJUNTIVE', 'Mood=Imp': 'IMPERATIVE', 'Mood=Cnd': 'CONDITIONAL',
        'Definite=Def': 'DET', 'Definite=Ind': 'UNDET', 'Polarity=Neg': 'NEG',     
        'AdpType=Prep': '_', 'AdpType=Circ': '_', 'AdpType=Post': '_', 'AdpType=Prep': '_',

        'Case=Acc,Dat': '_', 'Case=Acc,Nom': '_', 'Case=Par': '_', 'Case=Voc': '_',    
        'Case=Nom': '_', 'Case=Acc': '_', 'Case=Dat': '_', 'Case=Gen': '_', 'Case=Com': '_',
        'Case=Ins': '_', 'Case=Loc': '_', 'ConjType=Comp': '_', 'Hyph=Yes': '_',    

        'Degree=Pos': '_', 'Degree=Cmp': '_', 'Degree=Sup': '_', 'Degree=Abs': '_',                
        'Voice=Pass': '_', 'Voice=Act': '_', 'Voice=Mid': '_', 'Foreign=Yes': '_', 'Variant=Short': '_',
        'Typo=Yes': '_', 'Poss=Yes': '_',  'Reflex=Yes': '_', 'Aspect=Perf': '_', 'Aspect=Imp': 'IMPERFECT',
        'PunctType=Peri': '_', 'PunctType=Brck': '_', 'PunctType=Comm': '_', 'PunctSide=Ini': '_',
        'PunctType=Colo': '_', 'PunctType=Dash': '_', 'PunctType=Excl': '_', 'PunctSide=Fin': '_', 
        'PunctType=Qest': '_', 'PunctType=Quot': '_', 'PunctType=Semi': '_', 
        'PartType=Inf': '_', 'PartType=Res': '_', 'PartType=Vbp': '_', 'Animacy=Anim': '_', 'Animacy=Inan': '_',
        'PrepCase=Npr': '_', 'PrepCase=Pre': '_', 'AdvType=Tim': '_', 'Polite=Form': '_', 
        'NameType=Com': '_', 'NameType=Geo': '_', 'NameType=Giv': '_', 'NameType=Oth': '_', 'NameType=Patrn': '_', 
        'NameType=Prs': '_', 'NameType=Sur': '_', 'NameType=Zoo': '_', 'NameType=Pro': '_',  
    }
    pattern = re.compile("|".join(replacements.keys()))

    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = pattern.sub(lambda m: replacements[m.group(0)], line)
            new_lines.append(new_line)
    return new_lines  

def check_abbr(lines):
    new_lines = []
    for line in lines:
      if line.startswith('#'):
        new_lines.append(line)
      else:
        new_line = line.split("\t")
        if len(new_line) >= 9:
          if re.search(r"Abbr=Yes", new_line[5]):
            new_line[5] = re.sub(r"Abbr=Yes","_",new_line[5])
            new_line[3] = "ABBR"
        new_lines.append("\t".join(new_line))
    return new_lines      
 
def del_gaps(lines):
    new_lines = []
    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = line.split('\t')
            if len(new_line) >= 6:
              new_line[5] = re.sub(r'^_:', '', new_line[5])
              new_line[5] = re.sub(r':_$', '', new_line[5])
              new_line[5] = re.sub(r'^:', '', new_line[5])
              new_line[5] = re.sub(r':$', '', new_line[5])
            new_lines.append('\t'.join(new_line))
    return new_lines

# If in the 3d column the value is VERB or VERB_AUX, then in the 5th column change the order of the values in the following way:
def swap_values4verb(lines):
    new_lines = []
    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = line.split('\t')
            if len(new_line) >= 9:
                if new_line[3] == 'VERB' or new_line[3] == 'VERB_AUX':
                    # Swap SINGULAR and PRESENT  
                    if 'SINGULAR' in new_line[5] and 'PRESENT' in new_line[5]:
                        if new_line[5].index('SINGULAR') < new_line[5].index('PRESENT'):
                            new_line[5] = re.sub(r'SINGULAR', 'SINGULAR|', new_line[5])
                            new_line[5] = re.sub(r'PRESENT', 'SINGULAR', new_line[5])
                            new_line[5] = re.sub(r'SINGULAR\|', 'PRESENT', new_line[5])
                    # Swap PLURAL and PRESENT         
                    if 'PLURAL' in new_line[5] and 'PRESENT' in new_line[5]:
                        if new_line[5].index('PLURAL') < new_line[5].index('PRESENT'):
                            new_line[5] = re.sub(r'PLURAL', 'PLURAL|', new_line[5])
                            new_line[5] = re.sub(r'PRESENT', 'PLURAL', new_line[5])
                            new_line[5] = re.sub(r'PLURAL\|', 'PRESENT', new_line[5])
                    # Swap SINGULAR and PAST
                    if 'SINGULAR' in new_line[5] and 'PAST' in new_line[5]:
                        if new_line[5].index('SINGULAR') < new_line[5].index('PAST'):
                            new_line[5] = re.sub(r'SINGULAR', 'SINGULAR|', new_line[5])
                            new_line[5] = re.sub(r'PAST', 'SINGULAR', new_line[5])
                            new_line[5] = re.sub(r'SINGULAR\|', 'PAST', new_line[5])
                    # Swap PLURAL and PAST
                    if 'PLURAL' in new_line[5] and 'PAST' in new_line[5]:
                        if new_line[5].index('PLURAL') < new_line[5].index('PAST'):
                            new_line[5] = re.sub(r'PLURAL', 'PLURAL|', new_line[5])
                            new_line[5] = re.sub(r'PAST', 'PLURAL', new_line[5])
                            new_line[5] = re.sub(r'PLURAL\|', 'PAST', new_line[5])
                    # Swap SINGULAR and FUTURE     
                    if 'SINGULAR' in new_line[5] and 'FUTURE' in new_line[5]:
                        if new_line[5].index('SINGULAR') < new_line[5].index('FUTURE'):
                            new_line[5] = re.sub(r'SINGULAR', 'SINGULAR|', new_line[5])
                            new_line[5] = re.sub(r'FUTURE', 'SINGULAR', new_line[5])
                            new_line[5] = re.sub(r'SINGULAR\|', 'FUTURE', new_line[5])
                    # Swap PLURAL and FUTURE
                    if 'PLURAL' in new_line[5] and 'FUTURE' in new_line[5]:
                        if new_line[5].index('PLURAL') < new_line[5].index('FUTURE'):
                            new_line[5] = re.sub(r'PLURAL', 'PLURAL|', new_line[5])
                            new_line[5] = re.sub(r'FUTURE', 'PLURAL', new_line[5])
                            new_line[5] = re.sub(r'PLURAL\|', 'FUTURE', new_line[5])  
                    # Swap SINGULAR and IMPERFECT 
                    if 'SINGULAR' in new_line[5] and 'IMPERFECT' in new_line[5]:
                        if new_line[5].index('SINGULAR') < new_line[5].index('IMPERFECT'):
                            new_line[5] = re.sub(r'SINGULAR', 'SINGULAR|', new_line[5])
                            new_line[5] = re.sub(r'IMPERFECT', 'SINGULAR', new_line[5])
                            new_line[5] = re.sub(r'SINGULAR\|', 'IMPERFECT', new_line[5])
                    # Swap PLURAL and IMPERFECT         
                    if 'PLURAL' in new_line[5] and 'IMPERFECT' in new_line[5]:
                        if new_line[5].index('PLURAL') < new_line[5].index('IMPERFECT'):
                            new_line[5] = re.sub(r'PLURAL', 'PLURAL|', new_line[5])
                            new_line[5] = re.sub(r'IMPERFECT', 'PLURAL', new_line[5])
                            new_line[5] = re.sub(r'PLURAL\|', 'IMPERFECT', new_line[5])
                    # Swap INDICATIVE and IMPERFECT
                    if 'IMPERFECT' in new_line[5] and 'INDICATIVE' in new_line[5]:
                        if new_line[5].index('IMPERFECT') < new_line[5].index('INDICATIVE'):
                            new_line[5] = re.sub(r'IMPERFECT', 'IMPERFECT|', new_line[5])
                            new_line[5] = re.sub(r'INDICATIVE', 'IMPERFECT', new_line[5])
                            new_line[5] = re.sub(r'IMPERFECT\|', 'INDICATIVE', new_line[5])                                                                                
            new_lines.append('\t'.join(new_line))
    return new_lines

# If in the 3d column the value is VERB or VERB_AUX, then in the 5th column change the position of the value PARTICIPLE to the beginning of the string
    # (before the first colon) and delete the second PARTICIPLE value. 
def change_pos4participle(lines):
    new_lines = []
    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = line.split('\t')
            if len(new_line) >= 9:
                if new_line[3] == 'VERB' or new_line[3] == 'VERB_AUX':
                    if 'PARTICIPLE' in new_line[5]:
                        if new_line[5].index('PARTICIPLE') > 0:
                            new_line[5] = re.sub(r'PARTICIPLE:', '', new_line[5])
                            new_line[5] = re.sub(r'PARTICIPLE', '', new_line[5])
                            new_line[5] = 'PARTICIPLE:' + new_line[5]
            new_lines.append('\t'.join(new_line))
    return new_lines

# If the line is a multi-word token, then the next two lines are skipped and ther values are added to the multi-word token.
def check_multitoken(lines):
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        new_line = line.split('\t')
        if new_line[0].startswith("#"):
            new_lines.append(line)
        elif re.search(r'([0-9])-([0-9])', new_line[0]):
            if new_line[5] == "_":
                for j in range(1,3):
                    if i+j < len(lines):
                        next_line = lines[i+j].split('\t')
                        if next_line[3] == "ART" and next_line[5] != "_":
                            new_line[5] = next_line[5]
                            break
            new_line[3] = re.sub(r'^_', '_PREP', new_line[3])
            if new_line[5].startswith("DET") or new_line[5].startswith("UNDET"):
                new_line[5] = new_line[5].replace("DET","ART").replace("UNDET","ART")
            new_lines.append('\t'.join(new_line))
        else:
            new_lines.append(line)
        i += 1
    return new_lines

def del_multitoken(lines):
    new_lines = []
    skip_lines = 0
    for line in lines:
        if line.startswith("#"):
            new_lines.append(line)
        elif re.search(r'([0-9])-([0-9])', line.split('\t')[0]):
            new_lines.append(line)
            skip_lines = 2
        elif skip_lines > 0:
            skip_lines -= 1
        else:
            new_lines.append(line)
    return new_lines

# OPTIONAL
# Since in my task I couldn't ise PART as POS for the participle, I changed it case by case
# GERMAN DATASET
def check_part_de(lines):
    new_lines = []
    for line in lines:
        if line.startswith("#"):
            new_lines.append(line)
            continue
        new_line = line.split("\t")
        if len(new_line) < 9:
            new_lines.append("\t".join(new_line))
            continue
        if new_line[3] == "???":
            #ja ecc. -> ADV
            if new_line[2] in ["ja", "Ja", "statt", "preis", "vor", "hin", "dar", "ab", "an", "wie", "Bitte", "aus", "wohl"]:
                new_line[3] = "ADV"
            # nein -> ADV + NEG
            elif new_line[2] in ["nein", "ncht", "Nein"]:
                new_line[3] = "ADV"
                new_line[5] = "NEG"
            # nicht -> ADV
            elif new_line[5] == "NEG":
                new_line[3] = "ADV"
            # zu ecc. -> PREP
            elif new_line[2] in ["zu", "Zu", "auf", "als"]:
                new_line[3] = "PREP"  
            # wehen ecc. -> Verb 
            elif new_line[2] in ["wehen", "einnehmen", "auflaufen"]:
                new_line[3] = "VERB"
            # ADV
            if new_line[4] in ["ADV"]:
                new_line[3] = "ADV"
            # INT
            if new_line[4] in ["ITJ"]:
                new_line[3] = "INT"
            # INT
            if new_line[2] in ["danke"]:
                new_line[3] = "INT"                           
        new_lines.append("\t".join(new_line))
    return new_lines    

# SPANISH DATASET, same optional
def check_part_es(lines):
    new_lines = []
    for line in lines:
        if line.startswith("#"):
            new_lines.append(line)
            continue
        new_line = line.split("\t")
        if len(new_line) < 9:
            new_lines.append("\t".join(new_line))
            continue
        if new_line[3] == "???":
            # no -> ADV + NEG
            if new_line[2] in ["no", "No"]:
                new_line[3] = "ADV"
                new_line[5] = "NEG"
            # NeG -> ADV
            elif new_line[5] == "NEG":
                new_line[3] = "ADV"
            # Adj
            elif new_line[2] in ["ruso", ]:
                new_line[3] = "ADJ"
            # Adj
            elif new_line[2] in ["ex", "hoc", "to", "re", "pre", "sub", "co", "semi", "gram", "ser", "super", "trans"]:
                new_line[3] = "OTHER"
            # PROPER_NOUN
            elif new_line[2] in ["vice"]:
                new_line[3] = "PROPER_NOUN"
            # COMMON_NOUN
            elif new_line[2] in ["ficha", "adio"]:
                new_line[3] = "COMMON_NOUN" 
            # Verb
            elif new_line[2] in ["abandono", "ir"]:
                new_line[3] = "VERB"                                            
            # Pron
            elif new_line[2] in ["que"]:
                new_line[3] = "PRON"                
            # INT
            elif new_line[2] in ["hola"]:
                new_line[3] = "INT" 
            # compound -> OTHER
            elif new_line[7] in ["compound"]:
                new_line[3] = "OTHER"                           
        new_lines.append("\t".join(new_line))
    return new_lines

# RUSSIAN DATASET, same optional
def check_part_ru(lines):
    new_lines = []
    for line in lines:
        if line.startswith("#"):
            new_lines.append(line)
            continue
        new_line = line.split("\t")
        if len(new_line) < 9:
            new_lines.append("\t".join(new_line))
            continue
        if new_line[3] == "???":
            # no -> ADV + NEG
            if new_line[2] in ["не", "Не", "Нет", "нет"]:
                new_line[3] = "ADV"
                new_line[5] = "NEG"
            # NeG -> ADV
            elif new_line[5] == "NEG":
                new_line[3] = "ADV"
            # Adj
            elif new_line[1] in ["де", "Де", "ди", "Ди", "д", "Д", "ле", "Ле",
                                 "фон", "Фон", "Ван", "ван", "Дер", "аль", "деи",
                                 "ла", "Ла", "дер", "ибн", "Ибн", "ал", "О", "o", "Эль"]:
                new_line[3] = "PROPER_NOUN"
            # Adj
            elif new_line[2] in ["су", "ида", "хай"]:
                new_line[3] = "OTHER"
            # PROPER_NOUN
            elif new_line[2] in ["и", "будто", "ведь", "ж", "да", "хоть", "хотя", 
                                 "пусть", "всё-таки", "все-таки", "словно", "же",
                                 "что", "аж", "как", "якобы", "таки-таки", "жеш",
                                 "зато", "че"]:
                new_line[3] = "CONJ"
            # Verb_Aux
            elif new_line[2] in ["бы", "было"]:
                new_line[3] = "VERB_AUX"                                            
            # Pron
            elif new_line[2] in ["это", "всеж", "всего", "все", "всё", "всеже", 
                                 "что-то", "чето", "нибудь", "этот"]:
                new_line[3] = "PRON"
            # COMMON_NOUN
            elif new_line[2] in ["спасибо", "пожалуйста", "типа", "типо", "норм", "тип",
                                 "что-ли", "ти-по"]:
                new_line[3] = "COMMON_NOUN" 
            # COMMON_NOUN
            elif new_line[2] in ["конечно", "супер"]:
                new_line[3] = "ADJ"
            # COMMON_NOUN
            elif new_line[2] in ["пускай", "дай", "давайте", "мож"]:
                new_line[3] = "VERB"                                                 
            # INT
            elif new_line[2] in ["ну", "мол", "то", "але", "ага", "те", "ль",
                                 "поди", "во", "а", "здрасте"]:
                new_line[3] = "INT"                               
            # ADV
            elif new_line[2] in ["тоже", "даже", "также", "только", "лишь", "ли", "именно", 
                                 "вот", "вон", "просто", "уж", "точно", "таки", "разве", 
                                 "хорошо", "неужели", "ужели", "неужель", "ладно", "так", 
                                 "прямо", "токмо", "ужель", "только-только", "прям", "там",
                                 "еле", "тока", "таже", "ток", "-таки", "нето", "прост",
                                 "прямо-таки"]:
                new_line[3] = "ADV" 
            # OTHER
            elif new_line[2] in ["на", "с"]:
                new_line[3] = "PREP"                           
        new_lines.append("\t".join(new_line))
    return new_lines

#THIS ONE IS ALSO FOR RUSSIAN DATASET
def check_extra_ru(lines):
    new_lines = []
    for line in lines:
        if line.startswith("#"):
            new_lines.append(line)
            continue
        new_line = line.split("\t")
        if len(new_line) < 9:
            new_lines.append("\t".join(new_line))
            continue
        if new_line[3] == "OTHER":
            if new_line[2] in ["и", "И"]:
                new_line[3] = "CONJ"
            # Verb_Aux
            elif new_line[1] in ["бы"]:
                new_line[3] = "VERB_AUX"
        if new_line[3] != "NUM":
            if re.match(r'^[0-9]+$', new_line[1]):
                new_line[3] = "NUM"
            else:
                new_line[3] = new_line[3]                                                                            
        new_lines.append("\t".join(new_line))
    return new_lines

# OPTIONAL: It could be better to check all of them in the end but I felt safer to check them after each change
# If after all interaction the gaps appear, recheck them and delete them
# The string in the column 3 shouldn't start or finish with a colon (:) or an underscore (_)
def del_gaps2(lines):
    new_lines = []
    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = line.split('\t')
            if len(new_line) >= 6:
              new_line[5] = re.sub(r'^_:', '', new_line[5])
              new_line[5] = re.sub(r'^_:_:', '', new_line[5])
              new_line[5] = re.sub(r':_$', '', new_line[5])
              new_line[5] = re.sub(r':_:_$', '', new_line[5])
              new_line[5] = re.sub(r':_:', ':', new_line[5])
              new_line[5] = re.sub(r':_:_:', ':', new_line[5])

              new_line[3] = re.sub(r'^_PREP', 'PREP', new_line[3])
              new_line[5] = re.sub(r'^_ART', 'ART', new_line[5])  
                          
              new_line[5] = re.sub(r'^:', '', new_line[5])
              new_line[5] = re.sub(r':$', '', new_line[5])             
            new_lines.append('\t'.join(new_line))
    return new_lines

# OPTIONAL: In some datasets some weird values appear in FEAT that doesn't work to clean up until this point  
def change_feats2(lines):
    new_lines = []
    replacements = {
        'Number\[psor\]=Sing': '', 'Number\[psor\]=Plur': '',
        'Number\[psor\]=Sing:': '', 'Number\[psor\]=Plur:': '',        
        ':Number\[psor\]=Sing': '', ':Number\[psor\]=Plur': '',

        'Person\[psor\]=1': '', 'Person\[psor\]=2': '', 'Person\[psor\]=3': '',
        'Person\[psor\]=1:': '', 'Person\[psor\]=2:': '', 'Person\[psor\]=3:': '',
        ':Person\[psor\]=1': '', ':Person\[psor\]=2': '', ':Person\[psor\]=3': '',     

        'Gender\[psor\]=Masc,Neut': '',
        'Gender\[psor\]=Neut': '', 'Gender\[psor\]=Masc': '', 'Gender\[psor\]=Fem': '',
    }
    pattern = re.compile("|".join(replacements.keys()))

    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = pattern.sub(lambda m: '', line)
            new_lines.append(new_line)
    return new_lines

# OPTIONAL:
def del_gaps3(lines):
    new_lines = []
    for line in lines:
        if line.startswith('#'):
            new_lines.append(line)
        else:
            new_line = line.split('\t')
            if len(new_line) >= 6:
              new_line[5] = re.sub(r'^_:', '', new_line[5])
              new_line[5] = re.sub(r'^_:_:', '', new_line[5])
              new_line[5] = re.sub(r':_$', '', new_line[5])
              new_line[5] = re.sub(r':_:_$', '', new_line[5])
              new_line[5] = re.sub(r':_:', ':', new_line[5])
              new_line[5] = re.sub(r':_:_:', ':', new_line[5])
              new_line[5] = re.sub(r'::', ':', new_line[5])
              new_line[5] = re.sub(r'^:', '', new_line[5])
              new_line[5] = re.sub(r':$', '', new_line[5])
            new_lines.append('\t'.join(new_line))
    return new_lines

def access_data(input_file, output_file):
    lines = setting_conllu.read_conllu(input_file)
    # processing for cleaning the data here 
    lines = change_upos(lines)
    lines = setting_conllu.change_divider(lines)
    lines = change_feats(lines)
    lines = check_abbr(lines)
    lines = del_gaps(lines)
    lines = swap_values4verb(lines)
    lines = check_multitoken(lines)
    lines = change_pos4participle(lines)
    lines = del_multitoken(lines)
    # OPTIONAL:
    lines = check_part_de(lines) # for German
    lines = check_part_es(lines) # for Spanish
    lines = check_part_ru(lines) # for Russian
    lines = check_extra_ru(lines) # for Russian
    lines = del_gaps2(lines) 
    lines = change_feats2(lines) 
    lines = del_gaps3(lines) 
    setting_conllu.write_conllu(output_file, lines)