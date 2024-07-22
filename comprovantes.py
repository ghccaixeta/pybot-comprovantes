import pdfplumber, os, glob

def extractComprovante():
    

    files = glob.glob('./assets/comprovantes/*')
    for f in files:
        os.remove(f)

    with pdfplumber.open('./pdf/comprovantes.pdf') as pdf:
        for i, page in enumerate(pdf.pages):
            
            top = 0
            bottom = page.height / 3.4
            left = 0
            right = page.width
            
            rpa = page.within_bbox((left, top, right, bottom))
            firstText = page.crop((left, top, right, bottom)).extract_text()
            splitFirstText = firstText.splitlines()        
            matchesFirstText = [match for match in splitFirstText if "Conta:" in match] 
            if(len(matchesFirstText)):
                nameOfFirstFile = matchesFirstText[1].split('/')[1]

            top = page.height / 3.4
            bottom = page.height

            rpa2 = page.within_bbox((left, top, right, bottom))
            secondText = page.crop((left, top, right, bottom)).extract_text()
            splitSecondText = secondText.splitlines()
            matchesSecondText = [match for match in splitSecondText if "Conta:" in match]
            if(len(matchesSecondText)):
                nameOfSecondFile = matchesSecondText[1].split('/')[1]
            
            im = rpa.to_image(resolution=300)
            im2 = rpa2.to_image(resolution=300)
            
            im.save(f"./assets/comprovantes/{nameOfFirstFile}.png", format="PNG")
            im2.save(f"./assets/comprovantes/{nameOfSecondFile}.png", format="PNG")
    
    return True

if __name__ == "__main__":
    extractComprovante()