library(ggplot2)
library(dplyr)
library(ggthemes)
library(extrafont)
library(readr)
library(plotly)
library(htmlwidgets)

theme_set(theme_bw())
dir <- dirname(rstudioapi::getSourceEditorContext()$path)
setwd(dir = dir)
primaryvote <- data.frame(
  party = c("Labor", "Coalition", "Greens","One Nation","Others"),
  primary = c(36,36,10,4,14)
)

#df <- within(df,
#             party <- factor(party,
#                             levels = names(sort(table(party),
#                                                 decreasing=TRUE))))

head(primaryvote)


primaryvote.plot <- ggplot(primaryvote, aes(x = reorder(party,primary), 
                                   y = primary,
                                   text=paste0("Party:",party,"\nExpected Primary Vote:",primary,"%")))+
  geom_col(aes(fill = party), width = 0.7)+
  scale_fill_manual(values=c("Labor" ="#c20000",
                             "Coalition" = "#003db8",
                             "Greens" = "#008f24",
                             "One Nation" ="#E69F00", 
                             "Others" ="#999999"))+ 
  #theme(legend.position="none")+ 
  coord_flip()+
  labs(y = "Primary Vote %")+
  theme(axis.title.y = element_blank(),
        axis.title.x = element_text(size = 20),
        axis.text.y = element_text(size = 20),
        legend.position="none",panel.border = element_blank(), panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), axis.line = element_line(colour = "black"),
        panel.background = element_rect(fill = "transparent"), # bg of the panel
        plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
        legend.background = element_rect(fill = "transparent"), # get rid of legend bg
        legend.box.background = element_rect(fill = "transparent")) 

font = list(
  family = "DM Sans",
  size = 15,
  color = "white"
)
label = list(
  bordercolor = "transparent",
  font = font
  
)

primaryvote.plotly = ggplotly(primaryvote.plot, tooltip=c("text")) %>%
  style(hoverlabel = label) %>%
  layout(font = font,
         yaxis = list(fixedrange=TRUE),
         xaxis = list(fixedrange=TRUE)) %>%
  layout(plot_bgcolor='rgba(0, 0, 0,0)') %>% 
  layout(paper_bgcolor='rgba(0, 0, 0,0)')%>%
  layout(coloraxis   = "rgba(0, 0, 0, 0)")%>%
  config(displayModeBar = FALSE,showTips=FALSE)

saveWidget(primaryvote.plotly,file ="PrimaryVoteTable.html")