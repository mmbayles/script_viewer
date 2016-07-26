library(XML)
library(resample)
#Problem # 1
#Membership in southern states
#states pop

lds_southern <- read.table(header=TRUE, text='
pop
36255 
29345
146509
81563
33757
29682
21699
81189
39473
48612
93395
  ')
mean(lds_southern$pop)
var(lds_southern$pop)
sd(lds_southern$pop)


#Problem # 2
lds_Midwest <- read.table(header=TRUE, text='
pop
57080
43614
27131
36377
43478
32030
69451
24357
11017
60810
10875
25871

                  ')
mean(lds_Midwest$pop)
var(lds_Midwest$pop)
sd(lds_Midwest$pop)

#Problem 3
boxplot(lds_southern$pop,lds_Midwest$pop,xlab = "Region of the United States", ylab = "LDS Population",col = c("red","blue"), names = c("Southern States","Western States"))
median(lds_southern$pop)
median(lds_Midwest$pop)


#Problem 6
body_temp <- read.table(header=TRUE, text='
Temp
99.2
97.4
98.5
97.1
97.0
97.8
97.5
98.6
98.0
99.0
98.0
98.6
97.4
98.4
98.6
97.8
97.8
98.0
98.6
97.9
97.5
97.6
97.7
98.4
99.4
                          
')
boxplot(body_temp, xlab = "Body Temps of Men", ylab = "Body temp in degrees F")
#Part B
mean(body_temp$Temp)
sd(body_temp$Temp)
#Part C
t.test(body_temp$Temp)
#Part D
t.test(body_temp$Temp,mu = 98.6)

#Problem 7
# Movie ROI
# DATA:
# R library to read HTML files
library(XML)
setClass("AccountingNumber")
setAs("character", "AccountingNumber", 
      function(from) as.numeric(gsub(",", "", gsub("[:$:]", "", from) ) ) )
# web scraper for data
#  webpage with data table
movies.url<-"http://www.the-numbers.com/movie/budgets/all"
#  read webpage and store in memory
movies.webpage<-htmlParse(movies.url)
#  create R dataset from webpage contents
movies<-readHTMLTable(movies.webpage,
                      which=1,skip.rows=1,stringsAsFactors = FALSE,header=F,
                      colClasses=c("numeric","character","character",rep("AccountingNumber",3)))
names(movies)<-c("rank","rel.date","title","prod.budget","domestic","worldwide")
movies<-movies[!is.na(movies$title),]
# change units to $ millions
movies$prod.budget<-movies$prod.budget/10^6
movies$domestic<-movies$domestic/10^6
movies$worldwide<-movies$worldwide/10^6
# remove movies currently in distribution (gross=0)
movies<-movies[movies$domestic>0,]
# create rel.year (the year the movie was released)
# and subset to movies since 2007
movies$rel.year<-substr(movies$rel.date,nchar(movies$rel.date)-3,nchar(movies$rel.date))
movies<-subset(movies,rel.year>=2007 & rel.year<2015)


#My Code
#Part A
movies$roi = 100*((movies$domestic-movies$prod.budget)/movies$prod.budget)
#Part B
boxplot(movies$roi,xlab= "Movies", ylab= "ROI")

#Part c
dim(movies)

mean(movies$prod.budget)
mean(movies$domestic)
mean(movies$roi)

sd(movies$prod.budget)
sd(movies$domestic)
sd(movies$roi)

median(movies$prod.budget)
median(movies$domestic)
median(movies$roi)


quantile(movies$prod.budget,.75)
quantile(movies$domestic,.75)
quantile(movies$roi,.75)

quantile(movies$prod.budget,.99)
quantile(movies$domestic,.99)
quantile(movies$roi,.99)
#Part D
roi.out = bootstrap(movies$roi, median)
CI.t(roi.out)
