document.getElementById('contactForm').addEventListener('submit', function(e) {
  e.preventDefault();
  alert('Vaša správa bola odoslaná. Ďakujeme za kontakt!');
  this.reset();
});