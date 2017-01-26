# DomWorld import script. Do not edit
# Source me in the directory of the *.csv files!

Runs <- list()
for (r in 1:5) {
    Runs <- rbind(Runs, read.csv(paste0("No_oestrus", r, ".csv"), sep="\t", header=TRUE))
}
