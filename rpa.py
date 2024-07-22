import pdfplumber, os, glob

def extractRpa():
    files = glob.glob('./assets/rpa/*')
    for f in files:
        os.remove(f)
    with pdfplumber.open('./pdf/rpa.pdf') as pdf:
        for i, page in enumerate(pdf.pages):
            listOfNames = page.extract_table()[8]
            dirtNames = listOfNames[0].split('INSS')
            name = dirtNames[0].split(':')[1].replace('\n','').replace('Nº','')
            
            top = 0
            bottom = page.height / 1.7
            left = 0
            right = page.width
            
            rpa = page.within_bbox((left, top, right, bottom))
            
            im = rpa.to_image(resolution=300)
            
            im.save(f"./assets/rpa/{name}.png", format="PNG")
    
    return True

if __name__ == "__main__":
    extractRpa()