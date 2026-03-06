from fpdf import FPDF

def create_journal_pdf(text, sentiment):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Moodie Journal Entry", ln=True, align='C')
    
    # Date & Sentiment
    pdf.set_font("Arial", size=12)
    pdf.ln(10)
    pdf.cell(200, 10, txt=f"Detected Mood: {sentiment}", ln=True)
    
    # The Content
    pdf.ln(5)
    pdf.multi_cell(0, 10, txt=f"Journal Text: {text}")
    
    # Save it to a temporary location
    file_path = "latest_entry.pdf"
    pdf.output(file_path)
    return file_path