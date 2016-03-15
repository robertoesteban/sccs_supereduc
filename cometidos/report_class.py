from reportlab.pdfgen import canvas
from reportlab.lib.units import cm, inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize

class CjReport(object):
	CMI_INDEX = {}
	PAGE_HEIGHT = defaultPageSize[1]
	PAGE_WIDTH = defaultPageSize[0]
	styles = getSampleStyleSheet()

	Title = "Solicitud de Cometidos"
	pageinfo = "SuperIntendecia de Educacion"

	c = canvas.Canvas("Report.pdf")
	c.translate(cm,cm)
	c.setFont("Helvetica", 14)


	def addHeader(self, main_header):
		self.c.setStrokeColorRGB(0.2,0.5,0.3)
		self.c.setFillColorRGB(1,0,1)
		self.c.setLineWidth(4)
		self.c.setFont("Helvetica", 20)
		self.c.drawString(10*cm,27.5*cm,main_header)
		self.c.line(0.3*cm,27*cm,19*cm,27*cm)

	def addFooter(self, main_footer):
		self.c.setStrokeColorRGB(0.2,0.5,0.3)
		self.c.setFillColorRGB(1,0,1)
		self.c.setFont("Helvetica", 5)
		self.c.line(0.3*cm,0.8*cm,19*cm,0.8*cm)
		self.c.drawString(10*cm,0.5*cm,main_footer)

	def setCoverPage(self, left_margin):
		self.addHeader("Roberto Sanchez")
		self.c.setFillColorRGB(1,0,0)
		self.c.setFont("Helvetica", 30)
		self.c.drawString(left_margin * cm, 25*cm, "Carrer Profiling Report")
		self.c.setFont("Helvetica-Bold", 10)
		self.c.setFillColorRGB(0,0,1)
		self.c.drawString(left_margin * cm, 24*cm, "Preparado por Roberto Sanchez")
                self.c.setFillColorRGB(0,0,0)
		self.c.drawString(left_margin * cm, 23.5*cm, "Chief Consultant and ....")
                self.c.setFillColorRGB(0,0,1)
		self.c.drawString(left_margin * cm, 23*cm, "Centro de Desarrollo")
                self.c.setFillColorRGB(0,0,0)
		self.c.drawString(left_margin * cm, 22.5*cm, "Fecha (Insert)")
		
		self.c.setStrokeColorRGB(0.2,0.5,0.3)
		self.c.setFillColorRGB(0,1,0)
		self.c.line(0.3*cm,22*cm,19*cm,22*cm)
                self.c.setFillColorRGB(0,0,0)
		self.c.drawString(left_margin * cm, 21*cm, "identificacion Confirmada")
		self.c.setFont("Times-Italic",10)
		self.c.drawString(left_margin * cm, 20.5*cm, "Por favor verifique datos del personal")
                self.c.setFillColorRGB(0,0,0)
		self.c.setFont("Helvetica-Bold",10)
		self.c.drawString(left_margin * cm, 20*cm, "Name: (Insert)")
		self.c.drawString(left_margin * cm, 19.5*cm, "Age: (Insert)")
		self.c.drawString(left_margin * cm, 19*cm, "Gender: (Insert)")
		self.c.drawString(left_margin * cm, 18.5*cm, "Occupation: (Insert)")
		self.c.drawString(left_margin * cm, 18*cm, "education: (Insert)")
		self.c.drawString(left_margin * cm, 17.5*cm, "Location: (Insert)")


	def generate(self):
		self.c.showPage()
		self.c.save()
		return self
