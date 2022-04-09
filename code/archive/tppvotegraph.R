library(ggplot2)
library(dplyr)
library(ggthemes)
library(extrafont)
library(readr)
library(plotly)

theme_set(theme_bw())
dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(dir = dir)
tppvote <- data.frame(
  party = c("Labor", "Coalition"),
  tpp = c(53,47)
)

head(tppvote)


tppvote.plot <- ggplot(tppvote, aes(x = reorder(party,-tpp), 
                                            y = tpp,
                                            text=paste0("Party:",party,"\nExpected TPP ",tpp,"%")))+
  geom_col(aes(fill = party), width = 0.7)+
  scale_fill_manual(values=c("Labor" ="#c20000",
                             "Coalition" = "#003db8"))+ 
  #theme(legend.position="none")+ 
  labs(y = "TPP %")+
  theme(axis.title.x = element_blank(),
        axis.title.y = element_text(size = 20),
        axis.text.x = element_text(size = 20),
        legend.position="none",panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black")) 

font = list(
  family = "DM Sans",
  size = 15,
  color = "white"
)
label = list(
  bordercolor = "transparent",
  font = font
  
)


tppvote.plotly = ggplotly(tppvote.plot, tooltip=c("text")) %>%
  style(hoverlabel = label) %>%
  layout(font = font,
         yaxis = list(fixedrange=TRUE),
         xaxis = list(fixedrange=TRUE)) %>%
  config(displayModeBar = FALSE,showTips=FALSE)

saveWidget(tppvote.plotly,file ="TPPVoteTable.html")