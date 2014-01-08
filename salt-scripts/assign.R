assignments_csv <- "aments.csv"
as <- read.csv(assignments_csv, header=FALSE)
colnames(as) <- 3:250

assignments <- function() {
  boxes <- matrix(0, nrow=4, ncol=248, dimnames=list(c(),3:250))
  counter <- 1
  for (colname in colnames(as)) {
    # have to do some hideous surgery to make the alphabetical order of
    # reviewers in the spreadsheet match the alphabetical order of reviewers
    # in easychair (differences in diacritics and initials)
    col <- as.character(as[[colname]])
    Saebo <- col[165]
    Sassoon <- col[166]
    preCB <- col[1:12]
    preDB <- col[13:19]
    preLCSC <- col[20:26]
    preSM <- col[27:123]
    preOldSaebo <- col[124:164]
    prePS <- col[167:168]
    preAS <- col[169:189]   
    preNewSassoon <- col[190:199]
    final <- col[200:218]
    col <- c(preCB, "", preDB, "", preLCSC, "", "", preSM, "", preOldSaebo,
             prePS, "", preAS, "", Saebo, preNewSassoon, Sassoon, final)
    reviewers <- which(!(col %in% c(NA, "", "Q")))
    reviewers <- c(reviewers, rep(0, 4))[1:4]
    boxes[,counter] <- reviewers
    counter = counter + 1
  }
  return(boxes)
}
