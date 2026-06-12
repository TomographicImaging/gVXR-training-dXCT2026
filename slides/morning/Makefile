DOCS=gVXR.html \
	gVXR.docx

PANDOC=pandoc -V lang=en-gb
all: ${DOCS}

#%.md: %pptx
#	pptx2md -o $@ $< --disable_wmf

%.pptx: %.md
	${PANDOC} -s $< -o $@ #--reference-doc theme.pptx

%.html: %.md
	#${PANDOC} -t  slidy -s $(<F) -o $(@F)
	#${PANDOC} -t  slideous -s $(<F) -o $(@F)
	#${PANDOC} -t  dzslides -s $< -o $@
	cd $(<D) ; ${PANDOC} --mathjax --template template.slidy -t  slidy --css=./custom.css -s $(<F) -o $(@F)

%.pdf: %.html
	# ${PANDOC} -t  beamer -s $< -o $@
	#${PANDOC} -t context -s $< -o $@
	cd $(<D) ; ${PANDOC} --pdf-engine=xelatex  -t  beamer --toc  -s $(<F) -o $(@F)
# 	cd $(<D) ; google-chrome --headless --print-to-pdf=$(@F) $(<F)
# 		#${PANDOC} \
# 		#-N \
# 		#--template=${PWD}/template.tex \
# 		#--variable fontsize=12pt \
# 		#--variable version=2.0 \
# 		#-s $(<F) --pdf-engine=xelatex  --toc -o $(@F)


%.docx: %.md
	cd $(<D) ; ${PANDOC} -t docx  -s $(<F) -o $(@F)

%.pptx: %.md
	cd $(<D) ; ${PANDOC} -t pptx  -s $(<F) -o $(@F)

clean:
	${RM} ${DOCS}
