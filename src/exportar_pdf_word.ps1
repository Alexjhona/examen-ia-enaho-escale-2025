# Requiere Microsoft Word en Windows. Exporta el DOCX final, sin modificarlo.
$raizProyectoIA = Split-Path -Parent $PSScriptRoot
$wordEntregaIA = New-Object -ComObject Word.Application
$wordEntregaIA.Visible = $false
$wordEntregaIA.DisplayAlerts = 0
try {
    $docEntregaIA = $wordEntregaIA.Documents.Open((Join-Path $raizProyectoIA 'Articulo_Cientifico_IA.docx'), $false, $true)
    $docEntregaIA.ExportAsFixedFormat((Join-Path $raizProyectoIA 'Articulo_Cientifico_IA.pdf'), 17)
    Write-Output ('Páginas: ' + $docEntregaIA.ComputeStatistics(2))
    $docEntregaIA.Close(0)
} finally { $wordEntregaIA.Quit() }
