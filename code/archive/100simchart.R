library(ggplot2)
library(dplyr)
library(ggthemes)
library(extrafont)
library(readr)
library(plotly)
library(htmlwidgets)

set.seed(1995)
y <- round(rnorm(50), 1)

df <- data.frame(y = y,
                 group = rep("G1",50),
                 party = sample(c("Lab","Col"),size=50,replace=TRUE))

swarm <- ggplot(df, aes(x = group, y = y,color=party)) +
  geom_beeswarm(cex = 10,size = 7,priority = "density")+
  scale_fill_manual(values=c("Lab" ="#000000",
                             "Col" = "#ffffff"))+ 
  #theme(legend.position="none")+ 
  coord_flip()+
  labs(y = "Primary Vote %")+
  theme(axis.title.y = element_blank(),
        axis.text.y = element_blank(),
        axis.title.x = element_text(size = 20),
        legend.position="none",
        panel.border = element_blank(), 
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(), 
        axis.line = element_blank(),
        panel.background = element_rect(fill = "transparent"), # bg of the panel
        plot.background = element_rect(fill = "transparent", color = NA), # bg of the plot
        legend.background = element_rect(fill = "transparent"), # get rid of legend bg
        legend.box.background = element_rect(fill = "transparent")
        
        )
ggsave(swarm, filename = "SwarmChart.png",  bg = "transparent")