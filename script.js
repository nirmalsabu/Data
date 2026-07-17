const button = document.getElementById('demoButton');
const status = document.getElementById('status');

button.addEventListener('click', () => {
  status.textContent = 'The button was clicked. You can now start building your app.';
});
