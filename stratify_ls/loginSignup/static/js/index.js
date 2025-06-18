console.log('test');

document.addEventListener("DOMContentLoaded", function () {
    const categorySelect = document.querySelector(".categor");
    const reputationSelect = document.querySelector(".repu");
    const formButton = document.querySelector(".filterSubmit");

    
    

    categorySelect.addEventListener("change", () => {
        console.log(categorySelect);
        formButton.click();
    });

    reputationSelect.addEventListener("change", () => {
        console.log(reputationSelect);
        formButton.click();
    });
});