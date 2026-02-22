document.querySelectorAll('.counter').forEach((el) => {
  const target = parseInt(el.dataset.value || '0', 10);
  let value = 0;
  const step = Math.max(1, Math.ceil(target / 20));
  const interval = setInterval(() => {
    value += step;
    if (value >= target) { value = target; clearInterval(interval); }
    el.textContent = value;
  }, 35);
});

const searchInput = document.getElementById('searchInput');
if (searchInput) {
  searchInput.addEventListener('input', () => {
    if (searchInput.value.length === 0 || searchInput.value.length >= 2) {
      searchInput.form.submit();
    }
  });
}
