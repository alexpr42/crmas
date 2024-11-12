// scripts.js

// Example: Confirmation for deleting a lead or deal
function confirmDeletion(itemType) {
    return confirm(`Are you sure you want to delete this ${itemType}?`);
}

// Example: Automatic renewal date alert (for custom enhancements)
document.addEventListener("DOMContentLoaded", function () {
    const renewalAlert = document.getElementById("renewal-alert");
    if (renewalAlert) {
        alert("Reminder: Some deals are approaching their renewal date.");
    }
});