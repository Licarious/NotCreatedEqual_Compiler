#ToDo
#Hire/Fire events   -   Done
#Notificaion everns -   Done
#Promotion everts   -   Done
#Random MTTH evernts-   Done
#Mod Support        -   Done
#Event_Modifiers    -   Done
#Localization
#   Eng             -   Done
#   Ger             -   Done
#   Fra             -   Done
#   Spa             -   Done
#
#InGame Testing     -   Looking Good
#   
import py_compile
import re
import os
import copy

try:
    py_compile.compile("NCE_Translator.py")
    os.remove("RunMe.pyc")
    os.rename("__pycache__/NCE_Translator.cpython-37.pyc","RunMe.pyc")
except:
    print("Compiler Error! Will attempt to continue.")

class Advisor:
    dataName = ""
    titleEng = ""
    titleGer = ""
    titleFra = ""
    titleSpa = ""
    modSuffix = ""
    pointType = ""
    modifierNames = ""
    modifierValues = ""

advisor_list = []
Input = open("input.csv", "r", encoding='utf-8-sig')
Config = open("config.cfg", "r", encoding='utf-8-sig')
advisor_level_data = ["terrible", "inept", "mediocre", "good", "great", "amazing"]
#If adding more events per advisor I encourage you to tack them onto the end of that range to not disrupt the math involved with events calling other events
numEventsPerAdvisor = 8


#This stuff is placeholders and will be overridden by the what is in the config file
levelMult = [-0.5,-0.3,0,0.3,0.6,1.0]
Lx0 = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
LxL = [[0,25,40,25,10,0],[0,35,45,15,5,0],[0,30,45,20,10,0]]
Lx = [[0,25,40,25,10,0],[0,20,40,25,15,0],[0,10,35,30,20,0]]
LxB = [[0,5,30,35,30,0],[0,20,35,30,15,0],[0,15,35,30,20,0]]
LxS = [[0,0,30,35,35,0],[0,10,30,40,20,0],[0,5,35,35,25,0]]
LxC1 = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
LxC2 = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
LxC3 = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
money = [162,30,96] #Money
influence = [18,12,16] #Monarch Points
manpower = [0.1667,0.0833,0.125] #in years
sailors = [2,1,1.5] #in years
corruption = [3,4,5]
inflation = [1,1.5,2]
embezzleMoney = [-10,-32,-54]
embezzleInfluence = [-6,-8,-9]
PrecentagePerOption = [2,3,3,3,4,1,1]
AIPrecentage = [20,20,20,0,0,0,0]
advProPresentage = [[50,40,10,0,0,0],[10,40,40,10,0,0],[0,10,40,40,10,0],[0,0,10,40,40,10],[0,0,0,10,60,30],[0,0,0,0,20,80]]
advMTTPresentage = [[10,90,0,0,0,0],[30,0,70,0,0,0],[0,30,0,70,0,0],[0,0,30,0,70,0],[0,0,0,30,0,70],[0,0,0,0,20,80]]
MTTHMonths = [7300]
MaxAdvisorLevel = [5]
MaxLevelBeforPromote = [3]
AIEvents = [1]


AdvisorPresentage = [Lx0,LxL,Lx,LxB,LxS,LxC1,LxC2,LxC3]

for line in Input:
    DataElement = line.split(";")
    if DataElement[0].startswith("#"):
        pass
    else:
        test = Advisor()
        test.dataName = DataElement[0]
        test.titleEng = DataElement[1]
        test.titleGer = DataElement[2]
        test.titleFra = DataElement[3]
        test.titleSpa = DataElement[4]
        test.modSuffix = DataElement[5].upper()
        test.pointType = DataElement[6]
        test.modifierName = DataElement[7]
        test.modifierValue = DataElement[8]
        advisor_list.append(test)
i=0

def English_localization(advisor_list, advisor_level_data, modTitle):
    localization = open(("localisation\\NCE_%s_l_english.yml"%modTitle), "w", encoding='utf-8-sig')
    localization.write("l_english:")
    advisor_level_Name = ["Terrible", "Inept", "Mediocre", "Good", "Great", "Amazing"]

    #General Localizations
    #localization.write("\nNCE_%s.1.t:0 \"Not all men are created equal.\""%modTitle)
    localization.write("\nNCE_%s.1.a:0 \"Do nothing.\""%modTitle)            
    localization.write("\nNCE_%s.1.b:0 \"Spare no expense.\""%modTitle)
    localization.write("\nNCE_%s.1.c:0 \"Exert our influence.\""%modTitle)
    localization.write("\nNCE_%s.1.d:0 \"Throw men at the problem.\""%modTitle)
    localization.write("\nNCE_%s.1.e:0 \"Let's push off that expense for later.\""%modTitle)

    localization.write("\nNCE_%s.1.f:0 \"...Succeed by fraud. ~Sophocles\""%modTitle)
    localization.write("\nNCE_%s.1.g:0 \"I am the King.\""%modTitle)

    localization.write("\nNCE_%s.2.t:0 \"Advisor has left your court.\""%modTitle)
    localization.write("\nNCE_%s.2.a:0 \"OK\""%modTitle)
    #localization.write("\nNCE_%s.3.t:0 \"Skill level report\"\n"%modTitle)            
    for l in range(len(advisor_level_Name)):      #Level Name Buttons
        localization.write("\nNCE_%s.3.%s:0"%(modTitle,chr(97+l)))
        localization.write(" \"%s.\""%(advisor_level_Name[l]))
    localization.write("\nNCE_%s.4.a:0 \"Advisor Lost\""%modTitle)
    localization.write("\nNCE_%s.4.t:0 \"Your not meant to be here. No one is supposed to be here.\""%modTitle)
    #localization.write("\nNCE_%s.5.t:0 \"Skill change\"\n\n"%modTitle)

    #Advisor Spacific
    j=0
    for advisor in advisor_list:
        i=0
        localization.write("\n")
        #Advisor Level Localizations
        for level in advisor_level_data:
            localization.write("\nNCE_%s_%s:0 "%(level,advisor.dataName))
            localization.write("\"%s %s\""%(advisor_level_Name[i],advisor.titleEng))
            i +=1
        
        localization.write("\nNCE_%s.%s_test.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"How should we proceed to evaluate $%s$?\"\n"%(advisor.dataName.upper()))
        
        localization.write("NCE_%s.%s_left.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Your %s has departed your court and his unique abilities have left as well.\"\n"%advisor.titleEng)

        localization.write("NCE_%s.%s_skill.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"After evaluation it was determined that  $%s$'s abilities are\"\n"%(advisor.dataName.upper()))

        localization.write("NCE_%s.%s_ProG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"After $%s$ recent promotion $%s_S_PRONOUN$ has risen to the occasion and is now\"\n"%(advisor.dataName.upper(),advisor.dataName.upper()))
        
        localization.write("NCE_%s.%s_ProB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"After $%s$ recent promotion $%s_S_PRONOUN$ has cracked under the pressure and is now\"\n"%(advisor.dataName.upper(),advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"After many years of service $%s$ abilities have improved to\"\n"%(advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"After many years of service $%s$ abilities have declined to\""%(advisor.dataName.upper()))
        
        localization.write("\nNCE_%s.%i.t:0 \"Not all men are created equal. ~ %s\""%(modTitle,j*numEventsPerAdvisor+1,advisor.titleEng))
        localization.write("\nNCE_%s.%i.t:0 \"Skill level report ~ %s\""%(modTitle,j*numEventsPerAdvisor+3,advisor.titleEng))   
        localization.write("\nNCE_%s.%i.t:0 \"Skill change ~ %s\""%(modTitle,j*numEventsPerAdvisor+5,advisor.titleEng))
        j+=1
    localization.close()

def German_localization(advisor_list, advisor_level_data, modTitle):
    localization = open(("localisation\\NCE_%s_l_german.yml"%modTitle), "w", encoding='utf-8-sig')
    localization.write("l_german:")
    advisor_level_Name = ["Furchtbar", "Ungeschickt", "Mittelmäßig", "Gut", "Großartig", "Tolle"]

    #General Localizations
    #localization.write("\nNCE_%s.1.t:0 \"Nicht alle Männer sind gleich geschaffen.\""%modTitle)
    localization.write("\nNCE_%s.1.a:0 \"Nichts tun.\""%modTitle)            
    localization.write("\nNCE_%s.1.b:0 \"Sparen Sie keine Kosten.\""%modTitle)
    localization.write("\nNCE_%s.1.c:0 \"Üben Sie Ihren Einfluss aus.\""%modTitle)
    localization.write("\nNCE_%s.1.d:0 \"Wirf Männer auf das Problem.\""%modTitle)
    localization.write("\nNCE_%s.1.e:0 \"Lassen Sie uns diese Kosten für später verschieben.\""%modTitle)
    localization.write("\nNCE_%s.1.f:0 \"...Erfolg durch Betrug. ~Sophocles\""%modTitle)
    localization.write("\nNCE_%s.1.g:0 \"Ich bin der König.\""%modTitle)
    localization.write("\nNCE_%s.2.t:0 \"Der Berater hat Ihr Gericht verlassen.\""%modTitle)         
    localization.write("\nNCE_%s.2.a:0 \"OK\""%modTitle)
    #localization.write("\nNCE_%s.3.t:0 \"Erfahrungsbericht\"\n"%modTitle)            
    for l in range(len(advisor_level_Name)):      #Level Name Buttons
        localization.write("\nNCE_%s.3.%s:0"%(modTitle,chr(97+l)))
        localization.write(" \"%s.\""%(advisor_level_Name[l]))
    localization.write("\nNCE_%s.4.a:0 \"Berater verloren\""%modTitle)
    localization.write("\nNCE_%s.4.t:0 \"Your not meant to be here. No one is supposed to be here.\""%modTitle)
    #localization.write("\nNCE_%s.5.t:0 \"Fähigkeitsänderung\"\n\n"%modTitle)

    #Advisor Spacific
    j=0
    for advisor in advisor_list:
        i=0
        localization.write("\n")
        #Advisor Level Localizations
        for level in advisor_level_data:
            localization.write("\nNCE_%s_%s:0 "%(level,advisor.dataName))
            localization.write("\"%s %s\""%(advisor_level_Name[i],advisor.titleGer))
            i +=1
        
        localization.write("\nNCE_%s.%s_test.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Wie sollen wir vorgehen, $%s$, Ihr %s?\"\n"%(advisor.dataName.upper(),advisor.titleGer))
        
        localization.write("NCE_%s.%s_left.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Ihr %s hat Ihr Gericht verlassen und auch seine einzigartigen Fähigkeiten haben Ihr Gericht verlassen.\"\n"%advisor.titleGer)

        localization.write("NCE_%s.%s_skill.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Nach der Bewertung wurde festgestellt, dass Ihre %s, $%s$, Fähigkeiten sind\"\n"%(advisor.titleGer,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_ProG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Nach Ihrem %s, $%s$, kürzlich erfolgter Beförderung ist er zu Anlass aufgestiegen und ist es jetzt\"\n"%(advisor.titleGer,advisor.dataName.upper()))
        
        localization.write("NCE_%s.%s_ProB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Nach Ihrem %s, $%s$s, jüngster Beförderung hat er unter dem Druck geknackt und ist jetzt\"\n"%(advisor.titleGer,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Nach vielen Jahren des Dienstes haben sich die Fähigkeiten von %s, $%s$, verbessert\"\n"%(advisor.titleGer,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Nach vielen Jahren des Dienstes haben sich die Fähigkeiten von %s, $%s$, verschlechtert\""%(advisor.titleGer,advisor.dataName.upper()))

        localization.write("\nNCE_%s.%i.t:0 \"Nicht alle Männer sind gleich geschaffen. ~ %s\""%(modTitle,j*numEventsPerAdvisor+1,advisor.titleGer))
        localization.write("\nNCE_%s.%i.t:0 \"Erfahrungsbericht ~ %s\""%(modTitle,j*numEventsPerAdvisor+3,advisor.titleGer)) 
        localization.write("\nNCE_%s.%i.t:0 \"Fähigkeitsänderung ~ %s\""%(modTitle,j*numEventsPerAdvisor+5,advisor.titleGer)) 
        j+=1
    localization.close()

def French_localization(advisor_list, advisor_level_data, modTitle):
    localization = open(("localisation\\NCE_%s_l_french.yml"%modTitle), "w", encoding='utf-8-sig')
    localization.write("l_french:")
    advisor_level_Name = ["Terrible", "Inepte", "Médiocre", "Bon", "Génial", "Incroyable"]

    #General Localizations
    #localization.write("\nNCE_%s.1.t:0 \"Tous les hommes ne sont pas créés égaux.\""%modTitle)
    localization.write("\nNCE_%s.1.a:0 \"Ne Fais Rien.\""%modTitle)            
    localization.write("\nNCE_%s.1.b:0 \"Ne Ménagez Aucune Dépense.\""%modTitle)
    localization.write("\nNCE_%s.1.c:0 \"Exercez notre Influence.\""%modTitle)
    localization.write("\nNCE_%s.1.d:0 \"Jetez les Hommes au Problème.\""%modTitle)
    localization.write("\nNCE_%s.1.e:0 \"Repoussons ces dépenses pour plus tard.\""%modTitle)
    localization.write("\nNCE_%s.1.f:0 \"...Réussir par la fraude. ~Sophocles\""%modTitle)
    localization.write("\nNCE_%s.1.g:0 \"Je suis le roi.\""%modTitle)
    localization.write("\nNCE_%s.2.t:0 \"Le Conseiller a Quitté Votre Court.\""%modTitle)
    localization.write("\nNCE_%s.2.a:0 \"OK\""%modTitle)
    #localization.write("\nNCE_%s.3.t:0 \"Rapport sur le niveau de compétence\"\n"%modTitle)            
    for l in range(len(advisor_level_Name)):      #Level Name Buttons
        localization.write("\nNCE_%s.3.%s:0"%(modTitle,chr(97+l)))
        localization.write(" \"%s.\""%(advisor_level_Name[l]))
    localization.write("NCE_%s.4.a:0 \"Conseiller Perdu\""%modTitle)
    localization.write("\nNCE_%s.4.t:0 \"Your not meant to be here. No one is supposed to be here.\""%modTitle)
    #localization.write("\nNCE_%s.5.t:0 \"Changement de Compétence\"\n\n"%modTitle)

    #Advisor Spacific
    j=0
    for advisor in advisor_list:
        i=0
        localization.write("\n")
        #Advisor Level Localizations
        for level in advisor_level_data:
            localization.write("\nNCE_%s_%s:0 "%(level,advisor.dataName))
            localization.write("\"%s %s\""%(advisor_level_Name[i],advisor.titleFra))
            i +=1
        
        localization.write("NCE_%s.%s_test.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Comment procéder pour évaluer, $%s$, votre %s?\"\n"%(advisor.dataName.upper(),advisor.titleFra))
        
        localization.write("NCE_%s.%s_left.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Votre %s a quitté votre terrain et ses capacités uniques sont également parties.\"\n"%advisor.titleFra)

        localization.write("NCE_%s.%s_skill.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Après évaluation, il a été déterminé que vos capacités %s, $%s$, sont\"\n"%(advisor.titleFra,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_ProG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Après la récente promotion de votre %s, $%s$, $%s_S_PRONOUN$ a su saisir l'occasion et est maintenant\"\n"%(advisor.titleFra,advisor.dataName.upper(),advisor.dataName.upper()))
        
        localization.write("NCE_%s.%s_ProB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Après la récente promotion de votre %s, $%s$, $%s_S_PRONOUN$ a craqué sous la pression et est maintenant\"\n"%(advisor.titleFra,advisor.dataName.upper(),advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Après de nombreuses années de service vos capacités %s, $%s$, se sont améliorées pour\"\n"%(advisor.titleFra,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Après de nombreuses années de service vos capacités %s, $%s$, se ont diminué\""%(advisor.titleFra,advisor.dataName.upper()))

        localization.write("\nNCE_%s.%i.t:0 \"Tous les hommes ne sont pas créés égaux. ~ %s\""%(modTitle,j*numEventsPerAdvisor+1,advisor.titleFra))
        localization.write("\nNCE_%s.%i.t:0 \"Rapport sur le niveau de compétence ~ %s\""%(modTitle,j*numEventsPerAdvisor+3,advisor.titleFra)) 
        localization.write("\nNCE_%s.%i.t:0 \"Changement de Compétence ~ %s\""%(modTitle,j*numEventsPerAdvisor+5,advisor.titleFra)) 
        j+=1
    localization.close()

def Spanish_localization(advisor_list, advisor_level_data, modTitle):
    localization = open(("localisation\\NCE_%s_l_spanish.yml"%modTitle), "w", encoding='utf-8-sig')
    localization.write("l_spanish:")
    advisor_level_Name = ["Terrible", "Inepto", "Mediocre", "Bueno", "Excelente", "Increíble"]

    #General Localizations
    #localization.write("\nNCE_%s.1.t:0 \"No todos los hombres son creados iguales.\""%modTitle)
    localization.write("\nNCE_%s.1.a:0 \"Hacer Nada.\""%modTitle)            
    localization.write("\nNCE_%s.1.b:0 \"No escatimar gastos.\""%modTitle)
    localization.write("\nNCE_%s.1.c:0 \"Ejercer nuestra influencia.\""%modTitle)
    localization.write("\nNCE_%s.1.d:0 \"Lanzar hombres al problema.\""%modTitle)
    localization.write("\nNCE_%s.1.e:0 \"Alejemos ese gasto para más tarde.\""%modTitle)
    localization.write("\nNCE_%s.1.f:0 \"...Tener éxito por fraude. ~Sophocles\""%modTitle)
    localization.write("\nNCE_%s.1.g:0 \"Soy el Rey.\""%modTitle)
    localization.write("\nNCE_%s.2.t:0 \"El asesor ha abandonado tu corte.\""%modTitle)         
    localization.write("\nNCE_%s.2.a:0 \"OK\""%modTitle)
    #localization.write("\nNCE_%s.3.t:0 \"Informe de nivel de habilidad\"\n"%modTitle)            
    for l in range(len(advisor_level_Name)):      #Level Name Buttons
        localization.write("\nNCE_%s.3.%s:0"%(modTitle,chr(97+l)))
        localization.write(" \"%s.\""%(advisor_level_Name[l]))
    localization.write("NCE_%s.4.a:0 \"Asesor perdido\""%modTitle)
    localization.write("\nNCE_%s.4.t:0 \"Your not meant to be here. No one is supposed to be here.\""%modTitle)
    #localization.write("\nNCE_%s.5.t:0 \"Cambio de habilidad\"\n\n"%modTitle)

    #Advisor Spacific
    j=0
    for advisor in advisor_list:
        i=0
        localization.write("\n")
        #Advisor Level Localizations
        for level in advisor_level_data:
            localization.write("\nNCE_%s_%s:0 "%(level,advisor.dataName))
            localization.write("\"%s %s\""%(advisor_level_Name[i],advisor.titleSpa))
            i +=1
        
        localization.write("NCE_%s.%s_test.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"¿Cómo debemos proceder para evaluar, $%s$, su %s?\"\n"%(advisor.titleSpa,advisor.dataName.upper()))
        
        localization.write("NCE_%s.%s_left.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Tu %s se fue de tu corte y sus habilidades únicas también se fueron.\"\n"%advisor.titleSpa)

        localization.write("NCE_%s.%s_skill.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Después de la evaluación se determinó que las habilidades de tu %s, $%s$, son\"\n"%(advisor.titleSpa,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_ProG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Después de la reciente promoción de tu %s, $%s$, $%s_S_PRONOUN$ ha estado a la altura y ahora\"\n"%(advisor.titleSpa,advisor.dataName.upper(),advisor.dataName.upper()))
        
        localization.write("NCE_%s.%s_ProB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Después de la reciente promoción de tu %s, $%s$, $%s_S_PRONOUN$ ha roto bajo la presión y ahora está\"\n"%(advisor.titleSpa,advisor.dataName.upper(),advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHG.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Después de muchos años de servicio, las habilidades de tu %s, $%s$, han mejorado\"\n"%(advisor.titleSpa,advisor.dataName.upper()))

        localization.write("NCE_%s.%s_MTTHB.d:0 "%(advisor.modSuffix,advisor.dataName))
        localization.write("\"Después de muchos años de servicio, las habilidades de tu %s, $%s$ han disminuido\""%(advisor.titleSpa,advisor.dataName.upper()))

        localization.write("\nNCE_%s.%i.t:0 \"No todos los hombres son creados iguales. ~ %s\""%(modTitle,j*numEventsPerAdvisor+1,advisor.titleSpa))
        localization.write("\nNCE_%s.%i.t:0 \"Informe de nivel de habilidad ~ %s\""%(modTitle,j*numEventsPerAdvisor+3,advisor.titleSpa)) 
        localization.write("\nNCE_%s.%i.t:0 \"Cambio de habilidad ~ %s\""%(modTitle,j*numEventsPerAdvisor+5,advisor.titleSpa)) 
        j+=1
    localization.close()

def combinedMTTHEvents(advisor_list,modTitle,HEvent,x,PointType):
    counter = 0
    q=0
    HEvent.write("\nCountry_event = {")
    HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
    HEvent.write("\n\ttitle = NCE_%s.%s.t"%(modTitle,PointType))
    HEvent.write("\n\tdesc = NCE_%s_%s.%i"%(modTitle,PointType,x))
    HEvent.write("\n\tpicture = ADVISOR_eventPicture")
    HEvent.write("\n\thidden = yes")
    HEvent.write("\n\ttrigger = {")
    if AIEvents[0] <1:
        HEvent.write("\n\t\tai = no")
    HEvent.write("\n\t\tOR = {")
    for advisor in advisor_list:
        if advisor.pointType == PointType:
            HEvent.write("\n\t\t\thas_country_flag = NCE_%s_skill"%advisor.dataName)
    HEvent.write("\n\t\t}")
    HEvent.write("\n\t}")
    HEvent.write("\n\tmean_time_to_happen = { months = %g }"%MTTHMonths[0]) 
    HEvent.write("\n\toption = {")

    for advisor in advisor_list:
        if advisor.pointType == PointType:
            if counter==0:
                HEvent.write("\n\t\tif = {")
            else:
                HEvent.write("\n\t\telse_if = {")
            HEvent.write("\n\t\t\tlimit = { advisor = %s }"%advisor.dataName)
            for l in range(len(advisor_level_data)):
                if l==0:
                    HEvent.write("\n\t\t\tif = {")
                elif l==5:
                    HEvent.write("\n\t\t\telse = {")
                else:
                    HEvent.write("\n\t\t\telse_if = {")
                HEvent.write("\n\t\t\t\tlimit = { has_country_modifier = NCE_%s_%s }"%(advisor_level_data[l],advisor.dataName))
                HEvent.write("\n\t\t\t\trandom_list = {")
                for k in range(len(advisor_level_data)):
                    if advMTTPresentage[l][k] == 0:
                        pass
                    else:
                        HEvent.write("\n\t\t\t\t\t%i = {"%advMTTPresentage[l][k])
                        if l == k:
                            HEvent.write(" }")
                        else:
                            HEvent.write("\n\t\t\t\t\t\tremove_country_modifier = NCE_%s_%s"%(advisor_level_data[l],advisor.dataName))
                            HEvent.write("\n\t\t\t\t\t\tadd_country_modifier = {")
                            if k==5:
                                HEvent.write("\n\t\t\t\t\t\t\tname = NCE_%s_%s"%(advisor_level_data[k-1],advisor.dataName))
                            else:
                                HEvent.write("\n\t\t\t\t\t\t\tname = NCE_%s_%s"%(advisor_level_data[k],advisor.dataName))
                            HEvent.write("\n\t\t\t\t\t\t\tduration = -1")
                            HEvent.write("\n\t\t\t\t\t\t}")
                            HEvent.write("\n\t\t\t\t\t\tif = {")
                            HEvent.write("\n\t\t\t\t\t\t\tlimit = {")
                            HEvent.write("\n\t\t\t\t\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                            HEvent.write("\n\t\t\t\t\t\t\t}")
                            HEvent.write("\n\t\t\t\t\t\t\tcountry_event = {")
                            if l<k:
                                HEvent.write("\n\t\t\t\t\t\t\t\tid = NCE_%s.%i"%(modTitle,(q*numEventsPerAdvisor+7)))
                            else:
                                HEvent.write("\n\t\t\t\t\t\t\t\tid = NCE_%s.%i"%(modTitle,(q*numEventsPerAdvisor+8)))
                            HEvent.write("\n\t\t\t\t\t\t\t\tdays = 0")
                            HEvent.write("\n\t\t\t\t\t\t\t}")
                            HEvent.write("\n\t\t\t\t\t\t}")
                            HEvent.write("\n\t\t\t\t\t}")
                HEvent.write("\n\t\t\t\t}")
                HEvent.write("\n\t\t\t}")
            HEvent.write("\n\t\t}")

            counter+=1
        q+=1
    HEvent.write("\n\t}")
    HEvent.write("\n}")

def combinedHireEvents(advisor_list,modTitle,HEvent,x,PointType):
    counter = 0
    q=0
    HEvent.write("\nCountry_event = {")
    HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
    HEvent.write("\n\ttitle = NCE_%s.%s.t"%(modTitle,PointType))
    HEvent.write("\n\tdesc = NCE_%s_%s.%i"%(modTitle,PointType,x))
    HEvent.write("\n\tpicture = ADVISOR_eventPicture")
    HEvent.write("\n\thidden = yes")
    HEvent.write("\n\ttrigger = {")
    if AIEvents[0] <1:
        HEvent.write("\n\t\tai = no")
    HEvent.write("\n\t\tOR = {")
    for advisor in advisor_list:
        if advisor.pointType == PointType:
            HEvent.write("\n\t\t\tAND = {")
            HEvent.write("\n\t\t\t\tadvisor = %s"%advisor.dataName)
            HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_%s_skill }"%advisor.dataName)
            HEvent.write("\n\t\t\t}")
    HEvent.write("\n\t\t}")
    HEvent.write("\n\t}")
    HEvent.write("\n\tmean_time_to_happen = { days = -1 }") 
    HEvent.write("\n\toption = {")

    for advisor in advisor_list:
        if advisor.pointType == PointType:
            if counter==0:
                HEvent.write("\n\t\tif = {")
            else:
                HEvent.write("\n\t\telse_if = {")
            HEvent.write("\n\t\t\tlimit = { advisor = %s }"%advisor.dataName)

            HEvent.write("\n\t\t\tcountry_event = {")
            HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(q*numEventsPerAdvisor+1)))
            HEvent.write("\n\t\t\t\tdays = 0")
            HEvent.write("\n\t\t\t}")

            HEvent.write("\n\t\t}")

            counter+=1
        q+=1
    HEvent.write("\n\t}")
    HEvent.write("\n}")

def combinedFireEvents(advisor_list,modTitle,HEvent,x,PointType):
    counter = 0
    q=0
    HEvent.write("\nCountry_event = {")
    HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
    HEvent.write("\n\ttitle = NCE_%s.%s.t"%(modTitle,PointType))
    HEvent.write("\n\tdesc = NCE_%s_%s.%i"%(modTitle,PointType,x))
    HEvent.write("\n\tpicture = ADVISOR_eventPicture")
    HEvent.write("\n\thidden = yes")
    HEvent.write("\n\ttrigger = {")
    #if AIEvents[0] <1: #in case users disable events mid save this will allow AI to still lose modifiers
    #    HEvent.write("\n\t\tai = no")
    HEvent.write("\n\t\tOR = {")
    for advisor in advisor_list:
        if advisor.pointType == PointType:
            HEvent.write("\n\t\t\tAND = {")
            HEvent.write("\n\t\t\t\tnot = { advisor = %s }"%advisor.dataName)
            HEvent.write("\n\t\t\t\thas_country_flag = NCE_%s_skill"%advisor.dataName)
            HEvent.write("\n\t\t\t}")
    HEvent.write("\n\t\t}")
    HEvent.write("\n\t}")
    HEvent.write("\n\tmean_time_to_happen = { days = -1 }") 
    HEvent.write("\n\toption = {")

    for advisor in advisor_list:
        if advisor.pointType == PointType:
            if counter==0:
                HEvent.write("\n\t\tif = {")
            else:
                HEvent.write("\n\t\telse_if = {")
            HEvent.write("\n\t\t\tlimit = { has_country_flag = NCE_%s_skill }"%advisor.dataName)

            HEvent.write("\n\t\t\tcountry_event = {")
            HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(q*numEventsPerAdvisor+2)))
            HEvent.write("\n\t\t\t\tdays = 0")
            HEvent.write("\n\t\t\t}")

            HEvent.write("\n\t\t}")

            counter+=1
        q+=1
    HEvent.write("\n\t}")
    HEvent.write("\n}")

def combinedPromoteEvents(advisor_list,modTitle,HEvent,x,PointType):
    counter = 0
    q=0
    HEvent.write("\nCountry_event = {")
    HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
    HEvent.write("\n\ttitle = NCE_%s.%s.t"%(modTitle,PointType))
    HEvent.write("\n\tdesc = NCE_%s_%s.%i"%(modTitle,PointType,x))
    HEvent.write("\n\tpicture = ADVISOR_eventPicture")
    HEvent.write("\n\thidden = yes")
    HEvent.write("\n\ttrigger = {")
    if AIEvents[0] <1:
        HEvent.write("\n\t\tai = no")
    HEvent.write("\n\t\tOR = {")
    for advisor in advisor_list:
        if advisor.pointType == PointType:
            for l in range(1,MaxAdvisorLevel[0]):
                HEvent.write("\n\t\t\tand = {")
                HEvent.write("\n\t\t\t\thas_country_flag = NCE_%s_level_%i"%(advisor.dataName,l))
                HEvent.write("\n\t\t\t\tadvisor = %s"%advisor.dataName)
                HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,l+1))

                HEvent.write("\n\t\t\t}")

    HEvent.write("\n\t\t}")
    HEvent.write("\n\t}")
    HEvent.write("\n\tmean_time_to_happen = { days = -1 }") 
    HEvent.write("\n\toption = {")
    for advisor in advisor_list:
        if advisor.pointType == PointType:
            if counter==0:
                HEvent.write("\n\t\tif = {")
            else:
                HEvent.write("\n\t\telse_if = {")
            HEvent.write("\n\t\t\tlimit = { advisor = %s }"%advisor.dataName)

            HEvent.write("\n\t\t\tcountry_event = {")
            HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(q*numEventsPerAdvisor+4)))
            HEvent.write("\n\t\t\t\tdays = 0")
            HEvent.write("\n\t\t\t}")

            HEvent.write("\n\t\t}")

            counter+=1
        q+=1

    HEvent.write("\n\t}")
    HEvent.write("\n}")

def Hire_Events(advisor_list, modTitle):
    x=1
    writeProEvents = False
    writeMTTHEvents = False
    showHireEvent = False
    for i in range(len(advProPresentage)):
        for j in range(len(advProPresentage[i])):
            if not advProPresentage[i][j] > 0:
                writeProEvents = True
                break
    for i in range(len(advMTTPresentage)):
        for j in range(len(advMTTPresentage[i])):
            if not advMTTPresentage[i][j] > 0:
                writeMTTHEvents = True
                break
    for i in range(len(PrecentagePerOption)):
        if i==0:
            pass
        else:
            if PrecentagePerOption[i] >0:
                showHireEvent = True
                break
    pointArray = ['MIL','ADM','DIP']
    HEvent = open(("events/NCE_%s.txt"%modTitle), "w", encoding='utf-8')
    HEvent.write("########################################\n# Events for Not Created Equal\n#\n# written by Licarious Fenrir\n########################################")
    HEvent.write("\n\nnamespace = NCE_%s"%modTitle)
    j = 0
    for advisor in advisor_list:
        if advisor.titleEng == "":
            HEvent.write("\n\n#%s"%advisor.dataName)
        else:
            HEvent.write("\n\n#%s"%advisor.titleEng)
        for e in range(1,numEventsPerAdvisor+1):
            HEvent.write("\nCountry_event = {")

            #Gained Advisor
            if e%numEventsPerAdvisor==1: 
                HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
                HEvent.write("\n\ttitle = NCE_%s.1.t"%(modTitle))
                HEvent.write("\n\tdesc = NCE_%s.%s_test.d"%(modTitle,advisor.dataName))
                HEvent.write("\n\tpicture = ADVISOR_eventPicture")
                HEvent.write("\n\tis_triggered_only = yes")
                HEvent.write("\n\timmediate = { set_country_flag = NCE_%s_skill }"%advisor.dataName)

                if not showHireEvent:
                    HEvent.write("\n\thidden = yes")

                #Option Do Nothing
                if PrecentagePerOption[0]>0 and PrecentagePerOption[0]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #Do nothing")
                    HEvent.write("\n\t\tname = NCE_%s.%i.a"%(modTitle,j*numEventsPerAdvisor+1))
                
                    HEvent.write("\n\t\tai_chance = { factor = %s }"%AIPrecentage[0])
                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[0]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[0]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")
                #Spare No Expense
                if PrecentagePerOption[1]>0 and PrecentagePerOption[1]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #Spare No Expense")
                    HEvent.write("\n\t\tname = NCE_%s.1.b"%modTitle)

                    #limit
                    HEvent.write("\n\t\t\tai_chance = {")
                    HEvent.write("\n\t\t\t\tfactor = %s"%AIPrecentage[1])
                    HEvent.write("\n\t\t\t\tmodifier = {\n\t\t\t\t\tfactor = 0")
                    HEvent.write("\n\t\t\t\t\tor = {")
                    for l in range(3):
                        HEvent.write("\n\t\t\t\t\t\tand = {")
                        HEvent.write("\n\t\t\t\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t\t\t\t\tnot = { treasury = %i }"%int(money[l]*1.35))
                        HEvent.write("\n\t\t\t\t\t\t\tnot = { monthly_income = %g }"%(money[l]/12))
                        HEvent.write("\n\t\t\t\t\t\t}")
                    HEvent.write("\n\t\t\t\t\t}")
                    HEvent.write("\n\t\t\t\t}")
                    HEvent.write("\n\t\t\t\tmodifier = {\n\t\t\t\t\tfactor = 0")
                    HEvent.write("\n\t\t\t\t\tnot = { is_bankrupt = yes }")
                    HEvent.write("\n\t\t\t\t}")
                    HEvent.write("\n\t\t\t}")


                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")


                        HEvent.write("\n\t\t\tadd_treasury = %i"%(-1*money[l]))
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[1]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[1]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")
                #Exert Our Influence
                if PrecentagePerOption[2]>0 and PrecentagePerOption[2]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #Exert Our Influence")
                    HEvent.write("\n\t\tname = NCE_%s.1.c"%modTitle)
                    
                    #limit
                    HEvent.write("\n\t\t\tai_chance = {")
                    HEvent.write("\n\t\t\t\tfactor = %s"%AIPrecentage[2])
                    HEvent.write("\n\t\t\t\tmodifier = {\n\t\t\t\t\tfactor = 0")
                    HEvent.write("\n\t\t\t\t\tor = {")
                    for l in range(3):
                        HEvent.write("\n\t\t\t\t\t\tand = {")
                        HEvent.write("\n\t\t\t\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t\t\t\t\tnot = { %s_power = %i }"%(advisor.pointType.lower(),int(influence[l]*10)))
                        HEvent.write("\n\t\t\t\t\t\t}")
                    HEvent.write("\n\t\t\t\t\t}")
                    HEvent.write("\n\t\t\t\t}")
                    HEvent.write("\n\t\t\t}")

                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")
                        

                        HEvent.write("\n\t\t\tadd_%s_power = %i"%(advisor.pointType.lower(),(-1*influence[l])))
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[2]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[2]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")
                #Throw Men at the Problem
                if PrecentagePerOption[3]>0 and PrecentagePerOption[3]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #Throw Men at the Problem")
                    HEvent.write("\n\t\tname = NCE_%s.1.d"%modTitle)

                    #limit
                    HEvent.write("\n\t\t\tai_chance = {")
                    HEvent.write("\n\t\t\t\tfactor = %s"%AIPrecentage[3])
                    HEvent.write("\n\t\t\t\tmodifier = {\n\t\t\t\t\tfactor = 0")
                    HEvent.write("\n\t\t\t\t\tnot = { manpower_percentage  = 0.65 }")
                    HEvent.write("\n\t\t\t\t}")
                    HEvent.write("\n\t\t\t\tmodifier = {\n\t\t\t\t\tfactor = 0")
                    HEvent.write("\n\t\t\t\t\tnot = { sailors_percentage = 0.5 }")
                    HEvent.write("\n\t\t\t\t}")
                    HEvent.write("\n\t\t\t}")

                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")
                        
                
                        HEvent.write("\n\t\t\tadd_yearly_manpower = %g"%(-1*(manpower[l])))
                        HEvent.write("\n\t\t\tadd_yearly_sailors = %g"%(-1*(sailors[l])))
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[3]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[3]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")
                #Corruption & Inflation
                if PrecentagePerOption[4]>0 and PrecentagePerOption[4]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #push off that expense for later.")
                    HEvent.write("\n\t\tname = NCE_%s.1.e"%modTitle)

                    #limit
                    HEvent.write("\n\t\t\tai_chance = {")
                    HEvent.write("\n\t\t\t\tfactor = %s"%AIPrecentage[4])
                    HEvent.write("\n\t\t\t}")

                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")
                        
                
                        HEvent.write("\n\t\t\tadd_corruption = %g"%((corruption[l])))
                        HEvent.write("\n\t\t\tadd_inflation = %g"%((inflation[l])))
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[4]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[4]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")
                #Embezzle Money
                if PrecentagePerOption[5]>0 and PrecentagePerOption[5]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #Embezzle Money")
                    HEvent.write("\n\t\tname = NCE_%s.1.f"%modTitle)

                    #limit
                    HEvent.write("\n\t\t\tai_chance = {")
                    HEvent.write("\n\t\t\t\tfactor = %s"%AIPrecentage[5])
                    HEvent.write("\n\t\t\t}")

                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")


                        HEvent.write("\n\t\t\tadd_treasury = %i"%(-1*embezzleMoney[l]))
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[5]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[5]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")
                #Embezzle Influence
                if PrecentagePerOption[6]>0 and PrecentagePerOption[6]<=len(AdvisorPresentage):
                    HEvent.write("\n\toption = { #Embezzle Influence")
                    HEvent.write("\n\t\tname = NCE_%s.1.g"%modTitle)
                    
                    #limit
                    HEvent.write("\n\t\t\tai_chance = {")
                    HEvent.write("\n\t\t\t\tfactor = %s"%AIPrecentage[6])
                    HEvent.write("\n\t\t\t}")

                    for l in range(MaxLevelBeforPromote[0]):
                        if l==0:
                            HEvent.write("\n\t\tif = {")
                        elif l==MaxLevelBeforPromote[0]-1:
                            HEvent.write("\n\t\telse = {")
                        else:
                            HEvent.write("\n\t\telse_if = {")
                        HEvent.write("\n\t\t\tlimit = {")
                        HEvent.write("\n\t\t\t\t%s = %i"%(advisor.dataName,(l+1)))
                        if l < 2:
                            HEvent.write("\n\t\t\t\tnot = { %s = %i }"%(advisor.dataName,(l+2)))
                        HEvent.write("\n\t\t\t}")
                        

                        HEvent.write("\n\t\t\tadd_%s_power = %i"%(advisor.pointType.lower(),(-1*embezzleInfluence[l])))
                        HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,(l+1)))
                        HEvent.write("\n\t\t\trandom_list = {")
                        for k in range (len(advisor_level_data)):
                            if int(AdvisorPresentage[PrecentagePerOption[6]][l][k]) == 0:
                                pass
                            else:
                                HEvent.write("\n\t\t\t\t%s = {"%AdvisorPresentage[PrecentagePerOption[6]][l][k])
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = \"NCE_%s_%s\""%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1\n\t\t\t\t\t}\n\t\t\t\t}")
                        HEvent.write("\n\t\t\t}")
                        HEvent.write("\n\t\t}")
                    HEvent.write("\n\t\tif = {")
                    HEvent.write("\n\t\t\tlimit = {")
                    HEvent.write("\n\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t\tcountry_event = {")
                    HEvent.write("\n\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                    HEvent.write("\n\t\t\t\tdays = 0")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                    HEvent.write("\n\t}")

            #Fire
            elif e%numEventsPerAdvisor==2:
                HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
                HEvent.write("\n\ttitle = NCE_%s.2.t"%modTitle)
                HEvent.write("\n\tdesc = NCE_%s.%s_left.d"%(modTitle,advisor.dataName))
                HEvent.write("\n\tpicture = ADVISOR_eventPicture")
                HEvent.write("\n\thidden = yes")
                HEvent.write("\n\tis_triggered_only = yes")
                HEvent.write("\n\timmediate = {")

                HEvent.write("\n\t\tclr_country_flag = NCE_%s_skill"%advisor.dataName)
                for level in advisor_level_data:
                    HEvent.write("\n\t\tremove_country_modifier = NCE_%s_%s"%(level,advisor.dataName))
                for alf in range(1,MaxAdvisorLevel[0]+1):
                    HEvent.write("\n\t\tclr_country_flag = NCE_%s_level_%i"%(advisor.dataName,alf))
                HEvent.write("\n\t}")
                HEvent.write("\n\toption = { name = NCE_%s.2.a }"%modTitle)
            
            #Hire Report
            elif e%numEventsPerAdvisor==3:
                HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
                HEvent.write("\n\ttitle = NCE_%s.%i.t"%(modTitle,x))
                HEvent.write("\n\tdesc = NCE_%s.%s_skill.d"%(modTitle,advisor.dataName))
                HEvent.write("\n\tpicture = ADVISOR_eventPicture")
                HEvent.write("\n\tis_triggered_only = yes")
                for opt in range(6):
                    HEvent.write("\n\toption = {")
                    HEvent.write("\n\t\tname = NCE_%s.3.%s"%(modTitle,chr(97+opt)))
                    HEvent.write("\n\t\ttrigger = {has_country_modifier = NCE_%s_%s}"%(advisor_level_data[opt],advisor.dataName))
                    HEvent.write("\n\t}")

            #Promote
            elif e%numEventsPerAdvisor==4:
                HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
                HEvent.write("\n\ttitle = NCE_%s.4.t"%modTitle)
                HEvent.write("\n\tdesc = NCE_%s.%s_test.d"%(modTitle,advisor.dataName))
                HEvent.write("\n\tpicture = ADVISOR_eventPicture")
                HEvent.write("\n\thidden = yes")
                HEvent.write("\n\tis_triggered_only = yes")

                HEvent.write("\n\timmediate = { ")
                for l in range(1,MaxAdvisorLevel[0]):
                    if l == 1:
                        HEvent.write("\n\t\tif = {")
                    elif l == MaxAdvisorLevel[0]-1:
                        HEvent.write("\n\t\telse = {")
                    else:
                        HEvent.write("\n\t\telse_if = {")
                    HEvent.write("\n\t\t\tlimit = { has_country_flag = NCE_%s_level_%i }"%(advisor.dataName,l))
                    HEvent.write("\n\t\t\tclr_country_flag = NCE_%s_level_%i"%(advisor.dataName,l))
                    HEvent.write("\n\t\t\tset_country_flag = NCE_%s_level_%i"%(advisor.dataName,l+1))
                    HEvent.write("\n\t\t}")
                HEvent.write("\n\t}")

                #options
                HEvent.write("\n\toption = {")
                HEvent.write("\n\t\tname = NCE_%s.2.a"%modTitle)
                
                for l in range(len(advisor_level_data)):
                    if l == 0:
                        HEvent.write("\n\t\tif = {")
                    elif l == 5:
                        HEvent.write("\n\t\telse = {")
                    else:
                        HEvent.write("\n\t\telse_if = {")
                    HEvent.write("\n\t\t\tlimit = { has_country_modifier = NCE_%s_%s }"%(advisor_level_data[l],advisor.dataName))
                    HEvent.write("\n\t\t\trandom_list = {")
                    for k in range(len(advisor_level_data)):
                        if advProPresentage[l][k] == 0:
                            pass
                        else:
                            HEvent.write("\n\t\t\t\t%i = {"%advProPresentage[l][k])
                            if l == k:
                                HEvent.write(" }")
                            else:
                                HEvent.write("\n\t\t\t\t\tremove_country_modifier = NCE_%s_%s"%(advisor_level_data[l],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\tadd_country_modifier = {")
                                HEvent.write("\n\t\t\t\t\t\tname = NCE_%s_%s"%(advisor_level_data[k],advisor.dataName))
                                HEvent.write("\n\t\t\t\t\t\tduration = -1")
                                HEvent.write("\n\t\t\t\t\t}")

                                HEvent.write("\n\t\t\t\t\tif = {")
                                HEvent.write("\n\t\t\t\t\t\tlimit = {")
                                HEvent.write("\n\t\t\t\t\t\t\tnot = { has_country_flag = NCE_hide_notification }")
                                HEvent.write("\n\t\t\t\t\t\t}")

                                HEvent.write("\n\t\t\t\t\t\tcountry_event = {")
                                if l<k:
                                    HEvent.write("\n\t\t\t\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+1)))
                                else:
                                    HEvent.write("\n\t\t\t\t\t\t\tid = NCE_%s.%i"%(modTitle,(x+2)))
                                HEvent.write("\n\t\t\t\t\t\t\tdays = 0")
                                HEvent.write("\n\t\t\t\t\t\t}")
                                HEvent.write("\n\t\t\t\t\t}")
                                HEvent.write("\n\t\t\t\t}")
                    HEvent.write("\n\t\t\t}")
                    HEvent.write("\n\t\t}")
                HEvent.write("\n\t}")
            
            #Promote Report
            elif (x%numEventsPerAdvisor==5 or x%numEventsPerAdvisor==6):
                HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
                HEvent.write("\n\ttitle = NCE_%s.%i.t"%(modTitle,j*numEventsPerAdvisor+5))
                if x%numEventsPerAdvisor == 5:
                    HEvent.write("\n\tdesc = NCE_%s.%s_ProG.d"%(modTitle,advisor.dataName))
                else:
                    HEvent.write("\n\tdesc = NCE_%s.%s_ProB.d"%(modTitle,advisor.dataName))
                HEvent.write("\n\tpicture = ADVISOR_eventPicture")
                HEvent.write("\n\tis_triggered_only = yes")
                for l in range(len(advisor_level_data)):
                    HEvent.write("\n\toption = {")
                    HEvent.write("\n\t\tname = NCE_%s.3.%s"%(modTitle,chr(97+l)))
                    HEvent.write("\n\t\ttrigger = { has_country_modifier = NCE_%s_%s }"%(advisor_level_data[l],advisor.dataName))
                    HEvent.write("\n\t}")

            #MTTH Report
            elif (x%numEventsPerAdvisor==7 or x%numEventsPerAdvisor==0):
                HEvent.write("\n\tid = NCE_%s.%i"%(modTitle,x))
                HEvent.write("\n\ttitle = NCE_%s.%i.t"%(modTitle,j*numEventsPerAdvisor+5))
                HEvent.write("\n\tdesc = NCE_%s.%s_MTTH"%(modTitle,advisor.dataName))
                if x%numEventsPerAdvisor==7:
                    HEvent.write("G.d")
                else:
                    HEvent.write("B.d")
                HEvent.write("\n\tpicture = ADVISOR_eventPicture")
                HEvent.write("\n\tis_triggered_only = yes")
                for l in range(len(advisor_level_data)):
                    HEvent.write("\n\toption = {")
                    HEvent.write("\n\t\tname = NCE_%s.3.%s"%(modTitle,chr(97+l)))
                    HEvent.write("\n\t\ttrigger = { has_country_modifier = NCE_%s_%s }"%(advisor_level_data[l],advisor.dataName))
                    HEvent.write("\n\t}")

            HEvent.write("\n}")
            x +=1
        j+=1
    #Advisor Combined Events
    HEvent.write("\n\n#Advisor Combined Events")
    for p in pointArray:
        inList = False
        for advisor in advisor_list:
            if p in advisor.pointType:
                inList = True
                break
        if inList:
            HEvent.write("\n#%s"%p)
            if MTTHMonths[0] > 0 and writeMTTHEvents:
                combinedMTTHEvents(advisor_list,modTitle,HEvent,x,p)
                x +=1
            combinedHireEvents(advisor_list,modTitle,HEvent,x,p)
            x +=1
            combinedFireEvents(advisor_list,modTitle,HEvent,x,p)
            x +=1
            if writeProEvents:
                combinedPromoteEvents(advisor_list,modTitle,HEvent,x,p)
                x +=1
    i=0

def Contry_modifiers(advisor_list, modTitle):
    HEvent = open(("common/event_modifiers/NCE_%s_modifiers.txt"%modTitle), "w", encoding='utf-8')
    for advisor in advisor_list:
        mName = advisor.modifierName.split(" ") #for spliting modifiers when advisors have more than one
        mValue = advisor.modifierValue.split(" ")
        for l in range(len(advisor_level_data)):
            HEvent.write("\nNCE_%s_%s = {"%(advisor_level_data[l],advisor.dataName))
            for m in range(len(mName)):
                HEvent.write(" %s = %g "%(mName[m],(float(mValue[m])*levelMult[l])))
            HEvent.write("}")
        HEvent.write("\n")

def mod_seperator(advisor_list):
    modList = []
    sepAdvisorList = []
    x=0
    for advisor in advisor_list:
        if advisor.modSuffix not in modList:
            modList.append(advisor.modSuffix)
    for mod in modList:
        sepAdvisorList.append([])
        for advisor in advisor_list:
            if advisor.modSuffix == mod:
                sepAdvisorList[x].append(advisor)
        x +=1
    return sepAdvisorList

def getConfig():
    lineList =[]
    for line in Config:
        if line.strip().startswith("#") or line.strip() == "":
            pass
        else:
            lineList.append(re.split(r'[\<\>\{\}\(\)\[\];,\s]\s*', line.strip()))
    for line in lineList:
        if "levelMult" in line:
            levelMult.clear()
            for element in line:
                try:
                    float(element)
                    levelMult.append(float(element))
                except:
                    pass
        if "LowPrecentage" in line:
            x=0
            LxL.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        LxL.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "NormalPercentage" in line:
            x=0
            Lx.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        Lx.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "BoostedPercentage" in line:
            x=0
            LxB.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        LxB.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "SuperPresentage" in line:
            x=0
            LxS.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        LxS.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "custom1" in line:
            x=0
            LxC1.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        LxC1.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "custom2" in line:
            x=0
            LxC2.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        LxC2.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "custom3" in line:
            x=0
            LxC3.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(element)
                    x+=1
                    if x==len(advisor_level_data):
                        LxC3.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "money" in line:
            money.clear()
            for element in line:
                try:
                    float(element)
                    money.append(float(element))
                except:
                    pass
        if "influence" in line:
            influence.clear()
            for element in line:
                try:
                    float(element)
                    influence.append(int(element))
                except:
                    pass
        if "manpower" in line:
            manpower.clear()
            for element in line:
                try:
                    float(element)
                    manpower.append(float(element))
                except:
                    pass
        if "sailors" in line:
            sailors.clear()
            for element in line:
                try:
                    float(element)
                    sailors.append(float(element))
                except:
                    pass
        if "corruption" in line:
            corruption.clear()
            for element in line:
                try:
                    float(element)
                    corruption.append(float(element))
                except:
                    pass
        if "inflation" in line:
            inflation.clear()
            for element in line:
                try:
                    float(element)
                    inflation.append(float(element))
                except:
                    pass
        if "embezzleMoney" in line:
            embezzleMoney.clear()
            for element in line:
                try:
                    float(element)
                    embezzleMoney.append(float(element))
                except:
                    pass
        if "embezzleInfluence" in line:
            embezzleInfluence.clear()
            for element in line:
                try:
                    float(element)
                    embezzleInfluence.append(int(element))
                except:
                    pass
        if "PrecentagePerOption" in line:
            PrecentagePerOption.clear()
            for element in line:
                try:
                    int(element)
                    PrecentagePerOption.append(int(element))
                except:
                    pass
        if "AIPrecentage" in line:
            AIPrecentage.clear()
            for element in line:
                try:
                    float(element)
                    AIPrecentage.append(element)
                except:
                    pass
        if "advProPresentage" in line:
            x=0
            advProPresentage.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(float(element))
                    x+=1
                    if x==len(advisor_level_data):
                        advProPresentage.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "advMTTHPresentage" in line:
            x=0
            advMTTPresentage.clear()
            tmp = []
            for element in line:
                try:
                    float(element)
                    tmp.append(float(element))
                    x+=1
                    if x==len(advisor_level_data):
                        advMTTPresentage.append(copy.deepcopy(tmp))
                        tmp.clear()
                        x=0
                except:
                    pass
        if "MTTHMonths" in line:
            MTTHMonths.clear()
            for element in line:
                try:
                    int(element)
                    MTTHMonths.append(int(element))
                except:
                    pass
        if "MaxAdvisorLevel" in line:
            MaxAdvisorLevel.clear()
            for element in line:
                try:
                    int(element)
                    MaxAdvisorLevel.append(int(element))
                except:
                    pass
        if "MaxLevelBeforPromote" in line:
            MaxLevelBeforPromote.clear()
            for element in line:
                try:
                    int(element)
                    MaxLevelBeforPromote.append(int(element))
                except:
                    pass
        if "AIEvents" in line:
            AIEvents.clear()
            for element in line:
                try:
                    int(element)
                    AIEvents.append(int(element))
                except:
                    pass
    i=0

getConfig()
AdvList = mod_seperator(advisor_list)
if not os.path.exists('localisation'):
    os.makedirs('localisation')
if not os.path.exists('events'):
    os.makedirs('events')
if not os.path.exists('common/event_modifiers'):
    os.makedirs('common/event_modifiers')

for m in AdvList:
    Hire_Events(m,m[0].modSuffix)
    Contry_modifiers(m,m[0].modSuffix)
    English_localization(m, advisor_level_data,m[0].modSuffix)
    German_localization(m, advisor_level_data,m[0].modSuffix)
    French_localization(m, advisor_level_data,m[0].modSuffix)
    Spanish_localization(m, advisor_level_data,m[0].modSuffix)


print("Done")