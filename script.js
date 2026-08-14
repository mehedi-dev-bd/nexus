document.addEventListener("DOMContentLoaded", () => {
    
    const navItems = document.querySelectorAll('.nav-item');
    const panels = document.querySelectorAll('.setting-panel');
    const headerTitle = document.getElementById('current-section-title');

    // --- POS Tab Switching Logic ---
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // 1. Remove active state from all nav items
            navItems.forEach(nav => nav.classList.remove('active'));
            
            // 2. Add active state to clicked item
            this.classList.add('active');

            // 3. Update the Top Header Title based on the span text inside the nav item
            const sectionName = this.querySelector('span').innerText;
            headerTitle.innerText = sectionName;

            // 4. Hide all panels
            panels.forEach(panel => {
                panel.classList.remove('active');
            });

            // 5. Show targeted panel
            const targetId = this.getAttribute('data-target');
            const targetPanel = document.getElementById(targetId);
            
            if (targetPanel) {
                targetPanel.classList.add('active');
            } else {
                // If a panel isn't built yet, show a placeholder toast
                showToast(`Warning: UI module for ${sectionName} is under construction.`, 'warning');
            }
        });
    });
});

// --- Mock Save Functionality ---
function saveSettings() {
    const saveBtn = document.querySelector('.btn-save');
    const originalText = saveBtn.innerText;
    
    // Add visual loading state
    saveBtn.innerHTML = '<i class="fa-solid fa-circle-notch fa-spin"></i> Saving...';
    saveBtn.style.opacity = '0.8';
    saveBtn.disabled = true;

    // Simulate network request
    setTimeout(() => {
        // Reset button
        saveBtn.innerHTML = originalText;
        saveBtn.style.opacity = '1';
        saveBtn.disabled = false;
        
        // Show success notification
        showToast('Configuration saved successfully to Nexus database.', 'success');
    }, 1200);
}

// --- Toast Notification System ---
function showToast(message, type = 'success') {
    const container = document.getElementById('toast-container');
    
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    
    let icon = '<i class="fa-solid fa-check-circle" style="color: #10b981;"></i>'; // default success
    if (type === 'warning') {
        icon = '<i class="fa-solid fa-triangle-exclamation" style="color: #f59e0b;"></i>';
    }

    toast.innerHTML = `${icon} <span>${message}</span>`;
    
    container.appendChild(toast);

    // Remove toast after 3.5 seconds
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}