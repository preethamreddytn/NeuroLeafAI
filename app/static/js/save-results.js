// Save Results as Text-Based PDF (not image-based)
document.addEventListener('DOMContentLoaded', function() {
    const perCardButtons = document.querySelectorAll('.save-result-btn');
    const saveAllBtn = document.getElementById('save-all-results-btn');

    // Extract text content from a result card
    function extractResultData(card) {
        const fileName = card.querySelector('h4')?.textContent?.trim() || 'Unknown Image';
        const diseaseName = card.querySelector('.disease-name')?.textContent?.trim() || 'Not detected';
        const symptoms = Array.from(card.querySelectorAll('.symptoms-list li')).map(li => li.textContent.trim());
        const treatments = Array.from(card.querySelectorAll('.treatment-list li')).map(li => li.textContent.trim());
        const confidence = card.querySelector('.progress-fill')?.textContent?.trim() || '0%';
        const imgElement = card.querySelector('.image-container img');
        const imageData = imgElement ? imgElement.src : null;
        
        return { fileName, diseaseName, symptoms, treatments, confidence, imageData };
    }

    // Generate a text-based PDF for a single result (with image)
    async function generateTextPdf(resultData, fileName) {
        const { jsPDF } = window.jspdf;
        const pdf = new jsPDF('p', 'mm', 'a4');
        const pageWidth = pdf.internal.pageSize.getWidth();
        const pageHeight = pdf.internal.pageSize.getHeight();
        const margin = 15;
        const contentWidth = pageWidth - (2 * margin);
        let yPosition = margin;

        // Header with title
        pdf.setFillColor(46, 125, 50);
        pdf.rect(0, 0, pageWidth, 25, 'F');
        pdf.setTextColor(255, 255, 255);
        pdf.setFontSize(18);
        pdf.setFont(undefined, 'bold');
        pdf.text('BioAgriCure', margin, 12);
        pdf.setFontSize(11);
        pdf.setFont(undefined, 'normal');
        pdf.text('Plant Disease Detection Report', margin, 20);
        
        yPosition = 35;

        // Add plant image if available
        if (resultData.imageData) {
            try {
                const imgWidth = 80;
                const imgHeight = 80;
                const imgX = (pageWidth - imgWidth) / 2;
                pdf.addImage(resultData.imageData, 'JPEG', imgX, yPosition, imgWidth, imgHeight);
                yPosition += imgHeight + 10;
            } catch (err) {
                console.warn('Could not add image to PDF:', err);
                yPosition += 10;
            }
        }

        // Image filename and date
        pdf.setTextColor(100, 100, 100);
        pdf.setFontSize(10);
        pdf.text(`Image: ${resultData.fileName}`, margin, yPosition);
        yPosition += 6;
        pdf.text(`Generated: ${new Date().toLocaleString()}`, margin, yPosition);
        yPosition += 12;

        // Disease Detection Section
        pdf.setTextColor(0, 0, 0);
        pdf.setFontSize(13);
        pdf.setFont(undefined, 'bold');
        pdf.text('Detected Disease:', margin, yPosition);
        yPosition += 8;

        pdf.setFontSize(14);
        pdf.setTextColor(46, 125, 50);
        pdf.text(resultData.diseaseName, margin, yPosition);
        yPosition += 10;

        // Confidence Score
        pdf.setTextColor(0, 0, 0);
        pdf.setFontSize(11);
        pdf.setFont(undefined, 'bold');
        pdf.text(`Confidence Score: ${resultData.confidence}`, margin, yPosition);
        yPosition += 10;

        // Symptoms Section
        pdf.setFontSize(12);
        pdf.setFont(undefined, 'bold');
        pdf.setTextColor(46, 125, 50);
        pdf.text('Symptoms:', margin, yPosition);
        yPosition += 7;

        pdf.setFontSize(10);
        pdf.setFont(undefined, 'normal');
        pdf.setTextColor(0, 0, 0);
        
        if (resultData.symptoms.length > 0) {
            resultData.symptoms.forEach((symptom, idx) => {
                if (yPosition > pageHeight - 30) {
                    pdf.addPage();
                    yPosition = margin;
                }
                const lines = pdf.splitTextToSize(`${idx + 1}. ${symptom}`, contentWidth - 5);
                pdf.text(lines, margin + 5, yPosition);
                yPosition += lines.length * 5 + 2;
            });
        } else {
            pdf.text('No symptoms information available', margin + 5, yPosition);
            yPosition += 5;
        }

        yPosition += 5;

        // Treatment Section
        if (yPosition > pageHeight - 50) {
            pdf.addPage();
            yPosition = margin;
        }

        pdf.setFontSize(12);
        pdf.setFont(undefined, 'bold');
        pdf.setTextColor(46, 125, 50);
        pdf.text('Recommended Treatment:', margin, yPosition);
        yPosition += 7;

        pdf.setFontSize(10);
        pdf.setFont(undefined, 'normal');
        pdf.setTextColor(0, 0, 0);
        
        if (resultData.treatments.length > 0) {
            resultData.treatments.forEach((treatment, idx) => {
                if (yPosition > pageHeight - 20) {
                    pdf.addPage();
                    yPosition = margin;
                }
                const lines = pdf.splitTextToSize(`${idx + 1}. ${treatment}`, contentWidth - 5);
                pdf.text(lines, margin + 5, yPosition);
                yPosition += lines.length * 5 + 2;
            });
        } else {
            pdf.text('No treatment information available', margin + 5, yPosition);
            yPosition += 5;
        }

        // Footer
        pdf.setFontSize(9);
        pdf.setTextColor(100, 100, 100);
        const footerY = pageHeight - 10;
        pdf.text('© 2025 BioAgriCure. All Rights Reserved.', pageWidth / 2, footerY, { align: 'center' });

        pdf.save(fileName);
        return true;
    }

    // Per-card download
    if (perCardButtons && perCardButtons.length) {
        perCardButtons.forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const idx = btn.getAttribute('data-index');
                const cards = Array.from(document.querySelectorAll('.result-card'));
                const card = cards[Number(idx)];
                if (!card) return alert('Result not found for download');

                btn.disabled = true;
                const originalText = btn.querySelector('svg') ? btn.innerHTML : btn.textContent;
                btn.textContent = 'Preparing...';
                
                try {
                    const resultData = extractResultData(card);
                    const fileName = `BioAgriCure_Result_${idx}_${Date.now()}.pdf`;
                    await generateTextPdf(resultData, fileName);
                    alert('Downloaded PDF successfully');
                } catch (err) {
                    console.error('Error downloading PDF:', err);
                    alert('Error downloading PDF. Please try again.');
                } finally {
                    btn.disabled = false;
                    btn.innerHTML = originalText || 'Download';
                }
            });
        });
    }

    // Download all results into a single text-based PDF (each result on its own page)
    if (saveAllBtn) {
        saveAllBtn.addEventListener('click', async () => {
            const { jsPDF } = window.jspdf;
            const pdf = new jsPDF('p', 'mm', 'a4');
            const cards = Array.from(document.querySelectorAll('.result-card'));
            if (!cards.length) return alert('No results to download');

            saveAllBtn.disabled = true;
            const originalText = saveAllBtn.querySelector('svg') ? saveAllBtn.innerHTML : saveAllBtn.textContent;
            saveAllBtn.textContent = 'Preparing...';

            try {
                for (let idx = 0; idx < cards.length; idx++) {
                    const card = cards[idx];
                    if (idx > 0) pdf.addPage();
                    const resultData = extractResultData(card);
                    
                    const pageWidth = pdf.internal.pageSize.getWidth();
                    const pageHeight = pdf.internal.pageSize.getHeight();
                    const margin = 15;
                    const contentWidth = pageWidth - (2 * margin);
                    let yPosition = margin;

                    // Header with title
                    pdf.setFillColor(46, 125, 50);
                    pdf.rect(0, 0, pageWidth, 25, 'F');
                    pdf.setTextColor(255, 255, 255);
                    pdf.setFontSize(18);
                    pdf.setFont(undefined, 'bold');
                    pdf.text('BioAgriCure', margin, 12);
                    pdf.setFontSize(11);
                    pdf.setFont(undefined, 'normal');
                    pdf.text('Plant Disease Detection Report', margin, 20);
                    
                    yPosition = 35;

                    // Add plant image if available
                    if (resultData.imageData) {
                        try {
                            const imgWidth = 80;
                            const imgHeight = 80;
                            const imgX = (pageWidth - imgWidth) / 2;
                            pdf.addImage(resultData.imageData, 'JPEG', imgX, yPosition, imgWidth, imgHeight);
                            yPosition += imgHeight + 10;
                        } catch (err) {
                            console.warn('Could not add image to PDF:', err);
                            yPosition += 10;
                        }
                    }

                    // Image filename and date
                    pdf.setTextColor(100, 100, 100);
                    pdf.setFontSize(10);
                    pdf.text(`Image: ${resultData.fileName}`, margin, yPosition);
                    yPosition += 6;
                    pdf.text(`Generated: ${new Date().toLocaleString()}`, margin, yPosition);
                    yPosition += 12;

                    // Disease Detection Section
                    pdf.setTextColor(0, 0, 0);
                    pdf.setFontSize(13);
                    pdf.setFont(undefined, 'bold');
                    pdf.text('Detected Disease:', margin, yPosition);
                    yPosition += 8;

                    pdf.setFontSize(14);
                    pdf.setTextColor(46, 125, 50);
                    pdf.text(resultData.diseaseName, margin, yPosition);
                    yPosition += 10;

                    // Confidence Score
                    pdf.setTextColor(0, 0, 0);
                    pdf.setFontSize(11);
                    pdf.setFont(undefined, 'bold');
                    pdf.text(`Confidence Score: ${resultData.confidence}`, margin, yPosition);
                    yPosition += 10;

                    // Symptoms Section
                    pdf.setFontSize(12);
                    pdf.setFont(undefined, 'bold');
                    pdf.setTextColor(46, 125, 50);
                    pdf.text('Symptoms:', margin, yPosition);
                    yPosition += 7;

                    pdf.setFontSize(10);
                    pdf.setFont(undefined, 'normal');
                    pdf.setTextColor(0, 0, 0);
                    
                    if (resultData.symptoms.length > 0) {
                        resultData.symptoms.forEach((symptom, symIdx) => {
                            if (yPosition > pageHeight - 50) {
                                pdf.addPage();
                                yPosition = margin;
                            }
                            const lines = pdf.splitTextToSize(`${symIdx + 1}. ${symptom}`, contentWidth - 5);
                            pdf.text(lines, margin + 5, yPosition);
                            yPosition += lines.length * 5 + 2;
                        });
                    } else {
                        pdf.text('No symptoms information available', margin + 5, yPosition);
                        yPosition += 5;
                    }

                    yPosition += 5;

                    // Treatment Section
                    if (yPosition > pageHeight - 50) {
                        pdf.addPage();
                        yPosition = margin;
                    }

                    pdf.setFontSize(12);
                    pdf.setFont(undefined, 'bold');
                    pdf.setTextColor(46, 125, 50);
                    pdf.text('Recommended Treatment:', margin, yPosition);
                    yPosition += 7;

                    pdf.setFontSize(10);
                    pdf.setFont(undefined, 'normal');
                    pdf.setTextColor(0, 0, 0);
                    
                    if (resultData.treatments.length > 0) {
                        resultData.treatments.forEach((treatment, tIdx) => {
                            if (yPosition > pageHeight - 20) {
                                pdf.addPage();
                                yPosition = margin;
                            }
                            const lines = pdf.splitTextToSize(`${tIdx + 1}. ${treatment}`, contentWidth - 5);
                            pdf.text(lines, margin + 5, yPosition);
                            yPosition += lines.length * 5 + 2;
                        });
                    } else {
                        pdf.text('No treatment information available', margin + 5, yPosition);
                        yPosition += 5;
                    }

                    // Footer
                    pdf.setFontSize(9);
                    pdf.setTextColor(100, 100, 100);
                    const footerY = pageHeight - 10;
                    pdf.text('© 2025 BioAgriCure. All Rights Reserved.', pageWidth / 2, footerY, { align: 'center' });
                }

                pdf.save(`BioAgriCure_All_Results_${Date.now()}.pdf`);
                alert('Downloaded combined PDF successfully');
            } catch (err) {
                console.error('Error generating combined PDF:', err);
                alert('Error generating combined PDF.');
            } finally {
                saveAllBtn.disabled = false;
                saveAllBtn.innerHTML = originalText || 'Download All';
            }
        });
    }
});
