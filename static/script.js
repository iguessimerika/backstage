// static/script.js

document.getElementById('addPlatformBtn').addEventListener('click', function() {
    console.log("Hier würde JavaScript per DOM-Manipulation ein weiteres URL-Input-Feld einfügen.");
});

const fileInput = document.getElementById('profilePicture');
const imagePreview = document.getElementById('imagePreview');

if (fileInput && imagePreview) { // Sicherheitsabfrage, ob Elemente auf der aktuellen Seite existieren
    fileInput.addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const imageUrl = URL.createObjectURL(file);
            imagePreview.src = imageUrl;
            imagePreview.style.display = 'block';
            imagePreview.onload = () => URL.revokeObjectURL(imagePreview.src);
        } else {
            imagePreview.src = '';
            imagePreview.style.display = 'none';
        }
    });
}