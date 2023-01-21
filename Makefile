config: config.yml preamble.tex
	`which python3` conf2tex.py config.yml template.tex
	pdflatex template.tex

template: template.tex
	pdflatex template.tex

tex: ${var}.tex
	pdflatex ${var}.tex

clean:
	rm *.aux *.log *.out
