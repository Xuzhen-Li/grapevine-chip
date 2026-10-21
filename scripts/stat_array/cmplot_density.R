library(CMplot)
mydata<-read.table("postion_all_id_sort.tsv",header=TRUE,sep="\t")
head(mydata)
my_breaks <- c(0, 1, 2, 3, 5, 10, 20) 
CMplot(mydata,type="p",plot.type="d",bin.size=1e4,bin.breaks=my_breaks,chr.den.col=c("#e6d30aff", "#654009ff" ,"#ff0000"),file="jpg",dpi=300, main="SNP array",file.output=TRUE,verbose=TRUE,width=9,height=6)

