import lib2to3.pgen2.token
import math
import random
import time
import  numpy as np
from copy import deepcopy
import scipy.stats as sc
from matplotlib import pyplot as plt

"#برای مشخص کردن تعداد وزیر ها که به صورت عمومی تعریف شده است"
global queensNumber
global found_answer


#کلاس وزیر ها که در حقیقت یک حالت از مسئله ی ما به وجود می آورد
class Queens:


    #در این تابع سازنده مقادیر لیستی از مکان وزیر ها و هزینه(تعداد عدم برخورد) به ابجکت کویینز نسبت داده شده است
    def __init__(self , queens = [],cost = 0, childs = []):
        self.queens = queens
        self.fitness = self.Cost()
        self.Mediator()


    #برای تبدیل مختصات وزیر ها به تصویری مانند صفحه شطرنج استفاده میشود
    def Board(self):
        queens = self.queens
        n = len(queens)
        board = [['*' for i in range(n)]for i in range(n)]
        for i in range(n):
            board[i][queens[i]] = 'Q'
        return board


    #کلاس بالایی را به نمایش میگذارد
    def Display(self):
        board = self.Board()
        for item in board:
            print(item)


    #برای محاسبه ی برخورد وزیر ها استفاده میشود
    def Cost(self):
        queens = self.queens
        n = len(queens)
        max = n*(n-1)/2#ماکسیموم تعداد برخورد ها
        cost = 0
        for i in range(n):
            for j in range(i + 1, n):
                cost += self.CheckInterSection(queens[i], queens[j], i, j)
        self.fitness =int(max - cost)#تعداد برخورد ها - ماکسیموم مقدار بخورد ها = تعداد عدم برخورد


    #با این شرط ها بررسی میکند که آیا دو وزیر با هم برخورد عمودی یا اریب دارند یا خیر
    def CheckInterSection(self, a, b, i, j):
        if a == b:
            return 1
            #return 2 #میتوانیم با بیشتر کردن مقدار پنالتی برخورد های سطری به صورت اتومات حالت هایی که جایگشت ندارند را حذف کنیم
        elif abs(a - b) == abs(i - j):
            return 1
        return 0


    #حالت رندوم اولیه ای را تولید میکند
    def SetQueens(self, n):
        #self.queens = [random.randrange(0, n) for i in range(n)] #استاندارد

        self.Permutataion(n)#جایگشت


    def Permutataion(self,n):# با استفاده از تابع رندوم و یک لیست از اعداد صفر تا n تولید حالت جایگشت میکند
        numbers = [i for i in range(n)]
        x = []

        for i in range(n):
            x.append(random.choice(numbers))
            numbers.remove(x[-1])

        self.queens = deepcopy(x)

    #مقادیر مربوط به کوییز را ست میکند(برای جلوگیری از به وجود آمدن مشکل در حالات اولیه نوشته شده است)
    def Mediator(self):
        if self.queens==[]:
            self.SetQueens(queensNumber)
        self.Cost()



'''genetic algorithm'''

def Pop(n): # تولید جمعیت n نفری به صورت رندوم
    list_queens = []
    for i in range(n):
        list_queens.append(Queens())
    return list_queens

def Select_normal(population, percentage):#تابع انتخاب چرخ رولت استاندارد که جمعیت که لیست افراد را رتبه بندی میکند و از رتبه ها به عنوان وزن برای تابع رندوم استفاده میکند
    sum = 0
    for q in population:
        sum += q.fitness
    indexes = []
    for q in population:
        indexes.append(q.fitness)
    indexes=sc.rankdata(indexes)#مرتب کردن بر اساس رتبه
    length = int(len(indexes) * percentage)
    selection = random.choices(population,weights=indexes,k=length)
    '''
    selection = []
    while len(selection) < length:
        index = np.argmax(indexes)
        selection.append(population[index])
        indexes.pop(index)#نخبه گرایی
    '''
    return selection


def Select_rouletwheel(population, percentage,alpha ,beta):#انتخاب چرخ رولت با استفاده از ضرایب الفا و بتا که بر اساس مینیمم فیتنس جمعیت وزن یا شانس هر فرد را مشخص میکند
    #alpha =20
    #beta =5
    #الفا و بتا باعث حل مشکل فشار انتخابی محو شونده و چیرگی میشوند
    minimum=Minimum_Fitness(population)


    indexes = []
    for q in population:
        if q.fitness > (beta * minimum):
            indexes.append(q.fitness+alpha)
            #indexes.append(q.fitness * alpha)  برای فیتنس های بالا تغییر زیادی ایجاد میکند و مناسب نیست
        else : indexes.append(q.fitness)
    #indexes=sc.rankdata(indexes)#مرتب کردن بر اساس رتبه
    length = int(len(indexes) * percentage)
    selection = random.choices(population,weights=indexes,k=length)
    return selection


def Select_tournament(population, percentage):#  انتخاب بر اساس رقابت k تایی
    new_population = []
    for i in range(len(population)):
        players = random.choices(population, k=int(percentage * len(population)))
        max=0
        for q in players:
            if q.fitness >= max:
                rnd = random.randrange(0, 100) / 100
                rnd_small = random.randrange(0, 100) / 100#با استفاده از این رندوم تورنومنت را دستکاری میکنیم تا در صورت نیاز افراد ضعیف تر به نسل بعد بروند و چیرگی کنترل شود
                if (q.fitness==max and rnd>0.5) or (q.fitness>max) or (rnd_small < 0.5):# با اعمال ضریب الفا و استفاده از تابع رندوم میتوانیم شانسی برای رفتن افراد با فیتنس کم به نسل بعد ایجاد کنیم
                    max=q.fitness
                    selection = q
        new_population.append(selection)
    return new_population


def Crossover(a,b):#کراس اور تک نقطه ای
    a_copy=deepcopy(a)
    b_copy=deepcopy(b)
    middle_point = len(a.queens) / 2
    i = 0
    while i < middle_point:
        a_copy.queens[i], b_copy.queens[i] = b_copy.queens[i], a_copy.queens[i]
        i += 1
    re=[a_copy,b_copy]
    return re


"کراس اور یکنواخت که در آن به صورت شانسی مشخص میشود کدام صفات به فرزندان منتقل شوند"
def Crossover2(a,b):
    i = 0
    a_copy = deepcopy(a)
    b_copy = deepcopy(b)
    while i < len(a.queens):
        rnd = random.randrange(0, 100) / 100
        if rnd>0.5:
            a_copy.queens[i], b_copy.queens[i] = b_copy.queens[i], a_copy.queens[i]
        i += 1
    re=[a_copy,b_copy]
    return re

"در کراس اور ترتیب استفاده میشود"
def Order(a,b):
    length = len(a.queens)
    a_copy = deepcopy(a)
    b_copy = deepcopy(b)
    child = Queens([None for i in range(length)])

    i = random.randrange(0, length)
    j = random.randrange(0, length)
    x=deepcopy(i)

    if i>j: i , j = j, i

    while i<=j:
        child.queens[i]=a_copy.queens[i]
        i+=1

    j=j+1
    z=deepcopy(j)
    while child.queens.__contains__(None):

        if z == length: z = 0
        if j == length: j = 0

        if not (child.queens.__contains__(b_copy.queens[j])) and child.queens[z]==None:
            child.queens[z]=b_copy.queens[j]
            z += 1

        j+=1

    return child

"کراس اور ترتیب که جایگشت را حفظ میکند"
def CrossoverOrder(a,b):
    re = [Order(a,b),Order(b,a)]
    return re

"در این تابع با استفاده از میانگین و انحراف معیار و  فیتنس هر فرد مشخص میکنیم که چگونه میتواند کراس اور داشته باشد و چند فرزند خواهد داشت ."
def Crossover_control(population,avg,avg_deviation):
    measure_1 = avg - avg_deviation
    measure_2 = avg + avg_deviation
    two_childs = []#لیست والد هایی که میتوانند دو فرزند تولید کنند
    one_childes = []#لیست والد هایی که میتوانند تنها یک فرزند تولید کنند
    no_childs = []#لیست والد هایی که نباید فرزندی تولید کنند (به علت فیتنس بسیار کم)
    new_population = []
    for q in population:
        if q.fitness < measure_2 and q.fitness > measure_1:
            one_childes.append(q)
        elif q.fitness > measure_2:
            two_childs.append(q)
        elif q.fitness < measure_1:
            no_childs.append(q)

    i=0
    length = len(one_childes)
    if length%2 !=0 : length-=1
    while i < (length):
        c = CrossoverOrder(one_childes[i], one_childes[i + 1])# به صورت پیش فرض از کراس اور ترتیب استفاده شده اما میتوان از دیگر حالات نیز استفاده نمود
        new_population.append(c[0])
        new_population.append(c[1])
        i += 2

    length = len(two_childs)
    if length % 2 != 0: length -= 1
    i = 0
    while i < (length):
        for j in range(2):
            c = CrossoverOrder(two_childs[i], two_childs[i + 1])
            new_population.append(c[0])
            new_population.append(c[1])
        i += 2

    #counter = len(new_population)-(len(two_childs)*2)-len(one_childes)
    counter = len(new_population) - len(population)
    if counter>0:
        for i in range(counter):
            new_population.pop(i)
    elif counter<0:
        i=0
        while len(new_population)!=len(population) and len(no_childs)>0:
            new_population.append(no_childs[i])
            i+=1
            if i==len(no_childs):
                i=0
                break
        while len(new_population)<len(population):
            new_population.append(one_childes[i])

"استاندارد"
def Mutate(person):
    person_copy=deepcopy(person)
    x = random.randrange(0, 100) / 100
    if x < 0.1:
        length = len(person_copy.queens)
        index = random.randrange(0, length)
        result = random.randrange(0, length)
        person_copy.queens[index] = result

    return person_copy


"تعویض"
def Mutate_replacement(person):
    person_copy = deepcopy(person)
    x = random.randrange(0, 100) / 100
    if x < 0.2:
        length = len(person.queens)
        index1=0
        index2=0
        while index1==index2:#برای اطمینان از مساوی نشدن ایندکس ها
            index1 = random.randrange(0, length)
            index2 = random.randrange(0, length)
        person_copy.queens[index1] , person_copy.queens[index2] = person_copy.queens[index2] , person_copy.queens[index1]

    return person_copy


" محسابه ی میانگین فیتنس یک جمعیت"
def AvgFitness(population):
    fitness=0
    for q in population:
        fitness+=q.fitness
    return fitness/len(population)


"پیدا کردن بهترین عضو یک جمعیت"
def Fittest(population):
    max=0
    for q in population:
        if q.fitness>max:
            max=q.fitness
    return max


"پیدا کردن بدترین فیتنس"
def Minimum_Fitness(population):
    #alpha = 80/100
    minimum = 9999999999
    for q in population:
        if q.fitness < minimum : minimum = q.fitness
    #for q in population:
    #    q.fitness = (alpha*q.fitness) - minimum
    return minimum


"بدست آوردن میانگین و انحراف معیار فیتنس های افراد یک نسل"
def avg_devi(population):
    avg = 0
    for q in population:
        avg += q.fitness
    avg = avg / len(population)
    avg_deviation = 0
    for q in population:
        avg_deviation += (q.fitness - avg) ** 2
    avg_deviation = avg_deviation / (len(population) - 1)
    avg_deviation = math.sqrt(avg_deviation)
    for q in population:
        q.fitness = q.fitness - avg + avg_deviation
    re=[avg,avg_deviation]
    return re


"""اپدیت کردن فیتنس کل جمعیت"""
def Evaluate(population):
    for q in population:
        q.Cost()
    #Minimum_Fitness(population)
    #avg_devi(population)
    '''
    avg = 0
    for q in population:
        avg+= q.fitness
    avg=avg/len(population)
    avg_deviation=0
    for q in population:
        avg_deviation+= (q.fitness - avg) ** 2
    avg_deviation = avg_deviation/(len(population)-1)
    avg_deviation = math.sqrt(avg_deviation)
    for q in population:
        q.fitness = q.fitness - avg + avg_deviation
    '''


"فهمیدن اینکه آیا یک فرد از حالت جایگشت حارج شده یا نه"
def Duplicates(person):
    p=deepcopy(person.queens)
    if len(p)!=len(set(p)):
        return True
    else :
        return False


"برگرداندن فرد به حالت جایگشت"
def Adjustment(person):
    p=deepcopy(person)
    n=len(p.queens)
    z=0
    while Duplicates(p):
        z+=1

        numbers = [i for i in range(n)]
        for i in p.queens:
            if numbers.__contains__(i): numbers.remove(i)

        for i in range(n):
            for j in range(i+1,n):
                if p.queens[i]==p.queens[j]:
                    rnd = random.randrange(0, 100) / 100
                    x = random.choice(numbers)
                    numbers.remove(x)
                    if rnd<0.5:
                        p.queens[i]= x
                    else :
                        p.queens[j] = x
    return deepcopy(p)


"جریمه ی فرد با کم کردن فیتنس آن به دلیل خارج شدن از حالت جایگشت"
def Penalty(person,rate):
    p = deepcopy(person)
    if Duplicates(person):
        p.fitness -= rate
    return p





"تعداد وزیر ها"
queensNumber=200
populations = []
def Genetic(population_number=500):
    #fitness_list = []

    g=0

    alpha = 10
    beta = 1.4

    p=Pop(population_number)

    #l=avg_devi(p)
    #avg = l[0]
    #avg_deviation = l[1]


    found_answer = False

    while found_answer==False and g!=100:
        g+=1

        "برای ایجاد میزانی برای کنترل انتخاب ها و دینامیک بودن آن با توجه به تغییر نسل استفاده میشود." \
        "برای مثال طوری مقدار دهی شوند که در نسل خای ابندایی رفتار شانسی را مشاهده کنیم اما هر چه به نسل های پایانی نزدیک تر  میشویم نخبه گرایی بیشتر شود"
        #alpha+=0.1
        #beta-=0.05

        pnew=[]
        "مکانیزم انتخاب"
        pnew = Select_rouletwheel(p, 1,alpha,beta)  # selection


        """crossover"""

        i=0
        while i<(population_number):
            rnd = random.randrange(0,100)/100
            if rnd<0.5:
                c=CrossoverOrder(pnew[i],pnew[i+1])
                pnew[i]=c[0]
                pnew[i+1]=c[1]
            i+=2


        #Crossover_control(pnew,avg,avg_deviation)

        "برگرداندن حالات خارج شده از جایگشت به حالت مطلوب بدون توجه به میوتیت شده ها "
        #for q in pnew:
         #   q=Adjustment(q)

        "مکانیزم جهش"
        for q in pnew:
            q=Mutate_replacement(q)

        "برگرداندن حالات خارج شده از جایگشت به حالت مطلوب با تاثیر بر روی میوتیت شده ها"
        #for q in pnew:
        #    q=Adjustment(q)


        p=deepcopy(pnew)

        "آپدیت کردن مقادیر فیتنس ها"
        Evaluate(p)

        "ایجاد پنالتی برای حالت های خارج شده از جایگشت"
        #for q in p:
        #    q = Penalty(q,5)

        #محاسبه ی میانگین فیتنس و بهترین فیتنس
        f=AvgFitness(p)
        bf=Fittest(p)

        "نمایشی نمودار و روند تغییر مسیر نسل ها " \
        "در ژوپیتر نوت بوک باز شود تا نمایش به درستی انجام شود"
        """display charts
        fitness_list.append(f)
        plt.plot(fitness_list, "rx")
        plt.xlabel("generation")
        plt.ylabel("avg fitness")
        plt.show()
        """

        '''using avg and avg_deviation'''
        #l = avg_devi(p)
        #avg = l[0]
        #avg_deviation = l[1]


        "بررسی اینکه به پاسخ رسیده ایم یا حیر"
        for q in p:
            if q.fitness==int((len(q.queens)*(len(q.queens)-1))/2):
                found_answer=True



        print(f"generation: {g} | Average fitness: {f} |  Best fitness: {bf}")
        print("***************************************************************")






#for i in range(10):
Genetic()
