import pdfplumber, os, glob, re

def extractRpa():
    files = glob.glob('./assets/rpa/*')
    for f in files:
        os.remove(f)
    with pdfplumber.open('./pdf/rpa.pdf') as pdf:
        for i, page in enumerate(pdf.pages):
            listOfNames = page.extract_table()[1]
            dirtNames = listOfNames[0].split('\n')
            
            arrayOfNames = dirtNames[1].split(' ')            
            
            list = arrayOfNames[1:-3]
            
            name = ' '.join(list)            
            
            top = 0
            bottom = page.height / 2.3
            left = 0
            right = page.width
            
            rpa = page.within_bbox((left, top, right, bottom))
            
            im = rpa.to_image(resolution=300)

            if os.path.isfile(f"./assets/rpa/{name}.png"):
                im.save(f"./assets/comprovantes/{name}-{i}.png", format="PNG")
            else:
                im.save(f"./assets/rpa/{name}.png", format="PNG")
    
    return True

if __name__ == "__main__":
    extractRpa()