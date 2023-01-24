build: config.yml preamble.tex template.tex
	`which python3` conf2tex.py config.yml template.tex
	pdflatex template.tex
	`which python3` pdf2png.py

template: template.tex
	pdflatex template.tex

tex: ${var}.tex
	pdflatex ${var}.tex

clean:
	rm *.aux *.log *.out
