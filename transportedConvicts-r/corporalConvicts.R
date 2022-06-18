install.packages('tidyverse')
install.packages('tidytext')
install.packages('dplyr')
install.packages("slam")
install.packages("topicmodels")
install.packages("reshape2")
install.packages("ggplot2")
install.packages("pals")

# libraries
library(tidyverse)
library(tidytext)
library("dplyr")
library(tm)
library(topicmodels)
library("reshape2")
library("ggplot2")
library("pals")



# load, clean, and get data into shape

cc  <- read_csv('corporalConvicts.csv')

#cc_df <- cc_df %>% mutate(id = row_number())

cc_df <- tibble(id = cc$id, text = (str_remove_all(cc$trialText, "[0-9]")), date = cc$crimeDate)

tidy_cc <- cc_df %>%
  unnest_tokens(word, text)

data(stop_words)

tidy_cc <- tidy_cc %>%
  anti_join(stop_words)

cc_words <- tidy_cc %>%
  count(id, word, sort = TRUE)

head(cc_words)

dtm <- cc_words %>%
  cast_dtm(id, word, n)

require(topicmodels)
# number of topics
K <- 5
# set random number generator seed
# for purposes of reproducibility
set.seed(9161)
# compute the LDA model, inference via 1000 iterations of Gibbs sampling
topicModel <- LDA(dtm, K, method="Gibbs", control=list(iter = 500, verbose = 25))

# have a look a some of the results (posterior distributions)
tmResult <- posterior(topicModel)

# format of the resulting object
attributes(tmResult)

# lengthOfVocab
ncol(dtm)

beta <- tmResult$terms   # get beta from results
dim(beta)

theta <- tmResult$topics
dim(theta) 

top5termsPerTopic <- terms(topicModel, 3)
topicNames <- apply(top5termsPerTopic, 2, paste, collapse=" ")
topicNames

exampleIds <- c(2, 10, 20)

N <- length(exampleIds)
# get topic proportions form example documents
topicProportionExamples <- theta[exampleIds,]
colnames(topicProportionExamples) <- topicNames

# put the data into a dataframe just for our visualization
vizDataFrame <- melt(cbind(data.frame(topicProportionExamples), document = factor(1:N)), variable.name = "topic", id.vars = "document") 

ggplot(data = vizDataFrame, aes(topic, value, fill = document), ylab = "proportion") +
  geom_bar(stat="identity") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1)) +  
  coord_flip() +
  facet_wrap(~ document, ncol = N)

#topics over time
# append decade information for aggregation
cc$decade <- paste0(substr(cc$crimeDate, 0, 3), "0")

# get mean topic proportions per decade
topic_proportion_per_decade <- aggregate(theta, by = list(decade = cc$decade), mean)
# set topic names to aggregated columns
colnames(topic_proportion_per_decade)[2:(K+1)] <- topicNames

vizDataFrame <- melt(topic_proportion_per_decade, id.vars = "decade")

require(pals)

ggplot(vizDataFrame, aes(x=decade, y=value, fill=variable)) +
  geom_bar(stat = "identity") + ylab("proportion") +
  scale_fill_manual(values = paste0(alphabet(20), "FF"), name = "decade") +
  theme(axis.text.x = element_text(angle = 90, hjust = 1))

