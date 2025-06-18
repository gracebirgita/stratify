document.addEventListener('DOMContentLoaded', function () {
    console.log('EditProfile Loaded...');
    const inputProfile = document.getElementById('profile-upload');
    const inputBackground = document.getElementById('bg-upload');

    const fileNameSpanProfile = inputProfile?.parentElement.querySelector('.file-name');
    const fileNameSpanBackground = inputBackground?.parentElement.querySelector('.file-name');

    const clearBtnProfile = document.querySelector('.clear-profile');
    const clearBtnBackground = document.querySelector('.clear-bg');

    const profileImagePreview = document.getElementById('profileImagePreview');
    const bgImagePreview = document.getElementById('bgImagePreview');

    clearBtnProfile.style.display = 'none';
    clearBtnBackground.style.display = 'none';

    // Update file name when file is selected
    inputProfile?.addEventListener('change', function () {
    const fileName = inputProfile.files.length > 0 ? inputProfile.files[0].name : 'No file chosen';
    fileNameSpanProfile.textContent = fileName;
    });

    inputBackground?.addEventListener('change', function () {
    const fileName = inputBackground.files.length > 0 ? inputBackground.files[0].name : 'No file chosen';
    fileNameSpanBackground.textContent = fileName;
    });

    // Show profile preview
    inputProfile?.addEventListener('change', () => {
    const file = inputProfile.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
        profileImagePreview.src = e.target.result;
        profileImagePreview.style.display = 'block';
        clearBtnProfile.style.display = 'inline-block';
        };
        reader.readAsDataURL(file);
    }
    });

    // Show background preview
    inputBackground?.addEventListener('change', () => {
    const file = inputBackground.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
        bgImagePreview.src = e.target.result;
        bgImagePreview.style.display = 'block';
        clearBtnBackground.style.display = 'inline-block';
        };
        reader.readAsDataURL(file);
    }
    });


    // Clear profile
    clearBtnProfile?.addEventListener('click', function () {
    if (profileImagePreview.style.display !== 'none') {
        inputProfile.value = '';
        // profileImagePreview.src = '';
        profileImagePreview.style.display = 'none';
        fileNameSpanProfile.textContent = 'No file chosen';
    }
    });

    // Clear background
    clearBtnBackground?.addEventListener('click', function () {
    if (bgImagePreview.style.display !== 'none') {
        inputBackground.value = '';
        // bgImagePreview.src = '';
        bgImagePreview.style.display = 'none';
        fileNameSpanBackground.textContent = 'No file chosen';
    }
    });

});