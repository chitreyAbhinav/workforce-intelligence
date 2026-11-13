$pptx_path = "C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\Industrial_Training_Presentation.pptx"
$pdf_path = "C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\Industrial_Training_Presentation.pdf"

Write-Host "Converting PPTX to PDF..."
try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($pptx_path, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse, [Microsoft.Office.Core.MsoTriState]::msoFalse)
    # ppSaveAsPDF = 32
    $pres.SaveAs($pdf_path, 32)
    $pres.Close()
    $ppt.Quit()
    Write-Host "SUCCESS: PPTX Converted to PDF -> $pdf_path"
} catch {
    Write-Host "ERROR converting PPT: $($_.Exception.Message)"
}
