# Please note: While I was able to find these constants within the source code, on my system (using LibreOffice,) I was only presented with a solid line, varying from thin to thick; no dotted or dashed lines.
import xlwt

def writeToExcel(ctsVersion, deviceFingerPrint, failedCases):
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet('FailResult')
    rowCount = 0
    #set the column width
    worksheet.col(1).width = 10000
    worksheet.col(2).width = 10000
    #wirte cts version ,deviceFingerPrint and total failed case
    worksheet.write_merge(rowCount,rowCount,0,2,deviceFingerPrint,getStyle(isBold=True,alignemnt=xlwt.Alignment.HORZ_CENTER,color=5))
    rowCount += 1
    worksheet.write_merge(rowCount,rowCount,0,2,"CTS Version: "+ctsVersion,getStyle(isBold=False,alignemnt=xlwt.Alignment.HORZ_RIGHT,color=5))
    rowCount += 1
    worksheet.write_merge(rowCount,rowCount,0,2,"Total Failed Cases: "+ str(len(failedCases)),getStyle(isBold=False,alignemnt=xlwt.Alignment.HORZ_RIGHT,color=5))
    rowCount += 1

    #write all failed cases
    for key in failedCases:
        worksheet.write_merge(rowCount,rowCount,0,2,key,getStyle(isBold=True,alignemnt=xlwt.Alignment.HORZ_LEFT,color=7))
        rowCount += 1
        for caseName in failedCases[key]:
            worksheet.write(rowCount,1,caseName)
            rowCount += 1


    workbook.save('Excel_Workbook.xls')

def getStyle(isBold,alignemnt,color):

    #alignment
    mAlignment = xlwt.Alignment()
    mAlignment.horz = alignemnt

    #background color
    mPattern = xlwt.Pattern()
    mPattern.pattern = xlwt.Pattern.SOLID_PATTERN
    mPattern.pattern_fore_colour = color

    #Font style
    mFont = xlwt.Font()
    mFont.bold = isBold

    #cell border line
    borders = xlwt.Borders()  # Create Borders
    borders.left = xlwt.Borders.MEDIUM_DASHED  # May be: NO_LINE, THIN, MEDIUM, DASHED, DOTTED, THICK, DOUBLE, HAIR, MEDIUM_DASHED, THIN_DASH_DOTTED, MEDIUM_DASH_DOTTED, THIN_DASH_DOT_DOTTED, MEDIUM_DASH_DOT_DOTTED, SLANTED_MEDIUM_DASH_DOTTED, or 0x00 through 0x0D.
    borders.right = xlwt.Borders.MEDIUM_DASHED
    borders.top = xlwt.Borders.MEDIUM_DASHED
    borders.bottom = xlwt.Borders.MEDIUM_DASHED
    borders.left_colour = 0x100
    borders.right_colour = 0x80
    borders.top_colour = 0x50
    borders.bottom_colour = 0x3a

    style = xlwt.XFStyle()
    style.font = mFont
    style.pattern = mPattern
    style.alignment = mAlignment
    style.border = borders

    return style


