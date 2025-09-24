Add-Type -AssemblyName System.Drawing

# Source and destination paths
$sourcePath = "src\church-image.jpg"
$heroDir = "src\assets\images\hero"

# Create directory if it doesn't exist
if (-not (Test-Path $heroDir)) {
    New-Item -ItemType Directory -Path $heroDir -Force
}

# Copy original image
Copy-Item $sourcePath "$heroDir\church-hero.jpg" -Force

# Load the image
$image = [System.Drawing.Image]::FromFile((Resolve-Path $sourcePath))

# Calculate mobile dimensions (max width 768px)
$mobileWidth = [Math]::Min(768, $image.Width)
$mobileHeight = [int]($image.Height * ($mobileWidth / $image.Width))

# Create mobile version
$mobileBitmap = New-Object System.Drawing.Bitmap($mobileWidth, $mobileHeight)
$graphics = [System.Drawing.Graphics]::FromImage($mobileBitmap)
$graphics.DrawImage($image, 0, 0, $mobileWidth, $mobileHeight)

# Save mobile version
$mobileBitmap.Save("$heroDir\church-hero-mobile.jpg", [System.Drawing.Imaging.ImageFormat]::Jpeg)

# Cleanup
$graphics.Dispose()
$mobileBitmap.Dispose()
$image.Dispose()

Write-Host "Images processed successfully!"
Write-Host "Original image copied to: $heroDir\church-hero.jpg"
Write-Host "Mobile version saved to: $heroDir\church-hero-mobile.jpg"