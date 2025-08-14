import pdfplumber, os, glob
from PyPDF2 import PdfWriter, PdfReader

def extractComprovante():
    

    files = glob.glob('./assets/comprovantes/*')
    for f in files:
        os.remove(f)
        
    inputPDFFile = PdfReader(open(rf'./pdf/comprovantes.pdf', "rb"))
    

    with pdfplumber.open('./pdf/comprovantes.pdf') as pdf:
        for i, page in enumerate(pdf.pages):
            
            output = PdfWriter()
            output.add_page(inputPDFFile.pages[i])
            
            pdfText = page.extract_text()
            splitFirstText = pdfText.splitlines()        
            matchesFirstText = [match for match in splitFirstText if "Conta:" in match]
            
            fileName = ''
            
            if(len(matchesFirstText)):
                name = matchesFirstText[1].split('/')[1]
                
                fileName = name
                
            if os.path.isfile(f"./assets/comprovantes/{fileName}.pdf"):
                with open(f"./assets/comprovantes/%s-%s.pdf" % (fileName, i), "wb") as outputStream:
                    output.write(outputStream)
            else:    
                with open(f"./assets/comprovantes/%s.pdf" % fileName, "wb") as outputStream:
                    output.write(outputStream)

    
    return True

if __name__ == "__main__":
    extractComprovante()
