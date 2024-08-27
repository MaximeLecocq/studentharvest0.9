// Avatar Dropdown Toggle
const avatarButton = document.getElementById('avatarButton');
const avatarDropdown = document.getElementById('avatarDropdown');

avatarButton.addEventListener('click', () => {
    avatarDropdown.classList.toggle('hidden');
});

// Close dropdown when clicked outside
document.addEventListener('click', (e) => {
    if (!avatarButton.contains(e.target)) {
        avatarDropdown.classList.add('hidden');
    }
});
