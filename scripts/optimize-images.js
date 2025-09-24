const sharp = require('sharp');
const fs = require('fs-extra');
const path = require('path');

const inputImage = path.join(__dirname, '../src/church-image.jpg');
const outputDir = path.join(__dirname, '../src/assets/images/hero');

// Image sizes for different breakpoints
const sizes = [
    { width: 768, name: 'small' },
    { width: 1024, name: 'medium' },
    { width: 1536, name: 'large' },
    { width: 2048, name: 'xlarge' }
];

async function optimizeImages() {
    try {
        // Ensure output directory exists
        await fs.ensureDir(outputDir);

        // Process each size
        for (const size of sizes) {
            const image = sharp(inputImage);
            
            // Get image metadata
            const metadata = await image.metadata();
            const aspectRatio = metadata.width / metadata.height;
            
            // Calculate height maintaining aspect ratio
            const height = Math.round(size.width / aspectRatio);

            // Generate WebP version
            await image
                .resize(size.width, height, {
                    fit: 'cover',
                    withoutEnlargement: true
                })
                .webp({ quality: 80 })
                .toFile(path.join(outputDir, `church-hero-${size.name}.webp`));

            // Generate JPEG version
            await image
                .resize(size.width, height, {
                    fit: 'cover',
                    withoutEnlargement: true
                })
                .jpeg({ quality: 80, progressive: true })
                .toFile(path.join(outputDir, `church-hero-${size.name}.jpg`));
        }

        console.log('Image optimization complete!');
    } catch (error) {
        console.error('Error optimizing images:', error);
    }
}

optimizeImages();