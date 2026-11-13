$docx_path = "C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\Industrial_Training_Report.docx"
$pdf_path = "C:\Users\chitr_mzkaj0t\.gemini\antigravity\scratch\workforce_intelligence\reports\internship_submission\Industrial_Training_Report.pdf"

Write-Host "Converting DOCX to PDF..."
try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($docx_path)
    $doc.SaveAs([ref]$pdf_path, [ref]17)
    $doc.Close()
    $word.Quit()
    Write-Host "SUCCESS: Converted to PDF -> $pdf_path"
} catch {
    Write-Host "ERROR converting Word: $($_.Exception.Message)"
}
