document.addEventListener('DOMContentLoaded', () => {
    // 讓警告訊息在 5 秒後自動消失
    const alerts = document.querySelectorAll('.alert:not(.alert-important)');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });
});
