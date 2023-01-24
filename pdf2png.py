from pdf2image import convert_from_path, convert_from_bytes

images = convert_from_path('./template.pdf', size=3000, dpi=400)[0]
images.save('template.png', 'PNG')
